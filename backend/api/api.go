package api

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"
	"vision-web-scraper/backend/kg" // Added for Neo4j service
	"vision-web-scraper/backend/parser"
)

type ExtractRequest struct {
	URL      string `json:"url"`
	PageType string `json:"type"` // "product" or "article"
}

// ExtractHandler now accepts a Neo4jService instance
func ExtractHandler(w http.ResponseWriter, r *http.Request, kgService *kg.Neo4jService) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST method is allowed", http.StatusMethodNotAllowed)
		return
	}

	var req ExtractRequest
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		http.Error(w, fmt.Sprintf("Error decoding request body: %v", err), http.StatusBadRequest)
		return
	}

	if req.URL == "" {
		http.Error(w, "URL is required", http.StatusBadRequest)
		return
	}
	if req.PageType == "" {
		http.Error(w, "Page type ('type') is required (e.g., 'product', 'article')", http.StatusBadRequest)
		return
	}

	extractedData, err := parser.ParsePage(req.URL, req.PageType)
	if err != nil {
		fmt.Printf("Error calling ParsePage: %v\n", err)
		http.Error(w, fmt.Sprintf("Error processing page: %v", err), http.StatusInternalServerError)
		return
	}

	// Save to Neo4j if it's a product
	if req.PageType == "product" && extractedData != nil {
		err := kgService.SaveProduct(
			extractedData.ProductName,
			extractedData.Price,
			extractedData.Currency,
			extractedData.SourceURL,
			extractedData.Images,
			extractedData.Attributes,
		)
		if err != nil {
			// Log this error, but don't fail the whole API request
			fmt.Printf("Error saving product to Neo4j: %v\n", err)
			// Depending on requirements, you might want to inform the client,
			// but for now, we just log it and continue.
		}
	}
	// TODO: Add similar for Article if SaveArticle is implemented in kgService

	responsePayload := make(map[string]interface{})
	if req.PageType == "product" {
		productData := map[string]interface{}{
			"name":       extractedData.ProductName,
			"price":      extractedData.Price,
			"currency":   extractedData.Currency,
			"images":     extractedData.Images,
			"attributes": extractedData.Attributes,
		}
		responsePayload["product"] = productData
	} else if req.PageType == "article" {
		responsePayload["article"] = map[string]interface{}{
			"title": extractedData.ArticleTitle,
			"text":  extractedData.ArticleText,
		}
	} else {
		responsePayload["data"] = extractedData
	}

	responsePayload["metadata"] = map[string]interface{}{
		"confidence": 0.92, // Placeholder
		"source":     req.URL,
		"timestamp":  time.Now().Format(time.RFC3339),
	}

	w.Header().Set("Content-Type", "application/json")
	err = json.NewEncoder(w).Encode(responsePayload)
	if err != nil {
		fmt.Printf("Error encoding response: %v\n", err)
	}
}

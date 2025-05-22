package kg

import (
	"fmt"
	"os"
	"time"
	// Official Neo4j Go driver
	"github.com/neo4j/neo4j-go-driver/v4/neo4j"
)

// Neo4jService handles interactions with the Neo4j database.
type Neo4jService struct {
	Driver neo4j.Driver
}

// NewNeo4jService creates a new Neo4jService.
// Reads URI, user, pass from environment variables (NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
func NewNeo4jService() (*Neo4jService, error) {
	uri := os.Getenv("NEO4J_URI")
	user := os.Getenv("NEO4J_USER")
	pass := os.Getenv("NEO4J_PASSWORD")

	if uri == "" {
		uri = "neo4j://localhost:7687" // Default if not set
		fmt.Println("NEO4J_URI not set, using default:", uri)
	}
	if user == "" {
		user = "neo4j" // Default
		fmt.Println("NEO4J_USER not set, using default:", user)
	}
	if pass == "" {
		pass = "password" // Default (as in docker-compose.yml)
		fmt.Println("NEO4J_PASSWORD not set, using default (not recommended for production):", pass)
	}

	driver, err := neo4j.NewDriver(uri, neo4j.BasicAuth(user, pass, ""))
	if err != nil {
		return nil, fmt.Errorf("could not create neo4j driver: %w", err)
	}
	// TODO: Check connectivity with driver.VerifyConnectivity() here or in main

	return &Neo4jService{Driver: driver}, nil
}

// Close handles closing the Neo4j driver.
func (s *Neo4jService) Close() {
	if s.Driver != nil {
		s.Driver.Close()
	}
}

// SaveProduct saves extracted product data to Neo4j.
// Takes relevant fields from parser.ExtractedData.
func (s *Neo4jService) SaveProduct(productName, price, currency, url string, images []string, attributes map[string]string) error {
	session := s.Driver.NewSession(neo4j.SessionConfig{AccessMode: neo4j.AccessModeWrite})
	defer session.Close()

	_, err := session.WriteTransaction(func(transaction neo4j.Transaction) (interface{}, error) {
		// Using MERGE to create or update product based on URL
		query := `
			MERGE (p:Product {url: $url})
			ON CREATE SET p.name = $name, p.price = $price, p.currency = $currency, p.images = $images, p.attributes = $attributes, p.extracted_at = datetime($extracted_at)
			ON MATCH SET p.name = $name, p.price = $price, p.currency = $currency, p.images = $images, p.attributes = $attributes, p.extracted_at = datetime($extracted_at)
			RETURN p.name`
		
		// Convert attributes map to JSON string for storage if your driver/Neo4j version requires it
		// For simplicity, Neo4j 4.x+ often handles maps directly. If not, serialize 'attributes'.
        // For now, let's assume attributes can be passed as a map.
        // If attributes map causes issues, serialize it to a JSON string:
        // attributesJson, _ := json.Marshal(attributes)

		parameters := map[string]interface{}{
			"url":          url,
			"name":         productName,
			"price":        price,
			"currency":     currency,
			"images":       images,        // Ensure this is a list of strings
			"attributes":   attributes,    // Ensure this is a map[string]string or compatible
			"extracted_at": time.Now().Format(time.RFC3339),
		}
		
		_, err := transaction.Run(query, parameters)
		return nil, err
	})

	if err != nil {
		return fmt.Errorf("failed to save product to Neo4j: %w", err)
	}
	fmt.Printf("Placeholder: Product data for %s (URL: %s) would be saved to Neo4j.\n", productName, url)
	return nil
}
// Add SaveArticle function similarly if time permits.

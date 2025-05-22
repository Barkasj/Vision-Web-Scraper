package main

import (
	"fmt"
	"log"
	"net/http"
	"vision-web-scraper/backend/api"
	"vision-web-scraper/backend/kg" // Added for Neo4j service
)

func main() {
	fmt.Println("Backend service starting...")

	// Initialize Neo4j Service
	neo4jService, err := kg.NewNeo4jService()
	if err != nil {
		log.Fatalf("Failed to initialize Neo4j service: %v", err)
	}
	defer neo4jService.Close()

	// Optional: Verify Neo4j Connectivity
	// Note: For Neo4j Go Driver v4, VerifyConnectivity is part of the Driver interface.
	// For v5, it might be driver.VerifyConnectivity(context.Background())
	if err := neo4jService.Driver.VerifyConnectivity(); err != nil {
		log.Fatalf("Failed to verify Neo4j connectivity: %v", err)
	}
	fmt.Println("Successfully connected to Neo4j (or at least driver initialized).")

	mux := http.NewServeMux()
	// Pass neo4jService to the handler using a closure
	mux.HandleFunc("/api/v1/extract", func(w http.ResponseWriter, r *http.Request) {
		api.ExtractHandler(w, r, neo4jService) // Pass the service instance
	})

	port := "8080" // This should ideally be configurable
	fmt.Printf("Starting HTTP server on port %s\n", port)
	fmt.Println("Listening on endpoint: /api/v1/extract (POST)")

	err = http.ListenAndServe(":"+port, mux)
	if err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}

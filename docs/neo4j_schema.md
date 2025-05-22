# Neo4j Schema for Vision-Web-Scraper

## Node Labels

### Product
- **Label:** `Product`
- **Properties:**
    - `name`: STRING (Name of the product)
    - `price`: STRING (Price of the product, consider FLOAT for actual implementation)
    - `currency`: STRING (Currency code, e.g., "IDR", "USD")
    - `url`: STRING (Source URL of the product page, unique identifier)
    - `extracted_at`: DATETIME (Timestamp of when the data was extracted)
    - `attributes`: STRING (Serialized JSON map of product attributes)
    - `images`: LIST<STRING> (List of image URLs)

### Article
- **Label:** `Article`
- **Properties:**
    - `title`: STRING (Title of the article)
    - `url`: STRING (Source URL of the article page, unique identifier)
    - `extracted_at`: DATETIME (Timestamp of when the data was extracted)
    - `text_snippet`: STRING (A short snippet of the article text, if available)

## Relationships (Examples for future extension)

- `(Product)-[:HAS_BRAND]->(Brand)`
- `(Product)-[:SOLD_BY]->(Seller)`
- `(Product)-[:IN_CATEGORY]->(Category)`
- `(Article)-[:MENTIONS]->(Entity)`

## Indexes (Recommended)

- Create unique constraint on `Product(url)`
- Create unique constraint on `Article(url)`
- Create index on `Product(name)`
- Create index on `Article(title)`

# CSV Product Search API

A lightweight MCP (Model Context Protocol) server built with **FastMCP** for searching products from a CSV catalog and checking inventory availability.

This project demonstrates how to expose CSV-backed product search tools through MCP with built-in validation, timeout handling, and error recovery.

---

## Features

- Search products by keyword
- Filter products by maximum price
- Limit number of returned results
- Check inventory status for a specific product
- Async MCP tool implementation
- Timeout protection for long-running requests
- Graceful handling for:
  - missing CSV file
  - invalid input
  - empty search results
  - unexpected runtime failures

---

## Project Structure

```bash
csv-product-search/
│
├── product_server.py
├── products.csv
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Requirements

- Python 3.10+
- uv
- FastMCP
- pandas

Install **uv** if you don’t already have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or on macOS:

```bash
brew install uv
```

Verify installation:

```bash
uv --version
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/csv-product-search.git
cd csv-product-search
```

Create a virtual environment:

```bash
uv venv
```

Activate it:

**macOS/Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
uv add fastmcp pandas
```

Or install from lockfile:

```bash
uv sync
```

---

## Product Catalog Format

The application expects a `products.csv` file in the project root.

Example:

```csv
id,title,price,available
1,Wireless Mouse,29.99,True
2,Mechanical Keyboard,89.99,True
3,USB-C Hub,45.50,False
4,Laptop Stand,39.99,True
```

### Required Columns

| Column | Type | Description |
|--------|------|-------------|
| id | integer | Unique product identifier |
| title | string | Product name |
| price | float | Product price |
| available | boolean | Product stock availability |

---

## Running the Server

Start the MCP server:

```bash
uv run python app.py
```

If `products.csv` is missing:

```text
products.csv not found - using empty catalog
```

The server will still run with an empty product catalog.

---

## Available Tools

## search_products

Search for available products matching a keyword.

### Parameters

| Parameter | Type | Required | Description |
|----------|------|----------|-------------|
| query | string | Yes | Search term |
| max_price | float | No | Maximum allowed price |
| limit | integer | No | Maximum number of results (default: 5, max: 50) |

### Example

```python
await search_products("keyboard", max_price=100, limit=3)
```

### Example Response

```json
{
  "success": true,
  "error": null,
  "message": "Found 1 product(s) matching 'keyboard'.",
  "results": [
    {
      "id": 2,
      "title": "Mechanical Keyboard",
      "price": 89.99,
      "available": true
    }
  ],
  "total_matches": 1
}
```

### Validation Rules

- Query cannot be empty
- `max_price` must be greater than zero
- `limit` is clamped between 1 and 50

### Timeout Protection

`search_products` includes timeout protection:

```python
@with_timeout(5.0)
```

Timeout response:

```json
{
  "success": false,
  "error": "timeout",
  "message": "Request timed out after 5.0 seconds.",
  "results": []
}
```

---

## check_inventory

Check inventory for a specific product ID.

### Parameters

| Parameter | Type | Required | Description |
|----------|------|----------|-------------|
| product_id | integer | Yes | Product identifier |

### Example

```python
await check_inventory(1)
```

### Example Response

```json
{
  "success": true,
  "found": true,
  "product": {
    "id": 1,
    "title": "Wireless Mouse",
    "price": 29.99,
    "available": true,
    "status": "In Stock"
  }
}
```

Invalid product example:

```json
{
  "success": true,
  "found": false,
  "message": "No product found with ID 99."
}
```

---

## Development

Run directly:

```bash
uv run python app.py
```

Add dependencies:

```bash
uv add package-name
```

Remove dependencies:

```bash
uv remove package-name
```

Update dependencies:

```bash
uv lock --upgrade
```

Sync environment:

```bash
uv sync
```

---

## Error Handling

The application gracefully handles:

- Missing CSV file
- Invalid product IDs
- Invalid price filters
- Empty queries
- Search failures
- Timeout failures

Logging is enabled using Python’s built-in logging:

```python
logger = logging.getLogger(__name__)
```

---

## Future Improvements

Potential enhancements:

- fuzzy product matching
- category filtering
- pagination
- stock quantity tracking
- SQLite/PostgreSQL backend
- sorting support
- caching
- authentication
- unit/integration tests
- Docker support

---

## Example Use Cases

Useful for:

- AI shopping assistants
- MCP demos
- chatbot product lookup
- inventory assistants
- product recommendation agents

---

## License

MIT License

---

## Author
By: Abby Nyakara 
Built with FastMCP, Python, and uv
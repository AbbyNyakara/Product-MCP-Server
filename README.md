# CSV Product Search API

A lightweight MCP (Model Context Protocol) server built with **FastMCP** for searching products from a CSV catalog and checking inventory availability.

This project demonstrates how to expose CSV-backed product search tools through MCP with built-in validation, timeout handling, and error recovery.

---

## Features

- Search products by keyword
- Filter products by maximum price
- Limit number of returned results
- Check inventory status for a specific product
- Graceful handling for:
  - missing CSV file
  - invalid input
  - empty search results
  - timeouts
  - unexpected runtime errors

---

## Project Structure

```bash
product_mcp_server/
│
├── products.csv          # Product catalog
├── product_server.py               # FastMCP server implementation
├── README.md
└── pyproject.toml
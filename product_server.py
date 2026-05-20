from fastmcp import FastMCP
import pandas as pd
import logging
from typing import Optional
import asyncio
from functools import wraps

app = FastMCP("CSV Product Search")
logger = logging.getLogger(__name__)

# Load with error handling
try:
    PRODUCTS_DF = pd.read_csv("products.csv")
except FileNotFoundError:
    logger.error("products.csv not found - using empty catalog")
    PRODUCTS_DF = pd.DataFrame(columns=["id", "title", "price", "available"])


def with_timeout(seconds: float):
    """Decorator to add timeout to async tool functions."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(
                    func(*args, **kwargs), 
                    timeout=seconds
                )
            except asyncio.TimeoutError:
                return {
                    "success": False,
                    "error": "timeout",
                    "message": f"Request timed out after {seconds} seconds.",
                    "results": []
                }
        return wrapper
    return decorator

@app.tool()
@with_timeout(5.0)
async def search_products(query: str, 
                          max_price: Optional[float] = None, 
                          limit: int = 5) -> dict:
    """
    Search the product catalog.
    Returns products matching the query, filtered by price and availability.
    """
    # Validate inputs
    if not query or not query.strip():
        return {
            "success": False,
            "error": "empty_query",
            "message": "Please provide a search term.",
            "results": []
        }
    

    if max_price is not None and max_price <= 0:
        return {
            "success": False,
            "error": "invalid_price",
            "message": "Price must be greater than zero.",
            "results": []
        }
    

    if limit < 1 or limit > 50:
        limit = min(max(limit, 1), 50)  # Clamp to valid range


    try:
        df = PRODUCTS_DF.copy()
        
        # Search for matches
        query_clean = query.strip().lower()
        df = df[df["title"].str.lower().str.contains(query_clean, na=False)]
        
        # Apply filters
        if max_price is not None:
            df = df[df["price"] <= max_price]
        
        df = df[df["available"] == True]
        
        #Check for empty results
        if df.empty:
            return {
                "success": True,
                "error": None,
                "message": f"No available products found matching '{query}'.",
                "results": [],
                "suggestion": "Try broader search terms or remove the price filter."
            }
        
        # Return successful results
        results = df.head(limit).to_dict(orient="records")
        
        return {
            "success": True,
            "error": None,
            "message": f"Found {len(results)} product(s) matching '{query}'.",
            "results": results,
            "total_matches": len(df)
        }
        
    except Exception as e:
        logger.exception(f"Search failed for query: {query}")
        return {
            "success": False,
            "error": "search_failed",
            "message": "Product search is temporarily unavailable. Please try again.",
            "results": []
        }



@app.tool()
async def check_inventory(product_id: int) -> dict:
    """
    Check inventory status for a specific product.
    Returns availability, price, and stock information.
    """

    if product_id < 1:
        return {
            "success": False,
            "error": "invalid_id",
            "message": "Product ID must be a positive number."
        }

    try:
        df = PRODUCTS_DF[PRODUCTS_DF["id"] == product_id]

        if df.empty:
            return {
                "success": True,
                "found": False,
                "message": f"No product found with ID {product_id}."
            }

        product = df.iloc[0]

        return {
            "success": True,
            "found": True,
            "product": {
                "id": int(product["id"]),
                "title": product["title"],
                "price": float(product["price"]),
                "available": bool(product["available"]),
                "status": "In Stock" if product["available"] else "Out of Stock"
            }
        }

    except Exception as e:
        logger.exception(f"Inventory check failed for product {product_id}")
        return {
            "success": False,
            "error": "lookup_failed",
            "message": "Could not check inventory. Please try again."
        }

if __name__ == "__main__":
    app.run()

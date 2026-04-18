# tools.py - Fixed version with real data sources

from app.scrapper import scrape_amazon, scrape_flipkart
import requests
import time
from typing import List, Dict, Optional
import random

# Cache to avoid repeated scraping
_search_cache = {}
CACHE_TTL = 300  # 5 minutes

def search_products(query: str, source: str = "amazon") -> List[Dict]:
    """
    Search products from multiple sources with caching
    """
    cache_key = f"{query}_{source}"
    
    # Check cache
    if cache_key in _search_cache:
        cached_data, timestamp = _search_cache[cache_key]
        if time.time() - timestamp < CACHE_TTL:
            print(f"📦 Returning cached results for '{query}'")
            return cached_data
    
    products = []
    
    # Try primary source
    if source == "amazon":
        products = scrape_amazon(query)
    
    # Fallback to Flipkart if Amazon fails
    if not products:
        print(f"⚠️ Amazon failed, trying Flipkart for '{query}'")
        products = scrape_flipkart(query)
    
    # Final fallback: Use SerpAPI (requires API key)
    if not products:
        print(f"⚠️ Both scrapers failed, using SerpAPI for '{query}'")
        products = search_serpapi(query)
    
    # Last resort: Return mock data with warning
    if not products:
        print(f"❌ All sources failed for '{query}', using mock data")
        products = get_mock_results(query)
    
    # Cache results
    _search_cache[cache_key] = (products, time.time())
    
    return products

def search_serpapi(query: str) -> List[Dict]:
    """
    Use SerpAPI as reliable fallback (requires free API key)
    Sign up at https://serpapi.com/
    """
    api_key = "YOUR_SERPAPI_KEY"  # Move to environment variables
    url = "https://serpapi.com/search"
    
    params = {
        "api_key": "02ec5fba4bd4c4cc96a8100b9797cbefff8c67b440133792d9956cf1405017d5",
        "engine": "amazon_product",
        "q": query,
        "amazon_domain": "amazon.in"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        products = []
        for item in data.get("organic_results", [])[:5]:
            products.append({
                "title": item.get("title", "Unknown"),
                "price": parse_price(item.get("price", "₹0")),
                "rating": float(item.get("rating", "0")) if item.get("rating") else 0.0,
                "source": "SerpAPI"
            })
        return products
    except Exception as e:
        print(f"SerpAPI error: {e}")
        return []

def get_mock_results(query: str) -> List[Dict]:
    """
    Context-aware mock data for demo purposes
    """
    query_lower = query.lower()
    
    # Categorized mock data
    mock_database = {
        "laptop": [
            {"title": "HP Pavilion 15", "price": 72000, "rating": 4.3},
            {"title": "Lenovo IdeaPad Slim 5", "price": 68000, "rating": 4.2},
            {"title": "Dell Inspiron 14", "price": 75000, "rating": 4.4},
        ],
        "phone": [
            {"title": "iPhone 15", "price": 79900, "rating": 4.7},
            {"title": "Samsung Galaxy S24", "price": 69999, "rating": 4.5},
            {"title": "Google Pixel 8", "price": 64999, "rating": 4.6},
        ],
        "shoes": [
            {"title": "Nike Air Max", "price": 8999, "rating": 4.5},
            {"title": "Adidas Ultraboost", "price": 11999, "rating": 4.6},
            {"title": "Puma Running Shoes", "price": 4999, "rating": 4.3},
        ]
    }
    
    # Find matching category
    for category, products in mock_database.items():
        if category in query_lower:
            return products
    
    # Default fallback
    return [
        {"title": f"Top {query} - Premium", "price": 10000, "rating": 4.5},
        {"title": f"Best {query} - Standard", "price": 5000, "rating": 4.0},
        {"title": f"{query} - Budget", "price": 2000, "rating": 3.5},
    ]

def parse_price(price_str: str) -> float:
    """Extract numeric price from string like '₹72,000' or '$999'"""
    import re
    numbers = re.findall(r'\d+', price_str.replace(',', ''))
    return float(numbers[0]) if numbers else 0.0

def rank_products(products: List[Dict]) -> List[Dict]:
    """
    Improved ranking logic with normalized scoring
    """
    if not products:
        return []
    
    # Find price range for normalization
    prices = [p.get("price", 0) for p in products if p.get("price", 0) > 0]
    if not prices:
        return products
    
    min_price = min(prices)
    max_price = max(prices)
    
    for p in products:
        # Normalize price (0 to 1, where lower price = higher score)
        if max_price > min_price:
            price_score = 1 - ((p["price"] - min_price) / (max_price - min_price))
        else:
            price_score = 0.5
        
        # Normalize rating (0 to 1)
        rating_score = p.get("rating", 0) / 5.0
        
        # Weighted combination (adjust weights as needed)
        # 70% rating, 30% price for quality-focused shopping
        p["score"] = (rating_score * 0.7) + (price_score * 0.3)
        
        # Add value rating
        p["value_rating"] = "Excellent" if p["score"] > 0.8 else "Good" if p["score"] > 0.6 else "Average"
    
    return sorted(products, key=lambda x: x["score"], reverse=True)
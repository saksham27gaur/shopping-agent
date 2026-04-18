from app.scrapper import scrape_amazon
import requests

# def search_products(query):
#     return scrape_amazon(query)

def search_products(query):
    # (use mock or API for now)
    return [
        {"title": "HP Pavilion 15", "price": 72000, "rating": 4.3},
        {"title": "Lenovo IdeaPad Slim 5", "price": 68000, "rating": 4.2},
        {"title": "Dell Inspiron 14", "price": 75000, "rating": 4.4},
    ]

def rank_products(products):
    # simple scoring logic
    for p in products:
        p["score"] = (p["rating"] * 2) + (100000 / (p["price"] + 1))

    return sorted(products, key=lambda x: x["score"], reverse=True)

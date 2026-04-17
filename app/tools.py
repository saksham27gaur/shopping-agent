from app.scrapper import scrape_amazon

def search_products(query):
    return scrape_amazon(query)


def rank_products(products):
    # simple scoring logic
    for p in products:
        p["score"] = (p["rating"] * 2) + (100000 / (p["price"] + 1))

    return sorted(products, key=lambda x: x["score"], reverse=True)

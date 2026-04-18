import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_amazon(query):
    url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    products = []

    for item in soup.select(".s-result-item")[:5]:
        try:
            title = item.select_one("h2 span").text
            price = item.select_one(".a-price-whole").text.replace(",", "")
            rating = item.select_one(".a-icon-alt").text.split()[0]

            products.append({
                "title": title,
                "price": float(price),
                "rating": float(rating)
            })
        except:
            continue

    return products

def scrape_flipkart(query: str) -> list:
    """
    Scrape Flipkart as fallback when Amazon fails
    """
    url = f"https://www.flipkart.com/search?q={query.replace(' ', '%20')}"
    
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        ]),
        "Accept-Language": "en-IN,en-GB;q=0.9,en;q=0.8",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        products = []
        items = soup.select("._1AtVbE")[:5]  # Flipkart product card selector
        
        for item in items:
            try:
                title_elem = item.select_one("._4rR01T")
                price_elem = item.select_one("._30jeq3")
                rating_elem = item.select_one(".gUuXy-")
                
                if title_elem and price_elem:
                    price_text = price_elem.text.replace("₹", "").replace(",", "")
                    products.append({
                        "title": title_elem.text,
                        "price": float(price_text),
                        "rating": float(rating_elem.text) if rating_elem else 0.0,
                        "source": "Flipkart"
                    })
            except:
                continue
        
        return products
    except Exception as e:
        print(f"Flipkart scraping failed: {e}")
        return []
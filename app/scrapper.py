import requests
from bs4 import BeautifulSoup

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

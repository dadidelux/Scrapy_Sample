import requests
import json
import csv
import time

# Set realistic browser headers
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.6367.91 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.alo.com/",
    "Origin": "https://www.alo.com",
    "Connection": "keep-alive"
}

url = "https://product-service.alo.software/graphql"

def fetch_products(offset):
    variables = {
        "handle": "accessories-shop-all",
        "offset": offset,
        "limit": 15,
        "sortKey": "DEFAULT",
        "filters": [],
        "countryCode": "US"
    }

    payload = {
        "operationName": "GetCollectionData",
        "variables": variables,
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "1647816df62eafdb2ef8305209f54c5c24a715ee12af8e0a86721913abb10dd1"
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

all_products = []
offset = 0

while True:
    print(f"🔄 Fetching offset {offset}...")
    data = fetch_products(offset)

    items = data.get("data", {}).get("collection", {}).get("products", {}).get("items", [])
    if not items:
        print("✅ No more products.")
        break

    for item in items:
        node = item.get("product")
        if node:
            all_products.append({
                "title": node.get("title"),
                "price": node.get("priceRange", {}).get("minVariantPrice", {}).get("amount"),
                "image": node.get("media", [{}])[0].get("previewImage", {}).get("url"),
                "handle": node.get("handle")
            })

    offset += 15
    time.sleep(0.5)  # Respectful delay

# Save to CSV
with open("alo/json/alo_accessories.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "image", "handle"])
    writer.writeheader()
    writer.writerows(all_products)

print(f"✅ Saved {len(all_products)} accessories to alo_accessories.csv")

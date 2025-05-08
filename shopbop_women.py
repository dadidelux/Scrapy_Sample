import requests
import json
import time

BASE_URL = "https://api.shopbop.com/public/products"
PARAMS = {
    "siteId": "1000",
    "lang": "en-PH",
    "currency": "USD",
    "categoryId": "13266", # Women's category ID
    "facetAllowList": "C",
    "limit": 100,
    "includeFacets": "true",
    "allowOutOfStockItems": "false",
    "disableSiteEligibilityFiltering": "true",
    "imageStrategy": "Q_ASPECT",
}

all_products = []
offset = 0

while True:
    PARAMS["offset"] = offset
    response = requests.get(BASE_URL, params=PARAMS)
    
    if response.status_code != 200:
        print(f"Failed at offset {offset}: Status {response.status_code}")
        break

    data = response.json()
    items = data.get("products", [])
    
    if not items:
        print("No more products to fetch.")
        break

    all_products.extend(items)
    print(f"Fetched {len(items)} items at offset {offset}")
    
    offset += PARAMS["limit"]
    time.sleep(0.5)  # Be kind to their server

# Save to file
with open("shopbop_products.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, ensure_ascii=False, indent=2)

print(f"Total items downloaded: {len(all_products)}")

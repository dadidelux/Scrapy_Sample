import requests
import json
import time

BASE_URL = "https://api.shopbop.com/public/products"
PARAMS = {
    "siteId": "1000",
    "lang": "en-PH",
    "currency": "USD",
    "categoryId": "2",  # MEN'S CATEGORY
    "facetAllowList": "C",
    "limit": 100,
    "includeFacets": "true",
    "allowOutOfStockItems": "false",
    "disableSiteEligibilityFiltering": "true",
    "imageStrategy": "Q_ASPECT"
}

all_products = []
offset = 0

print("⏳ Downloading men's products from Shopbop...")

while True:
    PARAMS["offset"] = offset
    response = requests.get(BASE_URL, params=PARAMS)

    if response.status_code != 200:
        print(f"❌ Failed at offset {offset}: HTTP {response.status_code}")
        break

    data = response.json()
    items = data.get("products", [])

    if not items:
        print("✅ No more products to fetch.")
        break

    all_products.extend(items)
    print(f"✅ Fetched {len(items)} products at offset {offset}")
    
    offset += PARAMS["limit"]
    time.sleep(0.5)  # Be polite to the API

# Save all products to JSON
with open("shopbop_mens_products.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, ensure_ascii=False, indent=2)

print(f"🎉 Done! Total items downloaded: {len(all_products)}")

import requests
import json
import time

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

base_url = "https://product-service.alo.software/graphql"
query_params = {
    "opName": "GetCollectionData",
    "operationName": "GetCollectionData",
    "extensions": json.dumps({
        "persistedQuery": {
            "version": 1,
            "sha256Hash": "1647816df62eafdb2ef8305209f54c5c24a715ee12af8e0a86721913abb10dd1"
        }
    }),
}

def fetch_page(offset=0, limit=15):
    variables = {
        "handle": "womens-shop-all",
        "offset": offset,
        "limit": limit,
        "sortKey": "DEFAULT",
        "filters": [],
        "countryCode": "PH"
    }

    query_params["variables"] = json.dumps(variables)
    response = requests.get(base_url, headers=headers, params=query_params)
    return response.json()

# Accumulate all products
all_products = []
offset = 0
limit = 15
max_products = 1455  # total products listed on site

while offset < max_products:
    print(f"🔄 Fetching offset {offset}...")
    data = fetch_page(offset=offset, limit=limit)

    try:
        nodes = data["data"]["productsByCollectionHandle"]["products"]["nodes"]
        if not nodes:
            print("No more products returned. Ending early.")
            break

        all_products.extend(nodes)
        offset += limit
        time.sleep(1)  # be kind to the server

    except Exception as e:
        print(f"❌ Error at offset {offset}: {e}")
        with open("debug_last_error.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        break

# Save to JSON
with open("alo_yoga_products.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, ensure_ascii=False, indent=2)

print(f"✅ Done! Saved {len(all_products)} products to alo_yoga_products.json")

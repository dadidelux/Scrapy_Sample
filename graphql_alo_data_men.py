import requests
import json
import time
import os

headers = {
    "Content-Type": "application/json",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.6367.91 Safari/537.36"
    )
}

base_url = "https://product-service.alo.software/graphql"
hash_version = {
    "version": 1,
    "sha256Hash": "1647816df62eafdb2ef8305209f54c5c24a715ee12af8e0a86721913abb10dd1"
}

query_params = {
    "opName": "GetCollectionData",
    "operationName": "GetCollectionData",
    "extensions": json.dumps({
        "persistedQuery": hash_version
    }),
}

def fetch_page(offset=0, limit=15):
    variables = {
        "handle": "mens-shop-all",  # ← changed from mens-shop-all
        "offset": offset,
        "limit": limit,
        "sortKey": "DEFAULT",
        "filters": [],
        "countryCode": "US"
    }

    query_params["variables"] = json.dumps(variables)
    response = requests.get(base_url, headers=headers, params=query_params)
    return response

# Ensure error log folder
os.makedirs("graphql_error_logs", exist_ok=True)

# Accumulate all products
all_products = []
offset = 0
limit = 15
max_products = 1000  # adjust as needed

while True:
    print(f"🔄 Fetching offset {offset}...")
    response = fetch_page(offset=offset, limit=limit)

    try:
        if response.status_code != 200:
            raise Exception(f"Non-200 status code: {response.status_code}")

        data = response.json()

        if "errors" in data:
            raise Exception(data["errors"])

        products = data["data"]["productsByCollectionHandle"]["products"]["nodes"]
        if not products:
            print("✅ Reached end of products.")
            break

        all_products.extend(products)
        offset += limit
        time.sleep(1)

    except Exception as e:
        print(f"❌ Error at offset {offset}: {e}")
        error_path = f"graphql_error_logs/error_log_offset_{offset}.json"
        with open(error_path, "w", encoding="utf-8") as f:
            try:
                f.write(response.text)
            except:
                f.write(json.dumps({"error": str(e)}))
        break

# Ensure save folder exists
os.makedirs("alo/json", exist_ok=True)

# Save to JSON
with open("alo/json/alo_yoga_mens_products.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, ensure_ascii=False, indent=2)

print(f"✅ Done. Saved {len(all_products)} accessories to alo_yoga_men_products.json")

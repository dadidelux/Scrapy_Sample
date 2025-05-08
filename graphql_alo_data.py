import requests
import json

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

# Fetch and print first page's raw JSON
data = fetch_page(offset=0)

# Save raw JSON to inspect manually
with open("alo_yoga_raw_page_0.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("🔍 Response for offset=0 saved to alo_yoga_raw_page_0.json.")
print("Open the file and look for 'products', 'nodes', or 'edges' under 'data'.")

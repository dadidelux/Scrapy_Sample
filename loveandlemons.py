import requests
import json
import time

base_url = "https://sxyn6w.a.searchspring.io/api/search/search.json"

params = {
    "resultsFormat": "native",
    "siteId": "sxyn6w",
    "resultsPerPage": 32,
    "bgfilter.ss_is_published": 1,
    "bgfilter.collection_handle": "lingerie",
    "intellisuggest": 0,
    "page": 1
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_products = []
max_pages = 20  # Adjust as needed

for page in range(1, max_pages + 1):
    params["page"] = page
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch page {page}")
        break

    data = response.json()
    products = data.get("results", [])
    if not products:
        print(f"🚫 No products on page {page}, stopping.")
        break

    all_products.extend(products)
    print(f"✅ Page {page}: {len(products)} products")
    time.sleep(1)  # Be respectful of rate limits

# Save to JSON
with open("forloveandlemons_lingerie.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, indent=2, ensure_ascii=False)

print(f"🎉 Done! Total products: {len(all_products)}")

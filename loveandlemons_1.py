import requests
import json
import time
import html
import pandas as pd

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
max_pages = 20  # You can increase if needed

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

    for product in products:
        cleaned = {
            "name": product.get("name"),
            "price": product.get("price"),
            "url": product.get("url"),
            "image": product.get("imageUrl"),
            "variants": []
        }

        raw_variants = product.get("variants")
        if raw_variants:
            try:
                unescaped = html.unescape(raw_variants)
                decoded_variants = json.loads(unescaped)

                for v in decoded_variants:
                    cleaned["variants"].append({
                        "size": v.get("option1"),
                        "color": v.get("option2"),
                        "price": v.get("price"),
                        "sku": v.get("sku"),
                        "inventory": v.get("inventory_quantity"),
                        "hs_code": v.get("mfield_global_harmonized_system_code")
                    })
            except Exception as e:
                cleaned["variant_parse_error"] = str(e)

        all_products.append(cleaned)

    print(f"✅ Page {page}: {len(products)} products processed.")
    time.sleep(1)

# Save to JSON file
output_filename = "forloveandlemons_lingerie_with_variants.json"
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(all_products, f, indent=2, ensure_ascii=False)

print(f"🎉 Done! Saved {len(all_products)} products to {output_filename}")

# # import json
# # import pandas as pd

# # Load JSON file
# with open("forloveandlemons_lingerie_full.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# # Normalize the top-level fields but keep nested structures like 'variants' and 'metafields'
# df = pd.json_normalize(data)

# # Select the first 22 columns only
# df_base_22 = df.iloc[:, :22]

# # Save to CSV if needed
# df_base_22.to_csv("forloveandlemons_lingerie_full.csv", index=False)

# # Display a preview
# print(df_base_22.head())


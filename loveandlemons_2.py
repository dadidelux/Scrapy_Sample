import requests
import json
import html
import time

base_url = "https://sxyn6w.a.searchspring.io/api/search/search.json"
headers = {
    "User-Agent": "Mozilla/5.0"
}
params = {
    "resultsFormat": "native",
    "siteId": "sxyn6w",
    "resultsPerPage": 32,
    "bgfilter.ss_is_published": 1,
    "bgfilter.collection_handle": "lingerie",
    "intellisuggest": 0,
    "page": 1
}

all_products = []
max_pages = 20  # Adjust this as needed

for page in range(1, max_pages + 1):
    params["page"] = page
    res = requests.get(base_url, params=params, headers=headers)

    if res.status_code != 200:
        print(f"❌ Page {page} failed.")
        break

    results = res.json().get("results", [])
    if not results:
        print(f"🚫 No results on page {page}. Ending.")
        break

    for item in results:
        product = {
            "id": item.get("id"),
            "uid": item.get("uid"),
            "name": item.get("name"),
            "title": item.get("title"),
            "brand": item.get("brand"),
            "description": item.get("description"),
            "handle": item.get("handle"),
            "product_type": item.get("product_type"),
            "product_type_unigram": item.get("product_type_unigram"),
            "price": item.get("price"),
            "msrp": item.get("msrp"),
            "sku": item.get("sku"),
            "url": item.get("url"),
            "image": item.get("imageUrl"),
            "thumbnail": item.get("thumbnailImageUrl"),
            "images": item.get("images"),
            "tags": item.get("tags"),
            "collection_handle": item.get("collection_handle"),
            "ss_in_stock": item.get("ss_in_stock"),
            "ss_inventory_count": item.get("ss_inventory_count"),
            "variants": [],
            "metafields": []
        }

        # Decode variants
        raw_variants = item.get("variants")
        if raw_variants:
            try:
                decoded = json.loads(html.unescape(raw_variants))
                for v in decoded:
                    product["variants"].append({
                        "title": v.get("title"),
                        "sku": v.get("sku"),
                        "price": v.get("price"),
                        "size": v.get("option1"),
                        "color": v.get("option2"),
                        "inventory_quantity": v.get("inventory_quantity"),
                        "hs_code": v.get("mfield_global_harmonized_system_code")
                    })
            except Exception as e:
                product["variants_error"] = str(e)

        # Decode metafields
        raw_meta = item.get("metafields")
        if raw_meta and isinstance(raw_meta, list) and raw_meta[0]:
            try:
                meta_decoded = json.loads(html.unescape(raw_meta[0]))
                product["metafields"] = meta_decoded
            except Exception as e:
                product["metafields_error"] = str(e)

        all_products.append(product)

    print(f"✅ Page {page}: {len(results)} products added.")
    time.sleep(1)  # polite crawling

# Save output
with open("forloveandlemons_lingerie_full.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, indent=2, ensure_ascii=False)

print(f"🎉 Done! Saved {len(all_products)} products.")

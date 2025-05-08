import requests
import json
from tqdm import tqdm

base_url = "https://smmarkets.ph/graphql"
category_id = "1270"
page_size = 24

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
}

def build_query(page):
    return {
        "query": f"""
        {{
            unbxdProducts(
                filter: {{ category_id: {{ eq: "{category_id}" }} }},
                pageSize: {page_size},
                currentPage: {page}
            ) {{
                items {{
                    id
                    name
                    sku
                    url_key
                    product_link
                    price {{
                        regularPrice {{
                            amount {{
                                value
                                currency
                            }}
                        }}
                    }}
                    price_range {{
                        minimum_price {{
                            final_price {{ value currency }}
                        }}
                    }}
                    small_image {{ url }}
                }}
                request_id
            }}
        }}
        """
    }

all_products = []
current_page = 1

while True:
    payload = build_query(current_page)
    response = requests.post(base_url, headers=headers, json=payload)
    data = response.json()
    
    try:
        items = data["data"]["unbxdProducts"]["items"]
    except KeyError:
        print("Failed to parse page", current_page)
        break

    if not items:
        break  # No more products
    
    all_products.extend(items)
    print(f"Extracted page {current_page} with {len(items)} products")
    current_page += 1

# Save to JSON file
with open("smmarkets_products.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, ensure_ascii=False, indent=2)

print(f"✅ Extraction complete: {len(all_products)} products saved.")

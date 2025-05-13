import json
import pandas as pd
from datetime import datetime
import pytz
import os

# Load JSON file
with open("alo/json/alo_yoga_acc_products.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Flatten and collect data
records = []
for product in data:
    base = {
        "gid": product.get("gid"),
        "images": ";".join(product.get("images", [])),
        "handle": product.get("handle"),
        "title": product.get("title"),
        "minPrice": product.get("priceRange", {}).get("minVariantPrice", {}).get("amount"),
        "maxPrice": product.get("priceRange", {}).get("maxVariantPrice", {}).get("amount"),
        "compareAtMinPrice": product.get("compareAtPriceRange", {}).get("minVariantPrice", {}).get("amount"),
        "compareAtMaxPrice": product.get("compareAtPriceRange", {}).get("maxVariantPrice", {}).get("amount"),
        "availableForSale": product.get("availableForSale"),
        "productType": product.get("productType"),
        "vendor": product.get("vendor"),
        "onlineStoreUrl": product.get("onlineStoreUrl"),
        "totalInventory_website_settings": product.get("totalInventory"),
        "colorOptions": ";".join([opt.get("values")[0] for opt in product.get("options", []) if opt.get("name") == "Color"]),
        "sizeOptions": ";".join([",".join(opt.get("values")) for opt in product.get("options", []) if opt.get("name") == "Size"]),
    
    }

    # # Expand tags to columns
    # tags = product.get("tags", [])
    # for tag in tags:
    #     key_value = tag.split(":", 1)
    #     if len(key_value) == 2:
    #         key, value = key_value
    #         base[f"tag_{key.strip()}"] = value.strip()
    #     else:
    #         base[f"tag_{tag.strip()}"] = True  # Standalone tag

    COMMON_TAG_KEYS = {
    "b", "BVCategory", "Color", "ColorGroup", "Content", "Maintenance",
    "not_clearance", "pricing", "Status", "StyleId", "X",
    "YCRF_reviews", "YGroup", "ProductType"
    }

    # Save all tags as reference
    base["all_tags"] = ";".join(product.get("tags", []))

    # Extract and expand only common tags into their own columns
    for tag in product.get("tags", []):
        parts = tag.split(":", 1)
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            if key in COMMON_TAG_KEYS:
                base[f"tag_{key}"] = value
        else:
            # Standalone tag, like "not_clearance"
            if tag in COMMON_TAG_KEYS:
                base[f"tag_{tag}"] = True



    # Process first availableColorsMetafieldValue item
    metafield_str = product.get("availableColorsMetafieldValue")
    if metafield_str:
        try:
            color_meta_list = json.loads(metafield_str)
            if color_meta_list:
                first_color = color_meta_list[0]
                base["availableColorsMeta_name"] = first_color.get("name")
                base["availableColorsMeta_handle"] = first_color.get("handle")
                base["availableColorsMeta_totalInventory"] = first_color.get("totalInventory")
                base["availableColorsMeta_price"] = first_color.get("price")
                base["availableColorsMeta_isAlmostGone"] = first_color.get("isAlmostGone")

                # # Flatten inventoryBySize into individual columns (optional)
                # inventory_by_size = first_color.get("inventoryBySize", {})
                # for size, qty in inventory_by_size.items():
                #     col_name = f"invSize_{size.replace('/', '_').replace('.', '_').replace('-', '_')}"  # e.g., 3.5M/5W -> invSize_3_5M_5W
                #     base[col_name] = qty
                
                # Convert inventoryBySize to JSON string
                inventory_by_size = first_color.get("availableColors_inventoryBySize", {})
                base["availableColors_inventoryBySize"] = json.dumps(inventory_by_size)

        except Exception as e:
            print(f"⚠️ Error parsing availableColorsMetafieldValue for gid {product.get('gid')}: {e}")


    # Add processed date (no time), in Cerritos timezone
    cerritos_tz = pytz.timezone("America/Los_Angeles")
    base["processed_date"] = datetime.now(cerritos_tz).date().isoformat()

    records.append(base)

# Create DataFrame
df = pd.DataFrame(records)

# Ensure save folder exists
os.makedirs("alo/csv", exist_ok=True)

# Save to CSV
df.to_csv("alo/csv/alo_yoga_products_acc_processed.csv", index=False)

print("✅ Data processed and saved to 'alo_yoga_products_acc_processed.csv'")

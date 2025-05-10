import json
import pandas as pd
from datetime import datetime
import pytz
import os

# Load JSON file
with open("alo/json/alo_yoga_womens_products.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Flatten and collect data
records = []
for product in data:
    base = {
        "gid": product.get("gid"),
        "handle": product.get("handle"),
        "title": product.get("title"),
        "vendor": product.get("vendor"),
        "productType": product.get("productType"),
        "onlineStoreUrl": product.get("onlineStoreUrl"),
        "availableForSale": product.get("availableForSale"),
        "totalInventory": product.get("totalInventory"),
        "minPrice": product.get("priceRange", {}).get("minVariantPrice", {}).get("amount"),
        "maxPrice": product.get("priceRange", {}).get("maxVariantPrice", {}).get("amount"),
        "compareAtMinPrice": product.get("compareAtPriceRange", {}).get("minVariantPrice", {}).get("amount"),
        "compareAtMaxPrice": product.get("compareAtPriceRange", {}).get("maxVariantPrice", {}).get("amount"),
        "images": ";".join(product.get("images", [])),
        "colorOptions": ";".join([opt.get("values")[0] for opt in product.get("options", []) if opt.get("name") == "Color"]),
        "sizeOptions": ";".join([",".join(opt.get("values")) for opt in product.get("options", []) if opt.get("name") == "Size"]),
    }

    # Expand tags to columns
    tags = product.get("tags", [])
    for tag in tags:
        key_value = tag.split(":", 1)
        if len(key_value) == 2:
            key, value = key_value
            base[f"tag_{key.strip()}"] = value.strip()
        else:
            base[f"tag_{tag.strip()}"] = True  # Standalone tag

    # Add processed date (no time), in Cerritos timezone
    cerritos_tz = pytz.timezone("America/Los_Angeles")
    base["processed_date"] = datetime.now(cerritos_tz).date().isoformat()

    records.append(base)

# Create DataFrame
df = pd.DataFrame(records)

# Ensure save folder exists
os.makedirs("alo/csv", exist_ok=True)

# Save to CSV
df.to_csv("alo/csv/alo_yoga_products_womens_processed.csv", index=False)

print("✅ Data processed and saved to 'alo_yoga_products_womens_processed.csv'")

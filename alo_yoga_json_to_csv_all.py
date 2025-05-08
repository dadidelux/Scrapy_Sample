import json
import pandas as pd
from collections import defaultdict
from ast import literal_eval

# Load JSON
with open("alo_yoga_products.json", "r", encoding="utf-8") as f:
    data = json.load(f)

main_fields = [
    "gid", "title", "handle", "vendor", "productType", "availableForSale",
    "onlineStoreUrl", "totalInventory"
]

rows = []

for item in data:
    row = {field: item.get(field) for field in main_fields}
    row["price_min"] = item.get("priceRange", {}).get("minVariantPrice", {}).get("amount")
    row["price_max"] = item.get("priceRange", {}).get("maxVariantPrice", {}).get("amount")
    row["image_1"] = item.get("images", [None])[0]

    # Flatten size and color from options
    for opt in item.get("options", []):
        if opt["name"].lower() == "size":
            row["sizes"] = ", ".join(opt["values"])
        elif opt["name"].lower() == "color":
            row["colors"] = ", ".join(opt["values"])

    # Expand tag fields
    tag_groups = defaultdict(list)
    for tag in item.get("tags", []):
        if ":" in tag:
            key, *value = tag.split(":")
            tag_groups[f"tag_{key.strip()}"].append(":".join(value).strip())
        else:
            tag_groups["tag_misc"].append(tag)
    for key, value in tag_groups.items():
        row[key] = ", ".join(value)

    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv("alo_yoga_products_expanded.csv", index=False)

import json
import pandas as pd

# Load JSON data from file
with open('alo_yoga_products.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Flatten each product to extract relevant fields
flattened_data = []
for product in data:
    try:
        flattened_data.append({
            'gid': product.get('gid'),
            'title': product.get('title'),
            'handle': product.get('handle'),
            'productType': product.get('productType'),
            'vendor': product.get('vendor'),
            'price_min': float(product['priceRange']['minVariantPrice']['amount']),
            'price_max': float(product['priceRange']['maxVariantPrice']['amount']),
            'url': product.get('onlineStoreUrl'),
            'availableForSale': product.get('availableForSale'),
            'totalInventory': product.get('totalInventory'),
            'tags': ", ".join(product.get('tags', [])),  # join list of tags into a string
            'images': ", ".join(product.get('images', []))  # join list of image URLs into a string
        })
    except Exception as e:
        print(f"⚠️ Skipping product due to error: {e}")

# Convert to DataFrame
df = pd.DataFrame(flattened_data)

# Save to CSV
output_path = 'alo_yoga_products_sample.csv'
df.to_csv(output_path, index=False)

print(f"✅ CSV file saved at: {output_path}")

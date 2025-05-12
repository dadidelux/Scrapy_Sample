import json
import pandas as pd

def clean_price_field(raw):
    try:
        value = float(str(raw).replace("$", "").replace(",", ""))
        return value if value != 0 else None
    except:
        return None

# Load JSON file
with open("shopbop/json/shopbop_mens_products.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Build rows
records = []
for item in data:
    product = item.get("product", {})
    base = {
        "productSin": product.get("productSin"),
        "productCode": product.get("productCode"),
        "shortDescription": product.get("shortDescription"),
        "designerName": product.get("designerName"),
        "designerCode": product.get("designerCode"),
        "price": product.get("retailPrice", {}).get("usdPrice"),
        "highPrice": clean_price_field(product.get("highPrice", {}).get("price")),
        "lowPrice": clean_price_field(product.get("lowPrice", {}).get("price")),
        "productCategory": product.get("productCategory"),
        "productDetailUrl": product.get("productDetailUrl"),
        "designerUrl": product.get("designerUrl"),
        "inStock": product.get("inStock"),
        "cleanBeauty": product.get("cleanBeauty"),
        "shippingRestriction": product.get("shippingRestriction"),
        "gender": product.get("gender"),
        "sizeScale": product.get("sizeScale"),
        "browsePromoEligibility": product.get("browsePromoEligibility"),
        "detailPromoEligibility": product.get("detailPromoEligibility"),
        "reviewsCount": product.get("reviews", {}).get("count"),
        "reviewsAvg": product.get("reviews", {}).get("average"),
    }

    # Loop through colors
    for color in product.get("colors", []):
        row = base.copy()
        row["color"] = color.get("name")
        row["colorPrice"] = clean_price_field(color.get("colorPrice", {}).get("price"))
        row["colorOnSale"] = color.get("colorPrice", {}).get("onSale")
        row["colorFinalSale"] = color.get("colorPrice", {}).get("finalSale")
        row["inStockColor"] = color.get("inStock")
        row["imagePrimary"] = color.get("images", [{}])[0].get("src") if color.get("images") else ""
        row["swatchImage"] = color.get("swatch", {}).get("src")
        row["skuCodes"] = ", ".join(color.get("skuCodes", []))
        row["sizeSins"] = ", ".join(color.get("sizeSins", []))
        row["fullIngredients"] = color.get("fullIngredients", "")
        row["imageOverlayValue"] = color.get("imageOverlayValue", "")
        row["statusCode"] = color.get("statusCode", "")
        records.append(row)

# Create dataframe and save
df = pd.DataFrame(records)
df.to_csv("shopbop/csv/shopbop_mens_products_full.csv", index=False, encoding="utf-8")

print("✅ CSV created: shopbop_mens_products_full.csv")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import re

# 1. Launch browser and go to collection page
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Remove for debugging
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

collection_url = "https://jadedldn.com/en-ph/collections/mens-all"
driver.get(collection_url)
time.sleep(5)  # Wait for JS to render

# 2. Find all product links (collect hrefs)
product_links = []
product_card_elems = driver.find_elements(By.CSS_SELECTOR, 'a.full-unstyled-link')
for elem in product_card_elems:
    href = elem.get_attribute('href')
    if href and href not in product_links:
        product_links.append(href)

print(f"Found {len(product_links)} product links.")

products_data = []

# 3. For each product, extract product meta JSON from product page
for idx, product_url in enumerate(product_links):
    driver.get(product_url)
    time.sleep(2)
    html = driver.page_source

    # Try to find the JSON inside <script type="application/ld+json">
    scripts = driver.find_elements(By.XPATH, "//script[@type='application/ld+json']")
    product_json = None
    for s in scripts:
        txt = s.get_attribute('innerHTML')
        if '"@type": "Product"' in txt:
            try:
                data = json.loads(txt)
                product_json = data
                break
            except Exception as e:
                continue

    # If not found, skip
    if product_json is None:
        print(f"Could not find JSON for {product_url}")
        continue

    # Optional: also extract Shopify's big embedded JSON for even more detail
    # You can search for "var __st = {" or window.ShopifyAnalytics.meta or "ShopifyAnalytics.meta = " if needed

    # Add to final products list
    products_data.append(product_json)
    print(f"Processed [{idx+1}/{len(product_links)}]: {product_json.get('name','?')}")

# 4. Save all products to JSON
with open("jadedldn_all_products.json", "w", encoding="utf-8") as f:
    json.dump(products_data, f, ensure_ascii=False, indent=2)

driver.quit()
print(f"\n💾 Done! Saved {len(products_data)} products to jadedldn_all_products.json")

import time
import pandas as pd
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Change to True for headless
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.freepeople.com/womens-clothes/", timeout=90000)

    # Wait for product tiles to appear
    page.wait_for_selector("div.c-product-tile", timeout=20000)

    # Simulate infinite scroll
    for _ in range(5):
        page.mouse.wheel(0, 5000)  # Simulate human scroll
        time.sleep(3)

    # One more wait to ensure products load
    page.wait_for_selector("div.c-product-tile", timeout=10000)

    # Extract product data
    product_elements = page.query_selector_all("div.c-product-tile")
    data = []
    for p in product_elements:
        try:
            name = p.query_selector(".c-product-tile__heading").inner_text().strip()
            price = p.query_selector(".c-product-price__current").inner_text().strip()
            url = p.query_selector("a").get_attribute("href")
            data.append({
                "title": name,
                "price": price,
                "url": url
            })
        except Exception as e:
            continue

    browser.close()

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("freepeople_products_playwright.csv", index=False)
print(f"✅ Saved {len(df)} products to freepeople_products_playwright.csv")

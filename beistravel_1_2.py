# from playwright.sync_api import sync_playwright
# import json
# import time

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)  # Set True to hide browser
#     page = browser.new_page()
#     page.goto("https://beistravel.com/collections/all", timeout=120000)

#     # Keep scrolling until no more products are loaded
#     previous_height = 0
#     for _ in range(50):  # Scroll up to 50 times max
#         page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#         time.sleep(1.2)
#         # Wait for more products to load
#         current_height = page.evaluate("document.body.scrollHeight")
#         if current_height == previous_height:
#             break
#         previous_height = current_height

#     # Now extract the JS variable directly!
#     products = page.evaluate("""
#         () => {
#             return typeof slideruleData === 'object' && 
#                    slideruleData.collection && 
#                    slideruleData.collection.rawProducts 
#                    ? slideruleData.collection.rawProducts : []
#         }
#     """)
#     print(f"✅ Found {len(products)} products")

#     # Save all products to JSON
#     with open("beis_products.json", "w", encoding="utf-8") as f:
#         json.dump(products, f, ensure_ascii=False, indent=2)
#     print("✅ Saved beis_products.json")

#     # Optionally: Preview the first product
#     print(json.dumps(products[0], indent=2))

#     browser.close()


from playwright.sync_api import sync_playwright
import json
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://beistravel.com/collections/all", timeout=120_000)

    last_viewed = 0
    total_products = 495  # or parse from the page

    while True:
        # Check "You've viewed X of Y products"
        viewed_text = page.inner_text('p:has(span.viewed)')
        print("Status:", viewed_text)
        viewed_count = int(page.locator("span.viewed").inner_text())
        if viewed_count == last_viewed:
            print("No new products loaded; breaking.")
            break
        last_viewed = viewed_count

        if viewed_count >= total_products:
            print("All products loaded!")
            break

        # Try to click the "Load More" <a> button
        try:
            load_more = page.query_selector('a.load-more_btn')
            if load_more and load_more.is_visible():
                print("Clicking Load More...")
                load_more.click()
                time.sleep(2.5)
            else:
                print("No Load More button visible; breaking.")
                break
        except Exception as e:
            print("Error clicking Load More:", e)
            break

    # Get all products from slideruleData
    products = page.evaluate("""
        () => {
            return typeof slideruleData === 'object' && 
                   slideruleData.collection && 
                   slideruleData.collection.rawProducts 
                   ? slideruleData.collection.rawProducts : []
        }
    """)
    print(f"✅ Found {len(products)} products")
    with open("beis_products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print("✅ Saved beis_products.json")
    browser.close()


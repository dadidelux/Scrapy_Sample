# from playwright.sync_api import sync_playwright
# import pandas as pd
# import time
# import re

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     page = browser.new_page()
#     page.goto("https://beistravel.com/collections/all", timeout=120_000)

#     # Dynamically determine total products
#     counter_text = page.inner_text('p:has(span.viewed)')
#     print("Initial status:", counter_text)
#     match = re.search(r'of\s+([\d,]+)\s+products', counter_text)
#     if match:
#         total_products = int(match.group(1).replace(",", ""))
#         print(f"Total products on this page: {total_products}")
#     else:
#         total_products = 999999
#         print("Failed to detect total products, using very high ceiling.")

#     last_viewed = 0

#     while True:
#         viewed_text = page.inner_text('p:has(span.viewed)')
#         print("Status:", viewed_text)
#         viewed_count = int(page.locator("span.viewed").inner_text())
#         if viewed_count == last_viewed:
#             print("No new products loaded; breaking.")
#             break
#         last_viewed = viewed_count

#         if viewed_count >= total_products:
#             print("All products loaded!")
#             break

#         try:
#             load_more = page.query_selector('a.load-more_btn')
#             if load_more and load_more.is_visible():
#                 print("Clicking Load More...")
#                 load_more.click()
#                 time.sleep(2.5)
#             else:
#                 print("No Load More button visible; breaking.")
#                 break
#         except Exception as e:
#             print("Error clicking Load More:", e)
#             break

#     # SCRAPE PRODUCT CARDS FROM DOM INSTEAD OF JS VARIABLE
#     print("Scraping all loaded product cards from DOM...")
#     cards = page.query_selector_all('.product-card')

#     data = []
#     for c in cards:
#         try:
#             title = c.query_selector('.product-card-title').inner_text().strip()
#             price = c.query_selector('.product-card-price .price').inner_text().strip() \
#                 if c.query_selector('.product-card-price .price') else ""
#             url = c.query_selector('a').get_attribute('href')
#             if url and not url.startswith('http'):
#                 url = 'https://beistravel.com' + url
#             img = c.query_selector('img').get_attribute('src') \
#                 if c.query_selector('img') else ""
#             data.append({
#                 "title": title,
#                 "price": price,
#                 "url": url,
#                 "image": img
#             })
#         except Exception:
#             continue

#     print(f"✅ Scraped {len(data)} product cards.")

#     # Save to CSV
#     df = pd.DataFrame(data)
#     df.to_csv("beis_products_full.csv", index=False)
#     print("✅ Saved beis_products_full.csv")
#     browser.close()


from playwright.sync_api import sync_playwright
import pandas as pd
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://beistravel.com/collections/all", timeout=120_000)

    # Load all products dynamically (click "Load More" as needed)
    while True:
        try:
            load_more = page.query_selector('a.load-more_btn')
            if load_more and load_more.is_visible():
                load_more.click()
                time.sleep(2.5)
            else:
                break
        except Exception:
            break

    time.sleep(2)  # Wait for all to load

    # Find all product-card elements
    product_cards = page.query_selector_all("product-card")

    data = []
    for card in product_cards:
        # Main product info
        try:
            main_url = card.query_selector('a.product-card__url').get_attribute('href')
            if main_url and not main_url.startswith('http'):
                main_url = 'https://beistravel.com' + main_url
            main_title = card.query_selector('a.product-card__url').inner_text().strip()
            main_img = card.query_selector('img.product-card__img').get_attribute('src')
            price_elem = card.query_selector('span.price-item--regular')
            main_price = price_elem.inner_text().strip() if price_elem else ''
        except Exception as ex:
            print(f"Error main info: {ex}")
            continue

        # For each color variant (swatch)
        swatches = card.query_selector_all('span.color-swatch')
        for sw in swatches:
            try:
                color = sw.get_attribute('data-product-color')
                variant_id = sw.get_attribute('data-product-id')
                available = sw.get_attribute('data-product-available')
                url = sw.get_attribute('data-product-url')
                if url and not url.startswith('http'):
                    url = 'https://beistravel.com' + url
                image = sw.get_attribute('data-product-image')
                hover_image = sw.get_attribute('data-product-image-on-hover')
                badge = sw.get_attribute('data-product-badge')
                data.append({
                    'main_title': main_title,
                    'main_url': main_url,
                    'main_price': main_price,
                    'main_image': main_img,
                    'variant_color': color,
                    'variant_id': variant_id,
                    'variant_available': available,
                    'variant_url': url,
                    'variant_image': image,
                    'variant_hover_image': hover_image,
                    'variant_badge': badge,
                })
            except Exception as sw_ex:
                print(f"Swatch error: {sw_ex}")
                continue

    print(f"Extracted {len(data)} variants")

    # Save to CSV
    df = pd.DataFrame(data)
    df.to_csv("beis_full_variants.csv", index=False)
    print("Saved as beis_full_variants.csv")
    browser.close()

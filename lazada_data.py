from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv

def run():
    all_items = []

    # Chrome on Windows 10 user-agent
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()

        for page_num in range(1, 6):  # First 5 pages
            print(f"🔄 Fetching page {page_num}...")
            url = f"https://www.lazada.com.ph/shop-mobiles/?page={page_num}"
            page.goto(url, timeout=60000)
            page.wait_for_timeout(4000)

            html = page.content()
            soup = BeautifulSoup(html, "html.parser")

            cards = soup.select("div[data-qa-locator='product-item']")
            if not cards:
                print("✅ No more product cards found.")
                break

            for card in cards:
                title = card.select_one("div[data-qa-locator='product-item-name']")
                price = card.select_one(".currency")
                link = card.find("a", href=True)
                image = card.find("img", src=True)

                if title and price and link and image:
                    all_items.append({
                        "title": title.get_text(strip=True),
                        "price": price.get_text(strip=True),
                        "url": "https:" + link['href'],
                        "image": image['src']
                    })

        browser.close()

    with open("lazada_mobiles_playwright.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "url", "image"])
        writer.writeheader()
        writer.writerows(all_items)

    print(f"✅ Saved {len(all_items)} products to lazada_mobiles_playwright.csv")

if __name__ == "__main__":
    run()

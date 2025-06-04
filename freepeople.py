from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

# Setup browser
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # uncomment for headless mode

driver = webdriver.Chrome(options=options)
driver.get("https://www.freepeople.com/womens-clothes/")

# Wait for page to load
time.sleep(100)

# Scroll to load more (simulate infinite scroll)
for _ in range(5):  # scroll 5 times
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # let new items load

# Extract product data
products = driver.find_elements(By.CSS_SELECTOR, "div.c-product-tile")

data = []
for p in products:
    try:
        name = p.find_element(By.CSS_SELECTOR, ".c-product-tile__heading").text.strip()
        price = p.find_element(By.CSS_SELECTOR, ".c-product-price__current").text.strip()
        url = p.find_element(By.TAG_NAME, "a").get_attribute("href")
        data.append({
            "title": name,
            "price": price,
            "url": url
        })
    except Exception as e:
        continue

driver.quit()

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("freepeople_products_selenium.csv", index=False)
print(f"✅ Saved {len(df)} products to freepeople_products_selenium.csv")

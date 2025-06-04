import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Setup undetected Chrome
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options)

# Go to the product page
driver.get("https://www.freepeople.com/womens-clothes/")

# Step 1: Try to interact with the page to pass bot check
try:
    print("🖱 Clicking page to bypass modal...")
    actions = ActionChains(driver)
    actions.move_by_offset(10, 10).click().perform()
    time.sleep(3)
except Exception as e:
    print("❌ Interaction failed:", e)

# Step 2: Wait for product tiles to load
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.c-product-tile"))
    )
    print("✅ Product tiles appeared.")
except Exception as e:
    print("❌ Product tiles never loaded:", e)

# Step 3: Scroll to load more products
for _ in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

# Step 4: Debug screenshot
driver.save_screenshot("fp_debug.png")
print("📸 Screenshot saved as fp_debug.png")

# Step 5: Extract product data
products = driver.find_elements(By.CSS_SELECTOR, "div.c-product-tile")
print(f"🧺 Found {len(products)} product tiles.")

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
    except Exception:
        continue

driver.quit()

# Step 6: Save to CSV
df = pd.DataFrame(data)
df.to_csv("freepeople_products_selenium_stealth.csv", index=False)
print(f"✅ Saved {len(df)} products to freepeople_products_selenium_stealth.csv")

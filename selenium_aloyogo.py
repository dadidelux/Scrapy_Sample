from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time

options = Options()
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

driver = webdriver.Chrome(options=options)
driver.get("https://www.aloyoga.com/en-ph/collections/womens-shop-all")


# Allow page to load
time.sleep(5)

# Infinite scroll logic
last_height = driver.execute_script("return document.body.scrollHeight")

scroll_attempt = 0
max_attempts = 15

while scroll_attempt < max_attempts:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for products to load
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        break
    last_height = new_height
    scroll_attempt += 1

# Gather performance logs to find GraphQL calls
logs = driver.get_log("performance")
graphql_requests = []

for entry in logs:
    try:
        message = json.loads(entry["message"])["message"]
        if message.get("method") == "Network.requestWillBeSent":
            request = message.get("params", {}).get("request", {})
            url = request.get("url", "")
            if "/graphql" in url:
                graphql_requests.append({
                    "url": url,
                    "headers": request.get("headers", {}),
                    "postData": request.get("postData", "")
                })
    except Exception as e:
        continue  # Skip malformed logs

driver.quit()

# Print captured GraphQL POSTs
for gql in graphql_requests:
    print("=== GraphQL Request ===")
    print("URL:", gql["url"])
    print("PostData:", gql["postData"])
    print()

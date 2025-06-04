from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import json
import os

url = 'https://jadedldn.com/en-ph/collections/mens-all'

# Set up headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

# If chromedriver is not in PATH, specify the path here:
# driver = webdriver.Chrome(executable_path='C:/path/to/chromedriver.exe', options=chrome_options)
driver = webdriver.Chrome(options=chrome_options)

print("Loading page...")
driver.get(url)
time.sleep(5)  # Wait for JS to load. Increase if needed.

html = driver.page_source

with open("jadedldn_mens_all_rendered.html", "w", encoding="utf-8") as f:
    f.write(html)
print("\n💾 Saved rendered HTML to jadedldn_mens_all_rendered.html")

def extract_js_object(text, start_key):
    start = text.find(start_key)
    if start == -1:
        return None
    brace_start = text.find('{', start)
    if brace_start == -1:
        return None
    depth = 0
    for i in range(brace_start, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return text[brace_start:i+1]
    return None

js_obj_str = extract_js_object(html, "collectionView")
if js_obj_str:
    js_obj_str = re.sub(r'([,{{\s])(\w+)\s*:', r'\1"\2":', js_obj_str)
    js_obj_str = re.sub(r':\s*([A-Za-z0-9_\-/\\.]+)(?=,|})', lambda m: f':"{m.group(1)}"' if not re.match(r'^(true|false|null|\d+(\.\d+)?)$', m.group(1)) else f':{m.group(1)}', js_obj_str)
    js_obj_str = js_obj_str.replace("'", '"')
    js_obj_str = re.sub(r',\s*([}}\]])', r'\1', js_obj_str)
    try:
        collection_json = json.loads(js_obj_str)
        with open("jadedldn_collectionView.json", "w", encoding="utf-8") as out_f:
            json.dump(collection_json, out_f, ensure_ascii=False, indent=2)
        print("\n💾 Extracted collectionView to jadedldn_collectionView.json")
    except Exception as e:
        print(f"❌ Could not parse collectionView as JSON: {e}")
else:
    print("❌ collectionView block not found in rendered HTML.")

driver.quit()

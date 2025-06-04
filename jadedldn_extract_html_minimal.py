import requests
import re
import json
import os

# 1. Download the page HTML
url = 'https://jadedldn.com/en-ph/collections/mens-all'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}
resp = requests.get(url, headers=headers)
print("Status code:", resp.status_code)
if resp.status_code != 200:
    print(f"❌ Request failed with status code {resp.status_code}")
    exit(1)
html = resp.text

# Save the HTML to a file
with open("jadedldn_mens_all.html", "w", encoding="utf-8") as html_file:
    html_file.write(html)
print("\n💾 Saved the HTML to jadedldn_mens_all_poga.html")

# Print the first 3000 characters of the HTML to confirm content
# print("\nHTML preview (first 3000 chars):\n", html[:500])

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

# Extract collectionView block from the HTML file
if not os.path.exists("jadedldn_mens_all.html"):
    print("❌ HTML file 'jadedldn_mens_all.html' not found. Please ensure the download step succeeded.")
    exit(1)

with open("jadedldn_mens_all.html", "r", encoding="utf-8") as f:
    html_content = f.read()

js_obj_str = extract_js_object(html_content, "collectionView")
if js_obj_str:
    # Add quotes around all keys that are not already quoted
    js_obj_str = re.sub(r'([,{{\s])(\w+)\s*:', r'\1"\2":', js_obj_str)
    # Add quotes around all unquoted string values (not numbers, not true/false/null, not objects/arrays)
    js_obj_str = re.sub(r':\s*([A-Za-z0-9_\-/\\.]+)(?=,|})', lambda m: f':"{m.group(1)}"' if not re.match(r'^(true|false|null|\d+(\.\d+)?)$', m.group(1)) else f':{m.group(1)}', js_obj_str)
    # Convert single to double quotes
    js_obj_str = js_obj_str.replace("'", '"')
    # Remove trailing commas
    js_obj_str = re.sub(r',\s*([}}\]])', r'\1', js_obj_str)
    try:
        collection_json = json.loads(js_obj_str)
        with open("jadedldn_collectionView.json", "w", encoding="utf-8") as out_f:
            json.dump(collection_json, out_f, ensure_ascii=False, indent=2)
        print("\n💾 Extracted collectionView to jadedldn_collectionView.json")
    except Exception as e:
        print(f"❌ Could not parse collectionView as JSON: {e}")
else:
    print("❌ collectionView block not found in HTML.")

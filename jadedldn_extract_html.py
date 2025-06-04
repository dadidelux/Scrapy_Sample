# import requests
# import re
# import json

# # 1. Download the page HTML
# url = 'https://jadedldn.com/en-ph/collections/mens-all'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
# }
# resp = requests.get(url, headers=headers)
# html = resp.text

# # 2. Find the configUrl
# match = re.search(r'configUrl\s*=\s*["\']([^"\']+)["\']', html)
# if not match:
#     raise Exception("Couldn't find configUrl")
# config_url = match.group(1)
# # Build the full URL
# config_full_url = 'https://jadedldn.com' + config_url

# # 3. Download the JS config file
# js_resp = requests.get(config_full_url, headers=headers)
# js_text = js_resp.text

# # 4. Extract the JSON object (after "export default ")
# json_match = re.search(r'export\s+default\s+(\{.*\});?$', js_text, re.DOTALL)
# if not json_match:
#     raise Exception("Couldn't extract JSON from config.js")

# json_str = json_match.group(1)

# # 5. Parse the JSON (fix trailing commas if needed)
# # (Optional: you can use a safer JSON5 parser if the JS isn't strict JSON)
# config = json.loads(json_str)

# # 6. Print or save the config
# print(json.dumps(config, indent=2))

# # Save the JSON file locally
# with open("config.json", "w", encoding="utf-8") as json_file:
#     json.dump(config, json_file, ensure_ascii=False, indent=2)
# print("\n💾 Saved the JSON config to config.json")

# # Extract and save collectionView.items if present
# items = config.get("collectionView", {}).get("items", [])
# with open("jadedldn_collection_items.json", "w", encoding="utf-8") as out_f:
#     json.dump(items, out_f, ensure_ascii=False, indent=2)
# print(f"\n💾 Extracted {len(items)} items to jadedldn_collection_items.json")


import requests
import re
import json

# 1. Download the page HTML
url = 'https://jadedldn.com/en-ph/collections/mens-all'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}
resp = requests.get(url, headers=headers)
html = resp.text

# Save the HTML to a file
with open("jadedldn_mens_all.html", "w", encoding="utf-8") as html_file:
    html_file.write(html)
print("\n💾 Saved the HTML to jadedldn_mens_all.html")

# 2. Extract JSON blobs from <script type="application/ld+json"> tags
json_blobs = re.findall(
    r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',
    html, re.DOTALL | re.IGNORECASE
)

json_objects = []
for i, blob in enumerate(json_blobs):
    blob = blob.strip()
    try:
        json_obj = json.loads(blob)
        json_objects.append(json_obj)
    except Exception as e:
        print(f"Skipping blob {i+1}: Could not parse as JSON ({e})")

if not json_objects:
    print("No JSON objects found in <script type='application/ld+json'>.")
else:
    print(f"Found {len(json_objects)} JSON object(s) in HTML.")

# 3. Save all JSON blobs to file (as a list)
with open("jadedldn_html_embedded_json.json", "w", encoding="utf-8") as out_f:
    json.dump(json_objects, out_f, ensure_ascii=False, indent=2)
print(f"\n💾 Saved {len(json_objects)} JSON objects to jadedldn_html_embedded_json.json")

# 4. Optionally, print a sample
if json_objects:
    print("\nSample JSON object:\n")
    print(json.dumps(json_objects[0], indent=2))

# Extract cartData block from the HTML file
with open("jadedldn_mens_all.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Regex to match cartData: { ... } (non-greedy, multiline)
cartdata_match = re.search(r"cartData\s*:\s*\{(.*?)\}\s*[,}]", html_content, re.DOTALL)

if cartdata_match:
    cartdata_body = cartdata_match.group(1)
    cartdata_str = "{" + cartdata_body + "}"
    # Add quotes around all keys
    cartdata_str = re.sub(r'(\w+)\s*:', r'"\1":', cartdata_str)
    # Add quotes around all unquoted string values (for this specific structure)
    cartdata_str = re.sub(r':\s*([A-Za-z_][A-ZaZ0-9_]*)\s*([,}])', r':"\1"\2', cartdata_str)
    # Convert single to double quotes (if any)
    cartdata_str = cartdata_str.replace("'", '"')
    # Remove trailing commas (if any)
    cartdata_str = re.sub(r',\s*([}\]])', r'\1', cartdata_str)
    try:
        cartdata_json = json.loads(cartdata_str)
        with open("jadedldn_cartdata.json", "w", encoding="utf-8") as out_f:
            json.dump(cartdata_json, out_f, ensure_ascii=False, indent=2)
        print("\n💾 Extracted cartData to jadedldn_cartdata.json")
    except Exception as e:
        print(f"❌ Could not parse cartData as JSON: {e}")
else:
    print("❌ cartData block not found in HTML.")

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
with open("jadedldn_mens_all.html", "r", encoding="utf-8") as f:
    html_content = f.read()

js_obj_str = extract_js_object(html_content, "collectionView")
if js_obj_str:
    # Add quotes around all keys that are not already quoted
    js_obj_str = re.sub(r'([,{\s])(\w+)\s*:', r'\1"\2":', js_obj_str)
    # Add quotes around all unquoted string values (not numbers, not true/false/null, not objects/arrays)
    js_obj_str = re.sub(r':\s*([A-Za-z0-9_\-/\\.]+)(?=,|})', lambda m: f':"{m.group(1)}"' if not re.match(r'^(true|false|null|\d+(\.\d+)?)$', m.group(1)) else f':{m.group(1)}', js_obj_str)
    # Convert single to double quotes
    js_obj_str = js_obj_str.replace("'", '"')
    # Remove trailing commas
    js_obj_str = re.sub(r',\s*([}\]])', r'\1', js_obj_str)
    try:
        collection_json = json.loads(js_obj_str)
        with open("jadedldn_collectionView.json", "w", encoding="utf-8") as out_f:
            json.dump(collection_json, out_f, ensure_ascii=False, indent=2)
        print("\n💾 Extracted collectionView to jadedldn_collectionView.json")
    except Exception as e:
        print(f"❌ Could not parse collectionView as JSON: {e}")
else:
    print("❌ collectionView block not found in HTML.")

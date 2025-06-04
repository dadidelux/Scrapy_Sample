from bs4 import BeautifulSoup
import re
import json

with open("beis_all.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Try to find any large JSON-like array/object in any <script> tag
found = False
saved = False
for script in soup.find_all("script"):
    if not script.string:
        continue
    # Look for a large array or object
    matches = re.findall(r'(\[\s*\{.+?\}\s*\])', script.string, re.DOTALL)
    for m in matches:
        if len(m) > 1000:  # likely product data
            print("\n--- Found large JSON-like array in a <script> tag ---")
            print(m[:500] + ("..." if len(m) > 500 else ""))
            # Save the raw string as-is
            with open("beis_products_raw.txt", "w", encoding="utf-8") as raw_f:
                raw_f.write(m)
            print("\n💾 Saved raw matched string to beis_products_raw.txt")
            try:
                data = json.loads(re.sub(r',\s*([\]}])', r'\1', m))
                print(f"\n✅ Parsed array with {len(data)} items. Preview:")
                print(json.dumps(data[0], indent=2))
                with open("beis_products_extracted.json", "w", encoding="utf-8") as out_f:
                    json.dump(data, out_f, ensure_ascii=False, indent=2)
                print("\n💾 Saved extracted data to beis_products_extracted.json")
                saved = True
            except Exception as e:
                print(f"❌ Could not parse as JSON: {e}")
            found = True
    # Also look for large objects
    matches = re.findall(r'(\{\s*\"[\w-]+\"\s*:\s*.+?\})', script.string, re.DOTALL)
    for m in matches:
        if len(m) > 1000:
            print("\n--- Found large JSON-like object in a <script> tag ---")
            print(m[:500] + ("..." if len(m) > 500 else ""))
            try:
                data = json.loads(re.sub(r',\s*([\]}])', r'\1', m))
                print(f"\n✅ Parsed object with {len(data)} keys. Preview:")
                print(json.dumps(list(data.items())[:3], indent=2))
                with open("beis_products_extracted.json", "w", encoding="utf-8") as out_f:
                    json.dump(data, out_f, ensure_ascii=False, indent=2)
                print("\n💾 Saved extracted data to beis_products_extracted.json")
                saved = True
            except Exception as e:
                print(f"❌ Could not parse as JSON: {e}")
            found = True
# --- Extract the exact rawProducts assignment as a raw string ---
# --- Robust extraction of the exact rawProducts array as a raw string ---
for script in soup.find_all("script"):
    if not script.string:
        continue
    assign_str = "slideruleData.collection.rawProducts"
    idx = script.string.find(assign_str)
    if idx == -1:
        continue
    # Find the start of the array
    arr_start = script.string.find('[', idx)
    if arr_start == -1:
        continue
    # Bracket matching to find the end of the array
    depth = 0
    for i in range(arr_start, len(script.string)):
        c = script.string[i]
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                arr_end = i
                break
    else:
        continue  # No matching closing bracket found
    raw_products = script.string[arr_start:arr_end+1]
    with open("beis_raw_products_array.txt", "w", encoding="utf-8") as f:
        f.write(raw_products)
    print("\n💾 Saved exact raw slideruleData.collection.rawProducts array to beis_raw_products_array.txt")
    break
if not found:
    print("❌ No large JSON-like arrays or objects found in <script> tags. Try searching for product data in a different way.")

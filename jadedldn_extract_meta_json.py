import re
import json

# HTML_FILE = 'Scrapy_Sample/jadedldn_mens_all.html'
HTML_FILE = 'jadedldn_products_all.html'
# OUTPUT_JSON = 'Scrapy_Sample/jadedldn_html_embedded.json'
OUTPUT_JSON = 'jadedldn_html_embedded_all.json'

# Read the HTML file
with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# Find the start of the meta object
def find_meta_object(text):
    match = re.search(r'var meta\s*=\s*({)', text)
    if not match:
        raise ValueError('meta object not found')
    start = match.start(1)
    # Now extract the JS object by matching braces
    brace_count = 0
    in_string = False
    string_char = ''
    escape = False
    for i in range(start, len(text)):
        c = text[i]
        if in_string:
            if escape:
                escape = False
            elif c == '\\':
                escape = True
            elif c == string_char:
                in_string = False
        else:
            if c in ('"', "'"):
                in_string = True
                string_char = c
            elif c == '{':
                brace_count += 1
            elif c == '}':
                brace_count -= 1
                if brace_count == 0:
                    return text[start:i+1]
    raise ValueError('Could not extract meta object')

meta_js = find_meta_object(html)

# Clean up JS object to make it valid JSON
def js_object_to_json(js_obj):
    # Remove newlines and tabs for easier regex
    js_obj = js_obj.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    # Remove comments
    js_obj = re.sub(r'/\*.*?\*/', '', js_obj)
    js_obj = re.sub(r'//.*?\n', '', js_obj)
    # Replace single quotes with double quotes
    js_obj = re.sub(r"'", '"', js_obj)
    # Add quotes around unquoted keys
    js_obj = re.sub(r'([,{]\s*)([a-zA-Z0-9_\-]+)\s*:', r'\1"\2":', js_obj)
    # Remove trailing commas
    js_obj = re.sub(r',\s*([}\]])', r'\1', js_obj)
    return js_obj

meta_json_str = js_object_to_json(meta_js)
# Remove accidental double double-quotes
meta_json_str = re.sub(r'""+', '"', meta_json_str)

# Try to parse and pretty-print
try:
    meta_json = json.loads(meta_json_str)
except Exception as e:
    print('Error parsing JSON:', e)
    # Print context around the error location if available
    if hasattr(e, 'pos'):
        pos = e.pos
        context = 100
        print('Context around error:')
        print(meta_json_str[max(0, pos-context):pos+context])
    with open('meta_raw.json', 'w', encoding='utf-8') as f:
        f.write(meta_json_str)
    raise

with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(meta_json, f, indent=2, ensure_ascii=False)

print(f"Extracted meta object to {OUTPUT_JSON}")

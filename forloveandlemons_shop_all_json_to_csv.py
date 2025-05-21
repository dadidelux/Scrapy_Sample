import json
import pandas as pd
import re

# Load JSON file
with open("forloveandlemons_lingerie_shop_all_full.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Normalize the top-level fields but keep nested structures like 'variants' and 'metafields'
df = pd.json_normalize(data)

# Flatten 'metafields' so each key becomes its own column, using namespace and key for uniqueness
if 'metafields' in df.columns:
    def flatten_metafields(mf):
        flat = {}
        if isinstance(mf, list):
            for d in mf:
                if isinstance(d, dict):
                    ns = d.get('namespace', '')
                    key = d.get('key', '')
                    col = f"metafields_{ns}_{key}" if ns and key else None
                    if col:
                        val = d.get('value')
                        if key == 'ReviewsWidgetSnippet' and isinstance(val, str):
                            # Try to extract embedded JSON from <script type="application/json">...</script>
                            match = re.search(r'<script[^>]+type="application/json"[^>]*>(.*?)</script>', val, re.DOTALL)
                            if match:
                                try:
                                    extracted_json = json.loads(match.group(1))
                                    flat[col] = json.dumps(extracted_json, ensure_ascii=False)
                                except json.JSONDecodeError:
                                    flat[col] = val  # fallback: keep raw HTML if JSON is broken
                            else:
                                flat[col] = val  # no script tag found, keep original
                        else:
                            if isinstance(val, dict):
                                val = json.dumps(val, ensure_ascii=False)
                            flat[col] = val
        return flat

    metafields_df = df['metafields'].apply(flatten_metafields).apply(pd.Series)
    df = pd.concat([df.drop(columns=['metafields']), metafields_df], axis=1)

# Flatten 'variants' to JSON string for CSV output
if 'variants' in df.columns:
    df['variants'] = df['variants'].apply(lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, list) else "")

# Save all columns to CSV
df.to_csv("forloveandlemons_lingerie_shop_all_full.csv", index=False)

# Display a preview
print(df.head())

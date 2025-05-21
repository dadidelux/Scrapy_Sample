import json
import pandas as pd

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
                        # For ReviewsWidgetSnippet, just dump the JSON string as is
                        if key == 'ReviewsWidgetSnippet' and isinstance(val, str):
                            flat[col] = val
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
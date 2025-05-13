import json
import pandas as pd

# Load JSON file
with open("forloveandlemons_lingerie_full.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Normalize the top-level fields but keep nested structures like 'variants' and 'metafields'
df = pd.json_normalize(data)

# Select the first 22 columns only
df_base_22 = df.iloc[:, :22]

# Save to CSV if needed
df_base_22.to_csv("forloveandlemons_lingerie_full.csv", index=False)

# Display a preview
print(df_base_22.head())
# scripts/fetch_coincap.py
import requests
import os
from datetime import datetime

TOKEN = os.getenv("COINCAP_TOKEN")
URL = "https://rest.coincap.io/v3/assets"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

response = requests.get(URL, headers=headers)
response.raise_for_status()

data = response.json()
today = datetime.utcnow().strftime("%Y-%m-%d")

output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

with open(f"{output_dir}/coincap_{today}.json", "w", encoding="utf-8") as f:
    import json
    json.dump(data, f, indent=2)

print(f"✅ Saved data to data/coincap_{today}.json")

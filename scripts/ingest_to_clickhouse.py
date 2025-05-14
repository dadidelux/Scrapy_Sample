import os
import json
import datetime
from clickhouse_driver import Client

# Load env vars from GitHub secrets
host = os.getenv("CH_HOST")
port = 9000
user = os.getenv("CH_USERNAME")
password = os.getenv("CH_PASSWORD")
database = os.getenv("CH_DB")

print("🔍 ClickHouse connection info:")
print(f"  Host     : {host}")
print(f"  Port     : {port}")
print(f"  User     : {user}")
print(f"  Database : {database}")
print(f"  Password : {'(hidden)' if password else '(missing)'}")

required_vars = {
    "CH_HOST": host,
    "CH_PORT": port,
    "CH_USER": user,
    "CH_PASSWORD": password,
    "CH_DATABASE": database
}

missing = [key for key, val in required_vars.items() if not val]
if missing:
    raise EnvironmentError(f"❌ Missing required environment variables: {', '.join(missing)}")


# Load today's JSON file
today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
with open(f"data/coincap_{today}.json", "r", encoding="utf-8") as f:
    data = json.load(f)["data"]

# Connect to ClickHouse
client = Client(host=host, port=port, user=user, password=password, database=database)

# Create table if not exists
client.execute("""
CREATE TABLE IF NOT EXISTS coincap_assets (
    id String,
    rank UInt32,
    symbol String,
    name String,
    supply Float64,
    maxSupply Nullable(Float64),
    marketCapUsd Float64,
    volumeUsd24Hr Float64,
    priceUsd Float64,
    changePercent24Hr Float64,
    vwap24Hr Nullable(Float64),
    explorer Nullable(String),
    date Date DEFAULT today()
) ENGINE = MergeTree()
ORDER BY (date, rank)
""")

# Prepare and insert data
rows = [
    (
        asset["id"],
        int(asset["rank"]),
        asset["symbol"],
        asset["name"],
        float(asset["supply"]),
        float(asset["maxSupply"]) if asset["maxSupply"] else None,
        float(asset["marketCapUsd"]),
        float(asset["volumeUsd24Hr"]),
        float(asset["priceUsd"]),
        float(asset["changePercent24Hr"]),
        float(asset["vwap24Hr"]) if asset["vwap24Hr"] else None,
        asset["explorer"] or None
    )
    for asset in data
]

client.execute("""
INSERT INTO coincap_assets (
    id, rank, symbol, name, supply, maxSupply, marketCapUsd,
    volumeUsd24Hr, priceUsd, changePercent24Hr, vwap24Hr, explorer
)
VALUES
""", rows)

print(f"✅ Inserted {len(rows)} records into ClickHouse.")

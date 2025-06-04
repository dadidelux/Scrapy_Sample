import requests

url = "https://beistravel.com/collections/all"
headers = {"User-Agent": "Mozilla/5.0"}

resp = requests.get(url, headers=headers)
resp.raise_for_status()

with open("beis_all.html", "w", encoding="utf-8") as f:
    f.write(resp.text)

print("✅ HTML downloaded and saved as beis_all.html")

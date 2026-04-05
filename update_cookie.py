import requests
import json

URL = "https://raw.githubusercontent.com/Prtstream820894/prtstreams/refs/heads/main/ptt.m3u"

response = requests.get(URL)
lines = response.text.splitlines()

channels = []

for i in range(len(lines)):
    if lines[i].startswith("#EXTINF"):
        name = lines[i].split(",")[-1]
        url = lines[i+1]

        channels.append({
            "name": name,
            "logo": "",
            "group": "Live",
            "url": url
        })

with open("data.json", "w", encoding="utf-8") as f:
    json.dump({"channels": channels}, f, indent=2)

print("✅ JSON Created")

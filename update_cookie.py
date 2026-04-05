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

# Save JSON
with open("data.json", "w", encoding="utf-8") as f:
    json.dump({"channels": channels}, f, indent=2)

print("✅ JSON Created")import requests
from datetime import datetime

URL = "https://raw.githubusercontent.com/Prtstream820894/prtstreams/refs/heads/main/ptt.m3u"

try:
    r = requests.get(URL)
    data = r.text

    with open("min.m3u", "w", encoding="utf-8") as f:
        f.write(data)

    print("✅ Updated:", datetime.now())

except Exception as e:
    print("❌ Error:", e)

import requests

JSON_URL = "https://jtvp.byethost14.com/channels.json"
OUTPUT = "playlist.m3u"

res = requests.get(JSON_URL)
data = res.json()

m3u = "#EXTM3U\n"

for ch in data:
    name = ch.get("name", "Unknown")
    logo = ch.get("logo", "")
    group = ch.get("category", "Live")
    url = ch.get("url", "")

    m3u += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
    m3u += f"{url}\n"

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(m3u)

print("✅ M3U file created: playlist.m3u")

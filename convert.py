import requests

JSON_URL = "https://api.allorigins.win/raw?url=https://jtvp.byethost14.com/channels.json"
OUTPUT = "playlist.m3u"

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(JSON_URL, headers=headers)
data = res.json()

m3u = '#EXTM3U x-tvg-url="https://iptv-org.github.io/epg/guides/in.xml"\n'

for ch in data:
    name = ch.get("name", "No Name")
    logo = ch.get("logo", "")
    group = ch.get("category", "Live")
    url = ch.get("url", "")

    if not url:
        continue

    m3u += f'#EXTINF:-1 tvg-id="{name}" tvg-logo="{logo}" group-title="{group}",{name}\n'
    m3u += f"{url}\n"

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(m3u)

print("✅ M3U + EPG Ready")

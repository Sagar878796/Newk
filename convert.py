import requests

url = "https://jtvp.byethost14.com/channels.json"
output = "playlist.m3u"

res = requests.get(url)

if res.status_code != 200:
    print("Failed to fetch JSON")
    exit(1)

data = res.json()

m3u = "#EXTM3U\n"

for ch in data:
    name = ch.get("name", "No Name")
    logo = ch.get("logo", "")
    group = ch.get("category", "Live")
    link = ch.get("url", "")

    if not link:
        continue

    m3u += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
    m3u += f"{link}\n"

with open(output, "w", encoding="utf-8") as f:
    f.write(m3u)

print("Done")

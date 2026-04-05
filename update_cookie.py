import json
import requests
import re

M3U_URL = "https://raw.githubusercontent.com/Prtstream820894/prtstreams/refs/heads/main/ptt.m3u"
OUTPUT = "data.json"

res = requests.get(M3U_URL)
lines = res.text.splitlines()

channels = []

i = 0
while i < len(lines):
    line = lines[i].strip()

    if line.startswith("#EXTINF"):
        name = line.split(",")[-1].strip()

        logo = re.search(r'tvg-logo="([^"]+)"', line)
        group = re.search(r'group-title="([^"]+)"', line)

        logo = logo.group(1) if logo else ""
        category = group.group(1) if group else "Live"

        cookie = ""
        user_agent = ""
        drm_key = ""
        drm_id = ""
        url = ""

        for j in range(i+1, min(i+10, len(lines))):
            l = lines[j].strip()

            if "#EXTHTTP" in l and "cookie" in l:
                try:
                    cookie = l.split('cookie":"')[1].split('"')[0]
                except:
                    pass

            if "user-agent" in l.lower():
                try:
                    user_agent = l.split("=")[-1].split("&")[0]
                except:
                    pass

            if "license_key" in l:
                try:
                    parts = l.split("=")[-1]
                    drm_id, drm_key = parts.split(":")
                except:
                    pass

            if l.startswith("http"):
                url = l.split("?")[0]
                break

        if url:
            channel = {
                "name": name,
                "logo": logo,
                "category": category,
                "url": url,
                "headers": {
                    "cookie": cookie,
                    "user-agent": user_agent
                }
            }

            if drm_key:
                channel["drm"] = {
                    "key_id": drm_id,
                    "key": drm_key
                }

            channels.append(channel)

    i += 1

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump({"channels": channels}, f, indent=2)

print("✅ Advanced JSON Created")
print("🔥 Channels:", len(channels))

import json
import requests
import re

M3U_URL = "https://raw.githubusercontent.com/Prtstream820894/prtstreams/refs/heads/main/ptt.m3u"

JSON_OUTPUT = "data.json"
M3U_OUTPUT = "output.m3u"

# =========================
# 🔹 M3U ➝ JSON
# =========================
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

# Save JSON
with open(JSON_OUTPUT, "w", encoding="utf-8") as f:
    json.dump({"channels": channels}, f, indent=2)

print("✅ JSON Created")
print("🔥 Channels:", len(channels))


# =========================
# 🔹 JSON ➝ M3U
# =========================

with open(JSON_OUTPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

channels = data.get("channels", [])

m3u_lines = ["#EXTM3U"]

for ch in channels:
    name = ch.get("name", "")
    logo = ch.get("logo", "")
    group = ch.get("category", "Live")
    url = ch.get("url", "")

    headers = ch.get("headers", {})
    cookie = headers.get("cookie", "")
    user_agent = headers.get("user-agent", "")

    drm = ch.get("drm", {})
    drm_id = drm.get("key_id", "")
    drm_key = drm.get("key", "")

    # EXTINF
    extinf = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}'
    m3u_lines.append(extinf)

    # Headers
    if cookie or user_agent:
        header = "#EXTHTTP:{"
        if cookie:
            header += f'"cookie":"{cookie}"'
        if user_agent:
            if cookie:
                header += ","
            header += f'"user-agent":"{user_agent}"'
        header += "}"
        m3u_lines.append(header)

    # DRM
    if drm_key:
        m3u_lines.append(f'#KODIPROP:inputstream.adaptive.license_key={drm_id}:{drm_key}')

    # URL
    m3u_lines.append(url)

# Save M3U
with open(M3U_OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(m3u_lines))

print("✅ M3U Created")

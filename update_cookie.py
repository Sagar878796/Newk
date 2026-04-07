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

print("✅ M3U file created: playlist.m3u")        for j in range(i+1, min(i+10, len(lines))):
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

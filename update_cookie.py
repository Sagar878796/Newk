import requests
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

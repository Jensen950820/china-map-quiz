"""Rebuild all province map.html files from Apple light/dark template."""

import os, re, json

BASE = r"C:\Users\user\Desktop\共享文件夹\【项目与工具】\【代码-暂存】\互动地图"

with open(os.path.join(BASE, "build_all.py"), "r", encoding="utf-8") as f:
    fc = f.read()

m = re.search(
    r'HTML_TEMPLATE = """(.*?)"""\s*\nfor adc, short, full in PROVINCES:', fc, re.DOTALL
)
tpl = m.group(1)

prov_matches = re.findall(r'\((\d+),\s*"([^"]+)",\s*"([^"]+)"\)', fc)
PROVINCES = [(int(a), s, f) for a, s, f in prov_matches]

for adc, short, full in PROVINCES:
    folder = os.path.join(BASE, short)
    hp = os.path.join(folder, "map.html")
    dp = os.path.join(folder, "gd_data.js")
    if not os.path.exists(hp) or not os.path.exists(dp):
        print(f"  SKIP {short}")
        continue
    with open(hp, "r", encoding="utf-8") as f:
        old = f.read()
    dm = re.search(
        r"DEF\s*=\s*\{\s*lonMin:\s*([\d.]+)\s*,\s*lonMax:\s*([\d.]+)\s*,\s*latMin:\s*([\d.]+)\s*,\s*latMax:\s*([\d.]+)\s*,\s*scale:\s*(\d+)",
        old,
    )
    if not dm:
        print(f"  FAIL {short}: no DEF")
        continue
    lomn, lomx, lamn, lamx = float(dm[1]), float(dm[2]), float(dm[3]), float(dm[4])
    sc = int(dm[5])
    with open(dp, "r", encoding="utf-8") as f:
        dc = f.read()
    jm = re.search(r"const GD_PREFECTURES\s*=\s*(.+);\s*$", dc, re.DOTALL)
    data = json.loads(jm.group(1))
    n = len(data.get("features", []))
    cap = data["features"][0]["properties"]["adcode"] if data.get("features") else adc
    html = tpl.format(
        full_name=full,
        short_name=short,
        total_pref=n,
        capital=cap,
        lon_min=lomn,
        lon_max=lomx,
        lat_min=lamn,
        lat_max=lamx,
        scale=sc,
    )
    with open(hp, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  OK {short}: {n} pref")

print(f"\nDone: {len(PROVINCES)} provinces")

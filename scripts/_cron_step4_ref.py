import json, os, datetime

for fn in ['reports/daily/2026-08-05.json', 'reports/daily/2026-08-03.json']:
    p = os.path.join('/home/pin/aI-product-daily-peport', fn)
    st = os.stat(p)
    print(f"=== {fn} | mtime={datetime.datetime.fromtimestamp(st.st_mtime)} size={st.st_size}")
    with open(p) as f:
        d = json.load(f)
    print("keys:", list(d.keys()))
    print("date:", d.get('date'), "| generatedAt:", d.get('generatedAt'), "| productCount:", d.get('productCount'))
    for prod in d.get('products', []):
        print("  -", prod.get('id'), "|", prod.get('name'), "|", prod.get('url'), "| type:", prod.get('type'))
        print("    tags:", prod.get('tags'), "| src:", prod.get('sourceChannels'))
        an = prod.get('analysis') or {}
        print("    analysis keys:", list(an.keys()))

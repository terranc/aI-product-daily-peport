import json

with open('data/raw-candidates.json') as f:
    raw = json.load(f)
cand_ids = {c['product_id'] for c in raw['products']}

with open('reports/daily/2026-08-05.json') as f:
    report = json.load(f)

print("report date:", report['date'], "| count:", report['productCount'])
ok = True
for p in report['products']:
    pid = p['id']
    match = pid in cand_ids
    if not match:
        ok = False
    print(f"  {'OK ' if match else 'BAD'} {pid} | {p['name']} | {p['type']} | shot={bool(p.get('screenshotUrl'))} | appstore_imgs={len(p.get('appStoreScreenshots') or [])}")
print("ALL IDS MATCH RAW CANDIDATES:", ok)

with open('data/products.json') as f:
    db = json.load(f)
print("db total:", len(db['products']), "| lastUpdated:", db.get('lastUpdated'))

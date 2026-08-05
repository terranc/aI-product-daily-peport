import json
from collections import Counter

with open('data/raw-candidates.json') as f:
    raw = json.load(f)

if isinstance(raw, dict):
    print("raw keys:", list(raw.keys()))
    candidates = raw.get('candidates') or raw.get('products') or raw.get('items') or []
else:
    candidates = raw

print("candidates count:", len(candidates))
if candidates:
    print("sample keys:", list(candidates[0].keys()))
    print(json.dumps(candidates[0], ensure_ascii=False)[:600])

channels = Counter(c.get('sourceChannel') or c.get('channel') or 'unknown' for c in candidates)
print("by channel:", dict(channels))

with open('data/products.json') as f:
    db = json.load(f)
print("db type:", type(db).__name__)
if isinstance(db, dict):
    print("db keys:", list(db.keys()))
    prods = db.get('products', [])
else:
    prods = db
print("db product count:", len(prods))
if prods:
    print("db sample keys:", list(prods[0].keys()))
    print(json.dumps(prods[0], ensure_ascii=False)[:600])

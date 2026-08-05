import json
from datetime import datetime, timezone

with open('data/raw-candidates.json') as f:
    raw = json.load(f)
candidates = raw['products']

with open('data/products.json') as f:
    db = json.load(f)
prods = db['products']

now = datetime.now(timezone.utc)
now_ts = now.timestamp()

# Build lookup: product_id -> cooldownExpiresAt (ISO string)
dup_ids = set()
for p in prods:
    pid = p.get('id')
    cde = p.get('cooldownExpiresAt')
    if not pid:
        continue
    if cde:
        try:
            exp = datetime.fromisoformat(cde.replace('Z', '+00:00'))
            if exp > now:
                dup_ids.add(pid)
        except Exception:
            dup_ids.add(pid)  # can't parse -> treat as active
    else:
        dup_ids.add(pid)

print(f"DB products: {len(prods)}, active cooldown ids: {len(dup_ids)}")

# Also: exclude if a product with same URL or name was featured within last 14 days via metrics.lastFeaturedDate
recent_featured = set()
from datetime import timedelta
cutoff = (now - timedelta(days=14)).date().isoformat()
for p in prods:
    m = p.get('metrics') or {}
    lfd = m.get('lastFeaturedDate')
    if lfd and lfd >= cutoff:
        recent_featured.add(p.get('id'))

print(f"Recently featured (14d): {len(recent_featured)}")

dups = []
fresh = []
for c in candidates:
    pid = c.get('product_id')
    if pid in dup_ids or pid in recent_featured:
        dups.append(c)
    else:
        fresh.append(c)

print(f"Total: {len(candidates)}, dup: {len(dups)}, fresh: {len(fresh)}")
print("\n-- DUPLICATES --")
for c in dups:
    print(f"  {c.get('product_id')} | {c.get('name','')[:60]}")

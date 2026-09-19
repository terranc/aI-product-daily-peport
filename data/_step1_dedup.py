import json
from datetime import datetime, timezone, timedelta

# Read raw candidates
with open('/home/pin/aI-product-daily-peport/data/raw-candidates.json', 'r') as f:
    raw = json.load(f)
candidates = raw['products']

# Read products database
with open('/home/pin/aI-product-daily-peport/data/products.json', 'r') as f:
    db = json.load(f)
db_products = db['products']

now = datetime.now(timezone.utc)

# Build set of product_ids with active cooldown
active_ids = set()
for p in db_products:
    pid = p.get('id', '')
    cooldown = p.get('cooldownExpiresAt')
    if cooldown:
        try:
            cd = datetime.fromisoformat(cooldown.replace('Z', '+00:00'))
            if cd > now:
                active_ids.add(pid)
        except:
            pass

print(f"DB products: {len(db_products)}")
print(f"Active cooldown IDs: {len(active_ids)}")
print(f"Raw candidates: {len(candidates)}")

# Deduplicate
deduped = []
for c in candidates:
    pid = c.get('product_id', '')
    if pid and pid not in active_ids:
        deduped.append(c)

print(f"After dedup: {len(deduped)}")

# Save deduped for next step
with open('/home/pin/aI-product-daily-peport/data/_deduped.json', 'w') as f:
    json.dump(deduped, f, ensure_ascii=False, indent=2)

# Print all deduped candidates for analysis
for i, c in enumerate(deduped):
    name = c.get('name', '')[:120]
    desc = c.get('description', '')[:300].replace('\n', ' ')
    source = c.get('source', '')
    score = c.get('score', 0)
    url = c.get('url', '')[:120]
    pid = c.get('product_id', '')
    print(f"\n[{i}] [{source}] score={score}")
    print(f"  PID: {pid}")
    print(f"  Name: {name}")
    print(f"  Desc: {desc}")
    print(f"  URL: {url}")

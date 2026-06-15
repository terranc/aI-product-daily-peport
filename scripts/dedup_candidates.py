import json
import os
from datetime import datetime, timedelta

DATA_DIR = '/Volumes/EXTEND/aI-product-daily-peport/data'
RAW_FILE = os.path.join(DATA_DIR, 'raw-candidates.json')
DB_FILE = os.path.join(DATA_DIR, 'products.json')

# Load raw candidates
with open(RAW_FILE, 'r', encoding='utf-8') as f:
    raw_data = json.load(f)
    
# Load product database
with open(DB_FILE, 'r', encoding='utf-8') as f:
    db_data = json.load(f)

products = db_data.get('products', [])
    candidates = raw_data.get('products', [])

# Get IDs of products in DB that are still in cooldown
active_cooldowns = set()
now = datetime.utcnow()

for p in products:
    if p.get('cooldownExpiresAt'):
        try:
            # Handle ISO format
            exp_str = p['cooldownExpiresAt'].replace('Z', '+00:00')
            # Simple parsing for ISO format
            if '+' in exp_str:
                exp = datetime.fromisoformat(exp_str)
            else:
                exp = datetime.fromisoformat(exp_str)
            
            if exp > now:
                active_cooldowns.add(p['id'])
        except:
            pass

print(f"Total candidates: {len(candidates)}")
print(f"Active cooldowns in DB: {len(active_cooldowns)}")

new_candidates = []
for c in candidates:
    pid = c.get('product_id')
    if pid and pid not in active_cooldowns:
        new_candidates.append(c)

print(f"New candidates after dedup: {len(new_candidates)}")

# Output new candidates for analysis (limit to top 30 for manageable context)
print("\n--- NEW CANDIDATES ---")
for i, c in enumerate(new_candidates[:30]):
    print(f"\n[IDX:{i}]")
    print(f"ID: {c.get('product_id')}")
    print(f"Source: {c.get('source')}")
    print(f"Name: {c.get('title', c.get('name'))}")
    print(f"URL: {c.get('url')}")
    print(f"Desc: {c.get('description', c.get('text'))[:200]}")
    print(f"Score: {c.get('score', c.get('heat'))}")

import json
import os
from datetime import datetime, timezone

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
now = datetime.now(timezone.utc)

for p in products:
        exp_str = p.get('cooldownExpiresAt')
        if exp_str:
            try:
                # Normalize ISO format
                if 'Z' in exp_str:
                    exp_str = exp_str.replace('Z', '+00:00')
                # If no timezone info, assume UTC
                if '+' not in exp_str and '-' not in exp_str[10:]:
                    exp_str += '+00:00'
                exp = datetime.fromisoformat(exp_str)
                if exp > now:
                    active_cooldowns.add(p['id'])
            except Exception as e:
                print(f"Warning: Could not parse date {exp_str} for {p['id']}: {e}")

print(f"Total candidates: {len(candidates)}")
print(f"Active cooldowns in DB: {len(active_cooldowns)}")

new_candidates = []
for c in candidates:
    pid = c.get('product_id')
    if pid and pid not in active_cooldowns:
        new_candidates.append(c)

print(f"New candidates after dedup: {len(new_candidates)}")

# Output new candidates for analysis
print("\n--- NEW CANDIDATES FOR ANALYSIS ---")
for i, c in enumerate(new_candidates):
    print(f"\n[IDX:{i}]")
    print(f"ID: {c.get('product_id')}")
    print(f"Source: {c.get('source')}")
    print(f"Name: {c.get('title', c.get('name'))}")
    print(f"URL: {c.get('url')}")
    # Clean description for LLM analysis
    desc = c.get('description', c.get('text', '')).replace('\n', ' ')[:300]
    print(f"Desc: {desc}")
    print(f"Score: {c.get('score', c.get('heat'))}")

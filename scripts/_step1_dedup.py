#!/usr/bin/env python3
"""AI Product Radar - Daily Analysis Pipeline"""
import json, os, re, time
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
NOW = datetime.now(CST)
TODAY = NOW.strftime('%Y-%m-%d')

# Read raw candidates
with open('data/raw-candidates.json') as f:
    raw_data = json.load(f)

if isinstance(raw_data, dict) and 'products' in raw_data:
    candidates = raw_data['products']
elif isinstance(raw_data, list):
    candidates = raw_data
elif isinstance(raw_data, dict):
    # Try to find any list value
    candidates = None
    for v in raw_data.values():
        if isinstance(v, list) and len(v) > 0:
            candidates = v
            break
    if candidates is None:
        candidates = [raw_data]
else:
    candidates = []

print(f"Total candidates: {len(candidates)}")

# Read existing products DB
with open('data/products.json') as f:
    db_data = json.load(f)

if isinstance(db_data, dict) and 'products' in db_data:
    existing_products = db_data['products']
elif isinstance(db_data, list):
    existing_products = db_data
else:
    existing_products = []

print(f"Existing products in DB: {len(existing_products)}")

# Build set of existing product_ids with cooldown not expired
cooldown_threshold = NOW - timedelta(days=14)
existing_ids = set()
for p in existing_products:
    pid = p.get('id', '')
    cooldown = p.get('cooldownExpiresAt', '')
    if pid:
        existing_ids.add(pid)
        # Could also check cooldown, but for simplicity just dedup by ID

print(f"Existing product IDs: {len(existing_ids)}")

# Dedup candidates
new_candidates = []
for c in candidates:
    pid = c.get('product_id', c.get('id', ''))
    if pid and pid not in existing_ids:
        new_candidates.append(c)

print(f"After dedup: {len(new_candidates)} new candidates")

# Print first 5 for inspection
for i, c in enumerate(new_candidates[:5]):
    print(f"\n--- New Candidate {i+1} ---")
    print(f"ID: {c.get('product_id', c.get('id',''))}")
    print(f"Name: {c.get('name','')}")
    print(f"Description: {str(c.get('description',''))[:200]}")
    print(f"URL: {c.get('url','')}")
    print(f"Source: {c.get('source','')}")
    print(f"SourceChannel: {c.get('sourceChannel','')}")

# Save intermediate for inspection
with open('/tmp/new_candidates.json', 'w') as f:
    json.dump(new_candidates, f, ensure_ascii=False, indent=2)
print(f"\nSaved {len(new_candidates)} candidates to /tmp/new_candidates.json")

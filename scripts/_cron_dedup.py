#!/usr/bin/env python3
"""Cron dedup helper: dedupe raw candidates against product db cooldowns, dump compact list."""
import json
from datetime import datetime, timezone

with open('data/raw-candidates.json') as f:
    raw = json.load(f)
with open('data/products.json') as f:
    db = json.load(f)

cands = raw.get('products', [])
products = db.get('products', [])

now = datetime.now(timezone.utc)

def parse_ts(s):
    if not s:
        return None
    s = s.strip()
    # handle Z suffix
    if s.endswith('Z'):
        s = s[:-1] + '+00:00'
    try:
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None

# db ids with unexpired cooldown
active_ids = set()
for p in products:
    exp = parse_ts(p.get('cooldownExpiresAt'))
    if exp and exp > now:
        active_ids.add(p['id'])
    elif not exp:
        # fall back to addedAt within 14 days
        add = parse_ts(p.get('addedAt'))
        if add and (now - add).days < 14:
            active_ids.add(p['id'])

print('total candidates:', len(cands))
print('active cooldown ids in db:', len(active_ids))

seen = set()
fresh = []
for c in cands:
    pid = c.get('product_id') or c.get('id')
    if not pid:
        continue
    key = pid.lower()
    if key in seen:
        continue
    seen.add(key)
    if key in active_ids:
        continue
    fresh.append(c)

print('after dedup:', len(fresh))
print('=' * 100)
for i, c in enumerate(fresh, 1):
    desc = (c.get('description') or '').replace('\n', ' ').replace('\r', ' ').strip()
    print(f"[{i}] pid={c.get('product_id')} | src={c.get('source')} | score={c.get('score')} | ts={c.get('timestamp')}")
    print(f"    name: {c.get('name')}")
    print(f"    url: {c.get('url')}")
    print(f"    desc: {desc[:220]}")
    print()

with open('scripts/_cron_fresh_candidates.json', 'w') as f:
    json.dump(fresh, f, ensure_ascii=False, indent=2)
print('saved to scripts/_cron_fresh_candidates.json')

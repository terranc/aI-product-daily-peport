#!/usr/bin/env python3
"""List all producthunt candidate ids in raw-candidates.json."""
import json

with open('data/raw-candidates.json') as f:
    raw = json.load(f)
cands = raw.get('products', [])

for c in cands:
    if c.get('source') == 'producthunt':
        print(repr(c.get('product_id')), '|', c.get('name'))

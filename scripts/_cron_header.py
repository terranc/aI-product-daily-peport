#!/usr/bin/env python3
"""Dump current raw-candidates.json header info."""
import json

with open('data/raw-candidates.json') as f:
    raw = json.load(f)
print('fetchedAt:', raw.get('fetchedAt'))
print('totalCount:', raw.get('totalCount'))
print('channels:', raw.get('channels'))
cands = raw.get('products', [])
print('actual products len:', len(cands))
from collections import Counter
print('sources:', Counter(c.get('source') for c in cands))
# check a PH-style pid presence
print('has producthunt pid:', any('producthunt' in (c.get('product_id') or '') for c in cands))

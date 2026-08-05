#!/usr/bin/env python3
"""Cron inspection helper: dump structure of raw-candidates.json and products.json"""
import json, sys

def load(path):
    with open(path) as f:
        return json.load(f)

raw = load('data/raw-candidates.json')
db = load('data/products.json')

print('raw type:', type(raw).__name__)
if isinstance(raw, dict):
    print('raw keys:', list(raw.keys()))
    cands = raw.get('candidates') or raw.get('products') or raw.get('items') or []
else:
    cands = raw
print('candidates count:', len(cands))
if cands:
    print('cand keys:', list(cands[0].keys()))
    print('cand sample:', json.dumps(cands[0], ensure_ascii=False)[:2000])
print()
print('db type:', type(db).__name__)
if isinstance(db, dict):
    print('db keys:', list(db.keys()))
    products = db.get('products', [])
else:
    products = db
print('db products count:', len(products))
if products:
    print('db product keys:', list(products[0].keys()))
    print('db sample:', json.dumps(products[0], ensure_ascii=False)[:1200])

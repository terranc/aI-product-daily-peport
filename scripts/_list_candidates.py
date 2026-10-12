#!/usr/bin/env python3
"""Print all new candidates for analysis"""
import json

with open('/tmp/new_candidates.json') as f:
    candidates = json.load(f)

for i, c in enumerate(candidates):
    print(f"=== Candidate {i+1} ===")
    print(f"ID: {c.get('product_id', c.get('id',''))}")
    print(f"Name: {c.get('name','')}")
    print(f"Description: {str(c.get('description',''))[:300]}")
    print(f"URL: {c.get('url','')}")
    print(f"Source: {c.get('source','')}")
    print(f"SourceChannel: {c.get('sourceChannel','')}")
    print(f"热度/Score: {c.get('heat', c.get('score',''))}")
    print()

print(f"Total: {len(candidates)} candidates")

#!/usr/bin/env python3
"""Extract full candidate records for chosen product_ids + resolve gesture.live."""
import json
import urllib.request

with open('data/raw-candidates.json') as f:
    raw = json.load(f)
cands = raw.get('products', [])

targets = [
    "producthunt.com/r/p/1215391",   # Hansel
    "producthunt.com/r/p/1214897",   # Wispr Flow Notetaker
    "producthunt.com/r/p/1203025",   # Driven
    "vocab.top",                     # Vocab Top
    "heybraza.com",                  # HeyBraza
    "producthunt.com/r/p/1212852",   # gesture.live (resolve check)
]

for c in cands:
    pid = c.get('product_id')
    if pid and any(pid == t or pid.startswith(t) for t in targets):
        print(json.dumps(c, ensure_ascii=False, indent=1)[:1200])
        print('---')

# resolve gesture.live
url = "https://www.producthunt.com/r/p/1212852?app_id=339"
try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=20)
    print("gesture.live 1212852 ->", resp.geturl())
except Exception as e:
    print("gesture.live 1212852 -> ERROR:", e)

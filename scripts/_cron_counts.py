#!/usr/bin/env python3
"""Count candidates by source."""
import json

with open('data/raw-candidates.json') as f:
    raw = json.load(f)
cands = raw.get('products', [])
print('total:', len(cands))
from collections import Counter
c = Counter(x.get('source') for x in cands)
print(c)
# print first 3 product_ids
for x in cands[:3]:
    print(repr(x.get('product_id')), x.get('source'))
# find any item whose product_id contains 'producthunt'
ph = [x for x in cands if 'producthunt' in (x.get('product_id') or '').lower()]
print('with producthunt in pid:', len(ph))
hn = [x for x in cands if x.get('source') == 'hackernews']
print('hn count:', len(hn))
print('hn sample:', hn[0].get('product_id') if hn else None)

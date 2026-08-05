#!/usr/bin/env python3
"""Check snapshot file contents and data dir."""
import json, os
from collections import Counter

d = json.load(open('scripts/_cron_fresh_candidates.json'))
print('snapshot count:', len(d))
print('snapshot sources:', Counter(x.get('source') for x in d))

print('\ndata dir:')
for f in sorted(os.listdir('data')):
    p = os.path.join('data', f)
    print(f, os.path.getsize(p), os.path.getmtime(p))

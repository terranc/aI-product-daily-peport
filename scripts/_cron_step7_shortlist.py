import json

with open('data/raw-candidates.json') as f:
    raw = json.load(f)
candidates = raw['products']

# Shortlist indices from the dump
shortlist = [10, 17, 25, 42, 50, 60, 72, 75, 86, 87, 95, 97, 101, 105, 106, 107, 109, 110, 111, 112, 115, 121, 123, 124, 130, 13]
for i in shortlist:
    c = candidates[i]
    print(f"===== [{i}] {c.get('source')} pid={c.get('product_id')}")
    print(f"name: {c.get('name')}")
    print(f"url: {c.get('url')}")
    print(f"source_url: {c.get('source_url')}")
    print(f"score: {c.get('score')} | timestamp: {c.get('timestamp')}")
    desc = c.get('description') or ''
    print(f"description: {desc[:900]}")
    print()

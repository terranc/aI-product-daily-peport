import json

with open('data/raw-candidates.json') as f:
    raw = json.load(f)

candidates = raw['products']
print("channels meta:", json.dumps(raw.get('channels'), ensure_ascii=False)[:300])

for i, c in enumerate(candidates):
    desc = (c.get('description') or '').replace('\r', ' ').replace('\n', ' ').strip()
    if len(desc) > 110:
        desc = desc[:110] + '...'
    print(f"[{i}] src={c.get('source','?')} score={c.get('score','?')} pid={c.get('product_id','?')}")
    print(f"    name: {c.get('name','?')}")
    print(f"    url: {c.get('url','?')}")
    print(f"    desc: {desc}")

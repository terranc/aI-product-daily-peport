import json

# Read all deduped candidates
with open('/home/pin/aI-product-daily-peport/data/_deduped.json', 'r') as f:
    candidates = json.load(f)

# Build lookup by product_id
by_id = {c['product_id']: c for c in candidates}
by_name = {c.get('name', '').lower(): c for c in candidates}

# Find specific products of interest
keywords = ['mosmos', 'whaleread', 'stilltalk', 'infinomni', 'gametomac', 'foleyfy', 'dictivo', 'lokalbot', 'smartcheck', 'peelaway', 'bring them to life', 'duvi', 'productbridge', 'jobjet', 'lumotutor', 'findog']

for kw in keywords:
    for c in candidates:
        if kw.lower() in c.get('name', '').lower():
            print(f"=== {kw.upper()} ===")
            print(f"  PID: {c['product_id']}")
            print(f"  Name: {c.get('name', '')}")
            print(f"  Desc: {c.get('description', '')[:300]}")
            print(f"  URL: {c.get('url', '')}")
            print(f"  Source: {c.get('source', '')}")
            print()
            break

import json
import sys
sys.path.insert(0, '/home/pin/aI-product-daily-peport/scripts')

# Read candidates
with open('/home/pin/aI-product-daily-peport/data/_deduped.json', 'r') as f:
    candidates = json.load(f)

by_pid = {c['product_id']: c for c in candidates}

# Selected top 5 PIDs
selected_pids = [
    'producthunt.com/r/p/1251122',   # MosMos
    'peelaway.io',                    # Peelaway
    'producthunt.com/r/p/1252513',   # GameToMac
    'producthunt.com/r/p/1253717',   # StillTalk
    'v2ex.com/t/1243128',             # FinDog
]

print("=== SELECTED PRODUCTS ===")
for pid in selected_pids:
    c = by_pid[pid]
    print(f"\nPID: {pid}")
    print(f"Name: {c['name']}")
    print(f"Desc: {c['description'][:300]}")
    print(f"URL: {c['url']}")
    print(f"Source: {c['source']}")
    print(f"Score: {c['score']}")

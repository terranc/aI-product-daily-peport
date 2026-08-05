import subprocess, json

repo = '/home/pin/aI-product-daily-peport'

def run(cmd):
    r = subprocess.run(cmd, cwd=repo, capture_output=True, text=True)
    return r.stdout

# diff stat between HEAD and working tree for data/reports/docs
print("=== git diff --stat HEAD (data/reports/docs) ===")
print(run(['git', 'diff', '--stat', 'HEAD', '--', 'data/', 'reports/', 'docs/']))

# committed 08-05 report
print("=== committed HEAD report (git show HEAD:reports/daily/2026-08-05.json) ===")
out = run(['git', 'show', 'HEAD:reports/daily/2026-08-05.json'])
try:
    d = json.loads(out)
    for p in d.get('products', []):
        print(' -', p.get('id'), '|', p.get('name'))
except Exception as e:
    print("not a report or error:", e)

# last commit info
print("=== HEAD commit ===")
print(run(['git', 'log', '-1', '--format=%h %ci %s']))

# check if Hand Wave / CoachAI / 织诗 are in DB with cooldown
with open(repo + '/data/products.json') as f:
    db = json.load(f)
prods = db['products']
print("=== DB check for 21:01 report products ===")
targets = ['producthunt.com/r/p/1199610', 'producthunt.com/r/p/1211832', 'producthunt.com/r/p/1212654',
           'v2ex.com/t/1232192', 'producthunt.com/r/p/1206082']
for t in targets:
    hits = [p for p in prods if p.get('id') == t]
    for p in hits:
        print(f"  {t}: addedAt={p.get('addedAt')} cooldown={p.get('cooldownExpiresAt')} lastFeatured={ (p.get('metrics') or {}).get('lastFeaturedDate') }")

# how many products have lastFeaturedDate >= 2026-08-05
recent = [p for p in prods if (p.get('metrics') or {}).get('lastFeaturedDate') == '2026-08-05']
print(f"=== products with lastFeaturedDate 2026-08-05: {len(recent)} ===")
for p in recent:
    print('  -', p.get('id'), '|', p.get('name'))

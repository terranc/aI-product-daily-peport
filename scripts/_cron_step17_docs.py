import subprocess, json, os, glob

base = '/home/pin/aI-product-daily-peport/docs'

# list docs top-level
print("=== docs/ top level ===")
for name in sorted(os.listdir(base))[:30]:
    print(" ", name)

# find daily report files in docs
print("\n=== docs reports daily ===")
for p in sorted(glob.glob(base + '/**/2026-08-05*', recursive=True)):
    print(" ", p.replace(base, 'docs'))

# check index.html around Wispr
idx = open(base + '/index.html').read()
i = idx.find('Wispr')
print("\n=== index.html context around Wispr ===")
print(idx[max(0, i-300):i+300].replace('\n', ' ')[:600])

# check all-products.json for our 5
ap = json.load(open(base + '/all-products.json'))
names = [p.get('name') for p in ap if isinstance(p, dict)]
hits = [n for n in names if any(k in (n or '') for k in ['Wispr', 'Reelang', 'PageForth', 'AdAnt', 'Workout'])]
print("\n=== all-products.json hits ===")
for h in hits:
    print(" ", h)

import os, json, subprocess

repo = '/home/pin/aI-product-daily-peport'
docs = repo + '/docs'

# 1. product pages still exist for morning report products
for slug in ['airproof-ai', 'hand-wave', 'coach-ai', 'scrolltoll']:
    p = f'{docs}/products/{slug}.html'
    print(f"docs/products/{slug}.html exists:", os.path.exists(p))

# 2. archive.html contains morning products
arch = open(f'{docs}/archive.html').read()
for kw in ['AirProof', 'Hand Wave', 'CoachAI', 'ScrollToll']:
    print(f"archive contains '{kw}':", kw in arch)

# 3. all-products.json count and includes both sets
ap = json.load(open(f'{docs}/all-products.json'))
names = [p.get('name', '') for p in ap]
print("all-products count:", len(names))
for kw in ['Wispr Flow Notetaker', 'AirProof', 'ScrollToll', 'Workout Narrator']:
    print(f"  contains '{kw}':", any(kw in n for n in names))

# 4. live archive spot check
r = subprocess.run(['curl', '-s', '-m', '30', 'https://ai-daily.asdasd.vip/archive.html'], capture_output=True, text=True)
live = r.stdout
print("\nlive archive size:", len(live), "| contains AirProof:", 'AirProof' in live, "| contains Workout Narrator:", 'Workout Narrator' in live)

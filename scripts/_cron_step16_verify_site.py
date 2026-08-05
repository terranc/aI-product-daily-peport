import subprocess, json

def curl(url):
    r = subprocess.run(['curl', '-s', '-m', '30', url], capture_output=True, text=True)
    return r.stdout

index = curl('https://ai-daily.asdasd.vip/')
print("index size:", len(index))
for kw in ['Wispr', 'Reelang', 'PageForth', 'AdAnt', 'Workout']:
    print(f"  index contains '{kw}':", kw in index)

rep = curl('https://ai-daily.asdasd.vip/reports/daily/2026-08-05.json')
print("report fetch size:", len(rep))
try:
    d = json.loads(rep)
    print("report date:", d.get('date'), "| count:", d.get('productCount'))
    for p in d.get('products', []):
        print("  -", p.get('name'))
except Exception as e:
    print("report parse failed:", e, "| first 200 chars:", rep[:200])

# also check the products detail page exists
p = curl('https://ai-daily.asdasd.vip/products/wispr-flow-notetaker.html')
print("wispr product page size:", len(p))

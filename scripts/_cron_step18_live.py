import subprocess

def curl(url):
    r = subprocess.run(['curl', '-s', '-m', '30', url], capture_output=True, text=True)
    return r.stdout

checks = [
    'https://ai-daily.asdasd.vip/products/wispr-flow-notetaker.html',
    'https://ai-daily.asdasd.vip/products/reelang.html',
    'https://ai-daily.asdasd.vip/products/pageforth.html',
    'https://ai-daily.asdasd.vip/products/adant-ai.html',
    'https://ai-daily.asdasd.vip/products/workout-narrator.html',
]
for u in checks:
    html = curl(u)
    ok = 'product' in html and len(html) > 3000
    print(f"{'OK ' if ok else 'MISS'} {u.split('/')[-1]} size={len(html)}")

idx = curl('https://ai-daily.asdasd.vip/')
for kw in ['Reelang', 'PageForth', 'AdAnt', 'Workout']:
    print(f"index contains '{kw}':", kw in idx)

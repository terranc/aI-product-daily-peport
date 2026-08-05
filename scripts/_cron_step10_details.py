import subprocess, re

def curl(url, timeout=25):
    try:
        r = subprocess.run(['curl', '-sL', '-m', str(timeout), '-A',
                            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36',
                            url], capture_output=True, text=True, timeout=timeout+5)
        return r.stdout
    except Exception as e:
        return f"ERROR: {e}"

def strip_html(h):
    h = re.sub(r'<script[\s\S]*?</script>', ' ', h)
    h = re.sub(r'<style[\s\S]*?</style>', ' ', h)
    h = re.sub(r'<[^>]+>', ' ', h)
    h = re.sub(r'\s+', ' ', h)
    return h.strip()

targets = [
    ('wisprflow.ai', 'https://wisprflow.ai/'),
    ('reelang.com', 'https://reelang.com'),
    ('pageforth.com', 'https://pageforth.com/'),
    ('adant.ai', 'https://adant.ai/'),
    ('HN reelang discussion', 'https://news.ycombinator.com/item?id=49183550'),
    ('HN pageforth discussion', 'https://news.ycombinator.com/item?id=49182365'),
]

for label, url in targets:
    html = curl(url)
    if html.startswith('ERROR') or len(html) < 300:
        print(f"===== {label}: FAILED ({html[:80]})")
        continue
    text = strip_html(html)
    # og:description / meta description
    md = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html)
    og = re.search(r'<meta[^>]+property="og:description"[^>]+content="([^"]+)"', html)
    ogt = re.search(r'<meta[^>]+property="og:title"[^>]+content="([^"]+)"', html)
    print(f"===== {label}")
    if ogt: print(f"  og:title: {ogt.group(1)[:150]}")
    if og: print(f"  og:desc: {og.group(1)[:300]}")
    elif md: print(f"  meta desc: {md.group(1)[:300]}")
    # first 700 chars of visible text
    print(f"  text: {text[:700]}")
    print()

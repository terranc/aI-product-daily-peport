import subprocess, re, json

def curl(url, timeout=25):
    try:
        r = subprocess.run(['curl', '-sL', '-m', str(timeout), '-A',
                            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36',
                            url], capture_output=True, text=True, timeout=timeout+5)
        return r.stdout
    except Exception as e:
        return f"ERROR: {e}"

pages = {
    'Wispr Flow Notetaker': 'https://www.producthunt.com/products/wisprflow',
    'AdAnt AI': 'https://www.producthunt.com/products/adant-ai',
    'StepGrab': 'https://www.producthunt.com/products/stepgrab',
    'VIDEO AI ME': 'https://www.producthunt.com/products/video-ai-me',
    'Hey Noah': 'https://www.producthunt.com/products/hey-noah',
    'Garden of Mind': 'https://www.producthunt.com/products/the-garden-of-mind',
}

for label, url in pages.items():
    html = curl(url)
    if html.startswith('ERROR') or len(html) < 500:
        print(f"{label}: fetch failed ({html[:80]})")
        continue
    # try common patterns for website URL
    found = None
    for pat in [r'"websiteUrl"\s*:\s*"([^"]+)"',
                r'data-test="product-url"[^>]*href="([^"]+)"',
                r'class="[^"]*website[^"]*"[^>]*href="([^"]+)"',
                r'href="(https?://[^"]+)"[^>]*rel="nofollow sponsored']:
        m = re.search(pat, html)
        if m:
            found = m.group(1)
            break
    if not found:
        # look for the canonical/og:url or any external links near "Visit"
        m = re.search(r'<a[^>]+href="(https?://[^"]+)"[^>]*>[^<]*Visit', html)
        if m:
            found = m.group(1)
    print(f"{label}: {found}")
    # also grab description meta
    md = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html)
    if md:
        print(f"    meta desc: {md.group(1)[:200]}")

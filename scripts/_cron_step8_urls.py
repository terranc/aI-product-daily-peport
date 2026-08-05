import subprocess, re, json

def curl(url, timeout=25):
    try:
        r = subprocess.run(['curl', '-sL', '-m', str(timeout), '-A',
                            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36',
                            url], capture_output=True, text=True, timeout=timeout+5)
        return r.stdout
    except Exception as e:
        return f"ERROR: {e}"

# 1. Resolve PH redirects (follow redirects, capture final URL via -w)
for pid, label in [('1214897', 'Wispr Flow Notetaker'), ('1212030', 'AdAnt AI'),
                   ('1198410', 'StepGrab'), ('1214128', 'VIDEO AI ME'),
                   ('1090720', 'Hey Noah'), ('1213237', 'Garden of Mind'),
                   ('1210439', 'Wondering'), ('1215391', 'Hansel')]:
    try:
        r = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{url_effective}', '-L', '-m', '20',
                            '-A', 'Mozilla/5.0', f'https://www.producthunt.com/r/p/{pid}'],
                           capture_output=True, text=True, timeout=25)
        print(f"{label}: {r.stdout}")
    except Exception as e:
        print(f"{label}: ERROR {e}")

# 2. Fetch V2EX post for Workout Narrator to find App Store link
print("\n=== V2EX 1232288 (Workout Narrator) ===")
html = curl('https://www.v2ex.com/t/1232288')
for pat in [r'https://apps\.apple\.com[^"\'<>\\ ]+', r'https://testflight\.apple\.com[^"\'<>\\ ]+']:
    for m in re.findall(pat, html)[:5]:
        print("found:", m[:160])
# also check github/testflight words
for kw in ['TestFlight', 'testflight', 'App Store', 'apps.apple']:
    idx = html.find(kw)
    if idx >= 0:
        print(f"ctx[{kw}]:", html[max(0,idx-120):idx+200].replace('\n', ' ')[:320])

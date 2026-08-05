import subprocess

repo = '/home/pin/aI-product-daily-peport'

def run(cmd):
    r = subprocess.run(cmd, cwd=repo, capture_output=True, text=True)
    return (r.stdout + r.stderr)

print("=== last commit stat ===")
print(run(['git', 'show', 'HEAD', '--stat', '--format=%h %s'])[:2500])

print("\n=== scan committed diff for secrets ===")
diff = run(['git', 'show', 'HEAD', '--', '.', ':!docs'])
import re
patterns = [
    (r'(sk-[A-Za-z0-9]{20,}|pk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,})', 'token pattern'),
    (r'(api[_-]?key\s*[=:]\s*["\'][^"\']{12,})', 'api key assignment'),
    (r'(AKIA[0-9A-Z]{16})', 'aws key'),
    (r'(-----BEGIN [A-Z ]*PRIVATE KEY-----)', 'private key'),
]
found = False
for pat, label in patterns:
    for m in re.finditer(pat, diff, re.I):
        print(f"  !! {label}: {m.group(0)[:40]}...")
        found = True
if not found:
    print("  no obvious secrets found")

print("\n=== reference check: _cron_ files referenced anywhere? ===")
out = run(['grep', '-rn', '_cron_', '--include=*.py', '--include=*.json', '--include=*.md', '--include=*.toml', '--include=*.yaml', '.', '--exclude-dir=docs'])
print(out[:800] or "  no references outside the files themselves")

import subprocess

repo = '/home/pin/aI-product-daily-peport'

def run(cmd):
    r = subprocess.run(cmd, cwd=repo, capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()

print("=== branches ===")
print(run(['git', 'branch', '-a']))

print("\n=== gh-pages log ===")
print(run(['git', 'log', 'gh-pages', '-3', '--format=%h %ci %s']))

print("\n=== main log ===")
print(run(['git', 'log', 'main', '-3', '--format=%h %ci %s']))

print("\n=== docs/ dirty? ===")
print(run(['git', 'status', '--short', 'docs/']) or "(clean)")

print("\n=== remote ===")
print(run(['git', 'remote', '-v']))

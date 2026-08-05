import subprocess

repo = '/home/pin/aI-product-daily-peport'

def run(cmd):
    r = subprocess.run(cmd, cwd=repo, capture_output=True, text=True)
    return r.stdout

print(run(['git', 'diff', 'HEAD', '--', 'scripts/crawl_raw.py', 'scripts/build_site.py'])[:3000])

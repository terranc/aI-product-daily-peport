import os, subprocess, glob

repo = '/home/pin/aI-product-daily-peport'
files = glob.glob(repo + '/scripts/_cron_step1*.py') + glob.glob(repo + '/scripts/_cron_step2*.py')
for f in files:
    if os.path.exists(f):
        os.remove(f)
        print("removed:", f.replace(repo + '/', ''))

# also remove any leftover _cron_ files not tracked
leftover = [f for f in glob.glob(repo + '/scripts/_cron_*') if os.path.exists(f)]
print("leftover _cron_ files:", [f.replace(repo + '/', '') for f in leftover] or "none")

r = subprocess.run(['git', 'status', '--short'], cwd=repo, capture_output=True, text=True)
print("\n=== git status ===")
print(r.stdout.strip() or "(clean)")

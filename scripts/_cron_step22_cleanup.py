import subprocess, glob, os

repo = '/home/pin/aI-product-daily-peport'

def run(cmd):
    r = subprocess.run(cmd, cwd=repo, capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()

# list temp files
files = []
files += glob.glob(repo + '/scripts/_cron_*.py')
files += glob.glob(repo + '/scripts/_cron_*.json')
files += glob.glob(repo + '/data/_cron_*.json')
print("temp files to remove:")
for f in files:
    print("  ", f.replace(repo + '/', ''))

# remove them (git rm to stage deletion)
for f in files:
    subprocess.run(['git', 'rm', '-q', '--ignore-unmatch', f], cwd=repo)

# also remove tracked __pycache__ pyc files? leave them - pre-existing.

status = run(['git', 'status', '--short'])
print("\n=== status after removal ===")
print(status[:1500])

if status.strip():
    print("\n=== commit cleanup ===")
    print(run(['git', 'commit', '-m', 'chore: 清理 cron 临时脚本与中间文件']))

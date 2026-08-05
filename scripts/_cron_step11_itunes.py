import subprocess, json

def curl(url, timeout=25):
    try:
        r = subprocess.run(['curl', '-sL', '-m', str(timeout), url], capture_output=True, text=True, timeout=timeout+5)
        return r.stdout
    except Exception as e:
        return f"ERROR: {e}"

# 1. Lookup by exact app id for Workout Narrator
print("=== lookup id6795447541 (Workout Narrator) ===")
d = json.loads(curl('https://itunes.apple.com/lookup?id=6795447541'))
if d.get('resultCount'):
    app = d['results'][0]
    print("trackName:", app.get('trackName'))
    print("trackViewUrl:", app.get('trackViewUrl'))
    print("screenshots:", len(app.get('screenshotUrls', [])), "| first:", app.get('screenshotUrls', [''])[0][:90])
else:
    print("NOT FOUND")

# 2. Search Wispr Flow
print("\n=== search 'Wispr Flow' ===")
d = json.loads(curl('https://itunes.apple.com/search?term=Wispr%20Flow&entity=software&limit=5'))
for app in d.get('results', [])[:5]:
    print("-", app.get('trackName'), "|", app.get('trackViewUrl', '')[:80])

# 3. Search Workout Narrator
print("\n=== search 'Workout Narrator' ===")
d = json.loads(curl('https://itunes.apple.com/search?term=Workout%20Narrator&entity=software&limit=5'))
for app in d.get('results', [])[:5]:
    print("-", app.get('trackName'), "|", app.get('trackViewUrl', '')[:80])

# 4. Search PageForth
print("\n=== search 'PageForth' ===")
d = json.loads(curl('https://itunes.apple.com/search?term=PageForth&entity=software&limit=5'))
print("count:", d.get('resultCount'))
for app in d.get('results', [])[:5]:
    print("-", app.get('trackName'), "|", app.get('trackViewUrl', '')[:80])

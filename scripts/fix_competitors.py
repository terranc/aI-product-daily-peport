import json
import os

BASE_DIR = '/Volumes/EXTEND/aI-product-daily-peport'
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPORT_PATH = os.path.join(BASE_DIR, 'reports', 'daily', '2026-06-15.json')
DB_PATH = os.path.join(DATA_DIR, 'products.json')

def fix_competitors(analysis):
    if 'competitors' in analysis:
        fixed = []
        for c in analysis['competitors']:
            if isinstance(c, str):
                fixed.append({"name": c, "url": "", "comparison": ""})
            elif isinstance(c, dict):
                fixed.append(c)
        analysis['competitors'] = fixed
    return analysis

# Fix report
with open(REPORT_PATH, 'r', encoding='utf-8') as f:
    report = json.load(f)

for p in report['products']:
    if 'analysis' in p:
        p['analysis'] = fix_competitors(p['analysis'])

with open(REPORT_PATH, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

# Fix DB
with open(DB_PATH, 'r', encoding='utf-8') as f:
    db = json.load(f)

for p in db['products']:
    if 'analysis' in p:
        p['analysis'] = fix_competitors(p['analysis'])

with open(DB_PATH, 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Competitors fixed.")

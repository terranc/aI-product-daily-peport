import sys
import os
import json
import time

# Setup paths
BASE_DIR = '/Volumes/EXTEND/aI-product-daily-peport'
DATA_DIR = os.path.join(BASE_DIR, 'data')
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts')

sys.path.insert(0, SCRIPTS_DIR)
from screenshot import process_product_screenshots

# Load the report we just created to get the URLs
today_str = '2026-06-15'
report_path = os.path.join(BASE_DIR, 'reports', 'daily', f"{today_str}.json")

with open(report_path, 'r', encoding='utf-8') as f:
    report = json.load(f)

print("Starting screenshots for 5 products...")
for prod in report['products']:
    print(f"Processing {prod['name']}...")
    result = process_product_screenshots(prod)
    
    # Update the report
    prod['screenshotUrl'] = result.get('screenshotUrl')
    prod['appStoreScreenshots'] = result.get('appStoreScreenshots', [])
    prod['appStoreName'] = result.get('appStoreName')
    prod['appStoreUrl'] = result.get('appStoreUrl')
    
    time.sleep(3) # Respect rate limits

# Save updated report
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

# Also update the products.json with screenshot info
db_path = os.path.join(DATA_DIR, 'products.json')
with open(db_path, 'r', encoding='utf-8') as f:
    db = json.load(f)

for prod in report['products']:
    for i, existing in enumerate(db['products']):
        if existing.get('id') == prod['id']:
            db['products'][i]['screenshotUrl'] = prod['screenshotUrl']
            db['products'][i]['appStoreScreenshots'] = prod['appStoreScreenshots']
            db['products'][i]['appStoreName'] = prod['appStoreName']
            db['products'][i]['appStoreUrl'] = prod['appStoreUrl']
            break

with open(db_path, 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Screenshots completed and files updated.")

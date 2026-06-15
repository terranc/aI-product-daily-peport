import json
import os
import glob

BASE_DIR = '/Volumes/EXTEND/aI-product-daily-peport'
SCREENSHOTS_DIR = os.path.join(BASE_DIR, 'assets', 'screenshots')
REPORT_PATH = os.path.join(BASE_DIR, 'reports', 'daily', '2026-06-15.json')
DB_PATH = os.path.join(BASE_DIR, 'data', 'products.json')

# Map product IDs to their screenshot files
screenshot_files = glob.glob(os.path.join(SCREENSHOTS_DIR, '*.png'))
print(f"Found {len(screenshot_files)} screenshot files")

# Build mapping: product_id -> relative path
screenshot_map = {}
for f in screenshot_files:
    fname = os.path.basename(f)
    # Extract product_id from filename: {product_id}_{timestamp}.png
    # Product IDs contain '/' which are replaced with '_'
    parts = fname.rsplit('_', 2)  # split from right: _YYYYMMDD_HHMMSS.png
    if len(parts) >= 3:
        safe_id = parts[0]
        # We need to reverse the _ replacement to match product IDs
        # But we have the product IDs from the report, so let's just check
        screenshot_map[safe_id] = f"assets/screenshots/{fname}"

print("Screenshot map:")
for k, v in screenshot_map.items():
    print(f"  {k}: {v}")

# Load report
with open(REPORT_PATH, 'r', encoding='utf-8') as f:
    report = json.load(f)

# Load DB
with open(DB_PATH, 'r', encoding='utf-8') as f:
    db = json.load(f)

# Update report and DB
for prod in report['products']:
    pid = prod['id']
    safe_id = pid.replace('/', '_').replace('\\', '_').replace(':', '_')
    if safe_id in screenshot_map:
        prod['screenshotUrl'] = screenshot_map[safe_id]
        print(f"Updated report for {prod['name']}: {screenshot_map[safe_id]}")
    
    # Update DB too
    for i, db_prod in enumerate(db['products']):
        if db_prod.get('id') == pid:
            db['products'][i]['screenshotUrl'] = prod.get('screenshotUrl')
            break

# Save
with open(REPORT_PATH, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

with open(DB_PATH, 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Report and DB updated with screenshot paths.")

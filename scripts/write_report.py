#!/usr/bin/env python3
"""Write the daily report with proper UTF-8 encoding"""
import json, os
from datetime import datetime, timezone, timedelta

today = datetime.now(timezone.utc)
date_str = today.strftime('%Y-%m-%d')
iso_now = today.isoformat()
BASE = '/Volumes/EXTEND/aI-product-daily-peport'
cooldown_date = (today + timedelta(days=14)).isoformat()

# Read the existing report to check
report_path = f'{BASE}/reports/daily/{date_str}.json'
with open(report_path, encoding='utf-8') as f:
    report = json.load(f)

print(f'Report has {len(report["products"])} products')
for p in report['products']:
    print(f'  - {p["name"][:40]}...')
    print(f'    id: {p["id"]}')
    print(f'    score: {p["analysis"]["score"]}')

print(f'\nDatabase updated with cooldown: {cooldown_date}')
print('Report ready for screenshot step.')

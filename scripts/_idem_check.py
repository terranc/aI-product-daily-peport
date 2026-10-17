#!/usr/bin/env python3
"""Idempotency check for today's AI Product Radar daily report."""
import json, os, datetime

CST = datetime.timezone(datetime.timedelta(hours=8))
today = datetime.datetime.now(CST).strftime('%Y-%m-%d')
proj = '/home/pin/aI-product-daily-peport'
report_path = f'{proj}/reports/daily/{today}.json'
db_path = f'{proj}/data/products.json'

print("now(CST) =", datetime.datetime.now(CST).isoformat())
print("today =", today)
print("report exists =", os.path.exists(report_path))

ok = False
if os.path.exists(report_path):
    try:
        rep = json.load(open(report_path, encoding='utf-8'))
        prods = rep.get('products', [])
        print("report products =", len(prods))
        db = json.load(open(db_path, encoding='utf-8'))
        dbprods = db.get('products', db) if isinstance(db, dict) else db
        dbids = {p.get('id') for p in dbprods}
        print("db size =", len(dbprods))
        print("db lastUpdated =", db.get('lastUpdated') if isinstance(db, dict) else None)
        if len(prods) >= 3:
            allgood = True
            for p in prods:
                missing = [k for k in ('id', 'name', 'slug') if not p.get(k)]
                if not (p.get('analysis') or {}).get('score'):
                    missing.append('analysis.score')
                if missing:
                    allgood = False
                    print("BAD fields", p.get('id'), missing)
                if p.get('id') not in dbids:
                    allgood = False
                    print("MISSING in db =", p.get('id'))
            ok = allgood
    except Exception as e:
        print("error reading:", repr(e))

print("IDEMPOTENT_COMPLETE =", ok)

import json, os, datetime

CST = datetime.timezone(datetime.timedelta(hours=8))
today = datetime.datetime.now(CST).strftime('%Y-%m-%d')
report_path = f'reports/daily/{today}.json'
db_path = 'data/products.json'
print("today(CST):", today)
print("report exists:", os.path.exists(report_path))

done = False
if os.path.exists(report_path):
    try:
        r = json.load(open(report_path))
        prods = r.get('products') or []
        db = json.load(open(db_path))
        dblist = db.get('products') if isinstance(db, dict) else db
        dbids = {p.get('id') for p in dblist}
        ok_items = [p for p in prods
                    if p.get('id') and p.get('name') and p.get('slug')
                    and (p.get('analysis') or {}).get('score')]
        in_db = [p for p in ok_items if p.get('id') in dbids]
        print("products:", len(prods), "ok:", len(ok_items), "in_db:", len(in_db))
        print("ids:", [p.get('id') for p in prods])
        done = (len(prods) >= 3 and len(ok_items) == len(prods)
                and len(in_db) == len(prods))
    except Exception as e:
        print("parse error:", repr(e))

print("DONE:", done)

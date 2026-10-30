import json, os, datetime

d = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime('%Y-%m-%d')
p = f"/home/pin/aI-product-daily-peport/reports/daily/{d}.json"
ok = False
if os.path.exists(p):
    try:
        r = json.load(open(p))
        prods = r.get('products', [])
        db = json.load(open('/home/pin/aI-product-daily-peport/data/products.json'))
        dbl = db.get('products', db) if isinstance(db, dict) else db
        dbids = {x.get('id') for x in dbl if isinstance(x, dict)}
        checks = [len(prods) >= 3]
        for x in prods:
            a = x.get('analysis') or {}
            checks.append(bool(x.get('id') and x.get('name') and x.get('slug') and a.get('score')))
            checks.append(x.get('id') in dbids)
        ok = all(checks)
        print("date", d, "products", len(prods), "DONE" if ok else "NOT_DONE", checks)
    except Exception as e:
        print("date", d, "err", repr(e))
else:
    print("date", d, "no report file -> NOT_DONE")

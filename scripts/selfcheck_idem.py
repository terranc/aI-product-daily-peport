import json, os, datetime
tz = datetime.timezone(datetime.timedelta(hours=8))
today = datetime.datetime.now(tz).strftime('%Y-%m-%d')
p = f"/home/pin/aI-product-daily-peport/reports/daily/{today}.json"
print("today:", today, "report exists:", os.path.exists(p))
ok = False
if os.path.exists(p):
    try:
        r = json.load(open(p))
        prods = r.get('products', [])
        db = json.load(open('/home/pin/aI-product-daily-peport/data/products.json'))
        dbl = db.get('products', db) if isinstance(db, dict) else db
        dbids = {x.get('id') for x in dbl}
        good = 0
        for x in prods:
            sc = (x.get('analysis') or {}).get('score')
            if x.get('id') and x.get('name') and x.get('slug') and sc and x.get('id') in dbids:
                good += 1
        print("products:", len(prods), "valid:", good)
        ok = len(prods) >= 3 and good == len(prods)
    except Exception as e:
        print("err", e)
print("COMPLETE:", ok)

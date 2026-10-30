import json, os, datetime
cst = datetime.timezone(datetime.timedelta(hours=8))
today = datetime.datetime.now(cst).strftime('%Y-%m-%d')
path = f"reports/daily/{today}.json"
done = False
missing = []
if os.path.exists(path):
    rep = json.load(open(path))
    prods = rep.get('products', [])
    db = json.load(open('data/products.json'))
    dbl = db.get('products', db) if isinstance(db, dict) else db
    dbids = {p.get('id') or p.get('product_id') for p in dbl}
    ok = len(prods) >= 3
    for p in prods:
        if not (p.get('id') and p.get('name') and p.get('slug') and p.get('analysis', {}).get('score')):
            ok = False; missing.append(p.get('id'))
        if p.get('id') not in dbids:
            ok = False; missing.append('NOT_IN_DB:'+str(p.get('id')))
    done = ok
    print("products:", len(prods), "valid:", ok)
    print("issues:", missing)
else:
    print("no report file yet")
print("DONE:", done)

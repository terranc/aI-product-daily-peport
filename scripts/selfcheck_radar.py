# -*- coding: utf-8 -*-
"""收尾自检：报告 / DB / gh-pages 提交"""
import json, os, datetime, subprocess

PROJ = '/home/pin/aI-product-daily-peport'
today = datetime.datetime.now().strftime('%Y-%m-%d')

ok = True

# 1) 报告
rp = f'{PROJ}/reports/daily/{today}.json'
r = json.load(open(rp))
prods = r['products']
assert len(prods) >= 3, 'too few'
for p in prods:
    assert p['id'] and p['name'] and p['slug'], str(p.get('name'))
    s = (p.get('analysis') or {}).get('score')
    assert isinstance(s, int) and 1 <= s <= 10, f'bad score {p["slug"]} {s}'
    assert p['analysis'].get('competitors'), p['slug']
    assert p['analysis'].get('useCases'), p['slug']
print('报告 OK:', rp, 'productCount=', r['productCount'], 'date=', r['date'])

# 2) DB
db = json.load(open(f'{PROJ}/data/products.json'))
dbl = db['products']
ids = {e['id'] for e in dbl}
for p in prods:
    assert p['id'] in ids, 'missing in db ' + p['id']
    e = next(x for x in dbl if x['id'] == p['id'])
    assert e.get('cooldownExpiresAt'), p['id']
    t = datetime.datetime.fromisoformat(e['cooldownExpiresAt'].replace('Z','+00:00'))
    now = datetime.datetime.now(datetime.timezone.utc)
    days = (t - now).days
    assert 12 <= days <= 15, f'cooldown {days}d for {p["id"]}'
lu = db.get('lastUpdated','')[:10]
assert lu == today, f'lastUpdated={db.get("lastUpdated")}'
print('DB OK: total=', len(dbl), 'lastUpdated=', db['lastUpdated'][:19], 'cooldown~14d verified')

# 3) gh-pages 提交
out = subprocess.check_output(['git','log','origin/gh-pages','-1'], cwd=PROJ).decode()
print('origin/gh-pages -1:', out.strip().splitlines()[0])
out2 = subprocess.check_output(['git','log','origin/main','-1'], cwd=PROJ).decode()
print('origin/main -1:', out2.strip().splitlines()[0])
assert 'daily: ' + today in out or 'daily: ' + today in out2, 'commit message missing'
# 页面是否在分支里
tree = subprocess.check_output(['git','ls-tree','origin/gh-pages','products/','--name-only'], cwd=PROJ).decode()
for p in prods:
    assert f'products/{p["slug"]}.html' in tree, 'page missing in gh-pages: ' + p['slug']
print('gh-pages OK: 5 product pages present')
print('ALL CHECKS PASSED')

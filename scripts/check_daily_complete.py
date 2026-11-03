#!/usr/bin/env python3
"""幂等检查：判断今天的 AI 产品日报是否已经完成。

退出码 0 = 已完成（应回 [SILENT] 结束）；1 = 未完成（继续执行抓取分析）。
stdout 打印人类可读的状态，便于 cron 日志排查。
"""
import datetime
import json
import os
import sys

BASE = "/home/pin/aI-product-daily-peport"
tz = datetime.timezone(datetime.timedelta(hours=8))
today = datetime.datetime.now(tz).strftime("%Y-%m-%d")
report = f"{BASE}/reports/daily/{today}.json"
db_path = f"{BASE}/data/products.json"

print(f"today: {today}")
print(f"report: {report} exists={os.path.exists(report)}")

if not os.path.exists(report):
    print("COMPLETE: False (no report file)")
    sys.exit(1)

try:
    with open(report, encoding="utf-8") as f:
        rpt = json.load(f)
    prods = rpt.get("products") or []
    with open(db_path, encoding="utf-8") as f:
        db = json.load(f)
    dbl = db.get("products", db) if isinstance(db, dict) else db
    dbids = {x.get("id") for x in dbl if isinstance(x, dict)}
    print(f"products: {len(prods)}  db entries: {len(dbids)}")

    good = 0
    for x in prods:
        score = (x.get("analysis") or {}).get("score")
        if x.get("id") and x.get("name") and x.get("slug") and score and x.get("id") in dbids:
            good += 1
    print(f"valid: {good}/{len(prods)}")

    ok = len(prods) >= 3 and good == len(prods)
except Exception as exc:
    print(f"err: {exc}")
    ok = False

print(f"COMPLETE: {ok}")
sys.exit(0 if ok else 1)

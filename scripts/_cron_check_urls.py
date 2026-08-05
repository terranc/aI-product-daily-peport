#!/usr/bin/env python3
"""Fetch title + meta description + status for candidate product URLs."""
import urllib.request
import re
import html

urls = [
    "https://hansel.so",
    "https://www.vocab.top/",
    "https://videoai.me/",
    "https://adant.ai/",
    "https://stepgrab.net/",
    "https://space-ocr.com/",
    "https://www.heynoah.io/",
    "https://driven.ai/",
    "https://wisprflow.ai/notetaker",
    "https://pageforth.com/",
    "https://heybraza.com",
    "https://stynar.com/",
    "https://www.crodo.ai/",
    "https://wondering.app/",
    "https://snapdown.com.au/",
    "https://howto.plow.co/domo",
    "https://quantsignals.xyz/fst",
    "https://auditbadger.com/",
    "https://www.piximagen.com/",
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"})
        resp = urllib.request.urlopen(req, timeout=25)
        data = resp.read(200000)
        try:
            txt = data.decode('utf-8', errors='ignore')
        except Exception:
            txt = ''
        title = re.search(r'<title[^>]*>(.*?)</title>', txt, re.S | re.I)
        desc = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', txt, re.S | re.I)
        if not desc:
            desc = re.search(r'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']description["\']', txt, re.S | re.I)
        t = html.unescape(title.group(1).strip()) if title else 'NO TITLE'
        d = html.unescape(desc.group(1).strip()[:300]) if desc else 'NO DESC'
        print(f"OK  {u}\n    status={resp.status} final={resp.geturl()}\n    title={t}\n    desc={d}\n")
    except Exception as e:
        print(f"ERR {u} -> {e}\n")

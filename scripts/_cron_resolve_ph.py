#!/usr/bin/env python3
"""Resolve Product Hunt redirect links to real product URLs."""
import json
import urllib.request

ids = [
    "1215391",  # Hansel
    "1214897",  # Wispr Flow Notetaker
    "1212030",  # AdAnt AI
    "1198410",  # StepGrab
    "1211314",  # space ocr
    "1090720",  # Hey Noah
    "1203025",  # Driven
    "1214128",  # VIDEO AI ME
    "1207933",  # Crodo AI
    "1214385",  # Stynar
    "1205777",  # Domo
    "1210439",  # Wondering
    "1212851",  # gesture.live
    "1212818",  # Snapdown
    "1213586",  # SpeakoFlow
    "1200155",  # Atlaso
]

for pid in ids:
    url = f"https://www.producthunt.com/r/p/{pid}?app_id=339"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"})
        resp = urllib.request.urlopen(req, timeout=20)
        final = resp.geturl()
        print(f"{pid} -> {final}")
    except Exception as e:
        print(f"{pid} -> ERROR: {e}")

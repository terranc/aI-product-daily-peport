#!/usr/bin/env python3
"""
原始数据抓取脚本
只负责从各渠道抓取候选产品，输出 JSON 供 agent 做 LLM 分析
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fetch_hackernews import fetch_hackernews_products
from fetch_github import fetch_github_trending
from fetch_twitter import fetch_twitter_products
from fetch_reddit import fetch_reddit_products

OUTPUT_FILE = Path("/Volumes/EXTEND/aI-product-daily-peport/data/raw-candidates.json")


def fetch_all():
    """从所有渠道抓取原始候选产品"""
    all_products = []

    print("📡 抓取各渠道数据...")

    # Hacker News
    try:
        print("  🟠 Hacker News...")
        hn = fetch_hackernews_products()
        print(f"     {len(hn)} 个")
        for p in hn:
            p['source'] = 'hackernews'
        all_products.extend(hn)
    except Exception as e:
        print(f"     错误: {e}")

    # GitHub
    try:
        print("  🐙 GitHub...")
        gh = fetch_github_trending()
        print(f"     {len(gh)} 个")
        for p in gh:
            p['source'] = 'github'
        all_products.extend(gh)
    except Exception as e:
        print(f"     错误: {e}")

    # Twitter
    try:
        print("  🐦 Twitter...")
        tw = fetch_twitter_products()
        print(f"     {len(tw)} 个")
        for p in tw:
            p['source'] = 'twitter'
        all_products.extend(tw)
    except Exception as e:
        print(f"     错误: {e}")

    # Reddit
    try:
        print("  🟠 Reddit...")
        rd = fetch_reddit_products()
        print(f"     {len(rd)} 个")
        for p in rd:
            p['source'] = 'reddit'
        all_products.extend(rd)
    except Exception as e:
        print(f"     错误: {e}")

    # 按热度排序
    all_products.sort(key=lambda x: x.get('score', 0) + x.get('stars', 0), reverse=True)

    # 去重（基于 URL）
    seen_urls = set()
    unique = []
    for p in all_products:
        url = p.get('url', '') or p.get('source_url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(p)
        elif not url:
            unique.append(p)

    print(f"\n✅ 共 {len(unique)} 个候选产品（去重后）")

    # 保存
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            'fetchedAt': datetime.now().isoformat(),
            'totalCount': len(unique),
            'products': unique
        }, f, ensure_ascii=False, indent=2)

    print(f"💾 已保存到 {OUTPUT_FILE}")

    # 输出摘要供 agent 阅读
    print("\n" + "=" * 60)
    print("📋 候选产品摘要（前 30 个）：")
    print("=" * 60)
    for i, p in enumerate(unique[:30], 1):
        name = p.get('name', 'Unknown')[:60]
        score = p.get('score', 0) or p.get('stars', 0)
        src = p.get('source', '?')
        url = p.get('url', '') or p.get('source_url', '')
        desc = (p.get('description', '') or '')[:100]
        print(f"\n{i}. [{src}] {name}")
        print(f"   热度: {score} | URL: {url}")
        print(f"   描述: {desc}")

    return unique


if __name__ == '__main__':
    fetch_all()

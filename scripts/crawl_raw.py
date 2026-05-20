#!/usr/bin/env python3
"""
原始数据抓取脚本
渠道：Hacker News、Reddit、Product Hunt、V2EX
输出 JSON 供 agent 做 LLM 分析
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import requests
from datetime import datetime
from pathlib import Path

OUTPUT_FILE = Path("/Volumes/EXTEND/aI-product-daily-peport/data/raw-candidates.json")
USER_AGENT = "agent-reach/1.0"
TWITTER_CLI = str(Path.home() / ".local" / "bin" / "twitter")


def generate_product_id(product):
    """
    生成产品唯一标识：
    1. 有官网 URL → 用标准化后的域名+路径（去掉 www、协议、尾部斜杠）
    2. APP 有 App Store URL → 用 App Store ID
    3. 其他 → 用产品原名（小写、去空格）
    """
    import re
    from urllib.parse import urlparse

    url = product.get("url", "") or product.get("homepage", "")
    name = product.get("name", "")

    # 1. 有 URL → 用域名+路径作为 ID
    if url:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        # 去掉 www.
        domain = re.sub(r'^www\.', '', domain)
        path = parsed.path.rstrip('/').lower()
        # 去掉常见的非产品页面路径
        if path in ('', '/', '/home', '/index.html'):
            path = ''
        if domain:
            raw_id = f"{domain}{path}"
            # 标准化：只保留字母数字和点斜杠
            raw_id = re.sub(r'[^a-z0-9./]', '', raw_id)
            if raw_id:
                return raw_id

    # 2. 用产品原名作为 fallback
    if name:
        # 小写、去特殊字符、取前50字符
        clean = re.sub(r'[^a-z0-9\s]', '', name.lower()).strip()[:50]
        clean = re.sub(r'\s+', '-', clean)
        if clean:
            return clean

    # 3. 最终 fallback
    return hashlib.md5(json.dumps(product, sort_keys=True).encode()).hexdigest()[:12]


def fetch_hackernews():
    """Hacker News - 通过 Algolia API 搜索 AI 相关 Show HN 帖子"""
    print("  🟠 Hacker News...")
    products = []
    try:
        # 搜索最近 24 小时的 Show HN 帖子（AI/产品相关）
        queries = [
            "Show HN",
        ]
        for q in queries:
            url = "https://hn.algolia.com/api/v1/search_by_date"
            params = {
                "query": q,
                "tags": "show_hn",
                "hitsPerPage": 30,
                "numericFilters": "created_at_i>{}".format(
                    int(datetime.now().timestamp()) - 86400 * 2
                ),
            }
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
            for hit in resp.json().get("hits", []):
                title = hit.get("title", "")
                url_val = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
                products.append({
                    "id": f"hn_{hit.get('objectID', '')}",
                    "name": title,
                    "description": (hit.get("story_text") or "")[:500],
                    "url": url_val,
                    "source_url": f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                    "score": hit.get("points", 0),
                    "source": "hackernews",
                    "timestamp": hit.get("created_at", ""),
                })
        print(f"     {len(products)} 个")
    except Exception as e:
        print(f"     错误: {e}")
    return products


def fetch_reddit():
    """Reddit - 通过公开 JSON API"""
    print("  🟠 Reddit...")
    products = []
    subreddits = ["SideProject", "SaaS", "startups", "IndieApps"]
    try:
        for sub in subreddits:
            url = f"https://www.reddit.com/r/{sub}/new.json?limit=15"
            resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
            if resp.status_code != 200:
                continue
            for child in resp.json().get("data", {}).get("children", []):
                post = child.get("data", {})
                title = post.get("title", "")
                selftext = (post.get("selftext") or "")[:500]
                post_url = post.get("url", "")
                permalink = f"https://reddit.com{post.get('permalink', '')}"
                # 优先用外部链接，否则用帖子链接
                link = post_url if post_url and "reddit.com" not in post_url else permalink
                products.append({
                    "id": f"reddit_{post.get('id', '')}",
                    "name": title,
                    "description": selftext,
                    "url": link,
                    "source_url": permalink,
                    "score": post.get("score", 0),
                    "source": "reddit",
                    "subreddit": sub,
                    "timestamp": datetime.fromtimestamp(post.get("created_utc", 0)).isoformat(),
                })
        print(f"     {len(products)} 个")
    except Exception as e:
        print(f"     错误: {e}")
    return products


def fetch_producthunt():
    """Product Hunt - 通过官方 RSS 获取最新产品"""
    print("  🚀 Product Hunt...")
    products = []
    try:
        import feedparser
        feed = feedparser.parse("https://www.producthunt.com/feed")

        for entry in feed.entries:
            title = entry.get("title", "")
            link = entry.get("link", "")  # PH 讨论页链接

            # 从 content 中提取产品官网链接
            product_url = ""
            for c in entry.get("content", []):
                url_match = re.search(
                    r'href="(https://www\.producthunt\.com/r/[^"]+)"',
                    c.get("value", ""),
                )
                if url_match:
                    product_url = url_match.group(1)
                    break

            # 提取简介（去 HTML 标签）
            summary = ""
            for c in entry.get("content", []):
                raw = c.get("value", "")
                # 去掉 HTML 标签，保留文本
                summary = re.sub(r"<[^>]+>", "", raw).strip()
                # 去掉 "Discussion | Link" 等固定文本
                summary = re.sub(r"\s*Discussion\s*\|.*$", "", summary).strip()
                break

            # 发布时间
            published = entry.get("published", "")

            # 用产品名作为 ID
            product_id = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")

            products.append({
                "id": f"ph_{product_id}",
                "name": title,
                "description": summary[:500],
                "url": product_url or link,
                "source_url": link,
                "score": 0,
                "source": "producthunt",
                "timestamp": published,
            })

        print(f"     {len(products)} 个")
    except ImportError:
        print("     ⚠️ feedparser 未安装，跳过")
    except Exception as e:
        print(f"     错误: {e}")

    return products


def fetch_v2ex():
    """V2EX - 通过公开 API 获取热门主题"""
    print("  💬 V2EX...")
    products = []
    try:
        # 热门主题
        resp = requests.get(
            "https://www.v2ex.com/api/topics/hot.json",
            headers={"User-Agent": USER_AGENT},
            timeout=15,
        )
        if resp.status_code == 200:
            for topic in resp.json():
                title = topic.get("title", "")
                content = (topic.get("content") or "")[:500]
                url = topic.get("url", "")
                node = topic.get("node", {}).get("name", "")
                products.append({
                    "id": f"v2ex_{topic.get('id', '')}",
                    "name": title,
                    "description": content,
                    "url": url,
                    "source_url": url,
                    "score": topic.get("replies", 0),
                    "source": "v2ex",
                    "node": node,
                    "timestamp": topic.get("created", ""),
                })

        # 也获取创意/分享节点
        for node in ["create", "share", "ideas"]:
            try:
                resp = requests.get(
                    f"https://www.v2ex.com/api/topics/show.json?node_name={node}&page=1",
                    headers={"User-Agent": USER_AGENT},
                    timeout=10,
                )
                if resp.status_code == 200:
                    for topic in resp.json():
                        title = topic.get("title", "")
                        content = (topic.get("content") or "")[:500]
                        url = topic.get("url", "")
                        products.append({
                            "id": f"v2ex_{topic.get('id', '')}",
                            "name": title,
                            "description": content,
                            "url": url,
                            "source_url": url,
                            "score": topic.get("replies", 0),
                            "source": "v2ex",
                            "node": node,
                            "timestamp": topic.get("created", ""),
                        })
            except Exception:
                pass

        # 去重（V2EX 可能在不同节点重复）
        seen = set()
        unique = []
        for p in products:
            if p["id"] not in seen:
                seen.add(p["id"])
                unique.append(p)
        products = unique

        print(f"     {len(products)} 个")
    except Exception as e:
        print(f"     错误: {e}")
    return products


def fetch_twitter():
    """Twitter/X - 通过「为你推荐」获取 AI 产品相关推文"""
    print("  🐦 Twitter...")
    products = []

    if not Path(TWITTER_CLI).exists():
        print(f"     ⚠️ twitter-cli 未安装: {TWITTER_CLI}")
        return products

    try:
        result = subprocess.run(
            [TWITTER_CLI, "feed", "--type", "for-you", "-n", "50", "--json"],
            capture_output=True, text=True, timeout=90,
        )
        if result.returncode != 0:
            print("     获取失败")
            return products

        data = json.loads(result.stdout)
        for tweet in data.get("data", []):
            text = tweet.get("text", "")
            author = tweet.get("author", {})
            tweet_id = tweet.get("id", "")
            metrics = tweet.get("metrics", {})
            products.append({
                "id": f"tw_{tweet_id}",
                "name": text[:100].replace("\n", " "),
                "description": text[:500],
                "url": f"https://x.com/{author.get('screenName', '')}/status/{tweet_id}",
                "source_url": f"https://x.com/{author.get('screenName', '')}/status/{tweet_id}",
                "score": metrics.get("likes", 0) + metrics.get("retweets", 0) * 2,
                "source": "twitter",
                "author": author.get("screenName", ""),
                "timestamp": tweet.get("createdAtISO", ""),
            })

        print(f"     {len(products)} 条")
    except Exception as e:
        print(f"     错误: {e}")

    return products


def main():
    """主流程"""
    print("📡 抓取各渠道数据...")
    all_products = []

    # 抓取各渠道
    all_products.extend(fetch_hackernews())
    all_products.extend(fetch_reddit())
    all_products.extend(fetch_producthunt())
    all_products.extend(fetch_twitter())
    all_products.extend(fetch_v2ex())

    # 按热度排序
    all_products.sort(key=lambda x: x.get("score", 0), reverse=True)

    # 生成统一的产品 ID
    for p in all_products:
        p["product_id"] = generate_product_id(p)

    # 基于 product_id 去重（跨渠道同一产品只保留热度最高的）
    seen_ids = {}
    for p in all_products:
        pid = p["product_id"]
        if pid not in seen_ids:
            seen_ids[pid] = p
        else:
            # 保留热度更高的
            if p.get("score", 0) > seen_ids[pid].get("score", 0):
                seen_ids[pid] = p

    unique = list(seen_ids.values())

    # 统计各渠道数量
    channels = {}
    for p in unique:
        ch = p.get("source", "unknown")
        channels[ch] = channels.get(ch, 0) + 1

    print(f"\n✅ 共 {len(unique)} 个候选产品（去重后）")
    for ch, count in channels.items():
        print(f"   {ch}: {count}")

    # 保存
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "fetchedAt": datetime.now().isoformat(),
            "totalCount": len(unique),
            "channels": channels,
            "products": unique,
        }, f, ensure_ascii=False, indent=2)

    print(f"💾 已保存到 {OUTPUT_FILE}")

    # 输出摘要
    print("\n" + "=" * 60)
    print("📋 候选产品摘要（前 20 个）：")
    print("=" * 60)
    for i, p in enumerate(unique[:20], 1):
        name = p.get("name", "Unknown")[:60]
        score = p.get("score", 0)
        src = p.get("source", "?")
        url = p.get("url", "")
        desc = (p.get("description", "") or "")[:80]
        print(f"\n{i}. [{src}] {name}")
        print(f"   热度: {score} | URL: {url}")
        print(f"   描述: {desc}")


if __name__ == "__main__":
    main()

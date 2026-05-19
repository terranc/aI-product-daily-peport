#!/usr/bin/env python3
"""
原始数据抓取脚本
渠道：Hacker News、Reddit、Product Hunt、V2EX
输出 JSON 供 agent 做 LLM 分析
"""

import json
import os
import subprocess
import sys
import requests
from datetime import datetime
from pathlib import Path

OUTPUT_FILE = Path("/Volumes/EXTEND/aI-product-daily-peport/data/raw-candidates.json")
USER_AGENT = "agent-reach/1.0"
TWITTER_CLI = str(Path.home() / ".local" / "bin" / "twitter")


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
    """Product Hunt - 通过 Exa 搜索最新产品"""
    print("  🚀 Product Hunt...")
    products = []

    # 读取 API key
    exa_key = os.environ.get("EXA_API_KEY", "")
    if not exa_key:
        # 尝试从 secrets 文件读取
        secrets_file = Path.home() / ".config" / "shell" / "env.secrets.sh"
        if secrets_file.exists():
            for line in secrets_file.read_text().splitlines():
                if line.startswith("export EXA_API_KEY="):
                    exa_key = line.split("=", 1)[1].strip().strip("'\"")
                elif line.startswith("EXA_API_KEY="):
                    exa_key = line.split("=", 1)[1].strip().strip("'\"")

    if not exa_key:
        print("     ⚠️ EXA_API_KEY 未设置，跳过 Product Hunt")
        return products

    try:
        # 使用 Exa REST API 搜索 Product Hunt 最新产品
        resp = requests.post(
            "https://api.exa.ai/search",
            headers={
                "x-api-key": exa_key,
                "Content-Type": "application/json",
            },
            json={
                "query": "new AI app launched site:producthunt.com",
                "numResults": 15,
                "type": "auto",
                "contents": {
                    "text": {"maxCharacters": 500},
                },
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        for item in data.get("results", []):
            title = item.get("title", "")
            url = item.get("url", "")
            snippet = item.get("text", "") or ""
            products.append({
                "id": f"ph_{url.split('/')[-1] if '/' in url else str(len(products))}",
                "name": title,
                "description": snippet[:500],
                "url": url,
                "source_url": url,
                "score": 0,
                "source": "producthunt",
                "timestamp": item.get("publishedDate", ""),
            })

        print(f"     {len(products)} 个")
    except requests.exceptions.HTTPError as e:
        print(f"     Exa API 错误: {e}")
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
    """Twitter/X - 通过 twitter-cli 获取 AI 产品相关推文"""
    print("  🐦 Twitter...")
    products = []

    if not Path(TWITTER_CLI).exists():
        print(f"     ⚠️ twitter-cli 未安装: {TWITTER_CLI}")
        return products

    def parse_tweets(data):
        """解析推文数据"""
        import re
        tweets = []
        for tweet in data.get("data", []):
            text = tweet.get("text", "")
            author = tweet.get("author", {})
            tweet_id = tweet.get("id", "")
            metrics = tweet.get("metrics", {})
            tweets.append({
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
        return tweets

    try:
        # 1. "为你推荐"推文（算法推荐，质量最高）
        print("     获取「为你推荐」...")
        result = subprocess.run(
            [TWITTER_CLI, "feed", "--type", "for-you", "-n", "20", "--json"],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            fy_tweets = parse_tweets(data)
            products.extend(fy_tweets)
            print(f"     为你推荐: {len(fy_tweets)} 条")
        else:
            print(f"     为你推荐获取失败")

        # 2. 关键词搜索（补充覆盖）
        queries = [
            "AI app launched",
            "new AI tool",
        ]
        for q in queries:
            result = subprocess.run(
                [TWITTER_CLI, "search", q, "-n", "10", "--json"],
                capture_output=True, text=True, timeout=60,
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                search_tweets = parse_tweets(data)
                products.extend(search_tweets)

        print(f"     共 {len(products)} 条")
    except json.JSONDecodeError:
        print("     JSON 解析失败")
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

    # 基于 URL 去重
    seen_urls = set()
    unique = []
    for p in all_products:
        url = p.get("url", "") or p.get("source_url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(p)
        elif not url:
            unique.append(p)

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

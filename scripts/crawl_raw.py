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
import xml.etree.ElementTree as ET
import requests
from datetime import datetime
from pathlib import Path

try:
    from _paths import DATA_DIR
    OUTPUT_FILE = DATA_DIR / "raw-candidates.json"
except ImportError:
    OUTPUT_FILE = Path("/Volumes/EXTEND/aI-product-daily-peport/data/raw-candidates.json")
USER_AGENT = "agent-reach/1.0"
TWITTER_CLI = str(Path.home() / ".local" / "bin" / "twitter")


# ─── 代理配置 ─────────────────────────────────────────────────────────
# V2EX / Reddit 在本机直连不可达（实测直连超时、走代理 200），且 cron 环境没有
# 系统代理 env，requests 默认会直连 → 两渠道被静默跳过。这里显式给需要翻墙的
# 渠道挂代理，不依赖外部 env；代理不可用时自动回落直连，不阻断其它渠道。
def _proxy_candidates():
    """按优先级返回候选代理地址（可用 PROXY_URL / HTTPS_PROXY env 覆盖）。"""
    env_proxy = (
        os.environ.get("PROXY_URL")
        or os.environ.get("https_proxy")
        or os.environ.get("HTTPS_PROXY")
        or os.environ.get("http_proxy")
        or os.environ.get("HTTP_PROXY")
    )
    urls = []
    if env_proxy:
        urls.append(env_proxy)
    urls.append("http://127.0.0.1:7890")  # mihomo 默认端口
    return urls


def _proxy_alive(url, timeout=5):
    """探测代理是否能出网（走 google 204 端点，轻量且稳定）。"""
    try:
        r = requests.get(
            "https://www.google.com/generate_204",
            proxies={"http": url, "https": url},
            timeout=timeout,
        )
        return r.status_code in (200, 204)
    except Exception:
        return False


_PROXY_CACHE = {"resolved": False, "proxy": None}


def get_proxy():
    """解析一个可用代理；不可用则返回 None（调用方回落直连）。结果缓存。"""
    if _PROXY_CACHE["resolved"]:
        return _PROXY_CACHE["proxy"]
    proxy = None
    for url in _proxy_candidates():
        if _proxy_alive(url):
            proxy = url
            break
    _PROXY_CACHE["resolved"] = True
    _PROXY_CACHE["proxy"] = proxy
    if proxy:
        print(f"  🌐 代理可用: {proxy}")
    else:
        print("  ⚠️  代理不可用，V2EX/Reddit 将尝试直连（可能失败）")
    return proxy


def proxied_get(url, **kwargs):
    """对需要翻墙的渠道发请求：优先走代理，失败回落直连。"""
    proxy = get_proxy()
    if proxy:
        kwargs.setdefault("timeout", 20)
        return requests.get(url, proxies={"http": proxy, "https": proxy}, **kwargs)
    return requests.get(url, **kwargs)



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
    """Reddit - 通过 RSS Feed（JSON API 已被 Reddit 禁止）"""
    print("  🟠 Reddit...")
    products = []
    subreddits = ["SideProject", "SaaS", "startups", "IndieApps"]
    try:
        for sub in subreddits:
            url = f"https://www.reddit.com/r/{sub}/new/.rss?limit=15"
            resp = proxied_get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
            if resp.status_code != 200:
                continue
            # Parse Atom XML
            root = ET.fromstring(resp.content)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("atom:entry", ns):
                title_el = entry.find("atom:title", ns)
                title = title_el.text.strip() if title_el is not None and title_el.text else ""
                # id is like "reddit.com/r/SideProject/abc123/..."
                id_el = entry.find("atom:id", ns)
                post_id = id_el.text.strip().split("/")[-1] if id_el is not None and id_el.text else ""
                # link: try to find external link, fallback to Reddit permalink
                links = entry.findall("atom:link", ns)
                permalink = ""
                external_url = ""
                for link in links:
                    href = link.get("href", "")
                    if "/comments/" in href and not external_url:
                        permalink = href
                    elif "reddit.com" not in href and href.startswith("http"):
                        external_url = href
                # content: sometimes contains the post body
                content_el = entry.find("atom:content", ns)
                content = ""
                if content_el is not None and content_el.text:
                    content = re.sub(r"<[^>]+>", "", content_el.text)[:500]
                # published
                pub_el = entry.find("atom:published", ns)
                published = pub_el.text if pub_el is not None and pub_el.text else ""
                link = external_url if external_url else permalink
                products.append({
                    "id": f"reddit_{post_id}",
                    "name": title,
                    "description": content,
                    "url": link,
                    "source_url": permalink,
                    "score": 0,  # RSS 不提供 score
                    "source": "reddit",
                    "subreddit": sub,
                    "timestamp": published,
                })
        print(f"     {len(products)} 个")
    except Exception as e:
        print(f"     错误: {e}")
    return products


def fetch_producthunt():
    """Product Hunt - 通过官方 RSS 获取最新产品

    优先用 feedparser；未安装时用标准库兜底解析（PH 的 feed 是 Atom，
    xml.etree 即可，不需要第三方依赖 —— 见 skill 记录：本机 pip 装 feedparser
    会被 Tirith 拦截，所以必须有兜底路径）。
    """
    print("  🚀 Product Hunt...")
    products = []
    try:
        raw_feed = proxied_get(
            "https://www.producthunt.com/feed",
            headers={"User-Agent": USER_AGENT},
            timeout=20,
        )
        if raw_feed.status_code != 200:
            print(f"     ⚠️ HTTP {raw_feed.status_code}，跳过")
            return products
        content_bytes = raw_feed.content
    except Exception as e:
        print(f"     错误（获取 feed）: {e}")
        return products

    entries = []
    try:
        import feedparser
        feed = feedparser.parse(content_bytes)
        for e in feed.entries:
            entries.append({
                "title": e.get("title", ""),
                "link": e.get("link", ""),
                "content_html": " ".join(
                    c.get("value", "") for c in e.get("content", [])
                ),
                "published": e.get("published", ""),
            })
    except ImportError:
        # 标准库兜底：PH feed 是 Atom（NS = http://www.w3.org/2005/Atom）
        try:
            root = ET.fromstring(content_bytes)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("atom:entry", ns):
                title_el = entry.find("atom:title", ns)
                content_el = entry.find("atom:content", ns)
                link_href = ""
                for link in entry.findall("atom:link", ns):
                    if link.get("rel") in (None, "alternate"):
                        link_href = link.get("href", "")
                        break
                pub_el = entry.find("atom:published", ns)
                # post id：<id>tag:...Post/12345</id> → 构造标准 PH 链接
                id_el = entry.find("atom:id", ns)
                post_id = ""
                if id_el is not None and id_el.text:
                    m = re.search(r"Post/(\d+)", id_el.text)
                    if m:
                        post_id = m.group(1)
                entries.append({
                    "title": (title_el.text or "").strip() if title_el is not None else "",
                    "link": link_href or (
                        f"https://www.producthunt.com/posts/{post_id}" if post_id else ""
                    ),
                    "content_html": content_el.text or "" if content_el is not None else "",
                    "published": (pub_el.text or "") if pub_el is not None else "",
                })
        except Exception as e:
            print(f"     错误（解析 feed）: {e}")
            return products

    for entry in entries:
        title = entry["title"]
        link = entry["link"]
        content_html = entry["content_html"]

        # 从 content 中提取产品官网链接
        product_url = ""
        url_match = re.search(
            r'href="(https://www\.producthunt\.com/r/[^"]+)"', content_html
        )
        if url_match:
            product_url = url_match.group(1)

        # 提取简介（去 HTML 标签 + 去掉固定尾串）
        summary = re.sub(r"<[^>]+>", "", content_html).strip()
        summary = re.sub(r"\s*Discussion\s*\|.*$", "", summary).strip()
        # content 是 HTML 转义文本时可能出现实体，做最小还原
        summary = (
            summary.replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&quot;", '"')
            .replace("&#39;", "'")
        )

        product_id = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")

        products.append({
            "id": f"ph_{product_id}",
            "name": title,
            "description": summary[:500],
            "url": product_url or link,
            "source_url": link,
            "score": 0,
            "source": "producthunt",
            "timestamp": entry["published"],
        })

    print(f"     {len(products)} 个")
    return products


def fetch_v2ex():
    """V2EX - 通过公开 API 获取热门主题"""
    print("  💬 V2EX...")
    products = []
    try:
        # 热门主题
        resp = proxied_get(
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
                resp = proxied_get(
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

    # 加载 twitter-cli 凭据（auth_token/ct0/代理），文件不存在则用已有环境变量
    env = dict(os.environ)
    cred_file = Path.home() / ".twitter-cli.env"
    if cred_file.exists():
        try:
            for line in cred_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env.setdefault(k.strip(), v.strip())
        except Exception as e:
            print(f"     凭据加载警告: {e}")

    try:
        result = subprocess.run(
            [TWITTER_CLI, "feed", "--type", "for-you", "-n", "50", "--json"],
            capture_output=True, text=True, timeout=90, env=env,
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

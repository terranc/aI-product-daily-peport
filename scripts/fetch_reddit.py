#!/usr/bin/env python3
"""
Reddit AI 产品抓取脚本
抓取多个子版块的 AI 产品相关帖子
"""

import json
import requests
import re
from datetime import datetime

REDDIT_BASE = "https://www.reddit.com"
USER_AGENT = "AI-Product-Radar/1.0"

# 目标子版块和关键词
SUBREDDITS = [
    {'name': 'SideProject', 'keywords': ['ai', 'llm', 'gpt', 'chatgpt', 'agent']},
    {'name': 'SaaS', 'keywords': ['ai', 'launched', 'new tool']},
    {'name': 'artificial', 'keywords': ['app', 'tool', 'assistant']},
    {'name': 'ChatGPT', 'keywords': ['built', 'launched', 'app', 'tool']},
    {'name': 'Entrepreneur', 'keywords': ['ai tool', 'saas', 'launched']},
    {'name': 'startups', 'keywords': ['ai', 'launched', 'shipped']},
]

def fetch_subreddit_posts(subreddit, mode='hot', limit=25):
    """获取子版块帖子"""
    try:
        url = f"{REDDIT_BASE}/r/{subreddit}/{mode}.json"
        params = {'limit': limit, 'raw_json': 1}
        headers = {'User-Agent': USER_AGENT}

        response = requests.get(url, params=params, headers=headers, timeout=15)

        if response.status_code == 403:
            print(f"  ⚠️ Reddit 403 for r/{subreddit} (服务器 IP 被限制)")
            return []

        response.raise_for_status()
        data = response.json()

        posts = []
        for child in data.get('data', {}).get('children', []):
            post = child.get('data', {})
            posts.append(post)

        return posts

    except Exception as e:
        print(f"  ❌ Error fetching r/{subreddit}: {e}")
        return []

def search_reddit(query, limit=25):
    """搜索 Reddit"""
    try:
        url = f"{REDDIT_BASE}/search.json"
        params = {'q': query, 'limit': limit, 'sort': 'new', 't': 'week', 'raw_json': 1}
        headers = {'User-Agent': USER_AGENT}

        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        posts = []
        for child in data.get('data', {}).get('children', []):
            posts.append(child.get('data', {}))

        return posts

    except Exception as e:
        print(f"  ❌ Error searching Reddit: {e}")
        return []

def is_ai_product_post(post, keywords):
    """判断帖子是否是 AI 产品相关"""
    title = (post.get('title', '') or '').lower()
    selftext = (post.get('selftext', '') or '').lower()
    content = f"{title} {selftext}"

    # 必须有关键词
    keyword_match = any(kw in content for kw in keywords)
    if not keyword_match:
        return False

    # 排除纯讨论帖
    exclude_words = ['question', 'help me', 'how to', 'what is', 'discussion']
    if any(ew in title for ew in exclude_words) and 'launched' not in title and 'shipped' not in title:
        return False

    return True

def extract_product_from_post(post):
    """从 Reddit 帖子提取产品信息"""
    title = post.get('title', '')

    # 清理标签
    title = re.sub(r'^\[(Show|Launch|I built|New|Update)\]\s*', '', title, flags=re.IGNORECASE)

    # 提取 URL
    url = post.get('url', '')
    if 'reddit.com' in url or not url.startswith('http'):
        # 尝试从 selftext 提取
        selftext = post.get('selftext', '')
        urls = re.findall(r'https?://[^\s\)]+', selftext)
        external_urls = [u for u in urls if 'reddit.com' not in u and 'imgur.com' not in u]
        url = external_urls[0] if external_urls else ''

    return {
        'id': f"reddit_{post.get('id', '')}",
        'name': title[:80],
        'title': post.get('title', ''),
        'url': url,
        'redditUrl': f"https://reddit.com{post.get('permalink', '')}",
        'description': (post.get('selftext', '') or '')[:500],
        'score': post.get('score', 0),
        'upvotes': post.get('ups', 0),
        'comments': post.get('num_comments', 0),
        'subreddit': post.get('subreddit', ''),
        'author': post.get('author', ''),
        'timestamp': datetime.fromtimestamp(post.get('created_utc', 0)).isoformat(),
        'source': 'reddit',
        'source_url': f"https://reddit.com{post.get('permalink', '')}"
    }

def fetch_reddit_products():
    """主抓取流程"""
    all_products = []
    seen_ids = set()

    print("  🟠 搜索 Reddit 子版块...")

    for sub_config in SUBREDDITS:
        subreddit = sub_config['name']
        keywords = sub_config['keywords']

        # 获取热门和最新帖子
        for mode in ['hot', 'new']:
            posts = fetch_subreddit_posts(subreddit, mode=mode, limit=25)
            for post in posts:
                if is_ai_product_post(post, keywords):
                    product = extract_product_from_post(post)
                    if product['id'] not in seen_ids and product.get('url'):
                        seen_ids.add(product['id'])
                        all_products.append(product)

    # 额外搜索
    print("  🔍 扩展搜索...")
    for query in ['AI tool launched', 'built an AI app', 'AI SaaS launched']:
        posts = search_reddit(query, limit=10)
        for post in posts:
            product = extract_product_from_post(post)
            if product['id'] not in seen_ids and product.get('url'):
                seen_ids.add(product['id'])
                all_products.append(product)

    # 按热度排序
    all_products.sort(key=lambda x: x.get('score', 0), reverse=True)

    return all_products[:30]

if __name__ == '__main__':
    products = fetch_reddit_products()
    print(f"\nFound {len(products)} AI products on Reddit")
    for p in products[:5]:
        print(f"- {p['name']} (r/{p['subreddit']}, {p['score']} pts): {p.get('url', 'N/A')}")

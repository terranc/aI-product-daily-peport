#!/usr/bin/env python3
"""
Twitter/X AI 产品抓取脚本
使用 agent-reach 的 bird 工具
"""

import subprocess
import json
import re
from datetime import datetime

# 搜索查询列表
TWITTER_QUERIES = [
    '"AI tool" launched OR shipped OR built',
    '"new AI app" OR "AI assistant" launched',
    '"just shipped" AI OR LLM OR GPT',
    '"Show HN" AI',
    '#buildinpublic AI tool',
    'site:producthunt.com AI launched',
]

# 重点关注的账号
WATCH_ACCOUNTS = [
    'ProductHunt', 'ainewsletter', 'TheRundownAI',
    'ai_breakdown', 'bleedingedgeai', 'Levelsio',
    'marc_louvion', 'yaborobbins', 'swyx'
]

def search_twitter_via_bird(query, limit=10):
    """使用 bird CLI 搜索 Twitter"""
    try:
        cmd = ['bird', 'search', query, '-n', str(limit), '--json']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            print(f"  bird search failed for '{query}': {result.stderr}")
            return []

        # bird 输出可能是多行 JSON 或 JSON 数组
        lines = result.stdout.strip().split('\n')
        tweets = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                tweet = json.loads(line)
                tweets.append(tweet)
            except json.JSONDecodeError:
                continue

        # 如果整体是一个 JSON 数组
        if not tweets:
            try:
                tweets = json.loads(result.stdout)
                if isinstance(tweets, dict):
                    tweets = [tweets]
            except json.JSONDecodeError:
                pass

        return tweets

    except FileNotFoundError:
        print("  ⚠️ bird CLI 未安装，跳过 Twitter 搜索")
        return []
    except subprocess.TimeoutExpired:
        print(f"  ⏰ bird search 超时: {query}")
        return []
    except Exception as e:
        print(f"  ❌ bird search 错误: {e}")
        return []

def get_user_tweets(username, limit=10):
    """获取用户最近推文"""
    try:
        cmd = ['bird', 'user-tweets', f'@{username}', '-n', str(limit), '--json']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            return []

        try:
            tweets = json.loads(result.stdout)
            return tweets if isinstance(tweets, list) else [tweets]
        except:
            return []

    except Exception:
        return []

def extract_product_from_tweet(tweet):
    """从推文中提取产品信息"""
    text = tweet.get('text', '') or tweet.get('content', '') or tweet.get('full_text', '')
    if not text:
        return None

    # 提取 URL
    urls = re.findall(r'https?://[^\s]+', text)

    # 过滤掉 Twitter 自身链接
    external_urls = [u for u in urls if 'twitter.com' not in u and 'x.com' not in u and 't.co' not in u]

    # 提取名称（通常是 @mention 或推文开头的关键词）
    author = tweet.get('author', {}).get('username', '') if isinstance(tweet.get('author'), dict) else tweet.get('user', {}).get('screen_name', '')

    # 从文本中提取产品名
    name_match = re.search(r'(?:launched|shipped|built|introducing|meet)\s+(?:our\s+)?(.+?)(?:\s*[-–—:]|\s*$)', text, re.IGNORECASE)
    name = name_match.group(1).strip() if name_match else text[:50].split('.')[0].strip()

    return {
        'id': f"tw_{tweet.get('id', '')}",
        'name': name[:80],
        'title': text[:200],
        'url': external_urls[0] if external_urls else '',
        'twitterUrl': tweet.get('url', '') or f"https://x.com/{author}/status/{tweet.get('id', '')}",
        'description': text[:500],
        'score': tweet.get('public_metrics', {}).get('like_count', 0) or tweet.get('likes', 0) or 0,
        'likes': tweet.get('public_metrics', {}).get('like_count', 0) or tweet.get('likes', 0) or 0,
        'retweets': tweet.get('public_metrics', {}).get('retweet_count', 0) or tweet.get('retweets', 0) or 0,
        'author': author,
        'timestamp': tweet.get('created_at', datetime.now().isoformat()),
        'source': 'twitter',
        'source_url': tweet.get('url', '') or f"https://x.com/{author}/status/{tweet.get('id', '')}"
    }

def fetch_twitter_products():
    """抓取 Twitter AI 产品"""
    all_products = []
    seen_ids = set()

    print("  🐦 搜索推文...")

    # 搜索关键词
    for query in TWITTER_QUERIES[:3]:  # 限制查询数量
        tweets = search_twitter_via_bird(query, limit=15)
        for tweet in tweets:
            product = extract_product_from_tweet(tweet)
            if product and product['id'] not in seen_ids and product.get('url'):
                seen_ids.add(product['id'])
                all_products.append(product)

    # 获取关注账号的推文
    print("  📡 检查关注账号...")
    for account in WATCH_ACCOUNTS[:5]:  # 限制数量
        tweets = get_user_tweets(account, limit=5)
        for tweet in tweets:
            product = extract_product_from_tweet(tweet)
            if product and product['id'] not in seen_ids and product.get('url'):
                seen_ids.add(product['id'])
                all_products.append(product)

    # 按热度排序
    all_products.sort(key=lambda x: x.get('score', 0) + x.get('likes', 0), reverse=True)

    return all_products[:30]

if __name__ == '__main__':
    products = fetch_twitter_products()
    print(f"\nFound {len(products)} AI products on Twitter")
    for p in products[:5]:
        print(f"- {p['name']} ({p['score']} likes): {p.get('url', 'N/A')}")

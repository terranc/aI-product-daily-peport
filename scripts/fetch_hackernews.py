#!/usr/bin/env python3
"""
Hacker News 产品抓取脚本
抓取 Show HN 和热门帖子，筛选 AI 相关产品
"""

import json
import requests
import re
from datetime import datetime
from urllib.parse import urlparse

HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
HN_SHOW_URL = "https://hacker-news.firebaseio.com/v0/showstories.json"
HN_TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_NEW_URL = "https://hacker-news.firebaseio.com/v0/newstories.json"

# AI 相关关键词
AI_KEYWORDS = [
    'ai', 'llm', 'gpt', 'chatgpt', 'claude', 'gemini', 'assistant',
    'agent', 'copilot', 'automation', 'generate', 'generative',
    'openai', 'anthropic', 'langchain', 'prompt', 'tools',
    'wrapper', 'app', 'platform', 'service'
]

def fetch_item(item_id):
    """获取单个帖子详情"""
    try:
        response = requests.get(HN_ITEM_URL.format(item_id), timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching item {item_id}: {e}")
        return None

def is_ai_related(item):
    """判断是否为 AI 相关产品"""
    if not item:
        return False

    title = item.get('title', '').lower()
    text = item.get('text', '').lower() if item.get('text') else ''

    # 检查关键词
    content = f"{title} {text}"
    keyword_count = sum(1 for kw in AI_KEYWORDS if kw in content)

    # Show HN 帖子更可能是产品发布
    is_show_hn = title.startswith('show hn:') or title.startswith('showhackernews')

    # 需要有一定热度
    score = item.get('score', 0)

    # 必须有链接（产品网站或演示）
    has_url = bool(item.get('url'))

    # 判断逻辑
    if is_show_hn and keyword_count >= 2:
        return True
    if keyword_count >= 3 and score >= 10 and has_url:
        return True

    return False

def extract_product_info(item):
    """提取产品信息"""
    title = item.get('title', '')

    # 清理标题
    title = re.sub(r'^(Show HN:?|Show Hacker News:?)[\s:]*', '', title, flags=re.IGNORECASE)

    return {
        'id': f"hn_{item.get('id')}",
        'name': title.split('–')[0].split('-')[0].split(':')[0].strip(),
        'title': title,
        'url': item.get('url'),
        'hn_url': f"https://news.ycombinator.com/item?id={item.get('id')}",
        'description': item.get('text', '')[:500] if item.get('text') else '',
        'score': item.get('score', 0),
        'comments': item.get('descendants', 0),
        'timestamp': datetime.fromtimestamp(item.get('time', 0)).isoformat(),
        'source': 'hackernews',
        'source_url': f"https://news.ycombinator.com/item?id={item.get('id')}"
    }

def fetch_hackernews_products(limit=100):
    """抓取 Hacker News 产品列表"""
    products = []

    # 抓取 Show HN
    try:
        response = requests.get(HN_SHOW_URL, timeout=10)
        show_ids = response.json()[:50]

        for item_id in show_ids:
            item = fetch_item(item_id)
            if item and is_ai_related(item):
                products.append(extract_product_info(item))
    except Exception as e:
        print(f"Error fetching Show HN: {e}")

    # 抓取热门帖子
    try:
        response = requests.get(HN_TOP_URL, timeout=10)
        top_ids = response.json()[:limit]

        for item_id in top_ids:
            item = fetch_item(item_id)
            if item and is_ai_related(item):
                product = extract_product_info(item)
                # 避免重复
                if not any(p['id'] == product['id'] for p in products):
                    products.append(product)
    except Exception as e:
        print(f"Error fetching top stories: {e}")

    # 按热度排序
    products.sort(key=lambda x: x['score'], reverse=True)

    return products

if __name__ == '__main__':
    products = fetch_hackernews_products()
    print(f"Found {len(products)} AI products on HN")
    for p in products[:5]:
        print(f"- {p['name']} ({p['score']} pts): {p['url']}")

#!/usr/bin/env python3
"""
GitHub Trending 和搜索脚本
抓取 AI 相关的热门项目
"""

import json
import requests
from datetime import datetime, timedelta

# GitHub Search API
GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"

AI_QUERIES = [
    "ai tools stars:>50",
    "llm app stars:>50",
    "chatgpt assistant stars:>50",
    "ai agent stars:>50",
    "claude automation stars:>50",
    "openai wrapper stars:>50"
]

def fetch_github_trending():
    """抓取 GitHub 上 AI 相关的热门项目"""
    products = []
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'AI-Product-Radar'
    }

    # 获取日期范围（最近7天）
    date_from = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    for query in AI_QUERIES[:3]:  # 限制查询数量避免 rate limit
        try:
            params = {
                'q': f'{query} created:>{date_from}',
                'sort': 'stars',
                'order': 'desc',
                'per_page': 10
            }

            response = requests.get(GITHUB_SEARCH_URL, params=params, headers=headers, timeout=15)

            if response.status_code == 403:
                print("GitHub API rate limit exceeded")
                break

            response.raise_for_status()
            data = response.json()

            for repo in data.get('items', []):
                product = {
                    'id': f"gh_{repo['id']}",
                    'name': repo['name'],
                    'title': f"{repo['name']}: {repo['description'][:100] if repo['description'] else 'AI tool'}",
                    'url': repo['html_url'],
                    'description': repo['description'] or '',
                    'homepage': repo['homepage'] or '',
                    'score': repo['stargazers_count'],
                    'stars': repo['stargazers_count'],
                    'forks': repo['forks_count'],
                    'language': repo['language'] or 'Unknown',
                    'timestamp': repo['created_at'],
                    'updated_at': repo['updated_at'],
                    'source': 'github',
                    'source_url': repo['html_url'],
                    'topics': repo.get('topics', [])
                }

                # 避免重复
                if not any(p['id'] == product['id'] for p in products):
                    products.append(product)

        except Exception as e:
            print(f"Error fetching GitHub: {e}")

    # 按 star 数排序
    products.sort(key=lambda x: x['stars'], reverse=True)

    return products[:20]

if __name__ == '__main__':
    products = fetch_github_trending()
    print(f"Found {len(products)} AI projects on GitHub")
    for p in products[:5]:
        print(f"- {p['name']} (⭐ {p['stars']}): {p['url']}")

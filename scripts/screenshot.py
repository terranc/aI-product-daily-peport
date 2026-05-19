#!/usr/bin/env python3
"""
网站截图和 App Store 截图抓取
使用 webshot.site API 生成网站截图
"""

import requests
import time
import os
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

ASSETS_DIR = Path("/Volumes/EXTEND/aI-product-daily-peport/assets/screenshots")
WEBSHOT_API = "https://webshot.site/api/capture"


def take_screenshot(url, product_id):
    """
    使用 webshot.site API 截取网站截图
    文件名格式: {product_id}_{timestamp}.png
    """
    if not url:
        return None

    parsed = urlparse(url)
    if not parsed.netloc:
        return None

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{product_id}_{timestamp}.png"
    output_file = ASSETS_DIR / filename

    try:
        response = requests.post(
            WEBSHOT_API,
            json={
                'url': url,
                'format': 'png',
                'mode': 'desktop_viewport',  # 首屏 1920x1080
            },
            timeout=120,
        )

        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"  📸 截图成功: {filename} ({len(response.content)} bytes)")
            return str(output_file.relative_to("/Volumes/EXTEND/aI-product-daily-peport"))

        elif response.status_code == 429:
            wait = int(response.headers.get('Retry-After', 60))
            print(f"  ⏰ 速率限制，等待 {wait} 秒...")
            time.sleep(wait)
            # 重试一次
            response = requests.post(
                WEBSHOT_API,
                json={'url': url, 'format': 'png', 'mode': 'desktop_viewport'},
                timeout=120,
            )
            if response.status_code == 200:
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                print(f"  📸 截图成功（重试）: {filename}")
                return str(output_file.relative_to("/Volumes/EXTEND/aI-product-daily-peport"))

        else:
            print(f"  ❌ 截图失败 HTTP {response.status_code}: {url}")

    except Exception as e:
        print(f"  ❌ 截图错误: {url} — {e}")

    return None


def search_app_store(app_name):
    """
    搜索 App Store 获取应用信息
    使用 iTunes Search API
    """
    try:
        params = {
            'term': app_name,
            'entity': 'software',
            'limit': 5
        }

        response = requests.get(
            'https://itunes.apple.com/search',
            params=params,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        results = data.get('results', [])
        if not results:
            return None

        for app in results:
            result_name = app.get('trackName', '').lower()
            if app_name.lower() in result_name or result_name in app_name.lower():
                return {
                    'name': app.get('trackName'),
                    'url': app.get('trackViewUrl'),
                    'bundleId': app.get('bundleId'),
                    'screenshots': app.get('screenshotUrls', [])[:3],
                    'description': app.get('description', '')[:500],
                    'icon': app.get('artworkUrl512') or app.get('artworkUrl100'),
                    'rating': app.get('averageUserRating'),
                    'ratingCount': app.get('userRatingCount')
                }

        if results:
            app = results[0]
            return {
                'name': app.get('trackName'),
                'url': app.get('trackViewUrl'),
                'bundleId': app.get('bundleId'),
                'screenshots': app.get('screenshotUrls', [])[:3],
                'description': app.get('description', '')[:500],
                'icon': app.get('artworkUrl512') or app.get('artworkUrl100'),
                'rating': app.get('averageUserRating'),
                'ratingCount': app.get('userRatingCount')
            }

    except Exception as e:
        print(f"  ❌ App Store 搜索失败 '{app_name}': {e}")

    return None


def download_app_screenshots(screenshot_urls, product_id):
    """
    下载 App Store 截图，文件名加时间戳
    """
    saved_paths = []
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    for i, url in enumerate(screenshot_urls[:3]):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            filename = f"{product_id}_app_{i+1}_{timestamp}.jpg"
            output_file = ASSETS_DIR / filename
            ASSETS_DIR.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'wb') as f:
                f.write(response.content)

            saved_paths.append(str(output_file.relative_to("/Volumes/EXTEND/aI-product-daily-peport")))
            print(f"  📱 App 截图下载: {filename}")

        except Exception as e:
            print(f"  ❌ 下载截图失败 {url}: {e}")

    return saved_paths


def process_product_screenshots(product):
    """
    处理产品的截图需求
    - 网站/App: 用 webshot.site 截图
    - iOS App: 搜索 App Store 获取截图
    """
    product_id = product.get('id', 'unknown')
    result = {
        'screenshotUrl': None,
        'appStoreScreenshots': [],
        'appStoreInfo': None
    }

    product_type = product.get('type', 'website')
    url = product.get('url') or product.get('homepage', '')

    if product_type in ['ios_app', 'app']:
        # App: 先搜索 App Store
        app_info = search_app_store(product.get('name', ''))
        if app_info:
            result['appStoreInfo'] = app_info
            if app_info.get('screenshots'):
                result['appStoreScreenshots'] = download_app_screenshots(
                    app_info['screenshots'], product_id
                )
            result['appStoreName'] = app_info['name']
            result['appStoreUrl'] = app_info['url']

        # 如果有官网也截一张
        if url:
            screenshot_path = take_screenshot(url, product_id)
            result['screenshotUrl'] = screenshot_path

    elif url:
        # 网站/SaaS: webshot.site 截图
        screenshot_path = take_screenshot(url, product_id)
        result['screenshotUrl'] = screenshot_path

    return result


if __name__ == '__main__':
    import json
    test = {'id': 'test', 'name': 'Drea', 'type': 'website', 'url': 'https://drea.fm/'}
    r = process_product_screenshots(test)
    print(json.dumps(r, indent=2, ensure_ascii=False))

#!/usr/bin/env python3
"""
网站截图和 App Store 截图抓取
"""

import subprocess
import os
from pathlib import Path
from urllib.parse import urlparse

ASSETS_DIR = Path("/Volumes/EXTEND/aI-product-daily-peport/assets/screenshots")

def take_screenshot(url, product_id):
    """
    使用 playwright 截取网站截图
    """
    if not url:
        return None

    # 提取域名用于文件名
    parsed = urlparse(url)
    if not parsed.netloc:
        return None

    output_file = ASSETS_DIR / f"{product_id}.png"
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    try:
        # 使用 playwright 截图
        script = f"""
const {{ chromium }} = require('playwright');
(async () => {{
    const browser = await chromium.launch({{ headless: true }});
    const context = await browser.newContext({{
        viewport: {{ width: 1440, height: 900 }},
        deviceScaleFactor: 1
    }});
    const page = await context.newPage();

    try {{
        await page.goto('{url}', {{ waitUntil: 'networkidle', timeout: 30000 }});
        await page.waitForTimeout(3000); // 等待动画完成
        await page.screenshot({{ path: '{output_file}', fullPage: false }});
        console.log('Screenshot saved: {output_file}');
    }} catch (e) {{
        console.error('Error:', e.message);
        process.exit(1);
    }}

    await browser.close();
}})();
"""

        # 执行 Node 脚本（自动查找 node 路径）
        import shutil
        node_bin = shutil.which('node') or '/opt/homebrew/bin/node'

        result = subprocess.run(
            [node_bin, '-e', script],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0 and output_file.exists():
            return str(output_file.relative_to("/Volumes/EXTEND/aI-product-daily-peport"))

    except Exception as e:
        print(f"Screenshot error for {url}: {e}")

    return None

def search_app_store(app_name):
    """
    搜索 App Store 获取应用信息
    使用 iTunes Search API
    """
    import requests

    try:
        # iTunes Search API
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

        # 找到最匹配的结果
        for app in results:
            result_name = app.get('trackName', '').lower()
            if app_name.lower() in result_name or result_name in app_name.lower():
                return {
                    'name': app.get('trackName'),
                    'url': app.get('trackViewUrl'),
                    'bundleId': app.get('bundleId'),
                    'screenshots': app.get('screenshotUrls', [])[:3],  # 最多3张
                    'description': app.get('description', '')[:500],
                    'icon': app.get('artworkUrl512') or app.get('artworkUrl100'),
                    'rating': app.get('averageUserRating'),
                    'ratingCount': app.get('userRatingCount')
                }

        # 如果没有精确匹配，返回第一个
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
        print(f"App Store search error for '{app_name}': {e}")

    return None

def download_app_screenshots(screenshot_urls, product_id):
    """
    下载 App Store 截图
    """
    import requests

    saved_paths = []

    for i, url in enumerate(screenshot_urls[:3]):  # 最多3张
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            filename = ASSETS_DIR / f"{product_id}_app_{i+1}.jpg"
            ASSETS_DIR.mkdir(parents=True, exist_ok=True)

            with open(filename, 'wb') as f:
                f.write(response.content)

            saved_paths.append(str(filename.relative_to("/Volumes/EXTEND/aI-product-daily-peport")))

        except Exception as e:
            print(f"Error downloading screenshot {url}: {e}")

    return saved_paths

def process_product_screenshots(product):
    """
    处理产品的截图需求
    网站类产品截首页，App类搜索App Store并下载截图
    """
    product_id = product.get('id', 'unknown')
    result = {
        'screenshotUrl': None,
        'appStoreScreenshots': [],
        'appStoreInfo': None
    }

    product_type = product.get('type', 'website')

    if product_type == 'website':
        # 网站截图
        url = product.get('url') or product.get('homepage')
        if url:
            screenshot_path = take_screenshot(url, product_id)
            result['screenshotUrl'] = screenshot_path

    elif product_type in ['ios_app', 'app']:
        # App Store 搜索
        app_info = search_app_store(product.get('name', ''))
        if app_info:
            result['appStoreInfo'] = app_info
            # 下载截图
            if app_info.get('screenshots'):
                result['appStoreScreenshots'] = download_app_screenshots(
                    app_info['screenshots'],
                    product_id
                )
            # 更新产品信息
            result['appStoreName'] = app_info['name']
            result['appStoreUrl'] = app_info['url']

    # 如果是 GitHub 项目，也截个网站图（如果有 homepage）
    if product_type == 'github':
        homepage = product.get('homepage')
        if homepage:
            screenshot_path = take_screenshot(homepage, product_id)
            result['screenshotUrl'] = screenshot_path

    return result

if __name__ == '__main__':
    # 测试
    test_product = {
        'id': 'test_001',
        'name': 'Test App',
        'type': 'website',
        'url': 'https://example.com'
    }
    result = process_product_screenshots(test_product)
    print(json.dumps(result, indent=2))

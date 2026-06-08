#!/usr/bin/env python3
"""
产品截图处理
- 网站产品：使用 webshot.site API 截图保存到本地
- APP 产品：从 iTunes API 获取 App Store 截图 URL（不下载，直接引用远程地址）
"""

import requests
import time
from datetime import datetime
from pathlib import Path

ASSETS_DIR = Path("/Volumes/EXTEND/aI-product-daily-peport/assets/screenshots")
WEBSHOT_API = "https://webshot.site/api/capture"


def take_website_screenshot(url, product_id, max_retries=2):
    """
    使用 webshot.site API 截取网站截图，保存到本地
    支持 429（速率限制）和 530（服务端临时故障）自动重试
    """
    if not url:
        return None

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 清理 product_id 中的特殊字符，避免创建子目录
    safe_id = product_id.replace('/', '_').replace('\\', '_').replace(':', '_')
    filename = f"{safe_id}_{timestamp}.png"
    output_file = ASSETS_DIR / filename

    for attempt in range(max_retries + 1):
        try:
            response = requests.post(
                WEBSHOT_API,
                json={'url': url, 'format': 'png', 'mode': 'desktop_viewport'},
                timeout=120,
            )

            if response.status_code == 200:
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                size_kb = len(response.content) // 1024
                retry_tag = "（重试）" if attempt > 0 else ""
                print(f"  📸 网站截图{retry_tag}: {filename} ({size_kb}KB)")
                return str(output_file.relative_to("/Volumes/EXTEND/aI-product-daily-peport"))

            elif response.status_code == 429:
                wait = int(response.headers.get('Retry-After', 60))
                print(f"  ⏰ 速率限制（429），等待 {wait} 秒后重试...")
                time.sleep(wait)
                continue

            elif response.status_code == 530:
                if attempt < max_retries:
                    wait = 300  # 5 分钟
                    print(f"  ⚠️ 服务端临时故障（530），等待 {wait // 60} 分钟后重试（{attempt + 1}/{max_retries}）...")
                    time.sleep(wait)
                    continue
                else:
                    print(f"  ❌ 截图失败 HTTP 530（已重试 {max_retries} 次，放弃）")

            else:
                print(f"  ❌ 截图失败 HTTP {response.status_code}")
                break

        except requests.exceptions.Timeout:
            if attempt < max_retries:
                wait = 300
                print(f"  ⚠️ 请求超时，等待 {wait // 60} 分钟后重试（{attempt + 1}/{max_retries}）...")
                time.sleep(wait)
                continue
            else:
                print(f"  ❌ 截图超时（已重试 {max_retries} 次，放弃）")

        except Exception as e:
            print(f"  ❌ 截图错误: {e}")
            break

    return None


def fetch_app_store_screenshots(app_name):
    """
    从 iTunes Search API 获取 App Store 截图 URL 列表
    不下载图片，直接返回远程 URL 供页面引用
    返回: {'name': str, 'url': str, 'screenshots': [str], 'icon': str} or None
    """
    try:
        response = requests.get(
            'https://itunes.apple.com/search',
            params={'term': app_name, 'entity': 'software', 'limit': 5},
            timeout=10,
        )
        response.raise_for_status()
        results = response.json().get('results', [])
        if not results:
            print(f"  ⚠️ App Store 未找到: {app_name}")
            return None

        # 优先精确匹配
        for app in results:
            if app_name.lower() in app.get('trackName', '').lower():
                return _extract_app_info(app)

        # 模糊匹配第一个
        return _extract_app_info(results[0])

    except Exception as e:
        print(f"  ❌ App Store 查询失败: {e}")
    return None


def _extract_app_info(app):
    """从 iTunes API 结果中提取需要的信息"""
    screenshots = app.get('screenshotUrls', [])
    # 只保留 iPhone 截图（过滤 iPad）
    iphone_screenshots = [s for s in screenshots if '1242' in s or '1290' in s or '1170' in s or '2688' in s or '2778' in s]
    if not iphone_screenshots:
        # 如果没有明确的 iPhone 尺寸，取前 5 张
        iphone_screenshots = screenshots[:5]

    return {
        'name': app.get('trackName', ''),
        'url': app.get('trackViewUrl', ''),
        'screenshots': iphone_screenshots[:5],  # 远程 URL 列表
        'icon': app.get('artworkUrl512') or app.get('artworkUrl100') or '',
    }


def process_product_screenshots(product):
    """
    处理产品的截图需求
    - 网站/SaaS: webshot.site 截图保存到本地
    - APP（有官网）: 网站截图 + App Store 截图 URL
    - APP（无官网）: 只获取 App Store 截图 URL
    """
    product_id = product.get('id', 'unknown')
    product_type = product.get('type', 'website')
    url = product.get('url') or product.get('homepage', '')

    result = {
        'screenshotUrl': None,           # 本地网站截图路径
        'appStoreScreenshots': [],       # App Store 远程 URL 列表
        'appStoreName': None,
        'appStoreUrl': None,
    }

    # APP 类型：获取 App Store 截图 URL
    if product_type in ['ios_app', 'app']:
        app_info = fetch_app_store_screenshots(product.get('name', ''))
        if app_info:
            result['appStoreScreenshots'] = app_info['screenshots']
            result['appStoreName'] = app_info['name']
            result['appStoreUrl'] = app_info['url']
            print(f"  📱 App Store 截图: {len(app_info['screenshots'])} 张")

        # 有官网也截一张
        if url:
            result['screenshotUrl'] = take_website_screenshot(url, product_id)

    # 网站/SaaS 类型
    elif url:
        result['screenshotUrl'] = take_website_screenshot(url, product_id)

    return result


if __name__ == '__main__':
    import json
    # 测试 App Store 查询
    info = fetch_app_store_screenshots('Notion')
    if info:
        print(f"App: {info['name']}")
        print(f"截图数: {len(info['screenshots'])}")
        for s in info['screenshots']:
            print(f"  {s}")

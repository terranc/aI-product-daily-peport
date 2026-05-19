#!/usr/bin/env python3
"""
产品数据库管理
处理产品存储、去重、冷却期管理
"""

import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

DATA_FILE = Path("/Volumes/EXTEND/aI-product-daily-peport/data/products.json")

def load_products():
    """加载产品数据库"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"version": "1.0", "lastUpdated": "", "products": [], "tracking": {"dailyFeatured": [], "weeklyDeepDive": []}}

def save_products(data):
    """保存产品数据库"""
    data['lastUpdated'] = datetime.now().isoformat()
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_product_id(name, url):
    """生成产品唯一ID"""
    content = f"{name.lower().strip()}:{url.lower().strip()}"
    return hashlib.md5(content.encode()).hexdigest()[:12]

def is_product_exists(products, product_id):
    """检查产品是否已存在"""
    return any(p['id'] == product_id for p in products)

def get_product_by_id(products, product_id):
    """根据ID获取产品"""
    for p in products:
        if p['id'] == product_id:
            return p
    return None

def check_cooldown(product, cooldown_days=14):
    """检查产品是否在冷却期内"""
    if 'cooldownExpiresAt' not in product:
        return False

    expires = datetime.fromisoformat(product['cooldownExpiresAt'])
    return datetime.now() < expires

def add_or_update_product(product_data, source_channel, cooldown_days=14):
    """
    添加新产品或更新已有产品
    返回: ('new'|'updated'|'cooldown', product)
    """
    data = load_products()
    products = data['products']

    # 生成唯一ID
    product_id = generate_product_id(
        product_data.get('name', ''),
        product_data.get('url', '') or product_data.get('source_url', '')
    )

    existing = get_product_by_id(products, product_id)

    if existing:
        # 已有产品，检查冷却期
        if check_cooldown(existing, cooldown_days):
            # 更新最后发现时间但不加入报告
            existing['lastSeen'] = datetime.now().isoformat()
            existing['mentions'].append({
                'date': datetime.now().isoformat(),
                'channel': source_channel,
                'url': product_data.get('source_url', ''),
                'title': product_data.get('title', '')
            })
            save_products(data)
            return 'cooldown', existing

        # 冷却期已过，检查是否有更新
        existing['lastSeen'] = datetime.now().isoformat()
        existing['mentions'].append({
            'date': datetime.now().isoformat(),
            'channel': source_channel,
            'url': product_data.get('source_url', ''),
            'title': product_data.get('title', '')
        })

        # 刷新冷却期
        existing['cooldownExpiresAt'] = (datetime.now() + timedelta(days=cooldown_days)).isoformat()

        save_products(data)
        return 'updated', existing

    # 新产品
    new_product = {
        'id': product_id,
        'name': product_data.get('name', ''),
        'slug': product_data.get('name', '').lower().replace(' ', '-').replace('.', '-'),
        'description': product_data.get('description', ''),
        'url': product_data.get('url', ''),
        'homepage': product_data.get('homepage', ''),
        'type': detect_product_type(product_data),
        'appStoreName': None,
        'appStoreUrl': None,
        'platforms': [],
        'categories': [],
        'tags': [],
        'firstSeen': datetime.now().isoformat(),
        'lastSeen': datetime.now().isoformat(),
        'cooldownExpiresAt': (datetime.now() + timedelta(days=cooldown_days)).isoformat(),
        'versions': [],
        'sourceChannels': [source_channel],
        'mentions': [{
            'date': datetime.now().isoformat(),
            'channel': source_channel,
            'url': product_data.get('source_url', ''),
            'title': product_data.get('title', '')
        }],
        'analysis': {
            'targetAudience': '',
            'useCases': [],
            'designIntent': '',
            'problemSolved': '',
            'score': 0,
            'scoreReason': '',
            'competitors': []
        },
        'metrics': {
            'weeklyViews': 0,
            'growthRate': 0,
            'featuredInDaily': False,
            'featuredInWeekly': False
        },
        'screenshotUrl': None,
        'appStoreScreenshots': [],
        'rawData': product_data
    }

    products.append(new_product)
    save_products(data)
    return 'new', new_product

def detect_product_type(product_data):
    """检测产品类型"""
    url = product_data.get('url', '')
    if not url:
        return 'unknown'

    if 'github.com' in url:
        return 'github'
    if 'apps.apple.com' in url or 'itunes.apple.com' in url:
        return 'ios_app'
    if 'play.google.com' in url:
        return 'android_app'

    return 'website'

def get_products_for_daily(cooldown_days=14):
    """获取适合每日推荐的新产品（冷却期内）"""
    data = load_products()
    products = data['products']

    # 筛选最近发现且未推荐过的产品
    candidates = []
    for p in products:
        if not p['metrics'].get('featuredInDaily', False):
            # 确认在冷却期内（即最近发现的）
            if check_cooldown(p, cooldown_days):
                candidates.append(p)

    return candidates

def mark_product_featured(product_id, feature_type='daily'):
    """标记产品已被推荐"""
    data = load_products()
    products = data['products']

    for p in products:
        if p['id'] == product_id:
            if feature_type == 'daily':
                p['metrics']['featuredInDaily'] = True
            elif feature_type == 'weekly':
                p['metrics']['featuredInWeekly'] = True
            break

    save_products(data)

def update_product_analysis(product_id, analysis_data):
    """更新产品分析数据"""
    data = load_products()
    products = data['products']

    for p in products:
        if p['id'] == product_id:
            p['analysis'].update(analysis_data)
            break

    save_products(data)

def update_product_screenshots(product_id, screenshot_path, app_screenshots=None):
    """更新产品截图"""
    data = load_products()
    products = data['products']

    for p in products:
        if p['id'] == product_id:
            if screenshot_path:
                p['screenshotUrl'] = screenshot_path
            if app_screenshots:
                p['appStoreScreenshots'] = app_screenshots
            break

    save_products(data)

if __name__ == '__main__':
    # 测试
    data = load_products()
    print(f"Database has {len(data['products'])} products")

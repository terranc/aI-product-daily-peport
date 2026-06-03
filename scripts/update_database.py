#!/usr/bin/env python3
"""
更新产品数据库：添加今日精选产品
"""
import json
from datetime import datetime, timedelta
from pathlib import Path

# 路径配置
BASE_DIR = Path("/Volumes/EXTEND/aI-product-daily-peport")
PRODUCTS_DB_PATH = BASE_DIR / "data" / "products.json"
REPORT_PATH = BASE_DIR / "reports/daily/2026-06-03.json"

def load_json(path):
    """加载 JSON 文件"""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    """保存 JSON 文件"""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def create_product_record(product_data, screenshot_path):
    """创建产品记录"""
    now = datetime.utcnow()
    cooldown_expires = now + timedelta(days=14)
    
    return {
        "id": product_data["id"],
        "name": product_data["name"],
        "slug": product_data["slug"],
        "description": product_data["description"],
        "url": product_data["url"],
        "homepage": product_data.get("homepage", ""),
        "type": product_data.get("type", "website"),
        "appStoreName": product_data.get("appStoreName"),
        "appStoreUrl": product_data.get("appStoreUrl"),
        "platforms": [],
        "categories": [],
        "tags": product_data.get("tags", []),
        "firstSeen": now.isoformat(),
        "lastSeen": now.isoformat(),
        "cooldownExpiresAt": cooldown_expires.isoformat(),
        "versions": [],
        "sourceChannels": product_data.get("sourceChannels", []),
        "mentions": [
            {
                "date": now.isoformat(),
                "channel": product_data.get("sourceChannels", ["unknown"])[0],
                "url": product_data.get("sourceUrl", ""),
                "title": product_data["name"]
            }
        ],
        "analysis": product_data.get("analysis", {}),
        "metrics": {
            "weeklyViews": 0,
            "growthRate": 0,
            "featuredInDaily": True,
            "featuredInWeekly": False
        },
        "screenshotUrl": screenshot_path,
        "appStoreScreenshots": product_data.get("appStoreScreenshots", []),
        "rawData": {}
    }

def main():
    """主函数"""
    print("📦 更新产品数据库...")
    
    # 加载数据
    products_db = load_json(PRODUCTS_DB_PATH)
    report = load_json(REPORT_PATH)
    
    existing_products = products_db.get("products", [])
    new_products = report.get("products", [])
    
    print(f"📊 当前数据库产品数: {len(existing_products)}")
    print(f"📊 今日新增产品数: {len(new_products)}")
    
    # 检查是否已存在
    existing_ids = {p.get("id") for p in existing_products if p.get("id")}
    added_count = 0
    
    for product in new_products:
        if product["id"] in existing_ids:
            print(f"  ⏭️  跳过已存在: {product['name']} (ID: {product['id']})")
            continue
        
        # 创建产品记录
        product_record = create_product_record(product, product.get("screenshotUrl"))
        existing_products.append(product_record)
        added_count += 1
        print(f"  ✅ 添加: {product['name']} (ID: {product['id']})")
    
    # 更新数据库
    products_db["products"] = existing_products
    products_db["lastUpdated"] = datetime.utcnow().isoformat()
    
    # 保存
    save_json(PRODUCTS_DB_PATH, products_db)
    
    print(f"\n📊 更新完成:")
    print(f"  新增: {added_count} 个产品")
    print(f"  总计: {len(existing_products)} 个产品")
    print(f"  冷却期: 14 天")
    print(f"  数据库: {PRODUCTS_DB_PATH}")

if __name__ == "__main__":
    main()
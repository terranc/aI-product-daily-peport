#!/usr/bin/env python3
"""
每日抓取主脚本
整合所有渠道，生成每日简报
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# 添加脚本路径
sys.path.insert(0, str(Path(__file__).parent))

from fetch_hackernews import fetch_hackernews_products
from fetch_github import fetch_github_trending
from fetch_twitter import fetch_twitter_products
from fetch_reddit import fetch_reddit_products
from product_db import add_or_update_product, get_products_for_daily, mark_product_featured, load_products
from analyze_product import analyze_product, is_application_product
from screenshot import process_product_screenshots

REPORTS_DIR = Path("/Volumes/EXTEND/aI-product-daily-peport/reports/daily")

def fetch_all_sources():
    """从所有渠道抓取产品"""
    all_products = []

    print("📡 开始抓取各渠道数据...")

    # Hacker News
    try:
        print("  🟠 Hacker News...")
        hn_products = fetch_hackernews_products()
        print(f"     找到 {len(hn_products)} 个候选产品")
        all_products.extend([('hackernews', p) for p in hn_products])
    except Exception as e:
        print(f"     错误: {e}")

    # GitHub
    try:
        print("  🐙 GitHub...")
        gh_products = fetch_github_trending()
        print(f"     找到 {len(gh_products)} 个候选项目")
        all_products.extend([('github', p) for p in gh_products])
    except Exception as e:
        print(f"     错误: {e}")

    # Twitter/X
    try:
        print("  🐦 Twitter...")
        tw_products = fetch_twitter_products()
        print(f"     找到 {len(tw_products)} 个候选产品")
        all_products.extend([('twitter', p) for p in tw_products])
    except Exception as e:
        print(f"     错误: {e}")

    # Reddit
    try:
        print("  🟠 Reddit...")
        rd_products = fetch_reddit_products()
        print(f"     找到 {len(rd_products)} 个候选产品")
        all_products.extend([('reddit', p) for p in rd_products])
    except Exception as e:
        print(f"     错误: {e}")

    # 按热度排序
    all_products.sort(key=lambda x: x[1].get('score', 0) + x[1].get('stars', 0), reverse=True)

    print(f"\n✅ 共抓取 {len(all_products)} 个候选产品")
    return all_products

def process_products(products_list):
    """处理产品：过滤技术产品 → 入库、去重"""
    new_products = []
    updated_products = []
    filtered_count = 0

    print("\n🔄 处理产品入库...")

    for source, product_data in products_list:
        try:
            # 过滤技术性产品，只保留应用侧产品
            is_app, reason = is_application_product(product_data)
            if not is_app:
                filtered_count += 1
                print(f"  🚫 过滤: {product_data.get('name', 'unknown')[:40]} — {reason}")
                continue

            status, product = add_or_update_product(product_data, source)

            if status == 'new':
                print(f"  ✨ 新产品: {product['name']}")
                new_products.append(product)
            elif status == 'updated':
                print(f"  📝 更新: {product['name']}")
                updated_products.append(product)
            else:
                print(f"  ⏸️  冷却期: {product['name']}")

        except Exception as e:
            print(f"  ❌ 处理 {product_data.get('name', 'unknown')} 失败: {e}")

    print(f"\n📊 过滤统计: {filtered_count} 个技术性产品被排除")
    return new_products, updated_products

def select_top_products(max_count=3):
    """从候选产品中选择最值得推荐的"""
    candidates = get_products_for_daily()

    if not candidates:
        print("⚠️ 没有新的候选产品")
        return []

    print(f"\n📊 从 {len(candidates)} 个候选产品中筛选...")

    # 这里可以加入更多智能筛选逻辑
    # 目前基于来源权重和已有数据
    scored_candidates = []
    for p in candidates:
        score = 0

        # 来源权重
        if 'hackernews' in p['sourceChannels']:
            raw = p.get('rawData', {})
            score += raw.get('score', 0) / 10

        if 'github' in p['sourceChannels']:
            raw = p.get('rawData', {})
            score += raw.get('stars', 0) / 50

        scored_candidates.append((score, p))

    # 按分数排序
    scored_candidates.sort(key=lambda x: x[0], reverse=True)

    selected = []
    for score, product in scored_candidates[:max_count]:
        # 进行分析
        print(f"\n🔍 分析产品: {product['name']}")
        analysis = analyze_product(product['rawData'])

        # 更新产品分析数据
        from product_db import update_product_analysis
        update_product_analysis(product['id'], analysis)
        product['analysis'] = analysis

        # 处理截图
        print(f"  📸 获取截图...")
        screenshot_data = process_product_screenshots(product)
        if screenshot_data.get('screenshotUrl') or screenshot_data.get('appStoreScreenshots'):
            from product_db import update_product_screenshots
            update_product_screenshots(
                product['id'],
                screenshot_data.get('screenshotUrl'),
                screenshot_data.get('appStoreScreenshots')
            )
            product.update(screenshot_data)

        selected.append(product)

    return selected

def generate_daily_report(products, date_str=None):
    """生成每日报告"""
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    report_data = {
        'date': date_str,
        'generatedAt': datetime.now().isoformat(),
        'productCount': len(products),
        'products': []
    }

    for product in products:
        # 标记为已推荐
        mark_product_featured(product['id'], 'daily')

        # 构建报告条目
        report_product = {
            'id': product['id'],
            'name': product['name'],
            'slug': product['slug'],
            'description': product['description'],
            'url': product['url'],
            'homepage': product.get('homepage', ''),
            'type': product['type'],
            'appStoreName': product.get('appStoreName'),
            'appStoreUrl': product.get('appStoreUrl'),
            'screenshotUrl': product.get('screenshotUrl'),
            'appStoreScreenshots': product.get('appStoreScreenshots', []),
            'tags': product.get('tags', []),
            'analysis': product.get('analysis', {}),
            'sourceChannels': product['sourceChannels'],
            'firstSeen': product['firstSeen']
        }

        report_data['products'].append(report_product)

    # 保存 JSON
    json_file = REPORTS_DIR / f"{date_str}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    print(f"\n💾 报告已保存: {json_file}")

    return report_data

def main():
    """主流程"""
    print("=" * 60)
    print("🤖 AI Product Radar - 每日抓取")
    print("=" * 60)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 1. 抓取所有渠道
    raw_products = fetch_all_sources()

    if not raw_products:
        print("❌ 没有抓取到任何产品")
        return

    # 2. 处理入库
    new, updated = process_products(raw_products)

    print(f"\n📈 统计: {len(new)} 新产品, {len(updated)} 个更新")

    # 3. 选择TOP产品
    top_products = select_top_products(max_count=3)

    if not top_products:
        print("\n⚠️ 没有适合推荐的产品")
        return

    # 4. 生成报告
    report = generate_daily_report(top_products)

    print("\n" + "=" * 60)
    print(f"✅ 完成！今日精选 {len(top_products)} 个产品:")
    for p in top_products:
        print(f"   • {p['name']} (评分: {p.get('analysis', {}).get('score', 'N/A')})")
    print("=" * 60)

    return report

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
每周深度分析脚本
从已推荐产品中，挑选"上线/更新10天后仍持续增长"的产品做深度分析
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from product_db import load_products, save_products, update_product_analysis

DATA_DIR = Path("/Volumes/EXTEND/aI-product-daily-peport/data")
REPORTS_DIR = Path("/Volumes/EXTEND/aI-product-daily-peport/reports/weekly")

def find_growth_candidates():
    """
    寻找适合深度分析的候选产品
    条件：
    1. 已在日报中推荐过
    2. 首次发现至少 10 天前
    3. 最近仍有提及（持续活跃）
    4. 未做过深度报告
    """
    data = load_products()
    products = data['products']

    now = datetime.now()
    candidates = []

    for p in products:
        # 条件1: 已在日报推荐
        if not p.get('metrics', {}).get('featuredInDaily', False):
            continue

        # 条件2: 已在周报中推荐过的跳过
        if p.get('metrics', {}).get('featuredInWeekly', False):
            continue

        # 条件3: 首次发现至少 10 天前
        first_seen = datetime.fromisoformat(p['firstSeen'])
        days_since_first = (now - first_seen).days
        if days_since_first < 10:
            continue

        # 条件4: 最近 7 天内仍有提及
        recent_mentions = [
            m for m in p.get('mentions', [])
            if (now - datetime.fromisoformat(m['date'])).days <= 7
        ]

        if not recent_mentions:
            continue

        # 计算增长分数
        growth_score = len(recent_mentions) * 10
        growth_score += len(p.get('sourceChannels', [])) * 5
        growth_score += p.get('analysis', {}).get('score', 0)

        candidates.append({
            'product': p,
            'growth_score': growth_score,
            'days_since_first': days_since_first,
            'recent_mention_count': len(recent_mentions)
        })

    # 按增长分数排序
    candidates.sort(key=lambda x: x['growth_score'], reverse=True)

    return candidates

def generate_weekly_deep_dive(candidate):
    """为候选产品生成深度分析报告"""
    product = candidate['product']
    analysis = product.get('analysis', {})

    report = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'generatedAt': datetime.now().isoformat(),
        'type': 'weekly_deep_dive',
        'product': {
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
            'firstSeen': product['firstSeen'],
            'sourceChannels': product['sourceChannels'],
        },
        'growthMetrics': {
            'daysSinceLaunch': candidate['days_since_first'],
            'recentMentions': candidate['recent_mention_count'],
            'mentionTimeline': product.get('mentions', []),
            'growthScore': candidate['growth_score'],
            'channels': list(set(m['channel'] for m in product.get('mentions', [])))
        },
        'analysis': analysis,
        'deepDive': {
            'whyItMatters': analysis.get('scoreReason', '待分析'),
            'marketPosition': f"在{', '.join(analysis.get('useCases', ['效率工具'])[:2])}领域，"
                              f"面向{analysis.get('targetAudience', '普通用户')}提供差异化的 AI 能力",
            'growthDrivers': generate_growth_drivers(product, candidate),
            'risksAndChallenges': generate_risks(product),
            'outlook': generate_outlook(product, analysis)
        }
    }

    return report

def generate_growth_drivers(product, candidate):
    """分析增长驱动力"""
    drivers = []

    mentions = product.get('mentions', [])
    channels = list(set(m['channel'] for m in mentions))

    if len(channels) >= 2:
        drivers.append(f"跨平台传播力强，在 {len(channels)} 个渠道被发现")

    if candidate['recent_mention_count'] >= 3:
        drivers.append("近期持续获得关注，话题热度不减")

    score = product.get('analysis', {}).get('score', 0)
    if score >= 8:
        drivers.append(f"综合评分 {score}/10，产品完成度高")

    tags = product.get('tags', [])
    if any(t in ['编程', '办公', '写作'] for t in tags):
        drivers.append("切入刚需场景，用户粘性潜力大")

    if not drivers:
        drivers.append("持续获得自然传播，具备基础增长动能")

    return drivers

def generate_risks(product):
    """分析风险"""
    risks = []

    tags = product.get('tags', [])
    if 'ChatGPT' in tags or 'Claude' in tags:
        risks.append("依赖特定模型提供商，存在 API 变动风险")

    if '开源项目' in tags:
        risks.append("开源项目商业化路径不确定")

    if product.get('type') == 'github':
        risks.append("项目成熟度待观察，需要持续维护")

    risks.append("AI 应用赛道竞争激烈，需保持产品差异化")

    return risks

def generate_outlook(product, analysis):
    """生成展望"""
    score = analysis.get('score', 5)
    if score >= 8:
        return "产品形态成熟，市场验证充分，值得持续跟踪"
    elif score >= 6:
        return "具备一定竞争力，需观察后续迭代速度和用户增长"
    else:
        return "尚在早期阶段，建议观望产品演进方向"

def main():
    print("=" * 60)
    print("🤖 AI Product Radar - 每周深度分析")
    print("=" * 60)

    # 寻找候选产品
    print("\n🔍 寻找增长候选产品...")
    candidates = find_growth_candidates()

    if not candidates:
        print("⚠️ 本周没有符合深度分析条件的产品")
        print("   条件：已在日报推荐 ≥10天 + 最近7天仍有提及 + 未做过周报")
        return

    print(f"  找到 {len(candidates)} 个候选产品")

    # 选择最值得关注的
    top = candidates[0]
    product_name = top['product']['name']

    print(f"\n🏆 本周深度分析: {product_name}")
    print(f"   发现天数: {top['days_since_first']}天")
    print(f"   近期提及: {top['recent_mention_count']}次")
    print(f"   增长分数: {top['growth_score']}")

    # 生成深度报告
    report = generate_weekly_deep_dive(top)

    # 保存报告
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime('%Y-%m-%d')
    report_file = REPORTS_DIR / f"{date_str}.json"

    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # 标记产品已做深度分析
    data = load_products()
    for p in data['products']:
        if p['id'] == top['product']['id']:
            p['metrics']['featuredInWeekly'] = True
            break
    save_products(data)

    print(f"\n💾 深度报告已保存: {report_file}")
    print("=" * 60)

    return report

if __name__ == '__main__':
    main()

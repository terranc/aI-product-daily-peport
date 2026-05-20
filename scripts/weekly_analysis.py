#!/usr/bin/env python3
"""
每周深度分析脚本
从已进入每日简报、且首次入选至少 10 天后的产品中挑选持续活跃对象。
"""

import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from product_db import load_products

BASE_DIR = Path("/Volumes/EXTEND/aI-product-daily-peport")
REPORTS_DIR = BASE_DIR / "reports"
DAILY_REPORTS_DIR = REPORTS_DIR / "daily"
WEEKLY_REPORTS_DIR = REPORTS_DIR / "weekly"
MIN_DAYS_SINCE_DAILY = 10
RECENT_MENTION_DAYS = 7


def parse_datetime(value):
    """把仓库里的 ISO/date 字符串统一转成 UTC aware datetime。"""
    if not value:
        return None

    text = str(value).strip()
    try:
        if len(text) == 10:
            dt = datetime.fromisoformat(text)
        else:
            dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None

    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def load_reports(report_dir):
    reports = []
    if not report_dir.exists():
        return reports

    for json_file in sorted(report_dir.glob("*.json")):
        with open(json_file, "r", encoding="utf-8") as f:
            reports.append(json.load(f))
    return reports


def product_keys(product):
    keys = []
    for field in ("slug", "id", "url", "homepage", "name"):
        value = product.get(field)
        if value:
            keys.append((field, str(value).strip().lower()))
    return keys


def primary_product_key(product):
    keys = product_keys(product)
    return keys[0] if keys else None


def build_daily_index(daily_reports):
    """按产品建立首次日报入选记录。"""
    index = {}

    for report in sorted(daily_reports, key=lambda r: r.get("date", "")):
        report_date = report.get("date", "")
        for product in report.get("products", []):
            key = primary_product_key(product)
            if not key or key in index:
                continue

            slug = product.get("slug", "")
            index[key] = {
                "product": deepcopy(product),
                "date": report_date,
                "dateTime": parse_datetime(report_date),
                "detailHref": f"products/{slug.lower()}.html" if slug else "",
            }

    return index


def weekly_product_keys(weekly_reports):
    keys = set()

    for report in weekly_reports:
        products = report.get("products", [])
        if not products and report.get("product"):
            products = [report["product"]]

        for product in products:
            keys.update(product_keys(product))

    return keys


def matching_db_products(daily_product, db_products):
    daily_keys = set(product_keys(daily_product))
    matches = []

    for product in db_products:
        if daily_keys.intersection(product_keys(product)):
            matches.append(product)

    return matches


def recent_mentions_for(products, now):
    mentions = []

    for product in products:
        for mention in product.get("mentions", []):
            mention_date = parse_datetime(mention.get("date"))
            if not mention_date:
                continue
            if 0 <= (now - mention_date).days <= RECENT_MENTION_DAYS:
                mentions.append(mention)

    return mentions


def merge_product_data(daily_product, db_products):
    merged = deepcopy(daily_product)

    for product in db_products:
        for field in ("analysis", "sourceChannels", "screenshotUrl", "appStoreScreenshots", "type"):
            if not merged.get(field) and product.get(field):
                merged[field] = deepcopy(product[field])

    source_channels = set(merged.get("sourceChannels", []))
    for product in db_products:
        source_channels.update(product.get("sourceChannels", []))
    merged["sourceChannels"] = sorted(source_channels)

    return merged


def find_growth_candidates(now=None):
    """
    寻找适合深度分析的候选产品。
    条件：
    1. 已在每日简报中出现；
    2. 距离首次日报入选至少 10 天；
    3. 最近 7 天内在产品库 mentions 中仍有提及；
    4. 未出现在已有周报中。
    """
    now = now or datetime.now(timezone.utc)
    daily_index = build_daily_index(load_reports(DAILY_REPORTS_DIR))
    weekly_keys = weekly_product_keys(load_reports(WEEKLY_REPORTS_DIR))
    db_products = load_products().get("products", [])
    candidates = []

    for key, daily_entry in daily_index.items():
        if key in weekly_keys:
            continue

        first_daily_at = daily_entry["dateTime"]
        if not first_daily_at:
            continue

        days_since_daily = (now - first_daily_at).days
        if days_since_daily < MIN_DAYS_SINCE_DAILY:
            continue

        db_matches = matching_db_products(daily_entry["product"], db_products)
        recent_mentions = recent_mentions_for(db_matches, now)
        if not recent_mentions:
            continue

        product = merge_product_data(daily_entry["product"], db_matches)
        analysis = product.get("analysis", {})
        growth_score = len(recent_mentions) * 10
        growth_score += len(product.get("sourceChannels", [])) * 5
        growth_score += analysis.get("score", 0)

        candidates.append({
            "product": product,
            "source_daily": daily_entry,
            "growth_score": growth_score,
            "days_since_daily": days_since_daily,
            "recent_mentions": recent_mentions,
        })

    candidates.sort(key=lambda x: x["growth_score"], reverse=True)
    return candidates


def generate_weekly_deep_dive(candidate, date_str=None):
    """为候选产品生成标准周报结构。"""
    product = candidate["product"]
    analysis = product.get("analysis", {})
    source_daily = candidate["source_daily"]
    date_str = date_str or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    recent_mentions = candidate["recent_mentions"]

    channels = sorted({
        mention.get("channel", "")
        for mention in recent_mentions
        if mention.get("channel")
    })
    use_cases = analysis.get("useCases", [])
    target = analysis.get("targetAudience", "目标用户")

    report_product = {
        "id": product.get("id", ""),
        "name": product.get("name", ""),
        "slug": product.get("slug", ""),
        "description": product.get("description", ""),
        "url": product.get("url", ""),
        "homepage": product.get("homepage", ""),
        "type": product.get("type", ""),
        "appStoreName": product.get("appStoreName"),
        "appStoreUrl": product.get("appStoreUrl"),
        "screenshotUrl": product.get("screenshotUrl"),
        "appStoreScreenshots": product.get("appStoreScreenshots", []),
        "tags": product.get("tags", []),
        "sourceChannels": product.get("sourceChannels", []),
        "sourceUrl": product.get("sourceUrl", ""),
        "firstSeen": product.get("firstSeen", ""),
        "analysis": analysis,
        "sourceDailyReport": {
            "date": source_daily["date"],
            "productSlug": product.get("slug", ""),
            "detailHref": source_daily["detailHref"],
        },
        "growthMetrics": {
            "daysSinceDailyFeature": candidate["days_since_daily"],
            "recentMentions": len(recent_mentions),
            "mentionTimeline": recent_mentions,
            "growthScore": candidate["growth_score"],
            "channels": channels,
        },
        "weeklyDeepDive": {
            "growthEvidence": (
                f"首次进入每日简报已 {candidate['days_since_daily']} 天，"
                f"最近 {RECENT_MENTION_DAYS} 天仍有 {len(recent_mentions)} 次可追踪提及。"
            ),
            "communityFeedback": (
                f"近期提及主要来自 {', '.join(channels)}。"
                if channels else "近期有持续提及，但来源渠道信息不足。"
            ),
            "recentUpdates": "基于产品库近期 mentions 继续跟踪，尚未接入独立版本更新源。",
            "marketPosition": (
                f"在{', '.join(use_cases[:2])}场景中，面向{target}提供差异化能力。"
                if use_cases else f"面向{target}，仍需要继续观察具体市场定位。"
            ),
            "differentiation": analysis.get("scoreReason", "差异化信息待补充。"),
            "risksAndChallenges": generate_risks(product),
            "outlook": generate_outlook(product, analysis),
        },
    }

    return {
        "date": date_str,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "productCount": 1,
        "products": [report_product],
    }


def generate_risks(product):
    """分析风险。"""
    risks = []
    tags = product.get("tags", [])

    if "ChatGPT" in tags or "Claude" in tags:
        risks.append("依赖特定模型提供商，存在 API 变动风险")
    if "开源项目" in tags:
        risks.append("开源项目商业化路径不确定")
    if product.get("type") == "github":
        risks.append("项目成熟度待观察，需要持续维护")

    risks.append("AI 应用赛道竞争激烈，需保持产品差异化")
    return risks


def generate_outlook(product, analysis):
    """生成展望。"""
    score = analysis.get("score", 5)
    if score >= 8:
        return "产品形态成熟，市场验证充分，值得持续跟踪"
    if score >= 6:
        return "具备一定竞争力，需观察后续迭代速度和用户增长"
    return "尚在早期阶段，建议观望产品演进方向"


def main():
    print("=" * 60)
    print("🤖 AI Product Radar - 每周深度分析")
    print("=" * 60)

    print("\n🔍 寻找增长候选产品...")
    candidates = find_growth_candidates()

    if not candidates:
        print("⚠️ 本周没有符合深度分析条件的产品")
        print("   条件：进入每日简报 ≥10天 + 最近7天仍有提及 + 未做过周报")
        return None

    print(f"  找到 {len(candidates)} 个候选产品")

    top = candidates[0]
    product_name = top["product"]["name"]

    print(f"\n🏆 本周深度分析: {product_name}")
    print(f"   距日报入选: {top['days_since_daily']}天")
    print(f"   近期提及: {len(top['recent_mentions'])}次")
    print(f"   增长分数: {top['growth_score']}")

    report = generate_weekly_deep_dive(top)
    WEEKLY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_file = WEEKLY_REPORTS_DIR / f"{report['date']}.json"

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n💾 深度报告已保存: {report_file}")
    print("=" * 60)
    return report


if __name__ == "__main__":
    main()

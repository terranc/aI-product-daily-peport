#!/usr/bin/env python3
"""
每周深度分析脚本
从已进入每日简报、且首次入选至少 10 天后的产品中挑选持续活跃对象。
采用 LLM 驱动的七维分析框架（回退到规则系统）。
"""

import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from product_db import load_products

# 导入 LLM 分析器
try:
    from llm_analyzer import get_analyzer
    HAS_LLM = True
except ImportError:
    HAS_LLM = False

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
        "weeklyDeepDive": generate_weekly_deep_dive_content(product, analysis, candidate, channels, recent_mentions),
    }

    return {
        "date": date_str,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "productCount": 1,
        "products": [report_product],
    }


def generate_weekly_deep_dive_content(product, analysis, candidate, channels, recent_mentions):
    """生成周报深度分析内容 - 优先使用 LLM，回退到规则系统"""
    # 尝试使用 LLM 进行深度分析
    if HAS_LLM:
        analyzer = get_analyzer()
        if analyzer.is_available():
            print(f"    🤖 使用 LLM 进行七维深度分析...")
            llm_result = analyzer.analyze_product_deep(product)
            if llm_result:
                # LLM 分析成功，补充增长证据等字段
                llm_result["growthEvidence"] = (
                    f"首次进入每日简报已 {candidate['days_since_daily']} 天，"
                    f"最近 {RECENT_MENTION_DAYS} 天仍有 {len(recent_mentions)} 次可追踪提及。"
                )
                llm_result["communityFeedback"] = (
                    f"近期提及主要来自 {', '.join(channels)}。"
                    if channels else "近期有持续提及，但来源渠道信息不足。"
                )
                llm_result["risksAndChallenges"] = generate_risks(product)
                llm_result["outlook"] = generate_outlook(product, analysis)
                print(f"    ✅ LLM 分析完成")
                return llm_result
            print(f"    ⚠️  LLM 分析失败，回退到规则系统")
    
    # 回退到规则系统
    print(f"    📊 使用规则系统进行七维分析...")
    return {
        # 七维深度分析框架（规则系统版本）
        "problemDefinition": generate_problem_definition(product, analysis),
        "aiIndispensability": generate_ai_indispensability(product, analysis),
        "workflowEmbedding": generate_workflow_embedding(product, analysis),
        "monetization": generate_monetization(product, analysis),
        "moatAnalysis": generate_moat_analysis(product, analysis),
        "competitivePositioning": generate_competitive_positioning(product, analysis),
        "fourQuestionsValidation": generate_four_questions(product, analysis),
        # 补充字段
        "growthEvidence": (
            f"首次进入每日简报已 {candidate['days_since_daily']} 天，"
            f"最近 {RECENT_MENTION_DAYS} 天仍有 {len(recent_mentions)} 次可追踪提及。"
        ),
        "communityFeedback": (
            f"近期提及主要来自 {', '.join(channels)}。"
            if channels else "近期有持续提及，但来源渠道信息不足。"
        ),
        "risksAndChallenges": generate_risks(product),
        "outlook": generate_outlook(product, analysis),
    }


def generate_problem_definition(product, analysis):
    """生成问题定义维度"""
    use_cases = analysis.get("useCases", [])
    target = analysis.get("targetAudience", "")
    description = product.get("description", "")

    # 痛点陈述
    pain_point = use_cases[0] if use_cases else description[:100] if description else "待补充"

    # 原有方案推断
    previous_solution = "人工处理" if "AI" in product.get("name", "") else "传统工具"

    # 痛感强度判断（基于评分和使用频率）
    score = analysis.get("score", 5)
    pain_intensity = "高频刚需" if score >= 7 else "低频痒点"

    return {
        "painPoint": pain_point,
        "previousSolution": previous_solution,
        "painIntensity": pain_intensity
    }


def generate_ai_indispensability(product, analysis):
    """生成AI不可替代性维度"""
    tags = product.get("tags", [])
    name = product.get("name", "")
    description = product.get("description", "")

    # 核心杠杆判断
    core_leverage = "效率"
    if "分析" in description or "洞察" in description:
        core_leverage = "体验"
    elif "成本" in description:
        core_leverage = "成本"
    elif "合规" in description:
        core_leverage = "合规"

    # AI角色判断
    ai_role = "核心能力"
    if "ChatGPT" in tags or "Claude" in tags:
        ai_role = "核心能力"
    elif "AI" in name:
        ai_role = "核心能力"

    # 反事实验证
    without_ai = "无法成立" if ai_role == "核心能力" else "仍可运作"

    return {
        "coreLeverage": core_leverage,
        "aiRole": ai_role,
        "withoutAI": without_ai
    }


def generate_workflow_embedding(product, analysis):
    """生成工作流嵌入维度"""
    use_cases = analysis.get("useCases", [])

    # 用户旅程（简化版）
    user_journey = "产品入口 → 核心功能 → 结果输出"
    if len(use_cases) > 0:
        user_journey = f"发现需求 → {use_cases[0]} → 获得结果"

    # 嵌入深度判断
    embedding_depth = "点状工具"
    if product.get("appStoreUrl") or product.get("homepage"):
        embedding_depth = "流程嵌入"

    # 迁移成本
    switching_cost = "低"
    tags = product.get("tags", [])
    if "企业" in tags or "团队" in tags:
        switching_cost = "中"

    return {
        "userJourney": user_journey,
        "embeddingDepth": embedding_depth,
        "switchingCost": switching_cost
    }


def generate_monetization(product, analysis):
    """生成商业化路径维度"""
    description = product.get("description", "")
    tags = product.get("tags", [])

    # 定价模式推断
    pricing_model = "订阅制"
    if "开源项目" in tags:
        pricing_model = "开源/增值服务"

    # ROI逻辑
    roi_logic = "提升效率节省时间成本"
    if "收入" in description or "转化" in description:
        roi_logic = "直接带来收入增长"

    # 付费意愿
    paying_willingness = "需培养"
    score = analysis.get("score", 5)
    if score >= 8:
        paying_willingness = "明确"

    return {
        "pricingModel": pricing_model,
        "roiLogic": roi_logic,
        "payingWillingness": paying_willingness
    }


def generate_moat_analysis(product, analysis):
    """生成护城河分析维度"""
    tags = product.get("tags", [])
    description = product.get("description", "")

    # 数据壁垒
    data_moat = "公开数据"
    if "私有" in description or "独家" in description:
        data_moat = "私有数据优势"

    # 工作流壁垒
    workflow_moat = "较弱"
    if product.get("appStoreUrl"):
        workflow_moat = "应用集成"

    # 网络效应
    network_effect = "无"
    if "社区" in tags or "协作" in tags:
        network_effect = "有"

    # 平台风险
    platform_risk = "高"
    if "开源项目" in tags:
        platform_risk = "中"
    if "垂直" in description or "细分" in description:
        platform_risk = "中"

    return {
        "dataMoat": data_moat,
        "workflowMoat": workflow_moat,
        "networkEffect": network_effect,
        "platformRisk": platform_risk
    }


def generate_competitive_positioning(product, analysis):
    """生成竞品位势对比维度"""
    competitors = analysis.get("competitors", [])
    use_cases = analysis.get("useCases", [])

    # 工作流对比
    workflow_comparison = "与现有工具对比待补充"
    if competitors and len(competitors) > 0:
        # 提取竞品名称
        comp = competitors[0]
        if isinstance(comp, dict):
            comp_name = comp.get("name", "竞品")
        else:
            comp_name = str(comp)
        workflow_comparison = f"相比{comp_name}，AI优先设计"

    # 关键差异点
    key_differentiator = analysis.get("scoreReason", "待分析")
    if len(key_differentiator) > 100:
        key_differentiator = key_differentiator[:100] + "..."

    # 生存利基
    survival_niche = "细分市场"
    target = analysis.get("targetAudience", "")
    if target:
        survival_niche = f"服务{target}"

    return {
        "workflowComparison": workflow_comparison,
        "keyDifferentiator": key_differentiator,
        "survivalNiche": survival_niche
    }


def generate_four_questions(product, analysis):
    """生成四问验证"""
    score = analysis.get("score", 5)
    use_cases = analysis.get("useCases", [])

    # 是高频刚需吗？
    high_frequency = score >= 6

    # AI是否不可替代？
    ai_indispensable = "AI" in product.get("name", "") or "AI" in product.get("description", "")

    # 是否深度嵌入工作流？
    workflow_embedded = product.get("appStoreUrl") is not None or len(use_cases) >= 2

    # 商业化路径是否清晰？
    monetization_clear = score >= 7

    return {
        "highFrequencyNeed": high_frequency,
        "aiIndispensable": ai_indispensable,
        "workflowEmbedded": workflow_embedded,
        "monetizationClear": monetization_clear
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

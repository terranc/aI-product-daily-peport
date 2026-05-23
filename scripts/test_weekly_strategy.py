#!/usr/bin/env python3
"""测试新的周报策略输出格式"""

import json
from datetime import datetime, timezone
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from product_db import load_products
from weekly_analysis import generate_problem_definition, generate_ai_indispensability, \
    generate_workflow_embedding, generate_monetization, generate_moat_analysis, \
    generate_competitive_positioning, generate_four_questions

BASE_DIR = Path("/Volumes/EXTEND/aI-product-daily-peport")

# 加载产品库
products_data = load_products()
products = products_data.get("products", [])

# 选择一个有完整分析的产品作为示例
sample_product = None
for p in products:
    if p.get("analysis") and p.get("analysis", {}).get("score", 0) >= 7:
        sample_product = p
        break

if not sample_product:
    # 如果没有高分的，选第一个有分析的
    for p in products:
        if p.get("analysis"):
            sample_product = p
            break

if not sample_product:
    print("没有找到有分析数据的产品")
    sys.exit(1)

print(f"测试产品: {sample_product.get('name', 'Unknown')}")
print(f"评分: {sample_product.get('analysis', {}).get('score', 0)}")
print("=" * 60)

analysis = sample_product.get("analysis", {})

# 生成七维分析
report = {
    "productName": sample_product.get("name", ""),
    "productSlug": sample_product.get("slug", ""),
    "analysisDate": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    "sevenDimensionAnalysis": {
        "problemDefinition": generate_problem_definition(sample_product, analysis),
        "aiIndispensability": generate_ai_indispensability(sample_product, analysis),
        "workflowEmbedding": generate_workflow_embedding(sample_product, analysis),
        "monetization": generate_monetization(sample_product, analysis),
        "moatAnalysis": generate_moat_analysis(sample_product, analysis),
        "competitivePositioning": generate_competitive_positioning(sample_product, analysis),
        "fourQuestionsValidation": generate_four_questions(sample_product, analysis),
    }
}

# 输出结果
print("\n七维深度分析结果：\n")
print(json.dumps(report, ensure_ascii=False, indent=2))

# 保存到文件
output_file = BASE_DIR / "reports" / "weekly" / f"test-{datetime.now().strftime('%Y%m%d')}.json"
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"\n✅ 测试报告已保存: {output_file}")

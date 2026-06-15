import json
import sys
import os
import time
from datetime import datetime, timezone

# Setup paths
BASE_DIR = '/Volumes/EXTEND/aI-product-daily-peport'
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports', 'daily')
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts')

sys.path.insert(0, SCRIPTS_DIR)
from screenshot import process_product_screenshots

# Load raw candidates to get full data for selected products
with open(os.path.join(DATA_DIR, 'raw-candidates.json'), 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# Selected Product IDs from raw candidates
selected_ids = [
    "producthunt.com/r/p/1170951", # Memoriq
    "producthunt.com/r/p/1171217", # Slashy
    "producthunt.com/r/p/1139531", # Allergo
    "producthunt.com/r/p/1169603", # LocIn AI
    "producthunt.com/r/p/1170971"  # Taste Lab
]

products_to_process = []
for p in raw_data.get('products', []):
    if p.get('product_id') in selected_ids:
        # Prepare product object for report and screenshot
        prod = {
            "id": p.get('product_id'),
            "name": p.get('name'),
            "slug": p.get('name', '').lower().replace(' ', '-'),
            "description": "", # To be filled
            "url": p.get('url'),
            "homepage": p.get('url'),
            "type": "website",
            "appStoreName": None,
            "appStoreUrl": None,
            "screenshotUrl": None,
            "appStoreScreenshots": [],
            "tags": [],
            "sourceChannels": [p.get('source')],
            "sourceUrl": p.get('source_url'),
            "firstSeen": datetime.now(timezone.utc).isoformat(),
            "analysis": {
                "targetAudience": "",
                "useCases": [],
                "designIntent": "",
                "problemSolved": "",
                "tags": [],
                "score": 0,
                "scoreReason": "",
                "competitors": []
            }
        }
        products_to_process.append(prod)

# Hardcoded analysis results from previous LLM reasoning
analysis_data = {
    "producthunt.com/r/p/1170951": {
        "name": "Memoriq",
        "description": "一款私密的 AI 记忆保险库，支持保存和管理来自 ChatGPT、Claude 等平台的对话历史。",
        "targetAudience": "使用 AI 助手进行深度工作或学习的用户。",
        "useCases": ["保存 AI 生成的长文本分析", "管理跨平台的 AI 对话历史", "构建个人 AI 知识库"],
        "designIntent": "解决 AI 对话无法持久化存储、难以跨平台同步和检索的痛点。",
        "problemSolved": "AI 的“遗忘”问题，用户无法方便地找回过去与 AI 共同产出的有价值内容。",
        "tags": ["AI 记忆", "知识管理", "隐私保护", "效率工具"],
        "score": 8.5,
        "scoreReason": "填补了 AI 对话管理的一个重要空白，端到端加密增加了信任感，且支持多主流平台。",
        "competitors": ["Mem", "Notion AI", "ChatGPT History"]
    },
    "producthunt.com/r/p/1171217": {
        "name": "Slashy",
        "description": "一个 AI 原生的邮件助手，能以你的语气起草回复、分类邮件并追踪待办。",
        "targetAudience": "需要处理大量邮件、追求高效沟通的职场人士。",
        "useCases": ["自动起草邮件回复", "邮件优先级分类与摘要", "追踪邮件中的待办事项"],
        "designIntent": "打造一个 AI 原生的邮件客户端，让 AI 深度参与邮件处理的全流程。",
        "problemSolved": "传统邮件客户端效率低下，AI 介入往往只是辅助，Slashy 提供了更一体化的体验。",
        "tags": ["AI 邮件", "办公自动化", "沟通协作", "效率提升"],
        "score": 8.0,
        "scoreReason": "邮件是职场核心场景，AI 原生的体验相比插件形式更有潜力改变用户习惯。",
        "competitors": ["Superhuman", "Spark Mail", "Gmail Copilot"]
    },
    "producthunt.com/r/p/1139531": {
        "name": "Allergo",
        "description": "利用 AI 生成多语言过敏原翻译卡片，帮助旅行者在海外安全饮食。",
        "targetAudience": "有食物过敏或饮食限制的旅行者。",
        "useCases": ["生成多语言过敏原翻译卡片", "在海外餐厅出示过敏信息", "紧急情况下的医疗提示"],
        "designIntent": "利用 AI 快速生成精准的过敏原翻译，解决跨语言环境下的健康安全隐患。",
        "problemSolved": "旅行中无法准确表达过敏原，导致饮食风险。",
        "tags": ["旅行工具", "健康安全", "AI 翻译", "生活服务"],
        "score": 7.5,
        "scoreReason": "场景极度垂直且刚需，支持 Apple Wallet 离线显示非常实用。",
        "competitors": ["Allergy Amulet", "Google Translate"]
    },
    "producthunt.com/r/p/1169603": {
        "name": "LocIn AI",
        "description": "AI 驱动的应用本地化工具，能够根据品牌语调自动翻译并优化应用内容。",
        "targetAudience": "需要进行 App 或网站国际化的开发者和产品经理。",
        "useCases": ["根据品牌语调自动翻译应用文案", "管理多语言翻译项目", "优化本地化内容"],
        "designIntent": "用 AI 理解语调（Tone-aware）来提升本地化的质量，而非死板的机器翻译。",
        "problemSolved": "传统翻译工具难以把握品牌语调，导致本地化内容生硬。",
        "tags": ["AI 本地化", "开发者工具", "翻译", "品牌语调"],
        "score": 7.0,
        "scoreReason": "解决了本地化中的一个高级痛点（语调一致性），对出海团队有吸引力。",
        "competitors": ["Lokalise", "Crowdin", "DeepL"]
    },
    "producthunt.com/r/p/1170971": {
        "name": "Taste Lab",
        "description": "通过 AI 提取任何网站的设计 DNA，包括配色、字体和布局风格。",
        "targetAudience": "UI/UX 设计师、前端开发、产品经理。",
        "useCases": ["分析竞争对手网站的设计风格", "提取配色方案和字体", "获取设计灵感"],
        "designIntent": "让 AI 自动“拆解”网站的设计 DNA，辅助设计决策。",
        "problemSolved": "手动分析网站设计元素耗时且容易遗漏。",
        "tags": ["UI 设计", "设计分析", "竞品研究", "AI 辅助设计"],
        "score": 6.5,
        "scoreReason": "对设计师有不错的辅助价值，但可能面临竞品分析工具的挑战。",
        "competitors": ["Dribbble", "Behance", "Landingfolio"]
    }
}

# Update products with analysis
for prod in products_to_process:
    if prod['id'] in analysis_data:
        data = analysis_data[prod['id']]
        prod['name'] = data['name']
        prod['description'] = data['description']
        prod['analysis']['targetAudience'] = data['targetAudience']
        prod['analysis']['useCases'] = data['useCases']
        prod['analysis']['designIntent'] = data['designIntent']
        prod['analysis']['problemSolved'] = data['problemSolved']
        prod['analysis']['tags'] = data['tags']
        prod['analysis']['score'] = data['score']
        prod['analysis']['scoreReason'] = data['scoreReason']
        prod['analysis']['competitors'] = data['competitors']
        prod['tags'] = data['tags']

# Take screenshots
print("Taking screenshots...")
for prod in products_to_process:
    print(f"Processing {prod['name']}...")
    result = process_product_screenshots(prod)
    prod['screenshotUrl'] = result.get('screenshotUrl')
    prod['appStoreScreenshots'] = result.get('appStoreScreenshots', [])
    prod['appStoreName'] = result.get('appStoreName')
    prod['appStoreUrl'] = result.get('appStoreUrl')
    time.sleep(3)

# Save daily report
today_str = datetime.now().strftime('%Y-%m-%d')
report = {
    "date": today_str,
    "generatedAt": datetime.now(timezone.utc).isoformat(),
    "productCount": len(products_to_process),
    "products": products_to_process
}

report_path = os.path.join(REPORTS_DIR, f"{today_str}.json")
os.makedirs(os.path.dirname(report_path), exist_ok=True)
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

# Update products.json
db_path = os.path.join(DATA_DIR, 'products.json')
with open(db_path, 'r', encoding='utf-8') as f:
    db = json.load(f)

for prod in products_to_process:
    prod['cooldownExpiresAt'] = (datetime.now(timezone.utc) + timedelta(days=14)).isoformat()
    prod['metrics'] = {
        "weeklyViews": 0,
        "growthRate": 0,
        "featuredInDaily": True,
        "featuredInWeekly": False
    }
    # Check if exists
    exists = False
    for i, existing in enumerate(db['products']):
        if existing['id'] == prod['id']:
            db['products'][i].update(prod)
            exists = True
            break
    if not exists:
        db['products'].append(prod)

with open(db_path, 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print(f"Report saved to {report_path}")
print(f"Database updated.")

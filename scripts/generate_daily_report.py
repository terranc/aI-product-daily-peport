#!/usr/bin/env python3
"""
AI 产品雷达 - 每日报告生成器
基于 LLM 分析结果，生成日报 JSON、更新数据库、截图
"""
import json
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE = Path("/Volumes/EXTEND/aI-product-daily-peport")
sys.path.insert(0, str(BASE / "scripts"))

from screenshot import process_product_screenshots

TODAY = datetime.now(timezone(timedelta(hours=8)))
DATE_STR = TODAY.strftime("%Y-%m-%d")
NOW_ISO = TODAY.isoformat()
COOLDOWN_EXPIRES = (TODAY + timedelta(days=14)).isoformat()

# ============================================================
# 第一步：LLM 分析筛选结果
# 从 174 个去重候选产品中，过滤技术性产品后，精选 TOP 5
# ============================================================

SELECTED_PRODUCTS = [
    {
        "id": "producthunt.com/r/p/1190590",
        "product_id": "producthunt.com/r/p/1190590",
        "name": "Lispr",
        "name_zh": "Lispr - 语音听写与翻译",
        "slug": "lispr",
        "description": "Lispr 是一款 macOS 菜单栏语音听写工具，内置实时翻译功能。按住 Option 键说话，AI 自动将语音转为文字并直接输入到当前光标位置；再按 Control 键可实时翻译成目标语言。支持 99 种语言的语音识别和 34 种语言的翻译，仅 4MB 大小，无需注册账户，语音数据加密传输后即删除。",
        "url": "https://lispr.ai/",
        "homepage": "https://lispr.ai/",
        "type": "saas",
        "appStoreName": None,
        "appStoreUrl": None,
        "screenshotUrl": None,
        "appStoreScreenshots": [],
        "tags": ["语音听写", "实时翻译", "Mac工具", "效率提升", "多语言"],
        "sourceChannels": ["producthunt"],
        "sourceUrl": "https://www.producthunt.com/r/p/1190590?app_id=339",
        "firstSeen": NOW_ISO,
        "analysis": {
            "targetAudience": "需要频繁进行跨语言沟通或语音输入的 macOS 用户，包括外贸从业者、多语言内容创作者、追求高效输入的职场人士",
            "useCases": [
                "跨国即时通讯时直接说出中文自动翻译成英文发送",
                "会议记录和灵感速记时通过语音快速录入文字",
                "在外文邮件、文档中边说边自动输出目标语言",
                "在 Slack、Figma、终端等任意应用中语音输入代码或文案",
                "构建自定义词汇库确保产品名、专业术语准确识别"
            ],
            "designIntent": "解决现有 macOS 自带听写功能需要手动切换语言、有超时限制、无实时翻译的问题。Lispr 希望让语音输入像快捷键一样自然——按住就说、松开就写完，消除跨语言沟通中的打字摩擦。",
            "problemSolved": "传统语音输入工具要么需要订阅付费，要么缺乏翻译功能且需要手动切换语言。Lispr 免费提供「语音输入 + 实时翻译」一站式体验，按住一个键即可在任何应用中完成多语言语音输入，大幅提升打字效率和跨语言沟通速度。",
            "tags": ["语音听写", "实时翻译", "Mac工具", "效率提升", "多语言"],
            "score": 8,
            "scoreReason": "产品设计极简优雅：4MB、无注册、按住即说，解决真实痛点。使用 Whisper large-v3 模型保证识别质量，免费模式降低使用门槛。但仅支持 macOS 且需要联网，是当前主要局限。",
            "competitors": [
                {"name": "Wispr Flow", "url": "https://wisprflow.ai", "comparison": "Wispr Flow 每月 15 美元订阅，Lispr 免费；Wispr 不支持翻译，Lispr 内置 34 语言翻译"},
                {"name": "Apple 自带听写", "url": "https://support.apple.com", "comparison": "Apple 听写免费但需手动切换语言、有超时限制、不支持翻译；Lispr 支持 99 种语言自动检测且可实时翻译"},
                {"name": "Google 语音输入", "url": "https://www.google.com", "comparison": "Google 语音输入仅限其生态应用，Lispr 可在任何 Mac 应用的光标处直接输入"}
            ]
        }
    },
    {
        "id": "producthunt.com/r/p/1189574",
        "product_id": "producthunt.com/r/p/1189574",
        "name": "JustVibe",
        "name_zh": "JustVibe - AI 搜索即应用",
        "slug": "justvibe",
        "description": "JustVibe 是一款 AI 搜索引擎，与传统搜索返回链接列表不同，它直接为你生成可交互的应用程序。搜索「规划我的 5 天东京旅行」→ 获得一个已设置好的行程规划器（含地图、预算、每日安排）。如果没有匹配的应用，JustVibe 会在几分钟内为你实时构建一个，且归你所有，可以编辑和分享。100% 免费，无需代码。",
        "url": "https://justvibe.com/",
        "homepage": "https://justvibe.com/",
        "type": "website",
        "appStoreName": None,
        "appStoreUrl": None,
        "screenshotUrl": None,
        "appStoreScreenshots": [],
        "tags": ["AI搜索", "应用生成", "无代码", "效率工具", "交互式"],
        "sourceChannels": ["producthunt"],
        "sourceUrl": "https://www.producthunt.com/r/p/1189574?app_id=339",
        "firstSeen": NOW_ISO,
        "analysis": {
            "targetAudience": "需要快速完成具体任务的普通互联网用户，从旅行规划到菜谱推荐、从预算管理到学习备考的广泛人群",
            "useCases": [
                "旅行规划时搜索目的地，获得即时可编辑的完整行程规划器",
                "根据冰箱剩余食材搜索，获得可交互的食谱推荐应用",
                "创建灵感看板、预算追踪器、学习闪卡等临时工具",
                "分享生成的 App 链接给朋友，对方无需登录即可使用",
                "通过聊天对已生成的应用进行实时修改和定制"
            ],
            "designIntent": "打破传统搜索引擎「返回链接、用户自己动手」的模式，让搜索结果直接是一个能用的工具。JustVibe 认为用户搜索的本质不是要看列表，而是要把事情做完，所以它直接生成完成任务的 App。",
            "problemSolved": "传统搜索返回 SEO 优化的列表文章，用户还得自己整理信息再动手实现；聊天机器人返回长篇文字，用户仍需转成可操作的工具。JustVibe 直接输出可交互的应用，省去「阅读→理解→动手」的中间步骤。",
            "tags": ["AI搜索", "应用生成", "无代码", "效率工具", "交互式"],
            "score": 9,
            "scoreReason": "理念极具创新性——从「搜到信息」到「得到工具」的范式跃迁。100% 免费、无需登录、响应快，覆盖场景广泛。但生成的应用功能深度有限，复杂需求可能无法满足。",
            "competitors": [
                {"name": "ChatGPT Search", "url": "https://chatgpt.com", "comparison": "ChatGPT Search 返回文字回答和链接，JustVibe 直接生成可交互的应用"},
                {"name": "Perplexity AI", "url": "https://perplexity.ai", "comparison": "Perplexity 侧重信息聚合和深度研究，JustVibe 侧重任务完成和工具生成"},
                {"name": "Zapier AI", "url": "https://zapier.com", "comparison": "Zapier 自动化工作流偏向企业级，配置复杂；JustVibe 面向个人消费级，零配置即用"}
            ]
        }
    },
    {
        "id": "producthunt.com/r/p/1189614",
        "product_id": "producthunt.com/r/p/1189614",
        "name": "ARKAD Wallet",
        "name_zh": "ARKAD Wallet - 语音预算管理",
        "slug": "arkad-wallet",
        "description": "ARKAD Wallet 是一款以语音为核心的预算管理应用。用自然语言说出「今天晚餐花了 120 元」，AI 自动解析并记录到对应预算分类。支持设置分类预算、追踪财务目标、查看净资产总览。数据存储在欧盟基础设施，符合 GDPR 标准，语音数据不上传训练 AI 模型。免费版可用，高级版 €2.49/月解锁无限语音输入。",
        "url": "https://arkadwallet.com/",
        "homepage": "https://arkadwallet.com/",
        "type": "website",
        "appStoreName": None,
        "appStoreUrl": None,
        "screenshotUrl": None,
        "appStoreScreenshots": [],
        "tags": ["预算管理", "语音输入", "个人理财", "隐私优先", "记账"],
        "sourceChannels": ["producthunt"],
        "sourceUrl": "https://www.producthunt.com/r/p/1189614?app_id=339",
        "firstSeen": NOW_ISO,
        "analysis": {
            "targetAudience": "觉得传统记账应用太复杂、想要更轻松理财的个人用户，特别是预算新手、自由职业者和注重隐私的欧盟用户",
            "useCases": [
                "消费后立即用语音记录「咖啡 35 元」，3 秒完成记账",
                "设置月度餐饮预算 2000 元，实时查看剩余额度",
                "追踪储蓄目标（如旅行基金），掌握进度",
                "查看净资产总览，了解资产负债全貌",
                "通过语音调整预算分配，无需进入复杂设置"
            ],
            "designIntent": "大多数人知道应该记账但坚持不下来，因为现有应用太复杂、录入太麻烦。ARKAD Wallet 希望把记账的门槛降到最低——说话就行。语音输入 + 简洁界面 + 隐私保护，让理财变成习惯而非负担。",
            "problemSolved": "传统记账应用需要手动逐条输入、分类繁琐，订阅费高昂。ARKAD Wallet 用语音将录入时间从 30 秒降到 3 秒，AI 自动分类，免费版即可满足基本需求，且数据托管在欧盟保障隐私。",
            "tags": ["预算管理", "语音输入", "个人理财", "隐私优先", "记账"],
            "score": 7,
            "scoreReason": "语音记账确实降低了记账门槛，解决真实痛点。隐私保护（GDPR、不上传语音训练）是差异化优势。但免费版每月仅 30 次语音输入，且不支持银行自动同步，功能深度有限。",
            "competitors": [
                {"name": "YNAB", "url": "https://www.ynab.com", "comparison": "YNAB 功能强大但学习曲线陡峭（14.99 美元/月），ARKAD 更轻量且支持语音输入"},
                {"name": "MoneyLion", "url": "https://www.moneylion.com", "comparison": "MoneyLion 侧重投资和信用，ARKAD 聚焦预算管理的简洁体验"},
                {"name": "随手记", "url": "https://www.sui-shou-ji.com", "comparison": "随手记功能全面但界面复杂，ARKAD 语音输入更便捷但功能较简单"}
            ]
        }
    },
    {
        "id": "martino.im/summarize",
        "product_id": "martino.im/summarize",
        "name": "Summarize",
        "name_zh": "Summarize - 视频转笔记工具",
        "slug": "summarize-video-notes",
        "description": "Summarize 是一款本地优先的视频知识萃取工具。粘贴任意视频链接（支持 YouTube、Bilibili 等），自动下载、语音转录、AI 总结，输出图文并茂的 Markdown 笔记。内置 Whisper 语音识别和 AI 大模型，所有数据在本地处理，不上传云端，保护隐私。适合将播客、课程、会议录屏快速转化为可检索的文字笔记。",
        "url": "https://martino.im/Summarize",
        "homepage": "https://martino.im/Summarize",
        "type": "website",
        "appStoreName": None,
        "appStoreUrl": None,
        "screenshotUrl": None,
        "appStoreScreenshots": [],
        "tags": ["视频转笔记", "AI摘要", "知识管理", "本地优先", "隐私保护"],
        "sourceChannels": ["hackernews"],
        "sourceUrl": "https://news.ycombinator.com/item?id=???",
        "firstSeen": NOW_ISO,
        "analysis": {
            "targetAudience": "需要从视频/播客中提取知识的重度学习者、研究人员、学生和知识工作者",
            "useCases": [
                "将 YouTube 教程视频转为结构化学习笔记",
                "把播客访谈转写成文字稿，方便检索和引用",
                "将会议录屏自动生成会议纪要和关键决策点",
                "B站课程视频一键转为图文笔记，导入 Obsidian 等知识库",
                "对视频中的关键帧自动截图，形成图文并茂的笔记文档"
            ],
            "designIntent": "视频内容越来越多，但回看和检索非常低效。Summarize 希望把「看视频」变成「读笔记」——用 AI 自动完成听写、总结和关键帧提取，让用户能在几分钟而非几小时内获取视频的核心知识。",
            "problemSolved": "手动做视频笔记耗时巨大，现有云端工具要么收费高要么需上传视频泄露隐私。Summarize 本地运行，免费且隐私安全，支持全网主流视频平台，一键输出结构化的 Markdown 笔记。",
            "tags": ["视频转笔记", "AI摘要", "知识管理", "本地优先", "隐私保护"],
            "score": 7,
            "scoreReason": "解决真实需求——视频学习者的笔记痛点。本地优先的设计保障隐私是重要差异化优势。但需要本地配置 AI 模型和依赖，对非技术用户有一定门槛。",
            "competitors": [
                {"name": "Otter.ai", "url": "https://otter.ai", "comparison": "Otter.ai 付费且云端处理，Summarize 免费且本地运行更隐私"},
                {"name": "Notta.ai", "url": "https://notta.ai", "comparison": "Notta 主打会议转录，Summarize 更偏向视频学习和内容萃取"},
                {"name": "Memo AI", "url": "https://memo.ai", "comparison": "Memo 已转型为 AI 笔记，Summarize 专注视频→笔记的单点功能"}
            ]
        }
    },
    {
        "id": "v2ex.com/t/1226861",
        "product_id": "v2ex.com/t/1226861",
        "name": "呼噜娃",
        "name_zh": "呼噜娃 - 睡眠鼾声监测",
        "slug": "snore-patrol",
        "description": "呼噜娃是一款专注睡眠录音与打鼾分析的 iOS 工具。睡前点击按钮一键开始监测，AI 自动识别鼾声和梦话，支持分贝阈值筛选快速定位「高能」时段。所有录音数据仅保存在手机本地，不上传云端。8 小时录制仅几十 MB，支持原始录音导出分享给医生参考。一次买断，无需订阅。",
        "url": "https://apps.apple.com/cn/app/id6758048088",
        "homepage": "https://apps.apple.com/cn/app/id6758048088",
        "type": "app",
        "appStoreName": "呼噜娃",
        "appStoreUrl": "https://apps.apple.com/cn/app/id6758048088",
        "screenshotUrl": None,
        "appStoreScreenshots": [],
        "tags": ["睡眠监测", "打鼾分析", "健康管理", "iOS应用", "隐私保护"],
        "sourceChannels": ["v2ex"],
        "sourceUrl": "https://www.v2ex.com/t/1226861",
        "firstSeen": NOW_ISO,
        "analysis": {
            "targetAudience": "想了解自己是否有打鼾问题的普通人，被伴侣抱怨打呼噜的用户，以及想验证止鼾方法（侧睡、呼吸贴等）效果的人群",
            "useCases": [
                "睡前一键开启监测，次日查看鼾声评分和录音回放",
                "通过分贝阈值筛选快速定位夜间打鼾高峰时段",
                "对比不同睡姿、止鼾产品的效果，用数据验证",
                "将异常鼾声录音导出给医生参考诊断",
                "了解自己是否说梦话以及梦话的频率和内容"
            ],
            "designIntent": "市面上的睡眠 App 功能太杂乱、订阅费昂贵，没有一个简单纯粹的鼾声监测工具。呼噜娃砍掉所有社交和冥想功能，只做一件事——记录和回溯夜晚的声音，让用户睡得清清楚楚。",
            "problemSolved": "想知道自己打不打鼾、鼾声有多大，但缺乏简单、便宜、隐私的工具。呼噜娃提供一键监测、本地存储、买断制，解决了大厂 App 收费高、功能杂、数据上云的顾虑。",
            "tags": ["睡眠监测", "打鼾分析", "健康管理", "iOS应用", "隐私保护"],
            "score": 7,
            "scoreReason": "产品定位极其专注——只做鼾声监测一件事，买断制（一杯奶茶价）比月费模式更友好。本地存储保障隐私是关键卖点。但功能相对单一，竞品 SnoreLab 更成熟。",
            "competitors": [
                {"name": "SnoreLab", "url": "https://www.snorelab.com", "comparison": "SnoreLab 是行业标杆但订阅制收费较高，呼噜娃买断更便宜且中文支持更好"},
                {"name": "鼾声分析器", "url": "https://apps.apple.com/app/id529443604", "comparison": "鼾声分析器功能全面但有订阅费，呼噜娃更简洁专注、一次买断"},
                {"name": "Apple 健康（睡眠）", "url": "https://www.apple.com/health", "comparison": "Apple 健康只追踪睡眠时长不记录鼾声，呼噜娃专注鼾声录音和分析"}
            ]
        }
    }
]

# ============================================================
# 第二步：截图
# ============================================================
print("=" * 60)
print("📸 开始截图处理...")
print("=" * 60)

for product in SELECTED_PRODUCTS:
    print(f"\n--- {product['name_zh']} ---")
    result = process_product_screenshots(product)
    product['screenshotUrl'] = result.get('screenshotUrl')
    product['appStoreScreenshots'] = result.get('appStoreScreenshots', [])
    product['appStoreName'] = result.get('appStoreName')
    product['appStoreUrl'] = result.get('appStoreUrl')
    time.sleep(3)

# ============================================================
# 第三步：写入今日报告
# ============================================================
print("\n" + "=" * 60)
print("📝 写入今日报告...")
print("=" * 60)

daily_report = {
    "date": DATE_STR,
    "generatedAt": NOW_ISO,
    "productCount": len(SELECTED_PRODUCTS),
    "products": []
}

for p in SELECTED_PRODUCTS:
    daily_report["products"].append({
        "id": p["product_id"],
        "name": p["name_zh"],
        "slug": p["slug"],
        "description": p["description"],
        "url": p["homepage"],
        "homepage": p["homepage"],
        "type": p["type"],
        "appStoreName": p["appStoreName"],
        "appStoreUrl": p["appStoreUrl"],
        "screenshotUrl": p["screenshotUrl"],
        "appStoreScreenshots": p["appStoreScreenshots"],
        "tags": p["tags"],
        "sourceChannels": p["sourceChannels"],
        "sourceUrl": p["sourceUrl"],
        "firstSeen": p["firstSeen"],
        "analysis": {
            "targetAudience": p["analysis"]["targetAudience"],
            "useCases": p["analysis"]["useCases"],
            "designIntent": p["analysis"]["designIntent"],
            "problemSolved": p["analysis"]["problemSolved"],
            "tags": p["analysis"]["tags"],
            "score": p["analysis"]["score"],
            "scoreReason": p["analysis"]["scoreReason"],
            "competitors": p["analysis"]["competitors"]
        }
    })

daily_path = BASE / f"reports/daily/{DATE_STR}.json"
daily_path.parent.mkdir(parents=True, exist_ok=True)
with open(daily_path, 'w', encoding='utf-8') as f:
    json.dump(daily_report, f, ensure_ascii=False, indent=2)
print(f"✅ 日报已保存: {daily_path}")

# ============================================================
# 第四步：更新产品数据库
# ============================================================
print("\n" + "=" * 60)
print("🗄️ 更新产品数据库...")
print("=" * 60)

with open(BASE / "data/products.json", 'r', encoding='utf-8') as f:
    db = json.load(f)
if isinstance(db, dict):
    products_list = db.get('products', [])
else:
    products_list = db

# 检查是否已有重复
existing_ids = {p.get('id') for p in products_list}
new_count = 0
for p in SELECTED_PRODUCTS:
    pid = p["product_id"]
    if pid in existing_ids:
        print(f"  ⏭️ 已存在: {p['name_zh']} ({pid})")
        continue
    products_list.append({
        "id": pid,
        "name": p["name_zh"],
        "slug": p["slug"],
        "description": p["description"],
        "url": p["homepage"],
        "homepage": p["homepage"],
        "type": p["type"],
        "appStoreName": p["appStoreName"],
        "appStoreUrl": p["appStoreUrl"],
        "screenshotUrl": p["screenshotUrl"],
        "appStoreScreenshots": p["appStoreScreenshots"],
        "tags": p["tags"],
        "sourceChannels": p["sourceChannels"],
        "sourceUrl": p["sourceUrl"],
        "firstSeen": p["firstSeen"],
        "analysis": {
            "targetAudience": p["analysis"]["targetAudience"],
            "useCases": p["analysis"]["useCases"],
            "designIntent": p["analysis"]["designIntent"],
            "problemSolved": p["analysis"]["problemSolved"],
            "tags": p["analysis"]["tags"],
            "score": p["analysis"]["score"],
            "scoreReason": p["analysis"]["scoreReason"],
            "competitors": p["analysis"]["competitors"]
        },
        "cooldownExpiresAt": COOLDOWN_EXPIRES,
        "addedAt": NOW_ISO
    })
    new_count += 1
    print(f"  ✅ 新增: {p['name_zh']} ({pid})")

if isinstance(db, dict):
    db['products'] = products_list
    db['lastUpdated'] = NOW_ISO
    db['version'] = db.get('version', 1) + 1

with open(BASE / "data/products.json", 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)
print(f"\n✅ 数据库更新完成: 新增 {new_count} 个，共 {len(products_list)} 个产品")

# ============================================================
# 输出摘要
# ============================================================
print("\n" + "=" * 60)
print("📊 处理摘要")
print("=" * 60)
print(f"日期: {DATE_STR}")
print(f"精选产品数: {len(SELECTED_PRODUCTS)}")
for p in SELECTED_PRODUCTS:
    print(f"  {p['name_zh']} (评分: {p['analysis']['score']}/10)")
    print(f"    截图: {'✅' if p['screenshotUrl'] else '❌'} | App Store: {'✅' if p.get('appStoreScreenshots') else '❌'}")
print(f"数据库总产品数: {len(products_list)}")
print(f"✅ 完成!")

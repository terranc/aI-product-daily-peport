#!/usr/bin/env python3
"""Generate daily report for AI Product Radar."""
import json
from datetime import datetime, timezone, timedelta

now = datetime.now(timezone.utc)
today = now.strftime("%Y-%m-%d")

selected_products = [
    {
        "id": "producthunt.com/r/p/1157517",
        "name": "NeuralAgent 2.5",
        "slug": "neuralagent-2-5",
        "description": "一款多模态桌面 AI 自动化助手，通过语音指令控制电脑完成各种任务。支持语音模式、屏幕识别、并行 Agent 和工作流编排，能真正代替用户操作鼠标键盘、浏览网页、填写表单。",
        "url": "https://www.getneuralagent.com/",
        "homepage": "https://www.getneuralagent.com/",
        "type": "app",
        "sourceChannels": ["producthunt"],
        "sourceUrl": "https://www.producthunt.com/r/p/1157517?app_id=339",
        "tags": ["AI助手", "桌面自动化", "语音控制", "效率工具"],
        "analysis": {
            "targetAudience": "需要在电脑上高效完成重复性操作的办公人员和知识工作者",
            "useCases": [
                "语音操控电脑完成日常办公任务（发邮件、填表单、整理文件）",
                "自动化浏览器操作（批量搜索、数据采集、表单填写）",
                "并行处理多个工作流（同时监控多个任务进度）",
                "通过观察学习模式让 AI 学习用户操作习惯",
                "无障碍辅助——帮助行动不便用户操控电脑"
            ],
            "designIntent": "让 AI 不再只是聊天窗口里的对话伙伴，而是真正能动手操作电脑的桌面助手。通过多模态感知（语音+视觉），实现人机交互从打字提问到说话即执行的跃迁。",
            "problemSolved": "解决了传统 AI 助手只能给建议不能动手的痛点。用户不再需要自己一步步执行 AI 给出的操作指南，而是直接让 AI 代劳，大幅缩短从知道怎么做到做完的时间差。",
            "score": 8,
            "scoreReason": "语音+视觉+操作三合一的桌面 Agent 方向极具前景，开源免费降低了体验门槛。但桌面自动化领域竞争激烈（Anthropic Computer Use、OpenAI Operator 等），需持续迭代才能保持优势。",
            "competitors": [
                {"name": "Anthropic Computer Use", "url": "https://docs.anthropic.com/en/docs/agents-and-tools/computer-use", "comparison": "Anthropic 官方的计算机操控能力，集成在 Claude 中，但需要 API 调用，面向开发者；NeuralAgent 是独立桌面应用，面向普通用户"},
                {"name": "OpenAI Operator", "url": "https://operator.openai.com/", "comparison": "OpenAI 的浏览器自动化 Agent，目前仅限 ChatGPT Pro 用户；NeuralAgent 支持本地多模型，更灵活"},
                {"name": "n8n + AI Agent", "url": "https://n8n.io/", "comparison": "开源工作流自动化平台，需要技术配置；NeuralAgent 开箱即用，零配置语音驱动"}
            ]
        }
    },
    {
        "id": "producthunt.com/r/p/1156976",
        "name": "Kim Personal Health Assistant",
        "slug": "kim-personal-health-assistant",
        "description": "Apple Health 的 AI 智能健康层，将你的健康数据转化为简洁对话和个性化实验。连接可穿戴设备和血液检测数据，帮助你理解什么方案真正适合自己的身体。",
        "url": "https://apps.apple.com/us/app/kim-ai-health-assistant/id6763202025",
        "homepage": "https://apps.apple.com/us/app/kim-ai-health-assistant/id6763202025",
        "type": "app",
        "appStoreName": "Kim - AI Health Assistant",
        "appStoreUrl": "https://apps.apple.com/us/app/kim-ai-health-assistant/id6763202025",
        "sourceChannels": ["producthunt"],
        "sourceUrl": "https://www.producthunt.com/r/p/1156976?app_id=339",
        "tags": ["健康AI", "Apple Health", "可穿戴设备", "个人健康管理"],
        "analysis": {
            "targetAudience": "关注健康数据但不知道如何解读和行动的 iPhone/Apple Watch 用户",
            "useCases": [
                "解读 Apple Health 中的睡眠、心率、运动等数据趋势",
                "设计个性化健康实验（追踪补剂、饮食习惯对身体的影响）",
                "将可穿戴设备数据与血液检测结果交叉分析",
                "用对话方式获取基于个人数据的健康建议",
                "长期追踪健康指标变化并发现潜在规律"
            ],
            "designIntent": "Apple Health 积累了海量数据，但大多数用户看不懂这些数字意味着什么。Kim 要做的就是在数据和行动之间搭一座桥——用 AI 把冰冷的数字变成你能理解、能执行的健康洞察。",
            "problemSolved": "解决了可穿戴设备数据丰富但洞察匮乏的问题。用户不再面对一堆心率曲线和睡眠分数发呆，而是获得基于自己数据的个性化解读和可操作建议。",
            "score": 8,
            "scoreReason": "健康+AI 是确定性极高的赛道，Apple Health 生态用户基数庞大。产品定位清晰——不做诊断，做洞察层。但需注意医疗合规风险，且依赖用户持续佩戴设备提供数据。",
            "competitors": [
                {"name": "Whoop", "url": "https://www.whoop.com/", "comparison": "专业健康追踪手环+分析平台，需要购买专用硬件；Kim 纯软件方案，利用已有 Apple 设备数据"},
                {"name": "InsideTracker", "url": "https://www.insidetracker.com/", "comparison": "基于血液检测的个性化健康建议，需要抽血；Kim 结合可穿戴+血液数据，更全面"},
                {"name": "Apple Health 原生", "url": "https://www.apple.com/health/", "comparison": "Apple 官方健康应用，数据展示为主；Kim 提供 AI 分析层，让数据变成行动"}
            ]
        }
    },
    {
        "id": "producthunt.com/r/p/1158437",
        "name": "Drafted",
        "slug": "drafted",
        "description": "AI 家居设计工具，上传一张房间照片，AI 秒级生成专业级室内设计方案。支持多种风格选择，可下载 PDF 和 CAD 文件，让你瞬间拥有梦想中的家。",
        "url": "https://www.drafted.ai/",
        "homepage": "https://www.drafted.ai/",
        "type": "website",
        "sourceChannels": ["producthunt"],
        "sourceUrl": "https://www.producthunt.com/r/p/1158437?app_id=339",
        "tags": ["AI设计", "室内装修", "家居改造", "创意工具"],
        "analysis": {
            "targetAudience": "正在装修或想改造家居空间的房主、室内设计爱好者、房产中介",
            "useCases": [
                "上传房间照片，一键生成多种风格的重新设计方案",
                "装修前预览不同家具摆放和配色方案的效果",
                "为房产展示生成虚拟 staging 效果图",
                "将 AI 设计方案导出为 CAD 文件供施工参考",
                "探索小空间改造可能性，寻找灵感"
            ],
            "designIntent": "让每个人都能成为自己家的设计师。传统室内设计需要聘请专业人士、花费数周时间；Drafted 用 AI 将这个过程压缩到几秒钟，让看到效果再决定成为可能。",
            "problemSolved": "解决了装修决策中最大的痛点——无法提前看到最终效果。用户不再需要凭想象选择家具和配色，而是用 AI 实时预览，降低装修踩坑风险和决策焦虑。",
            "score": 8,
            "scoreReason": "视觉化 AI 设计工具用户友好度极高，装修是刚需场景。上传照片即出效果的交互方式门槛极低。但 AI 生成的设计图与实际施工效果可能存在差距，需要管理用户预期。",
            "competitors": [
                {"name": "ReimagineHome", "url": "https://www.reimaginehome.ai/", "comparison": "类似的 AI 室内设计工具，功能全面但界面较复杂；Drafted 更轻量简洁"},
                {"name": "Coohom", "url": "https://www.coohom.com/", "comparison": "专业级 3D 室内设计平台，功能强大但学习曲线陡；Drafted 面向普通用户，即拍即出图"},
                {"name": "Homestyler", "url": "https://www.homestyler.com/", "comparison": "阿里旗下 3D 设计工具，需要手动建模；Drafted 完全 AI 驱动，零建模门槛"}
            ]
        }
    },
    {
        "id": "producthunt.com/r/p/1158026",
        "name": "Agent A by Ahrefs",
        "slug": "agent-a-by-ahrefs",
        "description": "Ahrefs 推出的 AI 营销代理，基于 170 万亿+索引页面的行业领先数据集构建。能分析、构建并执行营销洞察，从 SEO 分析到内容策略一站式搞定。",
        "url": "https://ahrefs.com/agent-a",
        "homepage": "https://ahrefs.com/agent-a",
        "type": "saas",
        "sourceChannels": ["producthunt"],
        "sourceUrl": "https://www.producthunt.com/r/p/1158026?app_id=339",
        "tags": ["AI营销", "SEO工具", "数据分析", "内容策略"],
        "analysis": {
            "targetAudience": "中小企业营销人员、SEO 从业者、内容营销团队",
            "useCases": [
                "用自然语言提问获取 SEO 竞品分析和关键词策略",
                "自动生成基于数据洞察的内容营销方案",
                "监控竞品动态并获得实时营销建议",
                "自动化执行重复性营销任务（报告生成、数据整理）",
                "跨平台营销效果分析和优化建议"
            ],
            "designIntent": "把 Ahrefs 十年积累的海量 SEO 数据库与 AI Agent 能力结合，让营销人员不再需要在 Excel 和仪表盘之间手动挖掘数据。从看数据升级为 AI 帮你想、帮你做。",
            "problemSolved": "解决了中小营销团队有数据但没时间分析的痛点。传统 SEO 工具需要专业技能才能用好，Agent A 让任何人用对话方式就能获得专业级营销洞察和执行方案。",
            "score": 8,
            "scoreReason": "Ahrefs 数据护城河深厚（170T+ 索引页面），AI Agent 化是数据平台的自然进化。$99/月的定价对中小企业友好。但营销 AI Agent 赛道拥挤，需证明 ROI 才能留住用户。",
            "competitors": [
                {"name": "Semrush Copilot", "url": "https://www.semrush.com/copilot/", "comparison": "Semrush 的 AI 助手，侧重数据可视化和建议；Agent A 更强调自主执行能力"},
                {"name": "Surfer SEO", "url": "https://surferseo.com/", "comparison": "AI 内容优化工具，侧重文章撰写；Agent A 覆盖更广的营销场景"},
                {"name": "ChatGPT + SEO Plugins", "url": "https://chat.openai.com/", "comparison": "通用 AI 加插件的 SEO 方案，数据源分散；Agent A 原生接入 Ahrefs 专业数据"}
            ]
        }
    },
    {
        "id": "producthunt.com/r/p/1157856",
        "name": "RabbitTravel",
        "slug": "rabbittravel",
        "description": "AI 驱动的智能旅行规划平台，为全球任何目的地构建优化行程。结合智能路线规划、实时交通整合和个性化推荐，让旅行规划变得轻松高效。",
        "url": "https://www.producthunt.com/products/rabbittravel",
        "homepage": "https://www.producthunt.com/products/rabbittravel",
        "type": "website",
        "sourceChannels": ["producthunt"],
        "sourceUrl": "https://www.producthunt.com/r/p/1157856?app_id=339",
        "tags": ["AI旅行", "行程规划", "旅游助手", "智能推荐"],
        "analysis": {
            "targetAudience": "喜欢自由行但厌倦做攻略的旅行者、经常出差需要高效安排行程的商务人士",
            "useCases": [
                "输入目的地和偏好，一键生成多日优化行程",
                "根据实时交通数据动态调整景点游览顺序",
                "基于个人兴趣推荐小众景点和本地美食",
                "多人同行时自动协调不同偏好的行程安排",
                "旅行中实时修改行程并获得即时路线优化"
            ],
            "designIntent": "旅行规划是很多人出行前最大的心理负担——要在海量信息中筛选、在有限时间内安排合理路线。RabbitTravel 用 AI 把做攻略从几小时压缩到几分钟，让旅行从累在规划变成乐在出发。",
            "problemSolved": "解决了自由行最大的前置障碍——攻略焦虑。传统方式需要翻阅几十篇游记、对比多个平台信息、手动规划路线；AI 行程规划让这些工作自动化，用户只需表达偏好即可。",
            "score": 7,
            "scoreReason": "旅行规划是高频刚需场景，AI 自动化价值明显。智能路线优化和实时交通整合是差异化亮点。但旅行 AI 赛道已有 TripPlanner AI、Wonderplan 等玩家，需在推荐质量上建立壁垒。",
            "competitors": [
                {"name": "TripPlanner AI", "url": "https://tripplanner.ai/", "comparison": "AI 行程规划工具，功能类似；RabbitTravel 强调实时交通整合和动态调整"},
                {"name": "Wanderlog", "url": "https://wanderlog.com/", "comparison": "旅行规划协作平台，侧重多人协作；RabbitTravel 更侧重 AI 自动规划"},
                {"name": "Google Trips (已停)", "url": "https://trips.google.com/", "comparison": "Google 曾推出的旅行工具，已停止服务；RabbitTravel 填补了这一空缺"}
            ]
        }
    }
]

# Write daily report
report = {
    "date": today,
    "generatedAt": now.isoformat(),
    "productCount": len(selected_products),
    "products": []
}

for p in selected_products:
    product = {
        "id": p["id"],
        "name": p["name"],
        "slug": p["slug"],
        "description": p["description"],
        "url": p["url"],
        "homepage": p["homepage"],
        "type": p["type"],
        "appStoreName": p.get("appStoreName"),
        "appStoreUrl": p.get("appStoreUrl"),
        "screenshotUrl": None,
        "appStoreScreenshots": [],
        "tags": p["tags"],
        "sourceChannels": p["sourceChannels"],
        "sourceUrl": p["sourceUrl"],
        "firstSeen": now.isoformat(),
        "analysis": p["analysis"]
    }
    report["products"].append(product)

report_path = f"/Volumes/EXTEND/aI-product-daily-peport/reports/daily/{today}.json"
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"Report written to {report_path}")
print(f"Products: {len(selected_products)}")
for p in selected_products:
    print(f"  - {p['name']} ({p['analysis']['score']}/10) [{', '.join(p['sourceChannels'])}]")

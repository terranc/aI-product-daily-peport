#!/usr/bin/env python3
"""
Step 4-5: 写入今日报告 + 更新数据库 + 截图
"""
import json
import sys
import time
from datetime import datetime, timezone, timedelta

sys.path.insert(0, '/home/pin/aI-product-daily-peport/scripts')
from screenshot import process_product_screenshots

BASE_DIR = '/home/pin/aI-product-daily-peport'
now_utc = datetime.now(timezone.utc)
today_str = now_utc.strftime('%Y-%m-%d')

# === TOP 5 精选产品 ===
# 经过 LLM 筛选（过滤技术产品、AI 模型/框架/SDK、编码工具、开源开发者工具等），
# 保留"把 AI 能力融入普通应用场景"的面向终端用户产品。

selected_products = [
    {
        'id': 'producthunt.com/r/p/1251122',
        'name': 'MosMos',
        'slug': 'mosmos',
        'name_cn': 'MosMos 语音写作助手',
        'description': '一款 AI 驱动的桌面语音写作与会议助手，在任何应用中通过语音输入即可生成润色后的专业文本；支持多人会议实时转写、说话人分离、自动总结与行动项提取。',
        'url': 'https://mosmos.io/',
        'homepage': 'https://mosmos.io/',
        'type': 'app',
        'appStoreName': None,
        'appStoreUrl': None,
        'screenshotUrl': None,
        'appStoreScreenshots': [],
        'tags': ['语音写作', '会议助手', 'AI 转写', '生产力'],
        'sourceChannels': ['producthunt'],
        'sourceUrl': 'https://www.producthunt.com/r/p/1251122?app_id=339',
        'firstSeen': now_utc.isoformat(),
        'analysis': {
            'targetAudience': '知识工作者、产品经理、远程会议频繁的职场人士和创意写作者',
            'useCases': [
                '会议实时转写与自动总结，提取行动项和负责人',
                '在任意应用中语音快速输入邮件、文档、消息',
                '头脑风暴时语音记录想法，AI 自动整理成结构化笔记',
                '多语言会议翻译与关键决策留痕',
            ],
            'designIntent': '旨在打破"语音输入只是听写"的局限，将自然口语转化为专业书面文本，同时覆盖会议前中后的全流程。让思考速度不再受打字速度限制，也让会议不再需要专人记录。',
            'problemSolved': '解决了传统语音听写只能逐字转录、需要手动修改的痛点，以及会议后花大量时间整理笔记和行动项的低效问题。同时支持个人词汇本，专业术语也能准确识别。',
            'score': 8,
            'scoreReason': '产品定位清晰，覆盖了"语音写作+会议智能"两个高频场景，AI 润色和说话人分离是差异化亮点。作为桌面端应用，跨应用的全局输入能力实用性强。扣分项是目前仅支持 macOS，生态较新。',
            'competitors': [
                {'name': 'Otter.ai', 'url': 'https://otter.ai', 'comparison': 'Otter 更侧重云端会议转写与协作，MosMos 则强调本地桌面端和全局语音输入，写作润色能力更强'},
                {'name': 'Fireflies.ai', 'url': 'https://fireflies.ai', 'comparison': 'Fireflies 主打企业级会议纪要与 CRM 集成，MosMos 更偏向个人生产力和写作场景'},
            ],
        },
    },
    {
        'id': 'peelaway.io',
        'name': 'Peelaway',
        'slug': 'peelaway',
        'name_cn': 'Peelaway 风格化图像生成器',
        'description': '一款 AI 图像创作工具，提供精心策划的视觉风格画廊，用户选择喜欢的风格后，可通过照片或文字提示生成插画、版画、微缩场景等各种风格化作品。',
        'url': 'https://peelaway.io/',
        'homepage': 'https://peelaway.io/',
        'type': 'website',
        'appStoreName': None,
        'appStoreUrl': None,
        'screenshotUrl': None,
        'appStoreScreenshots': [],
        'tags': ['AI 绘画', '图像生成', '设计工具', '创意'],
        'sourceChannels': ['hackernews'],
        'sourceUrl': 'https://peelaway.io/',
        'firstSeen': now_utc.isoformat(),
        'analysis': {
            'targetAudience': '设计师、社交媒体创作者、插画爱好者和需要快速制作风格化配图的内容创作者',
            'useCases': [
                '将照片转换为丝网版画、插画、微缩场景等艺术风格',
                '为博客文章、社交媒体帖子快速生成风格统一的配图',
                '设计师探索不同视觉风格，获取灵感参考',
                '个人头像、海报等创意图像制作',
            ],
            'designIntent': '从"风格选择"而非"提示词工程"切入，降低 AI 图像创作的门槛。用户不需要写复杂的 prompt，只要选一个喜欢的风格，上传照片或简单描述就能得到高质量作品。',
            'problemSolved': '解决了传统 AI 绘画工具需要大量提示词调试、风格难以稳定复现的问题。预先策划的风格画廊让创作过程更直观、结果更可控，特别适合非专业用户。',
            'score': 7,
            'scoreReason': '产品切入点巧妙，用"风格画廊"替代 prompt 工程，降低了使用门槛。视觉效果有特色，Hacker News 上反响不错。扣分项是功能相对单一，与 Midjourney、DALL-E 等大而全的工具相比竞争激烈。',
            'competitors': [
                {'name': 'Midjourney', 'url': 'https://midjourney.com', 'comparison': 'Midjourney 功能更全面但学习曲线陡，Peelaway 以风格画廊为核心，上手更快、结果更可预测'},
                {'name': 'Canva AI Image Generator', 'url': 'https://www.canva.com', 'comparison': 'Canva 是大而全的设计平台，Peelaway 更专注于风格化图像生成，艺术质感更突出'},
            ],
        },
    },
    {
        'id': 'producthunt.com/r/p/1252513',
        'name': 'GameToMac',
        'slug': 'gametomac',
        'name_cn': 'GameToMac 游戏兼容性工具',
        'description': '让 Apple Silicon Mac 用户流畅运行 Windows 游戏的 AI 优化兼容性工具。由 GPT-6 Astra 辅助识别性能瓶颈并优化，首款支持《帝国时代 IV》，帧率可达 70-150 FPS。',
        'url': 'https://gametomac.com/',
        'homepage': 'https://gametomac.com/',
        'type': 'app',
        'appStoreName': None,
        'appStoreUrl': None,
        'screenshotUrl': None,
        'appStoreScreenshots': [],
        'tags': ['游戏', 'Mac 工具', 'AI 优化', '兼容性'],
        'sourceChannels': ['producthunt'],
        'sourceUrl': 'https://www.producthunt.com/r/p/1252513?app_id=339',
        'firstSeen': now_utc.isoformat(),
        'analysis': {
            'targetAudience': 'Apple Silicon Mac 用户、游戏爱好者、想在 Mac 上玩 Windows 独占游戏的玩家',
            'useCases': [
                '在 Mac 上流畅运行 Windows 独占游戏如《帝国时代 IV》',
                '通过 Steam 集成直接管理和启动已拥有的游戏库',
                '无需安装 Windows 虚拟机或双系统即可享受 PC 游戏',
                '游戏开发者在 Mac 上测试 Windows 版本游戏表现',
            ],
            'designIntent': '用 AI 驱动的游戏级优化打破 Mac 游戏生态匮乏的困局。不是做通用兼容层，而是针对每款游戏做深度调优，确保"开箱即用"的流畅体验，让 Mac 用户不用再为玩游戏换电脑。',
            'problemSolved': '解决了 Apple Silicon Mac 上 Windows 游戏兼容性差、性能低下的长期痛点。通过 AI 识别 Wine 异常处理和 Rosetta 重复翻译等瓶颈，将帧间隔从 160ms 压缩到 11.75ms，实现了从"不能玩"到"流畅玩"的跨越。',
            'score': 8,
            'scoreReason': '技术突破显著，AI 辅助优化兼容性层的思路新颖且效果惊艳（帧率提升 10 倍以上）。对 Mac 游戏玩家是刚需产品，市场痛点明确。扣分项是目前支持游戏数量极少（仅 1 款），需要持续扩充游戏库。',
            'competitors': [
                {'name': 'Whisky', 'url': 'https://getwhisky.app', 'comparison': 'Whisky 是通用 Wine 封装工具，支持更多游戏但需用户自行配置，GameToMac 是精挑细选的游戏级优化，体验更稳定但游戏少'},
                {'name': 'CrossOver', 'url': 'https://www.codeweavers.com/crossover', 'comparison': 'CrossOver 是商业级兼容层，游戏支持更多但价格高，GameToMac 用 AI 做单游戏深度优化，性能上限更高'},
            ],
        },
    },
    {
        'id': 'producthunt.com/r/p/1253717',
        'name': 'StillTalk',
        'slug': 'stilltalk',
        'name_cn': 'StillTalk 会说话的照片',
        'description': '基于客户端渲染的 AI 数字人动画技术，让一张静态照片变成会说话、有表情的虚拟形象。所有动画在用户设备本地渲染，无需云端视频流，低延迟、低成本。',
        'url': 'https://stilltalk.ai/',
        'homepage': 'https://stilltalk.ai/',
        'type': 'website',
        'appStoreName': None,
        'appStoreUrl': None,
        'screenshotUrl': None,
        'appStoreScreenshots': [],
        'tags': ['AI 数字人', '图像动画', '客户端渲染', '交互设计'],
        'sourceChannels': ['producthunt'],
        'sourceUrl': 'https://www.producthunt.com/r/p/1253717?app_id=339',
        'firstSeen': now_utc.isoformat(),
        'analysis': {
            'targetAudience': '前端/移动端开发者、品牌营销团队、在线教育平台和需要虚拟形象的产品团队',
            'useCases': [
                '网站/APP 中嵌入交互式 AI 数字人客服或导览员',
                '在线教育课程中用虚拟讲师形象增加课程互动感',
                '品牌营销活动中制作低成本动态虚拟代言人',
                '游戏或社交产品中的角色实时对话动画',
            ],
            'designIntent': '把数字人动画的渲染从云端搬到终端设备，用轻量化的数据驱动替代视频流传输。目标是让数字人的使用成本降低几个数量级，同时获得更低的延迟和更好的隐私性。',
            'problemSolved': '解决了传统云端数字人视频流方案成本高、延迟大、依赖稳定网络的问题。客户端渲染让数字人可以在任何设备上即时运行，初始资源加载后几乎零额外成本，特别适合大规模用户场景。',
            'score': 7,
            'scoreReason': '技术路线有差异化，客户端渲染 vs 云端视频流的降本效应明显，对开发者和企业用户有实际价值。扣分项是目前更偏技术基础设施，终端用户直接使用的场景有限，B 端落地周期可能较长。',
            'competitors': [
                {'name': 'Synthesia', 'url': 'https://www.synthesia.io', 'comparison': 'Synthesia 是云端视频生成方案，效果精美但价格高且有延迟，StillTalk 走端侧渲染路线，成本低、延迟小但画面精细度略逊'},
                {'name': 'D-ID', 'url': 'https://www.d-id.com', 'comparison': 'D-ID 同样是云端 API 方案，专注照片驱动的数字人，StillTalk 的端侧渲染在数据隐私和大规模部署成本上更有优势'},
            ],
        },
    },
    {
        'id': 'v2ex.com/t/1243128',
        'name': 'FinDog',
        'slug': 'findog',
        'name_cn': 'FinDog 美股投研平台',
        'description': '面向中文用户的美股投研平台，覆盖标普 500 全部成分股的多维度指标，AI 自动抽取财报关键信息并可视化，支持股票对比和个股动态订阅。',
        'url': 'https://findog.app/',
        'homepage': 'https://findog.app/',
        'type': 'website',
        'appStoreName': None,
        'appStoreUrl': None,
        'screenshotUrl': None,
        'appStoreScreenshots': [],
        'tags': ['美股投研', 'AI 财报', '金融科技', '数据可视化'],
        'sourceChannels': ['v2ex'],
        'sourceUrl': 'https://www.v2ex.com/t/1243128',
        'firstSeen': now_utc.isoformat(),
        'analysis': {
            'targetAudience': '中文区美股投资者、个人交易者、关注美股市场的财经从业者',
            'useCases': [
                '每日盘后订阅美股总结，快速把握市场动态',
                '用 AI 快速阅读财报关键信息和数据可视化',
                '对比两只股票的核心指标差异辅助投资决策',
                '订阅个股动态，实时跟踪关注公司的信息变化',
            ],
            'designIntent': '为中文用户打造一站式美股投研工具，把零散的英文财报、市场数据用 AI 提炼成结构化、可视化的中文信息，降低中文投资者获取美股信息的门槛和时间成本。',
            'problemSolved': '解决了中文用户研究美股时面临的语言障碍、信息分散、工具分散的问题。传统投研工具要么是英文界面不友好，要么数据不全，FinDog 把标普 500 全量指标、AI 财报解读、动态订阅整合在一个中文平台上。',
            'score': 7,
            'scoreReason': '产品定位精准，瞄准中文美股投资者这个垂直群体，AI 财报可视化和个股动态订阅是实用功能。V2EX 社区反响不错。扣分项是盈利模式和数据权威性有待验证，且目前只覆盖标普 500，范围有限。',
            'competitors': [
                {'name': '老虎证券', 'url': 'https://www.tigersecurities.com', 'comparison': '老虎证券侧重交易和资讯，是券商属性的综合平台，FinDog 更专注投研分析和 AI 财报解读，工具属性更强'},
                {'name': '富途牛牛', 'url': 'https://www.futunn.com', 'comparison': '富途是全功能券商 APP，社区和交易强，FinDog 作为轻量级投研工具在 AI 分析深度和数据维度上更聚焦'},
            ],
        },
    },
]

# === Step 4: 网站截图 ===
print("=== Step 4: 网站截图 ===")
for i, product in enumerate(selected_products):
    print(f"\n[{i+1}/5] 截图: {product['name']} ({product['url']})")
    # 构造符合 process_product_screenshots 接口的 dict
    p_for_screenshot = {
        'id': product['id'],
        'type': product['type'],
        'url': product['url'],
        'homepage': product['homepage'],
        'name': product['name'],
    }
    try:
        result = process_product_screenshots(p_for_screenshot)
        product['screenshotUrl'] = result.get('screenshotUrl')
        product['appStoreScreenshots'] = result.get('appStoreScreenshots', [])
        product['appStoreName'] = result.get('appStoreName')
        product['appStoreUrl'] = result.get('appStoreUrl')
    except Exception as e:
        print(f"  ❌ 截图异常: {e}")
        product['screenshotUrl'] = None
    time.sleep(3)

# === Step 5a: 写入今日报告 ===
print("\n=== Step 5a: 写入今日报告 ===")
report = {
    'date': today_str,
    'generatedAt': now_utc.isoformat(),
    'productCount': len(selected_products),
    'products': selected_products,
}

report_path = f'{BASE_DIR}/reports/daily/{today_str}.json'
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(f"✅ 报告已写入: {report_path}")

# === Step 5b: 更新产品数据库 ===
print("\n=== Step 5b: 更新产品数据库 ===")
db_path = f'{BASE_DIR}/data/products.json'
with open(db_path, 'r', encoding='utf-8') as f:
    db = json.load(f)

cooldown = (now_utc + timedelta(days=14)).isoformat()
new_count = 0
for product in selected_products:
    pid = product['id']
    # 检查是否已存在
    exists = any(p.get('id') == pid for p in db['products'])
    if not exists:
        db_entry = {
            'id': pid,
            'name': product['name_cn'],
            'slug': product['slug'],
            'description': product['description'],
            'url': product['url'],
            'type': product['type'],
            'tags': product['tags'],
            'metrics': {},
            'analysis': product['analysis'],
            'addedAt': now_utc.isoformat(),
            'cooldownExpiresAt': cooldown,
        }
        db['products'].append(db_entry)
        new_count += 1
    else:
        # 更新 cooldown
        for p in db['products']:
            if p.get('id') == pid:
                p['cooldownExpiresAt'] = cooldown
                break

db['totalProducts'] = len(db['products'])
db['totalCount'] = len(db['products'])
db['lastUpdated'] = now_utc.isoformat()

with open(db_path, 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print(f"✅ 数据库已更新，新增 {new_count} 个产品，总数: {len(db['products'])}")

# Print summary
print("\n" + "="*60)
print("📊 最终结果")
print("="*60)
print(f"精选产品数: {len(selected_products)}")
for i, p in enumerate(selected_products):
    print(f"\n[{i+1}] {p['name_cn']}")
    print(f"    评分: {p['analysis']['score']}/10")
    print(f"    简介: {p['description'][:80]}...")
    print(f"    来源: {', '.join(p['sourceChannels'])}")
    print(f"    截图: {p.get('screenshotUrl', 'None')}")

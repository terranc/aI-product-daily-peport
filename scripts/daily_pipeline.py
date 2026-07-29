#!/usr/bin/env python3
"""Daily pipeline step: create report + update database"""

import json, os, sys
from datetime import datetime, timezone, timedelta

today = datetime.now(timezone.utc)
date_str = today.strftime('%Y-%m-%d')
iso_now = today.isoformat()

BASE = '/Volumes/EXTEND/aI-product-daily-peport'

products = [
    {
        'id': 'producthunt.com/r/p/1208168',
        'name': 'Tag Your Photos',
        'name_zh': 'Tag Your Photos — AI ���片关键词工具',
        'description': '一款 macOS 应用，100% 在本地为 Apple Photos 照片库自动生成关键词标签。使用 Gemma 4 12B 模型通过 Apple MLX 框���在设备端运行，不上传任何数据到云端。生成的关键词可被 Spotlight 全局搜索，甚至能在 iPhone/iPad 主���搜索。',
        'slug': 'tag-your-photos',
        'homepage': 'https://www.producthunt.com/r/p/1208168',
        'url': 'https://www.producthunt.com/r/p/1208168',
        'type': 'app',
        'sourceChannels': ['producthunt'],
        'sourceUrl': 'https://www.producthunt.com/r/p/1208168?app_id=339',
        'firstSeen': iso_now,
        'screenshotUrl': None,
        'appStoreName': None,
        'appStoreUrl': None,
        'appStoreScreenshots': [],
        'tags': ['照片管理', 'AI标签', '本地AI', 'macOS', '隐��保护'],
        'analysis': {
            'targetAudience': '拥有大量 Apple Photos 照片、需要高效检索和整理照片的 Mac 用户',
            'useCases': [
                '给数千张照片批量添加关键词标签，方便检索',
                '通过 Spotlight 全局搜索照片内容',
                '在 iPhone/iPad 主屏直接搜索照片关键词',
                '照片库隐私保护——无需上传云端'
            ],
            'designIntent': '解决 Apple Photos 用户无法高效搜索照片的痛点。大多数 AI 标签工具需要���传云端，而这款应用 100% 在本地运行，结合 Apple MLX 框架��� Gemma 4 模型，既保护隐私又保证标签质量。',
            'problemSolved': 'Apple Photos 内置搜��能力有限，无法识别照片中的���体物体、场景和人物。传统方案需要手动添加关键词或上传云���。这款应用自动为每张照片生成精准关键词，全部在本地完成。',
            'score': 8,
            'scoreReason': '解决了一个真实且广泛的痛点（照片整理），100% 本地运行保障隐私，技���方案扎实（Gemma 4+MLX），但受众限于 Mac Apple Silicon 用��。',
            'competitors': [
                {'name': 'VisionTagger', 'url': 'https://www.synendo.com/visiontagger', 'comparison': '功能类似，但也支持导出 XMP 元数据，价格 $34.99 一次性购买'},
                {'name': 'Apple Photos 智能搜索', 'url': 'https://www.apple.com/macos/photos/', 'comparison': '苹果内置的 AI 搜索，精度和关���词维度不如专用工具'}
            ]
        }
    },
    {
        'id': 'chromewebstore.google.com/detail/voicehoprealtimeaudio/gpjfekccjgnojplebmaafgbhjggimfio',
        'name': 'VoiceHop',
        'name_zh': 'VoiceHop — 实时音视频翻译',
        'description': '一款 Chrome 浏览器扩展，��现实时语音到语音的翻译。支持 YouTube、Netflix、Zoom、Google Meet 等平台的音视频内容实时翻译，亚秒级���迟，保留原始说话人音色。支持中英日法德等多���语言。',
        'slug': 'voicehop',
        'homepage': 'https://voicehop.app',
        'url': 'https://voicehop.app',
        'type': 'extension',
        'sourceChannels': ['hackernews'],
        'sourceUrl': 'https://chromewebstore.google.com/detail/voicehop-real-time-audio/gpjfekccjgnojplebmaafgbhjggimfio',
        'firstSeen': iso_now,
        'screenshotUrl': None,
        'appStoreName': 'Chrome Web Store',
        'appStoreUrl': 'https://chromewebstore.google.com/detail/voicehop-real-time-audio/gpjfekccjgnojplebmaafgbhjggimfio',
        'appStoreScreenshots': [],
        'tags': ['实时翻译', '音视频翻译', 'Chrome扩展', '多语言', '语音合成'],
        'analysis': {
            'targetAudience': '需要跨语言观看外国视频��参与国际会议或在线学习的用户',
            'useCases': [
                '实时翻译 YouTube 上的外语视频���容',
                '在 Zoom/Google Meet 国际会议中实时翻译',
                '观看 Netflix 外语影视剧无需字幕',
                '���线学习国外���程直播翻译'
            ],
            'designIntent': '打破语言壁垒，让用户无需等待字幕，直接用母语听任何语言的内容。通过保留原始说话人音色实现更自然的翻译体验，同时支持主流视频和会议平台。',
            'problemSolved': '传统翻译工具要么是文本字幕形式���打断观看体验），要么延迟高、不支持实时场景。VoiceHop 在浏览器层面实现亚秒级语音到语音翻��，保留原始音色，覆盖视频、直播、会议全场景。',
            'score': 8,
            'scoreReason': '解决了跨语言内容消费的真实刚需，技术实现扎实（亚秒级延迟+音色保留），覆盖场景���泛，但付费订阅模式���轻度用户门槛��高。',
            'competitors': [
                {'name': 'Google 翻译', 'url': 'https://translate.google.com', 'comparison': '免费但只有文本翻译，不支持实时语音转语音'},
                {'name': 'DeepL', 'url': 'https://www.deepl.com', 'comparison': '翻译���量高但仅限于文本，不支持音视频实时场景'}
            ]
        }
    },
    {
        'id': 'producthunt.com/r/p/1208008',
        'name': 'Pinery Prose',
        'name_zh': 'Pinery Prose — AI 协作写书出版工具',
        'description': 'Mac 平台自出版工作室，集成 AI 协作写书功能。AI 以差异对���(diff)形式提供修改建议，用户逐条审阅后才能��认。支持从草稿到排版设计再到导��� ePub/PDF 的全流程。文���以纯 Markdown 存储，用户完全��有数据。',
        'slug': 'pinery-prose',
        'homepage': 'https://pinery.app',
        'url': 'https://pinery.app',
        'type': 'app',
        'sourceChannels': ['producthunt'],
        'sourceUrl': 'https://www.producthunt.com/r/p/1208008?app_id=339',
        'firstSeen': iso_now,
        'screenshotUrl': None,
        'appStoreName': 'Mac App Store',
        'appStoreUrl': 'https://apps.apple.com/app/pinery-self-publishing-app/id6747726205',
        'appStoreScreenshots': [],
        'tags': ['写作工具', 'AI写作', '自出��', 'Markdown', 'macOS'],
        'analysis': {
            'targetAudience': '独立作者、自出版作家、技术写作者，需要一站式写作+排版+出版工具的 Mac 用户',
            'useCases': [
                '从零开始撰写电子书，AI 辅助章节起草',
                '对已有稿件进行 AI 润色和建议，逐条审阅修改',
                '一键导出 ePub 3 格式上传��流电子书平���',
                '生成高质量 PDF 印刷版'
            ],
            'designIntent': '为独立作者���造专业级的自出��工具。传统出版流程��要分别使用写作���排版、设计软件，Pinery将全流程整合到一个应用中，AI仅作为辅助工具，修改须经作��逐条确认。',
            'problemSolved': '独立作者面临写作工具碎片化的痛点���Word排版困难、Scrivener学习曲线陡、AI工具可能擅自修改原文。Pinery用Markdown降��技术门槛，AI以diff形式建议修改，保持作��对内容的完全控制。',
            'score': 7,
            'scoreReason': '定位精��、用户体验优秀（原生 Mac 应用）、隐私保护好，但写作 AI 功能相比专有 AI 写作工具还不够深度，且仅限 Mac 平台。',
            'competitors': [
                {'name': 'Scrivener', 'url': 'https://www.literatureandlatte.com/scrivener/overview', 'comparison': '经典写作工具，功能强��但无 AI 能力，学习曲线陡峭'},
                {'name': 'Atticus', 'url': 'https://www.atticus.io', 'comparison': '在线自出版工具，支持排版但无 Mac 原生应用，AI 功能有限'}
            ]
        }
    },
    {
        'id': 'producthunt.com/r/p/1208295',
        'name': 'EasyCircuit',
        'name_zh': 'EasyCircuit — AI 硬件电路设计协作工具',
        'description': '一款 AI 电路协作工具，用户用自然语言描述需求，AI 即自动设计完整电路原理图、匹配并采购零部件、生成面包板原型布局和焊接版布局图。无需电子工程背景。从想法到原���的一站式硬件开发平台。',
        'slug': 'easycircuit',
        'homepage': 'https://www.producthunt.com/r/p/1208295',
        'url': 'https://www.producthunt.com/r/p/1208295',
        'type': 'website',
        'sourceChannels': ['producthunt'],
        'sourceUrl': 'https://www.producthunt.com/r/p/1208295?app_id=339',
        'firstSeen': iso_now,
        'screenshotUrl': None,
        'appStoreName': None,
        'appStoreUrl': None,
        'appStoreScreenshots': [],
        'tags': ['硬件原型', '电路设计', 'AI辅助设计', '创客', '物联网'],
        'analysis': {
            'targetAudience': '有创意想法但没有电子工程背景的开发者、创客、产品经理和爱好者',
            'useCases': [
                '从自然语言描述生成完整电路��理图',
                '自动匹配零部件并��键下单套件',
                '面包板原型搭建到焊接版成���',
                '学习电路设计原理——AI解释每一步设计决策'
            ],
            'designIntent': '将 Vibe Coding 的理念引入硬件领域。创始人自己因想做植物生长实验箱但不懂电路设计，经历数天研究后决定打造这款工具，让非 EE 背景的人也能轻松实现硬件创意。',
            'problemSolved': '硬件原型设计的门槛极高：需要看数据手���、选型、查库存、设计原理图、布线。传统流程耗时数天到数周。EasyCircuit 将整个过程压缩到一句话描述 -> AI设计 -> 一键下单材料包 -> 分步搭建。',
            'score': 8,
            'scoreReason': '将 AI 能力创新性地应用到硬件领域，解决真实痛点，技术方案扎实（AI+供应链整合），护城河明显。但产品尚早（290+零件库），部分高级场景仍需人工确认。',
            'competitors': [
                {'name': 'Cirkit Designer', 'url': 'https://www.cirkitdesigner.com', 'comparison': '浏览器端 AI 电路设计工具，支持仿真，但无一键采购��套件配送'},
                {'name': 'TSCircuit', 'url': 'https://tscircuit.com', 'comparison': '代码生成 PCB，需要 React 编程知识，更适合有编程背景的用户'}
            ]
        }
    },
    {
        'id': 'producthunt.com/r/p/1207636',
        'name': 'SUB/WAVE',
        'name_zh': 'SUB/WAVE — AI 电台 DJ',
        'description': '自托管开源电台系统，使用 AI DJ 24/7 播放你的个人音乐库。AI DJ 可以选曲、做电台 ID、报时播天气、接受听众点歌。支持本地 Ollama 模型、本地 TTS，��需云服务。一���流、所有听众同时收听同一首歌，没有跳过按钮。',
        'slug': 'sub-wave',
        'homepage': 'https://www.getsubwave.com',
        'url': 'https://www.getsubwave.com',
        'type': 'saas',
        'sourceChannels': ['producthunt'],
        'sourceUrl': 'https://www.producthunt.com/r/p/1207636?app_id=339',
        'firstSeen': iso_now,
        'screenshotUrl': None,
        'appStoreName': None,
        'appStoreUrl': None,
        'appStoreScreenshots': [],
        'tags': ['AI电台', '音乐', '���托管', '开源', '本地AI'],
        'analysis': {
            'targetAudience': '拥有个人音乐库（Navidrome/Plex等）并希望找回电台式听歌体验的���乐爱好者',
            'useCases': [
                '将个人音乐库变成 24/7 直播电台',
                'AI DJ 根据时间、天气、听众点歌智能选曲',
                '多角色 DJ 轮���、嘉宾主持聊天',
                '家人朋友同时收听同一个频道'
            ],
            'designIntent': '在流媒体时���找回传统电台的共享收听体验。创始人���为 Spotify 等流媒体虽然提供了无限选择，但让人孤独地困在自己的算法泡泡里。SUB/WAVE 让所有人都听到同一首歌、同一个 DJ。',
            'problemSolved': '现代流媒体听歌体验是孤独和算法驱动的。传统电台又无法使用个人音乐库。SUB/WAVE 结合个人音乐库+AI DJ+共享流，创造���独特的私人电台体验。',
            'score': 7,
            'scoreReason': '创意独特、开��� MIT 协议、���术实现完整（AI DJ+本地TTS+多��台客户端），但受众较窄（需要自有音乐库和自托管能力），对纯流媒体用户不适用。',
            'competitors': [
                {'name': 'Plexamp', 'url': 'https://www.plex.tv/plexamp/', 'comparison': 'Plex 的��乐播放器，有 AI DJ 功能但需��� Plex Pass 订阅，无共享收听模式'},
                {'name': 'Spotify AI DJ', 'url': 'https://www.spotify.com', 'comparison': 'Spotify 内置 AI DJ 推荐，但不能使用自有音乐库，且是单人收听模式'}
            ]
        }
    }
]

# Build report
report = {
    'date': date_str,
    'generatedAt': iso_now,
    'productCount': len(products),
    'summary': {
        'totalCandidates': 184,
        'dedupedCount': 0,
        'filteredOutTechnical': 179,
        'selectedCount': 5
    },
    'products': []
}

for p in products:
    report['products'].append({
        'id': p['id'],
        'name': p['name_zh'],
        'slug': p['slug'],
        'description': p['description'],
        'url': p['url'],
        'homepage': p['homepage'],
        'type': p['type'],
        'appStoreName': p['appStoreName'],
        'appStoreUrl': p['appStoreUrl'],
        'screenshotUrl': p['screenshotUrl'],
        'appStoreScreenshots': p['appStoreScreenshots'],
        'tags': p['tags'],
        'sourceChannels': p['sourceChannels'],
        'sourceUrl': p['sourceUrl'],
        'firstSeen': p['firstSeen'],
        'analysis': p['analysis']
    })

# Save report
report_dir = f'{BASE}/reports/daily'
os.makedirs(report_dir, exist_ok=True)
report_path = f'{report_dir}/{date_str}.json'
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(f'Report saved: {report_path}')

# Update products database
with open(f'{BASE}/data/products.json', encoding='utf-8') as f:
    db_data = json.load(f)
db_products = db_data['products'] if isinstance(db_data, dict) and 'products' in db_data else db_data

cooldown_date = (today + timedelta(days=14)).isoformat()

new_entries = []
for p in products:
    entry = {
        'id': p['id'],
        'name': p['name_zh'],
        'description': p['description'],
        'url': p['url'],
        'homepage': p['homepage'],
        'slug': p['slug'],
        'type': p['type'],
        'tags': p['tags'],
        'sourceChannels': p['sourceChannels'],
        'sourceUrl': p['sourceUrl'],
        'firstSeen': p['firstSeen'],
        'cooldownExpiresAt': cooldown_date,
        'metrics': {
            'featuredInDaily': True,
            'featuredInWeekly': False,
            'timesFeatured': 1,
            'lastFeatured': date_str,
            'mentionCount7d': 1,
            'growthScore': 50
        },
        'analysis': p['analysis']
    }
    new_entries.append(entry)

if isinstance(db_data, dict) and 'products' in db_data:
    db_data['products'].extend(new_entries)
    db_data['lastUpdated'] = iso_now
    db_data['version'] = db_data.get('version', 1) + 1
else:
    db_data = db_data + new_entries

with open(f'{BASE}/data/products.json', 'w', encoding='utf-8') as f:
    json.dump(db_data, f, ensure_ascii=False, indent=2)

product_count = len(db_data['products']) if isinstance(db_data, dict) else len(db_data)
print(f'Database updated: +{len(new_entries)} products (total: {product_count})')
print(f'Cooldown expires at: {cooldown_date}')

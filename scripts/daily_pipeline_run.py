#!/usr/bin/env python3
"""AI Product Radar - Daily Pipeline (runs without user interaction)"""
import json
import time
import os
import sys
import requests
from datetime import datetime, timedelta, timezone

os.chdir('/home/pin/aI-product-daily-peport')

# === CONFIG ===
TODAY = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d')
NOW_ISO = datetime.now(timezone(timedelta(hours=8))).isoformat()
COOLDOWN_DAYS = 14
ASSETS_DIR = 'assets/screenshots'
WEBSHOT_API = 'https://webshot.site/api/capture'

os.makedirs(ASSETS_DIR, exist_ok=True)

# === LOAD DATA ===
with open('data/raw-candidates.json', 'r') as f:
    raw_data = json.load(f)

with open('data/products.json', 'r') as f:
    db_data = json.load(f)

candidates = raw_data.get('products', [])
existing_products = db_data.get('products', [])

print(f"Raw candidates: {len(candidates)}")
print(f"Existing DB products: {len(existing_products)}")

# === DEDUP ===
now = datetime.now(timezone.utc)
active_cooldowns = set()
for p in existing_products:
    cd = p.get('cooldownExpiresAt', '')
    if cd:
        try:
            cd_dt = datetime.fromisoformat(cd.replace('Z', '+00:00'))
            if cd_dt > now:
                active_cooldowns.add(p.get('id', ''))
        except:
            pass

deduped = [c for c in candidates if c.get('product_id', '') not in active_cooldowns]
print(f"Active cooldowns: {len(active_cooldowns)}")
print(f"After dedup: {len(deduped)}")

# === SELECTED PRODUCTS (5 items) ===
selected = [
    {
        "id": "x.com/vovudebosh/status/2104847341576741192",
        "name": "Jeeva",
        "slug": "jeeva-ai-sales-agent",
        "description": "Jeeva 是一个 AI 驱动的自动化销售平台，能够自动寻找目标客户、发送个性化邮件外联、管理回复并预约会议。用户只需定义理想的客户画像，Jeeva 就能在 10 亿+ 的联系人数据库中精准定位决策人，自动丰富数据点，生成个性化邮件序列，并在邮件/LinkedIn/电话等多渠道触达潜在客户，全程无需人工干预。",
        "url": "https://www.jeeva.ai",
        "homepage": "https://www.jeeva.ai",
        "type": "saas",
        "tags": ["AI销售", "自动化外联", "客户获取", "B2B SaaS"],
        "sourceChannels": ["twitter"],
        "sourceUrl": "https://x.com/vovudebosh/status/2104847341576741192",
        "analysis": {
            "targetAudience": "中小企业销售团队、独立创业者、B2B 销售人员",
            "useCases": ["自动化潜在客户开发与外联", "个性化邮件营销活动管理", "多渠道触达与会议预约", "CRM 数据自动同步"],
            "designIntent": "解决销售团队在客户开发中大量重复性工作的问题，将手动查找线索、写邮件、跟进回复等流程完全自动化，让销售人员专注于成交。",
            "problemSolved": "传统 B2B 销售流程中，销售人员每天花费数小时手动查找线索、填写数据、写跟进邮件，效率极低。Jeeva 通过 AI Agent 将整个销售外链路自动化，将数小时工作缩短至几分钟。",
            "score": 8,
            "scoreReason": "产品切入点精准（B2B 销售自动化），AI 能力与实际业务场景结合紧密，10 亿+ 联系人数据库是核心竞争壁垒。",
            "competitors": [
                {"name": "Instantly.ai", "url": "https://instantly.ai", "comparison": "专注于邮件外联自动化，功能相对单一"},
                {"name": "Apollo.io", "url": "https://apollo.io", "comparison": "侧重联系人数据库，AI 自动化深度不及 Jeeva"}
            ]
        }
    },
    {
        "id": "x.com/randyloop/status/2105577834169483645",
        "name": "Nowdex",
        "slug": "nowdex-ai-usage-tracker",
        "description": "Nowdex 是一款跨 Mac、iPhone 和 iPad 的 AI 工具使用追踪应用，帮助用户集中监控 Codex、Claude Code、Cursor、Grok、Antigravity、Kimi、GLM、MiniMax 等十余种 AI 编码工具的剩余额度、Token 消耗量和重置时间。支持桌面小组件一键查看，所有凭据存储在设备 Keychain 中，确保隐私安全。",
        "url": "https://nowdex.app",
        "homepage": "https://nowdex.app",
        "type": "app",
        "tags": ["AI工具追踪", "额度管理", "macOS", "iOS"],
        "sourceChannels": ["twitter"],
        "sourceUrl": "https://x.com/randyloop/status/2105577834169483645",
        "analysis": {
            "targetAudience": "使用多种 AI 编码工具的开发者、独立黑客、AI 重度用户",
            "useCases": ["集中管理多个 AI 工具的订阅额度", "桌面小组件实时查看剩余 Token", "追踪每日 Token 消耗趋势", "iCloud 同步跨设备共享"],
            "designIntent": "解决开发者在同时订阅多种 AI 工具时面临的额度分散、难以统一管理的问题。将所有 AI 编码工具的使用情况集中在一个菜单栏应用中一目了然。",
            "problemSolved": "现代开发者往往同时使用多种 AI 编码工具，每种工具的额度重置周期各不相同。Nowdex 解决了多工具额度管理混乱的痛点。",
            "score": 7,
            "scoreReason": "精准解决多 AI 工具用户的实际痛点，隐私优先设计（Keychain 存储），macOS/iOS 原生体验好。但目标用户群体相对垂直。",
            "competitors": [
                {"name": "CodeToken", "url": "https://codetoken.ai", "comparison": "类似工具但覆盖的 AI 服务商较少"}
            ]
        }
    },
    {
        "id": "orcah.app",
        "name": "Orcah",
        "slug": "orcah-video-intelligence",
        "description": "Orcah Studio 是一款本地优先的 Mac 视频智能管理工具，能够索引用户整个视频库中的内容——包括语音转录、说话人标注、人脸识别、物体检测、场景描述和相机元数据。用户可以用自然语言搜索视频素材，Orcah 会直接定位到精确帧并一键发送到剪辑时间线。完全在设备本地运行，不上传任何视频到云端。",
        "url": "https://orcah.app",
        "homepage": "https://orcah.app",
        "type": "app",
        "tags": ["视频管理", "AI搜索", "本地优先", "macOS", "创作者工具"],
        "sourceChannels": ["hackernews"],
        "sourceUrl": "https://news.ycombinator.com/item?id=49927561",
        "analysis": {
            "targetAudience": "专业视频创作者、纪录片制作人、影视剪辑师",
            "useCases": ["海量视频素材的自然语言检索", "基于说话人/物体/场景的智能筛选", "GoPro/无人机元数据搜索", "一键发送片段到剪辑软件时间线"],
            "designIntent": "解决专业视频创作者面对海量素材时查找困难的问题。将传统基于文件名和文件夹的管理方式升级为基于内容的 AI 语义搜索。",
            "problemSolved": "视频创作者往往积累数 TB 素材，传统方式只能通过文件名查找特定镜头。Orcah 通过本地 AI 分析将所有视频内容索引化，实现想到即找到的体验。",
            "score": 8,
            "scoreReason": "产品定位精准且技术门槛高，隐私优先设计契合创作者对素材安全的需求。Apple Silicon 优化良好。",
            "competitors": [
                {"name": "Adobe Prelude", "url": "https://www.adobe.com/products/prelude.html", "comparison": "传统素材管理，缺少 AI 语义搜索"}
            ]
        }
    },
    {
        "id": "x.com/githubdaily/status/2105651520557678731",
        "name": "Home_View",
        "slug": "home-view-3d-designer",
        "description": "Home_View 是一款完全在浏览器中运行的开源户型装修设计工具，集成了 2D 平面图绘制和 3D 实时漫游功能。用户可以在 2D 平面上从 60+ 种家具家电中拖拽摆放，支持贴墙自动吸附、非承重墙拆除、毫米级尺寸精度，并可一键切换至 3D 视角进行鸟瞰或第一人称行走漫游。还可模拟不同时段日照效果和夜景灯光。",
        "url": "https://github.com/lohith9/Home_View",
        "homepage": "https://github.com/lohith9/Home_View",
        "type": "website",
        "tags": ["家居设计", "3D可视化", "开源", "浏览器工具", "装修"],
        "sourceChannels": ["twitter"],
        "sourceUrl": "https://x.com/GitHub_Daily/status/2105651520557678731",
        "analysis": {
            "targetAudience": "准备装修的业主、室内设计爱好者、学生",
            "useCases": ["装修前自主规划家具摆放方案", "可视化不同装修风格的 3D 效果", "模拟房间日照和灯光效果", "精确计算材料用量与预算估算"],
            "designIntent": "让没有专业设计背景的普通用户也能在浏览器中轻松完成户型设计和家具摆放，无需安装任何软件。",
            "problemSolved": "传统装修流程中，业主只能依赖设计师效果图预览方案，沟通成本高。Home_View 让业主自主快速尝试多种布局方案。",
            "score": 7,
            "scoreReason": "开源免费降低使用门槛，浏览器内直接运行无需安装，2D/3D 实时同步是核心亮点。但产品仍在早期，缺少专业 CAD 级精确度。",
            "competitors": [
                {"name": "SketchUp Free", "url": "https://app.sketchup.com", "comparison": "专业 3D 建模工具，上手门槛高"},
                {"name": "Planner 5D", "url": "https://planner5d.com", "comparison": "功能更完善但收费"}
            ]
        }
    },
    {
        "id": "x.com/denziideng/status/2105280874325725294",
        "name": "Easel",
        "slug": "easel-social-media-creator",
        "description": "Easel 是由浙江大学 REAL Lab 开源的 AI 社交媒体内容工作台，将热点发现、选题策划、文案创作、视觉生成、视频制作和跨平台发布整合在一个统一的创作流水线中。通过 AI Agent 贯穿完整链路，自动筛选适合账号定位的热点选题，生成文案、海报、配音、字幕，支持小红书、抖音、快手、知乎、B站和微信视频号六大平台的一键发布与效果复盘。",
        "url": "https://zju-real.github.io/Easel/",
        "homepage": "https://zju-real.github.io/Easel/",
        "type": "website",
        "tags": ["社媒运营", "AI创作", "多平台发布", "开源", "内容创作者"],
        "sourceChannels": ["twitter"],
        "sourceUrl": "https://x.com/denziideng/status/2105280874325725294",
        "analysis": {
            "targetAudience": "社交媒体内容创作者、自媒体运营、小型营销团队",
            "useCases": ["自动化热点追踪与选题筛选", "AI 生成多平台适配内容（文案/图片/视频）", "六平台一键发布与统一管理", "基于数据反馈优化内容策略"],
            "designIntent": "解决自媒体创作者在多平台运营中面临的追热点难、做内容慢、跨平台发更累的问题。通过 AI Agent 将整条内容流水线自动化。",
            "problemSolved": "个人创作者在运营多个平台时，每天需要手动追热点、写文案、做图、剪视频、逐个发布，常常熬夜仍难以保持稳定更新。",
            "score": 7,
            "scoreReason": "产品理念创新（AI Agent 贯穿内容全流程），浙大实验室背书。但需要一定技术能力配置，对非技术用户不够友好。",
            "competitors": [
                {"name": "Buffer", "url": "https://buffer.com", "comparison": "多平台发布管理，缺少 AI 内容创作"},
                {"name": "Coze/扣子", "url": "https://coze.cn", "comparison": "字节推出的 AI 创作平台，集成度高但灵活性不如开源"}
            ]
        }
    }
]

print(f"\nSelected {len(selected)} products")

# === SCREENSHOTS ===
def take_screenshot(url, product_id, max_retries=2):
    if not url:
        return None
    safe_id = product_id.replace('/', '_').replace('\\', '_').replace(':', '_')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{safe_id}_{timestamp}.png"
    output_file = os.path.join(ASSETS_DIR, filename)
    
    for attempt in range(max_retries + 1):
        try:
            response = requests.post(WEBSHOT_API, json={'url': url, 'format': 'png', 'mode': 'desktop_viewport'}, timeout=120)
            if response.status_code == 200:
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                size_kb = len(response.content) // 1024
                print(f"  📸 Screenshot: {filename} ({size_kb}KB)")
                return f"assets/screenshots/{filename}"
            elif response.status_code == 429:
                wait = int(response.headers.get('Retry-After', 30))
                print(f"  ⏰ Rate limit (429), waiting {wait}s...")
                time.sleep(wait)
                continue
            else:
                print(f"  ❌ Screenshot failed: HTTP {response.status_code}")
                break
        except Exception as e:
            print(f"  ❌ Screenshot error: {e}")
            break
    return None

def fetch_app_store_screenshots(app_name):
    try:
        response = requests.get('https://itunes.apple.com/search', params={'term': app_name, 'entity': 'software', 'limit': 5}, timeout=10)
        response.raise_for_status()
        results = response.json().get('results', [])
        if not results:
            return None
        app = results[0]
        screenshots = app.get('screenshotUrls', [])
        iphone = [s for s in screenshots if any(x in s for x in ['1242', '1290', '1170', '2688', '2778'])]
        return {
            'name': app.get('trackName', ''),
            'url': app.get('trackViewUrl', ''),
            'screenshots': (iphone or screenshots)[:5],
            'icon': app.get('artworkUrl512') or app.get('artworkUrl100') or ''
        }
    except Exception as e:
        print(f"  ❌ App Store error: {e}")
        return None

print("\n--- Taking screenshots ---")
for product in selected:
    pid = product['id']
    ptype = product['type']
    url = product.get('url', '')
    print(f"\n[{product['name']}] type={ptype}")
    
    result = {'screenshotUrl': None, 'appStoreScreenshots': [], 'appStoreName': None, 'appStoreUrl': None}
    
    if ptype in ['ios_app', 'app']:
        app_info = fetch_app_store_screenshots(product['name'])
        if app_info:
            result['appStoreScreenshots'] = app_info['screenshots']
            result['appStoreName'] = app_info['name']
            result['appStoreUrl'] = app_info['url']
            print(f"  📱 App Store: {len(app_info['screenshots'])} screenshots")
        if url:
            result['screenshotUrl'] = take_screenshot(url, pid)
    elif url:
        result['screenshotUrl'] = take_screenshot(url, pid)
    
    product['screenshotUrl'] = result['screenshotUrl']
    product['appStoreScreenshots'] = result['appStoreScreenshots']
    product['appStoreName'] = result['appStoreName']
    product['appStoreUrl'] = result['appStoreUrl']
    
    time.sleep(3)

# === WRITE REPORT ===
report = {
    "date": TODAY,
    "generatedAt": NOW_ISO,
    "productCount": len(selected),
    "products": [
        {
            "id": p["id"],
            "name": p["name"],
            "slug": p["slug"],
            "description": p["description"],
            "url": p["url"],
            "homepage": p["homepage"],
            "type": p["type"],
            "appStoreName": p.get("appStoreName"),
            "appStoreUrl": p.get("appStoreUrl"),
            "screenshotUrl": p.get("screenshotUrl"),
            "appStoreScreenshots": p.get("appStoreScreenshots", []),
            "tags": p["tags"],
            "sourceChannels": p["sourceChannels"],
            "sourceUrl": p["sourceUrl"],
            "firstSeen": NOW_ISO,
            "analysis": p["analysis"]
        }
        for p in selected
    ]
}

report_path = f"reports/daily/{TODAY}.json"
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(f"\n✅ Report written to {report_path}")

# === UPDATE DATABASE ===
cooldown_at = (datetime.now(timezone.utc) + timedelta(days=COOLDOWN_DAYS)).strftime('%Y-%m-%dT%H:%M:%SZ')
for p in selected:
    existing_products.append({
        "id": p["id"],
        "name": p["name"],
        "slug": p["slug"],
        "description": p["description"],
        "url": p["url"],
        "type": p["type"],
        "tags": p["tags"],
        "metrics": {"featuredInDaily": 1, "featuredInWeekly": 0, "lastFeaturedDate": TODAY},
        "analysis": p["analysis"],
        "addedAt": NOW_ISO,
        "cooldownExpiresAt": cooldown_at,
        "screenshotUrl": p.get("screenshotUrl"),
        "appStoreScreenshots": p.get("appStoreScreenshots", [])
    })

db_data['products'] = existing_products
with open('data/products.json', 'w', encoding='utf-8') as f:
    json.dump(db_data, f, ensure_ascii=False, indent=2)
print(f"✅ Database updated ({len(existing_products)} products)")

# === SUMMARY ===
print(f"\n{'='*50}")
print(f"AI Product Radar Daily Report - {TODAY}")
print(f"{'='*50}")
print(f"Candidates: {len(candidates)} | After dedup: {len(deduped)} | Selected: {len(selected)}")
for i, p in enumerate(selected, 1):
    print(f"{i}. {p['name']} (score: {p['analysis']['score']}) - {', '.join(p['sourceChannels'])}")

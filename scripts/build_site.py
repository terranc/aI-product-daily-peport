#!/usr/bin/env python3
"""
生成静态网站
创建 GitHub Pages 可用的站点
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

BASE_DIR = Path("/Volumes/EXTEND/aI-product-daily-peport")
SITE_DIR = BASE_DIR / "docs"
REPORTS_DIR = BASE_DIR / "reports"
DATA_DIR = BASE_DIR / "data"

def load_products():
    """加载产品数据库"""
    products_file = DATA_DIR / "products.json"
    if products_file.exists():
        with open(products_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"products": []}

def load_daily_reports():
    """加载每日报告"""
    daily_dir = REPORTS_DIR / "daily"
    reports = []

    if daily_dir.exists():
        for json_file in sorted(daily_dir.glob("*.json"), reverse=True):
            with open(json_file, 'r', encoding='utf-8') as f:
                reports.append(json.load(f))

    return reports

def copy_assets():
    """复制静态资源到站点目录"""
    assets_dir = BASE_DIR / "assets"
    site_assets = SITE_DIR / "assets"

    if assets_dir.exists():
        if site_assets.exists():
            shutil.rmtree(site_assets)
        shutil.copytree(assets_dir, site_assets)

def generate_global_css():
    """生成全局样式"""
    css = """/* AI Product Radar - Global Styles */
:root {
  --primary: #6366f1;
  --primary-dark: #4f46e5;
  --secondary: #8b5cf6;
  --background: #0f0f23;
  --surface: #1a1a2e;
  --surface-light: #252542;
  --text: #f1f5f9;
  --text-muted: #94a3b8;
  --border: #334155;
  --success: #22c55e;
  --warning: #f59e0b;
  --danger: #ef4444;
  --radius: 12px;
  --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--background);
  color: var(--text);
  line-height: 1.6;
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Header */
header {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 20px 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

nav a {
  color: var(--text-muted);
  text-decoration: none;
  margin-left: 24px;
  transition: color 0.2s;
}

nav a:hover, nav a.active {
  color: var(--text);
}

/* Main Content */
main {
  padding: 40px 0;
}

.section-header {
  margin-bottom: 32px;
}

.section-header h1 {
  font-size: 2rem;
  margin-bottom: 8px;
  background: linear-gradient(135deg, var(--text), var(--text-muted));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.section-header p {
  color: var(--text-muted);
}

/* Date Tags */
.date-tag {
  display: inline-block;
  background: var(--surface-light);
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  color: var(--primary);
  margin-right: 8px;
  margin-bottom: 8px;
}

/* Product Cards */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 24px;
}

.product-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary);
}

.card-image {
  width: 100%;
  height: 200px;
  background: var(--surface-light);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-placeholder {
  font-size: 3rem;
  opacity: 0.3;
}

.card-content {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.card-score {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: white;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
}

.card-description {
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background: var(--surface-light);
  color: var(--text-muted);
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 0.75rem;
}

.tag.category {
  background: rgba(99, 102, 241, 0.2);
  color: var(--primary);
}

/* Product Detail Page */
.product-detail {
  background: var(--surface);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  overflow: hidden;
}

.detail-header {
  padding: 32px;
  background: linear-gradient(135deg, var(--surface), var(--surface-light));
  border-bottom: 1px solid var(--border);
}

.detail-title {
  font-size: 2.5rem;
  margin-bottom: 8px;
}

.detail-subtitle {
  color: var(--text-muted);
  margin-bottom: 16px;
}

.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: center;
}

.detail-score {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
}

.detail-links {
  display: flex;
  gap: 12px;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-primary {
  background: var(--primary);
  color: white;
}

.btn-primary:hover {
  background: var(--primary-dark);
}

.btn-secondary {
  background: var(--surface-light);
  color: var(--text);
  border: 1px solid var(--border);
}

.btn-secondary:hover {
  background: var(--border);
}

.detail-content {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 32px;
  padding: 32px;
}

@media (max-width: 900px) {
  .detail-content {
    grid-template-columns: 1fr;
  }
}

.detail-main h2 {
  font-size: 1.5rem;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border);
}

.detail-section {
  margin-bottom: 32px;
}

.detail-section p {
  color: var(--text-muted);
  line-height: 1.8;
}

.detail-list {
  list-style: none;
}

.detail-list li {
  padding: 8px 0;
  border-bottom: 1px solid var(--border);
  color: var(--text-muted);
}

.detail-list li:before {
  content: "→";
  color: var(--primary);
  margin-right: 8px;
}

.competitors-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.competitor-item {
  background: var(--surface-light);
  padding: 16px;
  border-radius: 8px;
}

.competitor-name {
  font-weight: 600;
  margin-bottom: 4px;
}

.competitor-name a {
  color: var(--primary);
  text-decoration: none;
}

.competitor-name a:hover {
  text-decoration: underline;
}

.competitor-comparison {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.detail-sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.sidebar-section {
  background: var(--surface-light);
  padding: 20px;
  border-radius: var(--radius);
}

.sidebar-section h3 {
  font-size: 1rem;
  margin-bottom: 16px;
  color: var(--text);
}

.screenshot-gallery {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.screenshot-item {
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--border);
}

.screenshot-item img {
  width: 100%;
  display: block;
}

/* Footer */
footer {
  background: var(--surface);
  border-top: 1px solid var(--border);
  padding: 40px 0;
  margin-top: 60px;
  text-align: center;
  color: var(--text-muted);
}

footer a {
  color: var(--primary);
  text-decoration: none;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-muted);
}

.empty-state-icon {
  font-size: 4rem;
  margin-bottom: 16px;
  opacity: 0.5;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 40px;
}

.pagination a {
  background: var(--surface);
  color: var(--text);
  padding: 10px 16px;
  border-radius: 8px;
  text-decoration: none;
  border: 1px solid var(--border);
  transition: all 0.2s;
}

.pagination a:hover, .pagination a.active {
  background: var(--primary);
  border-color: var(--primary);
}
"""

    css_file = SITE_DIR / "styles.css"
    css_file.parent.mkdir(parents=True, exist_ok=True)
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css)

def generate_index_page(reports):
    """生成首页 - 卡片列表"""

    # 收集所有日期的产品
    all_products = []
    for report in reports:
        date = report.get('date', '')
        for product in report.get('products', []):
            product['date'] = date
            all_products.append(product)

    # 生成产品卡片 HTML
    cards_html = ""
    for product in all_products[:30]:  # 显示最近30个产品
        screenshot = product.get('screenshotUrl', '')
        app_screenshots = product.get('appStoreScreenshots', [])
        image_url = screenshot if screenshot else (app_screenshots[0] if app_screenshots else '')

        image_html = f'<img src="/{image_url}" alt="{product["name"]}" loading="lazy">' if image_url else '<div class="card-placeholder">🤖</div>'

        analysis = product.get('analysis', {})
        score = analysis.get('score', 0)
        tags = product.get('tags', [])[:3]

        tags_html = ''.join([f'<span class="tag">{t}</span>' for t in tags])

        cards_html += f"""
        <a href="/products/{product['slug'].lower()}.html" class="product-card">
          <div class="card-image">
            {image_html}
          </div>
          <div class="card-content">
            <div class="card-header">
              <span class="date-tag">{product['date']}</span>
              <span class="card-score">{score}</span>
            </div>
            <h3 class="card-title">{product['name']}</h3>
            <p class="card-description">{product.get('description', '')[:120]}...</p>
            <div class="card-tags">
              {tags_html}
            </div>
          </div>
        </a>
        """

    # 生成日期筛选标签
    date_tags = ""
    unique_dates = list(dict.fromkeys([r['date'] for r in reports]))[:10]
    for date in unique_dates:
        date_tags += f'<span class="date-tag">{date}</span>'

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Product Radar - 每日AI应用发现</title>
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <header>
    <div class="container">
      <div class="logo">🤖 AI Product Radar</div>
      <nav>
        <a href="/" class="active">每日精选</a>
        <a href="/archive.html">归档</a>
        <a href="https://github.com/terranc/aI-product-daily-peport" target="_blank">GitHub</a>
      </nav>
    </div>
  </header>

  <main>
    <div class="container">
      <div class="section-header">
        <h1>每日AI应用发现</h1>
        <p>追踪最值得关注的AI创新产品，每日精选3个，每周深度分析1个</p>
        <div style="margin-top: 16px;">
          {date_tags}
        </div>
      </div>

      <div class="product-grid">
        {cards_html if cards_html else '<div class="empty-state"><div class="empty-state-icon">📭</div><h2>暂无产品数据</h2><p>运行每日抓取脚本后，这里将显示精选的AI产品</p></div>'}
      </div>
    </div>
  </main>

  <footer>
    <div class="container">
      <p>Generated with 🤖 by AI Product Radar</p>
      <p><a href="https://github.com/terranc/aI-product-daily-peport">View on GitHub</a></p>
    </div>
  </footer>
</body>
</html>
"""

    index_file = SITE_DIR / "index.html"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html)

def generate_product_pages(all_products):
    """生成产品详情页"""
    products_dir = SITE_DIR / "products"
    products_dir.mkdir(parents=True, exist_ok=True)

    for product in all_products:
        analysis = product.get('analysis', {})
        score = analysis.get('score', 0)
        tags = product.get('tags', [])

        tags_html = ''.join([f'<span class="tag category">{t}</span>' for t in tags])

        # 使用场景
        use_cases = analysis.get('useCases', [])
        use_cases_html = ''.join([f'<li>{case}</li>' for case in use_cases])

        # 竞品
        competitors = analysis.get('competitors', [])
        competitors_html = ''
        for comp in competitors:
            competitors_html += f"""
            <div class="competitor-item">
              <div class="competitor-name"><a href="{comp.get('url', '#')}" target="_blank">{comp.get('name', '')}</a></div>
              <div class="competitor-comparison">{comp.get('comparison', '')}</div>
            </div>
            """

        # 截图
        screenshot = product.get('screenshotUrl', '')
        app_screenshots = product.get('appStoreScreenshots', [])

        screenshots_html = '<div class="screenshot-gallery">'
        if screenshot:
            screenshots_html += f'<div class="screenshot-item"><img src="/{screenshot}" alt="{product["name"]} Screenshot"></div>'
        for ss in app_screenshots:
            screenshots_html += f'<div class="screenshot-item"><img src="/{ss}" alt="App Screenshot"></div>'
        screenshots_html += '</div>'

        # 链接
        website_url = product.get('url', '') or product.get('homepage', '')
        website_btn = f'<a href="{website_url}" target="_blank" class="btn btn-primary">🌐 访问官网</a>' if website_url else ''

        appstore_url = product.get('appStoreUrl', '')
        appstore_btn = f'<a href="{appstore_url}" target="_blank" class="btn btn-secondary">📱 App Store</a>' if appstore_url else ''

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{product['name']} - AI Product Radar</title>
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <header>
    <div class="container">
      <a href="/" class="logo">🤖 AI Product Radar</a>
      <nav>
        <a href="/">← 返回首页</a>
      </nav>
    </div>
  </header>

  <main>
    <div class="container">
      <article class="product-detail">
        <div class="detail-header">
          <span class="date-tag">{product.get('date', 'Unknown')}</span>
          <div style="margin-top: 12px;">{tags_html}</div>
          <h1 class="detail-title">{product['name']}</h1>
          <p class="detail-subtitle">{product.get('description', '')}</p>
          <div class="detail-meta">
            <span class="detail-score">评分: {score}/10</span>
            <div class="detail-links">
              {website_btn}
              {appstore_btn}
            </div>
          </div>
        </div>

        <div class="detail-content">
          <div class="detail-main">
            <div class="detail-section">
              <h2>🎯 目标受众</h2>
              <p>{analysis.get('targetAudience', '待分析')}</p>
            </div>

            <div class="detail-section">
              <h2>💡 使用场景</h2>
              <ul class="detail-list">
                {use_cases_html if use_cases_html else '<li>待补充</li>'}
              </ul>
            </div>

            <div class="detail-section">
              <h2>🎨 设计初衷</h2>
              <p>{analysis.get('designIntent', '待分析')}</p>
            </div>

            <div class="detail-section">
              <h2>❓ 解决什么问题</h2>
              <p>{analysis.get('problemSolved', '待分析')}</p>
            </div>

            <div class="detail-section">
              <h2>📊 评分理由</h2>
              <p>{analysis.get('scoreReason', '待分析')}</p>
            </div>

            <div class="detail-section">
              <h2>🆚 对标竞品</h2>
              <div class="competitors-list">
                {competitors_html if competitors_html else '<p>暂无竞品分析</p>'}
              </div>
            </div>
          </div>

          <aside class="detail-sidebar">
            <div class="sidebar-section">
              <h3>📸 产品截图</h3>
              {screenshots_html if (screenshot or app_screenshots) else '<p>暂无截图</p>'}
            </div>

            <div class="sidebar-section">
              <h3>🏷️ 标签</h3>
              <div class="card-tags">
                {tags_html}
              </div>
            </div>

            <div class="sidebar-section">
              <h3>📈 数据来源</h3>
              <p style="color: var(--text-muted); font-size: 0.9rem;">
                首次发现: {product.get('firstSeen', 'Unknown')[:10]}
              </p>
            </div>
          </aside>
        </div>
      </article>
    </div>
  </main>

  <footer>
    <div class="container">
      <p>Generated with 🤖 by AI Product Radar</p>
    </div>
  </footer>
</body>
</html>
"""

        product_file = products_dir / f"{product['slug'].lower()}.html"
        with open(product_file, 'w', encoding='utf-8') as f:
            f.write(html)

def generate_archive_page(reports):
    """生成归档页面"""
    # 按月份分组
    archive_html = ""
    for report in reports[:12]:  # 最近12期
        date = report['date']
        products = report.get('products', [])

        product_links = ""
        for p in products:
            product_links += f'<li><a href="/products/{p["slug"].lower()}.html">{p["name"]}</a> - {p.get("description", "")[:50]}...</li>'

        archive_html += f"""
        <div class="sidebar-section" style="margin-bottom: 24px;">
          <h3>{date}</h3>
          <ul class="detail-list">{product_links if product_links else '<li>暂无数据</li>'}</ul>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>归档 - AI Product Radar</title>
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <header>
    <div class="container">
      <a href="/" class="logo">🤖 AI Product Radar</a>
      <nav>
        <a href="/">每日精选</a>
        <a href="/archive.html" class="active">归档</a>
      </nav>
    </div>
  </header>

  <main>
    <div class="container">
      <div class="section-header">
        <h1>📚 历史归档</h1>
        <p>按日期浏览所有精选产品</p>
      </div>

      <div style="max-width: 800px;">
        {archive_html if archive_html else '<p style="color: var(--text-muted);">暂无历史数据</p>'}
      </div>
    </div>
  </main>

  <footer>
    <div class="container">
      <p>Generated with 🤖 by AI Product Radar</p>
    </div>
  </footer>
</body>
</html>
"""

    archive_file = SITE_DIR / "archive.html"
    with open(archive_file, 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    """主流程"""
    print("🔨 构建静态网站...")

    # 清理旧站点
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True)

    # 1. 复制静态资源
    print("  📁 复制静态资源...")
    copy_assets()

    # 2. 加载数据
    print("  📊 加载产品数据...")
    reports = load_daily_reports()

    if not reports:
        print("  ⚠️ 没有找到报告数据")

    # 3. 生成 CSS
    print("  🎨 生成样式...")
    generate_global_css()

    # 4. 收集所有产品
    all_products = []
    for report in reports:
        for product in report.get('products', []):
            product['date'] = report['date']
            all_products.append(product)

    # 5. 生成页面
    print("  📝 生成首页...")
    generate_index_page(reports)

    print("  📝 生成产品详情页...")
    generate_product_pages(all_products)

    print("  📝 生成归档页...")
    generate_archive_page(reports)

    print(f"\n✅ 网站已生成: {SITE_DIR}")
    print(f"   - 首页: {SITE_DIR}/index.html")
    print(f"   - 产品页: {len(all_products)} 个")

if __name__ == '__main__':
    main()

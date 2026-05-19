#!/usr/bin/env python3
"""
生成静态网站
创建 GitHub Pages 可用的站点（支持子路径部署）
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

BASE_DIR = Path("/Volumes/EXTEND/aI-product-daily-peport")
SITE_DIR = BASE_DIR / "docs"
REPORTS_DIR = BASE_DIR / "reports"
DATA_DIR = BASE_DIR / "data"

# GitHub Pages 子路径 —— 所有资源链接必须带上此前缀
BASE_PATH = "/aI-product-daily-peport"

def p(relative_path):
    """生成带子路径前缀的 URL"""
    if relative_path.startswith('/'):
        return f"{BASE_PATH}{relative_path}"
    return f"{BASE_PATH}/{relative_path}"

def load_products():
    products_file = DATA_DIR / "products.json"
    if products_file.exists():
        with open(products_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"products": []}

def load_daily_reports():
    daily_dir = REPORTS_DIR / "daily"
    reports = []
    if daily_dir.exists():
        for json_file in sorted(daily_dir.glob("*.json"), reverse=True):
            with open(json_file, 'r', encoding='utf-8') as f:
                reports.append(json.load(f))
    return reports

def copy_assets():
    assets_dir = BASE_DIR / "assets"
    site_assets = SITE_DIR / "assets"
    if assets_dir.exists():
        if site_assets.exists():
            shutil.rmtree(site_assets)
        shutil.copytree(assets_dir, site_assets)

def generate_global_css():
    css = r"""/* AI Product Radar - Design System
   Style: Dark Glass Morphism + Gradient Accents
   Inspired by ui-ux-pro-max best practices
*/

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  /* Core palette — deep navy + electric violet */
  --primary: #7c3aed;
  --primary-light: #a78bfa;
  --primary-dark: #5b21b6;
  --secondary: #06b6d4;
  --accent: #f472b6;

  /* Surfaces */
  --bg-base: #0b0f1a;
  --bg-raised: #111827;
  --bg-glass: rgba(17, 24, 39, 0.7);
  --bg-card: rgba(30, 41, 59, 0.5);
  --bg-hover: rgba(124, 58, 237, 0.08);

  /* Text */
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;

  /* Borders & effects */
  --border: rgba(148, 163, 184, 0.12);
  --border-hover: rgba(124, 58, 237, 0.4);
  --glass-blur: 16px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.4);
  --shadow-lg: 0 12px 40px rgba(0,0,0,0.5);
  --shadow-glow: 0 0 30px rgba(124, 58, 237, 0.15);

  /* Radius */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;

  /* Transitions */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --duration: 200ms;
}

*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: var(--bg-base);
  color: var(--text-primary);
  line-height: 1.6;
  min-height: 100vh;
}

/* Subtle animated background gradient */
body::before {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background:
    radial-gradient(ellipse 80% 60% at 10% 20%, rgba(124,58,237,0.08) 0%, transparent 60%),
    radial-gradient(ellipse 60% 50% at 90% 80%, rgba(6,182,212,0.06) 0%, transparent 60%);
  pointer-events: none;
  z-index: 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  position: relative;
  z-index: 1;
}

/* ===== HEADER ===== */
header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--bg-glass);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border-bottom: 1px solid var(--border);
}

header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
}

.logo {
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, var(--primary-light), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  -webkit-text-fill-color: white;
}

nav {
  display: flex;
  align-items: center;
  gap: 8px;
}

nav a {
  color: var(--text-secondary);
  text-decoration: none;
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  font-weight: 500;
  transition: all var(--duration) var(--ease-out);
  cursor: pointer;
}

nav a:hover {
  color: var(--text-primary);
  background: var(--bg-hover);
}

nav a.active {
  color: var(--primary-light);
  background: rgba(124, 58, 237, 0.12);
}

/* ===== HERO / SECTION HEADER ===== */
.hero {
  padding: 60px 0 40px;
  text-align: center;
}

.hero h1 {
  font-size: 2.5rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.2;
  margin-bottom: 12px;
  background: linear-gradient(135deg, var(--text-primary) 0%, var(--primary-light) 50%, var(--secondary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero p {
  color: var(--text-secondary);
  font-size: 1.1rem;
  max-width: 560px;
  margin: 0 auto 24px;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 32px;
  margin-top: 24px;
}

.stat {
  text-align: center;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-light);
}

.stat-label {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Date filter pills */
.filter-bar {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  margin-bottom: 40px;
}

.filter-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.8rem;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--duration) var(--ease-out);
}

.filter-pill:hover, .filter-pill.active {
  background: rgba(124, 58, 237, 0.15);
  border-color: var(--border-hover);
  color: var(--primary-light);
}

/* ===== PRODUCT GRID ===== */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
  padding-bottom: 60px;
}

/* ===== PRODUCT CARD ===== */
.product-card {
  background: var(--bg-card);
  backdrop-filter: blur(8px);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  transition: all var(--duration) var(--ease-out);
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-4px);
  border-color: var(--border-hover);
  box-shadow: var(--shadow-glow);
}

.card-image {
  width: 100%;
  height: 180px;
  background: linear-gradient(135deg, var(--bg-raised), var(--bg-card));
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
}

.card-image::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: linear-gradient(to top, var(--bg-card), transparent);
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-placeholder {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.6;
}

.card-placeholder svg {
  width: 28px;
  height: 28px;
  color: white;
}

.card-content {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.card-date {
  font-size: 0.75rem;
  color: var(--text-muted);
  font-weight: 500;
}

.card-score {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin-bottom: 8px;
  line-height: 1.3;
}

.card-description {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
  line-height: 1.6;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  background: rgba(124, 58, 237, 0.1);
  color: var(--primary-light);
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 0.7rem;
  font-weight: 500;
  border: 1px solid rgba(124, 58, 237, 0.15);
}

.tag.category {
  background: rgba(6, 182, 212, 0.1);
  color: var(--secondary);
  border-color: rgba(6, 182, 212, 0.15);
}

/* ===== PRODUCT DETAIL PAGE ===== */
.detail-back {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 24px;
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  transition: all var(--duration) var(--ease-out);
  cursor: pointer;
}

.detail-back:hover {
  color: var(--text-primary);
  background: var(--bg-hover);
}

.product-detail {
  background: var(--bg-card);
  backdrop-filter: blur(8px);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  overflow: hidden;
}

.detail-header {
  padding: 40px;
  background: linear-gradient(135deg, rgba(124,58,237,0.06), rgba(6,182,212,0.04));
  border-bottom: 1px solid var(--border);
}

.detail-header .card-meta {
  margin-bottom: 16px;
}

.detail-title {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  margin-bottom: 12px;
  line-height: 1.2;
}

.detail-subtitle {
  color: var(--text-secondary);
  font-size: 1rem;
  margin-bottom: 24px;
  line-height: 1.7;
  max-width: 700px;
}

.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: center;
}

.detail-score {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  padding: 8px 18px;
  border-radius: var(--radius-sm);
  font-weight: 700;
  font-size: 0.95rem;
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
  border-radius: var(--radius-sm);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all var(--duration) var(--ease-out);
  cursor: pointer;
  border: none;
}

.btn svg {
  width: 16px;
  height: 16px;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
}

.btn-primary:hover {
  box-shadow: var(--shadow-glow);
  transform: translateY(-1px);
}

.btn-secondary {
  background: var(--bg-raised);
  color: var(--text-primary);
  border: 1px solid var(--border);
}

.btn-secondary:hover {
  border-color: var(--border-hover);
  background: var(--bg-hover);
}

.detail-body {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 0;
}

.detail-main {
  padding: 40px;
  border-right: 1px solid var(--border);
}

.detail-section {
  margin-bottom: 36px;
}

.detail-section:last-child {
  margin-bottom: 0;
}

.detail-section h2 {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  letter-spacing: -0.01em;
}

.detail-section h2 .icon {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}

.detail-section h2 .icon.purple { background: rgba(124,58,237,0.15); }
.detail-section h2 .icon.cyan   { background: rgba(6,182,212,0.15); }
.detail-section h2 .icon.pink   { background: rgba(244,114,182,0.15); }
.detail-section h2 .icon.amber  { background: rgba(245,158,11,0.15); }
.detail-section h2 .icon.green  { background: rgba(34,197,94,0.15); }

.detail-section p {
  color: var(--text-secondary);
  line-height: 1.8;
  font-size: 0.95rem;
}

.detail-list {
  list-style: none;
}

.detail-list li {
  padding: 10px 0;
  border-bottom: 1px solid var(--border);
  color: var(--text-secondary);
  font-size: 0.95rem;
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.detail-list li:last-child {
  border-bottom: none;
}

.detail-list li::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--primary);
  flex-shrink: 0;
  margin-top: 8px;
}

.competitors-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.competitor-item {
  background: var(--bg-raised);
  padding: 16px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
}

.competitor-name {
  font-weight: 600;
  margin-bottom: 4px;
  font-size: 0.95rem;
}

.competitor-name a {
  color: var(--primary-light);
  text-decoration: none;
  transition: color var(--duration);
  cursor: pointer;
}

.competitor-name a:hover {
  color: var(--secondary);
}

.competitor-comparison {
  color: var(--text-muted);
  font-size: 0.85rem;
  line-height: 1.6;
}

/* Sidebar */
.detail-sidebar {
  padding: 40px 32px;
  display: flex;
  flex-direction: column;
  gap: 28px;
  background: rgba(0,0,0,0.15);
}

.sidebar-block h3 {
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  margin-bottom: 14px;
}

.screenshot-gallery {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.screenshot-item {
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--border);
}

.screenshot-item img {
  width: 100%;
  display: block;
}

.sidebar-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.sidebar-meta-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.875rem;
}

.sidebar-meta-item:last-child {
  border-bottom: none;
}

.sidebar-meta-item .label {
  color: var(--text-muted);
}

.sidebar-meta-item .value {
  color: var(--text-secondary);
  font-weight: 500;
}

/* ===== FOOTER ===== */
footer {
  background: var(--bg-glass);
  backdrop-filter: blur(var(--glass-blur));
  border-top: 1px solid var(--border);
  padding: 32px 0;
  text-align: center;
  color: var(--text-muted);
  font-size: 0.8rem;
  margin-top: 0;
}

footer a {
  color: var(--primary-light);
  text-decoration: none;
  transition: color var(--duration);
  cursor: pointer;
}

footer a:hover {
  color: var(--secondary);
}

footer .footer-links {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-bottom: 12px;
}

/* ===== EMPTY STATE ===== */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-muted);
}

.empty-state-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  border-radius: 50%;
  background: var(--bg-card);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border);
}

.empty-state-icon svg {
  width: 28px;
  height: 28px;
  color: var(--text-muted);
}

.empty-state h2 {
  font-size: 1.25rem;
  margin-bottom: 8px;
  color: var(--text-secondary);
}

/* ===== BLOG-STYLE DAILY POSTS ===== */
.blog-feed {
  max-width: 800px;
  margin: 0 auto;
  padding-bottom: 60px;
}

.blog-post {
  margin-bottom: 48px;
  padding-bottom: 48px;
  border-bottom: 1px solid var(--border);
}

.blog-post:last-child {
  border-bottom: none;
}

.blog-post-header {
  margin-bottom: 28px;
}

.blog-post-date {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 8px;
}

.blog-post-title {
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  line-height: 1.3;
}

.blog-product-entry {
  display: flex;
  gap: 20px;
  padding: 20px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  margin-bottom: 16px;
  text-decoration: none;
  color: inherit;
  transition: all var(--duration) var(--ease-out);
  cursor: pointer;
}

.blog-product-entry:hover {
  border-color: var(--border-hover);
  background: var(--bg-hover);
  transform: translateX(4px);
}

.blog-product-thumb {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-sm);
  background: var(--bg-raised);
  flex-shrink: 0;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.blog-product-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.blog-product-thumb .thumb-placeholder {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  opacity: 0.5;
}

.blog-product-body {
  flex: 1;
  min-width: 0;
}

.blog-product-name {
  font-size: 1.05rem;
  font-weight: 700;
  margin-bottom: 6px;
  color: var(--text-primary);
}

.blog-product-desc {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.blog-product-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.blog-product-score {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--primary-light);
  background: rgba(124,58,237,0.12);
  padding: 2px 8px;
  border-radius: 4px;
}

.blog-product-tags {
  display: flex;
  gap: 4px;
}

.blog-product-tags .tag {
  font-size: 0.65rem;
  padding: 2px 8px;
}

.post-count {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-weight: 400;
}

/* ===== ARCHIVE TABLE ===== */
.archive-table {
  width: 100%;
  border-collapse: collapse;
}

.archive-table th {
  text-align: left;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
}

.archive-table td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
  font-size: 0.9rem;
  vertical-align: top;
}

.archive-table tr:hover td {
  background: var(--bg-hover);
}

.archive-table .date-cell {
  white-space: nowrap;
  font-weight: 600;
  color: var(--primary-light);
  width: 120px;
}

.archive-table .products-cell {
  color: var(--text-secondary);
  line-height: 1.7;
}

.archive-table .products-cell a {
  color: var(--text-primary);
  text-decoration: none;
  font-weight: 500;
  transition: color var(--duration);
  cursor: pointer;
}

.archive-table .products-cell a:hover {
  color: var(--primary-light);
}

.archive-table .count-cell {
  width: 60px;
  text-align: center;
  color: var(--text-muted);
  font-weight: 600;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 900px) {
  .detail-body {
    grid-template-columns: 1fr;
  }
  .detail-main {
    border-right: none;
    border-bottom: 1px solid var(--border);
    padding: 24px;
  }
  .detail-sidebar {
    padding: 24px;
  }
  .product-grid {
    grid-template-columns: 1fr;
  }
  .hero h1 {
    font-size: 1.75rem;
  }
  .detail-header {
    padding: 24px;
  }
  .detail-title {
    font-size: 1.5rem;
  }
  .blog-feed {
    padding: 0 8px;
  }
  .blog-product-entry {
    gap: 14px;
  }
  .blog-product-thumb {
    width: 64px;
    height: 64px;
  }
  .blog-post-title {
    font-size: 1.25rem;
  }
  .archive-table .date-cell {
    width: 100px;
  }
  .archive-table td {
    padding: 12px;
    font-size: 0.85rem;
  }
}

@media (max-width: 480px) {
  header .container {
    flex-direction: column;
    height: auto;
    padding: 12px 16px;
    gap: 8px;
  }
  nav {
    width: 100%;
    justify-content: center;
  }
  .hero {
    padding: 32px 0 24px;
  }
  .container {
    padding: 0 16px;
  }
  .blog-product-entry {
    flex-direction: column;
    gap: 12px;
  }
  .blog-product-thumb {
    width: 100%;
    height: 140px;
  }
  .blog-post {
    margin-bottom: 32px;
    padding-bottom: 32px;
  }
  .archive-table {
    font-size: 0.8rem;
  }
  .archive-table .date-cell {
    width: 80px;
    font-size: 0.75rem;
  }
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--text-muted);
}
"""

    css_file = SITE_DIR / "styles.css"
    css_file.parent.mkdir(parents=True, exist_ok=True)
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css)

def svg_icon(name):
    """返回内联 SVG 图标"""
    icons = {
        'radar': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 0 20"/><path d="M12 2a6 6 0 0 1 0 12"/><circle cx="12" cy="8" r="1" fill="currentColor"/></svg>',
        'arrow-left': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg>',
        'external': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>',
        'smartphone': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>',
        'target': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
        'bulb': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/></svg>',
        'palette': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="13.5" cy="6.5" r="0.5" fill="currentColor"/><circle cx="17.5" cy="10.5" r="0.5" fill="currentColor"/><circle cx="8.5" cy="7.5" r="0.5" fill="currentColor"/><circle cx="6.5" cy="12.5" r="0.5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg>',
        'zap': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
        'bar-chart': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg>',
        'swords': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="14.5 17.5 3 6 3 3 6 3 17.5 14.5"/><line x1="13" y1="19" x2="19" y2="13"/><line x1="16" y1="16" x2="20" y2="20"/><line x1="19" y1="21" x2="21" y2="19"/><polyline points="14.5 6.5 18 3 21 3 21 6 17.5 9.5"/><line x1="5" y1="14" x2="9" y2="18"/><line x1="7" y1="17" x2="4" y2="20"/><line x1="3" y1="19" x2="5" y2="21"/></svg>',
        'inbox': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>',
        'github': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>',
        'calendar': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
        'trending': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
        'database': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>',
    }
    return icons.get(name, '')

def generate_index_page(reports):
    """生成首页 - 博客风格，每天一篇，只显示最近14天"""
    recent_reports = reports[:14]

    posts_html = ""
    for report in recent_reports:
        date = report.get('date', '')
        products = report.get('products', [])
        count = len(products)

        # 中文星期
        try:
            dt = datetime.strptime(date, '%Y-%m-%d')
            weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            weekday = weekdays[dt.weekday()]
            date_display = f"{date} {weekday}"
        except:
            date_display = date

        entries_html = ""
        for product in products:
            analysis = product.get('analysis', {})
            score = analysis.get('score', 0)
            tags = product.get('tags', [])[:3]
            tags_html = ''.join([f'<span class="tag">{t}</span>' for t in tags])

            screenshot = product.get('screenshotUrl', '')
            app_screenshots = product.get('appStoreScreenshots', [])
            image_url = screenshot if screenshot else (app_screenshots[0] if app_screenshots else '')

            if image_url:
                thumb_html = f'<img src="{p("/" + image_url)}" alt="{product["name"]}" loading="lazy">'
            else:
                thumb_html = '<div class="thumb-placeholder"></div>'

            entries_html += f"""
        <a href="{p("/products/" + product['slug'].lower() + ".html")}" class="blog-product-entry">
          <div class="blog-product-thumb">{thumb_html}</div>
          <div class="blog-product-body">
            <div class="blog-product-name">{product['name']}</div>
            <p class="blog-product-desc">{product.get('description', '')[:150]}</p>
            <div class="blog-product-meta">
              <span class="blog-product-score">{score}/10</span>
              <div class="blog-product-tags">{tags_html}</div>
            </div>
          </div>
        </a>"""

        posts_html += f"""
      <article class="blog-post">
        <div class="blog-post-header">
          <div class="blog-post-date">{date_display}</div>
          <h2 class="blog-post-title">今日精选 <span class="post-count">({count} 个产品)</span></h2>
        </div>
        {entries_html}
      </article>"""

    total = len([p for r in reports for p in r.get('products', [])])
    total_days = len(reports)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI 产品雷达 - 每日 AI 应用发现</title>
  <link rel="stylesheet" href="{p("/styles.css")}">
</head>
<body>
  <header>
    <div class="container">
      <a href="{p("/")}" class="logo">
        <span class="logo-icon">{svg_icon("radar")}</span>
        AI 产品雷达
      </a>
      <nav>
        <a href="{p("/")}" class="active">每日精选</a>
        <a href="{p("/archive.html")}">归档</a>
        <a href="https://github.com/terranc/aI-product-daily-peport" target="_blank">GitHub</a>
      </nav>
    </div>
  </header>

  <main>
    <div class="container">
      <div class="hero">
        <h1>每日 AI 应用发现</h1>
        <p>追踪最值得关注的 AI 创新产品，每日精选 3 个，每周深度分析 1 个</p>
        <div class="hero-stats">
          <div class="stat">
            <div class="stat-value">{total}</div>
            <div class="stat-label">已收录</div>
          </div>
          <div class="stat">
            <div class="stat-value">{total_days}</div>
            <div class="stat-label">期数</div>
          </div>
        </div>
      </div>

      <div class="blog-feed">
        {posts_html if posts_html else f'''<div class="empty-state">
          <div class="empty-state-icon">{svg_icon("inbox")}</div>
          <h2>暂无产品数据</h2>
          <p>运行每日抓取脚本后，这里将显示精选的 AI 产品</p>
        </div>'''}
      </div>
    </div>
  </main>

  <footer>
    <div class="container">
      <div class="footer-links">
        <a href="{p("/archive.html")}">历史归档</a>
        <a href="https://github.com/terranc/aI-product-daily-peport" target="_blank">GitHub</a>
      </div>
      <p>AI 产品雷达 &mdash; 自动化 AI 产品发现与分析</p>
    </div>
  </footer>
</body>
</html>"""

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

        use_cases = analysis.get('useCases', [])
        use_cases_html = ''.join([f'<li>{case}</li>' for case in use_cases])

        competitors = analysis.get('competitors', [])
        competitors_html = ''
        for comp in competitors:
            competitors_html += f"""
            <div class="competitor-item">
              <div class="competitor-name"><a href="{comp.get('url', '#')}" target="_blank">{comp.get('name', '')}</a></div>
              <div class="competitor-comparison">{comp.get('comparison', '')}</div>
            </div>"""

        screenshot = product.get('screenshotUrl', '')
        app_screenshots = product.get('appStoreScreenshots', [])

        screenshots_html = '<div class="screenshot-gallery">'
        if screenshot:
            screenshots_html += f'<div class="screenshot-item"><img src="{p("/" + screenshot)}" alt="{product["name"]}"></div>'
        for ss in app_screenshots:
            screenshots_html += f'<div class="screenshot-item"><img src="{p("/" + ss)}" alt="App Screenshot"></div>'
        screenshots_html += '</div>'

        website_url = product.get('url', '') or product.get('homepage', '')
        website_btn = f'<a href="{website_url}" target="_blank" class="btn btn-primary">{svg_icon("external")} 访问官网</a>' if website_url else ''

        appstore_url = product.get('appStoreUrl', '')
        appstore_btn = f'<a href="{appstore_url}" target="_blank" class="btn btn-secondary">{svg_icon("smartphone")} App Store</a>' if appstore_url else ''

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{product['name']} - AI 产品雷达</title>
  <link rel="stylesheet" href="{p("/styles.css")}">
</head>
<body>
  <header>
    <div class="container">
      <a href="{p("/")}" class="logo">
        <span class="logo-icon">{svg_icon("radar")}</span>
        AI 产品雷达
      </a>
      <nav>
        <a href="{p("/")}">每日精选</a>
        <a href="{p("/archive.html")}">归档</a>
        <a href="https://github.com/terranc/aI-product-daily-peport" target="_blank">GitHub</a>
      </nav>
    </div>
  </header>

  <main>
    <div class="container">
      <a href="{p("/")}" class="detail-back">{svg_icon("arrow-left")} 返回首页</a>

      <article class="product-detail">
        <div class="detail-header">
          <div class="card-meta">
            <span class="card-date">{product.get('date', 'Unknown')}</span>
            <div class="card-tags" style="display:flex;gap:6px;">{tags_html}</div>
          </div>
          <h1 class="detail-title">{product['name']}</h1>
          <p class="detail-subtitle">{product.get('description', '')}</p>
          <div class="detail-meta">
            <span class="detail-score">{svg_icon("bar-chart")} 评分 {score}/10</span>
            <div class="detail-links">
              {website_btn}
              {appstore_btn}
            </div>
          </div>
        </div>

        <div class="detail-body">
          <div class="detail-main">
            <div class="detail-section">
              <h2><span class="icon purple">{svg_icon("target")}</span> 目标受众</h2>
              <p>{analysis.get('targetAudience', '待分析')}</p>
            </div>

            <div class="detail-section">
              <h2><span class="icon cyan">{svg_icon("bulb")}</span> 使用场景</h2>
              <ul class="detail-list">
                {use_cases_html if use_cases_html else '<li>待补充</li>'}
              </ul>
            </div>

            <div class="detail-section">
              <h2><span class="icon pink">{svg_icon("palette")}</span> 设计初衷</h2>
              <p>{analysis.get('designIntent', '待分析')}</p>
            </div>

            <div class="detail-section">
              <h2><span class="icon amber">{svg_icon("zap")}</span> 解决什么问题</h2>
              <p>{analysis.get('problemSolved', '待分析')}</p>
            </div>

            <div class="detail-section">
              <h2><span class="icon green">{svg_icon("trending")}</span> 评分理由</h2>
              <p>{analysis.get('scoreReason', '待分析')}</p>
            </div>

            <div class="detail-section">
              <h2><span class="icon purple">{svg_icon("swords")}</span> 对标竞品</h2>
              <div class="competitors-list">
                {competitors_html if competitors_html else '<p style="color:var(--text-muted)">暂无竞品分析</p>'}
              </div>
            </div>
          </div>

          <aside class="detail-sidebar">
            <div class="sidebar-block">
              <h3>产品截图</h3>
              {screenshots_html if (screenshot or app_screenshots) else '<p style="color:var(--text-muted);font-size:0.875rem;">暂无截图</p>'}
            </div>

            <div class="sidebar-block">
              <h3>标签</h3>
              <div class="sidebar-tags">{tags_html}</div>
            </div>

            <div class="sidebar-block">
              <h3>元数据</h3>
              <div class="sidebar-meta-item">
                <span class="label">首次发现</span>
                <span class="value">{product.get('firstSeen', 'Unknown')[:10]}</span>
              </div>
              <div class="sidebar-meta-item">
                <span class="label">来源渠道</span>
                <span class="value">{', '.join(product.get('sourceChannels', []))}</span>
              </div>
              <div class="sidebar-meta-item">
                <span class="label">产品类型</span>
                <span class="value">{product.get('type', 'unknown')}</span>
              </div>
            </div>
          </aside>
        </div>
      </article>
    </div>
  </main>

  <footer>
    <div class="container">
      <div class="footer-links">
        <a href="{p("/")}">返回首页</a>
        <a href="https://github.com/terranc/aI-product-daily-peport" target="_blank">GitHub</a>
      </div>
      <p>AI 产品雷达</p>
    </div>
  </footer>
</body>
</html>"""

        product_file = products_dir / f"{product['slug'].lower()}.html"
        with open(product_file, 'w', encoding='utf-8') as f:
            f.write(html)

def generate_archive_page(reports):
    """生成归档页面 - 表格形式，每行显示日期和当天产品"""
    rows_html = ""
    for report in reports:
        date = report['date']
        products = report.get('products', [])
        count = len(products)

        # 产品名称列表，用中文逗号分隔
        product_links = []
        for prd in products:
            name = prd['name']
            link = p("/products/" + prd['slug'].lower() + ".html")
            product_links.append(f'<a href="{link}">{name}</a>')

        products_str = '、'.join(product_links) if product_links else '<span style="color:var(--text-muted)">暂无</span>'

        rows_html += f"""
        <tr>
          <td class="date-cell">{date}</td>
          <td class="products-cell">{products_str}</td>
          <td class="count-cell">{count}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>历史归档 - AI 产品雷达</title>
  <link rel="stylesheet" href="{p("/styles.css")}">
</head>
<body>
  <header>
    <div class="container">
      <a href="{p("/")}" class="logo">
        <span class="logo-icon">{svg_icon("radar")}</span>
        AI 产品雷达
      </a>
      <nav>
        <a href="{p("/")}">每日精选</a>
        <a href="{p("/archive.html")}" class="active">归档</a>
        <a href="https://github.com/terranc/aI-product-daily-peport" target="_blank">GitHub</a>
      </nav>
    </div>
  </header>

  <main>
    <div class="container">
      <div class="hero" style="padding-bottom:24px;">
        <h1 style="font-size:2rem;">历史归档</h1>
        <p>按日期浏览所有精选产品，共 {len(reports)} 期</p>
      </div>

      <div style="max-width:900px; margin:0 auto; padding-bottom:60px; background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-lg); overflow:hidden;">
        {f'''<table class="archive-table">
          <thead>
            <tr>
              <th>日期</th>
              <th>精选产品</th>
              <th>数量</th>
            </tr>
          </thead>
          <tbody>
            {rows_html}
          </tbody>
        </table>''' if rows_html else '<p style="color:var(--text-muted);text-align:center;padding:60px 20px;">暂无历史数据</p>'}
      </div>
    </div>
  </main>

  <footer>
    <div class="container">
      <div class="footer-links">
        <a href="{p("/")}">返回首页</a>
        <a href="https://github.com/terranc/aI-product-daily-peport" target="_blank">GitHub</a>
      </div>
      <p>AI 产品雷达</p>
    </div>
  </footer>
</body>
</html>"""

    archive_file = SITE_DIR / "archive.html"
    with open(archive_file, 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    print("🔨 构建静态网站...")

    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True)

    print("  📁 复制静态资源...")
    copy_assets()

    print("  📊 加载产品数据...")
    reports = load_daily_reports()

    if not reports:
        print("  ⚠️ 没有找到报告数据")

    print("  🎨 生成样式...")
    generate_global_css()

    all_products = []
    for report in reports:
        for product in report.get('products', []):
            product['date'] = report['date']
            all_products.append(product)

    print("  📝 生成首页...")
    generate_index_page(reports)

    print("  📝 生成产品详情页...")
    generate_product_pages(all_products)

    print("  📝 生成归档页...")
    generate_archive_page(reports)

    print(f"\n✅ 网站已生成: {SITE_DIR}")
    print(f"   - 首页: {SITE_DIR}/index.html")
    print(f"   - 产品页: {len(all_products)} 个")
    print(f"   - 子路径: {BASE_PATH}")

if __name__ == '__main__':
    main()

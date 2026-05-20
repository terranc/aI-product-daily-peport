#!/usr/bin/env python3
"""
AI 产品雷达 — 静态网站生成器
浅色系设计，博客风格首页，表格归档
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

BASE_DIR = Path("/Volumes/EXTEND/aI-product-daily-peport")
SITE_DIR = BASE_DIR / "docs"
REPORTS_DIR = BASE_DIR / "reports"
DATA_DIR = BASE_DIR / "data"
BASE_PATH = "/aI-product-daily-peport"


def rel(path, depth=0):
    """生成相对路径。depth=0 表示根目录页面，1 表示 products/ 子目录"""
    prefix = '../' * depth
    clean = path.lstrip('/')
    return f"{prefix}{clean}"


def home_href(depth=0):
    """生成首页目录链接，避免在导航里暴露 index.html。"""
    return '../' * depth if depth else './'


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


def load_weekly_reports():
    weekly_dir = REPORTS_DIR / "weekly"
    reports = []
    if weekly_dir.exists():
        for json_file in sorted(weekly_dir.glob("*.json"), reverse=True):
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


# ─── SVG Icons ────────────────────────────────────────────────────────

def icon(name):
    icons = {
        'radar': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 0 20"/><path d="M12 2a6 6 0 0 1 0 12"/><circle cx="12" cy="8" r="1" fill="currentColor"/></svg>',
        'arrow': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg>',
        'external': '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>',
        'phone': '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>',
        'target': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
        'bulb': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/></svg>',
        'palette': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg>',
        'zap': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
        'chart': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
        'swords': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="14.5 17.5 3 6 3 3 6 3 17.5 14.5"/><line x1="13" y1="19" x2="19" y2="13"/><line x1="16" y1="16" x2="20" y2="20"/><line x1="19" y1="21" x2="21" y2="19"/><polyline points="14.5 6.5 18 3 21 3 21 6 17.5 9.5"/><line x1="5" y1="14" x2="9" y2="18"/><line x1="7" y1="17" x2="4" y2="20"/><line x1="3" y1="19" x2="5" y2="21"/></svg>',
        'inbox': '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>',
        'github': '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>',
    }
    return icons.get(name, '')


# ─── CSS ──────────────────────────────────────────────────────────────

def generate_css():
    css = r"""@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

:root {
  --c-bg:       #f8f9fb;
  --c-surface:  #ffffff;
  --c-border:   #e5e7eb;
  --c-border-l: #f0f1f3;
  --c-text:     #111827;
  --c-text-2:   #4b5563;
  --c-text-3:   #9ca3af;
  --c-accent:   #4f46e5;
  --c-accent-l: #eef2ff;
  --c-accent-d: #3730a3;
  --c-tag-bg:   #f3f4f6;
  --c-green:    #059669;
  --c-amber:    #d97706;
  --shadow-sm:  0 1px 2px rgba(0,0,0,.04);
  --shadow-md:  0 2px 8px rgba(0,0,0,.06);
  --shadow-lg:  0 8px 24px rgba(0,0,0,.08);
  --radius:     8px;
  --radius-lg:  12px;
  --ease:       cubic-bezier(.16,1,.3,1);
}

*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }

html { scroll-behavior:smooth; -webkit-font-smoothing:antialiased; }

body {
  font-family: 'Noto Sans SC', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--c-bg);
  color: var(--c-text);
  line-height: 1.7;
  font-size: 15px;
}

a { color: inherit; text-decoration: none; }
img { display:block; max-width:100%; }

/* ─── Layout ─── */
.container { max-width:1120px; margin:0 auto; padding:0 24px; }
.container-wide { max-width:1120px; margin:0 auto; padding:0 24px; }

/* ─── Header ─── */
.site-header {
  position:sticky; top:0; z-index:50;
  background:rgba(255,255,255,.85);
  backdrop-filter:blur(12px);
  border-bottom:1px solid var(--c-border);
}
.site-header .container-wide {
  display:flex; align-items:center; justify-content:space-between;
  height:56px;
}
.site-logo {
  display:flex; align-items:center; gap:8px;
  font-weight:700; font-size:1rem; color:var(--c-text);
}
.site-logo svg { color:var(--c-accent); }
.site-nav { display:flex; gap:4px; }
.site-nav a {
  padding:6px 14px; border-radius:6px; font-size:.875rem;
  font-weight:500; color:var(--c-text-2);
  transition:all .15s var(--ease);
}
.site-nav a:hover { color:var(--c-text); background:var(--c-accent-l); }
.site-nav a.active { color:var(--c-accent); background:var(--c-accent-l); }

/* ─── Hero ─── */
.hero {
  padding:48px 0 40px;
  border-bottom:1px solid var(--c-border);
  margin-bottom:40px;
}
.hero h1 {
  font-size:clamp(1.75rem,4vw,2.25rem);
  font-weight:700; letter-spacing:-.02em;
  line-height:1.25; margin-bottom:8px;
}
.hero p { color:var(--c-text-2); font-size:1rem; margin-bottom:20px; }
.hero-stats {
  display:flex; gap:24px;
}
.hero-stat { display:flex; align-items:baseline; gap:6px; }
.hero-stat strong { font-size:1.25rem; font-weight:700; color:var(--c-accent); }
.hero-stat span { font-size:.8rem; color:var(--c-text-3); }

/* ─── Blog Feed ─── */
.blog-feed { padding-bottom:60px; }

.blog-post {
  margin-bottom:48px;
  padding-bottom:40px;
  border-bottom:1px solid var(--c-border-l);
}
.blog-post:last-child { border-bottom:none; margin-bottom:0; }

.blog-post-header { margin-bottom:24px; }
.blog-post-date {
  font-size:.75rem; font-weight:600; color:var(--c-text-3);
  text-transform:uppercase; letter-spacing:.06em;
  margin-bottom:4px;
}
.blog-post-title {
  font-size:1.25rem; font-weight:700; color:var(--c-text);
}
.blog-post-title .count {
  font-weight:400; color:var(--c-text-3); font-size:.9rem;
}

/* ─── Product Entry (blog item) ─── */
.product-entry {
  display:flex; gap:16px; padding:16px;
  background:var(--c-surface);
  border:1px solid var(--c-border);
  border-radius:var(--radius);
  margin-bottom:12px;
  transition:all .2s var(--ease);
  cursor:pointer;
}
.product-entry:hover {
  border-color:var(--c-accent);
  box-shadow:var(--shadow-md);
  transform:translateY(-1px);
}
.product-entry:last-child { margin-bottom:0; }

.entry-thumb {
  width:72px; height:72px; flex-shrink:0;
  border-radius:6px; overflow:hidden;
  background:var(--c-tag-bg);
  display:flex; align-items:center; justify-content:center;
}
.entry-thumb img { width:100%; height:100%; object-fit:cover; }
.entry-thumb .ph {
  width:32px; height:32px; border-radius:6px;
  background:linear-gradient(135deg,var(--c-accent),#818cf8);
  opacity:.3;
}

.entry-body { flex:1; min-width:0; }
.entry-name {
  font-size:.95rem; font-weight:600; margin-bottom:4px;
  color:var(--c-text); line-height:1.4;
}
.entry-desc {
  font-size:.8rem; color:var(--c-text-2); line-height:1.6;
  margin-bottom:8px;
  display:-webkit-box; -webkit-line-clamp:2;
  -webkit-box-orient:vertical; overflow:hidden;
}
.entry-meta { display:flex; align-items:center; gap:8px; flex-wrap:wrap; }
.entry-score {
  font-size:1.1rem; font-weight:800; color:var(--c-accent);
  min-width:28px; text-align:center;
}
.entry-tags { display:flex; gap:4px; }
.tag {
  font-size:.65rem; padding:2px 7px; border-radius:4px;
  background:var(--c-tag-bg); color:var(--c-text-3);
  font-weight:500;
}

/* ─── Product Detail ─── */
.back-link {
  display:inline-flex; align-items:center; gap:6px;
  font-size:.85rem; font-weight:500; color:var(--c-text-3);
  padding:8px 0; margin-bottom:20px;
  transition:color .15s;
}
.back-link:hover { color:var(--c-accent); }

.detail-card {
  background:var(--c-surface);
  border:1px solid var(--c-border);
  border-radius:var(--radius-lg);
  overflow:hidden;
}
.detail-hero {
  padding:32px;
  border-bottom:1px solid var(--c-border);
}
.detail-hero .entry-meta { margin-bottom:16px; }
.detail-title {
  font-size:1.75rem; font-weight:700;
  letter-spacing:-.02em; line-height:1.3; margin-bottom:8px;
}
.detail-subtitle {
  color:var(--c-text-2); font-size:.95rem;
  line-height:1.7; margin-bottom:20px;
}
.detail-actions { display:flex; gap:12px; align-items:center; flex-wrap:wrap; }
.detail-score-badge {
  font-size:2rem; font-weight:800; color:var(--c-accent);
  line-height:1;
}
.btn {
  display:inline-flex; align-items:center; gap:6px;
  padding:8px 16px; border-radius:6px;
  font-weight:600; font-size:.85rem;
  transition:all .15s var(--ease);
  cursor:pointer; border:none;
}
.btn-primary { background:var(--c-accent-l); color:var(--c-accent); }
.btn-primary:hover { background:var(--c-accent); color:#fff; }
.btn-ghost { background:transparent; color:var(--c-text-2); border:1px solid var(--c-border); }
.btn-ghost:hover { border-color:var(--c-accent); color:var(--c-accent); }

.detail-body {
  display:grid; grid-template-columns:1fr 300px;
}
.detail-main { padding:32px; }
.detail-aside {
  padding:32px 24px;
  background:var(--c-bg);
  border-left:1px solid var(--c-border);
}

.section { margin-bottom:32px; }
.section:last-child { margin-bottom:0; }
.section-title {
  display:flex; align-items:center; gap:8px;
  font-size:.95rem; font-weight:600; margin-bottom:12px;
  color:var(--c-text);
}
.section-title .ic {
  width:28px; height:28px; border-radius:6px;
  display:flex; align-items:center; justify-content:center;
  background:var(--c-accent-l); color:var(--c-accent);
  flex-shrink:0;
}
.section p { color:var(--c-text-2); line-height:1.8; font-size:.9rem; }

.use-case-list { list-style:none; }
.use-case-list li {
  padding:8px 0; border-bottom:1px solid var(--c-border-l);
  color:var(--c-text-2); font-size:.9rem;
  display:flex; align-items:flex-start; gap:8px;
}
.use-case-list li:last-child { border-bottom:none; }
.use-case-list li::before {
  content:''; width:5px; height:5px; border-radius:50%;
  background:var(--c-accent); flex-shrink:0; margin-top:8px;
}

.competitor-card {
  padding:14px; background:var(--c-surface);
  border:1px solid var(--c-border); border-radius:var(--radius);
  margin-bottom:10px;
}
.competitor-card:last-child { margin-bottom:0; }
.competitor-name { font-weight:600; font-size:.9rem; margin-bottom:2px; }
.competitor-name a { color:var(--c-accent); }
.competitor-name a:hover { text-decoration:underline; }
.competitor-desc { color:var(--c-text-3); font-size:.8rem; }

.aside-block { margin-bottom:24px; }
.aside-block:last-child { margin-bottom:0; }
.aside-label {
  font-size:.7rem; font-weight:600; text-transform:uppercase;
  letter-spacing:.06em; color:var(--c-text-3); margin-bottom:10px;
}
.screenshot-img {
  border-radius:var(--radius); overflow:hidden;
  border:1px solid var(--c-border); margin-bottom:8px;
  cursor:pointer; transition: box-shadow .2s;
}
.screenshot-img:hover { box-shadow: var(--shadow-md); }
a[data-fancybox] { display:block; text-decoration:none; }
.aside-tags { display:flex; flex-wrap:wrap; gap:6px; }
.meta-row {
  display:flex; justify-content:space-between;
  padding:8px 0; border-bottom:1px solid var(--c-border-l);
  font-size:.85rem;
}
.meta-row:last-child { border-bottom:none; }
.meta-row .label { color:var(--c-text-3); }
.meta-row .value { color:var(--c-text-2); font-weight:500; }

.source-links { display:flex; flex-direction:column; gap:6px; }
.source-link {
  display:inline-flex; align-items:center; gap:6px;
  font-size:.85rem; color:var(--c-accent); font-weight:500;
  padding:4px 0; transition:color .15s;
}
.source-link:hover { color:var(--c-accent-d); }

/* ─── Weekly Deep Dive ─── */
.weekly-reference {
  display:flex; align-items:center; justify-content:space-between; gap:12px;
  padding:14px 16px; margin-bottom:20px;
  background:var(--c-accent-l);
  border:1px solid var(--c-border);
  border-radius:var(--radius);
  color:var(--c-text-2); font-size:.88rem;
}
.weekly-reference a {
  display:inline-flex; align-items:center; gap:6px;
  color:var(--c-accent); font-weight:600;
}
.weekly-reference a:hover { color:var(--c-accent-d); }
.weekly-metric-grid {
  display:grid; grid-template-columns:repeat(3,1fr); gap:10px;
  margin-bottom:24px;
}
.weekly-metric {
  padding:12px; background:var(--c-bg);
  border:1px solid var(--c-border-l);
  border-radius:var(--radius);
}
.weekly-metric strong {
  display:block; font-size:1.25rem; color:var(--c-accent);
  line-height:1.2; margin-bottom:2px;
}
.weekly-metric span { font-size:.75rem; color:var(--c-text-3); }

/* ─── Archive Table ─── */
.archive-wrap {
  background:var(--c-surface);
  border:1px solid var(--c-border);
  border-radius:var(--radius-lg);
  overflow:hidden;
}
.archive-table { width:100%; border-collapse:collapse; }
.archive-table th {
  text-align:left; font-size:.7rem; font-weight:600;
  text-transform:uppercase; letter-spacing:.06em;
  color:var(--c-text-3); padding:12px 20px;
  background:var(--c-bg); border-bottom:1px solid var(--c-border);
}
.archive-table td {
  padding:14px 20px; border-bottom:1px solid var(--c-border-l);
  font-size:.9rem; vertical-align:top;
}
.archive-table tr:last-child td { border-bottom:none; }
.archive-table tr:hover td { background:var(--c-accent-l); }
.archive-date {
  white-space:nowrap; font-weight:600;
  color:var(--c-accent); width:110px;
}
.archive-products { color:var(--c-text-2); line-height:1.8; }
.archive-products a {
  color:var(--c-text); font-weight:500;
  transition:color .15s;
}
.archive-products a:hover { color:var(--c-accent); }
.archive-count {
  width:50px; text-align:center;
  color:var(--c-text-3); font-weight:600;
}

/* ─── Empty State ─── */
.empty {
  text-align:center; padding:80px 24px;
  color:var(--c-text-3);
}
.empty-icon {
  width:56px; height:56px; margin:0 auto 16px;
  border-radius:50%; background:var(--c-tag-bg);
  display:flex; align-items:center; justify-content:center;
  color:var(--c-text-3);
}
.empty h2 { font-size:1.1rem; color:var(--c-text-2); margin-bottom:4px; }
.empty p { font-size:.9rem; }

/* ─── Footer ─── */
.site-footer {
  border-top:1px solid var(--c-border);
  padding:24px 0; text-align:center;
  color:var(--c-text-3); font-size:.8rem;
}
.footer-links {
  display:flex; justify-content:center; gap:20px;
  margin-bottom:8px;
}
.footer-links a {
  color:var(--c-text-2); font-size:.85rem;
  transition:color .15s;
}
.footer-links a:hover { color:var(--c-accent); }

/* ─── Responsive: iPhone 16 (393px) + Desktop (1280px) ─── */
/* 默认样式 = iPhone 16 */
.detail-body { grid-template-columns:1fr; }
.detail-aside { border-top:1px solid var(--c-border); }
.hero { padding:32px 0 28px; margin-bottom:28px; }
.hero-stats { gap:16px; }
.product-entry { gap:12px; padding:12px; }
.entry-thumb { width:56px; height:56px; }
.blog-post { margin-bottom:32px; padding-bottom:28px; }
.detail-hero { padding:24px; }
.detail-main { padding:24px; }
.detail-aside { padding:24px; }
.detail-title { font-size:1.4rem; }
.archive-table th, .archive-table td { padding:10px 14px; }
.archive-date { width:90px; font-size:.8rem; }
.container { padding:0 16px; }
.container-wide { padding:0 16px; }
.site-header .container-wide { height:48px; }
.site-nav a { padding:5px 10px; font-size:.8rem; }

/* 桌面 ≥768px（适配 1280px） */
@media (min-width:768px) {
  .container { padding:0 24px; }
  .container-wide { padding:0 24px; }
  .site-header .container-wide { height:56px; }
  .site-nav a { padding:6px 14px; font-size:.875rem; }
  .hero { padding:48px 0 40px; margin-bottom:40px; }
  .hero-stats { gap:24px; }
  .product-entry { gap:16px; padding:16px; }
  .entry-thumb { width:72px; height:72px; }
  .blog-post { margin-bottom:48px; padding-bottom:40px; }
  .detail-hero { padding:32px; }
  .detail-main { padding:32px; }
  .detail-aside { padding:32px 24px; border-top:none; border-left:1px solid var(--c-border); }
  .detail-body { grid-template-columns:1fr 340px; }
  .detail-title { font-size:1.75rem; }
  .archive-table th, .archive-table td { padding:14px 20px; }
  .archive-date { width:110px; font-size:.9rem; }
}
@media (max-width:767px) {
  .weekly-reference { display:block; }
  .weekly-reference a { margin-top:8px; }
  .weekly-metric-grid { grid-template-columns:1fr; }
}
"""
    css_file = SITE_DIR / "styles.css"
    css_file.parent.mkdir(parents=True, exist_ok=True)
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css)


# ─── Header / Footer fragments ────────────────────────────────────────

def header_html(active='', depth=0):
    nav_items = [
        (home_href(depth), '每日简报', 'daily'),
        ('weekly.html', '每周深度', 'weekly'),
        ('archive.html', '归档', 'archive'),
    ]
    nav = ''
    for href, label, key in nav_items:
        cls = ' class="active"' if active == key else ''
        nav += f'<a href="{href if href.startswith(".") else rel(href, depth)}"{cls}>{label}</a>'
    nav += f'<a href="https://github.com/terranc/aI-product-daily-peport" target="_blank">{icon("github")}</a>'

    return f"""<header class="site-header">
  <div class="container-wide">
    <a href="{home_href(depth)}" class="site-logo">{icon("radar")} AI 产品雷达</a>
    <nav class="site-nav">{nav}</nav>
  </div>
</header>"""


def footer_html(depth=0):
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-links">
      <a href="{rel("archive.html", depth)}">历史归档</a>
      <a href="https://github.com/terranc/aI-product-daily-peport" target="_blank">GitHub</a>
    </div>
    <p>AI 产品雷达 · 自动化 AI 产品发现与分析</p>
  </div>
</footer>"""


def render_product_detail_content(prd, depth=0):
    a = prd.get('analysis', {})
    score = a.get('score', 0)
    tags = prd.get('tags', [])
    tags_h = ''.join(f'<a href="{rel(f"tags.html?tag={t}", depth)}" class="tag">{t}</a>' for t in tags)

    use_cases = a.get('useCases', [])
    uc_h = ''.join(f'<li>{c}</li>' for c in use_cases)

    competitors = a.get('competitors', [])
    comp_h = ''
    for c in competitors:
        comp_h += f"""<div class="competitor-card">
              <div class="competitor-name"><a href="{c.get('url','#')}" target="_blank">{c.get('name','')}</a></div>
              <div class="competitor-desc">{c.get('comparison','')}</div>
            </div>"""

    screenshot = prd.get('screenshotUrl', '')
    app_ss = prd.get('appStoreScreenshots', [])
    ss_h = ''
    if screenshot:
        # 本地网站截图，用相对路径
        ss_h += f'<a href="{rel(screenshot, depth)}" data-fancybox="gallery" data-caption="{prd["name"]}"><div class="screenshot-img"><img src="{rel(screenshot, depth)}" alt="{prd["name"]}" loading="lazy"></div></a>'
    for s in app_ss:
        # App Store 截图是远程 URL，直接引用
        ss_h += f'<a href="{s}" data-fancybox="gallery" data-caption="App Store 截图"><div class="screenshot-img"><img src="{s}" alt="App Store 截图" loading="lazy"></div></a>'

    # 数据来源链接
    raw = prd.get('rawData', {})
    source_links = []
    channel_labels = {'hackernews': 'Hacker News', 'reddit': 'Reddit', 'twitter': 'Twitter', 'github': 'GitHub'}

    # 优先使用报告中的 sourceUrl 字段
    source_url = prd.get('sourceUrl', '')
    if source_url:
        ch = prd.get('sourceChannels', ['未知'])[0]
        label = channel_labels.get(ch, ch)
        source_links.append(f'<a href="{source_url}" target="_blank" class="source-link">{icon("external")} {label}</a>')
    else:
        # 回退到 rawData 中的链接
        for ch in prd.get('sourceChannels', []):
            label = channel_labels.get(ch, ch)
            if ch == 'hackernews':
                url = raw.get('hn_url') or raw.get('source_url', '')
            elif ch == 'reddit':
                url = raw.get('redditUrl') or raw.get('source_url', '')
            elif ch == 'twitter':
                url = raw.get('twitterUrl') or raw.get('source_url', '')
            else:
                url = raw.get('source_url') or raw.get('url', '')
            if url:
                source_links.append(f'<a href="{url}" target="_blank" class="source-link">{icon("external")} {label}</a>')
    source_h = ''.join(source_links) if source_links else '<span style="color:var(--c-text-3);font-size:.85rem">暂无</span>'

    url = prd.get('url') or prd.get('homepage', '')
    btn_web = f'<a href="{url}" target="_blank" class="btn btn-primary">{icon("external")} 访问官网</a>' if url else ''
    btn_app = f'<a href="{prd["appStoreUrl"]}" target="_blank" class="btn btn-ghost">{icon("phone")} App Store</a>' if prd.get('appStoreUrl') else ''

    return f"""<div id="product-detail-content">
      <article class="detail-card">
        <div class="detail-hero">
          <div class="entry-meta">
            <span class="blog-post-date">{prd.get('date','')}</span>
            <div class="entry-tags">{tags_h}</div>
          </div>
          <h1 class="detail-title">{prd['name']}</h1>
          <p class="detail-subtitle">{prd.get('description','')}</p>
          <div class="detail-actions">
            <span class="detail-score-badge">{score}</span>
            {btn_web}{btn_app}
          </div>
        </div>
        <div class="detail-body">
          <div class="detail-main">
            <div class="section">
              <h2 class="section-title"><span class="ic">{icon("target")}</span> 目标受众</h2>
              <p>{a.get('targetAudience','待分析')}</p>
            </div>
            <div class="section">
              <h2 class="section-title"><span class="ic">{icon("bulb")}</span> 使用场景</h2>
              <ul class="use-case-list">{uc_h if uc_h else '<li>待补充</li>'}</ul>
            </div>
            <div class="section">
              <h2 class="section-title"><span class="ic">{icon("palette")}</span> 设计初衷</h2>
              <p>{a.get('designIntent','待分析')}</p>
            </div>
            <div class="section">
              <h2 class="section-title"><span class="ic">{icon("zap")}</span> 解决什么问题</h2>
              <p>{a.get('problemSolved','待分析')}</p>
            </div>
            <div class="section">
              <h2 class="section-title"><span class="ic">{icon("chart")}</span> 评分理由</h2>
              <p>{a.get('scoreReason','待分析')}</p>
            </div>
            <div class="section">
              <h2 class="section-title"><span class="ic">{icon("swords")}</span> 对标竞品</h2>
              {comp_h if comp_h else '<p style="color:var(--c-text-3)">暂无竞品分析</p>'}
            </div>
          </div>
          <aside class="detail-aside">
            <div class="aside-block">
              <div class="aside-label">产品截图</div>
              {ss_h if ss_h else '<p style="color:var(--c-text-3);font-size:.85rem">暂无截图</p>'}
            </div>
            <div class="aside-block">
              <div class="aside-label">标签</div>
              <div class="aside-tags">{tags_h}</div>
            </div>
            <div class="aside-block">
              <div class="aside-label">数据来源</div>
              <div class="source-links">{source_h}</div>
            </div>
            <div class="aside-block">
              <div class="aside-label">元数据</div>
              <div class="meta-row"><span class="label">首次发现</span><span class="value">{prd.get('firstSeen','')[:10]}</span></div>
              <div class="meta-row"><span class="label">来源渠道</span><span class="value">{', '.join(prd.get('sourceChannels',[]))}</span></div>
              <div class="meta-row"><span class="label">产品类型</span><span class="value">{prd.get('type','')}</span></div>
            </div>
          </aside>
        </div>
      </article>
    </div>"""


# ─── Page: Index (blog style) ─────────────────────────────────────────

def generate_index(reports):
    recent = reports[:14]

    posts_html = ''
    for report in recent:
        date = report.get('date', '')
        products = report.get('products', [])
        count = len(products)

        try:
            dt = datetime.strptime(date, '%Y-%m-%d')
            weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            date_label = f"{date} {weekdays[dt.weekday()]}"
            title_date = f"{dt.month}月{dt.day}日"
        except Exception:
            date_label = date
            title_date = date

        entries = ''
        for prd in products:
            a = prd.get('analysis', {})
            score = a.get('score', 0)
            tags = prd.get('tags', [])[:3]
            tags_h = ''.join(f'<span class="tag">{t}</span>' for t in tags)

            img_url = prd.get('screenshotUrl') or (prd.get('appStoreScreenshots', [''])[0] if prd.get('appStoreScreenshots') else '')
            thumb = f'<img src="{rel(img_url, 0)}" alt="{prd["name"]}" loading="lazy">' if img_url else '<div class="ph"></div>'

            link = rel("products/" + prd['slug'].lower() + ".html", 0)
            entries += f"""
      <a href="{link}" class="product-entry" data-slug="{prd['slug'].lower()}">
        <div class="entry-thumb">{thumb}</div>
        <div class="entry-body">
          <div class="entry-name">{prd['name']}</div>
          <p class="entry-desc">{prd.get('description', '')[:150]}</p>
          <div class="entry-meta">
            <span class="entry-score">{score}</span>
            <div class="entry-tags">{tags_h}</div>
          </div>
        </div>
      </a>"""

        posts_html += f"""
    <article class="blog-post">
      <div class="blog-post-header">
        <div class="blog-post-date">{date_label}</div>
        <h2 class="blog-post-title">{title_date} <span class="count">· {count} 个产品</span></h2>
      </div>
      {entries}
    </article>"""

    total = sum(len(r.get('products', [])) for r in reports)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI 产品雷达 · 每日 AI 应用发现</title>
  <link rel="stylesheet" href="{rel("styles.css", 0)}">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.css">
  <script src="https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.umd.js" defer></script>
  <style>
    /* ── Product Detail Modal ── */
    .product-modal-overlay {{
      display:none; position:fixed; inset:0; z-index:9000;
      background:rgba(0,0,0,.5); backdrop-filter:blur(4px);
      overflow-y:auto; -webkit-overflow-scrolling:touch;
    }}
    .product-modal-overlay.active {{ display:block; }}
    .product-modal-container {{
      position:relative; max-width:1120px; width:90%; margin:40px auto;
      min-height:auto; background:var(--c-bg);
      border-radius:var(--radius-lg); box-shadow:0 8px 32px rgba(0,0,0,.2);
      overflow:hidden;
    }}
    .product-modal-close {{
      position:sticky; top:0; z-index:10;
      display:flex; align-items:center; justify-content:space-between;
      padding:12px 16px; background:var(--c-surface);
      border-bottom:1px solid var(--c-border);
    }}
    .product-modal-close button {{
      background:none; border:none; cursor:pointer;
      font-size:1rem; color:var(--c-text-2); padding:4px 8px;
    }}
    .product-modal-close .title {{ font-weight:600; font-size:.9rem; color:var(--c-text); }}
    .product-modal-body {{
      padding:0;
    }}
    .fancybox__container {{ z-index:10000; }}
  </style>
</head>
<body>
  {header_html('daily', 0)}
  <main>
    <div class="container">
      <div class="hero">
        <h1>每日 AI 应用发现</h1>
        <p>追踪最值得关注的 AI 创新产品，每日精选 5 个，每周深度分析 1 个</p>
        <div class="hero-stats">
          <div class="hero-stat"><strong>{total}</strong><span>已收录</span></div>
          <div class="hero-stat"><strong>{len(reports)}</strong><span>期</span></div>
        </div>
      </div>
      <div class="blog-feed">
        {posts_html if posts_html else '<div class="empty"><div class="empty-icon">{icon("inbox")}</div><h2>暂无数据</h2><p>运行每日抓取后将在此显示</p></div>'}
      </div>
    </div>
  </main>

  <!-- 产品详情 Modal -->
  <div class="product-modal-overlay" id="product-modal">
    <div class="product-modal-container">
      <div class="product-modal-close">
        <span class="title" id="modal-title"></span>
        <button onclick="closeProductModal()" aria-label="关闭">✕ 关闭</button>
      </div>
      <div class="product-modal-body" id="modal-body">
        <div style="text-align:center;padding:40px;color:var(--c-text-3)">加载中...</div>
      </div>
    </div>
  </div>

  {footer_html(0)}

    <script>
    // Modal 逻辑（所有设备）
    const modal = document.getElementById('product-modal');
    const modalBody = document.getElementById('modal-body');
    const modalTitle = document.getElementById('modal-title');

    // 大屏设备用 Modal，手机端和无 JS 环境保持普通链接跳转
    const isDesktop = window.matchMedia('(min-width: 769px)').matches;
    if (isDesktop) {{
      document.querySelectorAll('.product-entry[href]').forEach(card => {{
        card.addEventListener('click', function(e) {{
          if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
          e.preventDefault();
          const name = this.querySelector('.entry-name')?.textContent || '';
          openProductModal(this.getAttribute('href'), name);
        }});
      }});
    }}

    function rebaseModalUrls(root, baseUrl) {{
      root.querySelectorAll('[src]').forEach(el => {{
        const value = el.getAttribute('src');
        if (value && !value.startsWith('http') && !value.startsWith('data:')) {{
          el.setAttribute('src', new URL(value, baseUrl).href);
        }}
      }});
      root.querySelectorAll('[href]').forEach(el => {{
        const value = el.getAttribute('href');
        if (value && !value.startsWith('http') && !value.startsWith('#') && !value.startsWith('mailto:')) {{
          el.setAttribute('href', new URL(value, baseUrl).href);
        }}
      }});
    }}

    async function openProductModal(detailUrl, name) {{
      modalTitle.textContent = name;
      modalBody.innerHTML = '<div style="text-align:center;padding:40px;color:var(--c-text-3)">加载中...</div>';
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';

      try {{
        const resp = await fetch(detailUrl);
        if (!resp.ok) throw new Error('HTTP ' + resp.status);
        const html = await resp.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');

        const detailContent = doc.querySelector('#product-detail-content');
        if (detailContent) {{
          rebaseModalUrls(detailContent, new URL(detailUrl, window.location.href).href);

          modalBody.replaceChildren(detailContent);
          if (typeof Fancybox !== 'undefined') {{
            Fancybox.bind(modalBody, '[data-fancybox]', {{
              Thumbs: false,
              parentEl: document.body
            }});
          }}
        }} else {{
          throw new Error('详情主体不存在');
        }}
      }} catch (err) {{
        modalBody.innerHTML = '<div style="text-align:center;padding:40px;color:var(--c-text-3)">加载失败，请<a href="' + detailUrl + '" style="color:var(--c-accent);font-weight:600">打开详情页</a></div>';
      }}

      modal.scrollTop = 0;
    }}

    function closeProductModal() {{
      modal.classList.remove('active');
      document.body.style.overflow = '';
      // 解绑 Fancybox
      if (typeof Fancybox !== 'undefined') {{
        try {{ Fancybox.close(); }} catch(e) {{}}
      }}
    }}

    // 点击遮罩关闭
    modal.addEventListener('click', function(e) {{
      if (e.target === modal) closeProductModal();
    }});

    function isFancyboxOpen() {{
      return document.querySelector('.fancybox__container') !== null;
    }}

    // ESC 关闭
    document.addEventListener('keydown', function(e) {{
      if (e.key === 'Escape' && modal.classList.contains('active')) {{
        if (isFancyboxOpen()) return;
        closeProductModal();
      }}
    }});
  </script>
</body>
</html>"""

    (SITE_DIR / "index.html").write_text(html, encoding='utf-8')


# ─── Page: Product Detail ─────────────────────────────────────────────

def generate_product_pages(all_products):
    out_dir = SITE_DIR / "products"
    out_dir.mkdir(parents=True, exist_ok=True)

    for prd in all_products:
        detail_content = render_product_detail_content(prd, depth=1)

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{prd['name']} · AI 产品雷达</title>
  <link rel="stylesheet" href="{rel("styles.css", 1)}">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.css">
  <script src="https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.umd.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', function() {{
      if (typeof Fancybox !== 'undefined') {{
        Fancybox.bind('[data-fancybox]', {{Thumbs: false}});
      }}
    }});
  </script>
</head>
<body>
  {header_html('', 1)}
  <main>
    <div class="container-wide">
      <a href="{home_href(1)}" class="back-link">{icon("arrow")} 返回首页</a>
      {detail_content}
    </div>
  </main>
  {footer_html(1)}
</body>
</html>"""

        (out_dir / f"{prd['slug'].lower()}.html").write_text(html, encoding='utf-8')


# ─── Page: Archive ────────────────────────────────────────────────────

def generate_archive(reports):
    rows = ''
    for rpt in reports:
        date = rpt['date']
        products = rpt.get('products', [])
        links = []
        for prd in products:
            href = rel("products/" + prd['slug'].lower() + ".html", 0)
            links.append(f'<a href="{href}">{prd["name"]}</a>')
        joined = '、'.join(links) if links else '<span style="color:var(--c-text-3)">暂无</span>'
        rows += f"""
        <tr>
          <td class="archive-date">{date}</td>
          <td class="archive-products">{joined}</td>
          <td class="archive-count">{len(products)}</td>
        </tr>"""

    table = f"""<table class="archive-table">
        <thead><tr><th>日期</th><th>精选产品</th><th>数量</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>""" if rows else '<div class="empty"><h2>暂无历史数据</h2></div>'

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>历史归档 · AI 产品雷达</title>
  <link rel="stylesheet" href="{rel("styles.css", 0)}">
</head>
<body>
  {header_html('archive', 0)}
  <main>
    <div class="container-wide">
      <div class="hero" style="padding-bottom:24px;margin-bottom:28px;">
        <h1 style="font-size:1.75rem;">历史归档</h1>
        <p>按日期浏览所有精选产品，共 {len(reports)} 期</p>
      </div>
      <div class="archive-wrap">{table}</div>
    </div>
  </main>
  {footer_html(0)}
</body>
</html>"""

    (SITE_DIR / "archive.html").write_text(html, encoding='utf-8')


def weekly_detail_href(date, slug, depth=0):
    return rel(f"weekly/{date}-{slug.lower()}.html", depth)


def render_weekly_value(value):
    if isinstance(value, list):
        if not value:
            return '<p style="color:var(--c-text-3)">待补充</p>'
        items = ''.join(f'<li>{item}</li>' for item in value)
        return f'<ul class="use-case-list">{items}</ul>'
    return f'<p>{value or "待补充"}</p>'


def render_weekly_detail_content(report, prd, depth=0):
    a = prd.get('analysis', {})
    deep = prd.get('weeklyDeepDive') or prd.get('deepDive') or {}
    metrics = prd.get('growthMetrics', {})
    source_daily = prd.get('sourceDailyReport', {})
    source_href = source_daily.get('detailHref') or f"products/{prd.get('slug', '').lower()}.html"
    source_date = source_daily.get('date', '')
    source_link = rel(source_href, depth) if source_href else '#'

    score = a.get('score', 0)
    tags = prd.get('tags', [])
    tags_h = ''.join(f'<a href="{rel(f"tags.html?tag={t}", depth)}" class="tag">{t}</a>' for t in tags)

    sections = [
        ('增长证据', 'chart', deep.get('growthEvidence') or deep.get('growthData')),
        ('社区反馈', 'bulb', deep.get('communityFeedback') or deep.get('communityActivity')),
        ('近期更新', 'zap', deep.get('recentUpdates') or deep.get('updateFrequency')),
        ('市场定位', 'target', deep.get('marketPosition')),
        ('差异化', 'palette', deep.get('differentiation')),
        ('风险挑战', 'swords', deep.get('risksAndChallenges')),
        ('后续观察', 'chart', deep.get('outlook')),
    ]

    sections_h = ''
    for title, icon_name, value in sections:
        sections_h += f"""
            <div class="section">
              <h2 class="section-title"><span class="ic">{icon(icon_name)}</span> {title}</h2>
              {render_weekly_value(value)}
            </div>"""

    channels = metrics.get('channels', [])
    channel_text = ', '.join(channels) if channels else ', '.join(prd.get('sourceChannels', []))
    url = prd.get('url') or prd.get('homepage', '')
    btn_web = f'<a href="{url}" target="_blank" class="btn btn-primary">{icon("external")} 访问官网</a>' if url else ''
    source_ref = f'{source_date} 每日产品详情' if source_date else '每日产品详情'

    return f"""<div id="weekly-detail-content">
      <article class="detail-card">
        <div class="detail-hero">
          <div class="entry-meta">
            <span class="blog-post-date">{report.get('date','')}</span>
            <div class="entry-tags">{tags_h}</div>
          </div>
          <h1 class="detail-title">{prd['name']} · 每周深度分析</h1>
          <p class="detail-subtitle">{prd.get('description','')}</p>
          <div class="detail-actions">
            <span class="detail-score-badge">{score}</span>
            {btn_web}
          </div>
        </div>
        <div class="detail-body">
          <div class="detail-main">
            <div class="weekly-reference">
              <span>本篇深度分析基于该产品入选每日简报后的持续跟踪。</span>
              <a href="{source_link}">{icon("external")} {source_ref}</a>
            </div>
            <div class="weekly-metric-grid">
              <div class="weekly-metric"><strong>{metrics.get('daysSinceDailyFeature', 0)}</strong><span>距日报入选天数</span></div>
              <div class="weekly-metric"><strong>{metrics.get('recentMentions', 0)}</strong><span>近 7 天提及</span></div>
              <div class="weekly-metric"><strong>{metrics.get('growthScore', 0)}</strong><span>增长分数</span></div>
            </div>
            {sections_h}
          </div>
          <aside class="detail-aside">
            <div class="aside-block">
              <div class="aside-label">引用日报</div>
              <div class="source-links"><a href="{source_link}" class="source-link">{icon("external")} {source_ref}</a></div>
            </div>
            <div class="aside-block">
              <div class="aside-label">标签</div>
              <div class="aside-tags">{tags_h}</div>
            </div>
            <div class="aside-block">
              <div class="aside-label">跟踪渠道</div>
              <p style="color:var(--c-text-2);font-size:.85rem">{channel_text or '暂无'}</p>
            </div>
            <div class="aside-block">
              <div class="aside-label">元数据</div>
              <div class="meta-row"><span class="label">周报日期</span><span class="value">{report.get('date','')}</span></div>
              <div class="meta-row"><span class="label">首次日报</span><span class="value">{source_date}</span></div>
              <div class="meta-row"><span class="label">产品类型</span><span class="value">{prd.get('type','')}</span></div>
            </div>
          </aside>
        </div>
      </article>
    </div>"""


def generate_weekly_detail_pages(reports):
    out_dir = SITE_DIR / "weekly"
    out_dir.mkdir(parents=True, exist_ok=True)

    for report in reports:
        date = report.get('date', '')
        for prd in report.get('products', []):
            slug = prd.get('slug', '').lower()
            if not date or not slug:
                continue

            detail_content = render_weekly_detail_content(report, prd, depth=1)
            html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{prd['name']} 每周深度分析 · AI 产品雷达</title>
  <link rel="stylesheet" href="{rel("styles.css", 1)}">
</head>
<body>
  {header_html('weekly', 1)}
  <main>
    <div class="container-wide">
      <a href="{rel("weekly.html", 1)}" class="back-link">{icon("arrow")} 返回每周深度</a>
      {detail_content}
    </div>
  </main>
  {footer_html(1)}
</body>
</html>"""

            (out_dir / f"{date}-{slug}.html").write_text(html, encoding='utf-8')


def generate_weekly(reports):
    """生成每周深度分析页面"""
    recent = reports[:10]  # 显示最近10期

    posts_html = ''
    for report in recent:
        date = report.get('date', '')
        products = report.get('products', [])
        count = len(products)

        try:
            dt = datetime.strptime(date, '%Y-%m-%d')
            weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            date_label = f"{date} {weekdays[dt.weekday()]}"
        except Exception:
            date_label = date

        entries = ''
        for prd in products:
            a = prd.get('analysis', {})
            score = a.get('score', 0)
            tags = prd.get('tags', [])[:3]
            tags_h = ''.join(f'<span class="tag">{t}</span>' for t in tags)

            img_url = prd.get('screenshotUrl') or (prd.get('appStoreScreenshots', [''])[0] if prd.get('appStoreScreenshots') else '')
            thumb = f'<img src="{rel(img_url, 0)}" alt="{prd["name"]}" loading="lazy">' if img_url else '<div class="ph"></div>'

            link = weekly_detail_href(date, prd['slug'], 0)
            entries += f"""
      <a href="{link}" class="product-entry" data-slug="{prd['slug'].lower()}">
        <div class="entry-thumb">{thumb}</div>
        <div class="entry-body">
          <div class="entry-name">{prd['name']}</div>
          <p class="entry-desc">{prd.get('description', '')[:150]}</p>
          <div class="entry-meta">
            <span class="entry-score">{score}</span>
            <div class="entry-tags">{tags_h}</div>
          </div>
        </div>
      </a>"""

        posts_html += f"""
    <article class="blog-post">
      <div class="blog-post-header">
        <div class="blog-post-date">{date_label}</div>
        <h2 class="blog-post-title">本周深度分析 <span class="count">· {count} 个产品</span></h2>
      </div>
      {entries}
    </article>"""

    total = sum(len(r.get('products', [])) for r in reports)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>每周深度分析 · AI 产品雷达</title>
  <link rel="stylesheet" href="{rel("styles.css", 0)}">
</head>
<body>
  {header_html('weekly', 0)}
  <main>
    <div class="container">
      <div class="hero">
        <h1>每周深度分析</h1>
        <p>每周精选 1 个 AI 产品进行深度调研分析，挖掘产品价值、竞品对比、市场定位</p>
        <div class="hero-stats">
          <div class="hero-stat"><strong>{total}</strong><span>已分析</span></div>
          <div class="hero-stat"><strong>{len(reports)}</strong><span>期</span></div>
        </div>
      </div>
      <div class="blog-feed">
        {posts_html if posts_html else '<div class="empty"><div class="empty-icon">' + icon("inbox") + '</div><h2>暂无数据</h2><p>运行每周深度分析后将在此显示</p></div>'}
      </div>
    </div>
  </main>
  {footer_html(0)}
</body>
</html>"""

    (SITE_DIR / "weekly.html").write_text(html, encoding='utf-8')


# ─── Data: All Products JSON ─────────────────────────────────────────

def generate_all_products_json(all_products):
    """生成所有产品的汇总 JSON，供 tags.html 客户端 JS 使用"""
    products_data = []
    for prd in all_products:
        products_data.append({
            'name': prd.get('name', ''),
            'slug': prd.get('slug', ''),
            'description': prd.get('description', ''),
            'url': prd.get('url', ''),
            'tags': prd.get('tags', []),
            'score': prd.get('analysis', {}).get('score', 0),
            'date': prd.get('date', ''),
            'type': prd.get('type', ''),
            'screenshotUrl': prd.get('screenshotUrl', ''),
            'appStoreScreenshots': prd.get('appStoreScreenshots', []),
        })

    # 按日期倒序
    products_data.sort(key=lambda x: x['date'], reverse=True)

    out_file = SITE_DIR / "all-products.json"
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(products_data, f, ensure_ascii=False)

    print(f"  📊 汇总数据: {len(products_data)} 个产品 → all-products.json")


# ─── Page: Tags ───────────────────────────────────────────────────────

def generate_tags_page():
    """生成标签筛选页面，客户端 JS 拉取 all-products.json 实现筛选+分页"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>标签筛选 · AI 产品雷达</title>
  <link rel="stylesheet" href="styles.css">
  <style>
    .tag-hero {{ text-align:center; padding:40px 0 24px; }}
    .tag-hero h1 {{ font-size:1.75rem; font-weight:700; margin-bottom:8px; }}
    .tag-hero .tag-name {{ color:var(--c-accent); }}
    .tag-hero p {{ color:var(--c-text-2); }}
    .tag-count {{ font-size:.85rem; color:var(--c-text-3); margin-top:8px; }}
    .product-list {{ max-width:800px; margin:0 auto; padding-bottom:40px; }}
    .product-item {{
      display:flex; gap:16px; padding:16px;
      background:var(--c-surface); border:1px solid var(--c-border);
      border-radius:var(--radius); margin-bottom:12px;
      text-decoration:none; color:inherit; cursor:pointer;
      transition:all .2s var(--ease);
    }}
    .product-item:hover {{ border-color:var(--c-accent); box-shadow:var(--shadow-md); transform:translateY(-1px); }}
    .product-thumb {{
      width:64px; height:64px; flex-shrink:0; border-radius:6px;
      overflow:hidden; background:var(--c-tag-bg);
      display:flex; align-items:center; justify-content:center;
    }}
    .product-thumb img {{ width:100%; height:100%; object-fit:cover; }}
    .product-thumb .ph {{ width:28px; height:28px; border-radius:6px; background:linear-gradient(135deg,var(--c-accent),#818cf8); opacity:.3; }}
    .product-info {{ flex:1; min-width:0; }}
    .product-name {{ font-size:.95rem; font-weight:600; margin-bottom:4px; }}
    .product-desc {{ font-size:.8rem; color:var(--c-text-2); line-height:1.6; margin-bottom:8px; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }}
    .product-meta {{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; }}
    .product-score {{ font-size:1.1rem; font-weight:800; color:var(--c-accent); min-width:28px; text-align:center; }}
    .product-date {{ font-size:.7rem; color:var(--c-text-3); }}
    .product-tags {{ display:flex; gap:4px; }}
    .product-tags .mini-tag {{ font-size:.6rem; padding:1px 6px; border-radius:3px; background:var(--c-tag-bg); color:var(--c-text-3); }}
    .load-more-btn {{
      display:block; margin:24px auto; padding:12px 32px;
      background:var(--c-accent-l); color:var(--c-accent);
      border:1px solid var(--c-accent); border-radius:var(--radius);
      font-weight:600; font-size:.9rem; cursor:pointer;
      transition:all .15s var(--ease);
    }}
    .load-more-btn:hover {{ background:var(--c-accent); color:#fff; }}
    .load-more-btn:disabled {{ opacity:.4; cursor:default; }}
    .loading {{ text-align:center; padding:40px; color:var(--c-text-3); }}
    .no-results {{ text-align:center; padding:60px; color:var(--c-text-3); }}
  </style>
</head>
<body>
  {header_html('tags', 0)}
  <main>
    <div class="container">
      <div class="tag-hero">
        <h1>标签：<span class="tag-name" id="tag-name">加载中...</span></h1>
        <p id="tag-desc"></p>
        <div class="tag-count" id="tag-count"></div>
      </div>
      <div class="product-list" id="product-list">
        <div class="loading">正在加载产品数据...</div>
      </div>
    </div>
  </main>
  {footer_html(0)}

  <script>
    const PAGE_SIZE = 5;
    let allFiltered = [];
    let shown = 0;

    function getTag() {{
      const params = new URLSearchParams(window.location.search);
      return params.get('tag') || '';
    }}

    function renderProduct(p) {{
      const slug = p.slug.toLowerCase();
      const thumb = p.screenshotUrl
        ? `<img src="${{p.screenshotUrl}}" alt="${{p.name}}" loading="lazy">`
        : (p.appStoreScreenshots && p.appStoreScreenshots.length
          ? `<img src="${{p.appStoreScreenshots[0]}}" alt="${{p.name}}" loading="lazy">`
          : '<div class="ph"></div>');
      const tags = (p.tags || []).slice(0, 3).map(t => `<span class="mini-tag">${{t}}</span>`).join('');
      return `
        <a href="products/${{slug}}.html" class="product-item">
          <div class="product-thumb">${{thumb}}</div>
          <div class="product-info">
            <div class="product-name">${{p.name}}</div>
            <p class="product-desc">${{p.description || ''}}</p>
            <div class="product-meta">
              <span class="product-score">${{p.score || '-'}}</span>
              <span class="product-date">${{p.date}}</span>
              <div class="product-tags">${{tags}}</div>
            </div>
          </div>
        </a>`;
    }}

    function renderBatch() {{
      const list = document.getElementById('product-list');
      const end = Math.min(shown + PAGE_SIZE, allFiltered.length);
      for (let i = shown; i < end; i++) {{
        list.insertAdjacentHTML('beforeend', renderProduct(allFiltered[i]));
      }}
      shown = end;

      // 更新"查看更多"按钮
      const existingBtn = document.getElementById('load-more');
      if (existingBtn) existingBtn.remove();
      if (shown < allFiltered.length) {{
        const btn = document.createElement('button');
        btn.id = 'load-more';
        btn.className = 'load-more-btn';
        btn.textContent = `查看更多（剩余 ${{allFiltered.length - shown}} 个）`;
        btn.onclick = renderBatch;
        list.appendChild(btn);
      }}
    }}

    async function init() {{
      const tag = getTag();
      if (!tag) {{
        document.getElementById('tag-name').textContent = '未指定标签';
        document.getElementById('product-list').innerHTML = '<div class="no-results">请在 URL 中添加 ?tag=标签名 参数</div>';
        return;
      }}

      document.getElementById('tag-name').textContent = tag;
      document.title = `${{tag}} · AI 产品雷达`;

      try {{
        const resp = await fetch('all-products.json');
        const products = await resp.json();

        // 按标签筛选
        allFiltered = products.filter(p => (p.tags || []).includes(tag));

        document.getElementById('tag-count').textContent = `共 ${{allFiltered.length}} 个产品`;

        if (allFiltered.length === 0) {{
          document.getElementById('product-list').innerHTML = '<div class="no-results">暂无标签为「' + tag + '」的产品</div>';
          return;
        }}

        document.getElementById('product-list').innerHTML = '';
        renderBatch();

      }} catch (e) {{
        document.getElementById('product-list').innerHTML = '<div class="no-results">数据加载失败：' + e.message + '</div>';
      }}
    }}

    init();
  </script>
</body>
</html>"""

    (SITE_DIR / "tags.html").write_text(html, encoding='utf-8')


# ─── Main ─────────────────────────────────────────────────────────────

def main():
    print("🔨 构建静态网站（浅色版）...")
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True)

    copy_assets()
    daily_reports = load_daily_reports()
    weekly_reports = load_weekly_reports()
    generate_css()

    all_products = []
    for rpt in daily_reports:
        for prd in rpt.get('products', []):
            prd['date'] = rpt['date']
            all_products.append(prd)

    # 周报产品也加入产品页生成（如果尚未存在）
    existing_slugs = {p.get('slug', '').lower() for p in all_products}
    for rpt in weekly_reports:
        for prd in rpt.get('products', []):
            prd['date'] = rpt['date']
            if prd.get('slug', '').lower() not in existing_slugs:
                all_products.append(prd)
                existing_slugs.add(prd.get('slug', '').lower())

    generate_index(daily_reports)
    generate_weekly(weekly_reports)
    generate_weekly_detail_pages(weekly_reports)
    generate_product_pages(all_products)
    generate_archive(daily_reports)
    generate_all_products_json(all_products)
    generate_tags_page()

    # 自定义域名 CNAME 文件
    (SITE_DIR / "CNAME").write_text("ai-daily.asdasd.vip", encoding="utf-8")

    print(f"✅ 完成：{SITE_DIR}  ({len(all_products)} 个产品页, {len(weekly_reports)} 期周报)")


if __name__ == '__main__':
    main()

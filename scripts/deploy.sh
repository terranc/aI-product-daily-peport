#!/bin/bash
# 部署脚本 - 构建网站并推送到 GitHub Pages
set -e

PROJECT_DIR="/Volumes/EXTEND/aI-product-daily-peport"
cd "$PROJECT_DIR"

echo "🔨 Step 1: 构建静态网站..."
python3 scripts/build_site.py

echo ""
echo "📦 Step 2: 提交变更..."
git add -A
git commit -m "🔄 Update: $(date '+%Y-%m-%d %H:%M')" --allow-empty

echo ""
echo "🌿 Step 3: 用 subtree 分离 docs/ 到 gh-pages 分支..."
# 删除旧的 gh-pages 分支（如果存在）
git branch -D gh-pages 2>/dev/null || true
# 从 docs/ 子目录创建 gh-pages 分支
git subtree split --prefix=docs -b gh-pages

echo ""
echo "🚀 Step 4: 推送到 GitHub..."
git push origin main
git push origin gh-pages --force

echo ""
echo "✅ 部署完成！"
echo "📡 GitHub Pages: https://terranc.github.io/aI-product-daily-peport/"

#!/bin/bash
# 部署脚本 - 构建网站并推送到 GitHub Pages
set -e

PROJECT_DIR="/Volumes/EXTEND/aI-product-daily-peport"
cd "$PROJECT_DIR"

echo "🔨 Step 1: 构建静态网站..."
python3 scripts/build_site.py

echo ""
echo "📦 Step 2: 提交并推送..."
cd docs

# 初始化 git（如果还没有的话）
if [ ! -d ".git" ]; then
    git init
    git remote add origin git@github.com:terranc/aI-product-daily-peport.git
    git checkout -b gh-pages
fi

git add -A
git commit -m "🔄 Auto-update: $(date '+%Y-%m-%d %H:%M')"

echo ""
echo "🚀 Step 3: 推送到 gh-pages 分支..."
git push origin gh-pages --force 2>/dev/null || {
    echo "⚠️ 推送失败，尝试使用 main 分支..."
    git checkout -b main 2>/dev/null || true
    git push origin main --force
}

echo ""
echo "✅ 部署完成！"
echo "📡 GitHub Pages: https://terranc.github.io/aI-product-daily-peport/"

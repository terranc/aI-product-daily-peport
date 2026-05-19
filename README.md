# AI Product Radar 🚀

每日 AI 应用发现与每周深度分析

## 项目简介

本项目通过自动化抓取多个平台（Hacker News、Twitter、Reddit、GitHub 等）的 AI 相关产品信息，筛选出最值得关注的创新产品，生成每日简报和每周深度报告。

## 项目结构

```
/
├── scripts/           # 抓取和分析脚本
├── data/              # 数据存储
├── reports/           # 生成的报告
│   ├── daily/        # 每日简报
│   └── weekly/       # 每周深度报告
├── assets/           # 静态资源
│   └── screenshots/  # 产品截图
├── docs/             # 文档
├── config.json       # 配置文件
└── README.md

# GitHub Pages 站点 (gh-pages 分支)
├── index.html        # 主页（卡片列表）
├── products/         # 产品详情页
└── css/              # 样式文件
```

## 数据流程

```
多平台抓取 → 去重筛选 → AI分析 → 截图生成 → 网站生成 → GitHub推送
```

## 配置说明

编辑 `config.json` 调整：
- 抓取平台开关
- AI分析标准
- 标签分类体系
- 冷却期设置

## 使用方法

```bash
# 运行每日抓取
python3 scripts/daily_crawl.py

# 运行每周深度分析
python3 scripts/weekly_analysis.py

# 生成网站
python3 scripts/build_site.py

# 推送到 GitHub
./scripts/deploy.sh
```

## 自动化

- **每日任务**: 每天早8点自动抓取生成简报
- **每周任务**: 每周一早8点生成深度报告

## License

MIT

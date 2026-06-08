# AI Product Radar - 长期记忆

## 项目架构

- **项目类型**: AI Product Radar - 多平台 AI 产品抓取、分析、去重、每日精选、每周深度分析
- **数据源**: Hacker News, Reddit, Product Hunt, Twitter, V2EX
- **产品数据库**: `data/products.json`（结构: `{version, lastUpdated, products: [], tracking: []}`）
- **日报输出**: `reports/daily/`
- **周报输出**: `reports/weekly/`
- **静态站点**: `docs/`（通过 `scripts/build_site.py` 生成）

## LLM 分析引擎 (2026-05-23)

已完成从"关键词匹配"到"LLM 驱动"的策略升级：

### 核心模块
- **`scripts/llm_analyzer.py`**: LLM 分析引擎
  - 基于 requests 直接调用 OpenAI API（无需 openai SDK）
  - 支持多 Provider 自动检测：OpenAI、火山引擎 DeepSeek、OpenRouter、xAI Grok
  - 环境变量优先级：`OPENAI_API_KEY` > `ZSH_AI_OPENAI_API_KEY` > `OPENROUTER_API_KEY` > `VOLCES_API_KEY` > `XAI_API_KEY`

### 分析能力
- **基础分析** (`analyze_product_basic`): 目标受众、使用场景、设计初衷、问题解决、标签、评分、竞品
- **深度分析** (`analyze_product_deep`): 七维框架
  1. problemDefinition (问题定义)
  2. aiIndispensability (AI 不可替代性)
  3. workflowEmbedding (工作流嵌入)
  4. monetization (商业化路径)
  5. moatAnalysis (护城河分析)
  6. competitivePositioning (竞品位势)
  7. fourQuestionsValidation (四问验证)

### 集成状态
- `analyze_product.py`: 优先使用 LLM，失败回退到规则系统
- `weekly_analysis.py`: 深度分析使用 LLM 七维框架

### 环境变量
```bash
# 火山引擎 DeepSeek（当前使用）
ZSH_AI_OPENAI_API_KEY=xxx
ZSH_AI_OPENAI_URL=https://ark.cn-beijing.volces.com/api/v3/chat/completions
ZSH_AI_OPENAI_MODEL=deepseek-v3-2-251201

# 或标准 OpenAI
OPENAI_API_KEY=xxx
OPENAI_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```

## 工作偏好

- 使用中文沟通
- Python 优先使用 `/opt/homebrew/bin/python3`
- 不提交密钥、令牌到代码库
- 提交信息使用 Conventional Commits
- 每次修改后重建 `docs/` 并推送 GitHub Pages

## 技术约束

- 本机有 GVM/RVM 配置，可能影响命令执行
- Homebrew Python 环境有 PEP 668 限制（禁止直接 pip install）
- products.json 是对象包装结构，读取时需要 `data['products']`
- webshot.site 截图服务可能返回 429/500，需要容错

## 已知问题

- **product_id 自动去重失效**：raw-candidates 的 `product_id`（如 `producthunt.com/r/p/1154630`）与数据库 `products[].id`（如简短 slug）格式不一致，导致基于 product_id 的自动去重始终为 0。当前解决方案：执行流程中增加 LLM 分析阶段手动检查近期报告中的精选产品，排除已推荐的项目。(2026-05-28)
- **Reddit JSON API 已被禁止**：Reddit 对未认证请求返回 403 HTML。解决方案：改用 RSS feed（`.rss`）解析，已修复并验证可用。(2026-06-08)
- **PH 页面 Cloudflare 保护**：Product Hunt 详情页被 Cloudflare 保护，无法通过 WebFetch 直接抓取。URL 验证改为通过搜索引擎查找产品官网。(2026-05-29)
- **gh-pages subtree split 失败**：`subtree split` 后 `push origin gh-pages` 报 "not an ancestor" 错误。解决方案：改用 `git push origin $(subtree split --prefix=docs):gh-pages --force` 一步完成。(2026-05-30)
- **字段路径纠正**：自动任务脚本中 `recommendedInDaily` 实际字段为 `metrics.featuredInDaily`，`featuredInWeekly` 为 `metrics.featuredInWeekly`。评分字段为 `analysis.score`。(2026-06-02)
- **周报 JSON 缺失字段**：手动写入周报 JSON 时容易遗漏 `sourceDailyReport` 和 `growthMetrics` 字段，导致详情页"近 7 天提及"和"增长分数"显示为 0。这两个字段由 `weekly_analysis.py` 正常流程生成，手动写报告时需补充。(2026-06-02)

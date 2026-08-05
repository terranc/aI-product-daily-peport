# AI Product Radar - 长期记忆

## 项目架构

- **项目类型**: AI Product Radar - 多平台 AI 产品抓取、分析、去重、每日精选、每周深度分析
- **数据源**: Hacker News, Reddit, Product Hunt, Twitter, V2EX
- **产品数据库**: `data/products.json`（结构: `{version, lastUpdated, products: [], tracking: []}`）
- **日报输出**: `reports/daily/`
- **周报输出**: `reports/weekly/`
- **静态站点**: `docs/`（通过 `scripts/build_site.py` 生成）
- **GitHub Pages**: https://ai-daily.asdasd.vip

## 站点功能：产品标星 (2026-07-15)

- 基于浏览器 localStorage 的产品收藏功能（无后端），key 为 `ai_radar_starred`，存 slug 数组
- 产品详情页 detail-actions 区有标星按钮（`btn-star` + `data-slug` + `onclick="toggleStar(this)"`）
- 顶部导航有「星标」入口 + 数量徽章（`.star-count-badge`，JS 动态更新）
- `starred.html` 星标列表页：fetch `all-products.json` + localStorage 过滤渲染，支持取消标星与实时同步
- 共享 `STAR_JS` 常量在详情页/首页/周报/星标页统一注入；Modal 注入 DOM 后手动 `initStarButtons()`（解决动态注入不执行 script）
- 相关代码在 `scripts/build_site.py` 的 `STAR_JS` 常量、`header_html()`、`render_product_detail_content()`、`generate_starred_page()` 中
- 星标列表页点击产品用 Modal 打开详情（与首页一致）：共享 `MODAL_CORE_JS`/`MODAL_CSS`/`MODAL_HTML` 常量，事件委托绑定 `.product-item a[href]`

## LLM 分析引擎 (2026-05-23)

已完成从"关键词匹配"到"LLM 驱动"的策略升级：

### 核心模块
- **`scripts/llm_analyzer.py`**: LLM 分析引擎
  - 基于 requests 直接调用 OpenAI API（无需 openai SDK）
  - 支持多 Provider 自动检测：OpenAI、火山引擎 DeepSeek、OpenRouter、xAI Grok
  - 环境变量优先级：`OPENAI_API_KEY` > `ZSH_AI_OPENAI_API_KEY` > `OPENROUTER_API_KEY` > `VOLCES_API_KEY` > `XAI_API_KEY`
  - 已集成到自动化任务中

### 分析能力
- **基础分析** (`analyze_product_basic`): 目标受众、使用场景、设计初衷、问题解决、标签、评分、竞品
- **深度分析** (`analyze_product_deep`): 七维框架
- **自动化筛选**：使用 LLM 能力进行产品筛选和分析
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
- 自动化任务：已集成 LLM 能力进行产品筛选和分析

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
- 自动化任务使用 LLM 能力进行产品筛选和分析

## 技术约束

- 本机有 GVM/RVM 配置，可能影响命令执行
- Homebrew Python 环境有 PEP 668 限制（禁止直接 pip install）
- products.json 是对象包装结构，读取时需要 `data['products']`
- webshot.site 截图服务可能返回 429/500，需要容错
- LLM 分析需要环境变量配置（OPENAI_API_KEY 等）

## 已知问题

- **product_id 自动去重失效**：raw-candidates 的 `product_id`（如 `producthunt.com/r/p/1154630`）与数据库 `products[].id`（如简短 slug）格式不一致，导致基于 product_id 的自动去重始终为 0。当前解决方案：执行流程中增加 LLM 分析阶段手动检查近期报告中的精选产品，排除已推荐的项目。(2026-05-28)
- **数据库去重有效**：当前数据库中已有 60 个有效去重记录，可以正常排除 14 天内已推荐的产品。(2026-06-18)
- **Reddit JSON API 已被禁止**：Reddit 对未认证请求返回 403 HTML。解决方案：改用 RSS feed（`.rss`）解析，已修复并验证可用。(2026-06-08)
- **PH 页面 Cloudflare 保护**：Product Hunt 详情页被 Cloudflare 保护，无法通过 WebFetch 直接抓取。URL 验证改为通过搜索引擎查找产品官网。(2026-05-29)
- **gh-pages subtree split 失败**：`subtree split` 后 `push origin gh-pages` 报 "not an ancestor" 错误。解决方案：改用 `git push origin $(subtree split --prefix=docs):gh-pages --force` 一步完成。(2026-05-30)
- **gh-pages 部署成功**：使用一步命令成功部署到 GitHub Pages，网站已更新。(2026-06-18)
- **字段路径纠正**：自动任务脚本中 `recommendedInDaily` 实际字段为 `metrics.featuredInDaily`，`featuredInWeekly` 为 `metrics.featuredInWeekly`。评分字段为 `analysis.score`。(2026-06-02)
- **LLM 分析能力**：已成功使用 LLM 能力进行产品筛选和分析，生成深度分析报告。(2026-06-18)
- **周报 JSON 缺失字段**：手动写入周报 JSON 时容易遗漏 `sourceDailyReport` 和 `growthMetrics` 字段，导致详情页"近 7 天提及"和"增长分数"显示为 0。这两个字段由 `weekly_analysis.py` 正常流程生成，手动写报告时需补充。(2026-06-02)
- **日报生成成功**：已成功生成 2026-06-18 日报，包含 5 个精选产品。(2026-06-18)
- **日报生成成功**：已成功生成 2026-06-19 日报，包含 5 个精选产品（Adapt、VoiceOS、AudienceCue、ClawEase、Dopami）。(2026-06-19)
- **日报生成成功**：已成功生成 2026-06-27 日报，包含 5 个精选产品（Swimio、Dub Ninja、Tough Tongue AI、CubeOne、Nimt）。(2026-06-27)
- **产品数据库更新**：数据库已更新至 227 个产品。(2026-06-27)
- **日报生成成功**：已成功生成 2026-07-14 日报，包含 5 个精选产品（Toyo、RepStandard、Breathing In Labour、Melodusk、ConnectMachine 2.0）。(2026-07-14)
- **产品数据库更新**：数据库已更新至 252 个产品（新增 5 个）。(2026-07-14)
- **产品数据库更新**：数据库已更新至 257 个产品（新增 5 个：VocalVia、Breva、DayReplay、ClipFlow、NeuralLen）。(2026-07-15)
- **日报生成成功**：已成功生成 2026-07-22 日报，包含 5 个精选产品（NeuroVidz、Backbeat Forge、Kogvio、Sorted Receipts、KaCutAI）。(2026-07-22)
- **产���数据库更新**：数据库已更新至 282 个产品（新增 5 个）。(2026-07-22)
- **日报生成成功**：已成功生成 2026-07-30 日报，包含 5 个精选产品（SoundGate Guitar、ClinicFrame、Edit Mind × Strava、Totem、AI私厨）。(2026-07-30)
- **产品数据库更新**：数据库已更新至 317 个产品（新增 5 个）。(2026-07-30)
- **日报生成成功**：已成功生成 2026-07-31 日报，包含 5 个精选产品（Keepers、Pally、CraftStory、Caimera、Fretseek）。(2026-07-31)
- **产品数据库更新**：数据库已更新至 322 个产品（新增 5 个）。(2026-07-31)
- **截图脚本 appStoreUrl 误解析**：当产品 URL 是 App Store 链接时，`process_product_screenshots` 可能把页面中其他 app 的链接解析进 appStoreUrl（如 Keepers ���解析成清洁工 app）。需要在写入报告前手动修���为产品自身的 App Store URL。(2026-07-31)
- **URL 验证经验**：PH 候选若通过搜索引擎无法确认官网（同名产品过多或无官网），应直接替换为官网可验证的产品，不要保留无法确认的 URL。(2026-07-31)
- **日报生成成功**：已成功生成 2026-08-02 日报，包含 5 个精选产品（Focus Room、Halo by Scam AI、Kopai、AI Google Earth、Dopamind）。(2026-08-02)
- **产品数据库更新**：数据库已更新至 327 个产品（新增 5 个）。(2026-08-02)
- **App Store 同名不同产品陷阱**：iTunes 搜索按名称匹配可能返回同名但不同的 app（如 Dopamind 被解析为 DopaMind LLC 的 id6738889403，官方实为 id6747915249）。写入报告前需用 iTunes lookup 核对 sellerName 与版本号，确认与产品官网下载页一致。(2026-08-02)
- **手动排除跨渠道重复**：同一产品在不同渠道的 product_id 不同（如 Honen 的 Twitter 推文 URL vs 官网域名），自动去重无法覆盖。需在 LLM 分析阶段手动检查近期精选产品名称，排除重复推荐。(2026-08-02)
- **日报生成成功**：已成功生成 2026-08-03 日报，包含 5 个精选产品（Zinley、NudgeForMe、AI Visibility、PulseNotch、MovePlaybook）。(2026-08-03)
- **产品数据库更新**：数据库已更新至 332 个产品（新增 5 个）。(2026-08-03)
- **官网验证新陷阱**：域名返回 200 不一定是产品官网——zenwhisper.com 实为域名售卖页（DomainMarket）。验证官网时需检查页面内容与产品描述是否匹配，不能只看 HTTP 状态码。(2026-08-03)
- **截图脚本文件名 unknown 问题**：`process_product_screenshots` 用 `product.get('id')` 生成截图文件名，若传入 dict 只有 `product_id` 字段则文件名为 `unknown_*`。调用时需同时传 `id` 字段或事后重命名。(2026-08-03)
- **部署验证 CDN 延迟**：push gh-pages 后 GitHub 官方域名（terranc.github.io）即时 200，自定义域名（ai-daily.asdasd.vip）有约 2-3 分钟 CDN 缓存延迟，验证时需等待或直接用官方域名确认。(2026-08-03)
- **周报生成成功**：已成功生成 2026-08-03 周报，深度分析 Zinley - AI 个人代表（评分 9）。PH 首发 325 upvotes/79 评论双榜第一；三件套（号码+邮箱+云端电脑）端到端落地；Real-World Reasoning 判断层 91% 准确率；定价 Free/Plus $20/Pro $100/Max $200。(2026-08-03)

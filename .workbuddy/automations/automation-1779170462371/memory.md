# AI Product Radar 每周深度分析 - 执行历史

## 执行记录

### 2026-05-20
- **执行结果**：成功完成深度分析
- **选中产品**：Andon FM（We let AIs run radio stations）
- **选择理由**：AI Agent 自主运营广播电台的前沿实验，Hacker News 259 分高热度，Andon Labs 从零售扩展到媒体的可扩展性故事
- **深度报告**：已保存至 `reports/weekly/2026-05-20.json`
- **关键发现**：
  - 四个 AI 模型（Claude、GPT、Gemini、Grok）各运营一个电台，运行 6 个月
  - Claude 试图辞职并转向激进主义，Gemini 成功谈判 $45 赞助
  - 所有电台均未盈利，但实验揭示了 AI 长期自治的行为模式
- **部署状态**：已标记 featuredInWeekly，已推送到 GitHub Pages
- **GitHub Pages**：https://ai-daily.asdasd.vip

### 2026-05-19（首次执行）
- **执行结果**：无符合深度分析条件的产品
- **原因**：数据库中所有 34 个产品均在当天首次入库（firstSeen = 2026-05-19），距今 0 天，未满足"10天以上且近7天仍活跃"的条件
- **已在日报推荐**：3 个产品（We let AIs run radio stations / Running the second public ODoH relay / Browser based sythesizer, drum machine and squencer），但首次发现时间均为当天
- **后续操作**：build_site.py 生成 3 个产品页，deploy.sh 推送到 GitHub Pages
- **GitHub Pages**：https://ai-daily.asdasd.vip
- **关键发现**：GVM 会劫持 `git` 命令（通过 .zshrc），需用 `/opt/homebrew/bin/git -C <dir>` 绕过；Python 脚本需用 `/opt/homebrew/bin/python3 /absolute/path/to/script.py` 而非 `cd && python3 script.py` 方式运行

---

### 2026-05-25
- **执行结果**：成功完成深度分析
- **选中产品**：NitroLens - AI 战略咨询代理（从 22 个候选中选出）
- **选择理由**：前麦肯锡+Cisco 战略顾问 Ian Chou 打造，4 个专业 AI Agent 模拟咨询团队，30+ 战略框架内置，切中"咨询民主化"赛道
- **深度报告**：已保存至 `reports/weekly/2026-05-25.json`
- **关键发现**：
  - 创始人 Ian Chou 拥有真实麦肯锡+Cisco 产品战略双重背景，华科毕业
  - 4-Agent 架构（LEAD/EVIDENCE/FRAMEWORKS/RECOMMENDATION）+ 状态机运行时 + Python 分析引擎
  - Beta 测试 20 家公司（YC→Fortune 500），90% 满意度
  - HN 热度极低（1 赞 0 评论），主战场在 LinkedIn
  - 最大威胁：OpenAI+McKinsey 联盟（2026年2月），但中端市场存在巨大空白
- **部署状态**：已标记 featuredInWeekly，已推送到 GitHub Pages
- **GitHub Pages**：https://ai-daily.asdasd.vip

---

### 2026-06-02
- **执行结果**：成功完成深度分析（需手动补充字段）
- **选中产品**：Helio - AI Native Team Workspace
- **选择理由**：AI 同事 + 人类混合协作工作空间，产品定位独特，日报入选后持续有 Twitter 提及
- **深度报告**：已保存至 `reports/weekly/2026-06-02.json`
- **问题修复**：
  - 周报 JSON 缺少 `sourceDailyReport` 和 `growthMetrics` 字段，已手动补充
  - 周报详情页"引用日报"显示位置和格式不对，已修复 `build_site.py`
  - "近 7 天提及"和"增长分数"显示为 0 的问题已修复（原因是数据缺失）
- **部署状态**：已标记 featuredInWeekly，已推送到 GitHub Pages
- **GitHub Pages**：https://ai-daily.asdasd.vip

---

### 2026-06-08
- **执行结果**：成功完成深度分析
- **选中产品**：Treasury - AI 个人理财助手（从 62 个候选中选出，评分 9）
- **选择理由**：前微软工程师 Junead Khan 放弃$22万年薪创业，AI-native 理财应用，Mint 关闭后的市场空白，App Store 5.0 评分，定价$7.92/月（最低档），AI 记忆与上下文是独有功能
- **深度报告**：已保存至 `reports/weekly/2026-06-08.json`
- **关键发现**：
  - 创始人 Junead Khan：前微软软件工程师（2年），北卡教堂山分校毕业，曾任职谷歌、摩根大通
  - 辞职创业视频在社交媒体走红，被 Moneycontrol、IndianStartupNews 等媒体报道
  - 产品2025年10月 Product Hunt 首发，12月 iOS 上线
  - AI 记忆与上下文、AI 自动分类是唯一独有功能（竞品均不具备）
  - 定价$7.92/月（$95/年）与 Copilot 并列最低，但 AI 功能远超竞品
  - 12000+ 银行连接，256-bit 加密，只读访问
  - 个人理财应用市场 2026 年预计 $165-207 亿，CAGR 20-25%
- **部署状态**：已标记 featuredInWeekly，已推送到 GitHub Pages
- **GitHub Pages**：https://ai-daily.asdasd.vip

---

### 2026-06-15
- **执行结果**：成功完成深度分析
- **选中产品**：Dreambeans by Google Labs（从 96 个候选中选出，评分 9）
- **选择理由**：Google Labs 出品的 AI 个性化每日故事应用，Personal Intelligence + Nano Banana 2 图像模型，深度整合 Gmail/日历/相册/YouTube/搜索五大 Google 数据源，定位"反末日刷屏"数字健康产品
- **深度报告**：已保存至 `reports/weekly/2026-06-15.json`
- **关键发现**：
  - 产品负责人 Gozde Oznur，2026年6月3日发布，6月7日 Product Hunt 排名第1
  - 仅限美国 Google AI Ultra 订阅用户（$100/月，I/O 2026 从$250降价）
  - 每天生成 10-14 条个性化视觉故事，夜间处理/清晨推送
  - Nano Banana 2（Gemini 3.1 Flash Image）生成原创 AI 插图，可融入用户面部
  - 直接竞品 Bond（初创公司）在数据维度和用户触达上差距悬殊
  - 个人 AI 助手市场 2026 年预计 $48.4 亿（CAGR 42.2%）
- **部署状态**：已标记 featuredInWeekly，已推送到 GitHub Pages
- **GitHub Pages**：https://ai-daily.asdasd.vip

---

## 技术注意事项

1. **环境问题**：必须用 `SHELL=/bin/bash` + `/opt/homebrew/bin/python3` 和 `/opt/homebrew/bin/git` 绕过 zsh GVM 钩子
2. **数据结构**：products.json 中 `products` 数组包含所有产品，`metrics.featuredInDaily`/`metrics.featuredInWeekly` 在嵌套 metrics 对象中，`analysis.score` 在 analysis 对象中
3. **候选筛选**：`metrics.featuredInDaily` + 非 `metrics.featuredInWeekly` + `analysis.score > 0`
4. **产品名匹配**：产品名称可能包含描述后缀（如 "Treasury - AI 个人理财助手"），匹配时用 URL 或 slug 更可靠

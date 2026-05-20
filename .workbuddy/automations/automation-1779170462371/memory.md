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
- **GitHub Pages**：https://terranc.github.io/aI-product-daily-peport/

### 2026-05-19（首次执行）
- **执行结果**：无符合深度分析条件的产品
- **原因**：数据库中所有 34 个产品均在当天首次入库（firstSeen = 2026-05-19），距今 0 天，未满足"10天以上且近7天仍活跃"的条件
- **已在日报推荐**：3 个产品（We let AIs run radio stations / Running the second public ODoH relay / Browser based sythesizer, drum machine and squencer），但首次发现时间均为当天
- **后续操作**：build_site.py 生成 3 个产品页，deploy.sh 推送到 GitHub Pages
- **GitHub Pages**：https://terranc.github.io/aI-product-daily-peport/
- **关键发现**：GVM 会劫持 `git` 命令（通过 .zshrc），需用 `/opt/homebrew/bin/git -C <dir>` 绕过；Python 脚本需用 `/opt/homebrew/bin/python3 /absolute/path/to/script.py` 而非 `cd && python3 script.py` 方式运行

---

## 技术注意事项

1. **环境问题**：必须用 `/opt/homebrew/bin/python3` 和 `/opt/homebrew/bin/git` 绕过 GVM 环境劫持
2. **数据结构**：products.json 中 `products` 数组包含所有产品，字段 `metrics.featuredInWeekly` 控制是否已周刊推荐
3. **候选筛选**：`recommendedInDaily` + 非 `featuredInWeekly` + `score > 0`

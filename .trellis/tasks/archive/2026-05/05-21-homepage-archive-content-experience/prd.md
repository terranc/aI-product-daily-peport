# 规划首页与归档长期内容体验

## Goal

当日报和产品数量长期增长后，保持首页轻量、历史内容可浏览、产品内容可检索，避免未来内容堆积后再大幅重构信息架构。

## Requirements

- 首页继续作为“最近发现”入口，只展示最近 14 期日报；旧内容不继续出现在首页。
- 历史归档页承接全部日报历史，并优化为按年/月分组浏览，避免单张表格无限增长后难以扫描。
- 增加或规划“产品库”入口，用于浏览全部产品，支持关键词搜索、标签筛选，并通过分页或“查看更多”控制一次展示数量。
- 导航结构需要让用户能清楚区分：每日简报、产品库、每周深度、历史归档。
- 方案应优先适配当前 GitHub Pages 静态站架构，复用现有 `reports/daily/`、`docs/all-products.json`、产品详情页和站点构建脚本。
- 暂不引入后端服务、数据库搜索服务或复杂索引系统；等产品规模明显增大后再评估按年/月拆分数据文件。
- 本任务目前只记录计划，不立即修改站点实现。

## Acceptance Criteria

- [ ] 首页仍只渲染最近 14 期日报，历史日报不会让首页持续变长。
- [ ] 归档页可以按年/月组织所有日报，并保留每期产品链接。
- [ ] 产品库可以从全部产品中搜索、按标签筛选，并限制首屏/单次加载数量。
- [ ] 导航中存在清晰入口，用户能从首页进入产品库和归档。
- [ ] 静态站构建后 `docs/` 输出完整，GitHub Pages 可直接部署。
- [ ] 若未来开始实现，先补充 `design.md` 和 `implement.md`，经 review 后再进入 implementation。

## Notes

- Current observed behavior: `scripts/build_site.py` 的首页生成逻辑使用 `recent = reports[:14]`，周报页显示最近 10 期，标签页已有基于 `all-products.json` 的批量加载雏形。
- Recommended future approach: keep homepage capped, upgrade archive grouping, add a dedicated product library/search page before content volume becomes large.
- Scope intentionally excludes implementing the UI/code in this turn.

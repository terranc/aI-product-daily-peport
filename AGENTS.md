# AI Product Radar 项目记忆

## 项目背景

- 项目从 WorkBuddy 迁移而来，旧目录为 `/Users/terranc/WorkBuddy/2026-05-19-task-19`，不要修改旧目录内容。
- 当前项目路径为 `/Volumes/EXTEND/aI-product-daily-peport`。
- GitHub 仓库为 `terranc/aI-product-daily-peport`。
- GitHub Pages 地址为 `https://terranc.github.io/aI-product-daily-peport/`。
- 自定义域名历史记录为 `https://ai-daily.asdasd.vip/`。

## 功能范围

- 这是一个 AI Product Radar：多平台 AI 产品抓取、LLM 分析、去重、每日精选、每周深度分析、静态网站生成与部署。
- 数据源包括 Hacker News、Reddit、Product Hunt、Twitter、V2EX；旧 WorkBuddy 记忆里也提到过 GitHub 与 Exa 辅助检索。
- 产品数据库在 `data/products.json`，结构包含 `products` 数组，不是直接数组。
- 日报输出在 `reports/daily/`，周报输出在 `reports/weekly/`。
- 静态站点生成脚本是 `scripts/build_site.py`，站点输出目录是 `docs/`。

## 运行注意事项

- 用户本机 shell 里有 GVM/RVM 相关配置，可能影响命令执行。必要时优先使用 `/opt/homebrew/bin/python3` 和 `/opt/homebrew/bin/git` 的绝对路径。
- 对需要完整用户环境的命令不要盲目使用 `env -i`，例如 `twitter-cli` 曾在精简环境下超时。
- JSON 报告务必通过结构化写入生成，例如 Python `json.dump()`，不要手写包含中文引号或特殊字符的大段 JSON。
- `products.json` 与 `raw-candidates.json` 都可能是对象包装结构，读取时先确认是否需要取 `.products`。
- `product_id` 或 slug 可能包含 `/` 等特殊字符，写入文件路径前要清理。
- webshot.site 截图服务可能返回 429 或 500，遇到限流时不要误判为产品数据错误。
- Product Hunt 详情页可能有 Cloudflare 保护，直接抓取失败时优先使用 RSS、搜索结果或其他公开源交叉验证。

## MCP 配置

- 根目录 `.mcp.json` 从旧 WorkBuddy 的 `config/mcporter.json` 迁移而来，但不能写入真实 API key。
- Exa MCP 使用环境变量 `EXA_API_KEY` 注入：`https://mcp.exa.ai/mcp?exaApiKey=${EXA_API_KEY}`。
- 如果 Codex 没有自动读取项目级 `.mcp.json`，可将同等配置写入 `~/.codex/config.toml`：

```toml
[mcp_servers.exa]
url = "https://mcp.exa.ai/mcp?exaApiKey=${EXA_API_KEY}"
```

## 工作偏好

- 默认使用中文沟通。
- 变更尽量小而明确，避免顺手重构无关代码。
- 不提交密钥、令牌、Cookie 或其他凭据。
- 提交信息使用 Conventional Commits，例如 `chore(config): add project mcp config`。

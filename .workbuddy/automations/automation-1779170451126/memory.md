# 自动化执行历史 - AI产品雷达-每日抓取

## 2026-05-19 20:00

- **状态**：✅ 成功
- **抓取数**：57 个候选产品（HN + GitHub + Reddit）
- **去重后**：57 个新鲜候选（无冷却期命中）
- **过滤后**：约 20 个面向用户的产品通过 LLM 筛选
- **精选 TOP 5**：
  1. drea - 播客广告屏蔽器（评分 8）
  2. Lumis - 与斯多葛哲学家对话日记（评分 8）
  3. GetFastVisa - AI 自动化签证预约（评分 8）
  4. Clawputer - 有真实记忆的个人 AI 助手（评分 7）
  5. Zuzu.club - 无账号即时陌生人对话（评分 7）
- **截图**：5 张网站截图全部成功
- **部署**：main + gh-pages 推送成功
- **踩坑**：直接写 JSON 文本含中文书名号会导致解析错误，改用 `json.dump()` 生成

---

## 2026-05-19 22:50（第二次执行）

- **状态**：✅ 成功
- **抓取数**：145 个候选产品（HN 30 + Reddit 60 + Product Hunt 15 + V2EX 40）
- **去重后**：145 个（数据库 39 个冷却期内产品 URL/名称均未命中候选）
- **过滤后**：约 38 个面向用户的产品通过 LLM 初筛
- **精选 TOP 5**：
  1. Saner.AI - ADHD 友好 AI 助手（笔记/邮件/日历整合，评分 9）
  2. PersonalPathways - 每日序列化 AI 故事（评分 8）
  3. Scripod - AI 播客剪辑工具站（评分 8）
  4. Rtriv - 跨 8 平台书签统一管理（评分 7）
  5. BillWatch - 美国联邦法案追踪警报（评分 7）
- **截图**：Saner.AI 和 Scripod 成功（2张），其余 3 个截图服务返回 HTTP 500
- **部署**：main + gh-pages 推送成功
- **踩坑**：
  - raw-candidates.json 结构是 `{"products": [...], "totalCount": N}`，需取 `.products`
  - products.json 结构是 `{"products": [...], "version": ...}`，需取 `.products`
  - cooldownExpiresAt 是不含时区的 ISO 格式，比较时用 `datetime.now(timezone.utc).replace(tzinfo=None)`
  - V2EX 帖子描述中的实际产品 URL 需解析，如播客工具站帖子里才有 scripod.io

---

## 2026-05-20 15:36

- **状态**：✅ 成功
- **抓取数**：225 个候选产品（Twitter 50 + V2EX 39 + Reddit 60 + HackerNews 26 + Product Hunt 50）
- **去重后**：225 个（数据库 50 个冷却期内产品均未命中）
- **过滤后**：精选 5 个面向用户的产品
- **精选 TOP 5**：
  1. Google Pics - AI 图像生成与编辑（Google I/O 2026，评分 9）
  2. Vocabi - 阅读时翻译记忆单词（评分 8）
  3. calog.cc - AI 卡路里追踪器/南亚食物（评分 8）
  4. Krea 2 - 风格控制 AI 图像生成（评分 8）
  5. Motion - AI 视频动态设计代理（评分 7）
- **截图**：webshot.site API 返回 429 限流，截图跳过
- **部署**：main + gh-pages 推送成功
- **踩坑**：
  - product_id 含 `/` 字符导致截图脚本创建子目录失败，需清理特殊字符
  - webshot.site API 限流频繁，需等待 Retry-After 或改用其他截图方案
  - Product Hunt 全站 Cloudflare 保护，WebFetch 无法直接抓取产品详情页

---

## 2026-05-21 12:00

- **状态**：✅ 成功
- **抓取数**：227 个候选产品（Twitter 50 + V2EX 40 + HackerNews 27 + Reddit 60 + Product Hunt 50）
- **去重后**：223 个（数据库 4 个冷却期内产品命中）
- **过滤后**：精选 5 个面向用户的产品
- **精选 TOP 5**：
  1. Avenor - 一键安装AI全能工作区（评分 9）
  2. Drowsebook（入梦书）- 睡前听书/本地阅读App（评分 8）
  3. Poplingo - AI浏览器翻译与沉浸阅读（评分 8）
  4. SongForge Crucible - AI歌词八维诊断工具（评分 8）
  5. Trainy - AI角色扮演产品学习平台（评分 7）
- **截图**：5 张网站截图全部成功
- **部署**：main + gh-pages 推送成功
- **踩坑**：Twitter 推文页面加载经常出错，需要通过搜索找到产品实际官网 URL

---

## 2026-05-22 12:00

- **状态**：✅ 成功
- **抓取数**：229 个候选产品（Twitter 50 + V2EX 40 + HackerNews 29 + Reddit 60 + Product Hunt 50）
- **去重后**：229 个（数据库 49 个冷却期内产品均未命中候选）
- **过滤后**：精选 5 个面向用户的产品
- **精选 TOP 5**：
  1. Invenio - 本地AI搜索Mac视频和照片库（评分 8）
  2. AutoSubtitles 2.0 - AI字幕和动画字幕生成器（评分 8）
  3. AI Local Recorder - 离线语音录音器+AI转写（评分 8）
  4. Framed - 将截图/视频/代码变成精美视觉素材（评分 7）
  5. GhostSnap - 多张截图一次粘贴AI自动压缩（评分 7）
- **截图**：5 张网站截图全部成功
- **部署**：main + gh-pages 推送成功
- **踩坑**：无新增踩坑

---

## 注意事项（供下次执行参考）

- git/python 命令需用 `env -i HOME=$HOME PATH=...` 避免 GVM 劫持
- JSON 报告务必用 `json.dump()` 生成，不要手写包含中文引号的 JSON 字符串
- drea App Store 搜索有可能命中同名游戏，需注意核验应用名称匹配
- Twitter 推文页面（x.com）经常返回加载错误，需通过 WebSearch 找到产品实际官网

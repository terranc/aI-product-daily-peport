#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate weekly report for Wispr Flow - clean UTF-8 output."""

import json

data = {
    "date": "2026-07-27",
    "generatedAt": "2026-07-27T12:25:14+08:00",
    "productCount": 1,
    "type": "weekly",
    "sourceDailyReport": "2026-07-26",
    "products": [
        {
            "id": "producthunt.com/r/p/1203598",
            "name": "Wispr Flow - AI语音输入",
            "slug": "wispr-flow",
            "description": "Wispr Flow 是一款系统级的 AI 语音转文字工具，支持 Mac、Windows、iOS 和 Android。按住快捷键说话，松开即获得完美格式的文本。核心差异在于 AI 后处理引擎——自动去除填充词、修正语法、补充标点、根据应用上下文调整语气，实现「零编辑」的语音输入体验。支持 100+ 种语言和代码混合输入，拥有 Command Mode 语音编辑、Snippet Library 快捷短语和团队共���词典等高级功能。定价 $15/月（Pro），企业版支持 SOC 2 Type II 和 HIPAA 合规。",
            "url": "https://wisprflow.ai",
            "homepage": "https://wisprflow.ai",
            "type": "app",
            "tags": ["语音输入", "AI写作", "���率工具", "跨平��", "语音转文字", "AI生产力", "无障碍"],
            "sourceChannels": ["producthunt"],
            "sourceUrl": "https://www.producthunt.com/r/p/1203598",
            "firstSeen": "2026-07-26T04:31:13.735725+00:00",
            "analysis": {
                "targetAudience": "知识工作者、程序员、内容创作者、企业管理者、律师、医疗从业者、学生、非母语英语使用者以及因残疾无法便捷使用键盘的���群",
                "useCases": [
                    "跨平台语音输入——在 Slack、Gmail、Notion、Google Docs、VS Code、Cursor、ChatGPT 等任何应用的文本框中说话即可输入，无需切换应用",
                    "AI 提示词工程——用语音快速撰写长篇 Prompt，60 秒说完 400 字，结合 Command Mode 精细��编辑",
                    "开发者编程辅助——在 Cursor、VS Code、Warp 终端中用语音写代码注释、文档和命令��支持 camelCase/snake_case 语法感知",
                    "企业文档批量处理——邮件回复、周报编写、客户沟通等高频文字工作，速度提升 4 倍（220 WPM vs 45 WPM）",
                    "多语言混合输入——在英语和母语之间自由切换，Flow 自动检测语言并保持上下文一致性",
                    "无障碍辅助——帮助 RSI（��复性劳损）、帕金森等运动障碍用户通过���音完成文字输入"
                ],
                "designIntent": "创始人 Tanay Kothari 10 岁看《钢铁侠》时就梦想建造 JARVIS���最初从 BCI 硬件可穿戴设备（读神经信号打字）起步，2021 年创立 Wispr，2024 年中果断转型软���。核心理念是「语音应该成为���键盘之后的默认输入层」，让技术交互像人与人对话一样���然。产品设计围绕「零编辑」体验展开：系统级集成（无需切换应用）、AI 自动后处理（去除口语冗余）、上下文感知（不同应用不同语气）、隐私可配置（零数据保留模式）。",
                "problemSolved": "传统语音输入面临三大痛点：(1) 准确率低——专业术语、多语言混合场景和噪音环境下表现差；(2) 输出质量差——口语中的填充词（um/uh）、颠三倒四的语序需要大量人工��辑；(3) 平台割裂——不同设备间的语音输入体验差异巨大。Wispr Flow 通过「AI 后处理 + 全平台覆盖 + 个人词典自学习」三位一体方案解决这些问题，将语音输入从「应急方案」升级为「主力输入方式」。",
                "score": 8,
                "scoreReason": "【深度调研亮点】(1) 创��团队硬核又浪漫——Tanay Kothari（Delhi->Stanford CS+AI 硕士，前 Forbes 30 Under 30，TA Andrew Ng 深度学习课）和 Sahaj Garg（Stanford AI Lab，Google Research 发表论文），从 BCI 硬件果断转型软件，经历堪称硅谷最经典 pivot 故事。(2) 增长数据亮眼——40% 月环比增长、100x 年同比增长、19% 付费率（行业平均 3-4%）、80% 六个月留存、270+ 财富 500 强企业使用，这些数字在 SaaS 领域极为罕见。(3) 硅谷核心圈口碑——Reid Hoffman（LinkedIn 联合创始人）公开 voicepilled，Marc Andreessen 和 Steve Wozniak 日活用户，Superhuman CEO Rahul Vohra 称「自 ChatGPT 以��最好的 AI 产品」。(4) 全套合规���证——SOC 2 Type II、ISO 27001、HIPAA BAA，企业级信任基础已建���。(5) 赛道意义——语音输入是 AI 应用市场规模最大的赛道之一，微软 Nuance Dragon 年收入超 10 亿美元，Wispr 从 BCI 硬件到语音软件的转型把握���「语音优先」的长期趋势。(6) 风险点——Trustpilot 2.7/5 评分反映试用到付费后的可靠性下降问题；云处理架���意味着数据隐私仍是用户顾虑；$15/月定价在���品类产品中最高，且无终身买断选项。",
                "competitors": [
                    {"name": "Apple 系统听写", "url": "https://support.apple.com", "comparison": "Apple 原生听写免费、Apple Silicon 本���处理（低延迟无隐私担忧），但功���最基础——无 AI 后处理、无填充词去除、无上下文感知语气调整。Wispr 在输出质量和平台覆盖面（Win/Android）上显著领先，但价格是 Apple 的 0 元。"},
                    {"name": "Superwhisper", "url": "https://superwhisper.com", "comparison": "Superwhisper 主打本地处理（Whisper 模型本地运行），隐私更优且支持离线使用。但平台覆盖面窄（Mac 为主），AI 后处理不如 Wispr 强大，$8.49/月或 $249 终身买断。选择在于「离线隐私 vs 云���理质量」之间权衡。"},
                    {"name": "Spokenly", "url": "https://spokenly.app", "comparison": "Spokenly 提供免费本地 Parakeet/Whisper 模型 + BYOK 云 API 方案，灵活性和���价比高（$9.99/月）。但无系统级集成，需要手动复制粘贴。Wispr 的 OS 级热键集成是核���体验差异点。"},
                    {"name": "Nuance Dragon", "url": "https://www.nuance.com/dragon.html", "comparison": "Dragon 深耕医疗/法律行业 20+ 年，垂直领域词库和合规性无出其右。Wispr 走消费级和企业级双路线，创新速度更快、定价更低，但在专业垂直领域的话语权远不如 Dragon。"},
                    {"name": "MacWhisper", "url": "https://goodsnooze.gumroad.com/l/macwhisper", "comparison": "MacWhisper 以 EUR 59 终���买断价格完胜 Wispr ��� $144/年订阅制。但功能局限在文件转录而非系统级实时听写，更多是「批量转写工具」而非「输入替代方案」。"},
                    {"name": "Aqua Voice", "url": "https://aqua.voice", "comparison": "Aqua Voice 是 Wispr Flow 最直接的同品类竞品，同样聚焦 AI 语音输入和跨平台体验。Wispr 在前沿功能（Command Mode、Snippet Library）和企业化程度（270 家财富 500 强 vs 初创阶段）上领先。"}
                ]
            },
            "weeklyDeepDive": {
                "growthData": "Wispr 成立于 2021 年，从 BCI 硬件可穿戴设备起步（识别无声口型->文字），2024 年中转型软件语音输入���2024 年 10 月 Mac 版发布即登顶 Product Hunt 日/周榜第一。2025 年 6 月完成 $30M Series A（Menlo Ventures 领投，NEA、8VC 参与），估值约 $4.2 亿；2025 年 11 月完成 $25M Series A extension（Notable Capital 领投���Flight Fund 参与），估值达 $7 亿。总融资 $81M。关键指标：40% MoM 增长（2025.6 起）、100x YoY、ARR 约 $10M（2025.10）、270+ 财富 500 强企业客户、单周新增 125 家、6 月留存率 80%、19% 付费转化率、每周 1 亿+ 词语音处理量。Android 版尚未正式商业化（Beta 期免费），375K 预约用户排队。团队约 50 人。",
                "communityActivity": "社区讨论集中在 Reddit（r/Mac、r/productivity���和 Product Hunt 的评论/评测板块。正面反馈：「AI Cleanup 是魔法」「上下文感知无与伦比」「最佳 onboarding ���验」；负面反馈集中在：Trustpilot 评分 2.7/5——用户反映从免费试用转为付费后可靠性下降，「自动修复」功��偶尔过度编辑准确���容；隐私争议重提——Context Awareness 截图上传功能默认开启，部分用户获知后感到不安。不���创始人直接回应 Reddit 社区，修复了资源占用、数据保留等问题，并将模型训练改为 Opt-in。目前口碑正在回升。",
                "updateFrequency": "Wispr Flow 保持每月至少一次功能性更新的节奏。关键里���碑：2024.10 Mac 首发 -> 2024.12 Windows 版 -> 2025.1 iOS App -> 2025.3 Warp 终端集成 -> 2025.6 Series A -> 2025.10 Privacy Mode 发布 -> 2025.11 Series A Extension -> 2026.2 Android Beta 版。���度更新包括：语音模型优化（准确率持续提升）、新语言支持、Snippet Library 增强、Teams 管理面板。未来路线图：Wispr Actions（语音驱动自动化工作流，2026 年底���）、自定义 AI 模型、混合本地/云端处理能力。",
                "marketPosition": "Wispr Flow 在 AI 语音输入市场中定位为「跨平台消费级 + 企业级并行」的领导者。核心竞争壁垒：(1) OS 级系统集成——在任何应用的任意文本框中直接语音输入，无需复制���贴，这是竞品不具备的体验。(2) AI 后处理精度——10% 错误率 vs Apple 47%、OpenAI Whisper 27%，差距显著。(3) 合规护城河——SOC 2 Type II、ISO 27001、HIPAA，企业采购的标准门槛。(4) 团队背景吸金能力——斯坦福 AI Lab 出身 + 硅谷顶级 VC 背书，人才和资本资源充足。2026 年 AI 语音输入市场快速扩增，Apple/Google/Microsoft 免���内置方案是最大威胁，Wispr 的答案是��续提升付费体验差距——让「免费方案够用，但 Wispr ���用到回不去」。",
                "differentiation": "Wispr Flow 的核���差异化优势有五层：第一，OS 级热键集成——按住 Fn/Ctrl+Win+Alt 在任何应用说话，松开即得完美文本，这一「瞬移式」体验是 Superwhisper 等竞品不具备的。第二，AI 后处理引擎——不是简单的语音转写，而是用微调 Llama 模型理解口语句子结构、去除填充词、修正自行纠正、补充标点、按应用调整���气，实现真正「零编辑」。第三，跨平台四端同步——Mac/Windows/iOS/Android 四端覆盖，私有词典、Snippet、风格设置跨设���同步，是目前市场上唯一实现这一点的产品。第四，企业合规先行——SOC 2 Type II、ISO 27001、HIPAA 全套认证，让语音输入��入受监管行业���医疗、法律、金融）成为可能。第五，社区驱动的进化——创始人 Tanay 在 Product Hunt 和 Reddit 上重度参与���户反馈，从删除 viral Reddit thread 的早期错误到后来诚恳道歉并修复问题，这一改错历程本身也构成了品牌信任故事的一部分。"
            }
        }
    ]
}

with open('reports/weekly/2026-07-27.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print('Written successfully')

# Verify
with open('reports/weekly/2026-07-27.json', 'r', encoding='utf-8') as f:
    content = f.read()
count_fffd = content.count('\ufffd')
print(f'U+FFFD count: {count_fffd}')

# Check for ASCII control chars in the CJK range
import re
# Find any non-ASCII char that could be garbled
if count_fffd == 0:
    print('All clean! PURE UTF-8')
else:
    print(f'Warning: {count_fffd} garbled chars remain')

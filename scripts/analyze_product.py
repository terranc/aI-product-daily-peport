#!/usr/bin/env python3
"""
产品 AI 分析脚本
使用 LLM 分析产品，生成深度洞察
"""

import json
import re

# 分析提示词模板
ANALYSIS_PROMPT = """请分析以下 AI 产品，提供结构化分析：

产品名称: {name}
产品描述: {description}
产品链接: {url}
来源: {source}

请提供以下分析（返回 JSON 格式）：

1. targetAudience: 目标受众群体（一句话描述）
2. useCases: 具体应用场景（3-5个点）
3. designIntent: 产品设计初衷和理念
4. problemSolved: 解决的核心问题
5. tags: 标签列表（3-5个，从类别、技术栈、目标用户等维度）
6. score: 综合评分（1-10分，基于创新性、实用性、市场潜力）
7. scoreReason: 评分理由（2-3句话）
8. competitors: 竞品分析（2-3个直接竞品，包含名称、网址、对比要点）

返回格式必须是有效的 JSON：
{{
  "targetAudience": "...",
  "useCases": ["...", "..."],
  "designIntent": "...",
  "problemSolved": "...",
  "tags": ["...", "..."],
  "score": 8,
  "scoreReason": "...",
  "competitors": [
    {{"name": "...", "url": "...", "comparison": "..."}}
  ]
}}
"""

def analyze_product(product):
    """
    分析单个产品
    这里我们先用简单的规则系统，后续可以接入真实 LLM API
    """
    name = product.get('name', '')
    description = product.get('description', '')
    url = product.get('url', '')

    # 基于关键词的简单分类
    tags = generate_tags(name, description)

    # 基于特征的受众分析
    audience = detect_audience(name, description, tags)

    # 使用场景推断
    use_cases = infer_use_cases(name, description, tags)

    # 基础评分
    score, reason = calculate_score(product)

    # 竞品推断
    competitors = infer_competitors(tags)

    return {
        'targetAudience': audience,
        'useCases': use_cases,
        'designIntent': f"基于{tags[0] if tags else 'AI'}技术，提供{description[:50] if description else '自动化服务'}",
        'problemSolved': f"解决{audience}在{use_cases[0] if use_cases else '日常工作中'}的效率问题",
        'tags': tags,
        'score': score,
        'scoreReason': reason,
        'competitors': competitors
    }

def generate_tags(name, description):
    """生成产品标签"""
    content = f"{name} {description}".lower()
    tags = []

    # 类别标签
    category_keywords = {
        '写作': ['write', 'content', 'blog', 'copy', 'article', 'text'],
        '设计': ['design', 'image', 'art', 'draw', 'photo', 'creative', 'visual'],
        '编程': ['code', 'dev', 'program', 'developer', 'coding', 'github'],
        '办公': ['productivity', 'work', 'office', 'document', 'email', 'meeting'],
        '教育': ['learn', 'education', 'study', 'course', 'teach'],
        '创意': ['creative', 'generate', 'create', 'make', 'build'],
        '生活': ['life', 'daily', 'personal', 'assistant'],
        '商业': ['business', 'sales', 'marketing', 'customer', 'enterprise'],
        '客服': ['support', 'chat', 'customer service', 'help desk'],
        '营销': ['marketing', 'seo', 'social media', 'ads'],
        '数据分析': ['data', 'analytics', 'report', 'insights']
    }

    for category, keywords in category_keywords.items():
        if any(kw in content for kw in keywords):
            tags.append(category)
            if len(tags) >= 3:
                break

    # 技术标签
    tech_keywords = {
        'ChatGPT': ['chatgpt', 'openai', 'gpt'],
        'Claude': ['claude', 'anthropic'],
        '开源模型': ['open source', 'local llm', 'llama', 'mistral'],
        '多模型': ['multi-model', 'universal', 'any model']
    }

    for tech, keywords in tech_keywords.items():
        if any(kw in content for kw in keywords):
            tags.append(tech)
            break

    # 形态标签
    if 'github' in content:
        tags.append('开源项目')
    elif 'app' in content or 'ios' in content or 'android' in content:
        tags.append('移动应用')
    else:
        tags.append('Web应用')

    # 确保至少3个标签
    if len(tags) < 3:
        tags.append('AI工具')

    return list(set(tags))[:5]

def detect_audience(name, description, tags):
    """检测目标受众"""
    content = f"{name} {description}".lower()

    if any(t in tags for t in ['编程', '开源项目']):
        return '开发者和技术团队'
    if '设计' in tags:
        return '设计师和创意工作者'
    if '写作' in tags:
        return '内容创作者和写作者'
    if '办公' in tags:
        return '职场人士和团队协作者'
    if '教育' in tags:
        return '学生和终身学习者'
    if '商业' in tags or '营销' in tags:
        return '创业者和市场营销人员'

    return '普通用户和效率追求者'

def infer_use_cases(name, description, tags):
    """推断使用场景"""
    content = f"{name} {description}".lower()
    cases = []

    if 'write' in content or '写作' in tags:
        cases.append('内容创作和文案撰写')
    if 'design' in content or '设计' in tags:
        cases.append('视觉设计和创意生成')
    if 'code' in content or '编程' in tags:
        cases.append('代码生成和开发辅助')
    if 'email' in content:
        cases.append('邮件起草和沟通优化')
    if 'meet' in content or 'meeting' in content:
        cases.append('会议记录和总结')
    if 'research' in content:
        cases.append('信息检索和研究辅助')
    if 'automation' in content or '自动' in content:
        cases.append('工作流自动化')
    if 'chat' in content or '对话' in content:
        cases.append('智能对话和问答')

    # 如果推断不出，添加通用场景
    if not cases:
        cases = ['日常效率提升', '重复任务自动化', '创意激发辅助']

    return cases[:4]

def calculate_score(product):
    """计算产品评分"""
    score = 5  # 基础分
    reasons = []

    # 来源权重
    source = product.get('source', '')
    if source == 'hackernews':
        score += 1
        hn_score = product.get('score', 0)
        if hn_score > 50:
            score += 1
            reasons.append(f"Hacker News 热度高（{hn_score}分）")
    elif source == 'github':
        stars = product.get('stars', 0)
        if stars > 100:
            score += 1
            reasons.append(f"GitHub 星星数可观（{stars}）")

    # 描述完整性
    desc = product.get('description', '')
    if len(desc) > 100:
        score += 1
        reasons.append("产品描述清晰完整")

    # 有实际落地页
    if product.get('homepage') or product.get('url'):
        score += 1
        reasons.append("有可用产品链接")

    # 限制在 1-10
    score = max(1, min(10, int(score)))

    if not reasons:
        reasons.append("具备基础产品形态")

    return score, "；".join(reasons)

def infer_competitors(tags):
    """推断竞品"""
    competitors = []

    # 基于标签推断竞品
    competitor_map = {
        '写作': [
            {'name': 'Notion AI', 'url': 'https://notion.so', 'comparison': '功能更全面但较重'},
            {'name': 'Jasper', 'url': 'https://jasper.ai', 'comparison': '营销导向，定价较高'}
        ],
        '设计': [
            {'name': 'Midjourney', 'url': 'https://midjourney.com', 'comparison': '图像生成标杆，社区活跃'},
            {'name': 'Canva AI', 'url': 'https://canva.com', 'comparison': '模板丰富，易用性强'}
        ],
        '编程': [
            {'name': 'GitHub Copilot', 'url': 'https://github.com/copilot', 'comparison': 'IDE集成深，代码能力强'},
            {'name': 'Cursor', 'url': 'https://cursor.sh', 'comparison': 'AI原生编辑器体验好'}
        ],
        '办公': [
            {'name': 'Microsoft Copilot', 'url': 'https://copilot.microsoft.com', 'comparison': ' Office生态整合'},
            {'name': 'Google Workspace AI', 'url': 'https://workspace.google.com', 'comparison': '云端协作优势'}
        ]
    }

    for tag in tags:
        if tag in competitor_map:
            competitors.extend(competitor_map[tag])

    # 返回前3个不重复的
    seen = set()
    unique = []
    for c in competitors:
        if c['name'] not in seen:
            seen.add(c['name'])
            unique.append(c)
            if len(unique) >= 3:
                break

    return unique if unique else [
        {'name': 'ChatGPT', 'url': 'https://chatgpt.com', 'comparison': '通用基准'}
    ]

if __name__ == '__main__':
    # 测试
    test_product = {
        'name': 'AI Writing Assistant',
        'description': 'A tool that helps you write better content using GPT-4',
        'url': 'https://example.com',
        'source': 'hackernews',
        'score': 45
    }
    result = analyze_product(test_product)
    print(json.dumps(result, ensure_ascii=False, indent=2))

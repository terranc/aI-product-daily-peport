#!/usr/bin/env python3
"""
LLM 分析引擎
提供基于 LLM 的产品深度分析能力

使用 requests 直接调用 OpenAI API，无需安装 openai SDK
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("⚠️  未安装 requests 包，LLM 分析将不可用")


class LLMAnalyzer:
    """LLM 分析引擎（基于 requests 实现）

    支持多个 API provider，自动检测环境变量：
    1. OPENAI_API_KEY + OPENAI_BASE_URL（标准 OpenAI）
    2. ZSH_AI_OPENAI_API_KEY + ZSH_AI_OPENAI_URL（火山引擎 DeepSeek）
    3. OPENROUTER_API_KEY（OpenRouter）
    4. VOLCES_API_KEY（火山引擎）
    5. XAI_API_KEY（xAI Grok）
    """

    def __init__(self):
        self.api_key = None
        self.base_url = None
        self.model = None
        self.provider = None

        # 优先级顺序检测 API provider
        providers = [
            {
                "name": "OpenAI",
                "key_env": "OPENAI_API_KEY",
                "url_env": "OPENAI_BASE_URL",
                "default_url": "https://api.openai.com/v1",
                "model_env": "LLM_MODEL",
                "default_model": "gpt-4o-mini"
            },
            {
                "name": "火山引擎 DeepSeek",
                "key_env": "ZSH_AI_OPENAI_API_KEY",
                "url_env": "ZSH_AI_OPENAI_URL",
                "default_url": "https://ark.cn-beijing.volces.com/api/v3",
                "model_env": "ZSH_AI_OPENAI_MODEL",
                "default_model": "deepseek-v3-2-251201"
            },
            {
                "name": "OpenRouter",
                "key_env": "OPENROUTER_API_KEY",
                "url_env": None,
                "default_url": "https://openrouter.ai/api/v1",
                "model_env": None,
                "default_model": "deepseek/deepseek-chat"
            },
            {
                "name": "火山引擎",
                "key_env": "VOLCES_API_KEY",
                "url_env": None,
                "default_url": "https://ark.cn-beijing.volces.com/api/v3",
                "model_env": None,
                "default_model": "deepseek-v3-2-251201"
            },
            {
                "name": "xAI",
                "key_env": "XAI_API_KEY",
                "url_env": None,
                "default_url": "https://api.x.ai/v1",
                "model_env": None,
                "default_model": "grok-beta"
            }
        ]

        for provider in providers:
            key = os.getenv(provider["key_env"])
            if key:
                self.api_key = key
                self.base_url = os.getenv(provider["url_env"]) or provider["default_url"]
                self.model = os.getenv(provider["model_env"]) or provider["default_model"]
                self.provider = provider["name"]
                break

        if HAS_REQUESTS and self.api_key:
            print(f"✅ LLM 分析引擎已初始化 (Provider: {self.provider}, Model: {self.model})")
        elif not self.api_key:
            print("⚠️  未检测到任何 LLM API Key")
            print("   请设置其中一个环境变量:")
            print("   - OPENAI_API_KEY (标准 OpenAI)")
            print("   - ZSH_AI_OPENAI_API_KEY (火山引擎 DeepSeek)")
            print("   - OPENROUTER_API_KEY (OpenRouter)")
            print("   - VOLCES_API_KEY (火山引擎)")
            print("   - XAI_API_KEY (xAI Grok)")

    def is_available(self) -> bool:
        """检查 LLM 是否可用"""
        return HAS_REQUESTS and self.api_key is not None

    def _build_api_url(self) -> str:
        """构建完整的 API URL"""
        base = self.base_url.rstrip("/")

        # 兼容完整路径（如 https://xxx/chat/completions）和基础路径（如 https://xxx/v1）
        if base.endswith("/chat/completions"):
            return base
        else:
            return f"{base}/chat/completions"

    def analyze(self, prompt: str, max_tokens: int = 2000) -> Optional[str]:
        """调用 LLM 进行分析"""
        if not self.is_available():
            return None

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个专业的产品分析师，擅长深度分析 AI 产品的商业价值、竞争位势和增长潜力。请用中文回答，输出格式为 JSON。"
                    },
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }

            url = self._build_api_url()
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                print(f"❌ LLM API 调用失败: {response.status_code}")
                print(f"   响应: {response.text[:200]}")
                return None

        except requests.exceptions.Timeout:
            print("❌ LLM 调用超时")
            return None
        except Exception as e:
            print(f"❌ LLM 调用失败: {e}")
            return None

    def analyze_product_basic(self, product: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """基础产品分析（用于 analyze_product.py）"""
        prompt = f"""请分析以下 AI 产品，提供结构化分析：

产品名称: {product.get('name', 'Unknown')}
产品描述: {product.get('description', '暂无描述')}
产品链接: {product.get('url', product.get('homepage', '暂无链接'))}
来源: {product.get('source', '未知')}

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
        result = self.analyze(prompt)
        if result:
            try:
                # 尝试提取 JSON
                if "```json" in result:
                    result = result.split("```json")[1].split("```")[0]
                elif "```" in result:
                    result = result.split("```")[1].split("```")[0]

                return json.loads(result.strip())
            except json.JSONDecodeError as e:
                print(f"⚠️  JSON 解析失败: {e}")
                return None
        return None

    def analyze_product_deep(self, product: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """深度产品分析（用于 weekly_analysis.py 的七维框架）"""
        analysis = product.get("analysis", {})

        prompt = f"""请对以下 AI 产品进行深度分析，采用七维分析框架：

# 产品信息
- 名称: {product.get('name', 'Unknown')}
- 描述: {product.get('description', '暂无描述')}
- 目标用户: {analysis.get('targetAudience', '未知')}
- 使用场景: {', '.join(analysis.get('useCases', []))}
- 竞品: {[c.get('name', '') for c in analysis.get('competitors', [])]}
- 当前评分: {analysis.get('score', 5)}/10
- 评分理由: {analysis.get('scoreReason', '暂无')}

# 七维分析框架

请按以下维度进行深度分析，每个维度都需要给出明确的判断和理由：

## 1. 问题定义 (problemDefinition)
- painPoint: 用户面临的核心痛点是什么？
- previousSolution: AI 出现前用户怎么解决这个问题？
- painIntensity: 这是高频刚需还是低频痒点？（高频刚需/低频痒点）

## 2. AI 不可替代性 (aiIndispensability)
- coreLeverage: AI 的核心杠杆是什么？（效率/体验/成本/合规）
- aiRole: AI 在产品中的角色？（核心能力/增值功能/装饰性功能）
- withoutAI: 如果没有 AI，这个产品还能成立吗？为什么？

## 3. 工作流嵌入 (workflowEmbedding)
- userJourney: 描述用户的完整使用路径（从哪里进来 → 首次体验 → 核心循环 → 离开点）
- embeddingDepth: 嵌入用户工作流的深度？（点状工具/流程嵌入/深度绑定）
- switchingCost: 迁移成本如何？（高/中/低）

## 4. 商业化路径 (monetization)
- pricingModel: 定价模式？（订阅/按量/按效果付费/开源增值）
- roiLogic: 用户如何从产品中获得 ROI？
- payingWillingness: 付费意愿如何？（明确/需培养/存疑）

## 5. 护城河分析 (moatAnalysis)
- dataMoat: 数据壁垒？（私有数据优势/整合公开数据/无数据优势）
- workflowMoat: 工作流壁垒？（切换成本来自哪里？）
- networkEffect: 是否有网络效应？（有/无）
- platformRisk: 大厂做同样功能的威胁程度？（高/中/低）

## 6. 竞品位势对比 (competitivePositioning)
- workflowComparison: 与主流竞品在工作流嵌入上的差异？
- keyDifferentiator: 最核心的差异化点是什么？
- survivalNiche: 这个产品的生存利基在哪里？

## 7. 四问验证 (fourQuestionsValidation)
- highFrequencyNeed: 是高频刚需吗？（true/false）
- aiIndispensable: AI 是否不可替代？（true/false）
- workflowEmbedded: 是否深度嵌入工作流？（true/false）
- monetizationClear: 商业化路径是否清晰？（true/false）

# 输出要求

请返回**严格的 JSON 格式**，不要添加任何解释性文字：

{{
  "problemDefinition": {{
    "painPoint": "...",
    "previousSolution": "...",
    "painIntensity": "高频刚需"
  }},
  "aiIndispensability": {{
    "coreLeverage": "效率",
    "aiRole": "核心能力",
    "withoutAI": "无法成立，会退化为普通数据库"
  }},
  "workflowEmbedding": {{
    "userJourney": "...",
    "embeddingDepth": "流程嵌入",
    "switchingCost": "中"
  }},
  "monetization": {{
    "pricingModel": "订阅制",
    "roiLogic": "...",
    "payingWillingness": "明确"
  }},
  "moatAnalysis": {{
    "dataMoat": "整合公开数据",
    "workflowMoat": "...",
    "networkEffect": "无",
    "platformRisk": "高"
  }},
  "competitivePositioning": {{
    "workflowComparison": "...",
    "keyDifferentiator": "...",
    "survivalNiche": "..."
  }},
  "fourQuestionsValidation": {{
    "highFrequencyNeed": true,
    "aiIndispensable": true,
    "workflowEmbedded": true,
    "monetizationClear": true
  }}
}}
"""

        result = self.analyze(prompt, max_tokens=3000)
        if result:
            try:
                # 尝试提取 JSON
                if "```json" in result:
                    result = result.split("```json")[1].split("```")[0]
                elif "```" in result:
                    result = result.split("```")[1].split("```")[0]

                return json.loads(result.strip())
            except json.JSONDecodeError as e:
                print(f"⚠️  JSON 解析失败: {e}")
                print(f"原始输出: {result[:200]}...")
                return None
        return None


# 全局实例
_analyzer = None


def get_analyzer() -> LLMAnalyzer:
    """获取全局 LLM 分析器实例"""
    global _analyzer
    if _analyzer is None:
        _analyzer = LLMAnalyzer()
    return _analyzer


if __name__ == "__main__":
    # 测试
    analyzer = get_analyzer()

    if analyzer.is_available():
        print("\n🧪 测试基础分析...")
        test_product = {
            "name": "AI Writing Assistant",
            "description": "A tool that helps you write better content using GPT-4",
            "url": "https://example.com",
            "source": "hackernews"
        }
        result = analyzer.analyze_product_basic(test_product)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("❌ 分析失败")

        print("\n🧪 测试深度分析（七维框架）...")
        test_product_with_analysis = {
            **test_product,
            "analysis": {
                "targetAudience": "内容创作者和营销人员",
                "useCases": ["文章写作", "营销文案", "邮件撰写"],
                "competitors": [{"name": "Jasper"}],
                "score": 7,
                "scoreReason": "有一定实用价值但竞争激烈"
            }
        }
        deep_result = analyzer.analyze_product_deep(test_product_with_analysis)
        if deep_result:
            print(json.dumps(deep_result, ensure_ascii=False, indent=2))
        else:
            print("❌ 深度分析失败")
    else:
        print("⚠️  LLM 不可用，请设置 OPENAI_API_KEY 环境变量")

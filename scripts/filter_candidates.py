#!/usr/bin/env python3
"""
筛选候选产品：去重 + 过滤非AI应用类产品
"""
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 路径配置
BASE_DIR = Path("/Volumes/EXTEND/aI-product-daily-peport")
RAW_CANDIDATES_PATH = BASE_DIR / "data" / "raw-candidates.json"
PRODUCTS_DB_PATH = BASE_DIR / "data" / "products.json"

def load_json(path):
    """加载 JSON 文件"""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def is_ai_application(product):
    """
    判断是否为 AI 应用类产品
    排除：AI 模型/框架/SDK/开发工具、Agent框架/MCP工具、开源项目（除非面向终端用户）、
    编码辅助工具、纯技术讨论帖、API中转站
    """
    name = (product.get('name', '') + product.get('description', '')).lower()
    
    # 排除模式
    exclude_patterns = [
        # AI 模型/框架/SDK
        'model', 'framework', 'sdk', 'api', 'open source', 'github', 'repo',
        'agent framework', 'mcp tool', 'prompt engineering',
        # 编码辅助
        'copilot', 'cursor', 'coding assistant', 'code generation',
        # 技术讨论
        'discussion', 'tutorial', 'guide', 'how to', 'learn',
        # API 中转
        'api proxy', 'account sharing', 'api relay',
        # 非 AI 相关
        'burger', 'nba', 'mlb', 'sports', 'food', 'restaurant',
        'whopper', 'jalapeño',
        # 纯新闻/事件
        'lawsuit', 'court', 'trial', 'verdict',
        # 硬件/基础设施
        'server', 'hardware', 'microprocessor', 'chip',
    ]
    
    # 检查排除模式
    for pattern in exclude_patterns:
        if pattern in name:
            return False
    
    # 必须包含 AI 相关关键词
    ai_keywords = [
        'ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning',
        'neural', 'gpt', 'llm', 'chatbot', 'assistant', 'copilot', 'automation',
        'intelligent', 'smart', 'predict', 'generate', 'create', 'design',
        'productivity', 'workflow', 'optimize', 'personal', 'health',
        'writing', 'image', 'video', 'audio', 'voice', 'text',
        'analysis', 'insight', 'recommend', 'suggest', 'help'
    ]
    
    has_ai_keyword = any(keyword in name for keyword in ai_keywords)
    
    return has_ai_keyword

def filter_candidates():
    """筛选候选产品"""
    print("🔍 开始筛选候选产品...")
    
    # 加载数据
    raw_data = load_json(RAW_CANDIDATES_PATH)
    products_db = load_json(PRODUCTS_DB_PATH)
    
    candidates = raw_data.get('products', [])
    existing_products = products_db.get('products', [])
    
    print(f"📊 候选产品总数: {len(candidates)}")
    print(f"📊 数据库已有产品: {len(existing_products)}")
    
    # 创建已有产品 product_id 集合（考虑冷却期）
    now = datetime.utcnow()
    existing_product_ids = set()
    
    for product in existing_products:
        product_id = product.get('id', '')
        cooldown_expires = product.get('cooldownExpiresAt', '')
        
        if cooldown_expires:
            try:
                cooldown_date = datetime.fromisoformat(cooldown_expires.replace('Z', '+00:00'))
                if cooldown_date > now:
                    existing_product_ids.add(product_id)
            except:
                # 如果日期解析失败，仍然添加到已存在集合
                existing_product_ids.add(product_id)
        else:
            existing_product_ids.add(product_id)
    
    print(f"📊 冷却期内的产品: {len(existing_product_ids)}")
    
    # 去重
    unique_candidates = []
    filtered_out_dedup = 0
    
    for candidate in candidates:
        product_id = candidate.get('product_id', '')
        if product_id not in existing_product_ids:
            unique_candidates.append(candidate)
        else:
            filtered_out_dedup += 1
    
    print(f"✅ 去重后剩余: {len(unique_candidates)} 个")
    print(f"❌ 去重排除: {filtered_out_dedup} 个")
    
    # 过滤非AI应用类产品
    ai_application_candidates = []
    filtered_out_non_ai = 0
    
    for candidate in unique_candidates:
        if is_ai_application(candidate):
            ai_application_candidates.append(candidate)
        else:
            filtered_out_non_ai += 1
    
    print(f"✅ AI应用类产品: {len(ai_application_candidates)} 个")
    print(f"❌ 非AI应用类排除: {filtered_out_non_ai} 个")
    
    # 输出筛选结果摘要
    print("\n" + "="*60)
    print("📋 筛选结果摘要:")
    print("="*60)
    print(f"原始候选: {len(candidates)}")
    print(f"去重排除: {filtered_out_dedup}")
    print(f"非AI应用排除: {filtered_out_non_ai}")
    print(f"最终候选: {len(ai_application_candidates)}")
    
    # 按来源渠道统计
    channel_stats = {}
    for candidate in ai_application_candidates:
        channel = candidate.get('source', 'unknown')
        channel_stats[channel] = channel_stats.get(channel, 0) + 1
    
    print("\n📊 来源渠道统计:")
    for channel, count in channel_stats.items():
        print(f"  {channel}: {count}")
    
    # 保存筛选后的候选产品
    output_path = BASE_DIR / "data" / "filtered-candidates.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'filteredAt': now.isoformat(),
            'totalCount': len(ai_application_candidates),
            'channelStats': channel_stats,
            'products': ai_application_candidates
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 筛选结果已保存到: {output_path}")
    
    return ai_application_candidates

if __name__ == "__main__":
    candidates = filter_candidates()
    print(f"\n✅ 筛选完成，共 {len(candidates)} 个候选产品")
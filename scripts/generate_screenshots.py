#!/usr/bin/env python3
"""
为精选产品生成截图
"""
import sys
import json
import time
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, '/Volumes/EXTEND/aI-product-daily-peport/scripts')
from screenshot import take_website_screenshot

# 精选产品列表
PRODUCTS = [
    {
        "id": "x.com/tradeoddsio/status/2050326043089609069",
        "name": "TradeOdds - AI 交易历史匹配工具",
        "url": "https://tradeodds.com"
    },
    {
        "id": "x.com/tuturetom/status/2061746000142684643",
        "name": "HTML 视频版剪映 (HyperFrames)",
        "url": "https://hyperframes.app/zh"
    },
    {
        "id": "tryjunco.com",
        "name": "Junco - AI 播客生成器",
        "url": "https://www.tryjunco.com"
    },
    {
        "id": "thomasdhughes.com/brontosaurus",
        "name": "Brontosaurus - 语音驱动 AI 画布",
        "url": "https://thomasdhughes.com/brontosaurus/"
    },
    {
        "id": "v2ex.com/t/1217525",
        "name": "Hermes Desktop - 跨平台 AI 助手",
        "url": "https://hermes-agent.nousresearch.com/desktop"
    }
]

def main():
    """生成所有产品的截图"""
    print("📸 开始为精选产品生成截图...")
    print("="*60)
    
    results = []
    
    for i, product in enumerate(PRODUCTS, 1):
        print(f"\n[{i}/5] 处理: {product['name']}")
        print(f"  URL: {product['url']}")
        
        try:
            screenshot_path = take_website_screenshot(product['url'], product['id'])
            if screenshot_path:
                results.append({
                    "id": product['id'],
                    "name": product['name'],
                    "url": product['url'],
                    "screenshotPath": screenshot_path,
                    "success": True
                })
                print(f"  ✅ 截图成功: {screenshot_path}")
            else:
                results.append({
                    "id": product['id'],
                    "name": product['name'],
                    "url": product['url'],
                    "screenshotPath": None,
                    "success": False,
                    "error": "截图失败"
                })
                print(f"  ❌ 截图失败")
        except Exception as e:
            results.append({
                "id": product['id'],
                "name": product['name'],
                "url": product['url'],
                "screenshotPath": None,
                "success": False,
                "error": str(e)
            })
            print(f"  ❌ 截图异常: {e}")
        
        # 等待3秒避免速率限制
        time.sleep(3)
    
    # 保存结果
    output_path = Path("/Volumes/EXTEND/aI-product-daily-peport/data/screenshot-results.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "totalCount": len(PRODUCTS),
            "successCount": sum(1 for r in results if r['success']),
            "results": results
        }, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*60)
    print("📊 截图结果汇总:")
    print(f"  总计: {len(PRODUCTS)}")
    print(f"  成功: {sum(1 for r in results if r['success'])}")
    print(f"  失败: {sum(1 for r in results if not r['success'])}")
    print(f"\n💾 结果已保存到: {output_path}")
    
    return results

if __name__ == "__main__":
    main()
"""精选 TOP 5 产品定义 + 截图执行"""
import sys, json, time
sys.path.insert(0, '/home/pin/aI-product-daily-peport/scripts')
from screenshot import process_product_screenshots

selected_products = [
    {
        "id": "producthunt.com/r/p/1214897",
        "name": "Wispr Flow",
        "type": "app",
        "url": "https://wisprflow.ai",
        "sourceChannel": "producthunt",
    },
    {
        "id": "reelang.com",
        "name": "Reelang",
        "type": "website",
        "url": "https://reelang.com",
        "sourceChannel": "hackernews",
    },
    {
        "id": "pageforth.com",
        "name": "PageForth",
        "type": "app",
        "url": "https://pageforth.com",
        "sourceChannel": "hackernews",
    },
    {
        "id": "producthunt.com/r/p/1212030",
        "name": "AdAnt AI",
        "type": "saas",
        "url": "https://adant.ai",
        "sourceChannel": "producthunt",
    },
    {
        "id": "v2ex.com/t/1232288",
        "name": "Workout Narrator",
        "type": "app",
        "url": "https://apps.apple.com/app/id6795447541",
        "sourceChannel": "v2ex",
    },
]

results = []
for i, product in enumerate(selected_products):
    print(f"=== [{i+1}/5] {product['name']} ({product['id']}) ===", flush=True)
    try:
        result = process_product_screenshots(product)
        product['screenshotUrl'] = result.get('screenshotUrl')
        product['appStoreScreenshots'] = result.get('appStoreScreenshots', [])
        product['appStoreName'] = result.get('appStoreName')
        product['appStoreUrl'] = result.get('appStoreUrl')
    except Exception as e:
        print(f"  ERROR: {e}", flush=True)
        product['screenshotUrl'] = None
        product['appStoreScreenshots'] = []
        product['appStoreName'] = None
        product['appStoreUrl'] = None
    results.append(product)
    time.sleep(3)

with open('/home/pin/aI-product-daily-peport/data/_cron_selected.json', 'w') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n=== SUMMARY ===")
for p in results:
    print(f"{p['name']}: shot={p.get('screenshotUrl')} | appstore={p.get('appStoreName')} ({len(p.get('appStoreScreenshots', []))} imgs)")

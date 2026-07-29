#!/usr/bin/env python3
"""Fix corrupted Chinese text in report using Unicode escapes"""
import json
import os
from datetime import datetime, timezone, timedelta

today = datetime.now(timezone.utc)
date_str = today.strftime('%Y-%m-%d')
iso_now = today.isoformat()
BASE = '/Volumes/EXTEND/aI-product-daily-peport'
cooldown_date = (today + timedelta(days=14)).isoformat()

# Build clean data using only safe ASCII constructs
# Chinese text is constructed via concatenation to avoid encoding issues

# ============================================
# Product 1: Tag Your Photos
# ============================================
p1 = {}
p1['id'] = 'producthunt.com/r/p/1208168'
p1['name'] = 'Tag Your Photos - AI \u7167\u7247\u5173\u952e\u8bcd\u5de5\u5177'
p1['description'] = '\u4e00\u6b3e macOS \u5e94\u7528\uff0c100% \u5728\u672c\u5730\u4e3a Apple Photos \u7167\u7247\u5e93\u81ea\u52a8\u751f\u6210\u5173\u952e\u8bcd\u6807\u7b7e\u3002\u4f7f\u7528 Gemma 4 12B \u6a21\u578b\u901a\u8fc7 Apple MLX \u6846\u67b6\u5728\u8bbe\u5907\u7aef\u8fd0\u884c\uff0c\u4e0d\u4e0a\u4f20\u4efb\u4f55\u6570\u636e\u5230\u4e91\u7aef\u3002\u751f\u6210\u7684\u5173\u952e\u8bcd\u53ef\u88ab Spotlight \u5168\u5c40\u641c\u7d22\uff0c\u751a\u81f3\u80fd\u5728 iPhone/iPad \u4e3b\u5c4f\u641c\u7d22\u3002'
p1['slug'] = 'tag-your-photos'
p1['homepage'] = 'https://www.producthunt.com/r/p/1208168'
p1['url'] = 'https://www.producthunt.com/r/p/1208168'
p1['type'] = 'app'
p1['sourceChannels'] = ['producthunt']
p1['sourceUrl'] = 'https://www.producthunt.com/r/p/1208168?app_id=339'
p1['tags'] = ['\u7167\u7247\u7ba1\u7406', 'AI\u6807\u7b7e', '\u672c\u5730AI', 'macOS', '\u9690\u79c1\u4fdd\u62a4']
p1['analysis'] = {
    'targetAudience': '\u62e5\u6709\u5927\u91cf Apple Photos \u7167\u7247\u3001\u9700\u8981\u9ad8\u6548\u68c0\u7d22\u548c\u6574\u7406\u7167\u7247\u7684 Mac \u7528\u6237',
    'useCases': [
        '\u7ed9\u6570\u5343\u5f20\u7167\u7247\u6279\u91cf\u6dfb\u52a0\u5173\u952e\u8bcd\u6807\u7b7e\uff0c\u65b9\u4fbf\u68c0\u7d22',
        '\u901a\u8fc7 Spotlight \u5168\u5c40\u641c\u7d22\u7167\u7247\u5185\u5bb9',
        '\u5728 iPhone/iPad \u4e3b\u5c4f\u76f4\u63a5\u641c\u7d22\u7167\u7247\u5173\u952e\u8bcd',
        '\u7167\u7247\u5e93\u9690\u79c1\u4fdd\u62a4\u2014\u2014\u65e0\u9700\u4e0a\u4f20\u4e91\u7aef'
    ],
    'designIntent': '\u89e3\u51b3 Apple Photos \u7528\u6237\u65e0\u6cd5\u9ad8\u6548\u641c\u7d22\u7167\u7247\u7684\u75db\u70b9\u3002\u5927\u591a\u6570 AI \u6807\u7b7e\u5de5\u5177\u9700\u8981\u4e0a\u4f20\u4e91\u7aef\uff0c\u800c\u8fd9\u6b3e\u5e94\u7528 100% \u5728\u672c\u5730\u8fd0\u884c\uff0c\u7ed3\u5408 Apple MLX \u6846\u67b6\u548c Gemma 4 \u6a21\u578b\uff0c\u65e2\u4fdd\u62a4\u9690\u79c1\u53c8\u4fdd\u8bc1\u6807\u7b7e\u8d28\u91cf\u3002',
    'problemSolved': 'Apple Photos \u5185\u7f6e\u641c\u7d22\u80fd\u529b\u6709\u9650\uff0c\u65e0\u6cd5\u8bc6\u522b\u7167\u7247\u4e2d\u7684\u5177\u4f53\u7269\u4f53\u3001\u573a\u666f\u548c\u4eba\u7269\u3002\u4f20\u7edf\u65b9\u6848\u9700\u8981\u624b\u52a8\u6dfb\u52a0\u5173\u952e\u8bcd\u6216\u4e0a\u4f20\u4e91\u7aef\u3002\u8fd9\u6b3e\u5e94\u7528\u81ea\u52a8\u4e3a\u6bcf\u5f20\u7167\u7247\u751f\u6210\u7cbe\u51c6\u5173\u952e\u8bcd\uff0c\u5168\u90e8\u5728\u672c\u5730\u5b8c\u6210\u3002',
    'score': 8,
    'scoreReason': '\u89e3\u51b3\u4e86\u4e00\u4e2a\u771f\u5b9e\u4e14\u5e7f\u6cdb\u7684\u75db\u70b9\uff08\u7167\u7247\u6574\u7406\uff09\uff0c100% \u672c\u5730\u8fd0\u884c\u4fdd\u969c\u9690\u79c1\uff0c\u6280\u672f\u65b9\u6848\u624e\u5b9e\uff08Gemma 4+MLX\uff09\uff0c\u4f46\u53d7\u4f17\u9650\u4e8e Mac Apple Silicon \u7528\u6237\u3002',
    'competitors': [
        {'name': 'VisionTagger', 'url': 'https://www.synendo.com/visiontagger', 'comparison': '\u529f\u80fd\u7c7b\u4f3c\uff0c\u4f46\u4e5f\u652f\u6301\u5bfc\u51fa XMP \u5143\u6570\u636e\uff0c\u4ef7\u683c $34.99 \u4e00\u6b21\u6027\u8d2d\u4e70'},
        {'name': 'Apple Photos \u667a\u80fd\u641c\u7d22', 'url': 'https://www.apple.com/macos/photos/', 'comparison': '\u82f9\u679c\u5185\u7f6e\u7684 AI \u641c\u7d22\uff0c\u7cbe\u5ea6\u548c\u5173\u952e\u8bcd\u7ef4\u5ea6\u4e0d\u5982\u4e13\u7528\u5de5\u5177'}
    ]
}

# ============================================
# Product 2: VoiceHop
# ============================================
p2 = {}
p2['id'] = 'chromewebstore.google.com/detail/voicehoprealtimeaudio/gpjfekccjgnojplebmaafgbhjggimfio'
p2['name'] = 'VoiceHop - \u5b9e\u65f6\u97f3\u89c6\u9891\u7ffb\u8bd1'
p2['description'] = '\u4e00\u6b3e Chrome \u6d4f\u89c8\u5668\u6269\u5c55\uff0c\u5b9e\u73b0\u5b9e\u65f6\u8bed\u97f3\u5230\u8bed\u97f3\u7684\u7ffb\u8bd1\u3002\u652f\u6301 YouTube\u3001Netflix\u3001Zoom\u3001Google Meet \u7b49\u5e73\u53f0\u7684\u97f3\u89c6\u9891\u5185\u5bb9\u5b9e\u65f6\u7ffb\u8bd1\uff0c\u4e9a\u79d2\u7ea7\u5ef6\u8fdf\uff0c\u4fdd\u7559\u539f\u59cb\u8bf4\u8bdd\u4eba\u97f3\u8272\u3002\u652f\u6301\u4e2d\u82f1\u65e5\u6cd5\u5fb7\u7b49\u591a\u79cd\u8bed\u8a00\u3002'
p2['slug'] = 'voicehop'
p2['homepage'] = 'https://voicehop.app'
p2['url'] = 'https://voicehop.app'
p2['type'] = 'extension'
p2['sourceChannels'] = ['hackernews']
p2['sourceUrl'] = 'https://chromewebstore.google.com/detail/voicehop-real-time-audio/gpjfekccjgnojplebmaafgbhjggimfio'
p2['tags'] = ['\u5b9e\u65f6\u7ffb\u8bd1', '\u97f3\u89c6\u9891\u7ffb\u8bd1', 'Chrome\u6269\u5c55', '\u591a\u8bed\u8a00', '\u8bed\u97f3\u5408\u6210']
p2['analysis'] = {
    'targetAudience': '\u9700\u8981\u8de8\u8bed\u8a00\u89c2\u770b\u5916\u56fd\u89c6\u9891\u3001\u53c2\u4e0e\u56fd\u9645\u4f1a\u8bae\u6216\u5728\u7ebf\u5b66\u4e60\u7684\u7528\u6237',
    'useCases': [
        '\u5b9e\u65f6\u7ffb\u8bd1 YouTube \u4e0a\u7684\u5916\u8bed\u89c6\u9891\u5185\u5bb9',
        '\u5728 Zoom/Google Meet \u56fd\u9645\u4f1a\u8bae\u4e2d\u5b9e\u65f6\u7ffb\u8bd1',
        '\u89c2\u770b Netflix \u5916\u8bed\u5f71\u89c6\u5267\u65e0\u9700\u5b57\u5e55',
        '\u5728\u7ebf\u5b66\u4e60\u56fd\u5916\u8bfe\u7a0b\u76f4\u64ad\u7ffb\u8bd1'
    ],
    'designIntent': '\u6253\u7834\u8bed\u8a00\u58c1\u5792\uff0c\u8ba9\u7528\u6237\u65e0\u9700\u7b49\u5f85\u5b57\u5e55\uff0c\u76f4\u63a5\u7528\u6bcd\u8bed\u542c\u4efb\u4f55\u8bed\u8a00\u7684\u5185\u5bb9\u3002\u901a\u8fc7\u4fdd\u7559\u539f\u59cb\u8bf4\u8bdd\u4eba\u97f3\u8272\u5b9e\u73b0\u66f4\u81ea\u7136\u7684\u7ffb\u8bd1\u4f53\u9a8c\uff0c\u540c\u65f6\u652f\u6301\u4e3b\u6d41\u89c6\u9891\u548c\u4f1a\u8bae\u5e73\u53f0\u3002',
    'problemSolved': '\u4f20\u7edf\u7ffb\u8bd1\u5de5\u5177\u8981\u4e48\u662f\u6587\u672c\u5b57\u5e55\u5f62\u5f0f\uff08\u6253\u65ad\u89c2\u770b\u4f53\u9a8c\uff09\uff0c\u8981\u4e48\u5ef6\u8fdf\u9ad8\u3001\u4e0d\u652f\u6301\u5b9e\u65f6\u573a\u666f\u3002VoiceHop \u5728\u6d4f\u89c8\u5668\u5c42\u9762\u5b9e\u73b0\u4e9a\u79d2\u7ea7\u8bed\u97f3\u5230\u8bed\u97f3\u7ffb\u8bd1\uff0c\u4fdd\u7559\u539f\u59cb\u97f3\u8272\uff0c\u8986\u76d6\u89c6\u9891\u3001\u76f4\u64ad\u3001\u4f1a\u8bae\u5168\u573a\u666f\u3002',
    'score': 8,
    'scoreReason': '\u89e3\u51b3\u4e86\u8de8\u8bed\u8a00\u5185\u5bb9\u6d88\u8d39\u7684\u771f\u5b9e\u521a\u9700\uff0c\u6280\u672f\u5b9e\u73b0\u624e\u5b9e\uff08\u4e9a\u79d2\u7ea7\u5ef6\u8fdf+\u97f3\u8272\u4fdd\u7559\uff09\uff0c\u8986\u76d6\u573a\u666f\u5e7f\u6cdb\uff0c\u4f46\u4ed8\u8d39\u8ba2\u9605\u6a21\u5f0f\u5bf9\u8f7b\u5ea6\u7528\u6237\u95e8\u69db\u8f83\u9ad8\u3002',
    'competitors': [
        {'name': 'Google \u7ffb\u8bd1', 'url': 'https://translate.google.com', 'comparison': '\u514d\u8d39\u4f46\u53ea\u6709\u6587\u672c\u7ffb\u8bd1\uff0c\u4e0d\u652f\u6301\u5b9e\u65f6\u8bed\u97f3\u8f6c\u8bed\u97f3'},
        {'name': 'DeepL', 'url': 'https://www.deepl.com', 'comparison': '\u7ffb\u8bd1\u8d28\u91cf\u9ad8\u4f46\u4ec5\u9650\u4e8e\u6587\u672c\uff0c\u4e0d\u652f\u6301\u97f3\u89c6\u9891\u5b9e\u65f6\u573a\u666f'}
    ]
}

# ============================================
# Product 3: Pinery Prose
# ============================================
p3 = {}
p3['id'] = 'producthunt.com/r/p/1208008'
p3['name'] = 'Pinery Prose - AI \u534f\u4f5c\u5199\u4e66\u51fa\u7248\u5de5\u5177'
p3['description'] = 'Mac \u5e73\u53f0\u81ea\u51fa\u7248\u5de5\u4f5c\u5ba4\uff0c\u96c6\u6210 AI \u534f\u4f5c\u5199\u4e66\u529f\u80fd\u3002AI \u4ee5\u5dee\u5f02\u5bf9\u6bd4(diff)\u5f62\u5f0f\u63d0\u4f9b\u4fee\u6539\u5efa\u8bae\uff0c\u7528\u6237\u9010\u6761\u5ba1\u9605\u540e\u624d\u80fd\u786e\u8ba4\u3002\u652f\u6301\u4ece\u8349\u7a3f\u5230\u6392\u7248\u8bbe\u8ba1\u518d\u5230\u5bfc\u51fa ePub/PDF \u7684\u5168\u6d41\u7a0b\u3002\u6587\u4ef6\u4ee5\u7eaf Markdown \u5b58\u50a8\uff0c\u7528\u6237\u5b8c\u5168\u62e5\u6709\u6570\u636e\u3002'
p3['slug'] = 'pinery-prose'
p3['homepage'] = 'https://pinery.app'
p3['url'] = 'https://pinery.app'
p3['type'] = 'app'
p3['sourceChannels'] = ['producthunt']
p3['sourceUrl'] = 'https://www.producthunt.com/r/p/1208008?app_id=339'
p3['tags'] = ['\u5199\u4f5c\u5de5\u5177', 'AI\u5199\u4f5c', '\u81ea\u51fa\u7248', 'Markdown', 'macOS']
p3['analysis'] = {
    'targetAudience': '\u72ec\u7acb\u4f5c\u8005\u3001\u81ea\u51fa\u7248\u4f5c\u5bb6\u3001\u6280\u672f\u5199\u4f5c\u8005\uff0c\u9700\u8981\u4e00\u7ad9\u5f0f\u5199\u4f5c+\u6392\u7248+\u51fa\u7248\u5de5\u5177\u7684 Mac \u7528\u6237',
    'useCases': [
        '\u4ece\u96f6\u5f00\u59cb\u64b0\u5199\u7535\u5b50\u4e66\uff0cAI \u8f85\u52a9\u7ae0\u8282\u8d77\u8349',
        '\u5bf9\u5df2\u6709\u7a3f\u4ef6\u8fdb\u884c AI \u6da6\u8272\u548c\u5efa\u8bae\uff0c\u9010\u6761\u5ba1\u9605\u4fee\u6539',
        '\u4e00\u952e\u5bfc\u51fa ePub 3 \u683c\u5f0f\u4e0a\u4f20\u4e3b\u6d41\u7535\u5b50\u4e66\u5e73\u53f0',
        '\u751f\u6210\u9ad8\u8d28\u91cf PDF \u5370\u5237\u7248'
    ],
    'designIntent': '\u4e3a\u72ec\u7acb\u4f5c\u8005\u6253\u9020\u4e13\u4e1a\u7ea7\u7684\u81ea\u51fa\u7248\u5de5\u5177\u3002\u4f20\u7edf\u51fa\u7248\u6d41\u7a0b\u9700\u8981\u5206\u522b\u4f7f\u7528\u5199\u4f5c\u3001\u6392\u7248\u3001\u8bbe\u8ba1\u8f6f\u4ef6\uff0cPinery\u5c06\u5168\u6d41\u7a0b\u6574\u5408\u5230\u4e00\u4e2a\u5e94\u7528\u4e2d\uff0cAI\u4ec5\u4f5c\u4e3a\u8f85\u52a9\u5de5\u5177\uff0c\u4fee\u6539\u987b\u7ecf\u4f5c\u8005\u9010\u6761\u786e\u8ba4\u3002',
    'problemSolved': '\u72ec\u7acb\u4f5c\u8005\u9762\u4e34\u5199\u4f5c\u5de5\u5177\u788e\u7247\u5316\u7684\u75db\u70b9\uff1aWord\u6392\u7248\u56f0\u96be\u3001Scrivener\u5b66\u4e60\u66f2\u7ebf\u9661\u3001AI\u5de5\u5177\u53ef\u80fd\u64c5\u81ea\u4fee\u6539\u539f\u6587\u3002Pinery\u7528Markdown\u964d\u4f4e\u6280\u672f\u95e8\u69db\uff0cAI\u4ee5diff\u5f62\u5f0f\u5efa\u8bae\u4fee\u6539\uff0c\u4fdd\u6301\u4f5c\u8005\u5bf9\u5185\u5bb9\u7684\u5b8c\u5168\u63a7\u5236\u3002',
    'score': 7,
    'scoreReason': '\u5b9a\u4f4d\u7cbe\u51c6\u3001\u7528\u6237\u4f53\u9a8c\u4f18\u79c0\uff08\u539f\u751f Mac \u5e94\u7528\uff09\u3001\u9690\u79c1\u4fdd\u62a4\u597d\uff0c\u4f46\u5199\u4f5c AI \u529f\u80fd\u76f8\u6bd4\u4e13\u6709 AI \u5199\u4f5c\u5de5\u5177\u8fd8\u4e0d\u591f\u6df1\u5ea6\uff0c\u4e14\u4ec5\u9650 Mac \u5e73\u53f0\u3002',
    'competitors': [
        {'name': 'Scrivener', 'url': 'https://www.literatureandlatte.com/scrivener/overview', 'comparison': '\u7ecf\u5178\u5199\u4f5c\u5de5\u5177\uff0c\u529f\u80fd\u5f3a\u5927\u4f46\u65e0 AI \u80fd\u529b\uff0c\u5b66\u4e60\u66f2\u7ebf\u9661\u5ced'},
        {'name': 'Atticus', 'url': 'https://www.atticus.io', 'comparison': '\u5728\u7ebf\u81ea\u51fa\u7248\u5de5\u5177\uff0c\u652f\u6301\u6392\u7248\u4f46\u65e0 Mac \u539f\u751f\u5e94\u7528\uff0cAI \u529f\u80fd\u6709\u9650'}
    ]
}

# ============================================
# Product 4: EasyCircuit
# ============================================
p4 = {}
p4['id'] = 'producthunt.com/r/p/1208295'
p4['name'] = 'EasyCircuit - AI \u786c\u4ef6\u7535\u8def\u8bbe\u8ba1\u534f\u4f5c\u5de5\u5177'
p4['description'] = '\u4e00\u6b3e AI \u7535\u8def\u534f\u4f5c\u5de5\u5177\uff0c\u7528\u6237\u7528\u81ea\u7136\u8bed\u8a00\u63cf\u8ff0\u9700\u6c42\uff0cAI \u5373\u81ea\u52a8\u8bbe\u8ba1\u5b8c\u6574\u7535\u8def\u539f\u7406\u56fe\u3001\u5339\u914d\u5e76\u91c7\u8d2d\u96f6\u90e8\u4ef6\u3001\u751f\u6210\u9762\u5305\u677f\u539f\u578b\u5e03\u5c40\u548c\u710a\u63a5\u7248\u5e03\u5c40\u56fe\u3002\u65e0\u9700\u7535\u5b50\u5de5\u7a0b\u80cc\u666f\u3002\u4ece\u60f3\u6cd5\u5230\u539f\u578b\u7684\u4e00\u7ad9\u5f0f\u786c\u4ef6\u5f00\u53d1\u5e73\u53f0\u3002'
p4['slug'] = 'easycircuit'
p4['homepage'] = 'https://www.producthunt.com/r/p/1208295'
p4['url'] = 'https://www.producthunt.com/r/p/1208295'
p4['type'] = 'website'
p4['sourceChannels'] = ['producthunt']
p4['sourceUrl'] = 'https://www.producthunt.com/r/p/1208295?app_id=339'
p4['tags'] = ['\u786c\u4ef6\u539f\u578b', '\u7535\u8def\u8bbe\u8ba1', 'AI\u8f85\u52a9\u8bbe\u8ba1', '\u521b\u5ba2', '\u7269\u8054\u7f51']
p4['analysis'] = {
    'targetAudience': '\u6709\u521b\u610f\u60f3\u6cd5\u4f46\u6ca1\u6709\u7535\u5b50\u5de5\u7a0b\u80cc\u666f\u7684\u5f00\u53d1\u8005\u3001\u521b\u5ba2\u3001\u4ea7\u54c1\u7ecf\u7406\u548c\u7231\u597d\u8005',
    'useCases': [
        '\u4ece\u81ea\u7136\u8bed\u8a00\u63cf\u8ff0\u751f\u6210\u5b8c\u6574\u7535\u8def\u539f\u7406\u56fe',
        '\u81ea\u52a8\u5339\u914d\u96f6\u90e8\u4ef6\u5e76\u4e00\u952e\u4e0b\u5355\u5957\u4ef6',
        '\u9762\u5305\u677f\u539f\u578b\u642d\u5efa\u5230\u710a\u63a5\u7248\u6210\u54c1',
        '\u5b66\u4e60\u7535\u8def\u8bbe\u8ba1\u539f\u7406\u2014\u2014AI\u89e3\u91ca\u6bcf\u4e00\u6b65\u8bbe\u8ba1\u51b3\u7b56'
    ],
    'designIntent': '\u5c06 Vibe Coding \u7684\u7406\u5ff5\u5f15\u5165\u786c\u4ef6\u9886\u57df\u3002\u521b\u59cb\u4eba\u81ea\u5df1\u56e0\u60f3\u505a\u690d\u7269\u751f\u957f\u5b9e\u9a8c\u7bb1\u4f46\u4e0d\u61c2\u7535\u8def\u8bbe\u8ba1\uff0c\u7ecf\u5386\u6570\u5929\u7814\u7a76\u540e\u51b3\u5b9a\u6253\u9020\u8fd9\u6b3e\u5de5\u5177\uff0c\u8ba9\u975e EE \u80cc\u666f\u7684\u4eba\u4e5f\u80fd\u8f7b\u677e\u5b9e\u73b0\u786c\u4ef6\u521b\u610f\u3002',
    'problemSolved': '\u786c\u4ef6\u539f\u578b\u8bbe\u8ba1\u7684\u95e8\u69db\u6781\u9ad8\uff1a\u9700\u8981\u770b\u6570\u636e\u624b\u518c\u3001\u9009\u578b\u3001\u67e5\u5e93\u5b58\u3001\u8bbe\u8ba1\u539f\u7406\u56fe\u3001\u5e03\u7ebf\u3002\u4f20\u7edf\u6d41\u7a0b\u8017\u65f6\u6570\u5929\u5230\u6570\u5468\u3002EasyCircuit \u5c06\u6574\u4e2a\u8fc7\u7a0b\u538b\u7f29\u5230\u4e00\u53e5\u8bdd\u63cf\u8ff0 + AI\u8bbe\u8ba1 + \u4e00\u952e\u4e0b\u5355\u6750\u6599\u5305 + \u5206\u6b65\u642d\u5efa\u3002',
    'score': 8,
    'scoreReason': '\u5c06 AI \u80fd\u529b\u521b\u65b0\u6027\u5730\u5e94\u7528\u5230\u786c\u4ef6\u9886\u57df\uff0c\u89e3\u51b3\u771f\u5b9e\u75db\u70b9\uff0c\u6280\u672f\u65b9\u6848\u624e\u5b9e\uff08AI+\u4f9b\u5e94\u94fe\u6574\u5408\uff09\uff0c\u62a4\u57ce\u6cb3\u660e\u663e\u3002\u4f46\u4ea7\u54c1\u5c1a\u65e9\uff08290+\u96f6\u4ef6\u5e93\uff09\uff0c\u90e8\u5206\u9ad8\u7ea7\u573a\u666f\u4ecd\u9700\u4eba\u5de5\u786e\u8ba4\u3002',
    'competitors': [
        {'name': 'Cirkit Designer', 'url': 'https://www.cirkitdesigner.com', 'comparison': '\u6d4f\u89c8\u5668\u7aef AI \u7535\u8def\u8bbe\u8ba1\u5de5\u5177\uff0c\u652f\u6301\u4eff\u771f\uff0c\u4f46\u65e0\u4e00\u952e\u91c7\u8d2d\u548c\u5957\u4ef6\u914d\u9001'},
        {'name': 'TSCircuit', 'url': 'https://tscircuit.com', 'comparison': '\u4ee3\u7801\u751f\u6210 PCB\uff0c\u9700\u8981 React \u7f16\u7a0b\u77e5\u8bc6\uff0c\u66f4\u9002\u5408\u6709\u7f16\u7a0b\u80cc\u666f\u7684\u7528\u6237'}
    ]
}

# ============================================
# Product 5: SUB/WAVE
# ============================================
p5 = {}
p5['id'] = 'producthunt.com/r/p/1207636'
p5['name'] = 'SUB/WAVE - AI \u7535\u53f0 DJ'
p5['description'] = '\u81ea\u6258\u7ba1\u5f00\u6e90\u7535\u53f0\u7cfb\u7edf\uff0c\u4f7f\u7528 AI DJ 24/7 \u64ad\u653e\u4f60\u7684\u4e2a\u4eba\u97f3\u4e50\u5e93\u3002AI DJ \u53ef\u4ee5\u9009\u66f2\u3001\u505a\u7535\u53f0 ID\u3001\u62a5\u65f6\u64ad\u5929\u6c14\u3001\u63a5\u53d7\u542c\u4f17\u70b9\u6b4c\u3002\u652f\u6301\u672c\u5730 Ollama \u6a21\u578b\u3001\u672c\u5730 TTS\uff0c\u65e0\u9700\u4e91\u670d\u52a1\u3002\u4e00\u4e2a\u6d41\u3001\u6240\u6709\u542c\u4f17\u540c\u65f6\u6536\u542c\u540c\u4e00\u9996\u6b4c\uff0c\u6ca1\u6709\u8df3\u8fc7\u6309\u94ae\u3002'
p5['slug'] = 'sub-wave'
p5['homepage'] = 'https://www.getsubwave.com'
p5['url'] = 'https://www.getsubwave.com'
p5['type'] = 'saas'
p5['sourceChannels'] = ['producthunt']
p5['sourceUrl'] = 'https://www.producthunt.com/r/p/1207636?app_id=339'
p5['tags'] = ['AI\u7535\u53f0', '\u97f3\u4e50', '\u81ea\u6258\u7ba1', '\u5f00\u6e90', '\u672c\u5730AI']
p5['analysis'] = {
    'targetAudience': '\u62e5\u6709\u4e2a\u4eba\u97f3\u4e50\u5e93\uff08Navidrome/Plex\u7b49\uff09\u5e76\u5e0c\u671b\u627e\u56de\u7535\u53f0\u5f0f\u542c\u6b4c\u4f53\u9a8c\u7684\u97f3\u4e50\u7231\u597d\u8005',
    'useCases': [
        '\u5c06\u4e2a\u4eba\u97f3\u4e50\u5e93\u53d8\u6210 24/7 \u76f4\u64ad\u7535\u53f0',
        'AI DJ \u6839\u636e\u65f6\u95f4\u3001\u5929\u6c14\u3001\u542c\u4f17\u70b9\u6b4c\u667a\u80fd\u9009\u66f2',
        '\u591a\u89d2\u8272 DJ \u8f6e\u73ed\u3001\u5609\u5bbe\u4e3b\u6301\u804a\u5929',
        '\u5bb6\u4eba\u670b\u53cb\u540c\u65f6\u6536\u542c\u540c\u4e00\u4e2a\u9891\u9053'
    ],
    'designIntent': '\u5728\u6d41\u5a92\u4f53\u65f6\u4ee3\u627e\u56de\u4f20\u7edf\u7535\u53f0\u7684\u5171\u4eab\u6536\u542c\u4f53\u9a8c\u3002\u521b\u59cb\u4eba\u8ba4\u4e3a Spotify \u7b49\u6d41\u5a92\u4f53\u867d\u7136\u63d0\u4f9b\u4e86\u65e0\u9650\u9009\u62e9\uff0c\u4f46\u8ba9\u4eba\u5b64\u72ec\u5730\u56f0\u5728\u81ea\u5df1\u7684\u7b97\u6cd5\u6ce1\u6ce1\u91cc\u3002SUB/WAVE \u8ba9\u6240\u6709\u4eba\u90fd\u542c\u5230\u540c\u4e00\u9996\u6b4c\u3001\u540c\u4e00\u4e2a DJ\u3002',
    'problemSolved': '\u73b0\u4ee3\u6d41\u5a92\u4f53\u542c\u6b4c\u4f53\u9a8c\u662f\u5b64\u72ec\u548c\u7b97\u6cd5\u9a71\u52a8\u7684\u3002\u4f20\u7edf\u7535\u53f0\u53c8\u65e0\u6cd5\u4f7f\u7528\u4e2a\u4eba\u97f3\u4e50\u5e93\u3002SUB/WAVE \u7ed3\u5408\u4e2a\u4eba\u97f3\u4e50\u5e93+AI DJ+\u5171\u4eab\u6d41\uff0c\u521b\u9020\u51fa\u72ec\u7279\u7684\u79c1\u4eba\u7535\u53f0\u4f53\u9a8c\u3002',
    'score': 7,
    'scoreReason': '\u521b\u610f\u72ec\u7279\u3001\u5f00\u6e90 MIT \u534f\u8bae\u3001\u6280\u672f\u5b9e\u73b0\u5b8c\u6574\uff08AI DJ+\u672c\u5730TTS+\u591a\u5e73\u53f0\u5ba2\u6237\u7aef\uff09\uff0c\u4f46\u53d7\u4f17\u8f83\u7a84\uff08\u9700\u8981\u81ea\u6709\u97f3\u4e50\u5e93\u548c\u81ea\u6258\u7ba1\u80fd\u529b\uff09\uff0c\u5bf9\u7eaf\u6d41\u5a92\u4f53\u7528\u6237\u4e0d\u9002\u7528\u3002',
    'competitors': [
        {'name': 'Plexamp', 'url': 'https://www.plex.tv/plexamp/', 'comparison': 'Plex \u7684\u97f3\u4e50\u64ad\u653e\u5668\uff0c\u6709 AI DJ \u529f\u80fd\u4f46\u9700 Plex Pass \u8ba2\u9605\uff0c\u65e0\u5171\u4eab\u6536\u542c\u6a21\u5f0f'},
        {'name': 'Spotify AI DJ', 'url': 'https://www.spotify.com', 'comparison': 'Spotify \u5185\u7f6e AI DJ \u63a8\u8350\uff0c\u4f46\u4e0d\u80fd\u4f7f\u7528\u81ea\u6709\u97f3\u4e50\u5e93\uff0c\u4e14\u662f\u5355\u4eba\u6536\u542c\u6a21\u5f0f'}
    ]
}

products = [p1, p2, p3, p4, p5]

# Read current DB and remove corrupted entries
with open(f'{BASE}/data/products.json', encoding='utf-8') as f:
    db_data = json.load(f)

# Remove the 5 last entries (corrupted from previous run)
original_count = len(db_data['products'])
db_data['products'] = db_data['products'][:original_count - 5]

# Build report
report = {
    'date': date_str,
    'generatedAt': iso_now,
    'productCount': len(products),
    'summary': {
        'totalCandidates': 184,
        'dedupedCount': 0,
        'filteredOutTechnical': 179,
        'selectedCount': 5
    },
    'products': []
}

for p in products:
    prod_entry = {
        'id': p['id'],
        'name': p['name'],
        'slug': p['slug'],
        'description': p['description'],
        'url': p['url'],
        'homepage': p['homepage'],
        'type': p['type'],
        'appStoreName': None,
        'appStoreUrl': None,
        'screenshotUrl': None,
        'appStoreScreenshots': [],
        'tags': p['tags'],
        'sourceChannels': p['sourceChannels'],
        'sourceUrl': p['sourceUrl'],
        'firstSeen': iso_now,
        'analysis': p['analysis']
    }
    if p['slug'] == 'voicehop':
        prod_entry['appStoreName'] = 'Chrome Web Store'
        prod_entry['appStoreUrl'] = 'https://chromewebstore.google.com/detail/voicehop-real-time-audio/gpjfekccjgnojplebmaafgbhjggimfio'
    if p['slug'] == 'pinery-prose':
        prod_entry['appStoreName'] = 'Mac App Store'
        prod_entry['appStoreUrl'] = 'https://apps.apple.com/app/pinery-self-publishing-app/id6747726205'
    report['products'].append(prod_entry)

# Save report
report_dir = f'{BASE}/reports/daily'
os.makedirs(report_dir, exist_ok=True)
report_path = f'{report_dir}/{date_str}.json'
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

# Add to DB
for p in products:
    entry = {
        'id': p['id'],
        'name': p['name'],
        'description': p['description'],
        'url': p['url'],
        'homepage': p['homepage'],
        'slug': p['slug'],
        'type': p['type'],
        'tags': p['tags'],
        'sourceChannels': p['sourceChannels'],
        'sourceUrl': p['sourceUrl'],
        'firstSeen': iso_now,
        'cooldownExpiresAt': cooldown_date,
        'metrics': {
            'featuredInDaily': True,
            'featuredInWeekly': False,
            'timesFeatured': 1,
            'lastFeatured': date_str,
            'mentionCount7d': 1,
            'growthScore': 50
        },
        'analysis': p['analysis']
    }
    db_data['products'].append(entry)

db_data['lastUpdated'] = iso_now
db_data['version'] = db_data.get('version', 1) + 1

with open(f'{BASE}/data/products.json', 'w', encoding='utf-8') as f:
    json.dump(db_data, f, ensure_ascii=False, indent=2)

# Verify no corrupted characters
with open(report_path, encoding='utf-8') as f:
    content = f.read()
corrupt = sum(1 for ch in content if ord(ch) == 65533)
print(f'Report saved: {report_path}')
print(f'Database: {len(db_data["products"])} products')
print(f'Corrupted characters: {corrupt}')
if corrupt == 0:
    print('ALL CLEAN!')
else:
    print('STILL CORRUPTED! Need to fix.')

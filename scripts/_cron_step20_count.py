import re, subprocess

# local index
idx = open('/home/pin/aI-product-daily-peport/docs/index.html').read()
m = re.search(r'8月5日.*?(?=<h2 class="blog-post-title day-post-title"|$)', idx, re.S)
seg = m.group(0) if m else ''
names = re.findall(r'entry-name">([^<]+)<', seg)
print("local index 8月5日 section products:", len(names))
for n in names:
    print("  -", n)

# also check archive.html
arch = open('/home/pin/aI-product-daily-peport/docs/archive.html').read()
print("\narchive contains Wispr:", 'Wispr' in arch, "| Reelang:", 'Reelang' in arch, "| Workout:", 'Workout' in arch)

# live index 8月5日 section
live = subprocess.run(['curl', '-s', '-m', '30', 'https://ai-daily.asdasd.vip/'], capture_output=True, text=True).stdout
m2 = re.search(r'8月5日.*?(?=<h2 class="blog-post-title day-post-title"|$)', live, re.S)
seg2 = m2.group(0) if m2 else ''
names2 = re.findall(r'entry-name">([^<]+)<', seg2)
print("\nlive index 8月5日 section products:", len(names2))
for n in names2:
    print("  -", n)

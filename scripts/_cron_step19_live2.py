import subprocess, os

base = '/home/pin/aI-product-daily-peport/docs/products'
names = sorted(os.listdir(base))
print(f"=== docs/products/ ({len(names)} files) ===")
for n in names[:15]:
    print(" ", n)
hits = [n for n in names if any(k in n for k in ['wispr', 'reelang', 'pageforth', 'adant', 'workout'])]
print("our 5:", hits)

# what does the live 404 page look like (title)?
r = subprocess.run(['curl', '-s', '-m', '30', 'https://ai-daily.asdasd.vip/products/wispr-flow-notetaker.html'], capture_output=True, text=True)
html = r.stdout
i = html.find('<title>')
print("\n=== live 404 title ===")
print(html[i:i+120] if i >= 0 else "no title tag")

idx = subprocess.run(['curl', '-s', '-m', '30', 'https://ai-daily.asdasd.vip/'], capture_output=True, text=True).stdout
print("\n=== live index size:", len(idx), "| contains Wispr:", 'Wispr' in idx)
j = idx.find('8月5日')
print(idx[max(0,j-100):j+200].replace('\n',' ')[:350] if j >= 0 else "no 8月5日 marker")

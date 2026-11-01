with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="sec-advisor-qr"')
with open('scratch/sec_qr.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx:idx+3500])

print("Saved sec-advisor-qr to scratch/sec_qr.txt")


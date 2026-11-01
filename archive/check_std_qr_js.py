with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("std-qr-id")
while idx != -1:
    print(text[idx-50:idx+250])
    print("="*40)
    idx = text.find("std-qr-id", idx+1)


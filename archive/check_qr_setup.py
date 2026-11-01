with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("const qrId = document.getElementById('std-qr-id');")
print(text[idx-200:idx+800])


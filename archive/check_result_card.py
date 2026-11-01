with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="qr-checkin-result-card"')
print(text[idx:idx+2000])


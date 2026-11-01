with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function startRealCameraScanner()')
print(text[idx-50:idx+2500])


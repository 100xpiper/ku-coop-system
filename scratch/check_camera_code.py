with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('startRealCameraScanner')
if idx != -1:
    print(text[idx-100:idx+800])
else:
    print("Not found")


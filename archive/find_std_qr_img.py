with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('std-qr-image')
if idx != -1:
    print(text[idx-50:idx+600])
    idx2 = text.find('std-qr-image', idx+50)
    if idx2 != -1:
        print("Second occurrence:")
        print(text[idx2-50:idx2+600])


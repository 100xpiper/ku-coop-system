with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('openMapForStudent')
while idx != -1:
    print(f"Found at {idx}: {text[idx-50:idx+70]}")
    idx = text.find('openMapForStudent', idx+1)


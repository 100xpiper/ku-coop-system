with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('openCompanyMap')
while idx != -1:
    print(f"Found at {idx}: {text[idx-30:idx+60]}")
    idx = text.find('openCompanyMap', idx+1)


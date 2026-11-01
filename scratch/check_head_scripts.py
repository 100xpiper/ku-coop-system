with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<!-- SheetJS')
print(text[idx-50:idx+600])


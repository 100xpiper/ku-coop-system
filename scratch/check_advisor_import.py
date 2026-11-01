with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="admin-card-import"')
print(text[idx+2000:idx+4500])


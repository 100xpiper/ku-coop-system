with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("function renderNav(role)")
print(text[idx+400:idx+1200])


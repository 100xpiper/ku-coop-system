with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("function renderNav(role)")
print("Position:", idx)
start = max(0, idx - 100)
print(text[start:start+1500])


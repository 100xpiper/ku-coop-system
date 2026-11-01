with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("function initUserDashboard")
print(text[idx-300:idx])


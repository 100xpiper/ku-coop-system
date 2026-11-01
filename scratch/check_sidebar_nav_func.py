with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function sidebarNavigate')
if idx != -1:
    print(text[idx:idx+800])
else:
    print("sidebarNavigate not found")


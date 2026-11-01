with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("getElementById('sidebar-nav-container')")
if idx != -1:
    print(text[idx-50:idx+1200])
else:
    print("Not found")


with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function renderSidebarNav')
if idx != -1:
    print(text[idx:idx+1500])
else:
    # search where sidebar-nav-container is used
    idx2 = text.find("sidebar-nav-container")
    print(text[idx2-50:idx2+1500])


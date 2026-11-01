with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function renderSidebarNav')
if idx != -1:
    with open('scratch/sidebar_nav_js.txt', 'w', encoding='utf-8') as out:
        out.write(text[idx-50:idx+2500])
    print("Found renderSidebarNav")


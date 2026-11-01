with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("function buildSidebarNav")
with open('scratch/build_sidebar_nav_part3.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx+2500:idx+4500])


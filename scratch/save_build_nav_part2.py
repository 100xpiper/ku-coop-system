with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("function buildSidebarNav")
with open('scratch/build_sidebar_nav_part2.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx+1200:idx+3500])


with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("function buildSidebarNav")
with open('scratch/build_sidebar_nav.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx:idx+2500])
print("Saved buildSidebarNav to scratch/build_sidebar_nav.txt")


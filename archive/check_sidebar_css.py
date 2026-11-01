with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('.desktop-sidebar {')
if idx != -1:
    with open('scratch/css_sidebar.txt', 'w', encoding='utf-8') as out:
        out.write(text[idx-50:idx+2500])
    print("Found .desktop-sidebar CSS")


with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="admin-card-import"')
with open('scratch/admin_import_part2.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx+1200:idx+4500])


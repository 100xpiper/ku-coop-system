with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="admin-card-import"')
with open('scratch/admin_import_inspect.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx-50:idx+3500])
print("Saved to scratch/admin_import_inspect.txt")


with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="admin-student-preview-container"')
with open('scratch/preview_container_full.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx:idx+3500])


with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="admin-student-import-btn"')
print(text[idx-50:idx+1500])


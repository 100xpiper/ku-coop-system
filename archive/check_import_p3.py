with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function renderAdminStudentPreImportPreview')
with open('scratch/excel_import_part2.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx:idx+4500])


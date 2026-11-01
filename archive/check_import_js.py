with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function handleStudentExcelSelected')
with open('scratch/excel_import_js.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx:idx+4500])
print("Saved to scratch/excel_import_js.txt")


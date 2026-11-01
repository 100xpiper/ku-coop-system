with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('async function importStudentExcelFile()')
with open('scratch/import_func_inspect.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx:idx+4500])


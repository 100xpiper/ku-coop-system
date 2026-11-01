with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function importStudentExcelFile()')
with open('scratch/import_student_end.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx+2000:idx+4500])


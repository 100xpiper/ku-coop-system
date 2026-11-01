with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function importStudentExcelFile()')
with open('scratch/import_student_end2.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx+3500:idx+6500])


with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('importStudentExcelFile')
while idx != -1:
    print(text[idx-30:idx+100])
    idx = text.find('importStudentExcelFile', idx+1)


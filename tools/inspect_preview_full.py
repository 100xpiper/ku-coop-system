with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function renderAdvisorImportPreview')
pos_end = text.find('function processAdvisorStudentFileImport')
print(text[pos:pos_end])

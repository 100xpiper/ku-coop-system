with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find('function renderAdvisorImportPreview')
pos2 = text.find('function processAdvisorStudentFileImport')
pos3 = text.find('function clearAdvisorImportFile')
print(f"renderAdvisorImportPreview at {pos1}")
print(f"processAdvisorStudentFileImport at {pos2}")
print(text[pos1:pos1+2000])

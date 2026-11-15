with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function openAdvisorAddStudentModal')
print(text[pos:pos+3500])

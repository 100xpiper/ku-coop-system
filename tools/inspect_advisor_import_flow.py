with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('downloadAdvisorStudentTemplate')
print(text[pos+1000:pos+3500])

with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function getAdvisorSections')
print(text[pos:pos+1500])

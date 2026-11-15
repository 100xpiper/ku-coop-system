with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('adv-student-excel-input')
print(text[pos-200:pos+2500])

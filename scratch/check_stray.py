with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('sec-student-dash')
print(text[idx-50:idx+150])


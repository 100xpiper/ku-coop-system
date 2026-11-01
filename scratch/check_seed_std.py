with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('students: [')
if idx != -1:
    print(text[idx:idx+1500])


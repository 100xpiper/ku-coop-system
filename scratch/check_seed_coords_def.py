with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('students: [')
print(text[idx:idx+1500])


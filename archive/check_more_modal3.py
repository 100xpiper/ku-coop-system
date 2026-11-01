with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx2 = text.find('Modal 3')
print(text[idx2+1500:idx2+3500])


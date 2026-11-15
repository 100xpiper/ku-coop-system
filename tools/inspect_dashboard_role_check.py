with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('if (stdName) stdName.textContent')
print(text[pos-2500:pos-1000])

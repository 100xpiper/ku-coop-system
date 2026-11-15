with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('if (stdName) stdName.textContent')
print(text[pos-1000:pos+1000])

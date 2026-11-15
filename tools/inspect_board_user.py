with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('board(user)')
print(text[pos-100:pos+200])

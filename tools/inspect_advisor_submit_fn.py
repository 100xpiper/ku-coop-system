with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('adv-import-submit-btn')
pos2 = text.find('function', pos)
print(text[pos2:pos2+3500])

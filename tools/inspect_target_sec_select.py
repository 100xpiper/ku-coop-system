with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('adv-import-target-sec-select')
print(text[pos-100:pos+800])

with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('adv-add-std-id')
pos2 = text.find('onclick=', pos)
print(text[pos2-50:pos2+200])

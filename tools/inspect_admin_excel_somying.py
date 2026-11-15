with open('js/admin-excel.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('somying.j@ku.th')
print(text[pos-400:pos+400])

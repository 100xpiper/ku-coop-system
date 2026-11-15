with open('js/admin-excel.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('สมหญิง แจ่มใส')
print(text[pos-300:pos+600])

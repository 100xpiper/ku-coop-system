with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="adv-import-preview-container"')
print(text[pos:pos+1000])

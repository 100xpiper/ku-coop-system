with open('server.ps1', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('letter-spacing:10px;')
print(text[pos:pos+1500])

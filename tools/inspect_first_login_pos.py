with open('server.ps1', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('POST /api/send-first-login')
print(text[pos-100:pos+300])

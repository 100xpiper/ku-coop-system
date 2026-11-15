with open('server.ps1', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('POST /api/send-otp')
print(text[pos:pos+2500])

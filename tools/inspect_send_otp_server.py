with open('server.ps1', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('POST /api/send-otp')
if pos == -1:
    pos = text.find('/api/send-otp')
    pos = text.find('/api/send-otp', pos + 30)

print(text[pos-20:pos+1500])

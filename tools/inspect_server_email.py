with open('server.ps1', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find('/api/send-otp')
print('=== /api/send-otp ===')
print(text[pos1-50:pos1+1500])

pos2 = text.find('/api/send-first-login')
print('=== /api/send-first-login ===')
print(text[pos2-50:pos2+1500])

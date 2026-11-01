with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find("function handleLogin(event)")
pos2 = text.find("function showFirstLoginPasswordResetModal(user)")
pos3 = text.find("function handleVerifyOtp(event)")
print('handleLogin pos:', pos1)
print('showFirstLogin pos:', pos2)
print('handleVerifyOtp pos:', pos3)
print('\n--- handleLogin snippet ---')
print(repr(text[pos1:pos1+800]))


with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function initUserDashboard')
print(text[pos:pos+600])

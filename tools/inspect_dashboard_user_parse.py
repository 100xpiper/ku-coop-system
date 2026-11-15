with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('buildSidebarNav(currentRole)')
print(text[pos-1200:pos+100])

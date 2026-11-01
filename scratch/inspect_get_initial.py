with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find("const savedSession = localStorage.getItem('currentUser');")
pos2 = text.find("window.addEventListener('DOMContentLoaded'", pos1)
print(repr(text[pos1:pos2]))

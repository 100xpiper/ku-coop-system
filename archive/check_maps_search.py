with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('https://www.google.com/maps/search/')
if idx != -1:
    print(text[idx-200:idx+200])


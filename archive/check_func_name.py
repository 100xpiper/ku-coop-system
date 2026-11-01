with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('https://www.google.com/maps/search/')
func_start = text.rfind('function ', 0, idx)
print(text[func_start:func_start+100])


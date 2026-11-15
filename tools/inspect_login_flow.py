with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('async function handleLogin')
if pos == -1:
    pos = text.find('function handleLogin')
print(text[pos:pos+2500])

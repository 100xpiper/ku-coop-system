with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('dispatchOtpEmail')
print(text[pos-50:pos+1500])

with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('สวัสดี')
while pos != -1:
    print('Found at', pos)
    print(text[pos-50:pos+300])
    print('='*50)
    pos = text.find('สวัสดี', pos+1)

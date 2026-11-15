with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('submitAdvisorAddStudent')
if pos == -1:
    pos = text.find('adv-add-std-id')
print(text[pos-100:pos+1200])

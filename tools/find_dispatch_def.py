with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'dispatchOtpEmail', text)
for m in matches:
    pos = m.start()
    print('Found at', pos)
    print(text[pos-50:pos+300])
    print('='*50)

with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'Q2222|somying', text, re.I)
for m in matches:
    pos = m.start()
    print(text[pos-100:pos+200])
    print('='*50)

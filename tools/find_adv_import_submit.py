with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'adv-import-submit-btn', text)
for m in matches:
    pos = m.start()
    print('Found at', pos)
    print(text[pos-100:pos+300])
    print('='*50)

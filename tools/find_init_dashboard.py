with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'initDashboard\s*\(', text)
for m in matches:
    pos = m.start()
    print('Found at', pos)
    print(text[pos-200:pos+200])
    print('='*50)

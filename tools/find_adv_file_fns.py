with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'handleAdvisorStudentFile|commitAdvisorStudentImport|submitAdvisorAddStudent', text)
for m in matches:
    pos = m.start()
    print('Found at', pos)
    print(text[pos:pos+1000])
    print('='*50)

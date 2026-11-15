with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'fetch\([^\)]+\)', text)
print('Fetch calls in dashboard.html:', len(matches))
for m in matches[:10]:
    print('  -', m)

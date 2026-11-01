with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [line for line in text.splitlines() if 'sidebar-nav' in line]
for m in matches[:10]:
    print(m)


with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'function\s+([a-zA-Z0-9_]*nav[a-zA-Z0-9_]*)\s*\(', text, re.IGNORECASE)
print("Nav functions:", matches)


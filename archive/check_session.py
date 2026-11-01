with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [line for line in text.splitlines() if 'sessionStorage' in line or 'currentUser' in line or 'logged' in line.lower()]
print(f"Matches count: {len(matches)}")
for m in matches[:10]:
    print(" - ", m.strip()[:100])


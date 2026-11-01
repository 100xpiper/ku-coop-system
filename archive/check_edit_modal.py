with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [line for line in text.splitlines() if 'company_lat' in line or 'modal-edit-user' in line or 'editUser' in line]
print(f"Matches count: {len(matches)}")
for m in matches[:10]:
    print(" - ", m.strip()[:100])


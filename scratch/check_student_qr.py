with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [line for line in text.splitlines() if 'sec-student-qrcode' in line or 'qrcode' in line.lower()]
print(f"Total qrcode lines: {len(matches)}")
for m in matches[:10]:
    print(" - ", m.strip()[:100])


with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [line for line in text.splitlines() if any(k in line for k in ['พิกัด', 'latitude', 'longitude', 'latStr', 'lngStr', 'รัศมี'])]
print(f"Total matches: {len(matches)}")
for m in matches[:25]:
    print(" - ", m.strip()[:100])


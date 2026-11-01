import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

sections = re.findall(r'id=["\'](sec-[^"\']+)["\']', text)
print("Section IDs:", sections)

evidence_matches = [line for line in text.splitlines() if 'หลักฐาน' in line]
print(f"Evidence lines count: {len(evidence_matches)}")
for line in evidence_matches[:10]:
    print(" - ", line[:120].strip())


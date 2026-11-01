with open('docs/Project_Progress_Report_Final.md', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'อาจารย์\s*สมชาย(?:\s*แจ่มใส)?', text)
print('Matches count:', len(matches))
for m in matches:
    print(repr(m))

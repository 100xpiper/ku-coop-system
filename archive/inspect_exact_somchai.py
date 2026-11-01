with open('docs/Project_Progress_Report_Final.md', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'สมชาย.{0,20}', text)
for m in matches:
    print(repr(m))

with open('docs/Project_Progress_Report_Final.md', 'r', encoding='utf-8') as f:
    text = f.read()

import re
pos = 0
while True:
    p = text.find('สมชาย', pos)
    if p == -1:
        break
    snippet = text[max(0, p-10):p+30]
    print(f'At {p}: {repr(snippet)}')
    pos = p + 1

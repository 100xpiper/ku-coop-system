with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'currentUser', text)]
for idx, p in enumerate(matches):
    print(f'Match {idx+1} at {p}:')
    print(repr(text[p-40:p+120]))
    print('---')


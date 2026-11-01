with open('index.html', 'r', encoding='utf-8') as f:
    text_idx = f.read()

import re
matches_idx = list(re.finditer(r"currentUser", text_idx))
print('Total currentUser in index.html:', len(matches_idx))
for i, m in enumerate(matches_idx):
    start = max(0, m.start() - 30)
    end = min(len(text_idx), m.end() + 30)
    print(f'Match {i+1}: {repr(text_idx[start:end])}')


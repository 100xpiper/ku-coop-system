import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = list(re.finditer(r"localStorage\.getItem\(['\"]currentUser['\"]\)", text))
print('Total matches in dashboard.html:', len(matches))
for i, m in enumerate(matches):
    start = max(0, m.start() - 30)
    end = min(len(text), m.end() + 30)
    print(f'Match {i+1}: {repr(text[start:end])}')

with open('index.html', 'r', encoding='utf-8') as f:
    text_idx = f.read()

matches_idx = list(re.finditer(r"localStorage\.(?:getItem|setItem|removeItem)\(['\"]currentUser['\"]\)", text_idx))
print('\nTotal matches in index.html:', len(matches_idx))
for i, m in enumerate(matches_idx):
    start = max(0, m.start() - 30)
    end = min(len(text_idx), m.end() + 30)
    print(f'Match {i+1}: {repr(text_idx[start:end])}')


# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer('index.html', text)]
print('Matches for index.html:', len(matches))
for m in matches:
    print(repr(text[max(0, m-50):min(len(text), m+70)]))


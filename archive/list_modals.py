# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'id=["\']modal-[a-zA-Z0-9_\-]+["\']', text)
print('Modals found:', set(matches))


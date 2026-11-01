# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = "const targetModal = urlParams.get('modal');"
print(text[text.find(target):text.find(target)+800])


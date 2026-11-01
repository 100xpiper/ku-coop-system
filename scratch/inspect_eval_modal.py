# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find("id=\"modal-eval-form\"")
print(text[pos:pos+1500])


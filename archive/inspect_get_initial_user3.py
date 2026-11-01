# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function getInitialUser()')
print(text[pos+2000:pos+3500])


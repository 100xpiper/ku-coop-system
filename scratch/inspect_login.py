# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find("localStorage.getItem('currentUser')")
print(text[pos-100:pos+1500])


# -*- coding: utf-8 -*-
with open('scratch/ch53_snippet.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines[:60]:
    if line.strip():
        safe_line = line.strip().encode('ascii', errors='replace').decode('ascii')
        print(safe_line[:90])


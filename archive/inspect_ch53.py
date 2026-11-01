# -*- coding: utf-8 -*-
with open('Project_Progress_Report_Final.md', 'r', encoding='utf-8') as f:
    text = f.read()

pos_53 = text.find('5.3')
with open('scratch/ch53_snippet.txt', 'w', encoding='utf-8') as out:
    out.write(text[pos_53:pos_53+3500])
print('Saved scratch/ch53_snippet.txt')


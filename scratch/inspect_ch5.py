# -*- coding: utf-8 -*-
with open('Project_Progress_Report_Final.md', 'r', encoding='utf-8') as f:
    text = f.read()

pos_ch5 = text.find('## บทที่ 5') if '## บทที่ 5' in text else text.find('5.3')
print('Position:', pos_ch5)
with open('scratch/ch5_snippet.txt', 'w', encoding='utf-8') as out:
    out.write(text[pos_ch5:pos_ch5+3000])
print('Saved scratch/ch5_snippet.txt')


# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('const evaluateDistanceAndDisplay =')
with open('scratch/eval_dist_code.txt', 'w', encoding='utf-8') as out:
    out.write(text[pos:pos+3500])
print('Saved scratch/eval_dist_code.txt')


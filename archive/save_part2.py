with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx2 = text.find('Modal 3')
with open('scratch/modal3_part2.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx2+1200:idx2+3200])


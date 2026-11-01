with open('tools/build_clean_report_final.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(350, len(lines)):
    print(f'{i+1}: {lines[i]}', end='')

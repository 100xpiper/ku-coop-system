with open('tools/build_clean_report_final.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('Total lines:', len(lines))
for i in range(min(50, len(lines))):
    print(f'{i+1}: {lines[i]}', end='')

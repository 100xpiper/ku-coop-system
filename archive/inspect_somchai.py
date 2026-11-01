with open('docs/Project_Progress_Report_Final.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines, 1):
    if 'สมชาย' in l:
        print(f'Line {i}: {l.strip()}')

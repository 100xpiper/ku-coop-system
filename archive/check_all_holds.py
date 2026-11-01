with open('scratch/transcript_lines.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
blocks = text.split('=== Line ')
print('Total user blocks:', len(blocks))
for b in blocks:
    if not b.strip():
        continue
    header = b.split('\n')[0]
    content = '\n'.join(b.split('\n')[1:])
    for word in ['พัก', 'ข้าม', 'ค่อย', 'ไว้ก่อน', 'ทีหลัง', 'ค้าง']:
        if word in content:
            # print line containing word
            for l in content.split('\n'):
                if l.strip().startswith('<ADDITIONAL_METADATA>') or l.strip().startswith('The current local'):
                    break
                if word in l:
                    print(f'[{header[:15]}] ({word}): {l.strip()[:100]}')


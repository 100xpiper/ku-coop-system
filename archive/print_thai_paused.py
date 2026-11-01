with open('scratch/transcript_lines.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re

blocks = text.split('=== Line ')
with open('scratch/paused_report.txt', 'w', encoding='utf-8') as out:
    for b in blocks:
        if not b.strip():
            continue
        header = b.split('\n')[0]
        content = '\n'.join(b.split('\n')[1:])
        if any(k in content for k in ['พัก', 'ไว้ก่อน', 'ค่อยทำ', 'ข้าม', 'ค้าง']):
            out.write(f'=== Line {header} ===\n')
            for line in content.split('\n'):
                if line.strip().startswith('<ADDITIONAL_METADATA>') or line.strip().startswith('The current local'):
                    break
                if line.strip():
                    out.write('   ' + line.strip() + '\n')
            out.write('\n')

print("Written to scratch/paused_report.txt successfully!")


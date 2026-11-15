import docx
import re
import os

doc_path = r'docs/บันทึกผลงานและผลการทดลอง_สอดคล้องกับ_Timesheet_วงศพัทธ์_อุเทน_6521655442.docx'
doc = docx.Document(doc_path)
full_text = '\n'.join([p.text for p in doc.paragraphs] + [cell.text for t in doc.tables for row in t.rows for cell in row.cells])

print('=== VERIFICATION OF DOCX ===')
print('Length of text:', len(full_text))

# Check required info
assert 'วงศพัทธ์ อุเทน' in full_text, 'Missing student name!'
assert '6521655442' in full_text, 'Missing student ID 6521655442!'
assert '6510402280' not in full_text, 'Found OLD student ID 6510402280!'
assert 'อาจารย์ปรวี วงศ์สวัสดิ์สุริยะ' in full_text, 'Missing advisor name!'

# Check forbidden words
forbidden = [
    'KU Science Smart',
    'ระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์',
    'System Usability Scale',
    'ความพึงพอใจ'
]
for f in forbidden:
    matches = [m.start() for m in re.finditer(re.escape(f), full_text, re.IGNORECASE)]
    print(f'Checking forbidden word "{f}": {len(matches)} occurrences')
    assert len(matches) == 0, f'Found forbidden word: {f}'

# Check chapters & pages alignment
assert 'หน้า 1' in full_text
assert 'หน้า 5' in full_text
assert 'หน้า 14' in full_text
assert 'หน้า 24' in full_text
assert 'หน้า 59' in full_text

# Check test cases
for i in range(1, 19):
    tc = f'TC-{i:02d}'
    assert tc in full_text, f'Missing {tc}!'

print('ALL ASSERTIONS PASSED!')
print('Images count in docx:', len(doc.inline_shapes))

# Check files exist and size
pdf_path = r'docs/บันทึกผลงานและผลการทดลอง_สอดคล้องกับ_Timesheet_วงศพัทธ์_อุเทน_6521655442.pdf'
md_path = r'docs/บันทึกผลงานและผลการทดลอง_สอดคล้องกับ_Timesheet_วงศพัทธ์_อุเทน_6521655442.md'

print('DOCX size:', os.path.getsize(doc_path), 'bytes')
print('PDF size:', os.path.getsize(pdf_path), 'bytes')
print('MD size:', os.path.getsize(md_path), 'bytes')


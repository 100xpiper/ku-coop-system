import docx
import re
import os

doc = docx.Document('docs/เอกสารบันทึกผลลัพธ์การดำเนินงานตาม_Timesheet_วงศพัทธ์_อุเทน_6521655442.docx')
text = '\n'.join([p.text for p in doc.paragraphs] + [c.text for t in doc.tables for r in t.rows for c in r.cells])

print('=== VERIFICATION OF DELIVERABLES DOCX ===')
assert 'วงศพัทธ์ อุเทน' in text, 'Missing student name'
assert '6521655442' in text, 'Missing student ID'
assert '6510402280' not in text, 'Found old student ID'
assert 'อาจารย์ปรวี วงศ์สวัสดิ์สุริยะ' in text, 'Missing advisor'

forbidden = [
    'KU Science Smart',
    'ระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์',
    'System Usability Scale',
    'ความพึงพอใจ'
]
for f in forbidden:
    matches = [m.start() for m in re.finditer(re.escape(f), text, re.IGNORECASE)]
    print(f'Checking "{f}": {len(matches)} occurrences')
    assert len(matches) == 0, f'Found forbidden word {f}'

for i in ['1.1', '1.2', '1.3', '2.1', '2.2', '3.1', '3.2', '4.1', '4.2', '4.3', '4.4', '4.5', '5.1', '5.2', '6.1', '6.2']:
    assert f'ข้อที่ {i}' in text or f'{i}' in text, f'Missing task {i}'

print('Image count in docx:', len(doc.inline_shapes))
print('SUCCESS! ALL ASSERTIONS PASSED!')


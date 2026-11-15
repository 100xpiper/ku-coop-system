import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('6521650102')
start = text.rfind('[', 0, pos)
end = text.find('];', pos) + 1

array_str = text[start:end]

# Split by individual object { ... }
# Look for id: '...' or student_id: '...'
pattern = re.compile(r'\{[^{}]+?student_id:\s*[\'"](?P<id>[^\'"]+)[\'"].*?name:\s*[\'"](?P<name>[^\'"]+)[\'"].*?\}', re.DOTALL)

students = []
for m in pattern.finditer(array_str):
    b = m.group(0)
    sid = m.group('id')
    name = m.group('name')
    sec_m = re.search(r'section:\s*[\'"]([^\'"]+)', b)
    comp_m = re.search(r'company_name:\s*[\'"]([^\'"]+)', b)
    adv_m = re.search(r'advisor_name:\s*[\'"]([^\'"]+)', b)
    status_m = re.search(r'status:\s*[\'"]([^\'"]+)', b)
    sem_m = re.search(r'semester:\s*[\'"]([^\'"]+)', b)
    
    students.append({
        'id': sid,
        'name': name,
        'sec': sec_m.group(1) if sec_m else '',
        'company': comp_m.group(1) if comp_m else '',
        'advisor': adv_m.group(1) if adv_m else '',
        'status': status_m.group(1) if status_m else '',
        'semester': sem_m.group(1) if sem_m else ''
    })

print(f'Total students found: {len(students)}')

# Group by semester and advisor
by_sem = {}
for s in students:
    sem = s['semester'] or 'ไม่ระบุ'
    adv = s['advisor'] or 'ไม่ระบุ'
    by_sem.setdefault(sem, {}).setdefault(adv, []).append(s)

for sem, advs in by_sem.items():
    total_stds = sum(len(v) for v in advs.values())
    print(f'\n==================================================')
    print(f'ภาคการศึกษา: {sem} (รวม {total_stds} คน)')
    print(f'==================================================')
    for adv, stds in advs.items():
        print(f'\n[อาจารย์ที่ปรึกษา: {adv}] ({len(stds)} คน):')
        for s in stds:
            print(f"  - {s['id']} | {s['name']} | {s['sec']} | สถานประกอบการ: {s['company']} | สถานะ: {s['status']}")

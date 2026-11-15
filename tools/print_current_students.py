import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('6521650102')
start = text.rfind('[', 0, pos)
end = text.find('];', pos) + 1
array_str = text[start:end]

pattern = re.compile(r'\{[^{}]+?student_id:\s*[\'"](?P<id>[^\'"]+)[\'"].*?name:\s*[\'"](?P<name>[^\'"]+)[\'"].*?\}', re.DOTALL)

current_students = []
for m in pattern.finditer(array_str):
    b = m.group(0)
    sem_m = re.search(r'semester:\s*[\'"]([^\'"]+)', b)
    sem = sem_m.group(1) if sem_m else ''
    if sem == 'ภาคต้น 2569':
        sid = m.group('id')
        name = m.group('name')
        sec_m = re.search(r'section:\s*[\'"]([^\'"]+)', b)
        comp_m = re.search(r'company_name:\s*[\'"]([^\'"]+)', b)
        adv_m = re.search(r'advisor_name:\s*[\'"]([^\'"]+)', b)
        status_m = re.search(r'status:\s*[\'"]([^\'"]+)', b)
        current_students.append({
            'id': sid,
            'name': name,
            'sec': sec_m.group(1) if sec_m else '',
            'company': comp_m.group(1) if comp_m else '',
            'advisor': adv_m.group(1) if adv_m else '',
            'status': status_m.group(1) if status_m else ''
        })

print(f'Students in ภาคต้น 2569: {len(current_students)}')
by_adv = {}
for s in current_students:
    by_adv.setdefault(s['advisor'], []).append(s)

for adv, stds in by_adv.items():
    print(f"\n{adv} (รวม {len(stds)} คน):")
    for s in stds:
        print(f"  {s['id']} | {s['name']} | {s['sec']} | {s['company']} | {s['status']}")

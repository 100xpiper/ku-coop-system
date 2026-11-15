# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

checks = [
    'id="cal-section-filter"',
    'id="cal-student-select"',
    'id="qr-scan-section-filter"',
    'id="qr-scan-student-select"',
    'onCalSectionFilterChange',
    'onQrSectionFilterChange',
    'populateAdvisorStudentSelects',
    'renderCalStudentSelectOptions',
    'renderQrStudentSelectOptions',
    'groupNorm.label =',
    'groupSpec.label ='
]

for c in checks:
    assert c in html, f"Missing: {c}"
    print(f"Verified: {c}")

print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")

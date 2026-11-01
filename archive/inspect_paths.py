with open('tools/build_clean_report_final.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'.*Project_Progress_Report_Final\..*', text)
for m in matches:
    print(m.strip())

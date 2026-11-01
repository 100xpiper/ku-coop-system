# -*- coding: utf-8 -*-
with open('docs/Project_Progress_Report_Final.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'href="Project_Progress_Report_Final.docx"'
replacement = 'href="Project_Progress_Report_Final_Latest.docx"'

if target in text:
    text = text.replace(target, replacement, 1)
    with open('docs/Project_Progress_Report_Final.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated download button link in HTML!")
else:
    print("Target already updated or not found.")

with open('docs/Project_Progress_Report_Final.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('tools/form_paragraphs.txt', 'w', encoding='utf-8') as out:
    for i, l in enumerate(lines, 1):
        if 'Form' in l or 'แบบฟอร์ม' in l:
            out.write(f"Line {i}: {l.strip()}\n\n")

print("Dumped all form paragraphs!")

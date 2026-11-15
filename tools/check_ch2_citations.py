import docx
import re

doc = docx.Document('docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs.docx')
for i in range(176, 230):
    p = doc.paragraphs[i]
    m = re.findall(r'\[\d+\]', p.text)
    if m:
        print(f"p{i}: {p.text.strip()[:60]} -> {m}")


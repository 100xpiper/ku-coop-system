import docx

doc = docx.Document('docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs_backup.docx')
for i in [91, 92, 93, 137, 138, 147, 148, 149]:
    p = doc.paragraphs[i]
    print(f"p{i}: text='{p.text}', xml={p._element.xml[:120]}...")


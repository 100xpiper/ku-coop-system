import docx

doc = docx.Document('docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs_backup.docx')
for i in range(58, 75):
    p = doc.paragraphs[i]
    print(f"p{i} text: '{p.text}'")
    if p.runs:
        print(f"   font={p.runs[0].font.name}, size={p.runs[0].font.size}, bold={p.runs[0].bold}")


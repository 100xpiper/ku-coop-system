import docx

doc = docx.Document('docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs_backup.docx')
for i in range(138, 160):
    print(f"p{i}: '{doc.paragraphs[i].text.strip()}'")


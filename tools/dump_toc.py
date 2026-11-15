import docx

doc = docx.Document('docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs.docx')
for i in range(55, 151):
    print(f"[{i}] {doc.paragraphs[i].text}")


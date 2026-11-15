import docx

doc = docx.Document('docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs_backup.docx')
for i, p in enumerate(doc.paragraphs):
    brs = p._element.xpath('.//w:br[@w:type="page"]')
    if brs:
        next_text = doc.paragraphs[i+1].text.strip() if i+1 < len(doc.paragraphs) else ""
        print(f"Page break at p{i} (text='{p.text}'), followed by p{i+1}: '{next_text[:40]}'")


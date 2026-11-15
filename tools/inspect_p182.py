import docx

doc = docx.Document('docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs.docx')
p = doc.paragraphs[182]
print(f"p182 text: '{p.text}'")
for i, r in enumerate(p.runs):
    drawings = r._element.xpath('.//w:drawing')
    print(f"run {i}: text='{r.text}', drawings={len(drawings)}")


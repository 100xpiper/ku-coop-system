import docx

doc = docx.Document('docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs.docx')
for i in range(177, 195):
    p = doc.paragraphs[i]
    drawings = p._element.xpath('.//w:drawing')
    txt = p.text.strip()
    if drawings or txt:
        print(f"[{i}] drawings={len(drawings)} | text='{txt}'")


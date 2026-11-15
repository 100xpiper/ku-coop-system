import docx

doc = docx.Document('docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs.docx')
for i in [180, 181, 182, 186, 187, 188, 189, 190]:
    p = doc.paragraphs[i]
    images = p._element.xpath('.//a:blip/@r:embed')
    drawings = p._element.xpath('.//w:drawing')
    print(f'p{i}: text="{p.text.strip()}", blips={len(images)}, drawings={len(drawings)}')


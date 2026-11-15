import docx

doc = docx.Document('docs/เล่มรายงานการพัฒนาระบบ_ตามเล่มตัวอย่าง.docx')
for i in range(138, 160):
    print(f"p{i}: '{doc.paragraphs[i].text.strip()}'")


import docx

doc = docx.Document('docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs.docx')
for i, p in enumerate(doc.paragraphs):
    if 'เอกสารและสิ่งอ้างอิง' in p.text:
        print(f"Header at {i}")
        for j in range(i, min(i + 25, len(doc.paragraphs))):
            t = doc.paragraphs[j].text.strip()
            if 'ประวัติ' in t:
                break
            if t:
                print(f"p{j}: {t}")


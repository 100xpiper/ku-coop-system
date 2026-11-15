import pymupdf

doc = pymupdf.open('docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs.pdf')

for p_idx in range(12, len(doc)):
    arabic_page = p_idx - 12 + 1
    txt = doc[p_idx].get_text()
    for line in txt.split('\n'):
        line_s = line.strip()
        if any(line_s.startswith(k) for k in ["บทที่", "1.", "2.", "3.", "4.", "5.", "ตารางที่", "ภาพที่", "เอกสาร", "ประวัติ"]):
            if len(line_s) < 80:
                print(f"p.{arabic_page}: {line_s}")


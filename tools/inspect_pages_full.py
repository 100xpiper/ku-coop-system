import pymupdf

doc = pymupdf.open('docs/เล่มรายงานการพัฒนาระบบ_ตามเล่มตัวอย่าง.pdf')
for p in range(9, 14):
    print(f"=== PHYSICAL PAGE {p+1} ===")
    print(doc[p].get_text())


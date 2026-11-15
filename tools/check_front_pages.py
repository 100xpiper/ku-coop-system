import pymupdf

doc = pymupdf.open('docs/เล่มรายงานการพัฒนาระบบ_ตามเล่มตัวอย่าง.pdf')
for p in range(8, 15):
    txt = doc[p].get_text().strip().split('\n')
    print(f"Physical page {p+1}: {txt[:2]}")


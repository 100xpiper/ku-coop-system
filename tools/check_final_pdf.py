import pymupdf

doc = pymupdf.open('docs/เล่มรายงานการพัฒนาระบบ_ตามเล่มตัวอย่าง.pdf')
print(f"Total pages in newly exported PDF: {len(doc)}")

# Check physical page 13 is Arabic page 1
txt13 = doc[12].get_text().strip().split('\n')
print(f"Physical page 13 (Arabic 1) starts with: {txt13[:2]}")

# Check references page
for i in range(len(doc)-10, len(doc)):
    txt = doc[i].get_text()
    if "เอกสารและสิ่งอ้างอิง" in txt:
        print(f"เอกสารและสิ่งอ้างอิง is on physical page {i+1} (Arabic {i-12+1})")
    if "ประวัติผู้จัดทำ" in txt:
        print(f"ประวัติผู้จัดทำ is on physical page {i+1} (Arabic {i-12+1})")


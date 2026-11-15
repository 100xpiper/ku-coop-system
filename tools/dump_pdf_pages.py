import pymupdf

doc = pymupdf.open('docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs.pdf')
for i in range(25):
    txt = doc[i].get_text().strip()
    first_line = txt.split('\n')[0] if txt else 'EMPTY'
    print(f"Physical Page {i+1}: {first_line[:70]}")


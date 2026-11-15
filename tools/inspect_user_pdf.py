import pymupdf

doc = pymupdf.open('docs/รายงานพัฒนาระบบ_ล่าสุด_user.pdf')
print(f"Total pages in user PDF: {len(doc)}")

for i in range(min(15, len(doc))):
    txt = doc[i].get_text().strip().split('\n')
    first = txt[0] if txt else ''
    print(f"Page {i+1}: {first[:80]}")


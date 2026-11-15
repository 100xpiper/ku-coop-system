import pymupdf

doc = pymupdf.open('docs/รายงานพัฒนาระบบ_ล่าสุด_user.pdf')

for p_num in range(len(doc)):
    txt = doc[p_num].get_text()
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    first_few = lines[:2]
    last_few = lines[-2:]
    # Check if there is a page number at top or bottom
    print(f"Physical Page {p_num+1}: lines={len(lines)}, first={first_few}, last={last_few}")


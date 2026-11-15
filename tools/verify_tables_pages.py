import pymupdf

doc = pymupdf.open('docs/รายงานพัฒนาระบบ_ล่าสุด_user.pdf')

for p_num in range(30, 34):
    txt = doc[p_num-1].get_text()
    for kw in ['ตารางที่ 1', 'ตารางที่ 2', 'ตารางที่ 3', 'ตารางที่ 4', 'ตารางที่ 5', 'ตารางที่ 6', 'ตารางที่ 7']:
        if kw in txt:
            print(f"{kw} is on Physical page {p_num} (Arabic page {p_num - 10})")


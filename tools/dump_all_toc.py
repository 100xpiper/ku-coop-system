import docx

doc = docx.Document('docs/รายงานพัฒนาระบบ_ล่าสุด_user.docx')
for i in range(57, 160):
    t = doc.paragraphs[i].text.strip()
    if t:
        print(f"p{i}: {t}")


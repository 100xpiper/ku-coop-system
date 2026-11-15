import docx

doc = docx.Document('docs/รายงานพัฒนาระบบ_ล่าสุด_user.docx')
for i in [58, 74, 75, 82, 85, 86, 90, 91, 140, 147]:
    p = doc.paragraphs[i]
    r = p.runs[0] if p.runs else None
    print(f"p{i}: text='{p.text}'")
    if r:
        print(f"   font={r.font.name}, size={r.font.size}, bold={r.bold}")


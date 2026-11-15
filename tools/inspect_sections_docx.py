import docx

doc = docx.Document('docs/รายงานพัฒนาระบบ_ล่าสุด_user.docx')
print(f"Total sections: {len(doc.sections)}")
for s_idx, sec in enumerate(doc.sections):
    h = sec.header
    f = sec.footer
    h_txt = "".join(p.text for p in h.paragraphs).strip()
    f_txt = "".join(p.text for p in f.paragraphs).strip()
    print(f"Section {s_idx}: header='{h_txt}', footer='{f_txt}'")


import docx

doc = docx.Document('docs/รายงานพัฒนาระบบ_ล่าสุด_user.docx')

# Let's inspect headings in Chapter 2, 3, 4, 5
headings_in_body = []
for p in doc.paragraphs[150:]: # from Chapter 1 onwards
    t = p.text.strip()
    if t.startswith(('1.', '2.', '3.', '4.', '5.', 'บทที่', 'เอกสาร', 'ประวัติ')):
        headings_in_body.append(t)

print("=== HEADINGS FOUND IN BODY ===")
for h in headings_in_body[:35]:
    print(f"- {h}")


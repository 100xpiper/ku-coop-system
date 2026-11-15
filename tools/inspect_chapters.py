# -*- coding: utf-8 -*-
import docx

doc = docx.Document('docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs.docx')

print("=== CHECKING CHAPTER 3, 4, 5 HEADINGS ===")
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if any(t.startswith(k) for k in ["บทที่", "3.", "4.", "5.", "เอกสาร", "บรรณานุกรม", "ประวัติ"]):
        print(f"[{i}] {t}")


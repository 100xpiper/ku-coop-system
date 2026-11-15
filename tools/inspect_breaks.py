import docx

doc = docx.Document('docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs_backup.docx')
for i in [57, 94, 139, 150]:
    p = doc.paragraphs[i]
    brs = p._element.xpath('.//w:br[@w:type="page"]')
    pb_before = p.paragraph_format.page_break_before
    print(f"p{i} ('{p.text[:20]}'): page_break_before={pb_before}, page_brs={len(brs)}")
    # Also check if previous paragraph had a page break
    p_prev = doc.paragraphs[i-1]
    brs_prev = p_prev._element.xpath('.//w:br[@w:type="page"]')
    print(f"   prev p{i-1} ('{p_prev.text[:20]}'): page_brs={len(brs_prev)}")


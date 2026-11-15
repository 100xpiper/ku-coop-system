import pymupdf

doc = pymupdf.open('docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs.pdf')

for p_num in [1, 17, 18, 19, 20, 21, 22, 23, 27, 28, 57, 58, 59, 60, 61, 64, 65, 66]:
    idx = p_num + 12 - 1 # 0-indexed physical page
    if idx < len(doc):
        txt = doc[idx].get_text().strip()
        lines = [line.strip() for line in txt.split('\n') if line.strip()][:4]
        print(f"--- Arabic Page {p_num} (Physical {idx+1}) ---")
        print(" | ".join(lines))


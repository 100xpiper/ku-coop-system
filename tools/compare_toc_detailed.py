import pymupdf
import re

doc = pymupdf.open('docs/รายงานพัฒนาระบบ_ล่าสุด_user.pdf')

# Offset: Physical Page 11 is Arabic Page 1 (11 - 10 = 1)
OFFSET = 10

def get_actual_page(pattern, start_p=10):
    for i in range(start_p, len(doc)):
        txt = doc[i].get_text()
        if re.search(pattern, txt):
            return i + 1 - OFFSET
    return None

# Parse TOC from docx
import docx
d = docx.Document('docs/รายงานพัฒนาระบบ_ล่าสุด_user.docx')

toc_lines = []
fig_lines = []
tbl_lines = []

mode = None
for p in d.paragraphs:
    t = p.text.strip()
    if t == 'สารบัญ':
        mode = 'TOC'
        continue
    elif t == 'สารบัญรูปภาพ':
        mode = 'FIG'
        continue
    elif t == 'สารบัญตาราง':
        mode = 'TBL'
        continue
    elif t.startswith('บทที่ 1') and mode == 'TBL':
        break
    
    if mode == 'TOC' and t:
        toc_lines.append(t)
    elif mode == 'FIG' and t:
        fig_lines.append(t)
    elif mode == 'TBL' and t:
        tbl_lines.append(t)

print(f"Parsed {len(toc_lines)} TOC lines, {len(fig_lines)} FIG lines, {len(tbl_lines)} TBL lines")

print("\n--- TOC COMPARISON ---")
for line in toc_lines:
    # parse title and page
    m = re.match(r'^(.*?)\s*\.{3,}\s*([^\s]+)$', line)
    if m:
        title = m.group(1).strip()
        stated_page = m.group(2).strip()
        print(f"Title: '{title}' | Stated: '{stated_page}'")


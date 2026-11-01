# -*- coding: utf-8 -*-
import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

sys_dir = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0, sys_dir)
from tor_helpers import set_cell_margins, set_table_borders

DOCS_DIR = os.path.abspath(os.path.join(sys_dir, "..", "docs"))
ARTIFACT_DIR = r"C:\Users\PER\.gemini\antigravity\brain\ddb60d44-47b2-4e84-bca5-28d119fdaf51"

FONT_NAME = "Angsana New"
BODY_SIZE_PT = 16

def set_run_font(run, font_name=FONT_NAME, size_pt=BODY_SIZE_PT, bold=None, italic=None, color_rgb=RGBColor(0, 0, 0)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color_rgb is not None:
        run.font.color.rgb = color_rgb

    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    rFonts.set(qn('w:eastAsia'), font_name)

    szCs = rPr.find(qn('w:szCs'))
    if szCs is None:
        szCs = OxmlElement('w:szCs')
        rPr.append(szCs)
    szCs.set(qn('w:val'), str(int(size_pt * 2)))

def format_inline_runs(paragraph, text, base_size=BODY_SIZE_PT):
    parts = re.split(r'(\*\*.*?\*\*|\*.*?\*|`.*?`)', text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            r = paragraph.add_run(part[2:-2])
            set_run_font(r, FONT_NAME, base_size, bold=True)
        elif part.startswith('*') and part.endswith('*'):
            r = paragraph.add_run(part[1:-1])
            set_run_font(r, FONT_NAME, base_size, italic=True)
        elif part.startswith('`') and part.endswith('`'):
            r = paragraph.add_run(part[1:-1])
            set_run_font(r, "Courier New", max(11, base_size - 3))
        else:
            r = paragraph.add_run(part)
            set_run_font(r, FONT_NAME, base_size)

# Update texts in md files
ts_path = os.path.join(DOCS_DIR, "Progress_Timesheet.md")
with open(ts_path, "r", encoding="utf-8") as f:
    ts_md = f.read()

ts_md = ts_md.replace("Form 01 - 11", "แบบฟอร์ม 00, Form 02, 04, 05, 06, 07, 08, 10, 11")
ts_md = ts_md.replace("Form 01-11", "แบบฟอร์ม 00, Form 02, 04, 05, 06, 07, 08, 10, 11")
ts_md = ts_md.replace("Form 0-11", "แบบฟอร์ม 00, Form 02, 04, 05, 06, 07, 08, 10, 11")
ts_md = ts_md.replace("อาจารย์ สมชาย แจ่มใส", "อาจารย์ปรวี วงศ์สวัสดิ์สุริยะ")

with open(ts_path, "w", encoding="utf-8") as f:
    f.write(ts_md)

print("Updated Progress_Timesheet.md")

# 1. BUILD DOCX FOR Progress_Timesheet
doc = docx.Document()

for sec in doc.sections:
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    sec.top_margin = Inches(0.8)
    sec.bottom_margin = Inches(0.8)
    sec.left_margin = Inches(0.8)
    sec.right_margin = Inches(0.8)

style = doc.styles['Normal']
style.font.name = FONT_NAME
style.font.size = Pt(BODY_SIZE_PT)
style.font.color.rgb = RGBColor(0, 0, 0)

# Set complex script fonts
rPr = style.element.get_or_add_rPr()
rFonts = rPr.find(qn('w:rFonts'))
if rFonts is None:
    rFonts = OxmlElement('w:rFonts')
    rPr.append(rFonts)
rFonts.set(qn('w:ascii'), FONT_NAME)
rFonts.set(qn('w:hAnsi'), FONT_NAME)
rFonts.set(qn('w:cs'), FONT_NAME)
rFonts.set(qn('w:eastAsia'), FONT_NAME)
szCs = rPr.find(qn('w:szCs'))
if szCs is None:
    szCs = OxmlElement('w:szCs')
    rPr.append(szCs)
szCs.set(qn('w:val'), str(int(BODY_SIZE_PT * 2)))

lines = ts_md.split('\n')
idx = 0

while idx < len(lines):
    line = lines[idx]
    trimmed = line.strip()

    if trimmed.startswith('# '):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(trimmed[2:].strip())
        set_run_font(r, FONT_NAME, 20, bold=True)
    elif trimmed.startswith('## '):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(8)
        r = p.add_run(trimmed[3:].strip())
        set_run_font(r, FONT_NAME, 17, bold=True)
    elif trimmed.startswith('|') and trimmed.endswith('|'):
        table_lines = []
        while idx < len(lines) and lines[idx].strip().startswith('|') and lines[idx].strip().endswith('|'):
            table_lines.append(lines[idx].strip())
            idx += 1

        if len(table_lines) >= 2:
            headers = [c.strip() for c in table_lines[0].strip('|').split('|')]
            rows = []
            for r_line in table_lines[2:]:
                cells = [c.strip() for c in r_line.strip('|').split('|')]
                rows.append(cells)

            col_count = len(headers)
            table = doc.add_table(rows=len(rows) + 1, cols=col_count)
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            table.autofit = False
            set_table_borders(table, color="000000", sz="4", val="single")

            # Column widths for 3 cols: [1.2 in, 2.8 in, 2.7 in]
            widths = [Inches(1.2), Inches(2.7), Inches(2.8)] if col_count == 3 else [Inches(6.7 / col_count)] * col_count

            hdr_cells = table.rows[0].cells
            for i, h in enumerate(headers):
                hdr_cells[i].text = ""
                hdr_cells[i].width = widths[i]
                p = hdr_cells[i].paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
                format_inline_runs(p, h.strip(), base_size=15)
                for run in p.runs:
                    set_run_font(run, FONT_NAME, 15, bold=True)
                set_cell_margins(hdr_cells[i], top=80, bottom=80, left=90, right=90)

            for r_idx, row_data in enumerate(rows):
                row_cells = table.rows[r_idx + 1].cells
                for c_idx in range(min(col_count, len(row_data))):
                    val = row_data[c_idx].strip()
                    row_cells[c_idx].text = ""
                    row_cells[c_idx].width = widths[c_idx]
                    p = row_cells[c_idx].paragraphs[0]
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    if c_idx == 0:
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    else:
                        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    format_inline_runs(p, val, base_size=14)
                    set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=90, right=90)

            p_post = doc.add_paragraph()
            p_post.paragraph_format.space_before = Pt(0)
            p_post.paragraph_format.space_after = Pt(4)
        continue
    elif trimmed:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        format_inline_runs(p, trimmed, base_size=16)

    idx += 1

docx_ts_path = os.path.join(DOCS_DIR, "Progress_Timesheet.docx")
doc.save(docx_ts_path)
print(f"Generated: {docx_ts_path}")

# 2. BUILD HTML FOR Progress_Timesheet
def md_inline_to_html(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    return text

html_body = []
idx = 0
while idx < len(lines):
    line = lines[idx]
    trimmed = line.strip()

    if trimmed.startswith('# '):
        html_body.append(f'<h1 style="text-align: center; margin-top: 18px; margin-bottom: 8px; font-size: 22pt;">{md_inline_to_html(trimmed[2:])}</h1>')
    elif trimmed.startswith('## '):
        html_body.append(f'<h2 style="text-align: center; margin-top: 6px; margin-bottom: 16px; font-size: 18pt;">{md_inline_to_html(trimmed[3:])}</h2>')
    elif trimmed.startswith('|') and trimmed.endswith('|'):
        table_lines = []
        while idx < len(lines) and lines[idx].strip().startswith('|') and lines[idx].strip().endswith('|'):
            table_lines.append(lines[idx].strip())
            idx += 1

        if len(table_lines) >= 2:
            headers = [c.strip() for c in table_lines[0].strip('|').split('|')]
            t_html = ['<table>', '<thead>', '<tr>']
            for h in headers:
                t_html.append(f'<th>{md_inline_to_html(h)}</th>')
            t_html.extend(['</tr>', '</thead>', '<tbody>'])

            for r_line in table_lines[2:]:
                cells = [c.strip() for c in r_line.strip('|').split('|')]
                t_html.append('<tr>')
                for c_idx, cell in enumerate(cells):
                    align = 'center' if c_idx == 0 else 'left'
                    t_html.append(f'<td align="{align}">{md_inline_to_html(cell)}</td>')
                t_html.append('</tr>')
            t_html.extend(['</tbody>', '</table>'])
            html_body.append('\n'.join(t_html))
        continue
    elif trimmed:
        html_body.append(f'<p style="margin: 4px 0 6px 0; font-size: 16pt;">{md_inline_to_html(trimmed)}</p>')

    idx += 1

html_full = f'''<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<title>รายงานการปฏิบัติงานประจำวัน (Daily Progress Timesheet Log)</title>
<style>
    body {{
        font-family: "Angsana New", "TH Sarabun New", "Sarabun", "Tahoma", sans-serif;
        font-size: 16pt;
        line-height: 1.25;
        color: #000000;
        background-color: #ffffff;
        margin: 0;
        padding: 20px;
    }}
    .document-container {{
        max-width: 900px;
        margin: 0 auto;
        background: #ffffff;
        padding: 30px 40px;
        font-family: "Angsana New", "TH Sarabun New", "Sarabun", "Tahoma", sans-serif;
    }}
    h1, h2, h3, h4 {{
        color: #000000;
        font-family: inherit;
        font-weight: bold;
    }}
    p, li, td, th {{
        font-size: 16pt;
        color: #000000;
        font-family: inherit;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 14px 0;
        font-size: 14.5pt;
        font-family: inherit;
    }}
    th, td {{
        border: 1px solid #000000;
        padding: 6px 10px;
        vertical-align: top;
        color: #000000;
    }}
    th {{
        background-color: #ffffff;
        font-weight: bold;
        text-align: center;
        font-size: 15.5pt;
    }}
    td {{
        font-size: 14pt;
    }}
    .action-bar {{
        position: sticky;
        top: 0;
        background: #ffffff;
        padding: 12px 0;
        border-bottom: 2px solid #000000;
        display: flex;
        justify-content: flex-end;
        gap: 10px;
        margin-bottom: 25px;
        z-index: 100;
    }}
    .btn {{
        background: #000000;
        color: #ffffff;
        border: 1px solid #000000;
        padding: 9px 16px;
        font-size: 13.5px;
        font-weight: bold;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        font-family: sans-serif;
    }}
    .btn:hover {{
        background: #333333;
    }}
    @media print {{
        .action-bar {{ display: none; }}
        body {{ padding: 0; }}
        .document-container {{ padding: 0; }}
    }}
</style>
</head>
<body>

<div class="document-container" id="timesheet-content">
    <div class="action-bar">
        <button class="btn" onclick="copyTimesheet()">คัดลอกตารางทั้งหมด (สำหรับวางใน Google Docs)</button>
        <button class="btn" onclick="window.print()">สั่งพิมพ์ / บันทึกเป็น PDF</button>
        <a href="Progress_Timesheet.docx" class="btn" download>ดาวน์โหลด Word (.docx)</a>
    </div>

    {'\\n'.join(html_body)}
</div>

<script>
function copyTimesheet() {{
    const el = document.getElementById('timesheet-content');
    const range = document.createRange();
    range.selectNode(el);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    try {{
        document.execCommand('copy');
        alert('คัดลอกตาราง Time Sheet เรียบร้อย นำไปกดวาง (Ctrl+V) ใน Google Docs ได้ทันที');
    }} catch (err) {{
        alert('กรุณากด Ctrl+A และ Ctrl+C เพื่อคัดลอกด้วยตนเอง');
    }}
    window.getSelection().removeAllRanges();
}}
</script>

</body>
</html>
'''

html_ts_path = os.path.join(DOCS_DIR, "Progress_Timesheet.html")
with open(html_ts_path, "w", encoding="utf-8") as f:
    f.write(html_full)
print(f"Generated: {html_ts_path}")

# Sync to brain artifact
if os.path.exists(ARTIFACT_DIR):
    import shutil
    for path in [ts_path, docx_ts_path, html_ts_path]:
        shutil.copy2(path, os.path.join(ARTIFACT_DIR, os.path.basename(path)))
    print("Synced timesheet files to brain artifact directory")

print("Timesheet docs generation completed successfully!")

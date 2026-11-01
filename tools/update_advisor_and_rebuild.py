# -*- coding: utf-8 -*-
import os
import re
import sys
import shutil
import base64
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tor_helpers import set_cell_margins, set_table_borders

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
DOCS_SCREENSHOTS_DIR = os.path.join(DOCS_DIR, "screenshots")
ARTIFACT_DIR = r"C:\Users\PER\.gemini\antigravity\brain\ddb60d44-47b2-4e84-bca5-28d119fdaf51"

MD_PATH = os.path.join(DOCS_DIR, "Project_Progress_Report_Final.md")
DOCX_PATH = os.path.join(DOCS_DIR, "Project_Progress_Report_Final.docx")
HTML_PATH = os.path.join(DOCS_DIR, "Project_Progress_Report_Final.html")

NEW_ADVISOR_NAME = "อาจารย์ปรวี วงศ์สวัสดิ์สุริยะ"
FONT_NAME = "Angsana New"
BODY_SIZE_PT = 16

# -----------------------------------------------------------------------------
# 1. READ CLEAN MARKDOWN
# -----------------------------------------------------------------------------
print(f"Reading: {MD_PATH}")
with open(MD_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Replace advisor name
content = re.sub(r'อาจารย์\s*สมชาย(?:\s*แจ่มใส|\s*ใจดี)?', NEW_ADVISOR_NAME, content)
content = re.sub(r'สมชาย\s*(?:แจ่มใส|ใจดี)', NEW_ADVISOR_NAME, content)

# Remove all horizontal divider lines (---)
clean_md = re.sub(r'^\s*---+\s*$', '', content, flags=re.MULTILINE)
clean_md = re.sub(r'\n{3,}', '\n\n', clean_md)

with open(MD_PATH, "w", encoding="utf-8") as f:
    f.write(clean_md)

print("Updated Project_Progress_Report_Final.md!")

# -----------------------------------------------------------------------------
# 2. GENERATE CLEAN Project_Progress_Report_Final.docx (Angsana New 16pt)
# -----------------------------------------------------------------------------
print(f"Building docx document using font '{FONT_NAME}', size {BODY_SIZE_PT}pt...")
doc = docx.Document()

for sec in doc.sections:
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    sec.top_margin = Inches(1.0)
    sec.bottom_margin = Inches(1.0)
    sec.left_margin = Inches(1.0)
    sec.right_margin = Inches(1.0)

style = doc.styles['Normal']
style.font.name = FONT_NAME
style.font.size = Pt(BODY_SIZE_PT)
style.font.color.rgb = RGBColor(0, 0, 0)

# Set complex script fonts in Normal style
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

def add_clean_paragraph(doc, text="", bold=False, italic=False, size_pt=BODY_SIZE_PT, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=6):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if text:
        run = p.add_run(text)
        set_run_font(run, FONT_NAME, size_pt, bold=bold, italic=italic)
    return p

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

def add_clean_table(doc, headers, rows):
    col_count = len(headers)
    table = doc.add_table(rows=len(rows) + 1, cols=col_count)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    set_table_borders(table, color="000000", sz="4", val="single")

    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = ""
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        format_inline_runs(p, h.strip(), base_size=15)
        for run in p.runs:
            set_run_font(run, FONT_NAME, 15, bold=True)
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=100, right=100)

    for r_idx, row_data in enumerate(rows):
        row_cells = table.rows[r_idx + 1].cells
        for c_idx in range(min(col_count, len(row_data))):
            val = row_data[c_idx].strip()
            row_cells[c_idx].text = ""
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            if c_idx == 0 and len(val) <= 15:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            format_inline_runs(p, val, base_size=14.5)
            set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=100, right=100)

    p_post = doc.add_paragraph()
    p_post.paragraph_format.space_before = Pt(0)
    p_post.paragraph_format.space_after = Pt(6)

lines = clean_md.split('\n')
idx = 0
in_code = False
code_lines = []

while idx < len(lines):
    line = lines[idx]
    trimmed = line.strip()

    if trimmed.startswith('```'):
        if not in_code:
            in_code = True
            code_lines = []
        else:
            in_code = False
            for c_line in code_lines:
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Inches(0.4)
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                run = p.add_run(c_line)
                set_run_font(run, "Courier New", 12)
            code_lines = []
        idx += 1
        continue

    if in_code:
        code_lines.append(line)
        idx += 1
        continue

    if trimmed.startswith('|') and trimmed.endswith('|'):
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
            add_clean_table(doc, headers, rows)
        continue

    img_match = re.match(r'!\[(.*?)\]\((.*?)\)', trimmed)
    if img_match:
        caption = img_match.group(1)
        rel_img_path = img_match.group(2).replace('\\', '/')
        img_basename = os.path.basename(rel_img_path)
        img_file = os.path.join(SCREENSHOTS_DIR, img_basename)
        if not os.path.exists(img_file):
            img_file = os.path.join(DOCS_SCREENSHOTS_DIR, img_basename)

        if os.path.exists(img_file):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.add_run().add_picture(img_file, width=Inches(5.9))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(10)
            run_cap = p_cap.add_run(caption)
            set_run_font(run_cap, FONT_NAME, 14, italic=True)
        idx += 1
        continue

    if trimmed.startswith('# '):
        add_clean_paragraph(doc, trimmed[2:].strip(), bold=True, size_pt=22, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=14, space_after=8)
    elif trimmed.startswith('## '):
        add_clean_paragraph(doc, trimmed[3:].strip(), bold=True, size_pt=18, space_before=12, space_after=6)
    elif trimmed.startswith('### '):
        add_clean_paragraph(doc, trimmed[4:].strip(), bold=True, size_pt=16, space_before=8, space_after=4)
    elif trimmed.startswith('#### '):
        add_clean_paragraph(doc, trimmed[5:].strip(), bold=True, size_pt=16, space_before=6, space_after=2)
    elif trimmed.startswith('- ') or trimmed.startswith('* '):
        bullet_text = trimmed[2:].strip()
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        r_bullet = p.add_run("•  ")
        set_run_font(r_bullet, FONT_NAME, BODY_SIZE_PT)
        format_inline_runs(p, bullet_text, base_size=BODY_SIZE_PT)
    elif re.match(r'^\d+\.\s', trimmed):
        m = re.match(r'^(\d+\.\s)(.*)', trimmed)
        prefix = m.group(1)
        body = m.group(2)
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        r_num = p.add_run(prefix)
        set_run_font(r_num, FONT_NAME, BODY_SIZE_PT, bold=True)
        format_inline_runs(p, body, base_size=BODY_SIZE_PT)
    elif trimmed:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        format_inline_runs(p, trimmed, base_size=BODY_SIZE_PT)

    idx += 1

alt_docx = os.path.join(DOCS_DIR, "Project_Progress_Report_Final_Latest.docx")
doc.save(alt_docx)
print(f"Generated: {alt_docx}")

try:
    doc.save(DOCX_PATH)
    print(f"Generated: {DOCX_PATH}")
except PermissionError:
    print(f"Notice: {DOCX_PATH} is locked by Microsoft Word.")


# -----------------------------------------------------------------------------
# 3. GENERATE CLEAN Project_Progress_Report_Final.html (Angsana New 16pt)
# -----------------------------------------------------------------------------
print("Building HTML document with Angsana New 16pt...")

def md_inline_to_html(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    return text

def get_base64_img(img_rel_path):
    img_basename = os.path.basename(img_rel_path.replace('\\', '/'))
    full_path = os.path.join(SCREENSHOTS_DIR, img_basename)
    if not os.path.exists(full_path):
        full_path = os.path.join(DOCS_SCREENSHOTS_DIR, img_basename)
    if os.path.exists(full_path):
        with open(full_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:image/png;base64,{encoded_string}"
    return img_rel_path

html_body = []
idx = 0
in_code = False
code_lines = []

while idx < len(lines):
    line = lines[idx]
    trimmed = line.strip()

    if trimmed.startswith('```'):
        if not in_code:
            in_code = True
            code_lines = []
        else:
            in_code = False
            code_text = '\n'.join(code_lines)
            html_body.append(f'<pre><code>{code_text}</code></pre>')
            code_lines = []
        idx += 1
        continue

    if in_code:
        code_lines.append(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
        idx += 1
        continue

    if trimmed.startswith('|') and trimmed.endswith('|'):
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
                    align = 'center' if c_idx == 0 and len(cell) <= 15 else 'left'
                    t_html.append(f'<td align="{align}">{md_inline_to_html(cell)}</td>')
                t_html.append('</tr>')
            t_html.extend(['</tbody>', '</table>'])
            html_body.append('\n'.join(t_html))
        continue

    img_match = re.match(r'!\[(.*?)\]\((.*?)\)', trimmed)
    if img_match:
        caption = img_match.group(1)
        rel_img_path = img_match.group(2)
        b64_src = get_base64_img(rel_img_path)
        fig_html = f'''<figure style="text-align: center; margin: 18px 0;">
  <img src="{b64_src}" alt="{caption}" style="max-width: 100%; border: 1px solid #000000;" />
  <figcaption style="font-family: 'Angsana New', 'Sarabun', sans-serif; font-size: 14pt; font-style: italic; margin-top: 6px; color: #000000;">{caption}</figcaption>
</figure>'''
        html_body.append(fig_html)
        idx += 1
        continue

    if trimmed.startswith('# '):
        html_body.append(f'<h1 style="text-align: center; margin-top: 24px; margin-bottom: 12px; font-size: 22pt;">{md_inline_to_html(trimmed[2:])}</h1>')
    elif trimmed.startswith('## '):
        html_body.append(f'<h2 style="margin-top: 20px; margin-bottom: 10px; font-size: 18pt;">{md_inline_to_html(trimmed[3:])}</h2>')
    elif trimmed.startswith('### '):
        html_body.append(f'<h3 style="margin-top: 16px; margin-bottom: 8px; font-size: 16pt;">{md_inline_to_html(trimmed[4:])}</h3>')
    elif trimmed.startswith('#### '):
        html_body.append(f'<h4 style="margin-top: 14px; margin-bottom: 6px; font-size: 16pt;">{md_inline_to_html(trimmed[5:])}</h4>')
    elif trimmed.startswith('- ') or trimmed.startswith('* '):
        html_body.append(f'<p style="margin: 3px 0 3px 25px; text-indent: -15px; font-size: 16pt;">• &nbsp; {md_inline_to_html(trimmed[2:])}</p>')
    elif re.match(r'^\d+\.\s', trimmed):
        m = re.match(r'^(\d+\.\s)(.*)', trimmed)
        html_body.append(f'<p style="margin: 3px 0 3px 25px; text-indent: -15px; font-size: 16pt;"><strong>{m.group(1)}</strong>{md_inline_to_html(m.group(2))}</p>')
    elif trimmed:
        html_body.append(f'<p style="margin: 4px 0 6px 0; text-align: justify; font-size: 16pt;">{md_inline_to_html(trimmed)}</p>')

    idx += 1

full_html = f'''<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<title>รายงานความก้าวหน้าโครงการฉบับสมบูรณ์ (KU Coop)</title>
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
        max-width: 850px;
        margin: 0 auto;
        background: #ffffff;
        padding: 40px 50px;
        font-family: "Angsana New", "TH Sarabun New", "Sarabun", "Tahoma", sans-serif;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: #000000;
        font-family: "Angsana New", "TH Sarabun New", "Sarabun", "Tahoma", sans-serif;
        font-weight: bold;
    }}
    h1 {{ font-size: 22pt; }}
    h2 {{ font-size: 18pt; }}
    h3 {{ font-size: 16pt; }}
    h4 {{ font-size: 16pt; }}
    p, li, td, th {{
        font-size: 16pt;
        color: #000000;
        font-family: "Angsana New", "TH Sarabun New", "Sarabun", "Tahoma", sans-serif;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 14px 0;
        font-size: 15pt;
        font-family: "Angsana New", "TH Sarabun New", "Sarabun", "Tahoma", sans-serif;
    }}
    th, td {{
        border: 1px solid #000000;
        padding: 6px 10px;
        vertical-align: top;
        color: #000000;
        font-family: "Angsana New", "TH Sarabun New", "Sarabun", "Tahoma", sans-serif;
    }}
    th {{
        background-color: #ffffff;
        font-weight: bold;
        text-align: center;
        font-size: 15.5pt;
    }}
    td {{
        font-size: 15pt;
    }}
    pre, code {{
        font-family: "Courier New", Courier, monospace;
        font-size: 12.5pt;
        color: #000000;
        background: #ffffff;
    }}
    pre {{
        border: 1px solid #000000;
        padding: 10px;
        white-space: pre-wrap;
        word-wrap: break-word;
        margin: 10px 0;
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

<div class="document-container" id="report-content">
    <div class="action-bar">
        <button class="btn" onclick="copyAllReport()">คัดลอกเนื้อหาทั้งหมด (สำหรับวางใน Google Docs)</button>
        <button class="btn" onclick="window.print()">สั่งพิมพ์ / บันทึกเป็น PDF</button>
        <a href="Project_Progress_Report_Final.docx" class="btn" download>ดาวน์โหลด Word (.docx)</a>
    </div>

    {'\\n'.join(html_body)}
</div>

<script>
function copyAllReport() {{
    const el = document.getElementById('report-content');
    const range = document.createRange();
    range.selectNode(el);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    try {{
        document.execCommand('copy');
        alert('คัดลอกรายงานเรียบร้อย สามารถนำไปกดวาง (Ctrl+V) ใน Google Docs ได้ทันทีครับ');
    }} catch (err) {{
        alert('กรุณากด Ctrl+A และ Ctrl+C เพื่อคัดลอกด้วยตนเอง');
    }}
    window.getSelection().removeAllRanges();
}}
</script>

</body>
</html>
'''

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(full_html)
print(f"Generated: {HTML_PATH}")

# -----------------------------------------------------------------------------
# 4. SYNC TO BRAIN ARTIFACT DIRECTORY
# -----------------------------------------------------------------------------
if os.path.exists(ARTIFACT_DIR):
    for f in [MD_PATH, DOCX_PATH, alt_docx, HTML_PATH]:
        dest = os.path.join(ARTIFACT_DIR, os.path.basename(f))
        shutil.copy2(f, dest)
        print(f"Synced to artifact: {dest}")

print("\nALL TASKS COMPLETED SUCCESSFULLY!")

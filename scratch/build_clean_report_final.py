# -*- coding: utf-8 -*-
import os
import re
import base64
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from tor_helpers import set_cell_margins, set_table_borders

# -----------------------------------------------------------------------------
# 1. READ AND UPDATE Project_Progress_Report_Final.md
# -----------------------------------------------------------------------------

with open("Project_Progress_Report_Final.md", "r", encoding="utf-8") as f:
    content = f.read()

# Remove all horizontal divider lines (---)
clean_md = re.sub(r'^\s*---+\s*$', '', content, flags=re.MULTILINE)

# Ensure no multi consecutive blank lines
clean_md = re.sub(r'\n{3,}', '\n\n', clean_md)

# Save updated Project_Progress_Report_Final.md
with open("Project_Progress_Report_Final.md", "w", encoding="utf-8") as f:
    f.write(clean_md)

print("Updated Project_Progress_Report_Final.md without divider lines successfully!")

# -----------------------------------------------------------------------------
# 2. GENERATE CLEAN Project_Progress_Report_Final.docx
# -----------------------------------------------------------------------------

doc = docx.Document()

# Page setup: A4, 1 inch margins
for sec in doc.sections:
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    sec.top_margin = Inches(1.0)
    sec.bottom_margin = Inches(1.0)
    sec.left_margin = Inches(1.0)
    sec.right_margin = Inches(1.0)

# Base style: TH Sarabun New, 15pt, 100% black text, no colors
style = doc.styles['Normal']
style.font.name = 'TH Sarabun New'
style.font.size = Pt(15)
style.font.color.rgb = RGBColor(0, 0, 0)
style.paragraph_format.line_spacing = 1.15
style.paragraph_format.space_after = Pt(4)

def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(18)
    run.font.color.rgb = RGBColor(0, 0, 0)
    p.paragraph_format.space_after = Pt(4)

def add_subtitle(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(0, 0, 0)
    p.paragraph_format.space_after = Pt(4)

def add_h1(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(0, 0, 0)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)

def add_h2(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(15)
    run.font.color.rgb = RGBColor(0, 0, 0)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)

def add_h3(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0, 0, 0)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)

def add_p(text, indent=False, bold=False):
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.left_indent = Inches(0.3)
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0, 0, 0)
    p.paragraph_format.space_after = Pt(4)
    return p

# Parse Markdown lines into docx
lines = clean_md.split('\n')
i = 0
in_table = False
table_lines = []

while i < len(lines):
    line = lines[i].strip()
    
    # Table parsing
    if line.startswith('|') and line.endswith('|'):
        table_lines = []
        while i < len(lines) and lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
            table_lines.append(lines[i].strip())
            i += 1
            
        # Parse table_lines
        parsed_rows = []
        for tl in table_lines:
            if re.match(r'^\|[\s\-:|]+\|$', tl):
                continue
            cells = [c.strip() for c in tl.strip('|').split('|')]
            parsed_rows.append(cells)
            
        if parsed_rows:
            cols_count = max(len(r) for r in parsed_rows)
            tbl = doc.add_table(rows=len(parsed_rows), cols=cols_count)
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            set_table_borders(tbl, color="000000")
            
            for r_idx, row_data in enumerate(parsed_rows):
                for c_idx, cell_value in enumerate(row_data):
                    if c_idx < cols_count:
                        c = tbl.rows[r_idx].cells[c_idx]
                        clean_val = cell_value.replace('**', '').replace('☑', '☑ ').strip()
                        c.text = clean_val
                        p_cell = c.paragraphs[0]
                        p_cell.paragraph_format.space_after = Pt(2)
                        p_cell.paragraph_format.space_before = Pt(2)
                        for run in p_cell.runs:
                            run.font.size = Pt(12)
                            run.font.color.rgb = RGBColor(0, 0, 0)
                            if r_idx == 0 or '**' in cell_value:
                                run.bold = True
                        set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            doc.add_paragraph().paragraph_format.space_after = Pt(6)
        continue

    # Code block skipping or monospace
    if line.startswith('```'):
        i += 1
        code_block = []
        while i < len(lines) and not lines[i].strip().startswith('```'):
            code_block.append(lines[i])
            i += 1
        i += 1
        p_code = doc.add_paragraph()
        p_code.paragraph_format.left_indent = Inches(0.3)
        run_code = p_code.add_run('\n'.join(code_block))
        run_code.font.name = 'Consolas'
        run_code.font.size = Pt(11)
        run_code.font.color.rgb = RGBColor(0, 0, 0)
        continue

    # Image line: ![alt](path)
    img_m = re.match(r'^!\[(.*?)\]\((.*?)\)', line)
    if img_m:
        alt = img_m.group(1)
        src = img_m.group(2)
        if os.path.exists(src):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(2)
            run_img = p_img.add_run()
            run_img.add_picture(src, width=Inches(5.8))
        i += 1
        continue

    # Caption line: *ภาพที่ ...*
    cap_m = re.match(r'^\*(ภาพที่.*?)\*$', line)
    if cap_m:
        cap_text = cap_m.group(1)
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_cap = p_cap.add_run(cap_text)
        run_cap.italic = True
        run_cap.font.size = Pt(12.5)
        run_cap.font.color.rgb = RGBColor(0, 0, 0)
        p_cap.paragraph_format.space_after = Pt(10)
        i += 1
        continue

    # Headings
    if line.startswith('# '):
        add_title(line[2:].replace('**', ''))
    elif line.startswith('## '):
        add_h1(line[3:].replace('**', ''))
    elif line.startswith('### '):
        add_h2(line[4:].replace('**', ''))
    elif line.startswith('#### '):
        add_h3(line[5:].replace('**', ''))
    elif line.startswith('- ') or line.startswith('* '):
        clean_text = line[2:].replace('**', '')
        add_p(f"• {clean_text}", indent=True)
    elif re.match(r'^\d+\.\s+', line):
        clean_text = re.sub(r'^\d+\.\s+', '', line).replace('**', '')
        match_num = re.match(r'^(\d+\.)\s+', line).group(1)
        add_p(f"{match_num} {clean_text}", indent=True)
    elif line:
        clean_text = line.replace('**', '')
        add_p(clean_text)
        
    i += 1

doc.save("Project_Progress_Report_Final.docx")
print("Project_Progress_Report_Final.docx generated successfully!")

# -----------------------------------------------------------------------------
# 3. GENERATE CLEAN Project_Progress_Report_Final.html (PLAIN BLACK, NO DECORATIONS, NO LINES)
# -----------------------------------------------------------------------------

def img_to_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            b64 = base64.b64encode(img_file.read()).decode('utf-8')
            return f"data:image/png;base64,{b64}"
    return None

html_body = []
lines = clean_md.split('\n')
i = 0

while i < len(lines):
    line = lines[i].strip()
    
    # Table parsing
    if line.startswith('|') and line.endswith('|'):
        t_lines = []
        while i < len(lines) and lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
            t_lines.append(lines[i].strip())
            i += 1
            
        rows_data = []
        for tl in t_lines:
            if re.match(r'^\|[\s\-:|]+\|$', tl):
                continue
            cells = [c.strip() for c in tl.strip('|').split('|')]
            rows_data.append(cells)
            
        if rows_data:
            tbl_html = ['<div style="overflow-x: auto; margin: 16px 0;"><table style="width: 100%; border-collapse: collapse; font-size: 14px; border: 1px solid #000000; color: #000000;">']
            for r_idx, r in enumerate(rows_data):
                tag = 'th' if r_idx == 0 else 'td'
                bg = ' style="background-color: #f5f5f5; border: 1px solid #000000; padding: 8px 10px; text-align: left; font-weight: bold; color: #000000;"' if r_idx == 0 else ' style="border: 1px solid #000000; padding: 8px 10px; color: #000000;"'
                row_str = '<tr>'
                for c in r:
                    clean_c = c.replace('**', '')
                    row_str += f'<{tag}{bg}>{clean_c}</{tag}>'
                row_str += '</tr>'
                tbl_html.append(row_str)
            tbl_html.append('</table></div>')
            html_body.append('\n'.join(tbl_html))
        continue

    # Code block
    if line.startswith('```'):
        i += 1
        code_block = []
        while i < len(lines) and not lines[i].strip().startswith('```'):
            code_block.append(lines[i].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
            i += 1
        i += 1
        html_body.append(f'<pre style="background: #fafafa; border: 1px solid #000000; padding: 12px; font-family: monospace; font-size: 13px; color: #000000; overflow-x: auto; margin: 14px 0;"><code>{"<br/>".join(code_block)}</code></pre>')
        continue

    # Image
    img_m = re.match(r'^!\[(.*?)\]\((.*?)\)', line)
    if img_m:
        alt = img_m.group(1)
        src = img_m.group(2)
        b64 = img_to_base64(src)
        if b64:
            html_body.append(f'<div style="text-align: center; margin: 20px 0;"><img src="{b64}" alt="{alt}" style="max-width: 95%; height: auto; border: 1px solid #000000;" /></div>')
        i += 1
        continue

    # Caption
    cap_m = re.match(r'^\*(ภาพที่.*?)\*$', line)
    if cap_m:
        cap_text = cap_m.group(1)
        html_body.append(f'<div style="text-align: center; font-size: 13px; font-style: italic; color: #000000; margin-top: -12px; margin-bottom: 22px;">{cap_text}</div>')
        i += 1
        continue

    # Headings
    if line.startswith('# '):
        html_body.append(f'<h1 style="text-align: center; font-size: 24px; color: #000000; margin: 20px 0 8px 0; font-weight: bold;">{line[2:].replace("**", "")}</h1>')
    elif line.startswith('## '):
        html_body.append(f'<h2 style="font-size: 20px; color: #000000; margin: 28px 0 10px 0; font-weight: bold;">{line[3:].replace("**", "")}</h2>')
    elif line.startswith('### '):
        html_body.append(f'<h3 style="font-size: 17px; color: #000000; margin: 20px 0 8px 0; font-weight: bold;">{line[4:].replace("**", "")}</h3>')
    elif line.startswith('#### '):
        html_body.append(f'<h4 style="font-size: 15px; color: #000000; margin: 16px 0 6px 0; font-weight: bold;">{line[5:].replace("**", "")}</h4>')
    elif line.startswith('- ') or line.startswith('* '):
        html_body.append(f'<p style="margin: 4px 0 4px 24px; font-size: 14.5px; color: #000000;">• {line[2:].replace("**", "")}</p>')
    elif re.match(r'^\d+\.\s+', line):
        html_body.append(f'<p style="margin: 4px 0 4px 24px; font-size: 14.5px; color: #000000;">{line.replace("**", "")}</p>')
    elif line:
        html_body.append(f'<p style="margin: 6px 0; font-size: 14.5px; line-height: 1.6; color: #000000; text-align: justify;">{line.replace("**", "")}</p>')
        
    i += 1

full_html = f'''<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="utf-8">
<title>รายงานความก้าวหน้าโครงงานฉบับสมบูรณ์ (เล่มจบ) - มหาวิทยาลัยเกษตรศาสตร์</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap');
    body {{
        font-family: 'Sarabun', 'TH Sarabun New', Tahoma, sans-serif;
        line-height: 1.6;
        color: #000000;
        background-color: #ffffff;
        margin: 0;
        padding: 40px 20px;
    }}
    .document-container {{
        max-width: 920px;
        margin: 0 auto;
        background: #ffffff;
        padding: 40px 50px;
        color: #000000;
    }}
    .action-bar {{
        position: sticky;
        top: 15px;
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
        <a href="Project_Progress_Report_Final.docx" class="btn" download>ดาวน์โหลดไฟล์ Word (.docx)</a>
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
        alert('คัดลอกเนื้อหารายงานเล่มจบทั้งหมดเรียบร้อยแล้ว สามารถนำไปกดวาง (Ctrl+V) ใน Google Docs ได้ทันทีครับ');
    }} catch (err) {{
        alert('กรุณากด Ctrl+A และ Ctrl+C เพื่อคัดลอกด้วยตนเอง');
    }}
    window.getSelection().removeAllRanges();
}}
</script>

</body>
</html>
'''

with open("Project_Progress_Report_Final.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("Project_Progress_Report_Final.html created successfully!")

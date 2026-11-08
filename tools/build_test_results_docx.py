# -*- coding: utf-8 -*-
import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

base_dir = r"c:\Users\PER\Downloads\Project"
docs_dir = os.path.join(base_dir, "docs")
screenshots_dir = os.path.join(base_dir, "screenshots")
md_path = os.path.join(docs_dir, "Test_Results_and_Evaluation.md")

with open(md_path, "r", encoding="utf-8") as f:
    md_content = f.read()

doc = docx.Document()

for sec in doc.sections:
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    sec.top_margin = Inches(1.0)
    sec.bottom_margin = Inches(1.0)
    sec.left_margin = Inches(1.0)
    sec.right_margin = Inches(1.0)

style = doc.styles['Normal']
style.font.name = 'Angsana New'
style.font.size = Pt(16)
style.font.color.rgb = RGBColor(0, 0, 0)
style.paragraph_format.line_spacing = 1.15
style.paragraph_format.space_after = Pt(4)

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'  <w:left w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def format_cell(cell, text, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.bold = bold
    run.font.name = 'Angsana New'
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0, 0, 0)

lines = md_content.split('\n')
idx = 0

while idx < len(lines):
    line = lines[idx]
    trimmed = line.strip()

    if not trimmed or trimmed == '---':
        idx += 1
        continue

    # Heading 1
    if trimmed.startswith('# '):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(trimmed[2:].strip())
        r.bold = True
        r.font.name = 'Angsana New'
        r.font.size = Pt(20)
        r.font.color.rgb = RGBColor(0, 0, 0)
    # Heading 2
    elif trimmed.startswith('## '):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(trimmed[3:].strip())
        r.bold = True
        r.font.name = 'Angsana New'
        r.font.size = Pt(18)
        r.font.color.rgb = RGBColor(0, 0, 0)
    # Heading 3
    elif trimmed.startswith('### '):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(trimmed[4:].strip())
        r.bold = True
        r.font.name = 'Angsana New'
        r.font.size = Pt(16)
        r.font.color.rgb = RGBColor(0, 0, 0)
    # Heading 4
    elif trimmed.startswith('#### '):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(trimmed[5:].strip())
        r.bold = True
        r.font.name = 'Angsana New'
        r.font.size = Pt(15)
        r.font.color.rgb = RGBColor(0, 0, 0)
    # Image
    elif trimmed.startswith('![') and '](' in trimmed:
        m = re.search(r'!\[(.*?)\]\((.*?)\)', trimmed)
        if m:
            raw_path = m.group(2)
            fname = os.path.basename(raw_path.replace('\\', '/'))
            img_path = os.path.join(screenshots_dir, fname)
            if not os.path.exists(img_path):
                img_path = os.path.join(screenshots_dir, "steps", fname)
            if os.path.exists(img_path):
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(6)
                p_img.paragraph_format.space_after = Pt(2)
                r_img = p_img.add_run()
                r_img.add_picture(img_path, width=Inches(5.5))
    # Image caption
    elif trimmed.startswith('*ภาพที่') and trimmed.endswith('*'):
        cap_text = trimmed[1:-1].strip()
        # Clean any markdown links in caption
        cap_text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', cap_text)
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(8)
        r_cap = p_cap.add_run(cap_text)
        r_cap.italic = True
        r_cap.font.name = 'Angsana New'
        r_cap.font.size = Pt(14)
        r_cap.font.color.rgb = RGBColor(0, 0, 0)
    # Table
    elif trimmed.startswith('|') and trimmed.endswith('|'):
        t_lines = []
        while idx < len(lines) and lines[idx].strip().startswith('|') and lines[idx].strip().endswith('|'):
            t_lines.append(lines[idx].strip())
            idx += 1

        if len(t_lines) >= 2:
            headers = [c.strip() for c in t_lines[0].strip('|').split('|')]
            rows = []
            for r_line in t_lines[2:]:
                cells = [c.strip() for c in r_line.strip('|').split('|')]
                rows.append(cells)

            table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            set_table_borders(table)

            for i, h in enumerate(headers):
                h_clean = re.sub(r'\*\*(.*?)\*\*', r'\1', h)
                format_cell(table.rows[0].cells[i], h_clean, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

            for r_i, row in enumerate(rows):
                for c_i in range(min(len(headers), len(row))):
                    val_clean = re.sub(r'\*\*(.*?)\*\*', r'\1', row[c_i])
                    val_clean = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', val_clean)
                    align = WD_ALIGN_PARAGRAPH.CENTER if c_i == 0 or len(val_clean) < 8 else WD_ALIGN_PARAGRAPH.LEFT
                    format_cell(table.rows[r_i + 1].cells[c_i], val_clean, align=align)

            p_space = doc.add_paragraph()
            p_space.paragraph_format.space_before = Pt(0)
            p_space.paragraph_format.space_after = Pt(4)
        continue
    # Regular paragraph
    else:
        clean_p = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', trimmed)
        is_list = clean_p.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '- '))
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        if is_list:
            p.paragraph_format.left_indent = Inches(0.3)
        parts = re.split(r'(\*\*.*?\*\*)', clean_p)
        for part in parts:
            if not part:
                continue
            if part.startswith('**') and part.endswith('**'):
                r = p.add_run(part[2:-2])
                r.bold = True
                r.font.name = 'Angsana New'
                r.font.size = Pt(16)
                r.font.color.rgb = RGBColor(0, 0, 0)
            else:
                r = p.add_run(part)
                r.font.name = 'Angsana New'
                r.font.size = Pt(16)
                r.font.color.rgb = RGBColor(0, 0, 0)

    idx += 1

out_docx = os.path.join(docs_dir, "บันทึกผลการทำงานและผลการทดลองใช้งานระบบ.docx")
doc.save(out_docx)
print(f"Generated: {out_docx} ({os.path.getsize(out_docx):,} bytes)")


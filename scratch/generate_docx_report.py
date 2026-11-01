# -*- coding: utf-8 -*-
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import re
import os

doc = Document()

# Set standard margins (1 inch = 2.54 cm all around)
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Set base style font to TH Sarabun New / Sarabun / Angsana New
style = doc.styles['Normal']
font = style.font
font.name = 'TH Sarabun New'
font.size = Pt(16)
font.color.rgb = RGBColor(0, 0, 0) # Plain black, no decoration

with open('Project_Progress_Report_Final.md', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
in_table = False
table_rows = []

img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

def format_inlines(paragraph, text_content):
    # Split text by bold markers **text**
    parts = re.split(r'(\*\*[^*]+\*\*)', text_content)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
            run.font.name = 'TH Sarabun New'
            run.font.color.rgb = RGBColor(0, 0, 0)
        else:
            # check italic *text*
            subparts = re.split(r'(\*[^*]+\*)', part)
            for subpart in subparts:
                if subpart.startswith('*') and subpart.endswith('*'):
                    run = paragraph.add_run(subpart[1:-1])
                    run.italic = True
                    run.font.name = 'TH Sarabun New'
                    run.font.color.rgb = RGBColor(0, 0, 0)
                else:
                    run = paragraph.add_run(subpart)
                    run.font.name = 'TH Sarabun New'
                    run.font.color.rgb = RGBColor(0, 0, 0)

for line in lines:
    line_s = line.strip()

    # Table line
    if line_s.startswith('|') and line_s.endswith('|'):
        if not in_table:
            in_table = True
            table_rows = []
        if re.match(r'^\|[\s\-:|]+\|$', line_s):
            continue
        cells = [c.strip() for c in line_s.strip('|').split('|')]
        table_rows.append(cells)
        continue
    else:
        if in_table:
            # Flush table
            if table_rows:
                num_cols = max(len(r) for r in table_rows)
                t = doc.add_table(rows=len(table_rows), cols=num_cols)
                t.style = 'Table Grid'
                t.alignment = WD_TABLE_ALIGNMENT.CENTER
                for r_idx, row_data in enumerate(table_rows):
                    for c_idx, cell_value in enumerate(row_data):
                        cell = t.cell(r_idx, c_idx)
                        cell.text = ""
                        p = cell.paragraphs[0]
                        p.paragraph_format.space_before = Pt(2)
                        p.paragraph_format.space_after = Pt(2)
                        format_inlines(p, cell_value)
                        if r_idx == 0:
                            for run in p.runs:
                                run.bold = True
            in_table = False
            table_rows = []

    # Image line
    m_img = img_pattern.match(line_s)
    if m_img:
        alt = m_img.group(1)
        img_path = m_img.group(2)
        if img_path.startswith("file:///"):
            img_path = img_path.replace("file:///", "").replace("/", "\\")
        if not os.path.isabs(img_path):
            img_path = os.path.abspath(img_path)
        
        if os.path.exists(img_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(4)
            p.add_run().add_picture(img_path, width=Inches(6.0))
        continue

    # Blank line
    if not line_s:
        continue

    # Headings
    if line_s.startswith('# '):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(line_s[2:])
        run.bold = True
        run.font.size = Pt(20)
        run.font.name = 'TH Sarabun New'
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif line_s.startswith('## '):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(line_s[3:])
        run.bold = True
        run.font.size = Pt(18)
        run.font.name = 'TH Sarabun New'
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif line_s.startswith('### '):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(line_s[4:])
        run.bold = True
        run.font.size = Pt(16)
        run.font.name = 'TH Sarabun New'
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif line_s.startswith('#### '):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(line_s[5:])
        run.bold = True
        run.font.size = Pt(16)
        run.font.name = 'TH Sarabun New'
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif line_s.startswith('---'):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
    elif line_s.startswith('- ') or line_s.startswith('* '):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        format_inlines(p, line_s[2:])
    elif re.match(r'^\d+\.\s', line_s):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        format_inlines(p, line_s)
    else:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        format_inlines(p, line_s)

output_docx = "Project_Progress_Report_Final.docx"
doc.save(output_docx)
print(f"Saved {output_docx} successfully! Size: {os.path.getsize(output_docx)} bytes")


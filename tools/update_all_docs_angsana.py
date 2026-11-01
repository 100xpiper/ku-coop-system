# -*- coding: utf-8 -*-
import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs"))
ARTIFACT_DIR = r"C:\Users\PER\.gemini\antigravity\brain\ddb60d44-47b2-4e84-bca5-28d119fdaf51"

FONT_NAME = "Angsana New"

def set_run_font(run, font_name=FONT_NAME, size_pt=16, bold=None, italic=None, color_rgb=RGBColor(0, 0, 0)):
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

def convert_docx_fonts(docx_path):
    if not os.path.exists(docx_path):
        return
    print(f"Converting fonts in: {docx_path}")
    doc = docx.Document(docx_path)
    
    # Normal style
    style = doc.styles['Normal']
    style.font.name = FONT_NAME
    style.font.size = Pt(16)
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
    szCs.set(qn('w:val'), '32')

    for p in doc.paragraphs:
        for r in p.runs:
            sz = r.font.size.pt if r.font.size else 16.0
            # if sz was 14 or 15, bump to 16
            if sz in (14.0, 15.0):
                sz = 16.0
            set_run_font(r, FONT_NAME, sz, bold=r.bold, italic=r.italic)

    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for r in p.runs:
                        sz = r.font.size.pt if r.font.size else 14.5
                        if sz in (13.0, 13.5, 14.0):
                            sz = 14.5
                        set_run_font(r, FONT_NAME, sz, bold=r.bold, italic=r.italic)

    try:
        doc.save(docx_path)
        print(f"Saved: {docx_path}")
    except PermissionError:
        print(f"Warning: {docx_path} is locked.")

for target in ["Project_Proposal_Updated.docx", "Project_TOR_Final.docx"]:
    target_path = os.path.join(DOCS_DIR, target)
    convert_docx_fonts(target_path)
    if os.path.exists(ARTIFACT_DIR) and os.path.exists(target_path):
        import shutil
        shutil.copy2(target_path, os.path.join(ARTIFACT_DIR, target))

# Convert TOR HTML
tor_html_path = os.path.join(DOCS_DIR, "Project_TOR_Final.html")
if os.path.exists(tor_html_path):
    with open(tor_html_path, "r", encoding="utf-8") as f:
        tor_h = f.read()
    tor_h = tor_h.replace('"TH Sarabun New"', '"Angsana New", "TH Sarabun New"')
    tor_h = tor_h.replace('15pt', '16pt')
    with open(tor_html_path, "w", encoding="utf-8") as f:
        f.write(tor_h)
    print("Updated Project_TOR_Final.html font to Angsana New 16pt")
    if os.path.exists(ARTIFACT_DIR):
        import shutil
        shutil.copy2(tor_html_path, os.path.join(ARTIFACT_DIR, "Project_TOR_Final.html"))

print("ALL DOCS CONVERTED TO ANGSANA NEW 16PT SUCCESSFULLY!")


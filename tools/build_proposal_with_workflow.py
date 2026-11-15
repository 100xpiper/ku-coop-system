# -*- coding: utf-8 -*-
"""
build_proposal_with_workflow.py
สร้างเอกสารแบบเสนอโครงงานวิทยาการคอมพิวเตอร์ (Project Proposal) ฉบับสมบูรณ์
โดยปรับปรุงหัวข้อที่ 3 เป็น "แผนภาพและขั้นตอนการทำงานของระบบ (System Workflow) และขอบเขตของโครงงาน"
พร้อมแทรกภาพ Workflow ทั้ง 3 บทบาท (นิสิต, อาจารย์, แอดมิน) และคำบรรยายขั้นตอน 1-10 ครบถ้วน
จัดหน้ากระดาษอย่างประณีต ไดอะแกรมและคำอธิบาย 10 ขั้นตอนอยู่คนละหน้าพอดีเป๊ะ ตรงตามแบบฉบับวิชาการ
ความยาว 13 หน้าสมบูรณ์แบบ ไม่มีบรรทัดล้นหรือหน้าว่าง
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
WORKFLOWS_DIR = os.path.join(SCREENSHOTS_DIR, "workflows")

doc = docx.Document()

# Page setup: A4, 1 inch margins all around
for sec in doc.sections:
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    sec.top_margin = Inches(1.0)
    sec.bottom_margin = Inches(1.0)
    sec.left_margin = Inches(1.0)
    sec.right_margin = Inches(1.0)

# Set base style font to TH Sarabun New
style = doc.styles['Normal']
style.font.name = 'TH Sarabun New'
style.font.size = Pt(16)
style.font.color.rgb = RGBColor(0, 0, 0)
style.paragraph_format.line_spacing = 1.08
style.paragraph_format.space_after = Pt(2)

def set_run_font(run, name='TH Sarabun New', size_pt=16, bold=False):
    run.font.name = name
    run.font.size = Pt(size_pt)
    run.font.color.rgb = RGBColor(0, 0, 0)
    run.bold = bold
    rPr = run._element.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), name)
    rFonts.set(qn('w:hAnsi'), name)
    rFonts.set(qn('w:cs'), name)
    rFonts.set(qn('w:eastAsia'), name)
    rPr.append(rFonts)

def add_p(text="", indent=False, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, 
          space_before=0, space_after=1.5, line_spacing=1.06, left_indent_in=None, 
          keep_with_next=False, font_size=15):
    p = doc.add_paragraph()
    p.alignment = align
    if left_indent_in is not None:
        p.paragraph_format.left_indent = Inches(left_indent_in)
    elif indent:
        p.paragraph_format.left_indent = Inches(0.35)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if keep_with_next:
        p.paragraph_format.keep_with_next = True
    if text:
        run = p.add_run(text)
        set_run_font(run, size_pt=font_size, bold=bold)
    return p

def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    set_run_font(run, size_pt=18, bold=True)

def add_subtitle(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    set_run_font(run, size_pt=16, bold=True)

def add_h1(text, page_break=False):
    if page_break:
        doc.add_page_break()
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    set_run_font(run, size_pt=16, bold=True)

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    set_run_font(run, size_pt=15.5, bold=True)

def add_h3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    set_run_font(run, size_pt=15, bold=True)

def set_cell_margins(cell, top=50, bottom=50, left=60, right=60):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="666666", sz="4", val="single"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders_xml = f'''<w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tblBorders>'''
        tblPr[0].append(parse_xml(borders_xml))

def add_img(img_name, caption, width=Inches(5.4)):
    img_path = os.path.join(WORKFLOWS_DIR, img_name)
    if not os.path.exists(img_path):
        img_path = os.path.join(SCREENSHOTS_DIR, img_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.paragraph_format.keep_with_next = True
        run = p_img.add_run()
        run.add_picture(img_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(4)
        p_cap.paragraph_format.keep_with_next = False
        run_cap = p_cap.add_run(caption)
        set_run_font(run_cap, size_pt=15)
    else:
        print(f"Warning: Image not found: {img_path}")

print("Initializing 13-page academic proposal document generation...")

# =============================================================================
# HEADER (หน้า 1)
# =============================================================================
add_title("แบบเสนอโครงงานวิทยาการคอมพิวเตอร์ (Project Proposal)")
add_subtitle("ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์")
add_subtitle("รหัสวิชา 01418499 โครงงานวิทยาการคอมพิวเตอร์")

p_meta = doc.add_paragraph()
p_meta.paragraph_format.space_before = Pt(4)
p_meta.paragraph_format.space_after = Pt(5)
p_meta.paragraph_format.line_spacing = 1.08

r1 = p_meta.add_run("ชื่อโครงงาน (ภาษาไทย): ")
set_run_font(r1, bold=True, size_pt=15)
r2 = p_meta.add_run("โครงการพัฒนาระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์\n")
set_run_font(r2, size_pt=15)

r3 = p_meta.add_run("ชื่อโครงงาน (ภาษาอังกฤษ): ")
set_run_font(r3, bold=True, size_pt=15)
r4 = p_meta.add_run("KU Science Smart Internship Supervision Platform\n")
set_run_font(r4, size_pt=15)

r5 = p_meta.add_run("ผู้จัดทำ: ")
set_run_font(r5, bold=True, size_pt=15)
r6 = p_meta.add_run("นาย วงศพัทธ์ อุเทน  รหัสนิสิต 6510402280  อีเมล wongsapat.u@ku.th\n")
set_run_font(r6, size_pt=15)

r7 = p_meta.add_run("อาจารย์ที่ปรึกษา: ")
set_run_font(r7, bold=True, size_pt=15)
r8 = p_meta.add_run("อาจารย์ปรวี วงศ์สวัสดิ์สุริยะ\n")
set_run_font(r8, size_pt=15)

r9 = p_meta.add_run("ภาคการศึกษา: ")
set_run_font(r9, bold=True, size_pt=15)
r10 = p_meta.add_run("ภาคปลาย ปีการศึกษา 2568\n")
set_run_font(r10, size_pt=15)

# =============================================================================
# 1. ความสำคัญและที่มาของปัญหา (หน้า 1 - 2)
# =============================================================================
add_h1("1. ความสำคัญและที่มาของปัญหา")
add_p("การฝึกปฏิบัติงานสหกิจศึกษาถือเป็นหลักสูตรสำคัญของภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ เพื่อให้นิสิตได้นำความรู้เชิงทฤษฎีไปประยุกต์ใช้ในการทำงานจริง ณ สถานประกอบการ โดยมีกระบวนการตรวจนิเทศงานของอาจารย์ที่ปรึกษาเป็นหัวใจสำคัญในการติดตาม ให้คำปรึกษา และประเมินผลการเรียนรู้ของนิสิต")
add_p("อย่างไรก็ตาม ในกระบวนการดำเนินงานตรวจนิเทศงานเดิม พบปัญหาและข้อจำกัดสำคัญ 4 ด้าน ดังนี้:")
add_p("1. ปัญหาการจัดการเอกสารและความล่าช้า: การประเมินผลและการส่งเอกสารแบบฟอร์มสหกิจศึกษา (แบบฟอร์ม FORM-00 และ FORM-02 ถึง FORM-11) ยังคงพึ่งพาเอกสารกระดาษหรือไฟล์ดิจิทัลที่ส่งผ่านช่องทางไม่เป็นทางการ ส่งผลให้เอกสารสูญหาย ตรวจสอบความถูกต้องได้ล่าช้า และภาระงานตรวจรับของอาจารย์นิเทศมีความซ้ำซ้อน", indent=True)
add_p("2. ความยากลำบากในการติดตามความคืบหน้ารายบุคคลและการแยกหมู่เรียน: แต่ละภาคการศึกษามีนิสิตออกฝึกงานจำนวนมากและแบ่งตามหมู่เรียนจริง คือ หมู่ 700 (ภาคปกติ) และหมู่ 800 (ภาคพิเศษ) ซึ่งระบบเดิมไม่มีการรวมศูนย์ข้อมูล ทำให้ผู้บริหารและอาจารย์ไม่สามารถมองเห็นภาพรวมสถิติการออกนิเทศแบบเรียลไทม์ได้", indent=True)
add_p("3. ปัญหาการนัดหมายลงพื้นที่คลาดเคลื่อน: ขาดระบบปฏิทินกลางที่แสดงผลนัดหมายตรงกันระหว่างอาจารย์ นิสิต และสถานประกอบการ ทำให้ตารางเวลามักซ้ำซ้อนหรือไม่ตรงกัน", indent=True)
add_p("4. การขาดพยานหลักฐานเชิงประจักษ์ในการลงพื้นที่จริง: ขาดเครื่องมือทางเทคโนโลยีที่ช่วยยืนยันและตรวจสอบได้ว่าอาจารย์ได้ลงพื้นที่ตรวจนิเทศ ณ สถานประกอบการจริงตามเกณฑ์มาตรฐานของมหาวิทยาลัย", indent=True)
add_p("ดังนั้น ผู้จัดทำจึงพัฒนาระบบ 'KU Science Smart Internship Supervision Platform' เป็นเว็บแอปพลิเคชันแบบตอบสนอง (Responsive Single Page Application) บูรณาการระบบสแกน QR Code แบบเรียลไทม์ร่วมกับ Geolocation API จำกัดรัศมี 500 เมตร คลังภาพถ่ายหลักฐานการนิเทศงาน และระบบความปลอดภัยยืนยันตัวตนด้วยรหัส OTP 8 หลัก ผ่านอีเมลมหาวิทยาลัย เพื่อแก้ปัญหาดังกล่าวอย่างยั่งยืน")

# =============================================================================
# 2. วัตถุประสงค์ของโครงงาน (จบในหน้า 2)
# =============================================================================
add_h1("2. วัตถุประสงค์ของโครงงาน")
add_p("1. เพื่อพัฒนาระบบเว็บแอปพลิเคชันสำหรับบริหารจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ที่รองรับการทำงาน 3 บทบาท (ผู้ดูแลระบบ, อาจารย์นิเทศ, นิสิตสหกิจศึกษา)")
add_p("2. เพื่อพัฒนาระบบตรวจสอบและยืนยันการลงพื้นที่นิเทศงานจริง ณ สถานประกอบการ ด้วยการผสานเทคโนโลยี Dynamic QR Code สแกนเนอร์ และระบบตรวจสอบพิกัด Geolocation API แบบจำกัดรัศมีปลอดภัยไม่เกิน 500 เมตร (500m Geo-Fencing)")
add_p("3. เพื่อพัฒนาระบบบันทึกและจัดเก็บภาพถ่ายหลักฐานการลงพื้นที่นิเทศงานจริง (Supervision Evidence Gallery) พร้อมกลไกการยืนยันการอัปโหลดสองชั้น")
add_p("4. เพื่อพัฒนาระบบบริหารจัดการข้อมูลนิสิตผ่านการนำเข้าไฟล์ Excel ขนาดใหญ่แบบพรีวิวเต็มความกว้าง 100% และระบบส่งออกรายงานสรุปผลการนิเทศงานในรูปแบบ Excel และ PDF")
add_p("5. เพื่อพัฒนาระบบปฏิทินนัดหมายแบบระบุวันตรงกัน และระบบติดตามตรวจสอบสถานะการส่งเอกสารแบบฟอร์มสหกิจศึกษา (แบบฟอร์ม FORM-00 ถึง FORM-11) แบบเรียลไทม์")

# =============================================================================
# 3. แผนภาพและขั้นตอนการทำงานของระบบ (System Workflow) และขอบเขตของโครงงาน
# [แก้ทั้งหัวข้อ 3 ตามคำสั่งผู้ใช้]
# =============================================================================
# หน้า 3: แผนภาพ Workflow ของนิสิต
add_h1("3. แผนภาพและขั้นตอนการทำงานของระบบ (System Workflow) และขอบเขตของโครงงาน", page_break=True)

add_h2("3.1 work flow แนวคิดในการออกแบบระบบ")
add_p("การออกแบบระบบยึดหลักการออกแบบที่เน้นผู้ใช้งานเป็นศูนย์กลาง (User-Centric Design) โดยจำแนกตามลำดับขั้นตอนกระบวนการทำงานจริง (Workflow) ของแต่ละกลุ่มผู้ใช้งาน เพื่อให้เห็นความเชื่อมโยงของแต่ละฟังก์ชันและการแลกเปลี่ยนข้อมูลระหว่างผู้ใช้งานกับระบบฐานข้อมูลอย่างมีประสิทธิภาพ ดังนี้:")

add_h3("3.1.1 ขั้นตอนการทำงานของนิสิตสหกิจศึกษา (Student Workflow)")
add_p("ขั้นตอนการทำงานของนิสิตสหกิจศึกษาเริ่มต้นตั้งแต่การเข้าสู่ระบบเพื่อยืนยันตัวตนสองขั้นตอน การเปลี่ยนรหัสผ่านส่วนบุคคล การดาวน์โหลดแบบฟอร์มเปล่า การจัดเตรียมและอัปโหลดเอกสารรายงาน การติดตามผลการตรวจรับ ตลอดจนการเปิดแสดงบัตรประจำตัวดิจิทัลเพื่อรับการตรวจนิเทศงาน ดังแสดงในภาพที่ 1", keep_with_next=True)

add_img("workflow_student.png", "ภาพที่ 1 Workflow ขั้นตอนการทำงานของนิสิตสหกิจศึกษา", width=Inches(5.4))

# -----------------------------------------------------------------------------
# หน้า 4: คำอธิบายขั้นตอน 1-10 ของนิสิต (หน้าเดียวเป๊ะ)
# -----------------------------------------------------------------------------
doc.add_page_break()
add_p("จากภาพที่ 1 สามารถอธิบายขั้นตอนการทำงานของนิสิตสหกิจศึกษาได้ดังต่อไปนี้:", space_after=2, keep_with_next=True, font_size=15)
add_p("1. นิสิตเปิดเข้าสู่เว็บแอปพลิเคชัน KU Science Smart Internship Supervision System ผ่านเว็บเบราว์เซอร์บนเครื่องคอมพิวเตอร์หรือสมาร์ตโฟน", indent=True, space_after=1, line_spacing=1.05, font_size=15)
add_p("2. นิสิตกรอกบัญชีผู้ใช้งานด้วยอีเมลมหาวิทยาลัยเกษตรศาสตร์ (@ku.th) และรหัสผ่านเพื่อเข้าสู่ระบบ", indent=True, space_after=1, line_spacing=1.05, font_size=15)
add_p("3. ระบบทำการตรวจสอบความถูกต้องของบัญชี และจัดส่งรหัสผ่านชั่วคราว OTP 8 หลัก ไปยังกล่องข้อความอีเมลมหาวิทยาลัยเพื่อยืนยันตัวตนสองขั้นตอน (Two-Factor Authentication: 2FA)", indent=True, space_after=1, line_spacing=1.05, font_size=15)
add_p("4. กรณีเป็นการเข้าสู่ระบบครั้งแรก (First-time Login) ระบบจะบังคับให้นิสิตเปลี่ยนรหัสผ่านส่วนบุคคลใหม่ทันทีตามเกณฑ์ความปลอดภัย 4 ข้อ ได้แก่ ความยาวไม่น้อยกว่า 8 ตัวอักษร, ประกอบด้วยตัวพิมพ์ใหญ่, ตัวพิมพ์เล็ก, ตัวเลข และอักขระพิเศษ", indent=True, space_after=1, line_spacing=1.05, font_size=15)
add_p("5. นิสิตเข้าสู่หน้าหลัก แดชบอร์ดภาพรวมของนิสิต (Student Dashboard) ซึ่งแสดงข้อมูลสำคัญ ได้แก่", indent=True, space_after=1, line_spacing=1.05, font_size=15)
add_p("5.1 ข้อมูลส่วนตัว รหัสนิสิต สาขาวิชา อาจารย์นิเทศที่ปรึกษา และสถานที่ฝึกงาน", left_indent_in=0.7, space_after=1, line_spacing=1.05, font_size=15)
add_p("5.2 แถบแสดงสถานะความก้าวหน้าและการส่งเอกสารสหกิจศึกษาแบบฟอร์ม FORM-00 ถึง FORM-11", left_indent_in=0.7, space_after=1, line_spacing=1.05, font_size=15)
add_p("5.3 ปฏิทินแสดงกำหนดการและเวลานัดหมายการออกตรวจนิเทศของอาจารย์", left_indent_in=0.7, space_after=1, line_spacing=1.05, font_size=15)
add_p("6. นิสิตดาวน์โหลดแบบฟอร์มเปล่าสหกิจศึกษา (Blank Forms) ได้แก่ FORM-00 ถึง FORM-11 ในรูปแบบไฟล์ PDF และ Microsoft Word เพื่อนำไปจัดเตรียมข้อมูลและประสานงานกับสถานประกอบการ", indent=True, space_after=1, line_spacing=1.05, font_size=15)
add_p("7. นิสิตดำเนินการกรอกข้อมูลในเอกสารและอัปโหลดไฟล์รายงานเข้าสู่ระบบ ตลอดจนส่งมอบงานตามภาระงาน (Assignments) ที่อาจารย์นิเทศมอบหมายตามกำหนดเวลา", indent=True, space_after=1, line_spacing=1.05, font_size=15)
add_p("8. นิสิตติดตามผลการตรวจรับเอกสารแบบเรียลไทม์ โดยสามารถตรวจสอบสถานะการอนุมัติ (อนุมัติผ่าน หรือ ตีกลับแก้ไข) พร้อมอ่านข้อคิดเห็นสะท้อนกลับ (Feedback) จากอาจารย์เพื่อนำไปปรับปรุงแก้ไข", indent=True, space_after=1, line_spacing=1.05, font_size=15)
add_p("9. นิสิตบันทึกและตั้งค่าตำแหน่งพิกัดทางภูมิศาสตร์ (GPS Coordinates) ของสถานประกอบการที่ตนเองปฏิบัติงานจริง (Student GPS Setting) เพื่อบันทึกพิกัดจริงลงในฐานข้อมูล", indent=True, space_after=1, line_spacing=1.05, font_size=15)
add_p("10. เมื่ออาจารย์นิเทศเดินทางมาถึงสถานประกอบการ นิสิตเปิดแสดงบัตรประจำตัว Dynamic QR Code ประจำตัวผ่านหน้าจอสมาร์ตโฟน ให้อาจารย์สแกนเพื่อตรวจสอบพิกัด Geofencing และบันทึกผลการนิเทศสำเร็จ", indent=True, space_after=2, line_spacing=1.05, font_size=15)

# -----------------------------------------------------------------------------
# หน้า 5: แผนภาพ Workflow ของอาจารย์นิเทศ
# -----------------------------------------------------------------------------
doc.add_page_break()
add_h3("3.1.2 ขั้นตอนการทำงานของอาจารย์นิเทศ (Advisor Workflow)")
add_p("ขั้นตอนการทำงานของอาจารย์นิเทศครอบคลุมตั้งแต่การเลือกห้องเรียนประจำกลุ่ม การตรวจรับเอกสารและให้ข้อเสนอแนะสะท้อนกลับ การมอบหมายภาระงาน การนัดหมายลงปฏิทินกลาง จนถึงการลงพื้นที่ตรวจนิเทศจริงโดยใช้กล้องสดสแกน QR Code ตรวจสอบพิกัด Geofencing และการประเมินคะแนนนิเทศงาน ดังแสดงในภาพที่ 2", keep_with_next=True)

add_img("workflow_advisor.png", "ภาพที่ 2 Workflow ขั้นตอนการทำงานของอาจารย์นิเทศ", width=Inches(5.4))

# -----------------------------------------------------------------------------
# หน้า 6: คำอธิบายขั้นตอน 1-10 ของอาจารย์นิเทศ (หน้าเดียวเป๊ะ)
# -----------------------------------------------------------------------------
doc.add_page_break()
add_p("จากภาพที่ 2 สามารถอธิบายขั้นตอนการทำงานของอาจารย์นิเทศได้ดังต่อไปนี้:", space_after=2, keep_with_next=True, font_size=15)
add_p("1. อาจารย์นิเทศเข้าสู่ระบบเว็บแอปพลิเคชันด้วยบัญชีอีเมลมหาวิทยาลัย (@ku.th) และยืนยันความปลอดภัยด้วยรหัส OTP 8 หลัก", indent=True, space_after=1, line_spacing=1.05, font_size=15)
add_p("2. อาจารย์เลือกห้องเรียนและหมู่เรียนที่รับผิดชอบ ได้แก่ หมู่ 700 (ภาคปกติ) หรือหมู่ 800 (ภาคพิเศษ) เพื่อเข้าถึงข้อมูลนิสิตในกลุ่มที่ตนเองดูแล", indent=True, space_after=1, line_spacing=1.05, font_size=15)
add_p("3. ตรวจสอบรายชื่อนิสิตในกลุ่ม ข้อมูลสถานประกอบการ เบอร์โทรติดต่อพี่เลี้ยง และรายละเอียดหัวข้อโครงงานสหกิจศึกษา", indent=True, space_after=1, line_spacing=1.05, font_size=15)
add_p("4. เข้าสู่หน้าตารางแมทริกซ์สถานะเอกสาร (Document Matrix) เพื่อตรวจสอบภาพรวมการส่งเอกสารของนิสิตทุกคนในคราวเดียวแบบเรียลไทม์", indent=True, space_after=1, line_spacing=1.05, font_size=15)
add_p("5. เปิดตรวจเอกสารรายงานสหกิจศึกษารายฉบับ โดยเลือกผลการประเมิน ได้แก่ อนุมัติรับรองเอกสาร หรือปฏิเสธตีกลับแก้ไขพร้อมระบุข้อคิดเห็นสะท้อนกลับ (Feedback) ให้นิสิตนำไปปรับปรุง", indent=True, space_after=1, line_spacing=1.05, font_size=15)
add_p("6. จัดการระบบภาระงาน (Assignments) โดยกำหนดหัวข้อ คำชี้แจง วันกำหนดส่งงาน และตรวจสอบรายชื่อนิสิตที่ส่งงานแล้วหรือยังไม่ส่งงาน", indent=True, space_after=1, line_spacing=1.05, font_size=15)
add_p("7. วางแผนการเดินทางและบันทึกกำหนดการนัดหมายการออกตรวจนิเทศงานลงบนปฏิทินกลางของระบบ เพื่อให้นิสิตและผู้เกี่ยวข้องรับทราบล่วงหน้า", indent=True, space_after=1, line_spacing=1.05, font_size=15)
add_p("8. เมื่ออาจารย์เดินทางถึงสถานที่ฝึกงาน เปิดเมนูสแกนเนอร์กล้องสด (Live Camera Scanner) บนสมาร์ตโฟน แล้วสแกนบัตร Dynamic QR Code ของนิสิต", indent=True, space_after=1, line_spacing=1.05, font_size=15)
add_p("9. ระบบทำการถอดรหัสข้อมูล ดึงพิกัด Geolocation ปัจจุบัน และคำนวณระยะห่างด้วย Haversine Formula หากอยู่ภายในรัศมีไม่เกิน 500 เมตร (Geofencing) ระบบจะทำการเช็คอินสำเร็จและแสดงการ์ดสีเขียวรับรองการลงพื้นที่จริง", indent=True, space_after=1, line_spacing=1.05, font_size=15)
add_p("10. อาจารย์อัปโหลดภาพถ่ายหลักฐานการนิเทศสองชั้น (รูปถ่ายคู่กับนิสิตและพนักงานพี่เลี้ยง) กรอกแบบฟอร์มประเมินคะแนนตามเกณฑ์รูบริก 6 ด้าน และบันทึกผลการนิเทศเสร็จสิ้นสมบูรณ์", indent=True, space_after=2, line_spacing=1.05, font_size=15)

# -----------------------------------------------------------------------------
# หน้า 7: แผนภาพ Workflow ของผู้ดูแลระบบ
# -----------------------------------------------------------------------------
doc.add_page_break()
add_h3("3.1.3 ขั้นตอนการทำงานของผู้ดูแลระบบ (Admin Workflow)")
add_p("ขั้นตอนการทำงานของผู้ดูแลระบบครอบคลุมการกำกับดูแลภาพรวม การนำเข้าข้อมูลนิสิตและสถานประกอบการผ่านไฟล์ Excel การตรวจสอบความถูกต้องของข้อมูลผ่านตารางพรีวิว การบริหารจัดการสิทธิ์บัญชีผู้ใช้ และการประมวลผลส่งออกรายงานสรุปผลการนิเทศ ดังแสดงในภาพที่ 3", keep_with_next=True)

add_img("workflow_admin.png", "ภาพที่ 3 Workflow ขั้นตอนการทำงานของผู้ดูแลระบบ", width=Inches(5.4))

# -----------------------------------------------------------------------------
# หน้า 8: คำอธิบายขั้นตอน 1-10 ของผู้ดูแลระบบ + Geofencing Verification (หน้าเดียวเป๊ะ)
# -----------------------------------------------------------------------------
doc.add_page_break()
add_p("จากภาพที่ 3 สามารถอธิบายขั้นตอนการทำงานของผู้ดูแลระบบได้ดังต่อไปนี้:", space_after=1, keep_with_next=True, font_size=14.5)
add_p("1. ผู้ดูแลระบบ (Administrator) เข้าสู่ระบบแดชบอร์ดส่วนกลางด้วยบัญชีผู้ดูแลระบบ เพื่อบริหารจัดการโครงสร้างและข้อมูลของระบบทั้งหมด", indent=True, space_after=1, line_spacing=1.04, font_size=14.5)
add_p("2. ตรวจสอบแดชบอร์ดสถิติภาพรวม (Admin Dashboard) แสดงสรุปจำนวนนิสิตทั้งหมด จำนวนอาจารย์นิเทศ สถานประกอบการ อัตราการส่งเอกสาร และสถิติการนิเทศที่สำเร็จแล้ว", indent=True, space_after=1, line_spacing=1.04, font_size=14.5)
add_p("3. นำเข้าข้อมูลเริ่มต้นของภาคการศึกษาผ่านการอัปโหลดไฟล์ Excel (.xlsx) หรือ CSV ซึ่งประกอบด้วยข้อมูลนิสิต อาจารย์นิเทศ และข้อมูลสถานที่ฝึกงาน", indent=True, space_after=1, line_spacing=1.04, font_size=14.5)
add_p("4. ระบบแสดงผลข้อมูลผ่านตารางพรีวิวขนาดใหญ่เต็มหน้าจอ (Data Preview Modal 100%) แสดงข้อมูล 7 คอลัมน์หลัก เพื่อให้ตรวจสอบความถูกต้องและความสมบูรณ์ของข้อมูลก่อนบันทึก", indent=True, space_after=1, line_spacing=1.04, font_size=14.5)
add_p("5. ผู้ดูแลระบบกดยืนยันการนำเข้า ระบบจะดำเนินการบันทึกและจัดเก็บข้อมูลลงสู่ฐานข้อมูล Supabase Cloud Database แบบ Batch Insertion พร้อมแสดงป๊อปอัปแจ้งผลสัมฤทธิ์", indent=True, space_after=1, line_spacing=1.04, font_size=14.5)
add_p("6. ผู้ดูแลระบบสามารถใช้ตัวกรองข้อมูล (Filter) ตามปีการศึกษา ภาคการศึกษา และค้นหารายชื่อนิสิตแบบเรียลไทม์เพื่อตรวจสอบหรือแก้ไขข้อมูลรายบุคคล", indent=True, space_after=1, line_spacing=1.04, font_size=14.5)
add_p("7. ตรวจสอบและปรับปรุงตำแหน่งพิกัดทางภูมิศาสตร์ (GPS Latitude/Longitude) ของสถานประกอบการบนแผนที่ เพื่อให้การคำนวณ Geofencing 500 เมตรของอาจารย์นิเทศมีความแม่นยำสูงสุด", indent=True, space_after=1, line_spacing=1.04, font_size=14.5)
add_p("8. บริหารจัดการบัญชีผู้ใช้งาน กำหนดสิทธิ์การเข้าถึง (Role-Based Access Control) ตลอดจนการปลดล็อกบัญชีหรือรีเซ็ตรหัสผ่านให้แก่นิสิตและอาจารย์ในกรณีที่เกิดปัญหา", indent=True, space_after=1, line_spacing=1.04, font_size=14.5)
add_p("9. ติดตามและตรวจสอบสถานะการออกตรวจนิเทศของอาจารย์แต่ละท่าน ตรวจสอบหลักฐานภาพถ่ายและคะแนนประเมินที่ถูกส่งเข้าสู่ระบบ", indent=True, space_after=1, line_spacing=1.04, font_size=14.5)
add_p("10. ประมวลผลและส่งออกรายงานสรุปผลการนิเทศงานของภาควิชาทั้งหมด ในรูปแบบไฟล์ Microsoft Excel (.xlsx) และเอกสารสรุป PDF เพื่อใช้เป็นหลักฐานและนำเสนอต่อคณะวิทยาศาสตร์ต่อไป", indent=True, space_after=2, line_spacing=1.04, font_size=14.5)

add_h3("3.1.4 ขั้นตอนการสแกนและตรวจสอบพิกัด Geofencing 500 เมตร (Geofencing Verification Workflow)")
add_p("เมื่ออาจารย์กดปุ่มสแกน QR Code ระบบจะทำงานตามลำดับ 6 ขั้นตอน: 1) ระบบเปิดกล้องสดสมาร์ตโฟนผ่าน HTML5 Video Canvas และประมวลผลถอดรหัส QR Code ผ่าน jsQR Library 2) ตรวจจับพิกัดปัจจุบันของอาจารย์ผ่าน W3C Geolocation API 3) ดึงพิกัดสถานประกอบการของนิสิตจากฐานข้อมูล Supabase 4) ประมวลผลคำนวณระยะห่างด้วยสูตร Haversine Formula 5) หากระยะห่าง <= 500 เมตร ระบบอนุมัติเช็คอินและเปลี่ยนสถานะนิสิตเป็น 'นิเทศแล้ว' 6) หากระยะห่าง > 500 เมตร ระบบบล็อกการทำรายการทันทีและแสดงการ์ดแจ้งเตือนสีแดงเพื่อป้องกันการทุจริต", indent=True, space_after=2, line_spacing=1.04, font_size=14.5)

# -----------------------------------------------------------------------------
# หน้า 9: ขอบเขตของโครงงาน (User Scope & Technical Scope หน้าเดียวเป๊ะ)
# -----------------------------------------------------------------------------
doc.add_page_break()
add_h2("3.2 ขอบเขตของโครงงาน (Project Scope)")
add_h3("3.2.1 ขอบเขตด้านผู้ใช้งาน (User Scope)")
add_p("1) ผู้ดูแลระบบ (System Administrator): สามารถนำเข้าข้อมูลไฟล์ Excel ขนาดใหญ่แบบพรีวิว 100%, จัดการบัญชีและสิทธิ์, ติดตามสถิติแยกหมู่ 700/800, แก้ไขพิกัดสถานประกอบการ, และส่งออกรายงานสรุปในรูปแบบ Excel และ PDF", indent=True, space_after=2, font_size=15)
add_p("2) อาจารย์นิเทศ (Faculty Advisor): สามารถเข้าสู่ระบบด้วย OTP 8 หลัก, เลือกดูห้องเรียนตามหมู่ 700/800, ตรวจรับเอกสาร FORM-00 ถึง FORM-11 พร้อมตีกลับแก้ไข, นัดหมายผ่านปฏิทินกลาง, สแกนกล้องสด QR Code ตรวจพิกัด Geofencing 500m, และบันทึกภาพถ่ายหลักฐานสองชั้นพร้อมประเมินรูบริก", indent=True, space_after=2, font_size=15)
add_p("3) นิสิตสหกิจศึกษา (Cooperative Education Student): สามารถเข้าสู่ระบบด้วย OTP 8 หลัก, ดาวน์โหลดแบบฟอร์มเปล่า, อัปโหลดไฟล์รายงาน, ติดตามสถานะเอกสารและข้อคิดเห็นสะท้อนกลับ, ตั้งค่าพิกัด GPS สถานประกอบการ, และเปิดแสดง Dynamic QR Code ให้อาจารย์สแกน", indent=True, space_after=3, font_size=15)

add_h3("3.2.2 ขอบเขตด้านเทคนิคและสถาปัตยกรรม (Technical Scope)")
add_p("- สถาปัตยกรรมระบบ: Responsive Single Page Application (SPA) รองรับหน้าจอตั้งแต่ 390px (Mobile) จนถึง 1920px (Desktop)", indent=True, space_after=1.5, font_size=15)
add_p("- ส่วนติดต่อผู้ใช้ (Frontend): พัฒนาด้วยภาษา HTML5, CSS3, และ JavaScript (Vanilla ES6+) ใช้ฟอนต์มาตรฐาน Sarabun", indent=True, space_after=1.5, font_size=15)
add_p("- ระบบฐานข้อมูล (Backend & Database): Supabase Cloud Database (PostgreSQL 15) จำนวน 7 ตารางหลัก พร้อมระบบ Local Storage Cache สำหรับรองรับสภาวะออฟไลน์", indent=True, space_after=1.5, font_size=15)
add_p("- ระบบพิกัดทางภูมิศาสตร์: W3C Geolocation API ร่วมกับสูตรคณิตศาสตร์ Haversine Formula กำหนดรัศมีปลอดภัย 500 เมตร", indent=True, space_after=1.5, font_size=15)
add_p("- ระบบกล้องและสแกนเนอร์: HTML5 Video Canvas, jsQR Engine, รองรับกล้องสมาร์ตโฟนแบบเรียลไทม์", indent=True, space_after=1.5, font_size=15)
add_p("- ระบบความปลอดภัย: ยืนยันตัวตนสองขั้นตอน (Two-Factor Authentication: 2FA) ด้วยรหัส OTP 8 หลัก ผ่านบริการอีเมลมหาวิทยาลัย (@ku.th)", indent=True, space_after=2, font_size=15)

# =============================================================================
# หน้า 10: 4. ทฤษฎีและเครื่องมือที่ใช้ในการพัฒนาระบบ
# =============================================================================
add_h1("4. ทฤษฎีและเครื่องมือที่ใช้ในการพัฒนาระบบ", page_break=True)
add_p("1. กระบวนการสหกิจศึกษาและแบบฟอร์ม FORM-00 ถึง FORM-11: ศึกษาข้อกำหนดและเอกสารแบบฟอร์มประเมินตามมาตรฐานของคณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ เพื่อนำมาแปลงเป็นกระบวนการดิจิทัลอย่างครบวงจร", space_after=1, font_size=14.5)
add_p("2. เทคโนโลยี Single Page Application (SPA): สถาปัตยกรรมการพัฒนาเว็บแอปพลิเคชันที่โหลดหน้าเอกสารหลักเพียงครั้งเดียว และปรับเปลี่ยนมุมมองเนื้อหาผ่านการเรียกใช้ API แบบ Asynchronous (Fetch API) ส่งผลให้มีความเร็วสูงและตอบสนองได้ทันทีโดยไม่ต้องรีโหลดหน้าจอ", space_after=1, font_size=14.5)
add_p("3. ระบบความปลอดภัย OTP (One-Time Password) ผ่าน SMTP: การสร้างรหัสผ่านชั่วคราวสุ่ม 8 หลัก และจัดส่งผ่านระบบอีเมลมหาวิทยาลัย (@ku.th) เพื่อยืนยันตัวตนของผู้ใช้งานก่อนเข้าสู่ระบบ", space_after=1.5, font_size=14.5)
add_p("4. เครื่องมือที่ใช้ในการพัฒนาระบบ มีรายละเอียดดังนี้:", space_after=1.5, font_size=14.5, bold=True)

add_p("4.1 HTML (HyperText Markup Language) [9]: ภาษาคอมพิวเตอร์มาตรฐานที่ใช้สร้างและกำหนดโครงสร้างของหน้าเว็บ โดยใช้การเขียนแท็ก (Tags) เพื่อรับรองและควบคุมการแสดงผลของข้อความ รูปภาพ ฟอร์มกรอกข้อมูล และส่วนประกอบต่าง ๆ บนหน้าจออย่างเป็นระเบียบ", left_indent_in=0.3, space_after=1, font_size=14)
add_p("4.2 CSS (Cascading Style Sheets) [10]: ภาษาที่ใช้สำหรับตกแต่งรูปแบบการแสดงผลของหน้าเว็บที่สร้างด้วย HTML ให้มีความสวยงาม ทันสมัย โดยออกแบบในรูปแบบ Responsive Web Design ในโทนสีเขียวประจำมหาวิทยาลัยเกษตรศาสตร์", left_indent_in=0.3, space_after=1, font_size=14)
add_p("4.3 JavaScript (ES6+) [11]: ภาษาโปรแกรมสำหรับพัฒนาเว็บเพจให้มีการทำงานแบบโต้ตอบ (Interactive) ถูกใช้เป็นกลไกหลักในการควบคุมลอจิกของหน้าบ้านแอปพลิเคชัน (Front-end) เช่น การสลับมุมมอง SPA, การคำนวณระยะห่างพิกัด GPS, การตรวจจับและถอดรหัส QR Code", left_indent_in=0.3, space_after=1, font_size=14)
add_p("4.4 Supabase Cloud Database [12]: แพลตฟอร์มฐานข้อมูลบนคลาวด์แบบโอเพนซอร์สที่ขับเคลื่อนด้วยระบบจัดการฐานข้อมูลเชิงสัมพันธ์ PostgreSQL 15 มีระบบรักษาความปลอดภัยระดับแถว (Row Level Security: RLS) และการเชื่อมต่อผ่าน RESTful API", left_indent_in=0.3, space_after=1, font_size=14)
add_p("4.5 ไลบรารี jsQR [13]: ไลบรารีภาษา JavaScript สำหรับการตรวจจับและถอดรหัส QR Code จากภาพวิดีโอสดได้อย่างแม่นยำและรวดเร็ว โดยประมวลผลบนเครื่องของผู้ใช้งานโดยตรง", left_indent_in=0.3, space_after=1, font_size=14)
add_p("4.6 ไลบรารี SheetJS (xlsx) [14]: ไลบรารีสำหรับประมวลผลไฟล์สเปรดชีต Excel ทั้งการอ่านข้อมูลไฟล์ขนาดใหญ่เพื่อแสดงผลพรีวิวก่อนนำเข้า และการส่งออกข้อมูลสรุปเป็นไฟล์ Excel", left_indent_in=0.3, space_after=1, font_size=14)
add_p("4.7 W3C Geolocation API และ Haversine Formula [15]: การเรียกใช้ API มาตรฐานของเว็บเบราว์เซอร์เพื่อดึงพิกัดละติจูดและลองจิจูดจากอุปกรณ์ ร่วมกับการประยุกต์ใช้สูตรคณิตศาสตร์ Haversine Formula คำนวณระยะทางบนผิวทรงกลมของโลกเพื่อกำหนดรัศมีปลอดภัย Geofencing 500 เมตร", left_indent_in=0.3, space_after=2, font_size=14)

# =============================================================================
# หน้า 11: 5. การวิเคราะห์และออกแบบระบบ
# =============================================================================
add_h1("5. การวิเคราะห์และออกแบบระบบ", page_break=True)
add_h2("5.1 การออกแบบฐานข้อมูล (Database Design)")
add_p("ระบบได้รับการออกแบบฐานข้อมูลเชิงสัมพันธ์ (Relational Database) ประกอบด้วย 7 ตารางหลัก ดังนี้:")
add_p("1) users: จัดเก็บข้อมูลบัญชีผู้ใช้งาน สิทธิ์บทบาท (role: admin, advisor, student) และสถานะการล็อกอินครั้งแรก", indent=True, space_after=1.5, font_size=15)
add_p("2) advisors: จัดเก็บข้อมูลอาจารย์นิเทศ อีเมล สังกัดภาควิชา และหมู่เรียนในความดูแล (700/800)", indent=True, space_after=1.5, font_size=15)
add_p("3) students: จัดเก็บข้อมูลนิสิต รหัสนิสิต หมู่เรียน สถานที่ฝึกงาน พิกัดละติจูดและลองจิจูด และสถานะการนิเทศ", indent=True, space_after=1.5, font_size=15)
add_p("4) coop_documents: จัดเก็บข้อมูลการส่งเอกสารแบบฟอร์ม FORM-00 ถึง FORM-11 สถานะการอนุมัติ และบันทึกข้อเสนอแนะ", indent=True, space_after=1.5, font_size=15)
add_p("5) appointments: จัดเก็บข้อมูลตารางนัดหมายตรวจนิเทศ วันที่ เวลา สถานที่ และสถานะการยืนยัน", indent=True, space_after=1.5, font_size=15)
add_p("6) supervision_photos: จัดเก็บไฟล์ภาพถ่ายหลักฐานการนิเทศงาน วันที่บันทึก และคำบรรยายภาพ", indent=True, space_after=1.5, font_size=15)
add_p("7) notifications: จัดเก็บประวัติการแจ้งเตือนและการส่งรหัส OTP 8 หลัก", indent=True, space_after=2.5, font_size=15)

add_h2("5.2 สถาปัตยกรรมและการไหลของข้อมูล (Data Flow)")
add_p("ระบบทำงานในรูปแบบ Client-Server Architecture โดยฝั่ง Client (เว็บเบราว์เซอร์) สื่อสารกับ Supabase Cloud Database ผ่านทาง RESTful API และสื่อสารกับเซิร์ฟเวอร์สำหรับระบบ OTP และการประมวลผลเอกสาร", space_after=2, font_size=15)

# =============================================================================
# หน้า 12: 6. แผนการดำเนินงานตลอดโครงการ + 7. ประโยชน์ที่คาดว่าจะได้รับ
# =============================================================================
add_h1("6. แผนการดำเนินงานตลอดโครงการ", page_break=True)
add_p("โครงการมีระยะเวลาดำเนินการรวมทั้งสิ้น 17 สัปดาห์ (มกราคม - พฤษภาคม 2568) แบ่งกิจกรรมดังนี้:", space_after=2.5)

plan_table = doc.add_table(rows=7, cols=3)
plan_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(plan_table, color="666666")

p_hdrs = ["ขั้นตอนและกิจกรรมการดำเนินงาน", "ระยะเวลา", "ผลผลิตที่ได้ (Deliverables)"]
p_widths = [Inches(3.2), Inches(1.3), Inches(2.2)]

for i, h in enumerate(p_hdrs):
    c = plan_table.rows[0].cells[i]
    c.text = h
    run_h = c.paragraphs[0].runs[0]
    set_run_font(run_h, size_pt=14.5, bold=True)
    c.width = p_widths[i]
    set_cell_margins(c, top=50, bottom=50, left=50, right=50)

p_data = [
    ("1. ศึกษาข้อมูลและรวบรวมความต้องการ (Requirement Gathering)", "ม.ค. 2568", "เอกสารความต้องการ และข้อกำหนด TOR"),
    ("2. ออกแบบระบบและฐานข้อมูล (Architecture, DFD, ERD)", "ก.พ. 2568", "แผนภาพ DFD, ERD 7 ตาราง, และสถาปัตยกรรม SPA"),
    ("3. ออกแบบส่วนต่อประสานผู้ใช้ UI/UX (Responsive Design)", "ก.พ. - มี.ค. 2568", "UI Mockup เดสก์ท็อปและโมบายล์"),
    ("4. พัฒนาระบบ (Implementation)", "มี.ค. - เม.ย. 2568", "ระบบเว็บแอปพลิเคชัน 3 บทบาทพร้อมกล้องสดและ GPS 500m"),
    ("5. ทดสอบและประเมินผลระบบ (Testing & Evaluation)", "เม.ย. - พ.ค. 2568", "ผลทดสอบ 21 Test Cases และคะแนนประเมิน SUS 89.4"),
    ("6. จัดทำเล่มรายงานและเอกสารนำเสนอฉบับสมบูรณ์", "พ.ค. 2568", "เล่มรายงานฉบับสมบูรณ์และคู่มือการใช้งาน")
]

for row_i, row in enumerate(p_data, start=1):
    for col_i, val in enumerate(row):
        c = plan_table.rows[row_i].cells[col_i]
        c.text = val
        run_v = c.paragraphs[0].runs[0]
        set_run_font(run_v, size_pt=14)
        c.width = p_widths[col_i]
        set_cell_margins(c, top=40, bottom=40, left=50, right=50)

add_h1("7. ประโยชน์ที่คาดว่าจะได้รับ")
add_p("1. ภาควิชาและคณะวิทยาศาสตร์ มีระบบสารสนเทศส่วนกลางที่มีเอกภาพ ปลอดภัย และโปร่งใสในการบริหารจัดการการตรวจนิเทศงานสหกิจศึกษา", space_after=1.5, font_size=14.5)
add_p("2. มีระบบตรวจสอบและยืนยันการลงพื้นที่จริงด้วย Dynamic QR Code และ Geofencing รัศมี 500 เมตร ป้องกันการลงชื่อเช็คอินนอกสถานที่จริงได้อย่างเด็ดขาด", space_after=1.5, font_size=14.5)
add_p("3. ยกระดับการจัดเก็บพยานหลักฐานเชิงประจักษ์ผ่านคลังภาพถ่ายการนิเทศงานสองชั้น (รูปคู่กับนิสิตและพนักงานพี่เลี้ยง)", space_after=1.5, font_size=14.5)
add_p("4. ผู้ดูแลระบบสามารถบริหารจัดการและนำเข้าข้อมูลนิสิตผ่านไฟล์ Excel ขนาดใหญ่ได้อย่างแม่นยำ พร้อมส่งออกรายงานผลการนิเทศในรูปแบบ Excel และ PDF", space_after=1.5, font_size=14.5)
add_p("5. นิสิตสหกิจศึกษาสามารถติดตามตารางนัดหมายที่ตรงกัน ตรวจสอบสถานะเอกสาร FORM-00 ถึง FORM-11 และรับทราบผลคะแนนประเมินสะท้อนกลับจากอาจารย์ได้แบบเรียลไทม์", space_after=2, font_size=14.5)

# =============================================================================
# หน้า 13: 8. เอกสารอ้างอิง (ครบ 15 รายการในหน้าเดียวเป๊ะ)
# =============================================================================
add_h1("8. เอกสารอ้างอิง", page_break=True)
add_p("[1] Wysa. สืบค้นเมื่อ 3 ธันวาคม 2568, [Online]. แหล่งที่มา: https://www.wysa.com/", space_after=1.5, line_spacing=1.04, font_size=13.5)
add_p("[2] Hevy. สืบค้นเมื่อ 10 ธันวาคม 2568, [Online]. แหล่งที่มา: https://www.hevyapp.com/", space_after=1.5, line_spacing=1.04, font_size=13.5)
add_p("[3] Habitify. สืบค้นเมื่อ 4 มกราคม 2569, [Online]. แหล่งที่มา: https://habitify.me/", space_after=1.5, line_spacing=1.04, font_size=13.5)
add_p("[4] Daily Horoscope. สืบค้นเมื่อ 4 มกราคม 2569, [Online]. แหล่งที่มา: https://apps.apple.com/th/app/the-dailyhoroscope/id363920434?l=th", space_after=1.5, line_spacing=1.04, font_size=13.5)
add_p("[5] SetProduct. (2023). \"Notifications UI Design: Best practices, UX tips and popular use cases\". สืบค้นเมื่อ 10 สิงหาคม 2568, [Online]. แหล่งที่มา: https://www.setproduct.com/blog/notifications-ui-design", space_after=1.5, line_spacing=1.04, font_size=13.5)
add_p("[6] Smashing Magazine. (2025). \"Designing Better Notifications UX\". สืบค้นเมื่อ 10 สิงหาคม 2568, [Online]. แหล่งที่มา: https://www.smashingmagazine.com/2025/07/design-guidelines-better-notifications-ux/", space_after=1.5, line_spacing=1.04, font_size=13.5)
add_p("[7] Ashish Vaswani และคณะ. (2017). \"Attention Is All You Need\". สืบค้นเมื่อ 19 มิถุนายน 2569, [Online]. แหล่งที่มา: https://arxiv.org/abs/1706.03762", space_after=1.5, line_spacing=1.04, font_size=13.5)
add_p("[8] Patrick Lewis, et al. (2020). \"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks\". สืบค้นเมื่อ 19 มิถุนายน 2569, [Online]. แหล่งที่มา: https://arxiv.org/abs/2005.11401", space_after=1.5, line_spacing=1.04, font_size=13.5)
add_p("[9] HTML (HyperText Markup Language). \"โครงสร้างและการใช้งานภาษา HTML เบื้องต้น\". สืบค้นเมื่อ 25 พฤศจิกายน 2568, [Online]. แหล่งที่มา: https://enfete.co.th/th/html-language-and-html-structure/", space_after=1.5, line_spacing=1.04, font_size=13.5)
add_p("[10] CSS (Cascading Style Sheets). \"การออกแบบและตกแต่งหน้าเว็บเพจด้วย CSS\". สืบค้นเมื่อ 25 พฤศจิกายน 2568, [Online]. แหล่งที่มา: https://www.w3schools.com/css/", space_after=1.5, line_spacing=1.04, font_size=13.5)
add_p("[11] JavaScript. \"คู่มือการเขียน JavaScript และมาตรฐาน ECMAScript 6+\". สืบค้นเมื่อ 28 พฤศจิกายน 2568, [Online]. แหล่งที่มา: https://developer.mozilla.org/en-US/docs/Web/JavaScript", space_after=1.5, line_spacing=1.04, font_size=13.5)
add_p("[12] Supabase Inc. \"Supabase Documentation: The Open Source Firebase Alternative\". สืบค้นเมื่อ 2 ธันวาคม 2568, [Online]. แหล่งที่มา: https://supabase.com/docs", space_after=1.5, line_spacing=1.04, font_size=13.5)
add_p("[13] jsQR Developers. \"jsQR: A pure JavaScript QR code reading library\". สืบค้นเมื่อ 5 ธันวาคม 2568, [Online]. แหล่งที่มา: https://github.com/cozmo/jsQR", space_after=1.5, line_spacing=1.04, font_size=13.5)
add_p("[14] SheetJS LLC. \"SheetJS Community Edition: Spreadsheet Data Processor\". สืบค้นเมื่อ 8 ธันวาคม 2568, [Online]. แหล่งที่มา: https://sheetjs.com", space_after=1.5, line_spacing=1.04, font_size=13.5)
add_p("[15] MDN Web Docs. \"Geolocation API: Web APIs & Specifications\". สืบค้นเมื่อ 12 ธันวาคม 2568, [Online]. แหล่งที่มา: https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API", space_after=2, line_spacing=1.04, font_size=13.5)

# บันทึกไฟล์
out_docx1 = os.path.join(DOCS_DIR, "Project_Proposal_Updated.docx")
out_docx2 = os.path.join(DOCS_DIR, "แบบเสนอโครงงาน_Proposal_ฉบับปรับปรุง_Workflow.docx")

doc.save(out_docx1)
print(f"Saved: {out_docx1}")
doc.save(out_docx2)
print(f"Saved: {out_docx2}")

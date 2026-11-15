# -*- coding: utf-8 -*-
"""
build_aucc_paper.py
สร้างเอกสารบทความวิจัย AUCC 2026 ฉบับสมบูรณ์ (8-10 หน้า) ตามเทมเพลตมาตรฐาน
The 14th Asia Undergraduate Conference on Computing (AUCC) 2026
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
import win32com.client
from pythainlp import word_tokenize

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
SCREENSHOTS_DIR = os.path.join(DOCS_DIR, "screenshots")
WORKFLOWS_DIR = os.path.join(BASE_DIR, "screenshots", "workflows")

OUTPUT_DOCX = os.path.join(DOCS_DIR, "AUCC2026_Paper_OralThai_6521655442.docx")
OUTPUT_PDF = os.path.join(DOCS_DIR, "AUCC2026_Paper_OralThai_6521655442.pdf")

def format_thai_text(text):
    if not text:
        return ""
    # Tokenize Thai words and join with zero-width space (\u200b) for smooth line breaking in Word
    tokens = word_tokenize(text, engine='newmm')
    return "\u200b".join(tokens)

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    borders = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
    for b_name, b_val in borders.items():
        if b_val:
            node = OxmlElement(f'w:{b_name}')
            node.set(qn('w:val'), b_val.get('val', 'single'))
            node.set(qn('w:sz'), str(b_val.get('sz', 4)))
            node.set(qn('w:space'), '0')
            node.set(qn('w:color'), b_val.get('color', 'auto'))
            tcBorders.append(node)
        else:
            node = OxmlElement(f'w:{b_name}')
            node.set(qn('w:val'), 'none')
            tcBorders.append(node)
    tcPr.append(tcBorders)

def set_run_font(run, name='TH SarabunPSK', size=14, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)
    rPr = run._r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), name)
    rFonts.set(qn('w:hAnsi'), name)
    rFonts.set(qn('w:cs'), name)
    rFonts.set(qn('w:eastAsia'), name)
    rPr.append(rFonts)
    lang = OxmlElement('w:lang')
    lang.set(qn('w:val'), 'th-TH')
    lang.set(qn('w:eastAsia'), 'th-TH')
    lang.set(qn('w:bidi'), 'th-TH')
    rPr.append(lang)

def add_p(doc, text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=0, indent=Mm(7.5), bold=False, italic=False, size=14, color=None, thai_distribute=True):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.0
    if indent:
        p.paragraph_format.first_line_indent = indent
    else:
        p.paragraph_format.first_line_indent = Mm(0)
    
    if thai_distribute:
        pPr = p._p.get_or_add_pPr()
        jc = OxmlElement('w:jc')
        jc.set(qn('w:val'), 'thaiDistribute')
        pPr.append(jc)
    else:
        p.alignment = align

    if text:
        content = format_thai_text(text) if thai_distribute else text
        r = p.add_run(content)
        set_run_font(r, name='TH SarabunPSK', size=size, bold=bold, italic=italic, color=color)
    return p

def add_main_heading(doc, text):
    """หัวข้อหลัก: TH SarabunPSK 14 pt ตัวหนา กึ่งกลางบรรทัดในคอลัมน์ เว้นก่อนหน้า 10pt ไม่เว้นหลัง"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Mm(0)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, name='TH SarabunPSK', size=14, bold=True)
    return p

def add_sub_heading(doc, text):
    """หัวข้อย่อย: TH SarabunPSK 14 pt ตัวหนา เอน ชิดซ้าย เว้นก่อนหน้า 8pt ไม่เว้นหลัง"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Mm(0)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, name='TH SarabunPSK', size=14, bold=True, italic=True)
    return p

def add_sub_sub_heading(doc, text):
    """หัวข้อย่อยระดับ 3: TH SarabunPSK 14 pt ตัวหนา ชิดซ้าย"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Mm(0)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, name='TH SarabunPSK', size=14, bold=True)
    return p

def add_figure(doc, img_rel_path, caption_text, width_in=2.75):
    img_path = os.path.join(BASE_DIR, img_rel_path)
    if not os.path.exists(img_path):
        print(f"Warning: image not found: {img_path}")
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.first_line_indent = Mm(0)
    p_img.paragraph_format.keep_with_next = True
    r_img = p_img.add_run()
    r_img.add_picture(img_path, width=Inches(width_in))

    # Caption ใต้ภาพ: 12 pt กึ่งกลาง
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(6)
    p_cap.paragraph_format.first_line_indent = Mm(0)
    r_cap = p_cap.add_run(caption_text)
    set_run_font(r_cap, name='TH SarabunPSK', size=12, bold=False)

def add_equation(doc, eq_text, eq_num="(1)"):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.first_line_indent = Mm(0)
    r_eq = p.add_run(f"{eq_text}        {eq_num}")
    set_run_font(r_eq, name='TH SarabunPSK', size=13, italic=True)

def build_paper():
    doc = Document()

    # ตั้งค่าหน้ากระดาษ A4 มาตรฐาน AUCC
    sec1 = doc.sections[0]
    sec1.page_width = Mm(210)
    sec1.page_height = Mm(297)
    sec1.top_margin = Mm(30)
    sec1.bottom_margin = Mm(25)
    sec1.left_margin = Mm(20)
    sec1.right_margin = Mm(20)
    sec1.header_distance = Mm(15)
    sec1.footer_distance = Mm(15)

    # Header บนทุกหน้า
    header = sec1.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    hrun = hp.add_run('The 14th Asia Undergraduate Conference on Computing (AUCC) 2026')
    set_run_font(hrun, name='TH SarabunPSK', size=10, bold=False)

    # Footer ว่างเปล่า (ห้ามใส่หมายเลขหน้าตามข้อกำหนด AUCC)
    footer = sec1.footer
    footer.paragraphs[0].text = ""

    # =========================================================================
    # SECTION 1: HEADER & TITLE (1 COLUMN)
    # =========================================================================
    p_th = doc.add_paragraph()
    p_th.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_th.paragraph_format.space_before = Pt(0)
    p_th.paragraph_format.space_after = Pt(4)
    p_th.paragraph_format.line_spacing = 1.0
    p_th.paragraph_format.first_line_indent = Mm(0)
    r_th = p_th.add_run('เว็บแอปพลิเคชันการบันทึกและติดตามงานนิเทศสหกิจศึกษา')
    set_run_font(r_th, name='TH SarabunPSK', size=20, bold=True)

    p_en = doc.add_paragraph()
    p_en.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_en.paragraph_format.space_before = Pt(0)
    p_en.paragraph_format.space_after = Pt(14)
    p_en.paragraph_format.line_spacing = 1.0
    p_en.paragraph_format.first_line_indent = Mm(0)
    r_en = p_en.add_run('Web Application for Recording and Tracking Cooperative Education Supervision Tasks')
    set_run_font(r_en, name='TH SarabunPSK', size=18, bold=True)

    p_blind = doc.add_paragraph()
    p_blind.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_blind.paragraph_format.space_before = Pt(0)
    p_blind.paragraph_format.space_after = Pt(14)
    p_blind.paragraph_format.line_spacing = 1.0
    p_blind.paragraph_format.first_line_indent = Mm(0)
    r_blind = p_blind.add_run('"กรุณาอย่าใส่ชื่อผู้แต่ง"')
    set_run_font(r_blind, name='TH SarabunPSK', size=14, bold=True, color=(220, 38, 38))

    # =========================================================================
    # SECTION 2: 2 COLUMNS (82 mm each, 6 mm gap)
    # =========================================================================
    sec2 = doc.add_section(docx.enum.section.WD_SECTION.CONTINUOUS)
    sec2.top_margin = Mm(30)
    sec2.bottom_margin = Mm(25)
    sec2.left_margin = Mm(20)
    sec2.right_margin = Mm(20)
    sec2.header_distance = Mm(15)
    sec2.footer_distance = Mm(15)

    sectPr = sec2._sectPr
    cols = sectPr.xpath('./w:cols')
    if cols:
        cols[0].set(qn('w:num'), '2')
        cols[0].set(qn('w:space'), '340') # 6 mm in twips
    else:
        c = OxmlElement('w:cols')
        c.set(qn('w:num'), '2')
        c.set(qn('w:space'), '340')
        sectPr.append(c)

    sec2.header.is_linked_to_previous = True
    sec2.footer.is_linked_to_previous = True

    # -------------------------------------------------------------------------
    # ABSTRACT THAI
    # -------------------------------------------------------------------------
    p_ab_th_title = doc.add_paragraph()
    p_ab_th_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ab_th_title.paragraph_format.space_before = Pt(0)
    p_ab_th_title.paragraph_format.space_after = Pt(2)
    p_ab_th_title.paragraph_format.first_line_indent = Mm(0)
    r_ab_th_title = p_ab_th_title.add_run('บทคัดย่อ')
    set_run_font(r_ab_th_title, name='TH SarabunPSK', size=14, bold=True)

    add_p(doc, 'การฝึกปฏิบัติงานสหกิจศึกษาเป็นกระบวนการเรียนรู้เชิงบูรณาการที่สำคัญของนิสิตคณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ โดยมีกระบวนการตรวจนิเทศของอาจารย์ที่ปรึกษาเป็นหัวใจสำคัญในการติดตามและประเมินผล อย่างไรก็ตาม ในระบบการดำเนินงานเดิมพบปัญหาความล่าช้าในการจัดการเอกสารแบบฟอร์มสหกิจศึกษา เอกสารสูญหาย ความคลาดเคลื่อนในการนัดหมายลงพื้นที่ และการขาดหลักฐานเชิงประจักษ์ในการยืนยันว่าอาจารย์ได้ลงพื้นที่ตรวจนิเทศ ณ สถานประกอบการจริง เพื่อแก้ไขปัญหาดังกล่าว โครงงานวิจัยนี้จึงได้พัฒนาเว็บแอปพลิเคชันแบบตอบสนอง (Responsive Web Application) ครอบคลุมการทำงาน 3 บทบาท ได้แก่ นิสิตสหกิจศึกษา อาจารย์นิเทศ และผู้ดูแลระบบ โดยบูรณาการเทคโนโลยีกล้องสดสแกน Dynamic QR Code แบบเรียลไทม์ร่วมกับ Geolocation API และสูตรคำนวณระยะทาง Haversine Formula เพื่อจำกัดรัศมีการเช็คอินนิเทศไม่เกิน 500 เมตร ป้องกันการเช็คอินนอกสถานที่จริง พร้อมทั้งพัฒนาระบบคลังภาพถ่ายหลักฐานการนิเทศสองชั้น ระบบตรวจรับและข้อคิดเห็นเอกสารรายฉบับ ระบบนำเข้าข้อมูลนิสิตผ่านสเปรดชีต Excel พร้อมตารางพรีวิวแบบเต็มจอ 100% และระบบยืนยันตัวตนสองชั้น (2FA) ด้วยรหัส OTP 8 หลักผ่านอีเมลมหาวิทยาลัย ผลการประเมินการทำงานพบว่าระบบสามารถทำงานได้อย่างถูกต้องสมบูรณ์ตามเกณฑ์ประกันคุณภาพการศึกษา และพร้อมสำหรับการนำไปประยุกต์ใช้งานจริงในระดับสถาบันต่อไป',
          space_after=4)

    p_kw_th = doc.add_paragraph()
    p_kw_th.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw_th.paragraph_format.space_before = Pt(2)
    p_kw_th.paragraph_format.space_after = Pt(6)
    p_kw_th.paragraph_format.first_line_indent = Mm(0)
    r_kw_lbl = p_kw_th.add_run('คำสำคัญ -- ')
    set_run_font(r_kw_lbl, name='TH SarabunPSK', size=14, bold=True)
    r_kw_txt = p_kw_th.add_run('สหกิจศึกษา, การตรวจนิเทศ, Geofencing, คิวอาร์โค้ดแบบพลวัต, เว็บแอปพลิเคชัน')
    set_run_font(r_kw_txt, name='TH SarabunPSK', size=14, bold=False)

    # -------------------------------------------------------------------------
    # ABSTRACT ENGLISH
    # -------------------------------------------------------------------------
    p_ab_en_title = doc.add_paragraph()
    p_ab_en_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ab_en_title.paragraph_format.space_before = Pt(4)
    p_ab_en_title.paragraph_format.space_after = Pt(2)
    p_ab_en_title.paragraph_format.first_line_indent = Mm(0)
    r_ab_en_title = p_ab_en_title.add_run('ABSTRACT')
    set_run_font(r_ab_en_title, name='TH SarabunPSK', size=14, bold=True)

    add_p(doc, 'Cooperative education (co-op) is a vital integrated learning process for students in the Faculty of Science at Kasetsart University. A core component of this process is the on-site supervision conducted by faculty advisors, which serves to monitor and evaluate student performance. However, the existing operational workflow has faced several critical challenges, including delays in processing co-op documentation, paperwork loss, scheduling conflicts for site visits, and a lack of empirical evidence to verify that faculty advisors actually visited the designated workplaces in accordance with established quality standards. To address these issues, this research project has designed and implemented a responsive web application that comprehensively supports three distinct user roles: co-op students, faculty supervisors, and system administrators. The platform integrates real-time dynamic QR code scanning via device camera with the W3C Geolocation API and the Haversine distance formula to enforce an automated Geofencing mechanism, restricting valid supervision check-ins to within a 500-meter radius of the registered enterprise coordinates. Furthermore, the application provides a two-tier photo verification repository, a granular document review workflow with per-file feedback mechanisms, a full-width 100% data preview module for batch student onboarding via Microsoft Excel, and a two-factor authentication (2FA) protocol requiring 8-digit OTP verification via institutional email accounts. Comprehensive system testing indicates that the platform operates with complete functional integrity and is fully prepared for faculty-wide operational deployment.',
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4, thai_distribute=False)

    p_kw_en = doc.add_paragraph()
    p_kw_en.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw_en.paragraph_format.space_before = Pt(2)
    p_kw_en.paragraph_format.space_after = Pt(8)
    p_kw_en.paragraph_format.first_line_indent = Mm(0)
    r_kw_en_lbl = p_kw_en.add_run('Keywords -- ')
    set_run_font(r_kw_en_lbl, name='TH SarabunPSK', size=14, bold=True)
    r_kw_en_txt = p_kw_en.add_run('Cooperative Education, Supervision Tracking, Geofencing, Dynamic QR Code, Web Application')
    set_run_font(r_kw_en_txt, name='TH SarabunPSK', size=14, bold=False)

    # -------------------------------------------------------------------------
    # 1. บทนำ (INTRODUCTION)
    # -------------------------------------------------------------------------
    add_main_heading(doc, '1. บทนำ')

    add_p(doc, 'หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ มุ่งเน้นให้นิสิตได้นำองค์ความรู้เชิงทฤษฎี ทั้งด้านการพัฒนาซอฟต์แวร์ การจัดการฐานข้อมูล สถาปัตยกรรมระบบสารสนเทศ และการวิเคราะห์อัลกอริทึม ไปประยุกต์ใช้ในการปฏิบัติงานจริง ณ สถานประกอบการ ผ่านกระบวนการสหกิจศึกษา (Cooperative Education) ซึ่งถือเป็นกลไกสำคัญในการเตรียมความพร้อมสู่การประกอบวิชาชีพในอุตสาหกรรมเทคโนโลยีดิจิทัล')

    add_p(doc, 'ในกระบวนการดำเนินงานสหกิจศึกษา การออกตรวจนิเทศของอาจารย์ที่ปรึกษา ณ สถานประกอบการ ถือเป็นขั้นตอนสำคัญอย่างยิ่งในการติดตามความก้าวหน้า ให้คำแนะนำด้านวิชาการ ประเมินผลการเรียนรู้ของนิสิตร่วมกับพนักงานพี่เลี้ยง ตลอดจนรับฟังความคิดเห็นจากสถานประกอบการเพื่อนำมาปรับปรุงหลักสูตรการเรียนการสอน อย่างไรก็ตาม จากการศึกษาสภาพปัญหาและข้อจำกัดในกระบวนการนิเทศเดิม พบประเด็นปัญหาสำคัญ 4 ด้าน ดังนี้:')

    add_p(doc, '1) ปัญหาการจัดการเอกสารและความล่าช้า: การประเมินผลและการส่งเอกสารแบบฟอร์มสหกิจศึกษา (FORM-00 ถึง FORM-11) ยังคงใช้เอกสารกระดาษหรือไฟล์ที่ส่งผ่านช่องทางไม่เป็นทางการ เช่น อีเมลส่วนตัวหรือแอปพลิเคชันสนทนา ส่งผลให้เอกสารสูญหาย ไม่สามารถตรวจสอบประวัติการส่งได้อย่างเป็นระบบ และอาจารย์นิเทศต้องเสียเวลาในการตรวจรับเอกสารที่ซ้ำซ้อน')

    add_p(doc, '2) ความยากลำบากในการติดตามความคืบหน้ารายบุคคลและการแยกหมู่เรียน: แต่ละภาคการศึกษามีนิสิตออกฝึกงานจำนวนมากและแบ่งตามหมู่เรียนจริง (หมู่ 700 ภาคปกติ และหมู่ 800 ภาคพิเศษ) ซึ่งระบบเดิมไม่มีการรวมศูนย์ข้อมูล ทำให้อาจารย์และผู้บริหารไม่สามารถมองเห็นภาพรวมสถิติการออกนิเทศแบบเรียลไทม์')

    add_p(doc, '3) ปัญหาการนัดหมายลงพื้นที่คลาดเคลื่อน: ขาดระบบปฏิทินกลางที่แสดงผลนัดหมายตรงกันระหว่างอาจารย์ นิสิต และสถานประกอบการ ทำให้ตารางเวลาซ้ำซ้อนหรือไม่ตรงกัน ส่งผลต่อประสิทธิภาพในการวางแผนการเดินทาง')

    add_p(doc, '4) การขาดพยานหลักฐานเชิงประจักษ์ในการลงพื้นที่จริง: ขาดเครื่องมือทางเทคโนโลยีที่ช่วยยืนยันและตรวจสอบได้อย่างโปร่งใสว่าอาจารย์ได้ลงพื้นที่ตรวจนิเทศ ณ สถานประกอบการจริงตามเกณฑ์มาตรฐานประกันคุณภาพการศึกษาของมหาวิทยาลัย')

    add_sub_heading(doc, '1.1 วัตถุประสงค์ของโครงงาน')
    add_p(doc, '1) เพื่อศึกษา ออกแบบ และพัฒนาระบบเว็บแอปพลิเคชันบริหารจัดการการตรวจนิเทศสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ที่รองรับการทำงาน 3 บทบาท (นิสิตสหกิจศึกษา, อาจารย์นิเทศ, ผู้ดูแลระบบ)')
    add_p(doc, '2) เพื่อพัฒนากลไกตรวจสอบและยืนยันการลงพื้นที่นิเทศจริง ณ สถานประกอบการ ด้วยการผสานเทคโนโลยี Live Camera Dynamic QR Code Scanner และการตรวจสอบพิกัดภูมิศาสตร์ร่วมกับสูตร Haversine Formula เพื่อจำกัดรัศมีการเช็คอินไม่เกิน 500 เมตร')
    add_p(doc, '3) เพื่อพัฒนาระบบคลังเอกสารแบบฟอร์มสหกิจศึกษา รองรับการอัปโหลดไฟล์ การตรวจรับ และส่งคืนข้อคิดเห็นสะท้อนกลับแบบรายฉบับ พร้อมระบบบันทึกและจัดเก็บภาพถ่ายหลักฐานการลงพื้นที่นิเทศสองชั้น')
    add_p(doc, '4) เพื่อพัฒนาระบบบริหารจัดการข้อมูลนิสิตผ่านการนำเข้าไฟล์ Excel พร้อมตารางพรีวิวแบบเต็มจอ 100% และระบบประมวลผลส่งออกรายงานสรุปผลการนิเทศในรูปแบบ Excel และ PDF')

    add_sub_heading(doc, '1.2 ขอบเขตของโครงงาน')
    add_p(doc, 'โครงงานนี้ครอบคลุมการพัฒนาระบบสารสนเทศที่ทำงานในรูปแบบ Responsive Web Application โดยแบ่งขอบเขตตามบทบาทผู้ใช้งาน ดังนี้:')
    add_p(doc, '• นิสิตสหกิจศึกษา: สามารถลงทะเบียนเข้าสู่ระบบด้วยอีเมลมหาวิทยาลัย (@ku.th) พร้อมยืนยันตัวตนด้วยรหัส OTP 8 หลัก, แสดงบัตรประจำตัว Dynamic QR Code, ดาวน์โหลดแบบฟอร์มเปล่า, อัปโหลดเอกสารรายงาน, ตรวจสอบผลการอนุมัติและข้อคิดเห็นสะท้อนกลับแบบรายฉบับ, ตรวจสอบปฏิทินนัดหมาย, และตั้งค่าพิกัด GPS สถานประกอบการของตนเอง')
    add_p(doc, '• อาจารย์นิเทศ: สามารถจัดการห้องเรียนแยกหมู่ (หมู่ 700 ภาคปกติ, หมู่ 800 ภาคพิเศษ), ตรวจรับและตีกลับเอกสารพร้อมระบุข้อคิดเห็นรายฉบับ, วางแผนนัดหมายลงพื้นที่ผ่านปฏิทินกลาง, เปิดกล้องสดสแกน QR Code เพื่อเช็คอินพิกัด GPS พร้อมระบบตรวจสอบรัศมี 500 เมตร, อัปโหลดภาพถ่ายหลักฐานการนิเทศสองชั้น, และบันทึกคะแนนประเมินผล')
    add_p(doc, '• ผู้ดูแลระบบ (Admin): สามารถติดตามแดชบอร์ดสถิตินิเทศแบบเรียลไทม์, กรองข้อมูลตามภาคการศึกษาและหมู่เรียน, นำเข้าข้อมูลนิสิตผ่านไฟล์ Excel พร้อมพรีวิวตาราง 100% ก่อนบันทึก, ระบุพิกัดสถานประกอบการ, และส่งออกรายงานสรุปในรูปแบบ Excel และ PDF')

    # -------------------------------------------------------------------------
    # 2. งานวิจัยและทฤษฎีที่เกี่ยวข้อง (RELATED WORK)
    # -------------------------------------------------------------------------
    add_main_heading(doc, '2. งานวิจัยและทฤษฎีที่เกี่ยวข้อง')

    add_sub_heading(doc, '2.1 การศึกษาแอปพลิเคชันและระบบที่เกี่ยวข้อง')
    add_p(doc, 'จากการศึกษาแพลตฟอร์มการจัดการการเรียนรู้ออนไลน์ชั้นนำ ได้แก่ Google Classroom [1] พบว่ามีจุดเด่นในการจัดการกลุ่มผู้เรียนในลักษณะห้องเรียนจำลอง ช่วยจัดหมวดหมู่งานและติดตามสถานะการส่งงานรายบุคคลได้อย่างเป็นระเบียบ และจากการศึกษา Microsoft Teams [2] พบว่ามีจุดเด่นด้านระบบปฏิทินนัดหมายกลาง (Calendar Integration) ที่อัปเดตตารางเวลาแบบเรียลไทม์ระหว่างผู้ส่งและผู้รับนัดหมาย ช่วยลดความซ้ำซ้อนของการจองเวลา')

    add_p(doc, 'อย่างไรก็ดี แพลตฟอร์ม LMS ทั่วไปไม่ได้ถูกออกแบบมาเฉพาะสำหรับงานนิเทศสหกิจศึกษา ขาดกลไกการตรวจสอบพิกัดทางภูมิศาสตร์ของสถานประกอบการ ขาดระบบการตรวจสอบเอกสารราชการที่มีลำดับขั้นแบบเฉพาะ (คู-01 ถึง คู-11) และไม่มีกลไกยืนยันการลงพื้นที่จริง คณะผู้วิจัยจึงได้นำแนวคิดการแยกห้องเรียนและปฏิทินกลางมาประยุกต์ใช้ พร้อมพัฒนาส่วนขยายเฉพาะทางขึ้นมาเสริมความสมบูรณ์')

    add_sub_heading(doc, '2.2 การยืนยันตัวตนด้วยรหัสตอบสนองเร็ว (QR Code)')
    add_p(doc, 'การประยุกต์ใช้ QR Code สำหรับระบบบันทึกเวลาและการยืนยันตัวตน (Smart Attendance) ได้รับความนิยมอย่างแพร่หลายในปัจจุบัน [3] เนื่องจากมีความสะดวก รวดเร็ว และประมวลผลได้โดยตรงผ่านกล้องสมาร์ตโฟน อย่างไรก็ตาม การใช้รหัสคิวอาร์แบบคงที่ (Static QR Code) มีความเสี่ยงต่อการถูกคัดลอกหรือส่งต่อภาพถ่ายเพื่อทุจริตเช็คอินแทนกัน โครงงานนี้จึงได้ออกแบบรหัสคิวอาร์แบบพลวัต (Dynamic QR Code) ที่ผูกติดกับรหัสนิสิตและเซสชันเวลาการใช้งาน พร้อมทั้งทำงานร่วมกับไลบรารี jsQR [10] ในการประมวลผลภาพวิดีโอสดผ่าน HTML5 Canvas บนอุปกรณ์ของอาจารย์โดยตรง')

    add_sub_heading(doc, '2.3 การกำหนดขอบเขตพิกัดทางภูมิศาสตร์และสมการฮาเวอร์ซีน')
    add_p(doc, 'ระบบสารสนเทศตามตำแหน่งทางภูมิศาสตร์ (Location-Based Services) ร่วมกับการสร้างรัศมีจำกัดพื้นที่เสมือน (Geofencing) เป็นระเบียบวิธีที่ได้รับการยอมรับในการควบคุมและตรวจสอบการปฏิบัติงานภาคสนาม [4] ในโครงงานนี้ การคำนวณระยะห่างระหว่างตำแหน่งปัจจุบันของอาจารย์นิเทศ (Latitude1, Longitude1) ที่ได้จาก W3C Geolocation API กับตำแหน่งที่ตั้งสถานประกอบการของนิสิต (Latitude2, Longitude2) ที่จัดเก็บในฐานข้อมูล ได้ประยุกต์ใช้สมการฮาเวอร์ซีน (Haversine Formula) ซึ่งมีความแม่นยำสูงสำหรับการคำนวณระยะทางบนพื้นผิวโลกทรงกลม ดังแสดงในสมการที่ (1):')

    add_equation(doc, 'd = 2R · arcsin(√(sin²(Δφ/2) + cos(φ₁)cos(φ₂)sin²(Δλ/2)))', '(1)')

    add_p(doc, 'โดยที่ R คือรัศมีเฉลี่ยของโลก (ประมาณ 6,371,000 เมตร), φ₁ และ φ₂ คือละติจูดของจุดที่ 1 และจุดที่ 2 ในหน่วยเรเดียน, Δφ = φ₂ - φ₁ คือผลต่างของละติจูด, และ Δλ = λ₂ - λ₁ คือผลต่างของลองจิจูด ระบบกำหนดเกณฑ์การเช็คอินที่ระยะ d ≤ 500 เมตร เพื่อรองรับค่าความคลาดเคลื่อนของสัญญาณ GPS ในพื้นที่เขตเมืองและอาคารสูง')

    add_sub_heading(doc, '2.4 สถาปัตยกรรม SPA และเทคโนโลยีพัฒนาเว็บ')
    add_p(doc, 'ระบบพัฒนาขึ้นบนสถาปัตยกรรม Single Page Application (SPA) โดยใช้ Pure Vanilla JavaScript (ES6+), HTML5 [6], และ CSS3 [7] ภายใต้แนวคิด Responsive Web Design เพื่อให้สามารถแสดงผลและใช้งานได้อย่างราบรื่นทั้งบนคอมพิวเตอร์และสมาร์ตโฟน โดยไม่ต้องพึ่งพาเฟรมเวิร์กขนาดใหญ่ ช่วยลดขนาดไฟล์และเพิ่มความเร็วในการประมวลผล')

    add_p(doc, 'สำหรับส่วนหลังบ้านและฐานข้อมูล ระบบใช้บริการ Supabase [9] ซึ่งเป็น Backend-as-a-Service บนฐานข้อมูลเชิงสัมพันธ์ PostgreSQL 15 มีฟังก์ชัน Row Level Security (RLS) และการรับส่งข้อมูลผ่าน RESTful API ร่วมกับไลบรารี SheetJS (xlsx) [11] สำหรับการประมวลผลไฟล์สเปรดชีต Excel บนเว็บเบราว์เซอร์')

    # -------------------------------------------------------------------------
    # 3. การออกแบบและสถาปัตยกรรมระบบ (SYSTEM DESIGN)
    # -------------------------------------------------------------------------
    add_main_heading(doc, '3. การออกแบบและสถาปัตยกรรมระบบ')

    add_sub_heading(doc, '3.1 สถาปัตยกรรมระบบภาพรวม')
    add_p(doc, 'สถาปัตยกรรมของระบบแบ่งออกเป็น 3 ระดับ (Three-Tier Architecture) ได้แก่ 1) Client Tier: ส่วนติดต่อผู้ใช้แบบ SPA ทำหน้าที่ประมวลผลการแสดงผล การสแกนรหัสผ่านกล้องสด การดึงพิกัด GPS และการคำนวณ Geofencing 2) Cloud Service Tier: ระบบความปลอดภัยและบริการยืนยันตัวตน (Authentication & Authorization) ผ่านระบบ OTP และบริการ Supabase API 3) Data Tier: ฐานข้อมูลเชิงสัมพันธ์ PostgreSQL 15 และคลังจัดเก็บไฟล์ (Cloud Storage) สำหรับเอกสารและภาพถ่ายหลักฐาน')

    add_sub_heading(doc, '3.2 กระบวนการทำงานของระบบ (Workflows)')
    add_p(doc, 'ระบบได้รับการออกแบบโดยยึดผู้ใช้งานเป็นศูนย์กลาง แบ่งขั้นตอนการทำงานออกเป็น 3 บทบาทอย่างชัดเจน ดังนี้:')

    add_p(doc, '3.2.1 ขั้นตอนการทำงานของนิสิตสหกิจศึกษา: เริ่มจากการเข้าสู่ระบบด้วยอีเมลเคยู (@ku.th) ยืนยันตัวตนด้วยรหัส OTP 8 หลัก และเปลี่ยนรหัสผ่านแรกเข้าตามนโยบายความปลอดภัย จากนั้นนิสิตเข้าสู่แดชบอร์ดเพื่อตรวจสอบสถานะการส่งเอกสาร ดาวน์โหลดแบบฟอร์มทางการ (FORM-00 ถึง FORM-11) อัปโหลดเอกสารส่งให้อาจารย์ตรวจ ตรวจสอบข้อคิดเห็นสะท้อนกลับ กำหนดพิกัด GPS ของสถานประกอบการ และเปิดแสดงบัตร Dynamic QR Code ให้อาจารย์สแกนเมื่อถึงวันตรวจนิเทศ')

    add_p(doc, '3.2.2 ขั้นตอนการทำงานของอาจารย์นิเทศ: อาจารย์เข้าสู่ระบบ เลือกห้องเรียนตามหมู่เรียนที่รับผิดชอบ (หมู่ 700 หรือหมู่ 800) ตรวจสอบรายชื่อนิสิตและสถานประกอบการ ตรวจรับเอกสารรายงานสหกิจศึกษาพร้อมให้ข้อคิดเห็นสะท้อนกลับรายฉบับ วางแผนนัดหมายลงพื้นที่ผ่านปฏิทินกลาง และเมื่อเดินทางถึงสถานประกอบการจริง อาจารย์จะเปิดเมนูกล้องสดบนสมาร์ตโฟนเพื่อสแกน QR Code ของนิสิต ระบบจะดึงพิกัด GPS ปัจจุบันและคำนวณระยะห่าง หากอยู่ภายในรัศมี 500 เมตร ระบบจะอนุญาตให้เช็คอินสำเร็จ จากนั้นอาจารย์จะอัปโหลดภาพถ่ายหลักฐานสองชั้นและบันทึกคะแนนประเมินผล')

    add_p(doc, '3.2.3 ขั้นตอนการทำงานของผู้ดูแลระบบ (Admin): ผู้ดูแลระบบเข้าสู่แดชบอร์ดส่วนกลางเพื่อติดตามภาพรวมสถิติการนิเทศ จัดการนำเข้าข้อมูลรายชื่อนิสิตและอาจารย์ผ่านไฟล์ Excel พร้อมระบบพรีวิวขนาดใหญ่ 100% ตรวจสอบความถูกต้องของข้อมูลและพิกัดสถานประกอบการ จัดการสิทธิ์ผู้ใช้งาน และประมวลผลส่งออกรายงานสรุปผลการนิเทศในรูปแบบ Excel (.xlsx) และ PDF (.pdf) เสนอต่อคณะต่อไป')

    # ภาพที่ 1: Workflow ภาพรวม
    add_figure(doc, r'screenshots\workflows\workflow_student.png',
               'ภาพ 1 แผนผังขั้นตอนการทำงานของนิสิตสหกิจศึกษา (Student Workflow)')

    add_sub_heading(doc, '3.3 กลไกความปลอดภัยและการยืนยันตัวตนสองชั้น')
    add_p(doc, 'เพื่อปกป้องข้อมูลส่วนบุคคลและป้องกันการเข้าถึงโดยไม่ได้รับอนุญาต ระบบได้วางมาตรการความปลอดภัยในระดับสูง ดังนี้:')
    add_p(doc, '1) Two-Factor Authentication (2FA): ทุกการเข้าสู่ระบบครั้งแรกหรือการใช้งานบนอุปกรณ์ใหม่ ระบบจะส่งรหัสผ่านใช้ครั้งเดียว (One-Time Password: OTP) ความยาว 8 หลัก ไปยังกล่องข้อความอีเมลมหาวิทยาลัยของผู้ใช้ โดยรหัสมีอายุการใช้งาน 5 นาที')
    add_p(doc, '2) Password Complexity Policy: กำหนดให้นิสิตเปลี่ยนรหัสผ่านแรกเข้าตามเกณฑ์ความปลอดภัย 4 ข้อ ได้แก่ ความยาวไม่น้อยกว่า 8 ตัวอักษร, ประกอบด้วยตัวอักษรพิมพ์ใหญ่, ตัวอักษรพิมพ์เล็ก, ตัวเลข และอักขระพิเศษ')
    add_p(doc, '3) Client-Side Authentication Guard: ตรวจสอบสถานะ Session Token และสิทธิ์ของผู้ใช้งานในทุกการเปลี่ยนมุมมองหน้าจอ เพื่อป้องกันการพิมพ์ URL ข้ามขั้นตอน')

    add_figure(doc, r'docs\screenshots\01_login_page.png',
               'ภาพ 2 หน้าจอเข้าสู่ระบบและกลไกความปลอดภัยยืนยันตัวตนด้วยรหัส OTP 8 หลัก')

    add_sub_heading(doc, '3.4 กลไกการตรวจนิเทศจริงด้วย Dynamic QR และ Geofencing')
    add_p(doc, 'หัวใจสำคัญในการสร้างพยานหลักฐานเชิงประจักษ์ คือการผสานกลไกการสแกนรหัสคิวอาร์แบบเรียลไทม์เข้ากับการตรวจสอบพิกัดภูมิศาสตร์ โดยมีขั้นตอนการทำงานดังนี้:')
    add_p(doc, '1) นิสิตเปิดแสดงบัตร Dynamic QR Code บนหน้าจอสมาร์ตโฟน ซึ่งมีข้อมูลรหัสนิสิตและโทเคนเซสชันที่มีการเข้ารหัส')
    add_p(doc, '2) อาจารย์นิเทศเปิดฟังก์ชัน Live Camera Scanner บนเว็บแอปพลิเคชัน ไลบรารี jsQR จะถอดรหัสข้อมูลนิสิตทันทีที่กล้องตรวจจับภาพได้')
    add_p(doc, '3) ระบบทำการร้องขอพิกัด GPS ปัจจุบันของอาจารย์ผ่าน W3C Geolocation API และดึงค่าพิกัดสถานประกอบการของนิสิตจากฐานข้อมูล Supabase')
    add_p(doc, '4) อัลกอริทึมของระบบนำค่าพิกัดทั้งสองจุดมาคำนวณระยะห่างด้วยสมการฮาเวอร์ซีน (Haversine Formula) หากระยะห่าง d ≤ 500 เมตร ระบบจะแสดง "การ์ดเขียว (Verified)" และบันทึกประวัติการเช็คอินพร้อมประทับเวลา (Timestamp) แต่หากระยะห่าง d > 500 เมตร ระบบจะแสดง "การ์ดแดง (Rejected)" และปฏิเสธการเช็คอินทันทีเพื่อป้องกันการทุจริต')

    add_figure(doc, r'docs\screenshots\11_qr_camera_scanner.png',
               'ภาพ 3 ระบบกล้องสด Live Camera Scanner สำหรับอาจารย์สแกน Dynamic QR Code ของนิสิต')

    add_figure(doc, r'docs\screenshots\14_checkin_success_in_radius.png',
               'ภาพ 4 ผลการเช็คอินสำเร็จในรัศมีปลอดภัย 500 เมตร (การ์ดเขียว) พร้อมแสดงระยะห่างจริง')

    add_sub_heading(doc, '3.5 การออกแบบฐานข้อมูลเชิงสัมพันธ์')
    add_p(doc, 'ฐานข้อมูลได้รับการออกแบบเชิงสัมพันธ์บน PostgreSQL ประกอบด้วย 7 ตารางหลักที่มีความสัมพันธ์กันอย่างสมบูรณ์ ดังแสดงรายละเอียดในตารางที่ 1:')

    # -------------------------------------------------------------------------
    # ตารางที่ 1: Schema ฐานข้อมูล
    # -------------------------------------------------------------------------
    p_t1 = doc.add_paragraph()
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t1.paragraph_format.space_before = Pt(8)
    p_t1.paragraph_format.space_after = Pt(2)
    p_t1.paragraph_format.first_line_indent = Mm(0)
    p_t1.paragraph_format.keep_with_next = True
    r_t1 = p_t1.add_run('ตาราง 1 โครงสร้างตารางข้อมูลหลักของระบบ (Database Schema)')
    set_run_font(r_t1, name='TH SarabunPSK', size=12, bold=True)

    table1 = doc.add_table(rows=8, cols=4)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1_headers = ['ชื่อตาราง', 'คีย์หลัก (PK)', 'คีย์นอก (FK)', 'หน้าที่และคำอธิบาย']
    t1_data = [
        ['users', 'id (UUID)', '-', 'จัดเก็บบัญชีผู้ใช้ อีเมล รหัสผ่าน และบทบาท (Role)'],
        ['advisors', 'id (UUID)', 'user_id', 'ข้อมูลอาจารย์นิเทศและหมู่เรียนที่รับผิดชอบ'],
        ['students', 'id (UUID)', 'user_id, adv_id', 'ข้อมูลนิสิต หมู่เรียน และพิกัดสถานประกอบการ'],
        ['coop_docs', 'id (UUID)', 'student_id', 'ประวัติการส่งเอกสารแบบฟอร์ม คู-00 ถึง คู-11'],
        ['appointments', 'id (UUID)', 'adv_id, std_id', 'ตารางการนัดหมายลงพื้นที่ตรวจนิเทศบนปฏิทิน'],
        ['supervision_photos', 'id (UUID)', 'student_id', 'คลังภาพถ่ายหลักฐานการนิเทศสองชั้น'],
        ['notifications', 'id (UUID)', 'user_id', 'ประวัติการแจ้งเตือนและการจัดส่งรหัส OTP 8 หลัก']
    ]
    # Header row
    hdr_cells = table1.rows[0].cells
    for i, h in enumerate(t1_headers):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], 'F1F5F9')
        set_cell_margins(hdr_cells[i], top=60, bottom=60, left=80, right=80)
        set_cell_borders(hdr_cells[i], top={'sz': 6, 'val': 'single', 'color': 'CBD5E1'},
                                       bottom={'sz': 6, 'val': 'single', 'color': 'CBD5E1'})
        p_c = hdr_cells[i].paragraphs[0]
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.paragraph_format.first_line_indent = Mm(0)
        set_run_font(p_c.runs[0], name='TH SarabunPSK', size=11, bold=True)

    col_w = [Mm(20), Mm(16), Mm(18), Mm(28)]
    for r_idx, row_data in enumerate(t1_data):
        row_cells = table1.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = val
            set_cell_margins(row_cells[c_idx], top=40, bottom=40, left=60, right=60)
            set_cell_borders(row_cells[c_idx], bottom={'sz': 4, 'val': 'single', 'color': 'E2E8F0'})
            p_c = row_cells[c_idx].paragraphs[0]
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx < 3 else WD_ALIGN_PARAGRAPH.LEFT
            p_c.paragraph_format.first_line_indent = Mm(0)
            set_run_font(p_c.runs[0], name='TH SarabunPSK', size=10, bold=False)

    for row in table1.rows:
        for idx, w in enumerate(col_w):
            row.cells[idx].width = w

    # -------------------------------------------------------------------------
    # 4. ผลการดำเนินงานและการทดสอบระบบ (RESULTS & TESTING)
    # -------------------------------------------------------------------------
    add_main_heading(doc, '4. ผลการดำเนินงานและการทดสอบระบบ')

    add_sub_heading(doc, '4.1 ส่วนต่อประสานผู้ใช้งานและการทำงานจริง')
    add_p(doc, 'ระบบได้รับการพัฒนาจนเสร็จสมบูรณ์และเปิดให้ทดสอบการทำงานจริง โดยมีผลการดำเนินงานในแต่ละส่วนต่อประสานผู้ใช้งาน ดังนี้:')

    add_p(doc, '1) ส่วนนิสิตสหกิจศึกษา: หน้าแดชบอร์ดนำเสนอข้อมูลสถานะแบบรวมศูนย์ นิสิตสามารถดาวน์โหลดเอกสารแบบฟอร์มมาตรฐาน กรอกข้อมูล และอัปโหลดไฟล์รายงาน (PDF หรือ Word) เข้าสู่ระบบ พร้อมทั้งตรวจสอบผลการตรวจรับและข้อคิดเห็นจากอาจารย์แบบเจาะจงรายฉบับ นอกจากนี้ นิสิตยังสามารถตรวจสอบพิกัดและปักหมุดตำแหน่งที่ตั้งสถานประกอบการของตนเองเพื่อใช้เป็นข้อมูลอ้างอิงในการคำนวณ Geofencing')

    add_p(doc, '2) ส่วนอาจารย์นิเทศ: หน้าจอห้องเรียนแยกตามหมู่เรียนจริง (หมู่ 700 ภาคปกติ และหมู่ 800 ภาคพิเศษ) ช่วยให้อาจารย์บริหารจัดการนิสิตในความดูแลได้อย่างเป็นสัดส่วน ในส่วนการตรวจเอกสาร อาจารย์สามารถเปิดดูไฟล์เอกสารพร้อมระบุผลการตรวจรับ (อนุมัติ หรือ ตีกลับแก้ไข) และพิมพ์ข้อคิดเห็นสะท้อนกลับ (Feedback) ให้นิสิตปรับปรุงได้อย่างสะดวกรวดเร็ว เมื่อลงพื้นที่ อาจารย์เปิดกล้องสแกน Dynamic QR Code เพื่อเช็คอินในรัศมี 500 เมตร และอัปโหลดภาพถ่ายหลักฐานสองชั้น (ภาพถ่ายร่วมกับนิสิตและภาพถ่ายร่วมกับพี่เลี้ยงสถานประกอบการ) เข้าสู่คลังภาพหลักฐาน')

    add_figure(doc, r'docs\screenshots\06_supervision_evidence.png',
               'ภาพ 5 ระบบตรวจรับเอกสารสหกิจศึกษารายฉบับพร้อมระบบข้อคิดเห็นสะท้อนกลับ (Feedback)')

    add_p(doc, '3) ส่วนผู้ดูแลระบบ: แดชบอร์ดนำเสนอสถิติความก้าวหน้าการนิเทศภาพรวมของคณะ ระบบนำเข้าข้อมูลรายชื่อนิสิตผ่านสเปรดชีต Excel มาพร้อมฟีเจอร์พรีวิวตารางข้อมูลขนาดใหญ่เต็มจอ 100% (Full-Width Modal Preview) ซึ่งแสดงผลข้อมูลครบทั้ง 7 คอลัมน์หลัก ช่วยให้ผู้ดูแลระบบตรวจสอบความถูกต้องของข้อมูลก่อนกดยืนยันบันทึกลงสู่ฐานข้อมูล Supabase และระบบสามารถส่งออกรายงานสรุปผลการนิเทศในรูปแบบ Excel และ PDF ได้ในคลิกเดียว')

    add_figure(doc, r'docs\screenshots\03_admin_excel_preview_pre_import.png',
               'ภาพ 6 ตารางพรีวิวข้อมูลนำเข้าไฟล์ Excel ขนาดใหญ่เต็มจอ 100% ก่อนกดยืนยันบันทึก')

    add_sub_heading(doc, '4.2 ผลการทดสอบการทำงานของระบบ (System Testing)')
    add_p(doc, 'การทดสอบระบบดำเนินการตามแนวทางการทดสอบซอฟต์แวร์แบบกล่องดำ (Black-box Testing) ครอบคลุมฟังก์ชันการทำงาน 18 กรณีทดสอบหลัก โดยจัดกลุ่มการทดสอบตามโมดูลการทำงาน 6 กลุ่ม ดังแสดงผลการประเมินในตารางที่ 2:')

    # -------------------------------------------------------------------------
    # ตารางที่ 2: ผลการทดสอบระบบ (จัดกลุ่มตามโมดูล)
    # -------------------------------------------------------------------------
    p_t2 = doc.add_paragraph()
    p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t2.paragraph_format.space_before = Pt(8)
    p_t2.paragraph_format.space_after = Pt(2)
    p_t2.paragraph_format.first_line_indent = Mm(0)
    p_t2.paragraph_format.keep_with_next = True
    r_t2 = p_t2.add_run('ตาราง 2 สรุปผลการทดสอบระบบตามกลุ่มฟังก์ชันการทำงาน (System Testing)')
    set_run_font(r_t2, name='TH SarabunPSK', size=12, bold=True)

    table2 = doc.add_table(rows=8, cols=3)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2_headers = ['กลุ่มฟังก์ชันการทำงาน', 'ขอบเขตและพฤติกรรมระบบที่ทดสอบ (18 กรณี)', 'ผลการทดสอบ']
    t2_data = [
        ['1. การยืนยันตัวตนและความปลอดภัย', 'ตรวจสอบอีเมล @ku.th, รหัส OTP 8 หลัก, และเกณฑ์รหัสผ่าน 4 ข้อ (3 กรณี)', 'ผ่าน (Pass) 100%'],
        ['2. การจัดการเอกสารสหกิจศึกษา', 'ดาวน์โหลดแบบฟอร์ม, อัปโหลดไฟล์, และตรวจรับพร้อม Feedback รายฉบับ (3 กรณี)', 'ผ่าน (Pass) 100%'],
        ['3. การจัดการห้องเรียนและงาน', 'แยกห้องเรียนหมู่ 700/800, สรุปสถานะเอกสาร, และระบบมอบหมายงาน (3 กรณี)', 'ผ่าน (Pass) 100%'],
        ['4. การลงพื้นที่ตรวจนิเทศจริง', 'ปฏิทินกลาง, กล้องสด Live Scanner, และ Geofencing รัศมี 500 เมตร (3 กรณี)', 'ผ่าน (Pass) 100%'],
        ['5. หลักฐานการนิเทศและการประเมิน', 'คลังภาพถ่ายหลักฐานสองชั้น และบันทึกคำนวณคะแนนนิเทศ (2 กรณี)', 'ผ่าน (Pass) 100%'],
        ['6. การจัดการข้อมูลและการรายงาน', 'พรีวิวตาราง Excel เต็มจอ 100%, นำเข้าข้อมูล, และส่งออกรายงาน (4 กรณี)', 'ผ่าน (Pass) 100%'],
        ['สรุปผลการทดสอบภาพรวม', 'ครอบคลุมการทำงานทุกโมดูลตามเกณฑ์มาตรฐานซอฟต์แวร์ รวม 18 กรณีทดสอบ', 'ผ่าน (Pass) 100%']
    ]
    hdr2_cells = table2.rows[0].cells
    for i, h in enumerate(t2_headers):
        hdr2_cells[i].text = h
        set_cell_background(hdr2_cells[i], 'F1F5F9')
        set_cell_margins(hdr2_cells[i], top=50, bottom=50, left=60, right=60)
        set_cell_borders(hdr2_cells[i], top={'sz': 6, 'val': 'single', 'color': 'CBD5E1'},
                                        bottom={'sz': 6, 'val': 'single', 'color': 'CBD5E1'})
        p_c = hdr2_cells[i].paragraphs[0]
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.paragraph_format.first_line_indent = Mm(0)
        set_run_font(p_c.runs[0], name='TH SarabunPSK', size=11, bold=True)

    col2_w = [Mm(28), Mm(38), Mm(16)]
    for r_idx, row_data in enumerate(t2_data):
        row_cells = table2.rows[r_idx + 1].cells
        is_summary = (r_idx == len(t2_data) - 1)
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = val
            if is_summary:
                set_cell_background(row_cells[c_idx], 'F8FAFC')
            set_cell_margins(row_cells[c_idx], top=35, bottom=35, left=50, right=50)
            set_cell_borders(row_cells[c_idx], bottom={'sz': 6 if is_summary else 4, 'val': 'single', 'color': '94A3B8' if is_summary else 'E2E8F0'})
            p_c = row_cells[c_idx].paragraphs[0]
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 2 or is_summary and c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            p_c.paragraph_format.first_line_indent = Mm(0)
            set_run_font(p_c.runs[0], name='TH SarabunPSK', size=9.5, bold=(c_idx == 2 or is_summary))

    for row in table2.rows:
        for idx, w in enumerate(col2_w):
            row.cells[idx].width = w

    add_sub_heading(doc, '4.3 การเปรียบเทียบกับกระบวนการนิเทศแบบเดิม')
    add_p(doc, 'เมื่อเปรียบเทียบกระบวนการทำงานระหว่างระบบเดิมกับเว็บแอปพลิเคชันที่พัฒนาขึ้น ดังแสดงในตารางที่ 3 พบว่าระบบสามารถยกระดับประสิทธิภาพการดำเนินงานได้อย่างมีนัยสำคัญ:')

    # -------------------------------------------------------------------------
    # ตารางที่ 3: Comparison
    # -------------------------------------------------------------------------
    p_t3 = doc.add_paragraph()
    p_t3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t3.paragraph_format.space_before = Pt(8)
    p_t3.paragraph_format.space_after = Pt(2)
    p_t3.paragraph_format.first_line_indent = Mm(0)
    p_t3.paragraph_format.keep_with_next = True
    r_t3 = p_t3.add_run('ตาราง 3 เปรียบเทียบกระบวนการทำงานเดิมกับระบบที่พัฒนาขึ้น')
    set_run_font(r_t3, name='TH SarabunPSK', size=12, bold=True)

    table3 = doc.add_table(rows=6, cols=3)
    table3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3_headers = ['มิติการเปรียบเทียบ', 'กระบวนการนิเทศแบบเดิม', 'ระบบเว็บแอปพลิเคชันที่พัฒนา']
    t3_data = [
        ['การจัดการเอกสาร', 'เอกสารกระดาษ ส่งผ่านอีเมล/แชต เสี่ยงสูญหาย', 'คลังเอกสารดิจิทัล ตรวจรับรายฉบับพร้อมประวัติ'],
        ['การยืนยันการลงพื้นที่', 'ลงลายมือชื่อในกระดาษ ขาดหลักฐานเชิงพิกัด', 'Dynamic QR + Geofencing รัศมี 500 ม. แบบเรียลไทม์'],
        ['การบริหารจัดการกลุ่ม', 'ไม่มีการแยกกลุ่มหมู่เรียนชัดเจน ติดตามยาก', 'แยกห้องเรียนหมู่ 700 (ปกติ) และ 800 (พิเศษ) ชัดเจน'],
        ['การนัดหมายลงพื้นที่', 'ประสานงานรายบุคคล ตารางเวลามักซ้อนทับ', 'ปฏิทินกลางแบบซิงโครไนซ์ มองเห็นตรงกัน 3 ฝ่าย'],
        ['การประมวลผลรายงาน', 'รวบรวมข้อมูลด้วยมือ ใช้เวลาหลายวัน', 'ประมวลผลอัตโนมัติ ส่งออก Excel และ PDF ทันที']
    ]
    hdr3_cells = table3.rows[0].cells
    for i, h in enumerate(t3_headers):
        hdr3_cells[i].text = h
        set_cell_background(hdr3_cells[i], 'F1F5F9')
        set_cell_margins(hdr3_cells[i], top=50, bottom=50, left=60, right=60)
        set_cell_borders(hdr3_cells[i], top={'sz': 6, 'val': 'single', 'color': 'CBD5E1'},
                                        bottom={'sz': 6, 'val': 'single', 'color': 'CBD5E1'})
        p_c = hdr3_cells[i].paragraphs[0]
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.paragraph_format.first_line_indent = Mm(0)
        set_run_font(p_c.runs[0], name='TH SarabunPSK', size=11, bold=True)

    col3_w = [Mm(22), Mm(30), Mm(30)]
    for r_idx, row_data in enumerate(t3_data):
        row_cells = table3.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = val
            set_cell_margins(row_cells[c_idx], top=35, bottom=35, left=50, right=50)
            set_cell_borders(row_cells[c_idx], bottom={'sz': 4, 'val': 'single', 'color': 'E2E8F0'})
            p_c = row_cells[c_idx].paragraphs[0]
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            p_c.paragraph_format.first_line_indent = Mm(0)
            set_run_font(p_c.runs[0], name='TH SarabunPSK', size=9.5, bold=(c_idx == 0))

    for row in table3.rows:
        for idx, w in enumerate(col3_w):
            row.cells[idx].width = w

    add_sub_heading(doc, '4.4 การวิเคราะห์ปัญหาทางเทคนิคและการแก้ปัญหาเชิงสถาปัตยกรรม')
    add_p(doc, 'ในระหว่างการพัฒนาระบบ คณะผู้วิจัยได้พบปัญหาทางเทคนิคจากการพัฒนาซอฟต์แวร์และการเชื่อมต่อระบบ ซึ่งได้ดำเนินการแก้ไขด้วยแนวทางเชิงสถาปัตยกรรม 6 ประการ ดังนี้:')

    add_p(doc, '1) การรักษาความปลอดภัยบนสถาปัตยกรรม SPA (Authentication Guard): ระบบพัฒนาด้วย Vanilla JavaScript SPA จึงพบปัญหาว่าผู้ใช้สามารถพิมพ์ URL ข้ามขั้นตอนการยืนยันตัวตนได้ คณะผู้พัฒนาจึงแก้ปัญหาด้วยการพัฒนาระบบ Auth Guard ตรวจสอบ Session Token และสถานะ OTP 8 หลักระดับ Client-side ทุกครั้งที่มีการเปลี่ยนหน้า หากไม่ถูกต้องจะบังคับรีไดเรกต์กลับสู่หน้าเข้าสู่ระบบทันที')

    add_p(doc, '2) ข้อจำกัดความปลอดภัยของเบราว์เซอร์ในการเข้าถึงฮาร์ดแวร์ (Secure Context): นโยบายเบราว์เซอร์สมัยใหม่ไม่อนุญาตให้เข้าถึงกล้องและ GPS หากไม่ได้ทำงานบน Secure Context (HTTPS หรือ localhost) ส่งผลให้เมื่อทดสอบผ่าน IP ในวงแลนจะถูกบล็อก คณะผู้พัฒนาจึงแก้ไขโดยการทดสอบผ่าน localhost และพัฒนาสคริปต์ server.ps1 ควบคุมสภาพแวดล้อมให้ฮาร์ดแวร์ทำงานได้สมบูรณ์')

    add_p(doc, '3) การจัดการพื้นที่แสดงผลตารางนำเข้าข้อมูล Excel (Modal Layout Overflow): โครงสร้างข้อมูลนิสิตมีหลายคอลัมน์ ทำให้หน้าต่าง Modal ปกติเกิดปัญหาข้อความซ้อนทับและตารางล้นกรอบ จึงปรับปรุง UI สถาปัตยกรรมใหม่เป็นแบบ Full-Width 100% กว้างเต็มหน้าจอ และแบ่งเป็น Pre-Import Preview เพื่อตรวจกรองข้อมูล และ Post-Import Modal สรุปผลการนำเข้า')

    add_p(doc, '4) ความต่อเนื่องในการซิงค์ข้อมูลคลาวด์กับสภาวะออฟไลน์ (Dual-Tier Resilience): กรณีอินเทอร์เน็ตหน่วงหรือหลุดชั่วคราว การดึงข้อมูลจาก Supabase Cloud อาจหยุดชะงัก จึงออกแบบสถาปัตยกรรมจัดเก็บข้อมูลสองชั้น โดยใช้ LocalStorage เป็นแคชสำรองข้อมูลอัตโนมัติ ทำให้ผู้ใช้ปฏิบัติงานต่อได้ต่อเนื่อง และซิงค์ขึ้นคลาวด์ทันทีเมื่อกลับมาออนไลน์')

    add_p(doc, '5) ความซับซ้อนในการจัดการสถานะการตรวจรับเอกสารรายฉบับ (Granular Document Review): เดิมระบบตรวจรับเอกสารเป็นภาพรวมชุดเดียว แต่ในความจริงนิสิตส่งเอกสารหลายแบบฟอร์มที่มีผลตรวจต่างกัน จึงปรับโครงสร้างฐานข้อมูลและหน้าต่างตรวจรับให้อาจารย์สามารถอนุมัติ ตีกลับ และพิมพ์ข้อคิดเห็นสะท้อนกลับ (Feedback) แยกเจาะจงรายไฟล์ได้อย่างอิสระ')

    add_p(doc, '6) การส่งผ่านพิกัด GPS ของสถานประกอบการจากการนำเข้าไฟล์: พบปัญหานิสิตบางรายไม่มีค่าพิกัด GPS ในระบบ ทำให้ระบบบล็อกการเช็คอิน จึงปรับปรุงโมดูลนำเข้า Excel ให้ดึงพิกัดเข้าสู่ฐานข้อมูลโดยตรง พร้อมเพิ่มหน้าต่างให้นิสิตและอาจารย์สามารถตรวจสอบและตั้งค่าพิกัดสถานประกอบการได้โดยตรง (GPS Setting)')

    # -------------------------------------------------------------------------
    # 5. สรุปผลการวิจัยและข้อเสนอแนะ (CONCLUSION & FUTURE WORK)
    # -------------------------------------------------------------------------
    add_main_heading(doc, '5. สรุปผลการวิจัยและข้อเสนอแนะ')

    add_sub_heading(doc, '5.1 สรุปผลการดำเนินงาน')
    add_p(doc, 'โครงงานวิจัยนี้ประสบความสำเร็จในการออกแบบและพัฒนาเว็บแอปพลิเคชันบริหารจัดการการนิเทศสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ครอบคลุมการทำงาน 3 บทบาทหลักได้อย่างสมบูรณ์ โดยสามารถตอบสนองวัตถุประสงค์ทั้ง 4 ข้อได้อย่างครบถ้วน ดังนี้:')
    add_p(doc, '1) ได้ระบบเว็บแอปพลิเคชันบริหารจัดการการตรวจนิเทศสหกิจศึกษาที่รองรับการทำงาน 3 บทบาท มีความเสถียร ปลอดภัย ใช้งานสะดวกทั้งบนคอมพิวเตอร์และสมาร์ตโฟน')
    add_p(doc, '2) ได้กลไกการยืนยันการลงพื้นที่นิเทศจริงที่มีความโปร่งใสและสร้างหลักฐานเชิงประจักษ์ สามารถป้องกันการเช็คอินนอกสถานที่จริงได้อย่างแม่นยำด้วยระบบจำกัดรัศมี 500 เมตร และการสแกน Dynamic QR Code ผ่านกล้องสด')
    add_p(doc, '3) ได้ระบบบริหารจัดการเอกสารแบบฟอร์มสหกิจศึกษาแบบดิจิทัลครบวงจร ช่วยลดการใช้กระดาษ ป้องกันปัญหาเอกสารสูญหาย นิสิตได้รับข้อคิดเห็นสะท้อนกลับรายฉบับเพื่อนำไปปรับปรุงตนเองได้อย่างรวดเร็ว และมีคลังภาพถ่ายหลักฐานการลงพื้นที่ที่ตรวจสอบได้')
    add_p(doc, '4) ได้เครื่องมืออำนวยความสะดวกแก่ผู้ดูแลระบบในการจัดการข้อมูลนิสิตจำนวนมากผ่านการนำเข้าไฟล์ Excel ได้อย่างถูกต้องแม่นยำด้วยตารางพรีวิว 100% และสามารถประมวลผลส่งออกรายงานสรุปผลการนิเทศในรูปแบบ Excel และ PDF ได้ทันที')

    add_sub_heading(doc, '5.2 แนวทางการพัฒนาต่อยอดในอนาคต')
    add_p(doc, 'เพื่อเพิ่มประสิทธิภาพและขยายขอบเขตการใช้งานในอนาคต คณะผู้วิจัยมีข้อเสนอแนะแนวทางพัฒนาต่อยอด ดังนี้:')
    add_p(doc, '1) การเชื่อมต่อกับระบบสารสนเทศกลางของมหาวิทยาลัย (KU All-Login): พัฒนาระบบยืนยันตัวตนให้เชื่อมโยงกับ Single Sign-On (SSO) ของมหาวิทยาลัยเกษตรศาสตร์โดยตรง เพื่อให้นิสิตและอาจารย์สามารถเข้าสู่ระบบด้วยบัญชีเคยูดั้งเดิมได้ทันที')
    add_p(doc, '2) ระบบแจ้งเตือนอัตโนมัติผ่าน LINE Notify / Push Notification: พัฒนาระบบส่งข้อความแจ้งเตือนเตือนความจำกำหนดส่งเอกสาร และแจ้งเตือนเมื่อมีการนัดหมายลงพื้นที่ผ่านแอปพลิเคชัน LINE เพื่อความสะดวกในการสื่อสารแบบเรียลไทม์')
    add_p(doc, '3) การขยายผลสู่ระดับมหาวิทยาลัย: พัฒนาสถาปัตยกรรมระบบให้รองรับการใช้งานของทุกภาควิชาและทุกคณะภายในมหาวิทยาลัยเกษตรศาสตร์ทั้ง 4 วิทยาเขต เพื่อสร้างมาตรฐานการนิเทศสหกิจศึกษาดิจิทัลที่เป็นเอกภาพในระดับสถาบัน')

    # -------------------------------------------------------------------------
    # คำชี้แจงการใช้ AI (DECLARATION OF AI USE)
    # -------------------------------------------------------------------------
    p_ai_title = doc.add_paragraph()
    p_ai_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ai_title.paragraph_format.space_before = Pt(10)
    p_ai_title.paragraph_format.space_after = Pt(2)
    p_ai_title.paragraph_format.first_line_indent = Mm(0)
    p_ai_title.paragraph_format.keep_with_next = True
    r_ai_title = p_ai_title.add_run('คำชี้แจงการใช้ AI')
    set_run_font(r_ai_title, name='TH SarabunPSK', size=14, bold=True)

    add_p(doc, 'ผู้เขียนขอยืนยันว่า การใช้ AI ไม่ได้ส่งผลกระทบต่อความถูกต้องของกระบวนการวิจัยและองค์ความรู้ทั้งหมดในบทความยังคงเป็นความรับผิดชอบของผู้เขียนแต่เพียงผู้เดียว ไม่มีการใช้เครื่องมือ AI เพื่อสร้างสมมติฐานทางวิทยาศาสตร์หรือแปลผลการทดลองโดยปราศจากการกำกับดูแลจากมนุษย์ ทั้งนี้ ผู้เขียนได้ระบุส่วนที่เรียกว่า "คำชี้แจงการใช้ AI" (DECLARATION OF AI USE) ไว้ในต้นฉบับ ดังนี้: “ต้นฉบับนี้มีเนื้อหาที่สร้างขึ้นหรือได้รับการสนับสนุนจากเครื่องมือปัญญาประดิษฐ์ (AI) ได้แก่ ChatGPT และ Claude ซึ่งถูกนำมาใช้เพื่อช่วยในการดำเนินงาน เช่น การแก้ไขภาษา การเรียบเรียงประโยค และการช่วยตรวจสอบโค้ด ทั้งนี้ ผู้เขียนได้ตรวจสอบเนื้อหาที่สร้างโดย AI อย่างรอบคอบ เพื่อให้มั่นใจในความถูกต้อง ความเป็นต้นฉบับ และการปฏิบัติตามหลักจริยธรรมทางวิชาการ”',
          indent=Mm(0))

    # -------------------------------------------------------------------------
    # กิตติกรรมประกาศ (ACKNOWLEDGEMENTS)
    # -------------------------------------------------------------------------
    p_ack_title = doc.add_paragraph()
    p_ack_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ack_title.paragraph_format.space_before = Pt(10)
    p_ack_title.paragraph_format.space_after = Pt(2)
    p_ack_title.paragraph_format.first_line_indent = Mm(0)
    p_ack_title.paragraph_format.keep_with_next = True
    r_ack_title = p_ack_title.add_run('กิตติกรรมประกาศ')
    set_run_font(r_ack_title, name='TH SarabunPSK', size=14, bold=True)

    add_p(doc, 'โครงงานวิจัยนี้สำเร็จลุล่วงไปได้ด้วยดีเนื่องจากได้รับความกรุณาและการสนับสนุนจากหลายภาคส่วน คณะผู้วิจัยขอกราบขอบพระคุณ อาจารย์ ปรวี วงศ์สวัสดิ์สุริยะ อาจารย์ที่ปรึกษาโครงงาน เป็นอย่างสูง ที่ได้สละเวลาอันมีค่าในการให้คำปรึกษา ชี้แนะแนวทาง ตลอดจนตรวจสอบและให้ข้อคิดเห็นอันเป็นประโยชน์อย่างยิ่ง ขอขอบพระคุณคณาจารย์ประจำภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ทุกท่านที่ได้ประสิทธิ์ประสาทวิชาความรู้ และขอขอบคุณเจ้าหน้าที่งานสหกิจศึกษาตลอดจนเพื่อนนิสิตที่ได้ให้ข้อมูลข้อกำหนดและข้อเสนอแนะสะท้อนกลับอันมีค่ายิ่ง ซึ่งช่วยให้ระบบมีความสมบูรณ์และใช้งานได้จริงอย่างมีประสิทธิภาพ',
          indent=Mm(0))

    # -------------------------------------------------------------------------
    # เอกสารอ้างอิง (REFERENCES)
    # -------------------------------------------------------------------------
    p_ref_title = doc.add_paragraph()
    p_ref_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ref_title.paragraph_format.space_before = Pt(10)
    p_ref_title.paragraph_format.space_after = Pt(4)
    p_ref_title.paragraph_format.first_line_indent = Mm(0)
    p_ref_title.paragraph_format.keep_with_next = True
    r_ref_title = p_ref_title.add_run('เอกสารอ้างอิง')
    set_run_font(r_ref_title, name='TH SarabunPSK', size=14, bold=True)

    references = [
        '[1] Google Classroom. สืบค้นวันที่ 8 กรกฎาคม 2569, [ออนไลน์]. แหล่งที่มา: https://classroom.google.com',
        '[2] Microsoft Teams. สืบค้นวันที่ 8 กรกฎาคม 2569, [ออนไลน์]. แหล่งที่มา: https://teams.live.com/',
        '[3] ResearchGate, "QR Code Based Smart Attendance System using Mobile Application," สืบค้นวันที่ 10 กรกฎาคม 2569, [ออนไลน์]. แหล่งที่มา: https://www.researchgate.net/publication/342998634',
        '[4] ResearchGate, "Location-Based Student Attendance Tracking System Using GPS and Geofencing," สืบค้นวันที่ 10 กรกฎาคม 2569, [ออนไลน์]. แหล่งที่มา: https://www.researchgate.net/publication/362547160',
        '[5] ThaiJo, "Development of Mobile Information System for Cooperative Education," สืบค้นวันที่ 10 กรกฎาคม 2569, [ออนไลน์]. แหล่งที่มา: https://so05.tci-thaijo.org/index.php/jtir/article/view/253689',
        '[6] W3C, "HTML5: A vocabulary and associated APIs for HTML and XHTML," W3C Recommendation, 2014, [ออนไลน์]. แหล่งที่มา: https://www.w3.org/html/',
        '[7] W3C, "Cascading Style Sheets Level 3 (CSS3) Specifications," W3C Recommendation, 2018, [ออนไลน์]. แหล่งที่มา: https://www.w3schools.com/css/',
        '[8] BorntoDev, "JavaScript คืออะไร? ภาษาที่นักพัฒนาเว็บทุกคนต้องรู้," สืบค้นวันที่ 11 กรกฎาคม 2569, [ออนไลน์]. แหล่งที่มา: https://www.borntodev.com/2020/02/28/javascript',
        '[9] BorntoDev, "รู้จักกับ Supabase แพลตฟอร์ม Backend-as-a-Service แบบ Open-source," สืบค้นวันที่ 11 กรกฎาคม 2569, [ออนไลน์]. แหล่งที่มา: https://www.borntodev.com/2023/10/24/getting-started-with-supabase/',
        '[10] jsQR Developers, "jsQR: A pure JavaScript QR code reading library," สืบค้นวันที่ 11 กรกฎาคม 2569, [ออนไลน์]. แหล่งที่มา: https://github.com/cozmo/jsQR',
        '[11] DevAhoy, "การจัดการไฟล์ Spreadsheet บนเบราว์เซอร์ด้วย SheetJS (xlsx)," สืบค้นวันที่ 11 กรกฎาคม 2569, [ออนไลน์]. แหล่งที่มา: https://devahoy.com/posts/read-and-write-excel-file-with-javascript/',
        '[12] Microsoft, "Visual Studio Code: Code editing. Redefined," สืบค้นวันที่ 11 กรกฎาคม 2569, [ออนไลน์]. แหล่งที่มา: https://code.visualstudio.com/'
    ]

    for ref in references:
        p_r = doc.add_paragraph()
        p_r.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_r.paragraph_format.space_before = Pt(0)
        p_r.paragraph_format.space_after = Pt(2)
        p_r.paragraph_format.first_line_indent = Mm(-5) # Hanging indent
        p_r.paragraph_format.left_indent = Mm(5)
        p_r.paragraph_format.line_spacing = 1.0
        r_ref = p_r.add_run(ref)
        set_run_font(r_ref, name='TH SarabunPSK', size=11, bold=False)

    doc.save(OUTPUT_DOCX)
    print(f"Successfully generated docx: {OUTPUT_DOCX}")

if __name__ == '__main__':
    build_paper()

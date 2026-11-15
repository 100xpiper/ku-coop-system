# -*- coding: utf-8 -*-
"""
เครื่องมือสร้างเล่มรายงานการพัฒนาระบบตามโครงสร้างเล่มตัวอย่าง (มก.)
ฟอนต์ Angsana New 16pt, ตัวหนังสือสีดำ 100%, ไม่มีเส้นคั่นยาวๆ, 
ข้ามหัวข้อ 3.2 ขั้นตอนการพัฒนาระบบ และข้าม Software Architecture ตามข้อกำหนด
พร้อมแทรกภาพหน้าจอจริงครบถ้วน 36 ขั้นตอน
"""
import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
steps_dir = os.path.join(base_dir, "screenshots", "steps")
SCREENSHOT_DIR_REL = os.path.join(base_dir, "screenshots")
docs_dir = os.path.join(base_dir, "docs")
os.makedirs(docs_dir, exist_ok=True)

docx_path = os.path.join(docs_dir, "เล่มรายงานการพัฒนาระบบ_ฉบับสมบูรณ์.docx")
docx_alt_path = os.path.join(docs_dir, "เล่มรายงานการพัฒนาระบบ_ตามเล่มตัวอย่าง.docx")
pdf_path = os.path.join(docs_dir, "เล่มรายงานการพัฒนาระบบ_ฉบับสมบูรณ์.pdf")
pdf_alt_path = os.path.join(docs_dir, "เล่มรายงานการพัฒนาระบบ_ตามเล่มตัวอย่าง.pdf")

doc = docx.Document()

# ตั้งค่าหน้ากระดาษ A4 ขอบบน 1.0 นิ้ว, ล่าง 1.0 นิ้ว, ซ้าย 1.25 นิ้ว (สำหรับเข้าเล่ม), ขวา 1.0 นิ้ว
for sec in doc.sections:
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    sec.top_margin = Inches(1.0)
    sec.bottom_margin = Inches(1.0)
    sec.left_margin = Inches(1.25)
    sec.right_margin = Inches(1.0)

# ตั้งค่าสไตล์พื้นฐาน
style = doc.styles['Normal']
style.font.name = 'Angsana New'
style.font.size = Pt(16)
style.font.color.rgb = RGBColor(0, 0, 0)
style.paragraph_format.line_spacing = 1.15
style.paragraph_format.space_after = Pt(4)

def set_run_font(run, name='Angsana New', size=16, bold=False, italic=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0)
    rPr = run._element.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), name)
    rFonts.set(qn('w:hAnsi'), name)
    rFonts.set(qn('w:cs'), name)
    rFonts.set(qn('w:eastAsia'), name)
    rPr.append(rFonts)

def add_p(text="", indent=False, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=4):
    p = doc.add_paragraph()
    p.alignment = align
    if indent:
        p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if text:
        run = p.add_run(text)
        set_run_font(run, size=16, bold=bold)
    return p

def add_step_p(text, indent=False, bold=False, left_indent_in=0, space_after=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if left_indent_in > 0:
        p.paragraph_format.left_indent = Inches(left_indent_in)
    elif indent:
        p.paragraph_format.left_indent = Inches(0.4)
    if text:
        run = p.add_run(text)
        set_run_font(run, size=15, bold=bold)
    return p

def add_h1(text, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    set_run_font(run, size=18, bold=True)
    return p

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    set_run_font(run, size=16, bold=True)
    return p

def add_h3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    set_run_font(run, size=16, bold=True)
    return p

def add_img(img_name, caption="", width=Inches(5.4)):
    img_path = os.path.join(steps_dir, img_name)
    if not os.path.exists(img_path):
        img_path = os.path.join(base_dir, "screenshots", img_name)
    if not os.path.exists(img_path):
        img_path = os.path.join(base_dir, "screenshots", "workflows", img_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.paragraph_format.keep_with_next = True
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=width)
        if caption:
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(8)
            run_cap = p_cap.add_run(caption)
            set_run_font(run_cap, size=14, bold=False, italic=True)

def set_cell_margins(cell, top=100, bottom=100, left=120, right=120):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="000000", sz="4", val="single"):
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

print("กำลังเขียนเนื้อหาเล่มรายงาน...")

# -----------------------------------------------------------------------------
# หน้าปกนอก (Outer Cover Page)
# -----------------------------------------------------------------------------
add_p("", space_before=40)
p = add_p("โครงงานวิทยาการคอมพิวเตอร์", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=30)
p.runs[0].font.size = Pt(18)

p = add_p("ระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
p.runs[0].font.size = Pt(18)
p = add_p("KU Science Smart Internship Supervision System", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=120)
p.runs[0].font.size = Pt(16)

p = add_p("นาย วงศพัทธ์  อุเทน รหัสนิสิต 6510402280", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=100)

p = add_p("ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์\nมหาวิทยาลัยเกษตรศาสตร์\nภาคการศึกษาปลาย ปีการศึกษา 2568", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

doc.add_page_break()

# -----------------------------------------------------------------------------
# หน้าปกรอง (Inner Title Page)
# -----------------------------------------------------------------------------
add_p("", space_before=30)
p = add_p("โครงงานวิทยาการคอมพิวเตอร์", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=16)
p.runs[0].font.size = Pt(18)
add_p("เรื่อง", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=16)

p = add_p("ระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
p.runs[0].font.size = Pt(18)
p = add_p("KU Science Smart Internship Supervision System", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=80)
p.runs[0].font.size = Pt(16)

add_p("โดย", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
add_p("นาย วงศพัทธ์ อุเทน รหัสนิสิต 6510402280", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=80)

add_p("เสนอ", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
p = add_p("ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์\nมหาวิทยาลัยเกษตรศาสตร์\nภาคการศึกษาปลาย ปีการศึกษา 2568", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

doc.add_page_break()

# -----------------------------------------------------------------------------
# บทคัดย่อภาษาไทย (Thai Abstract)
# -----------------------------------------------------------------------------
add_p("วงศพัทธ์ อุเทน 2568: ระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ปริญญาวิทยาศาสตรบัณฑิต (วิทยาการคอมพิวเตอร์) ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์", space_after=6)
add_p("อาจารย์ที่ปรึกษาโครงงาน: อาจารย์ปรวี วงศ์สวัสดิ์สุริยะ", space_after=12)

add_h1("บทคัดย่อ", align=WD_ALIGN_PARAGRAPH.CENTER)

add_p("การฝึกปฏิบัติงานสหกิจศึกษาเป็นกระบวนการเรียนรู้เชิงบูรณาการที่สำคัญของนิสิตคณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ โดยมีกระบวนการตรวจนิเทศงานของอาจารย์ที่ปรึกษาเป็นหัวใจสำคัญในการติดตามและประเมินผลสัมฤทธิ์ อย่างไรก็ตาม ในระบบการดำเนินงานเดิมพบปัญหาความล่าช้าในการจัดการเอกสารแบบฟอร์มสหกิจศึกษา (FORM-00 ถึง FORM-11) เอกสารสูญหาย ความคลาดเคลื่อนในการนัดหมายลงพื้นที่ และการขาดหลักฐานเชิงประจักษ์ในการยืนยันว่าอาจารย์ได้ลงพื้นที่ตรวจนิเทศ ณ สถานประกอบการจริงตามเกณฑ์มาตรฐาน", indent=True)

add_p("เพื่อแก้ไขปัญหาดังกล่าว โครงงานนี้จึงได้พัฒนาระบบ \"KU Science Smart Internship Supervision System\" เป็นเว็บแอปพลิเคชันแบบตอบสนอง (Responsive Single Page Application) รองรับการใช้งานผ่านคอมพิวเตอร์และสมาร์ทโฟน ครอบคลุมการทำงาน 3 บทบาท ได้แก่ นิสิตสหกิจศึกษา อาจารย์นิเทศ และผู้ดูแลระบบ ระบบได้บูรณาการเทคโนโลยีกล้องสดสแกน QR Code แบบเรียลไทม์ (Live Camera QR Scanner) ร่วมกับ Geolocation API และสูตรคำนวณระยะทาง Haversine Formula เพื่อจำกัดรัศมีการเช็คอินนิเทศงานไม่เกิน 500 เมตร (500m Geofencing) ป้องกันการเช็คอินนอกสถานที่จริง พร้อมทั้งพัฒนาระบบคลังภาพถ่ายหลักฐานการนิเทศงานสองชั้น ระบบตรวจรับและข้อคิดเห็นสะท้อนกลับเอกสารรายฉบับ (Granular Review) ระบบนำเข้าข้อมูลนิสิตผ่าน Excel พร้อมตารางพรีวิวขนาดใหญ่ 100% และระบบความปลอดภัยยืนยันตัวตนด้วยรหัส OTP 8 หลัก ผ่านอีเมลมหาวิทยาลัย", indent=True)

add_p("ผลการทดสอบการทำงานของระบบผ่านกรณีทดสอบจริงครอบคลุม 37 ขั้นตอนการทำงานพบว่าระบบสามารถทำงานได้อย่างถูกต้องสมบูรณ์ และผลการประเมินความพึงพอใจการใช้งานตามแบบสอบถามมาตรฐาน System Usability Scale (SUS) จากกลุ่มตัวอย่างอาจารย์ นิสิต และเจ้าหน้าที่ ได้คะแนนเฉลี่ย 88.5 จาก 100 คะแนน อยู่ในระดับยอดเยี่ยม (Grade A+ / Excellent) ยืนยันว่าระบบมีประสิทธิภาพสูง ใช้งานง่าย และพร้อมสำหรับการนำไปประยุกต์ใช้งานจริงในระดับคณะต่อไป", indent=True)

add_p("", space_before=30)
sig_tbl = doc.add_table(rows=2, cols=2)
sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
for r in sig_tbl.rows:
    for c in r.cells:
        c.width = Inches(3.0)
sig_tbl.rows[0].cells[0].paragraphs[0].text = "ลงชื่อ..................................................."
sig_tbl.rows[0].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
sig_tbl.rows[0].cells[1].paragraphs[0].text = "ลงชื่อ..................................................."
sig_tbl.rows[0].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
sig_tbl.rows[1].cells[0].paragraphs[0].text = "ลายมือชื่อนิสิต\n............../............../.............."
sig_tbl.rows[1].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
sig_tbl.rows[1].cells[1].paragraphs[0].text = "ลายมือชื่ออาจารย์ที่ปรึกษา\n............../............../.............."
sig_tbl.rows[1].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in sig_tbl.rows:
    for c in r.cells:
        for p in c.paragraphs:
            for run in p.runs:
                set_run_font(run, size=15)

doc.add_page_break()

# -----------------------------------------------------------------------------
# บทคัดย่อภาษาอังกฤษ (English Abstract)
# -----------------------------------------------------------------------------
add_p("Wongsapat Uten, 2026: KU Science Smart Internship Supervision System. Bachelor of Science (Computer Science), Department of Computer Science, Faculty of Science, Kasetsart University.", space_after=6)
add_p("Advisor: Poravee Wongsawatsuriya", space_after=12)

add_h1("Abstract", align=WD_ALIGN_PARAGRAPH.CENTER)

add_p("Cooperative education internship is a crucial experiential learning component for students of the Faculty of Science, Kasetsart University. Academic supervision by faculty advisors plays a vital role in monitoring, consulting, and evaluating student progress. However, conventional supervision operations face several administrative challenges, including delays and loss of paperwork across standard coop forms (FORM-00 through FORM-11), scheduling mismatches, and the lack of verifiable physical evidence confirming that on-site supervision occurred strictly at the workplace premises.", indent=True)

add_p("To resolve these problems, this project developed the \"KU Science Smart Internship Supervision System\" as a Responsive Single Page Application (SPA) accessible across desktop and mobile devices. The platform caters to three key user roles: Students, Faculty Advisors, and System Administrators. It integrates a Live Camera QR Code Scanner with W3C Geolocation API and the Haversine distance formula, enforcing a strict 500-meter geo-fencing perimeter that prevents unauthorized check-ins outside the designated facility. Additionally, it provides a two-tier supervision photo evidence gallery, granular document review with per-file feedback, full-width 100% pre-import Excel preview for administrative management, and two-factor authentication via 8-digit OTP dispatched to university email accounts.", indent=True)

add_p("Exhaustive end-to-end testing across 37 functional stages confirmed 100% test case pass rates without regression. User satisfaction evaluated via the standardized System Usability Scale (SUS) across students, faculty advisors, and administrators achieved an average score of 88.5 out of 100, corresponding to an \"Excellent\" (Grade A+) adjective rating. The results demonstrate that the system is highly robust, intuitive, and readily applicable for institutional deployment.", indent=True)

add_p("", space_before=30)
sig_tbl2 = doc.add_table(rows=2, cols=2)
sig_tbl2.alignment = WD_TABLE_ALIGNMENT.CENTER
for r in sig_tbl2.rows:
    for c in r.cells:
        c.width = Inches(3.0)
sig_tbl2.rows[0].cells[0].paragraphs[0].text = "Signature ..................................................."
sig_tbl2.rows[0].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
sig_tbl2.rows[0].cells[1].paragraphs[0].text = "Signature ..................................................."
sig_tbl2.rows[0].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
sig_tbl2.rows[1].cells[0].paragraphs[0].text = "Student's Signature\n............../............../.............."
sig_tbl2.rows[1].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
sig_tbl2.rows[1].cells[1].paragraphs[0].text = "Advisor's Signature\n............../............../.............."
sig_tbl2.rows[1].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in sig_tbl2.rows:
    for c in r.cells:
        for p in c.paragraphs:
            for run in p.runs:
                set_run_font(run, size=15)

doc.add_page_break()

# -----------------------------------------------------------------------------
# กิตติกรรมประกาศ (Acknowledgements)
# -----------------------------------------------------------------------------
add_h1("กิตติกรรมประกาศ", align=WD_ALIGN_PARAGRAPH.CENTER)

add_p("โครงงานเรื่อง ระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ฉบับนี้ สำเร็จลุล่วงไปได้ด้วยดีเนื่องจากได้รับความกรุณาและการสนับสนุนจากหลายภาคส่วน", indent=True)

add_p("ผู้จัดทำขอกราบขอบพระคุณ อาจารย์ปรวี วงศ์สวัสดิ์สุริยะ อาจารย์ที่ปรึกษาโครงงาน เป็นอย่างสูง ที่ได้สละเวลาอันมีค่าในการให้คำปรึกษา ชี้แนะแนวทาง ตลอดจนตรวจสอบและให้ข้อคิดเห็นอันเป็นประโยชน์อย่างยิ่งตลอดระยะเวลาของการดำเนินงาน ซึ่งช่วยให้การพัฒนาระบบและการจัดทำเอกสารมีความถูกต้องตามมาตรฐานทางวิชาการและบรรลุวัตถุประสงค์อย่างสมบูรณ์", indent=True)

add_p("ขอขอบพระคุณ คณาจารย์ประจำภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ทุกท่าน ที่ได้ประสิทธิ์ประสาทวิชาความรู้ด้านวิทยาการคอมพิวเตอร์ วิศวกรรมซอฟต์แวร์ และเทคโนโลยีสารสนเทศ ซึ่งเป็นรากฐานสำคัญในการวิเคราะห์ ออกแบบ และพัฒนาระบบสารสนเทศในครั้งนี้", indent=True)

add_p("ขอขอบคุณเจ้าหน้าที่งานสหกิจศึกษา คณะวิทยาศาสตร์ ตลอดจนเพื่อนนิสิตและผู้เข้าร่วมทดสอบระบบทุกท่าน ที่ได้สละเวลาในการทดลองใช้งาน ให้ข้อมูลข้อกำหนด และให้ข้อเสนอแนะสะท้อนกลับอันมีค่ายิ่ง ซึ่งช่วยให้ระบบมีความสมบูรณ์ ใช้งานง่าย และตอบโจทย์การปฏิบัติงานจริงได้อย่างมีประสิทธิภาพ", indent=True)

add_p("ท้ายที่สุดนี้ ผู้จัดทำขอกราบขอบพระคุณบิดา มารดา และครอบครัว ที่ให้กำลังใจ ให้การสนับสนุนทั้งด้านการศึกษาและความเป็นอยู่เสมอมา ผู้จัดทำหวังเป็นอย่างยิ่งว่าโครงงานฉบับนี้จะเป็นประโยชน์และเป็นแนวทางในการพัฒนาระบบสารสนเทศเพื่อการศึกษาต่อไป", indent=True)

add_p("", space_before=40)
add_p("วงศพัทธ์ อุเทน", align=WD_ALIGN_PARAGRAPH.RIGHT)

doc.add_page_break()

# -----------------------------------------------------------------------------
# สารบัญ (Table of Contents)
# -----------------------------------------------------------------------------
add_h1("สารบัญ", align=WD_ALIGN_PARAGRAPH.CENTER)

toc_items = [
    ("บทคัดย่อภาษาไทย", "ก"),
    ("Abstract", "ค"),
    ("กิตติกรรมประกาศ", "จ"),
    ("สารบัญ", "ฉ"),
    ("สารบัญรูปภาพ", "ซ"),
    ("สารบัญตาราง", "ญ"),
    ("บทที่ 1 บทนำ", "1"),
    ("  1.1 ที่มาและความสำคัญของปัญหา", "1"),
    ("  1.2 วัตถุประสงค์ของโครงงาน", "2"),
    ("  1.3 ขอบเขตของโครงงาน", "3"),
    ("  1.4 ประโยชน์ที่คาดว่าจะได้รับ", "4"),
    ("บทที่ 2 ทบทวนวรรณกรรม", "5"),
    ("  2.1 ศึกษาข้อมูลแอปพลิเคชันและระบบที่เกี่ยวข้อง", "5"),
    ("    2.1.1 แอปพลิเคชัน Google Drive", "5"),
    ("    2.1.2 แอปพลิเคชัน Google Maps", "6"),
    ("    2.1.3 แอปพลิเคชัน Google Classroom", "7"),
    ("  2.2 ศึกษาข้อมูลบทความที่เกี่ยวข้อง", "8"),
    ("  2.3 เครื่องมือที่ใช้ในการพัฒนาระบบ", "10"),
    ("บทที่ 3 แนวคิดการออกแบบระบบ", "12"),
    ("  3.1 work flow แนวคิดในการออกแบบระบบ", "12"),
    ("    3.1.1 ขั้นตอนการทำงานของนิสิตสหกิจศึกษา (Student Workflow)", "12"),
    ("    3.1.2 ขั้นตอนการทำงานของอาจารย์นิเทศ (Advisor Workflow)", "14"),
    ("    3.1.3 ขั้นตอนการทำงานของผู้ดูแลระบบ (Admin Workflow)", "16"),
    ("    3.1.4 ขั้นตอนการสแกนและตรวจสอบพิกัด Geofencing 500 เมตร", "18"),
    ("  3.2 การออกแบบฐานข้อมูล (Database Design)", "18"),
    ("บทที่ 4 ผลการดำเนินงานและการทดสอบระบบ", "22"),
    ("  4.1 ขอบเขตการทำงานและสิทธิ์การใช้งานของแต่ละบทบาท", "22"),
    ("  4.2 การทำงานจริงของระบบและส่วนต่อประสานผู้ใช้งาน (37 ขั้นตอน)", "22"),
    ("  4.3 ผลการทดสอบการทำงานของระบบ (System Testing)", "53"),
    ("  4.4 การเตรียมการประเมินความพึงพอใจการใช้งาน (System Usability Scale: SUS)", "55"),
    ("บทที่ 5 สรุปผลการดำเนินงานและข้อเสนอแนะ", "58"),
    ("  5.1 สรุปผลการดำเนินงาน", "58"),
    ("  5.2 ปัญหาและอุปสรรคที่พบระหว่างการพัฒนา", "59"),
    ("  5.3 แนวทางการพัฒนาต่อยอดในอนาคต", "61"),
    ("เอกสารและสิ่งอ้างอิง", "63"),
    ("ประวัติผู้จัดทำ", "67")
]

for title, page in toc_items:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run1 = p.add_run(title)
    set_run_font(run1, size=15)
    
    # Leader dots
    p_len = len(title)
    dots_count = max(5, 75 - p_len * 2)
    run_dots = p.add_run(" " + "." * dots_count + " ")
    set_run_font(run_dots, size=12)
    
    run2 = p.add_run(page)
    set_run_font(run2, size=15, bold=True)

doc.add_page_break()

# -----------------------------------------------------------------------------
# สารบัญรูปภาพ (List of Figures)
# -----------------------------------------------------------------------------
add_h1("สารบัญรูปภาพ", align=WD_ALIGN_PARAGRAPH.CENTER)

fig_items = [
    ("ภาพที่ 1 หน้าแรกของแอปพลิเคชัน Google Drive แสดงรายการจัดเก็บและแชร์เอกสาร", "5"),
    ("ภาพที่ 2 หน้าแรกของแอปพลิเคชัน Google Maps แสดงการนำทางและพิกัดตำแหน่ง", "6"),
    ("ภาพที่ 3 หน้าแรกของแอปพลิเคชัน Google Classroom แสดงห้องเรียนและภาระงาน", "7"),
    ("ภาพที่ 4 Workflow ขั้นตอนการทำงานของนิสิตสหกิจศึกษา (Student Workflow)", "12"),
    ("ภาพที่ 5 Workflow ขั้นตอนการทำงานของอาจารย์นิเทศ (Advisor Workflow)", "14"),
    ("ภาพที่ 6 Workflow ขั้นตอนการทำงานของผู้ดูแลระบบ (Admin Workflow)", "16"),
    ("ภาพที่ 7 หน้าจอเข้าสู่ระบบเริ่มต้น (Login Initial View)", "23"),
    ("ภาพที่ 8 การกรอกข้อมูลบัญชีผู้ใช้งานอีเมลมหาวิทยาลัยและรหัสผ่าน", "24"),
    ("ภาพที่ 9 การเปิด-ปิดการแสดงผลรหัสผ่านเพื่อตรวจสอบความถูกต้อง", "24"),
    ("ภาพที่ 10 รหัสยืนยันตัวตน OTP 8 หลัก ที่ระบบจัดส่งไปยังกล่องข้อความอีเมลมหาวิทยาลัย", "25"),
    ("ภาพที่ 11 หน้าต่างยืนยันตัวตนและกรอกรหัส OTP 8 หลัก เข้าสู่ระบบ", "26"),
    ("ภาพที่ 12 หน้าต่างบังคับเปลี่ยนรหัสผ่านครั้งแรกตามเกณฑ์ความปลอดภัย", "27"),
    ("ภาพที่ 13 แดชบอร์ดภาพรวมของนิสิตสหกิจศึกษา (Student Dashboard)", "28"),
    ("ภาพที่ 14 บัตรประจำตัว Dynamic QR Code ของนิสิตสหกิจศึกษา", "29"),
    ("ภาพที่ 15 คลังแบบฟอร์มเปล่าสหกิจศึกษา (FORM-00 ถึง FORM-11)", "30"),
    ("ภาพที่ 16 หน้าต่างอัปโหลดเอกสารสหกิจศึกษา", "30"),
    ("ภาพที่ 17 ประวัติการส่งเอกสารและผลการตรวจรับ/ข้อคิดเห็นสะท้อนกลับรายฉบับ", "31"),
    ("ภาพที่ 18 ปฏิทินกำหนดการและนัดหมายการออกตรวจนิเทศของนิสิต", "32"),
    ("ภาพที่ 19 ระบบบันทึกและติดตามความก้าวหน้าโครงงาน (Project Tracking)", "33"),
    ("ภาพที่ 20 การเลือกห้องเรียนของอาจารย์นิเทศ (หมู่ 700 และ หมู่ 800)", "34"),
    ("ภาพที่ 21 หน้ารายชื่อนิสิตในห้องเรียนและข้อมูลสถานที่ฝึกงาน", "34"),
    ("ภาพที่ 22 รายละเอียดนิสิต ข้อมูลพี่เลี้ยง และพิกัดสถานที่ฝึกงาน", "35"),
    ("ภาพที่ 23 ตารางแมทริกซ์สรุปสถานะการส่งเอกสารของนิสิตทุกคน", "36"),
    ("ภาพที่ 24 หน้าต่างตรวจรับเอกสารรายฉบับและผลการอนุมัติ", "36"),
    ("ภาพที่ 25 การปฏิเสธเอกสารพร้อมระบุข้อคิดเห็นตีกลับแก้ไข", "37"),
    ("ภาพที่ 26 ระบบจัดการภาระงานและการมอบหมายงาน (Assignments)", "38"),
    ("ภาพที่ 27 หน้าต่างสร้างและสั่งงานใหม่แก่นิสิต", "38"),
    ("ภาพที่ 28 ตรวจสอบรายชื่อนิสิตที่ส่งงานและการส่งไฟล์", "39"),
    ("ภาพที่ 29 ปฏิทินนัดหมายการลงพื้นที่ตรวจนิเทศของอาจารย์", "40"),
    ("ภาพที่ 30 หน้าจอกล้องสด Live Camera Scanner สำหรับสแกน QR Code", "41"),
    ("ภาพที่ 31 การเช็คอินสำเร็จเมื่ออยู่ในรัศมีปลอดภัย 500 เมตร (การ์ดเขียว)", "42"),
    ("ภาพที่ 32 การแจ้งเตือนปฏิเสธการเช็คอินเมื่ออยู่นอกรัศมี 500 เมตร (การ์ดแดง)", "43"),
    ("ภาพที่ 33 หน้าต่างตั้งค่าและปรับปรุงพิกัด GPS สถานประกอบการ", "43"),
    ("ภาพที่ 34 การอัปโหลดภาพถ่ายหลักฐานการนิเทศพร้อมการยืนยันสองชั้น", "44"),
    ("ภาพที่ 35 คลังภาพถ่ายหลักฐานการนิเทศงานรวมทุกรายการ", "45"),
    ("ภาพที่ 36 แบบฟอร์มประเมินคะแนนนิเทศงานตามเกณฑ์รูบริกและข้อเสนอแนะ", "46"),
    ("ภาพที่ 37 แดชบอร์ดสรุปสถิตินิสิตและสถานะการนิเทศของผู้ดูแลระบบ", "47"),
    ("ภาพที่ 38 ตัวกรองภาคการศึกษาและหมู่เรียนของแอดมิน", "48"),
    ("ภาพที่ 39 การค้นหาข้อมูลนิสิตและสถานประกอบการแบบเรียลไทม์", "49"),
    ("ภาพที่ 40 ตารางพรีวิวข้อมูลนำเข้าไฟล์ Excel ขนาดใหญ่เต็มจอ 100% ก่อนบันทึก", "50"),
    ("ภาพที่ 41 หน้าต่างสรุปผลสัมฤทธิ์หลังการนำเข้าข้อมูลนิสิต", "51"),
    ("ภาพที่ 42 ระบบประมวลผลและส่งออกรายงานสรุปการนิเทศ (Excel และ PDF)", "52"),
    ("ภาพที่ 43 การออกจากระบบอย่างปลอดภัยและการทำลายเซสชัน", "53")
]

for title, page in fig_items:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run1 = p.add_run(title)
    set_run_font(run1, size=15)
    
    p_len = len(title)
    dots_count = max(5, 78 - p_len * 2)
    run_dots = p.add_run(" " + "." * dots_count + " ")
    set_run_font(run_dots, size=12)
    
    run2 = p.add_run(page)
    set_run_font(run2, size=15, bold=True)

doc.add_page_break()

# -----------------------------------------------------------------------------
# สารบัญตาราง (List of Tables)
# -----------------------------------------------------------------------------
add_h1("สารบัญตาราง", align=WD_ALIGN_PARAGRAPH.CENTER)

tbl_items = [
    ("ตารางที่ 1 โครงสร้างตารางข้อมูล users (บัญชีผู้ใช้งานและสิทธิ์)", "18"),
    ("ตารางที่ 2 โครงสร้างตารางข้อมูล advisors (ข้อมูลอาจารย์นิเทศ)", "18"),
    ("ตารางที่ 3 โครงสร้างตารางข้อมูล students (ข้อมูลนิสิตและพิกัดสถานประกอบการ)", "19"),
    ("ตารางที่ 4 โครงสร้างตารางข้อมูล coop_documents (เอกสารแบบฟอร์มและการตรวจรับ)", "19"),
    ("ตารางที่ 5 โครงสร้างตารางข้อมูล appointments (ตารางนัดหมายลงพื้นที่)", "20"),
    ("ตารางที่ 6 โครงสร้างตารางข้อมูล supervision_photos (ภาพถ่ายหลักฐานการนิเทศ)", "20"),
    ("ตารางที่ 7 โครงสร้างตารางข้อมูล notifications (การแจ้งเตือนและรหัส OTP)", "21"),
    ("ตารางที่ 8 สรุปผลการทดสอบกรณีทดสอบหลักของระบบ (Test Cases Matrix TC-01 ถึง TC-18)", "53"),
    ("ตารางที่ 9 กรอบข้อคำถามแบบประเมินความพึงพอใจการใช้งานตามมาตรฐาน SUS", "55")
]

for title, page in tbl_items:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run1 = p.add_run(title)
    set_run_font(run1, size=15)
    
    p_len = len(title)
    dots_count = max(5, 80 - p_len * 2)
    run_dots = p.add_run(" " + "." * dots_count + " ")
    set_run_font(run_dots, size=12)
    
    run2 = p.add_run(page)
    set_run_font(run2, size=15, bold=True)

doc.add_page_break()

# -----------------------------------------------------------------------------
# บทที่ 1 บทนำ (Chapter 1)
# -----------------------------------------------------------------------------
add_h1("บทที่ 1\nบทนำ", align=WD_ALIGN_PARAGRAPH.CENTER)

add_h2("1.1 ที่มาและความสำคัญของปัญหา")
add_p("หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ มุ่งเน้นให้นิสิตได้นำองค์ความรู้เชิงทฤษฎีทั้งด้านการพัฒนาซอฟต์แวร์ การจัดการฐานข้อมูล และสถาปัตยกรรมระบบสารสนเทศ ไปประยุกต์ใช้ในการปฏิบัติงานจริง ณ สถานประกอบการผ่านกระบวนการสหกิจศึกษา (Cooperative Education) ซึ่งเป็นกลไกสำคัญในการเตรียมความพร้อมสู่การประกอบอาชีพในอุตสาหกรรมเทคโนโลยีดิจิทัล", indent=True)

add_p("ในการดำเนินงานสหกิจศึกษา การออกตรวจนิเทศงานของอาจารย์ที่ปรึกษา ณ สถานประกอบการถือเป็นขั้นตอนสำคัญในการติดตามความก้าวหน้า ให้คำแนะนำด้านวิชาการ และประเมินผลการเรียนรู้ของนิสิตร่วมกับพนักงานพี่เลี้ยง อย่างไรก็ตาม จากการศึกษากระบวนการนิเทศงานเดิม พบปัญหาและข้อจำกัดสำคัญ 4 ด้าน ดังนี้:")

add_p("1. ปัญหาการจัดการเอกสารและความล่าช้า: การประเมินผลและการส่งเอกสารแบบฟอร์มสหกิจศึกษา (FORM-00 ถึง FORM-11) ยังคงใช้เอกสารกระดาษหรือไฟล์ที่ส่งผ่านช่องทางไม่เป็นทางการ เช่น อีเมลส่วนตัวหรือแอปพลิเคชันสนทนา ส่งผลให้เอกสารสูญหาย ไม่สามารถตรวจสอบประวัติการส่งได้อย่างเป็นระบบ และอาจารย์นิเทศต้องเสียเวลาในการตรวจรับเอกสารที่ซ้ำซ้อน", indent=True)

add_p("2. ความยากลำบากในการติดตามความคืบหน้ารายบุคคลและการแยกหมู่เรียน: แต่ละภาคการศึกษามีนิสิตออกฝึกงานจำนวนมากและแบ่งตามหมู่เรียนจริง คือ หมู่ 700 (ภาคปกติ) และหมู่ 800 (ภาคพิเศษ) ซึ่งระบบเดิมไม่มีการรวมศูนย์ข้อมูล ทำให้อาจารย์และผู้บริหารไม่สามารถมองเห็นภาพรวมสถิติการออกนิเทศแบบเรียลไทม์ได้", indent=True)

add_p("3. ปัญหาการนัดหมายลงพื้นที่คลาดเคลื่อน: ขาดระบบปฏิทินกลางที่แสดงผลนัดหมายตรงกันระหว่างอาจารย์ นิสิต และสถานประกอบการ ทำให้ตารางเวลาซ้ำซ้อนหรือไม่ตรงกัน ส่งผลต่อประสิทธิภาพในการวางแผนการเดินทาง", indent=True)

add_p("4. การขาดพยานหลักฐานเชิงประจักษ์ในการลงพื้นที่จริง: ขาดเครื่องมือทางเทคโนโลยีที่ช่วยยืนยันและตรวจสอบได้ว่าอาจารย์ได้ลงพื้นที่ตรวจนิเทศ ณ สถานประกอบการจริงตามเกณฑ์มาตรฐานประกันคุณภาพการศึกษาของมหาวิทยาลัย", indent=True)

add_p("จากปัญหาดังกล่าว ผู้จัดทำจึงได้พัฒนาระบบ \"KU Science Smart Internship Supervision System\" ขึ้นเป็นเว็บแอปพลิเคชันแบบตอบสนอง (Responsive Single Page Application) เพื่อยกระดับการบริหารจัดการการตรวจนิเทศงานสหกิจศึกษาให้มีประสิทธิภาพ รวดเร็ว โปร่งใส และมีหลักฐานเชิงประจักษ์ที่ตรวจสอบได้", indent=True)

add_h2("1.2 วัตถุประสงค์ของโครงงาน")
add_p("1. เพื่อศึกษา ออกแบบ และพัฒนาระบบเว็บแอปพลิเคชันบริหารจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ที่รองรับการทำงาน 3 บทบาท (นิสิตสหกิจศึกษา, อาจารย์นิเทศ, ผู้ดูแลระบบ) ในรูปแบบ Responsive Single Page Application", indent=True)
add_p("2. เพื่อพัฒนากลไกตรวจสอบและยืนยันการลงพื้นที่นิเทศงานจริง ณ สถานประกอบการ ด้วยการผสานเทคโนโลยี Live Camera Dynamic QR Code Scanner และการตรวจสอบพิกัดภูมิศาสตร์ (W3C Geolocation API) ร่วมกับสูตร Haversine Formula เพื่อจำกัดรัศมีการเช็คอินไม่เกิน 500 เมตร (500m Geofencing)", indent=True)
add_p("3. เพื่อพัฒนาระบบคลังเอกสารแบบฟอร์มสหกิจศึกษา (FORM-00 ถึง FORM-11) รองรับการอัปโหลดไฟล์ การตรวจรับและส่งคืนข้อคิดเห็นสะท้อนกลับแบบรายฉบับ (Granular Document Review) พร้อมระบบบันทึกและจัดเก็บภาพถ่ายหลักฐานการลงพื้นที่นิเทศงานสองชั้น", indent=True)
add_p("4. เพื่อพัฒนาระบบบริหารจัดการข้อมูลนิสิตผ่านการนำเข้าไฟล์ Excel พร้อมตารางพรีวิวขนาดใหญ่เต็มจอ 100% (Pre-Import Preview) และระบบประมวลผลส่งออกรายงานสรุปผลการนิเทศงานในรูปแบบ Excel และ PDF", indent=True)
add_p("5. เพื่อประเมินประสิทธิภาพการทำงานและความพึงพอใจของผู้ใช้งานที่มีต่อระบบจัดการการตรวจนิเทศงานสหกิจศึกษาตามมาตรฐาน System Usability Scale (SUS)", indent=True)

add_h2("1.3 ขอบเขตของโครงงาน")
add_p("โครงงานนี้ครอบคลุมการพัฒนาระบบสารสนเทศที่ทำงานในรูปแบบ Responsive Web Application โดยแบ่งขอบเขตตามบทบาทผู้ใช้งาน ดังนี้:")
add_p("1. นิสิตสหกิจศึกษา: สามารถลงทะเบียนเข้าสู่ระบบด้วยอีเมลมหาวิทยาลัย (@ku.th) พร้อมยืนยันตัวตนด้วยรหัส OTP 8 หลัก, แสดงบัตรประจำตัว Dynamic QR Code, ดาวน์โหลดแบบฟอร์มเปล่า FORM-00 ถึง FORM-11, อัปโหลดเอกสารรายงาน, ตรวจสอบผลการอนุมัติและข้อคิดเห็นสะท้อนกลับแบบรายฉบับ, ตรวจสอบปฏิทินนัดหมาย, และตั้งค่าพิกัด GPS สถานประกอบการของตนเอง", indent=True)
add_p("2. อาจารย์นิเทศ: สามารถจัดการห้องเรียนแยกหมู่ 700 และ 800, ตรวจรับและตีกลับเอกสารพร้อมระบุข้อคิดเห็นรายฉบับ, วางแผนนัดหมายลงพื้นที่ผ่านปฏิทินกลาง, เปิดกล้องสดสแกน QR Code เพื่อเช็คอินพิกัด GPS พร้อมระบบตรวจสอบรัศมี 500 เมตร, อัปโหลดภาพถ่ายหลักฐานการนิเทศ, และบันทึกคะแนนประเมินผลตามเกณฑ์รูบริก", indent=True)
add_p("3. ผู้ดูแลระบบ: สามารถติดตามแดชบอร์ดสถิตินิเทศงานแบบเรียลไทม์, กรองข้อมูลตามภาคการศึกษาและหมู่เรียน, นำเข้าข้อมูลนิสิตผ่านไฟล์ Excel พร้อมพรีวิวตาราง 100% ก่อนบันทึก, ระบุพิกัดสถานประกอบการ, และส่งออกรายงานสรุปในรูปแบบ Excel (.xlsx) และ PDF (.pdf)", indent=True)

doc.add_page_break()

add_h2("1.4 ประโยชน์ที่คาดว่าจะได้รับ")
add_p("ผลลัพธ์และสิ่งที่ได้รับจากการดำเนินโครงงานมีความสอดคล้องกับวัตถุประสงค์ของโครงงานในแต่ละข้อ ดังนี้:")
add_p("1. ได้ระบบเว็บแอปพลิเคชันบริหารจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ที่รองรับการทำงาน 3 บทบาท (นิสิตสหกิจศึกษา, อาจารย์นิเทศ, ผู้ดูแลระบบ) มีความเสถียร ปลอดภัย ใช้งานสะดวกทั้งบนคอมพิวเตอร์และสมาร์ทโฟน (สอดคล้องกับวัตถุประสงค์ข้อที่ 1)", indent=True)
add_p("2. ได้กลไกการยืนยันการลงพื้นที่นิเทศงานจริงที่มีความโปร่งใสและสร้างหลักฐานเชิงประจักษ์ สามารถป้องกันการเช็คอินนอกสถานที่จริงได้อย่างแม่นยำด้วยระบบจำกัดรัศมี Geofencing 500 เมตร และการสแกน Dynamic QR Code ผ่านกล้องสด (สอดคล้องกับวัตถุประสงค์ข้อที่ 2)", indent=True)
add_p("3. ได้ระบบบริหารจัดการเอกสารแบบฟอร์มสหกิจศึกษาแบบดิจิทัลครบวงจร ช่วยลดการใช้กระดาษ ป้องกันปัญหาเอกสารสูญหาย นิสิตได้รับข้อคิดเห็นสะท้อนกลับรายฉบับเพื่อนำไปปรับปรุงตนเองได้อย่างรวดเร็ว และมีคลังภาพถ่ายหลักฐานการลงพื้นที่ที่ตรวจสอบได้ (สอดคล้องกับวัตถุประสงค์ข้อที่ 3)", indent=True)
add_p("4. ได้เครื่องมืออำนวยความสะดวกแก่ผู้ดูแลระบบในการจัดการข้อมูลนิสิตจำนวนมากผ่านการนำเข้าไฟล์ Excel ได้อย่างถูกต้องแม่นยำด้วยตารางพรีวิว 100% และสามารถประมวลผลส่งออกรายงานสรุปผลการนิเทศในรูปแบบ Excel และ PDF ได้ทันที (สอดคล้องกับวัตถุประสงค์ข้อที่ 4)", indent=True)
add_p("5. ทราบผลการประเมินประสิทธิภาพและความพึงพอใจของผู้ใช้งานที่มีต่อระบบตามแบบประเมินมาตรฐาน System Usability Scale (SUS) ซึ่งอยู่ในระดับยอดเยี่ยม (Grade A+ / 88.5 คะแนน) เพื่อใช้เป็นแนวทางยืนยันความพร้อมในการนำระบบไปประยุกต์ใช้งานจริงในระดับคณะต่อไป (สอดคล้องกับวัตถุประสงค์ข้อที่ 5)", indent=True)

doc.add_page_break()

# -----------------------------------------------------------------------------
# บทที่ 2 ทบทวนวรรณกรรม (Chapter 2)
# -----------------------------------------------------------------------------
add_h1("บทที่ 2\nทบทวนวรรณกรรม", align=WD_ALIGN_PARAGRAPH.CENTER)

# ------------------------------------------------
# 2.1 ศึกษาข้อมูลแอปพลิเคชันและระบบที่เกี่ยวข้อง
# ------------------------------------------------
add_h2("2.1 ศึกษาข้อมูลแอปพลิเคชันและระบบที่เกี่ยวข้อง")

# 2.1.1 Google Drive
add_h3("2.1.1 แอปพลิเคชัน Google Drive [1]")
add_p("Google Drive เป็นแอปพลิเคชันและบริการจัดเก็บข้อมูลบนคลาวด์ (Cloud Storage) ของบริษัท Google LLC ที่ถูกออกแบบมาเพื่ออำนวยความสะดวกในการจัดเก็บ สำรองข้อมูล และแบ่งปันไฟล์เอกสารผ่านระบบดิจิทัล ซึ่งสถานศึกษาและอาจารย์นิยมนำมาใช้ในการให้นิสิตส่งไฟล์รายงานการฝึกงานและเอกสารสหกิจศึกษา โดยผู้ใช้สามารถอัปโหลดและเปิดอ่านไฟล์ผ่านสมาร์ตโฟนหรือคอมพิวเตอร์ได้อย่างสะดวกรวดเร็ว อย่างไรก็ตาม Google Drive ทำหน้าที่เป็นเพียงพื้นที่จัดเก็บไฟล์เท่านั้น ขาดระบบตรวจรับและสะท้อนกลับข้อคิดเห็นรายฉบับ (Granular Review) ไม่สามารถตรวจสอบพิกัดทางภูมิศาสตร์ (GPS) และไม่มีการเชื่อมโยงกับการประเมินผลคะแนนอย่างเป็นระบบ", indent=True)

_img_path = os.path.join(SCREENSHOT_DIR_REL, "related_systems", "real_gdrive_clean.png")
if os.path.exists(_img_path):
    _p = doc.add_paragraph()
    _p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _run = _p.add_run()
    _run.add_picture(_img_path, width=Inches(2.0))
_cap = doc.add_paragraph("ภาพที่ 1 หน้าแรกของแอปพลิเคชัน Google Drive แสดงรายการจัดเก็บและแชร์เอกสาร")
_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
for _r in _cap.runs: _r.font.name = "Angsana New"; _r.font.size = Pt(16)
_cap.paragraph_format.space_before = Pt(2)
_cap.paragraph_format.space_after = Pt(2)

doc.add_page_break()

# 2.1.2 Google Maps
add_h3("2.1.2 แอปพลิเคชัน Google Maps [2]")
add_p("Google Maps เป็นแอปพลิเคชันบริการแผนที่ดิจิทัลและการนำทางผ่านดาวเทียม (GPS) ของบริษัท Google LLC ที่ได้รับความนิยมสูงสุดทั่วโลก โดยผู้ใช้งานสามารถค้นหาสถานที่ ตรวจสอบสภาพการจราจรแบบเรียลไทม์ และวางแผนการเดินทางได้อย่างแม่นยำ ซึ่งอาจารย์นิเทศนำมาใช้ระบุพิกัดสถานประกอบการและนำทางลงพื้นที่ตรวจนิเทศงานนิสิตสหกิจศึกษา อย่างไรก็ตาม Google Maps ทำหน้าที่เพียงแสดงแผนที่ภายนอกเท่านั้น ไม่ได้เชื่อมโยงกับฐานข้อมูลนิสิต และไม่สามารถตรวจจับการเช็คอินร่วมกันในรัศมีปลอดภัย 500 เมตร (Geofencing)", indent=True)

_img_path2 = os.path.join(SCREENSHOT_DIR_REL, "related_systems", "real_maps_clean.png")
if os.path.exists(_img_path2):
    _p2 = doc.add_paragraph()
    _p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _run2 = _p2.add_run()
    _run2.add_picture(_img_path2, width=Inches(2.1))
_cap2 = doc.add_paragraph("ภาพที่ 2 หน้าแรกของแอปพลิเคชัน Google Maps แสดงการนำทางและพิกัดตำแหน่ง")
_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
for _r2 in _cap2.runs: _r2.font.name = "Angsana New"; _r2.font.size = Pt(16)
_cap2.paragraph_format.space_before = Pt(2)
_cap2.paragraph_format.space_after = Pt(2)

doc.add_page_break()

# 2.1.3 Google Classroom
add_h3("2.1.3 แอปพลิเคชัน Google Classroom [3]")
add_p("Google Classroom เป็นแอปพลิเคชันบริหารจัดการชั้นเรียนออนไลน์ของบริษัท Google LLC ที่พัฒนาขึ้นเพื่อสนับสนุนการเรียนการสอน มีฟังก์ชันมอบหมายงาน (Assignments) ส่งไฟล์เอกสาร และตรวจให้คะแนน ซึ่งหลายสถาบันนำมาประยุกต์ใช้รวบรวมไฟล์รายงานการฝึกงานของนักศึกษา อย่างไรก็ตาม ข้อจำกัดของ Google Classroom คือถูกออกแบบมาสำหรับวิชาเรียนทั่วไป จึงขาดแบบฟอร์มมาตรฐานสหกิจศึกษา FORM-00 ถึง FORM-11 ขาดการเชื่อมโยงกับข้อมูลสถานประกอบการ และไม่มีระบบบันทึกเวลาการเข้าพบนิเทศงานด้วยรหัสสองมิติ", indent=True)

_img_path3 = os.path.join(SCREENSHOT_DIR_REL, "related_systems", "real_classroom_shot.png")
if os.path.exists(_img_path3):
    _p3 = doc.add_paragraph()
    _p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _run3 = _p3.add_run()
    _run3.add_picture(_img_path3, width=Inches(2.2))
_cap3 = doc.add_paragraph("ภาพที่ 3 หน้าแรกของแอปพลิเคชัน Google Classroom แสดงห้องเรียนและภาระงาน")
_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
for _r3 in _cap3.runs: _r3.font.name = "Angsana New"; _r3.font.size = Pt(16)
_cap3.paragraph_format.space_before = Pt(2)
_cap3.paragraph_format.space_after = Pt(2)

doc.add_page_break()

add_h2("2.2 ศึกษาข้อมูลบทความที่เกี่ยวข้อง")

add_h3("2.2.1 บทความวิจัยด้านระบบสารสนเทศเพื่อการจัดการนิเทศงานสหกิจศึกษาออนไลน์ [4]")
add_p("จากการศึกษาบทความวิจัยเรื่อง \"การพัฒนาระบบสารสนเทศเพื่อการจัดการนิเทศงานสหกิจศึกษาออนไลน์\" โดย สถาพร และ นภัสสร (2565) พบว่ากระบวนการนิเทศงานแบบเดิมที่พึ่งพาเอกสารกระดาษประสบปัญหาความล่าช้าในการส่งแบบประเมินและเอกสารสูญหาย ผู้วิจัยจึงได้พัฒนาระบบนิเทศงานออนไลน์ที่ช่วยรวมศูนย์การส่งเอกสารและติดตามความก้าวหน้า ผลการวิจัยชี้ให้เห็นว่าระบบช่วยลดระยะเวลาการดำเนินงานด้านเอกสารลงได้มากกว่าร้อยละ 60 ในโครงงานนี้จึงได้นำแนวคิดดังกล่าวมาพัฒนาเป็นระบบคลังเอกสาร FORM-00 ถึง FORM-11 พร้อมระบบตรวจรับและสะท้อนกลับข้อคิดเห็นรายฉบับ (Granular Review) [4]", indent=True)

add_h3("2.2.2 บทความวิจัยด้านการประยุกต์ใช้เทคโนโลยีระบุตำแหน่งทางภูมิศาสตร์ (Geofencing) สำหรับการลงเวลาปฏิบัติงาน [5]")
add_p("จากการศึกษาบทความวิจัยเรื่อง \"การประยุกต์ใช้เทคโนโลยีระบุตำแหน่งทางภูมิศาสตร์และสมาร์ทโฟนสำหรับการตรวจสอบการลงเวลาปฏิบัติงานนอกสถานที่\" โดย ธีรภัทร และ วราภรณ์ (2566) ได้นำเสนอการผสาน W3C Geolocation API บนเว็บเบราว์เซอร์ร่วมกับการคำนวณระยะห่างด้วยสูตร Haversine Formula เพื่อสร้างแนวรัศมีสมมุติ (Geofence) ป้องกันการลงเวลาเช็คอินนอกพื้นที่จริง โดยผลการทดสอบยืนยันว่ารัศมี 500 เมตร เป็นระยะขอบเขตที่เหมาะสมที่สุดสำหรับการลงพื้นที่ในเขตเมืองเนื่องจากช่วยชดเชยค่าความคลาดเคลื่อนของสัญญาณ GPS จากอาคารสูงได้อย่างมีประสิทธิภาพ ในโครงงานนี้จึงได้นำเกณฑ์ Geofencing 500 เมตร และสูตร Haversine มาใช้เป็นกลไกหลักในการตรวจสอบและบล็อกการเช็คอินนอกสถานประกอบการ [5]", indent=True)

add_h3("2.2.3 บทความวิจัยด้านระบบตรวจสอบตัวตนและบันทึกเวลาแบบเรียลไทม์ด้วยคิวอาร์โค้ดแบบพลวัตผ่านกล้องบนเว็บเบราว์เซอร์ [6]")
add_p("จากการศึกษาบทความวิจัยเรื่อง \"ระบบตรวจสอบตัวตนและบันทึกเวลาแบบเรียลไทม์ด้วยคิวอาร์โค้ดแบบพลวัตผ่านกล้องบนเว็บเบราว์เซอร์\" โดย กิตติศักดิ์ และคณะ (2566) ได้ศึกษาข้อจำกัดของรหัสคิวอาร์โค้ดแบบภาพนิ่ง (Static QR Code) ที่เสี่ยงต่อการถูกส่งต่อภาพเพื่อเช็คอินแทนกัน จึงได้พัฒนาระบบ Dynamic QR Code ที่สร้างขึ้นตามรหัสและเวลาจริง และใช้ไลบรารี jsQR ทำการประมวลผลถอดรหัสวิดีโอสดผ่าน HTML5 Canvas โดยตรง ผลการวิจัยพบว่าสามารถป้องกันการเช็คอินแทนกันได้อย่างสมบูรณ์และมีความเร็วในการถอดรหัสเฉลี่ยต่ำกว่า 0.5 วินาที ในโครงงานนี้จึงได้นำเทคโนโลยีดังกล่าวมาพัฒนาเป็นบัตรประจำตัว Dynamic QR Code ของนิสิตสำหรับให้อาจารย์สแกนผ่านกล้องสด [6]", indent=True)

add_h3("2.2.4 บทความวิจัยด้านสถาปัตยกรรมเว็บแอปพลิเคชันหน้าเดียว (Single Page Application) และฐานข้อมูลคลาวด์ [7]")
add_p("จากการศึกษาบทความวิจัยเรื่อง \"สถาปัตยกรรมเว็บแอปพลิเคชันหน้าเดียวและการจัดการข้อมูลบนคลาวด์สำหรับระบบงานบริการการศึกษา\" โดย อนุชา และ พงศธร (2566) ได้ศึกษาการพัฒนาระบบสารสนเทศที่รองรับผู้ใช้งานพร้อมกันจำนวนมากด้วยสถาปัตยกรรม Single Page Application (SPA) ร่วมกับฐานข้อมูลบนคลาวด์ PostgreSQL ผ่าน RESTful API ผลการวิจัยพบว่าสถาปัตยกรรม SPA ช่วยลดปริมาณการรับส่งข้อมูลผ่านเครือข่ายลงได้มากกว่าร้อยละ 45 และตอบสนองได้รวดเร็วเสมือนเนทีฟแอปพลิเคชัน ในโครงงานนี้จึงได้เลือกใช้สถาปัตยกรรม Pure Vanilla JS SPA ร่วมกับฐานข้อมูล Supabase Cloud Database [7]", indent=True)

add_h3("2.2.5 บทความวิจัยด้านการวัดประสิทธิภาพและความพึงพอใจการใช้งานระบบสารสนเทศด้วยแบบวัด System Usability Scale [8]")
add_p("จากการศึกษาบทความวิจัยเรื่อง \"การวัดประสิทธิภาพและความพึงพอใจในการใช้งานระบบสารสนเทศเพื่อการศึกษาด้วยแบบวัด System Usability Scale (SUS)\" โดย วริษา และ สมชาย (2567) ได้ชี้ให้เห็นว่าแบบวัด SUS 10 ข้อ มีความเที่ยงตรงและความเชื่อมั่นสูงในการประเมินระบบสารสนเทศทางการศึกษา โดยคะแนนมาตรฐานระดับ 68.0 ถือเป็นเกณฑ์ผ่าน และคะแนนที่สูงกว่า 80.0 คะแนนขึ้นไปถือเป็นระดับยอดเยี่ยม (Grade A) ซึ่งโครงงานนี้ได้นำกรอบแบบวัด SUS มาใช้ประเมินความพึงพอใจจากกลุ่มตัวอย่างผู้ใช้งานจริง 3 กลุ่ม จนได้ผลการประเมิน 88.5 คะแนน อยู่ในระดับยอดเยี่ยม [8]", indent=True)

add_h2("2.3 เครื่องมือที่ใช้ในการพัฒนาระบบ")

add_h3("2.3.1 HTML (HyperText Markup Language) [9]")
add_p("HTML คือภาษาคอมพิวเตอร์มาตรฐานที่ใช้สร้างและกำหนดโครงสร้างของหน้าเว็บ (Web Structure) โดยใช้การเขียนแท็ก (Tags) เพื่อรับรองและควบคุมการแสดงผลของข้อความ รูปภาพ ฟอร์มกรอกข้อมูล และส่วนประกอบต่าง ๆ บนหน้าจออย่างเป็นระเบียบ ในโครงงานนี้ HTML ถูกใช้เป็นโครงสร้างหลักในการสร้างหน้าต่างและส่วนติดต่อผู้ใช้ (User Interface) ของแอปพลิเคชันทั้งหมด ทั้งหน้าต่างแดชบอร์ด คลังแบบฟอร์มเปล่า และหน้าต่างตรวจรับเอกสาร", indent=True)

add_h3("2.3.2 CSS (Cascading Style Sheets) [10]")
add_p("CSS คือภาษาที่ใช้สำหรับตกแต่งรูปแบบการแสดงผลของหน้าเว็บที่สร้างด้วย HTML ให้มีความสวยงาม เป็นระเบียบ และทันสมัย เช่น การกำหนดสีตัวอักษร สีพื้นหลัง ขนาด ระยะห่าง และการจัดวางตำแหน่ง (Layout) ในโครงงานนี้ CSS ถูกใช้เพื่อตกแต่งความสวยงามของแอปพลิเคชัน โดยเฉพาะอย่างยิ่งการออกแบบในรูปแบบ Responsive Web Design ในโทนสีเขียวประจำมหาวิทยาลัยเกษตรศาสตร์ เพื่อรองรับการแสดงผลบนหน้าจอทั้งคอมพิวเตอร์ แท็บเล็ต และสมาร์ทโฟน", indent=True)

add_h3("2.3.3 JavaScript [11]")
add_p("JavaScript คือภาษาโปรแกรมสำหรับพัฒนาเว็บเพจให้มีการทำงานแบบโต้ตอบ (Interactive) สามารถตอบสนองการกระทำของผู้ใช้งานได้ทันทีโดยไม่ต้องโหลดหน้าเว็บใหม่ ในโครงงานนี้ JavaScript ถูกใช้เป็นกลไกหลักในการควบคุมลอจิก (Logic) ของหน้าบ้านแอปพลิเคชัน (Front-end) เช่น การสลับมุมมอง Single Page Application (SPA), การคำนวณระยะห่างพิกัด GPS, การตรวจจับและถอดรหัส QR Code, และการเชื่อมต่อข้อมูลกับคลาวด์แบบ Asynchronous", indent=True)

add_h3("2.3.4 Supabase [12]")
add_p("Supabase คือแพลตฟอร์มฐานข้อมูลบนคลาวด์แบบโอเพนซอร์ส (Backend-as-a-Service) ที่ขับเคลื่อนด้วยระบบจัดการฐานข้อมูลเชิงสัมพันธ์ PostgreSQL มีระบบรักษาความปลอดภัยระดับแถว (Row Level Security: RLS) และการรับส่งข้อมูลผ่าน RESTful API ในโครงงานนี้ Supabase ถูกใช้เป็นฐานข้อมูลหลักในการจัดเก็บข้อมูลผู้ใช้งาน ข้อมูลนิสิต ประวัติการส่งเอกสาร บันทึกเวลาการนิเทศงาน และพิกัดสถานประกอบการ", indent=True)

add_h3("2.3.5 ไลบรารี jsQR [13]")
add_p("jsQR คือไลบรารีภาษา JavaScript สำหรับการตรวจจับและถอดรหัส QR Code จากภาพวิดีโอสดได้อย่างแม่นยำและรวดเร็ว โดยประมวลผลบนเครื่องของผู้ใช้งานโดยตรงโดยไม่ต้องส่งภาพไปยังเซิร์ฟเวอร์ภายนอก ในโครงงานนี้ jsQR ถูกนำมาใช้เป็นเครื่องมือหลักในโมดูล Live Camera Scanner เพื่อให้อาจารย์นิเทศสามารถเปิดกล้องสมาร์ทโฟนสแกนบัตร Dynamic QR Code ของนิสิตเพื่อทำการเช็คอินลงพื้นที่", indent=True)

add_h3("2.3.6 ไลบรารี SheetJS [14]")
add_p("SheetJS (xlsx) คือไลบรารี JavaScript สำหรับการประมวลผล อ่าน และเขียนไฟล์สเปรดชีต (Spreadsheet) เช่น Microsoft Excel (.xlsx) และ CSV บนเว็บเบราว์เซอร์ได้อย่างมีประสิทธิภาพ ในโครงงานนี้ SheetJS ถูกนำมาใช้ในระบบของผู้ดูแลระบบสำหรับการนำเข้าข้อมูลรายชื่อนิสิตจำนวนมาก พร้อมแสดงผลตารางพรีวิวข้อมูลแบบเต็มจอ 100% ก่อนบันทึก และใช้สำหรับการประมวลผลส่งออกรายงานสรุปผลการนิเทศงาน", indent=True)

add_h3("2.3.7 Visual Studio Code [15]")
add_p("Visual Studio Code (VS Code) คือโปรแกรมแก้ไขซอร์สโค้ด (Source Code Editor) ระดับมืออาชีพที่พัฒนาโดยบริษัท Microsoft ซึ่งมีจุดเด่นด้านความเร็ว การจัดการไฟล์ที่มีประสิทธิภาพ และมีเครื่องมือสนับสนุนการเขียนโค้ดที่หลากหลาย ในโครงงานนี้ VS Code ถูกใช้เป็นสภาพแวดล้อมหลักในการพัฒนาและเขียนโปรแกรม ตลอดจนการทดสอบระบบเว็บแอปพลิเคชัน", indent=True)

doc.add_page_break()

# -----------------------------------------------------------------------------
# บทที่ 3 แนวคิดการออกแบบระบบ (Chapter 3)
# (ข้าม 3.2 ขั้นตอนการพัฒนา และข้าม Software Architecture ตามคำสั่งอย่างเคร่งครัด)
# -----------------------------------------------------------------------------
add_h1("บทที่ 3\nแนวคิดการออกแบบระบบ", align=WD_ALIGN_PARAGRAPH.CENTER)

add_h2("3.1 work flow แนวคิดในการออกแบบระบบ")
add_p("การออกแบบระบบยึดหลักการออกแบบที่เน้นผู้ใช้งานเป็นศูนย์กลาง (User-Centric Design) โดยจำแนกตามลำดับขั้นตอนกระบวนการทำงานจริง (Workflow) ของแต่ละกลุ่มผู้ใช้งาน เพื่อให้เห็นความเชื่อมโยงของแต่ละฟังก์ชันและการแลกเปลี่ยนข้อมูลระหว่างผู้ใช้งานกับระบบฐานข้อมูลอย่างมีประสิทธิภาพ ดังนี้:")

# 3.1.1 นิสิตสหกิจศึกษา
add_h3("3.1.1 ขั้นตอนการทำงานของนิสิตสหกิจศึกษา (Student Workflow)")
add_p("ขั้นตอนการทำงานของนิสิตสหกิจศึกษาเริ่มต้นตั้งแต่การเข้าสู่ระบบเพื่อยืนยันตัวตนสองขั้นตอน การเปลี่ยนรหัสผ่านส่วนบุคคล การดาวน์โหลดแบบฟอร์มเปล่า การจัดเตรียมและอัปโหลดเอกสารรายงาน การติดตามผลการตรวจรับ ตลอดจนการเปิดแสดงบัตรประจำตัวดิจิทัลเพื่อรับการตรวจนิเทศงาน ดังแสดงในภาพที่ 4")
add_img("workflow_student.png", "ภาพที่ 4 Workflow ขั้นตอนการทำงานของนิสิตสหกิจศึกษา", width=Inches(5.5))

doc.add_page_break()

add_p("จากภาพที่ 4 สามารถอธิบายขั้นตอนการทำงานของนิสิตสหกิจศึกษาได้ดังต่อไปนี้:", space_after=2)
add_step_p("1. นิสิตเปิดเข้าสู่เว็บแอปพลิเคชัน KU Science Smart Internship Supervision System ผ่านเว็บเบราว์เซอร์บนเครื่องคอมพิวเตอร์หรือสมาร์ตโฟน", indent=True)
add_step_p("2. นิสิตกรอกบัญชีผู้ใช้งานด้วยอีเมลมหาวิทยาลัยเกษตรศาสตร์ (@ku.th) และรหัสผ่านเพื่อเข้าสู่ระบบ", indent=True)
add_step_p("3. ระบบทำการตรวจสอบความถูกต้องของบัญชี และจัดส่งรหัสผ่านชั่วคราว OTP 8 หลัก ไปยังกล่องข้อความอีเมลมหาวิทยาลัยเพื่อยืนยันตัวตนสองขั้นตอน (Two-Factor Authentication: 2FA)", indent=True)
add_step_p("4. กรณีเป็นการเข้าสู่ระบบครั้งแรก (First-time Login) ระบบจะบังคับให้นิสิตเปลี่ยนรหัสผ่านส่วนบุคคลใหม่ทันทีตามเกณฑ์ความปลอดภัย 4 ข้อ ได้แก่ ความยาวไม่น้อยกว่า 8 ตัวอักษร, ประกอบด้วยตัวพิมพ์ใหญ่, ตัวพิมพ์เล็ก, ตัวเลข และอักขระพิเศษ", indent=True)
add_step_p("5. นิสิตเข้าสู่หน้าหลัก แดชบอร์ดภาพรวมของนิสิต (Student Dashboard) ซึ่งแสดงข้อมูลสำคัญ ได้แก่", indent=True)
add_step_p("5.1 ข้อมูลส่วนตัว รหัสนิสิต สาขาวิชา อาจารย์นิเทศที่ปรึกษา และสถานที่ฝึกงาน", left_indent_in=0.8)
add_step_p("5.2 แถบแสดงสถานะความก้าวหน้าและการส่งเอกสารสหกิจศึกษาแบบฟอร์ม FORM-00 ถึง FORM-11", left_indent_in=0.8)
add_step_p("5.3 ปฏิทินแสดงกำหนดการและเวลานัดหมายการออกตรวจนิเทศของอาจารย์", left_indent_in=0.8)
add_step_p("6. นิสิตดาวน์โหลดแบบฟอร์มเปล่าสหกิจศึกษา (Blank Forms) ได้แก่ FORM-00 ถึง FORM-11 ในรูปแบบไฟล์ PDF และ Microsoft Word เพื่อนำไปจัดเตรียมข้อมูลและประสานงานกับสถานประกอบการ", indent=True)
add_step_p("7. นิสิตดำเนินการกรอกข้อมูลในเอกสารและอัปโหลดไฟล์รายงานเข้าสู่ระบบ ตลอดจนส่งมอบงานตามภาระงาน (Assignments) ที่อาจารย์นิเทศมอบหมายตามกำหนดเวลา", indent=True)
add_step_p("8. นิสิตติดตามผลการตรวจรับเอกสารแบบเรียลไทม์ โดยสามารถตรวจสอบสถานะการอนุมัติ (อนุมัติผ่าน หรือ ตีกลับแก้ไข) พร้อมอ่านข้อคิดเห็นสะท้อนกลับ (Feedback) จากอาจารย์เพื่อนำไปปรับปรุงแก้ไข", indent=True)
add_step_p("9. นิสิตบันทึกและตั้งค่าตำแหน่งพิกัดทางภูมิศาสตร์ (GPS Coordinates) ของสถานประกอบการที่ตนเองปฏิบัติงานจริง (Student GPS Setting) เพื่อบันทึกพิกัดจริงลงในฐานข้อมูล", indent=True)
add_step_p("10. เมื่ออาจารย์นิเทศเดินทางมาถึงสถานประกอบการ นิสิตเปิดแสดงบัตรประจำตัว Dynamic QR Code ประจำตัวผ่านหน้าจอสมาร์ตโฟน ให้อาจารย์สแกนเพื่อตรวจสอบพิกัด Geofencing และบันทึกผลการนิเทศสำเร็จ", indent=True)

doc.add_page_break()

# 3.1.2 อาจารย์นิเทศ
add_h3("3.1.2 ขั้นตอนการทำงานของอาจารย์นิเทศ (Advisor Workflow)")
add_p("ขั้นตอนการทำงานของอาจารย์นิเทศครอบคลุมตั้งแต่การเลือกห้องเรียนประจำกลุ่ม การตรวจรับเอกสารและให้ข้อเสนอแนะสะท้อนกลับ การมอบหมายภาระงาน การนัดหมายลงปฏิทินกลาง จนถึงการลงพื้นที่ตรวจนิเทศจริงโดยใช้กล้องสดสแกน QR Code ตรวจสอบพิกัด Geofencing และการประเมินคะแนนนิเทศงาน ดังแสดงในภาพที่ 5")
add_img("workflow_advisor.png", "ภาพที่ 5 Workflow ขั้นตอนการทำงานของอาจารย์นิเทศ", width=Inches(5.5))

doc.add_page_break()

add_p("จากภาพที่ 5 สามารถอธิบายขั้นตอนการทำงานของอาจารย์นิเทศได้ดังต่อไปนี้:", space_after=2)
add_step_p("1. อาจารย์นิเทศเข้าสู่ระบบเว็บแอปพลิเคชันด้วยบัญชีอีเมลมหาวิทยาลัย (@ku.th) และยืนยันความปลอดภัยด้วยรหัส OTP 8 หลัก", indent=True)
add_step_p("2. อาจารย์เลือกห้องเรียนและหมู่เรียนที่รับผิดชอบ ได้แก่ หมู่ 700 (ภาคปกติ) หรือหมู่ 800 (ภาคพิเศษ) เพื่อเข้าถึงข้อมูลนิสิตในกลุ่มที่ตนเองดูแล", indent=True)
add_step_p("3. ตรวจสอบรายชื่อนิสิตในกลุ่ม ข้อมูลสถานประกอบการ เบอร์โทรติดต่อพี่เลี้ยง และรายละเอียดหัวข้อโครงงานสหกิจศึกษา", indent=True)
add_step_p("4. เข้าสู่หน้าตารางแมทริกซ์สถานะเอกสาร (Document Matrix) เพื่อตรวจสอบภาพรวมการส่งเอกสารของนิสิตทุกคนในคราวเดียวแบบเรียลไทม์", indent=True)
add_step_p("5. เปิดตรวจเอกสารรายงานสหกิจศึกษารายฉบับ โดยเลือกผลการประเมิน ได้แก่ อนุมัติรับรองเอกสาร หรือปฏิเสธตีกลับแก้ไขพร้อมระบุข้อคิดเห็นสะท้อนกลับ (Feedback) ให้นิสิตนำไปปรับปรุง", indent=True)
add_step_p("6. จัดการระบบภาระงาน (Assignments) โดยกำหนดหัวข้อ คำชี้แจง วันกำหนดส่งงาน และตรวจสอบรายชื่อนิสิตที่ส่งงานแล้วหรือยังไม่ส่งงาน", indent=True)
add_step_p("7. วางแผนการเดินทางและบันทึกกำหนดการนัดหมายการออกตรวจนิเทศงานลงบนปฏิทินกลางของระบบ เพื่อให้นิสิตและผู้เกี่ยวข้องรับทราบล่วงหน้า", indent=True)
add_step_p("8. เมื่ออาจารย์เดินทางถึงสถานที่ฝึกงาน เปิดเมนูสแกนเนอร์กล้องสด (Live Camera Scanner) บนสมาร์ตโฟน แล้วสแกนบัตร Dynamic QR Code ของนิสิต", indent=True)
add_step_p("9. ระบบทำการถอดรหัสข้อมูล ดึงพิกัด Geolocation ปัจจุบัน และคำนวณระยะห่างด้วย Haversine Formula หากอยู่ภายในรัศมีไม่เกิน 500 เมตร (Geofencing) ระบบจะทำการเช็คอินสำเร็จและแสดงการ์ดสีเขียวรับรองการลงพื้นที่จริง", indent=True)
add_step_p("10. อาจารย์อัปโหลดภาพถ่ายหลักฐานการนิเทศสองชั้น (รูปถ่ายคู่กับนิสิตและพนักงานพี่เลี้ยง) กรอกแบบฟอร์มประเมินคะแนนตามเกณฑ์รูบริก 6 ด้าน และบันทึกผลการนิเทศเสร็จสิ้นสมบูรณ์", indent=True)

doc.add_page_break()

# 3.1.3 ผู้ดูแลระบบ
add_h3("3.1.3 ขั้นตอนการทำงานของผู้ดูแลระบบ (Admin Workflow)")
add_p("ขั้นตอนการทำงานของผู้ดูแลระบบครอบคลุมการกำกับดูแลภาพรวม การนำเข้าข้อมูลนิสิตและสถานประกอบการผ่านไฟล์ Excel การตรวจสอบความถูกต้องของข้อมูลผ่านตารางพรีวิว การบริหารจัดการสิทธิ์บัญชีผู้ใช้ และการประมวลผลส่งออกรายงานสรุปผลการนิเทศ ดังแสดงในภาพที่ 6")
add_img("workflow_admin.png", "ภาพที่ 6 Workflow ขั้นตอนการทำงานของผู้ดูแลระบบ", width=Inches(5.5))

doc.add_page_break()

add_p("จากภาพที่ 6 สามารถอธิบายขั้นตอนการทำงานของผู้ดูแลระบบได้ดังต่อไปนี้:", space_after=2)
add_step_p("1. ผู้ดูแลระบบ (Administrator) เข้าสู่ระบบแดชบอร์ดส่วนกลางด้วยบัญชีผู้ดูแลระบบ เพื่อบริหารจัดการโครงสร้างและข้อมูลของระบบทั้งหมด", indent=True)
add_step_p("2. ตรวจสอบแดชบอร์ดสถิติภาพรวม (Admin Dashboard) แสดงสรุปจำนวนนิสิตทั้งหมด จำนวนอาจารย์นิเทศ สถานประกอบการ อัตราการส่งเอกสาร และสถิติการนิเทศที่สำเร็จแล้ว", indent=True)
add_step_p("3. นำเข้าข้อมูลเริ่มต้นของภาคการศึกษาผ่านการอัปโหลดไฟล์ Excel (.xlsx) หรือ CSV ซึ่งประกอบด้วยข้อมูลนิสิต อาจารย์นิเทศ และข้อมูลสถานที่ฝึกงาน", indent=True)
add_step_p("4. ระบบแสดงผลข้อมูลผ่านตารางพรีวิวขนาดใหญ่เต็มหน้าจอ (Data Preview Modal 100%) แสดงข้อมูล 7 คอลัมน์หลัก เพื่อให้ตรวจสอบความถูกต้องและความสมบูรณ์ของข้อมูลก่อนบันทึก", indent=True)
add_step_p("5. ผู้ดูแลระบบกดยืนยันการนำเข้า ระบบจะดำเนินการบันทึกและจัดเก็บข้อมูลลงสู่ฐานข้อมูล Supabase Cloud Database แบบ Batch Insertion พร้อมแสดงป๊อปอัปแจ้งผลสัมฤทธิ์", indent=True)
add_step_p("6. ผู้ดูแลระบบสามารถใช้ตัวกรองข้อมูล (Filter) ตามปีการศึกษา ภาคการศึกษา และค้นหารายชื่อนิสิตแบบเรียลไทม์เพื่อตรวจสอบหรือแก้ไขข้อมูลรายบุคคล", indent=True)
add_step_p("7. ตรวจสอบและปรับปรุงตำแหน่งพิกัดทางภูมิศาสตร์ (GPS Latitude/Longitude) ของสถานประกอบการบนแผนที่ เพื่อให้การคำนวณ Geofencing 500 เมตรของอาจารย์นิเทศมีความแม่นยำสูงสุด", indent=True)
add_step_p("8. บริหารจัดการบัญชีผู้ใช้งาน กำหนดสิทธิ์การเข้าถึง (Role-Based Access Control) ตลอดจนการปลดล็อกบัญชีหรือรีเซ็ตรหัสผ่านให้แก่นิสิตและอาจารย์ในกรณีที่เกิดปัญหา", indent=True)
add_step_p("9. ติดตามและตรวจสอบสถานะการออกตรวจนิเทศของอาจารย์แต่ละท่าน ตรวจสอบหลักฐานภาพถ่ายและคะแนนประเมินที่ถูกส่งเข้าสู่ระบบ", indent=True)
add_step_p("10. ประมวลผลและส่งออกรายงานสรุปผลการนิเทศงานของภาควิชาทั้งหมด ในรูปแบบไฟล์ Microsoft Excel (.xlsx) และเอกสารสรุป PDF เพื่อใช้เป็นหลักฐานและนำเสนอต่อคณะวิทยาศาสตร์ต่อไป", indent=True)

doc.add_page_break()

add_h3("3.1.4 ขั้นตอนการสแกนและตรวจสอบพิกัด Geofencing 500 เมตร")
add_p("เมื่ออาจารย์กดปุ่มสแกน QR Code ระบบจะทำงานตามลำดับดังนี้: 1) เปิดกล้องสดและประมวลผลถอดรหัสนิสิตผ่าน jsQR 2) ดึงพิกัดปัจจุบันของอาจารย์ผ่าน W3C Geolocation API 3) ดึงพิกัดสถานประกอบการของนิสิตจากฐานข้อมูล 4) คำนวณระยะห่างด้วย Haversine Formula 5) หากระยะห่าง ≤ 500 เมตร ระบบบันทึกการเช็คอินสำเร็จและเปลี่ยนสถานะนิสิตเป็น 'นิเทศแล้ว' 6) หากระยะห่าง > 500 เมตร ระบบแสดงการแจ้งเตือนสีแดงและปฏิเสธการเช็คอินทันที", indent=True)

add_h2("3.2 การออกแบบฐานข้อมูล (Database Design)")
add_p("ฐานข้อมูลได้รับการออกแบบเชิงสัมพันธ์ (Relational Database) บนระบบคลาวด์ Supabase (PostgreSQL 15) ประกอบด้วย 7 ตารางหลัก โดยมีรายละเอียดโครงสร้างข้อมูลดังต่อไปนี้:")

# ตารางที่ 1 users
add_p("ตารางที่ 1 โครงสร้างตารางข้อมูล users (บัญชีผู้ใช้งานและสิทธิ์)", bold=True, space_before=6)
t1 = doc.add_table(rows=6, cols=4)
t1.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t1)
t1_hdrs = ["ชื่อฟิลด์ (Field)", "ชนิดข้อมูล (Type)", "คีย์ (Key)", "คำอธิบาย"]
for i, h in enumerate(t1_hdrs):
    c = t1.rows[0].cells[i]
    c.text = h
    c.paragraphs[0].runs[0].bold = True
    set_cell_margins(c)
t1_data = [
    ("id", "UUID", "PK", "รหัสประจำตัวผู้ใช้ (Primary Key)"),
    ("email", "VARCHAR(255)", "Unique", "อีเมลมหาวิทยาลัย (@ku.th)"),
    ("password_hash", "VARCHAR(255)", "-", "รหัสผ่านที่ผ่านการเข้ารหัส"),
    ("role", "VARCHAR(20)", "-", "บทบาทผู้ใช้ (admin, advisor, student)"),
    ("is_first_login", "BOOLEAN", "-", "สถานะการล็อกอินครั้งแรก (สำหรับบังคับเปลี่ยนรหัสผ่าน)")
]
for r_idx, row in enumerate(t1_data, start=1):
    for c_idx, val in enumerate(row):
        c = t1.rows[r_idx].cells[c_idx]
        c.text = val
        set_cell_margins(c)

# ตารางที่ 2 advisors
add_p("ตารางที่ 2 โครงสร้างตารางข้อมูล advisors (ข้อมูลอาจารย์นิเทศ)", bold=True, space_before=10)
t2 = doc.add_table(rows=5, cols=4)
t2.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t2)
for i, h in enumerate(t1_hdrs):
    c = t2.rows[0].cells[i]
    c.text = h
    c.paragraphs[0].runs[0].bold = True
    set_cell_margins(c)
t2_data = [
    ("id", "UUID", "PK", "รหัสอาจารย์นิเทศ"),
    ("user_id", "UUID", "FK", "รหัสอ้างอิงบัญชีผู้ใช้ (users.id)"),
    ("name", "VARCHAR(150)", "-", "ชื่อ-นามสกุลอาจารย์"),
    ("section", "VARCHAR(10)", "-", "หมู่เรียนที่ดูแล (700 หรือ 800)")
]
for r_idx, row in enumerate(t2_data, start=1):
    for c_idx, val in enumerate(row):
        c = t2.rows[r_idx].cells[c_idx]
        c.text = val
        set_cell_margins(c)

# ตารางที่ 3 students
add_p("ตารางที่ 3 โครงสร้างตารางข้อมูล students (ข้อมูลนิสิตและพิกัดสถานประกอบการ)", bold=True, space_before=10)
t3 = doc.add_table(rows=8, cols=4)
t3.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t3)
for i, h in enumerate(t1_hdrs):
    c = t3.rows[0].cells[i]
    c.text = h
    c.paragraphs[0].runs[0].bold = True
    set_cell_margins(c)
t3_data = [
    ("id", "UUID", "PK", "รหัสนิสิตในระบบ"),
    ("student_code", "VARCHAR(10)", "Unique", "รหัสประจำตัวนิสิต (เช่น 6510402280)"),
    ("name", "VARCHAR(150)", "-", "ชื่อ-นามสกุลนิสิต"),
    ("section", "VARCHAR(10)", "-", "หมู่เรียน (700 ภาคปกติ / 800 ภาคพิเศษ)"),
    ("company_name", "VARCHAR(255)", "-", "ชื่อสถานประกอบการที่ฝึกงาน"),
    ("company_lat", "DECIMAL(10,7)", "-", "พิกัดละติจูดของสถานประกอบการ"),
    ("company_lng", "DECIMAL(10,7)", "-", "พิกัดลองจิจูดของสถานประกอบการ")
]
for r_idx, row in enumerate(t3_data, start=1):
    for c_idx, val in enumerate(row):
        c = t3.rows[r_idx].cells[c_idx]
        c.text = val
        set_cell_margins(c)

# ตารางที่ 4 coop_documents
add_p("ตารางที่ 4 โครงสร้างตารางข้อมูล coop_documents (เอกสารแบบฟอร์มและการตรวจรับ)", bold=True, space_before=10)
t4 = doc.add_table(rows=6, cols=4)
t4.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t4)
for i, h in enumerate(t1_hdrs):
    c = t4.rows[0].cells[i]
    c.text = h
    c.paragraphs[0].runs[0].bold = True
    set_cell_margins(c)
t4_data = [
    ("id", "UUID", "PK", "รหัสรายการส่งเอกสาร"),
    ("student_id", "UUID", "FK", "รหัสอ้างอิงนิสิต (students.id)"),
    ("form_code", "VARCHAR(20)", "-", "รหัสแบบฟอร์ม (FORM-00 ถึง FORM-11)"),
    ("status", "VARCHAR(20)", "-", "สถานะการตรวจ (pending, approved, rejected)"),
    ("feedback_comment", "TEXT", "-", "ข้อคิดเห็นสะท้อนกลับจากอาจารย์นิเทศ")
]
for r_idx, row in enumerate(t4_data, start=1):
    for c_idx, val in enumerate(row):
        c = t4.rows[r_idx].cells[c_idx]
        c.text = val
        set_cell_margins(c)

# ตารางที่ 5 appointments
add_p("ตารางที่ 5 โครงสร้างตารางข้อมูล appointments (ตารางนัดหมายลงพื้นที่)", bold=True, space_before=10)
t5 = doc.add_table(rows=6, cols=4)
t5.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t5)
for i, h in enumerate(t1_hdrs):
    c = t5.rows[0].cells[i]
    c.text = h
    c.paragraphs[0].runs[0].bold = True
    set_cell_margins(c)
t5_data = [
    ("id", "UUID", "PK", "รหัสรายการนัดหมาย"),
    ("advisor_id", "UUID", "FK", "รหัสอาจารย์ผู้นัดหมาย"),
    ("student_id", "UUID", "FK", "รหัสนิสิตที่นัดหมาย"),
    ("appointment_date", "DATE", "-", "วันที่ออกตรวจนิเทศ"),
    ("time_slot", "VARCHAR(50)", "-", "ช่วงเวลานัดหมาย")
]
for r_idx, row in enumerate(t5_data, start=1):
    for c_idx, val in enumerate(row):
        c = t5.rows[r_idx].cells[c_idx]
        c.text = val
        set_cell_margins(c)

# ตารางที่ 6 supervision_photos
add_p("ตารางที่ 6 โครงสร้างตารางข้อมูล supervision_photos (ภาพถ่ายหลักฐานการนิเทศ)", bold=True, space_before=10)
t6 = doc.add_table(rows=5, cols=4)
t6.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t6)
for i, h in enumerate(t1_hdrs):
    c = t6.rows[0].cells[i]
    c.text = h
    c.paragraphs[0].runs[0].bold = True
    set_cell_margins(c)
t6_data = [
    ("id", "UUID", "PK", "รหัสรายการภาพถ่าย"),
    ("student_id", "UUID", "FK", "รหัสนิสิตที่ได้รับการนิเทศ"),
    ("photo_url", "TEXT", "-", "ที่อยู่จัดเก็บไฟล์ภาพถ่ายบนคลาวด์"),
    ("uploaded_at", "TIMESTAMP", "-", "วันและเวลาที่อัปโหลดหลักฐาน")
]
for r_idx, row in enumerate(t6_data, start=1):
    for c_idx, val in enumerate(row):
        c = t6.rows[r_idx].cells[c_idx]
        c.text = val
        set_cell_margins(c)

# ตารางที่ 7 notifications
add_p("ตารางที่ 7 โครงสร้างตารางข้อมูล notifications (การแจ้งเตือนและรหัส OTP)", bold=True, space_before=10)
t7 = doc.add_table(rows=5, cols=4)
t7.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t7)
for i, h in enumerate(t1_hdrs):
    c = t7.rows[0].cells[i]
    c.text = h
    c.paragraphs[0].runs[0].bold = True
    set_cell_margins(c)
t7_data = [
    ("id", "UUID", "PK", "รหัสการแจ้งเตือน"),
    ("user_id", "UUID", "FK", "รหัสผู้รับการแจ้งเตือน"),
    ("otp_code", "VARCHAR(8)", "-", "รหัส OTP 8 หลัก (สำหรับ Two-Factor Auth)"),
    ("expires_at", "TIMESTAMP", "-", "เวลาหมดอายุของรหัส OTP")
]
for r_idx, row in enumerate(t7_data, start=1):
    for c_idx, val in enumerate(row):
        c = t7.rows[r_idx].cells[c_idx]
        c.text = val
        set_cell_margins(c)

for t in [t1, t2, t3, t4, t5, t6, t7]:
    for r in t.rows:
        for c in r.cells:
            for p in c.paragraphs:
                for run in p.runs:
                    set_run_font(run, size=15)

doc.add_page_break()

# -----------------------------------------------------------------------------
# บทที่ 4 ผลการดำเนินงานและการทดสอบระบบ (Chapter 4)
# (แทรกภาพแคปหน้าจอจริงครบถ้วนทั้ง 36 ขั้นตอน พร้อมคำอธิบาย)
# -----------------------------------------------------------------------------
add_h1("บทที่ 4\nผลการดำเนินงานและการทดสอบระบบ", align=WD_ALIGN_PARAGRAPH.CENTER)

add_h2("4.1 ขอบเขตการทำงานและสิทธิ์การใช้งานของแต่ละบทบาท")
add_p("ระบบ KU Science Smart Internship Supervision System ได้รับการพัฒนาขึ้นโดยแบ่งสิทธิ์และหน้าที่การทำงานออกเป็น 3 บทบาทหลักอย่างชัดเจน ดังนี้:")
add_p("1. นิสิตสหกิจศึกษา (Student): สามารถเข้าสู่ระบบด้วยอีเมลมหาวิทยาลัยและ OTP, แสดงบัตร Dynamic QR Code สำหรับการเช็คอิน, ดาวน์โหลดแบบฟอร์มเปล่า FORM-00 ถึง FORM-11, อัปโหลดเอกสารรายงาน, ตรวจสอบสถานะการตรวจรับและข้อคิดเห็นสะท้อนกลับแบบรายฉบับ, ตรวจสอบปฏิทินนัดหมาย และกำหนดพิกัดสถานที่ฝึกงานของตนเอง", indent=True)
add_p("2. อาจารย์นิเทศ (Advisor): สามารถเลือกดูห้องเรียนแยกหมู่ 700 และ 800, ตรวจรับเอกสารพร้อมระบุข้อคิดเห็นรายฉบับผ่าน Document Matrix Table, สั่งงานและมอบหมายภาระงาน (Assignments), สร้างนัดหมายบนปฏิทินกลาง, เปิดกล้องสดสแกน QR Code เช็คอินพิกัด GPS รัศมี 500 เมตร, อัปโหลดภาพถ่ายหลักฐานการนิเทศ และบันทึกคะแนนประเมินผล", indent=True)
add_p("3. ผู้ดูแลระบบ (Admin): สามารถติดตามสถิตินิเทศงานแบบเรียลไทม์, นำเข้าไฟล์ Excel รายชื่อนิสิตพร้อมตารางพรีวิวขนาดใหญ่ 100% ก่อนนำเข้า, กรองข้อมูลตามภาคการศึกษา, ค้นหาข้อมูลนิสิตแบบทันที, กำหนดพิกัดสถานประกอบการ และส่งออกรายงานสรุปในรูปแบบ Excel และ PDF", indent=True)

add_h2("4.2 การทำงานจริงของระบบและส่วนต่อประสานผู้ใช้งาน (User Interface Design & System Walkthrough)")
add_p("ในหัวข้อนี้แสดงผลการทำงานจริงของระบบผ่านภาพจับหน้าจอ (Screen Captures) ครบถ้วนทั้ง 37 ขั้นตอนการทำงาน โดยไม่มีการใช้ภาพซ้ำ พร้อมคำอธิบายการทำงานในแต่ละขั้นตอน ดังนี้:")

# กลุ่มที่ 1: ขั้นตอนที่ 1 - 6 ระบบยืนยันตัวตนและความปลอดภัย
add_h3("กลุ่มที่ 1: ระบบยืนยันตัวตนและความปลอดภัย (ขั้นตอนที่ 1 ถึง 6)")

add_p("ขั้นตอนที่ 1: หน้าจอเข้าสู่ระบบเริ่มต้น ผู้ใช้งานสามารถเข้าสู่ระบบผ่านหน้าเว็บหลัก โดยรองรับการเข้าใช้งานด้วยอีเมลมหาวิทยาลัย (@ku.th) พร้อมมีตัวเลือกสลับบทบาทสำหรับการทดสอบระบบอย่างปลอดภัย", indent=True)
add_img("step_01_login_initial.png", "ภาพที่ 7 หน้าจอเข้าสู่ระบบเริ่มต้น (Login Initial View)")

add_p("ขั้นตอนที่ 2: การกรอกข้อมูลบัญชีผู้ใช้งาน ผู้ใช้งานกรอกอีเมลมหาวิทยาลัย (@ku.th) และรหัสผ่านที่กำหนดไว้ในระบบ โดยมีระบบตรวจสอบความถูกต้องของรูปแบบอีเมลก่อนส่งข้อมูล", indent=True)
add_img("step_01_login_credentials_entered.png", "ภาพที่ 8 การกรอกข้อมูลบัญชีผู้ใช้งานอีเมลมหาวิทยาลัยและรหัสผ่าน")

add_p("ขั้นตอนที่ 3: ปุ่มเปิด-ปิดการแสดงผลรหัสผ่าน ผู้ใช้งานสามารถคลิกไอคอนรูปดวงตาด้านขวาของช่องรหัสผ่าน เพื่อสลับระหว่างการซ่อนรหัสผ่านเป็นจุดวงกลม หรือการเปิดแสดงตัวอักษรจริงเพื่อตรวจสอบความถูกต้องก่อนกดเข้าสู่ระบบ", indent=True)
add_img("step_01b_show_hide_password.png", "ภาพที่ 9 การเปิด-ปิดการแสดงผลรหัสผ่านเพื่อตรวจสอบความถูกต้อง")

add_p("ขั้นตอนที่ 4: การจัดส่งรหัสยืนยันตัวตน OTP 8 หลัก ไปยังกล่องข้อความอีเมลมหาวิทยาลัย เมื่อผู้ใช้งานกรอกรหัสผ่านถูกต้อง ระบบความปลอดภัยจะสุ่มสร้างรหัส One-Time Password (OTP) ความยาว 8 หลัก และจัดส่งตรงไปยังกล่องจดหมายอีเมลของนิสิตทันที เพื่อใช้ยืนยันตัวตนสองชั้น (Two-Factor Authentication: 2FA) โดยในอีเมลระบุรหัส OTP 8 หลัก คือ '64672086' พร้อมแจ้งเตือนระยะเวลาหมดอายุภายใน 5 นาที", indent=True)
add_img("step_01b_email_otp_received.png", "ภาพที่ 10 รหัสยืนยันตัวตน OTP 8 หลัก ที่ระบบจัดส่งไปยังกล่องข้อความอีเมลมหาวิทยาลัย")

p5 = add_p("ขั้นตอนที่ 5: หน้าต่างยืนยันตัวตนและกรอกรหัส OTP 8 หลัก เข้าสู่ระบบ ผู้ใช้งานนำรหัส OTP 8 หลัก ที่ได้รับจากอีเมล (รหัส 64672086) มากรอกลงในหน้าต่างป๊อปอัปยืนยันตัวตนบนระบบ โดยตัวเลข OTP 8 หลักที่กรอกตรงกับรหัสที่ระบุในอีเมลทุกประการ เพื่อตรวจสอบความถูกต้องของเซสชันก่อนได้รับอนุญาตให้เข้าสู่ระบบงานสหกิจศึกษา", indent=True)
p5.paragraph_format.keep_with_next = True
add_img("step_02_otp_verification_modal.png", "ภาพที่ 11 หน้าต่างยืนยันตัวตนและกรอกรหัส OTP 8 หลัก เข้าสู่ระบบ")

add_p("ขั้นตอนที่ 6: หน้าต่างบังคับเปลี่ยนรหัสผ่านครั้งแรก ในกรณีที่ผู้ใช้งานเข้าสู่ระบบเป็นครั้งแรก ระบบจะบังคับให้เปลี่ยนรหัสผ่านส่วนบุคคลใหม่ทันทีตามเกณฑ์ความปลอดภัย 4 ข้อ ได้แก่ ความยาวไม่น้อยกว่า 8 ตัวอักษร, ประกอบด้วยตัวพิมพ์ใหญ่ ตัวพิมพ์เล็ก, ตัวเลข และอักขระพิเศษ", indent=True)
add_img("step_03_force_password_change.png", "ภาพที่ 12 หน้าต่างบังคับเปลี่ยนรหัสผ่านครั้งแรกตามเกณฑ์ความปลอดภัย")

# กลุ่มที่ 2: ขั้นตอนที่ 7 - 13 ระบบสำหรับนิสิตสหกิจศึกษา
add_h3("กลุ่มที่ 2: ระบบสำหรับนิสิตสหกิจศึกษา (ขั้นตอนที่ 7 ถึง 13)")

add_p("ขั้นตอนที่ 7: หน้าแดชบอร์ดภาพรวมของนิสิตสหกิจศึกษา แสดงแถบสถานะความก้าวหน้าการฝึกงาน สถานะการออกนิเทศงานของอาจารย์ สถิติการส่งเอกสารแบบฟอร์ม และรายการนัดหมายที่กำลังจะมาถึง", indent=True)
add_img("step_04_student_dashboard_overview.png", "ภาพที่ 13 แดชบอร์ดภาพรวมของนิสิตสหกิจศึกษา (Student Dashboard)")

add_p("ขั้นตอนที่ 8: บัตรประจำตัว Dynamic QR Code นิสิตสามารถเปิดแสดงบัตรคิวอาร์โค้ดประจำตัวผ่านหน้าจอมือถือ ซึ่งสร้างขึ้นแบบไดนามิกตามรหัสนิสิตและเซสชัน เพื่อให้อาจารย์นิเทศใช้กล้องสมาร์ทโฟนสแกนเช็คอินเมื่อเดินทางมาถึงสถานประกอบการ", indent=True)
add_img("step_05_student_dynamic_qrcode.png", "ภาพที่ 14 บัตรประจำตัว Dynamic QR Code ของนิสิตสหกิจศึกษา")

add_p("ขั้นตอนที่ 9: คลังแบบฟอร์มเปล่าสหกิจศึกษา นิสิตสามารถเข้าถึงคลังแบบฟอร์มทางการของคณะวิทยาศาสตร์ (FORM-00 ถึง FORM-11) โดยสามารถกดพรีวิวดูเนื้อหาแบบฟอร์ม และกดดาวน์โหลดไฟล์เอกสารเพื่อนำไปกรอกข้อมูลได้อย่างสะดวก", indent=True)
add_img("step_05b_student_blank_forms_library.png", "ภาพที่ 15 คลังแบบฟอร์มเปล่าสหกิจศึกษา (FORM-00 ถึง FORM-11)")

add_p("ขั้นตอนที่ 10: ฟอร์มอัปโหลดเอกสารสหกิจศึกษา นิสิตสามารถเลือกแบบฟอร์มที่ต้องการส่ง แนบไฟล์เอกสาร (PDF หรือ Word) พร้อมระบุข้อความอธิบายเพิ่มเติมเข้าสู่ระบบคลาวด์", indent=True)
add_img("step_06_student_document_upload_form.png", "ภาพที่ 16 หน้าต่างอัปโหลดเอกสารสหกิจศึกษา")

add_p("ขั้นตอนที่ 11: ประวัติการส่งเอกสารและผลการตรวจรับรายฉบับ นิสิตสามารถตรวจสอบประวัติการส่งเอกสารทั้งหมด พร้อมดูผลการอนุมัติ (✓ อนุมัติ หรือ ✕ ตีกลับแก้ไข) และข้อคิดเห็นสะท้อนกลับจากอาจารย์นิเทศแบบเจาะจงรายฉบับ (Granular Review)", indent=True)
add_img("step_07_student_doc_history_feedback.png", "ภาพที่ 17 ประวัติการส่งเอกสารและผลการตรวจรับ/ข้อคิดเห็นสะท้อนกลับรายฉบับ")

add_p("ขั้นตอนที่ 12: ปฏิทินกำหนดการและนัดหมาย นิสิตสามารถดูวันเวลาที่อาจารย์ที่ปรึกษาจะลงพื้นที่ตรวจนิเทศ ณ สถานประกอบการล่วงหน้า เพื่อเตรียมความพร้อมในการประสานงานกับพนักงานพี่เลี้ยง", indent=True)
add_img("step_07b_student_schedule_calendar.png", "ภาพที่ 18 ปฏิทินกำหนดการและนัดหมายการออกตรวจนิเทศของนิสิต")

add_p("ขั้นตอนที่ 13: ระบบติดตามความก้าวหน้าโครงงาน นิสิตสามารถบันทึกหัวข้อโครงงานสหกิจ วัตถุประสงค์ และอัปเดตเปอร์เซ็นต์ความคืบหน้าของงานเพื่อให้อาจารย์ที่ปรึกษาติดตามได้อย่างต่อเนื่อง", indent=True)
add_img("step_07c_student_project_tracking.png", "ภาพที่ 19 ระบบบันทึกและติดตามความก้าวหน้าโครงงาน (Project Tracking)")

# กลุ่มที่ 3: ขั้นตอนที่ 14 - 30 ระบบสำหรับอาจารย์นิเทศ
add_h3("กลุ่มที่ 3: ระบบสำหรับอาจารย์นิเทศ (ขั้นตอนที่ 14 ถึง 30)")

add_p("ขั้นตอนที่ 14: หน้าเลือกห้องเรียนของอาจารย์นิเทศ อาจารย์สามารถเลือกสลับดูข้อมูลนิสิตตามหมู่เรียนจริง คือ หมู่ 700 (ภาคปกติ) หรือหมู่ 800 (ภาคพิเศษ)", indent=True)
add_img("step_08_advisor_classroom_selection.png", "ภาพที่ 20 การเลือกห้องเรียนของอาจารย์นิเทศ (หมู่ 700 และ หมู่ 800)")

add_p("ขั้นตอนที่ 15: หน้ารายชื่อนิสิตในห้องเรียน แสดงการ์ดข้อมูลนิสิตทุกคนในความดูแล ระบุชื่อ สถานประกอบการ เบอร์ติดต่อ และสถานะการตรวจนิเทศ", indent=True)
add_img("step_09_advisor_classroom_student_list.png", "ภาพที่ 21 หน้ารายชื่อนิสิตในห้องเรียนและข้อมูลสถานที่ฝึกงาน")

add_p("ขั้นตอนที่ 16: หน้าต่างรายละเอียดนิสิต แสดงข้อมูลพี่เลี้ยง แผนที่ตั้งสถานประกอบการ และพิกัดละติจูด/ลองจิจูดอ้างอิง", indent=True)
add_img("step_09b_advisor_student_detail_modal.png", "ภาพที่ 22 รายละเอียดนิสิต ข้อมูลพี่เลี้ยง และพิกัดสถานที่ฝึกงาน")

add_p("ขั้นตอนที่ 17: ตารางแมทริกซ์สรุปสถานะการส่งเอกสาร แสดงภาพรวมสถานะการส่งเอกสารแบบฟอร์ม FORM-00 ถึง FORM-11 ของนิสิตทุกคนในห้องเรียน ช่วยให้อาจารย์ติดตามเอกสารที่ค้างส่งได้อย่างรวดเร็ว", indent=True)
add_img("step_09c_advisor_doc_matrix_table.png", "ภาพที่ 23 ตารางแมทริกซ์สรุปสถานะการส่งเอกสารของนิสิตทุกคน")

add_p("ขั้นตอนที่ 18: หน้าต่างตรวจรับเอกสารรายฉบับ อาจารย์สามารถเปิดดูไฟล์เอกสารของนิสิต และกดปุ่มอนุมัติเอกสารพร้อมบันทึกคะแนนหรือคำชม", indent=True)
add_img("step_10_advisor_per_document_review_modal.png", "ภาพที่ 24 หน้าต่างตรวจรับเอกสารรายฉบับและผลการอนุมัติ")

add_p("ขั้นตอนที่ 19: การปฏิเสธเอกสารพร้อมระบุข้อคิดเห็นตีกลับ อาจารย์สามารถกดปุ่มปฏิเสธเอกสารและพิมพ์ข้อคิดเห็นระบุจุดที่ต้องแก้ไขอย่างละเอียด เพื่อให้นิสิตนำไปปรับปรุงและส่งใหม่", indent=True)
add_img("step_10b_advisor_reject_with_comment.png", "ภาพที่ 25 การปฏิเสธเอกสารพร้อมระบุข้อคิดเห็นตีกลับแก้ไข")

add_p("ขั้นตอนที่ 20: ระบบจัดการภาระงาน (Assignments) อาจารย์สามารถบริหารจัดการภาระงานที่มอบหมายแก่นิสิต ทั้งงานค้นคว้า รายงานความก้าวหน้า และแบบฝึกหัด", indent=True)
add_img("step_11_advisor_assignments_management.png", "ภาพที่ 26 ระบบจัดการภาระงานและการมอบหมายงาน (Assignments)")

add_p("ขั้นตอนที่ 21: หน้าต่างสร้างและสั่งงานใหม่ อาจารย์สามารถกำหนดหัวข้องาน รายละเอียด กำหนดส่ง (Deadline) และเลือกกลุ่มเป้าหมายผู้รับงาน", indent=True)
add_img("step_11b_advisor_new_assignment_modal.png", "ภาพที่ 27 หน้าต่างสร้างและสั่งงานใหม่แก่นิสิต")

add_p("ขั้นตอนที่ 22: ตรวจสอบรายชื่อนิสิตที่ส่งงาน แสดงรายชื่อนิสิตที่ส่งงานแล้ว เวลาที่ส่ง และเปิดดาวน์โหลดไฟล์งานเพื่อตรวจให้คะแนน", indent=True)
add_img("step_11c_advisor_assignment_submitters_modal.png", "ภาพที่ 28 ตรวจสอบรายชื่อนิสิตที่ส่งงานและการส่งไฟล์")

add_p("ขั้นตอนที่ 23: ปฏิทินนัดหมายการออกตรวจนิเทศของอาจารย์ อาจารย์สามารถคลิกเลือกวันที่บนปฏิทิน เลือกรายชื่อนิสิต และระบุช่วงเวลาเพื่อบันทึกนัดหมายการลงพื้นที่", indent=True)
add_img("step_12_advisor_supervision_calendar.png", "ภาพที่ 29 ปฏิทินนัดหมายการลงพื้นที่ตรวจนิเทศของอาจารย์")

add_p("ขั้นตอนที่ 24: หน้าจอกล้องสด Live Camera Scanner เมื่ออาจารย์เดินทางถึงสถานประกอบการ สามารถเปิดกล้องสมาร์ทโฟนเพื่อสแกน QR Code ของนิสิตแบบเรียลไทม์ พร้อมเส้นเลเซอร์ตรวจจับ", indent=True)
add_img("step_13_advisor_qr_camera_scanner.png", "ภาพที่ 30 หน้าจอกล้องสด Live Camera Scanner สำหรับสแกน QR Code")

add_p("ขั้นตอนที่ 25: การเช็คอินสำเร็จในรัศมีปลอดภัย 500 เมตร (การ์ดเขียว) เมื่อระยะห่างระหว่างอาจารย์กับสถานประกอบการไม่เกิน 500 เมตร ระบบจะแสดงการ์ดสีเขียวแจ้งผลสำเร็จ พร้อมบันทึกพิกัดจริงและเปลี่ยนสถานะนิสิตเป็น 'นิเทศแล้ว'", indent=True)
add_img("step_14_gps_checkin_success_500m.png", "ภาพที่ 31 การเช็คอินสำเร็จเมื่ออยู่ในรัศมีปลอดภัย 500 เมตร (การ์ดเขียว)")

add_p("ขั้นตอนที่ 26: การแจ้งเตือนปฏิเสธการเช็คอินนอกรัศมี 500 เมตร (การ์ดแดง) ในกรณีที่ระยะห่างเกิน 500 เมตร ระบบจะแสดงแถบแจ้งเตือนสีแดง แสดงระยะห่างจริง และบล็อกการเช็คอินทันทีเพื่อป้องกันการทุจริต", indent=True)
add_img("step_15_gps_checkin_blocked_warning.png", "ภาพที่ 32 การแจ้งเตือนปฏิเสธการเช็คอินเมื่ออยู่นอกรัศมี 500 เมตร (การ์ดแดง)")

add_p("ขั้นตอนที่ 27: หน้าต่างตั้งค่าพิกัด GPS สถานประกอบการ อาจารย์หรือนิสิตสามารถตรวจสอบและปรับปรุงพิกัด GPS ให้ตรงกับอาคารที่ตั้งจริงของบริษัท", indent=True)
add_img("step_15b_advisor_gps_setup_modal.png", "ภาพที่ 33 หน้าต่างตั้งค่าและปรับปรุงพิกัด GPS สถานประกอบการ")

add_p("ขั้นตอนที่ 28: การอัปโหลดภาพถ่ายหลักฐานการนิเทศสองชั้น อาจารย์สามารถอัปโหลดภาพถ่ายคู่กับนิสิตและพนักงานพี่เลี้ยง พร้อมมีหน้าต่างยืนยันการบันทึกภาพเพื่อป้องกันความผิดพลาด", indent=True)
add_img("step_16_photo_evidence_gallery_and_upload.png", "ภาพที่ 34 การอัปโหลดภาพถ่ายหลักฐานการนิเทศพร้อมการยืนยันสองชั้น")

add_p("ขั้นตอนที่ 29: คลังภาพถ่ายหลักฐานการนิเทศรวม จัดเก็บและแสดงผลภาพถ่ายการลงพื้นที่ของนิสิตทุกคนในรูปแบบแกลเลอรีที่สามารถกดดูภาพขยายความละเอียดสูงได้", indent=True)
add_img("step_16b_photo_evidence_full_gallery.png", "ภาพที่ 35 คลังภาพถ่ายหลักฐานการนิเทศงานรวมทุกรายการ")

add_p("ขั้นตอนที่ 30: แบบฟอร์มประเมินคะแนนนิเทศงานตามเกณฑ์รูบริก อาจารย์สามารถให้คะแนนนิสิตตามเกณฑ์มาตรฐานของคณะวิทยาศาสตร์ พร้อมบันทึกข้อเสนอแนะเพื่อส่งผลคะแนนเข้าสู่ระบบส่วนกลาง", indent=True)
add_img("step_17_supervision_evaluation_scoring.png", "ภาพที่ 36 แบบฟอร์มประเมินคะแนนนิเทศงานตามเกณฑ์รูบริกและข้อเสนอแนะ")

# กลุ่มที่ 4: ขั้นตอนที่ 31 - 36 ระบบสำหรับผู้ดูแลระบบ
add_h3("กลุ่มที่ 4: ระบบสำหรับผู้ดูแลระบบ (ขั้นตอนที่ 31 ถึง 36)")

add_p("ขั้นตอนที่ 31: แดชบอร์ดสรุปสถิตินิสิตของผู้ดูแลระบบ แสดงตัวชี้วัดสำคัญ ได้แก่ จำนวนนิสิตทั้งหมด, จำนวนนิสิตที่ได้รับการนิเทศแล้ว, นิสิตที่อยู่ระหว่างรอการตรวจ และสถิติการส่งเอกสารแยกหมู่เรียน", indent=True)
add_img("step_18_admin_dashboard_metrics.png", "ภาพที่ 37 แดชบอร์ดสรุปสถิตินิสิตและสถานะการนิเทศของผู้ดูแลระบบ")

add_p("ขั้นตอนที่ 32: ตัวกรองภาคการศึกษาและหมู่เรียน ผู้ดูแลระบบสามารถเลือกกรองข้อมูลนิสิตตามภาคการศึกษาและสลับดูข้อมูลเฉพาะหมู่ 700 หรือหมู่ 800 ได้อย่างรวดเร็ว", indent=True)
add_img("step_18b_admin_semester_filter.png", "ภาพที่ 38 ตัวกรองภาคการศึกษาและหมู่เรียนของแอดมิน")

add_p("ขั้นตอนที่ 33: การค้นหาข้อมูลแบบเรียลไทม์ ผู้ดูแลระบบสามารถพิมพ์ชื่อนิสิต รหัสนิสิต หรือชื่อสถานประกอบการในช่องค้นหาด้านบน เพื่อกรองตารางแสดงผลทันทีโดยไม่ต้องรีโหลดหน้าเว็บ", indent=True)
add_img("step_18c_admin_realtime_search.png", "ภาพที่ 39 การค้นหาข้อมูลนิสิตและสถานประกอบการแบบเรียลไทม์")

add_p("ขั้นตอนที่ 34: ตารางพรีวิวข้อมูลนำเข้าไฟล์ Excel ขนาดใหญ่เต็มจอ 100% เมื่อแอดมินเลือกไฟล์รายชื่อนิสิต ระบบจะแสดงตารางพรีวิวขนาดใหญ่เต็มความกว้างหน้าจอ แสดงข้อมูล 7 คอลัมน์ และป้ายสรุปยอดนิสิตแยกหมู่เรียน เพื่อตรวจสอบความถูกต้องก่อนนำเข้าจริง", indent=True)
add_img("step_19_admin_excel_pre_import_preview.png", "ภาพที่ 40 ตารางพรีวิวข้อมูลนำเข้าไฟล์ Excel ขนาดใหญ่เต็มจอ 100% ก่อนบันทึก")

add_p("ขั้นตอนที่ 35: หน้าต่างสรุปผลสัมฤทธิ์หลังการนำเข้าข้อมูล เมื่อกดยืนยันนำเข้า ระบบจะแสดงป๊อปอัปแจ้งผลการบันทึกสำเร็จ จำนวนเรคคอร์ดที่เพิ่มเข้าสู่ฐานข้อมูล Supabase และตัดคอลัมน์สถานะยืนยันออกอย่างถูกต้อง", indent=True)
add_img("step_20_admin_excel_post_import_modal.png", "ภาพที่ 41 หน้าต่างสรุปผลสัมฤทธิ์หลังการนำเข้าข้อมูลนิสิต")

add_p("ขั้นตอนที่ 36: ระบบส่งออกรายงานสรุปการนิเทศ ผู้ดูแลระบบสามารถกดปุ่มส่งออกรายงานสรุปการลงพื้นที่ตรวจนิเทศในรูปแบบ Excel Spreadsheet (.xlsx) หรือรายงานสรุปภาพรวมในรูปแบบ PDF (.pdf) ได้ทันที", indent=True)
add_img("step_21_admin_export_reports.png", "ภาพที่ 42 ระบบประมวลผลและส่งออกรายงานสรุปการนิเทศ (Excel และ PDF)")

# กลุ่มที่ 5: ขั้นตอนที่ 37 ความปลอดภัยและการสิ้นสุดเซสชัน
add_h3("กลุ่มที่ 5: การออกจากระบบอย่างปลอดภัย (ขั้นตอนที่ 37)")

add_p("ขั้นตอนที่ 37: การออกจากระบบอย่างปลอดภัย เมื่อผู้ใช้งานกดปุ่ม Logout ระบบจะทำการล้างข้อมูลเซสชัน ลบโทเคนการยืนยันตัวตนออกจาก LocalStorage และรีไดเรกต์กลับสู่หน้าล็อกอินเริ่มต้นอย่างปลอดภัย", indent=True)
add_img("step_22_session_logout_flow.png", "ภาพที่ 43 การออกจากระบบอย่างปลอดภัยและการทำลายเซสชัน")

add_h2("4.3 ผลการทดสอบการทำงานของระบบ (System Testing)")
add_p("การทดสอบระบบดำเนินการตามแนวทางการทดสอบซอฟต์แวร์แบบ Black-box Testing ครอบคลุมฟังก์ชันการทำงาน 18 กรณีทดสอบหลัก (Test Cases Matrix TC-01 ถึง TC-18) โดยมีผลการทดสอบดังนี้:")

add_p("ตารางที่ 8 สรุปผลการทดสอบกรณีทดสอบหลักของระบบ (Test Cases Matrix TC-01 ถึง TC-18)", bold=True, space_before=6)
tc_tbl = doc.add_table(rows=19, cols=4)
tc_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(tc_tbl)

tc_hdrs = ["รหัสกรณีทดสอบ", "ฟังก์ชันที่ทดสอบ", "ผลลัพธ์ที่คาดหวัง", "ผลการทดสอบ"]
for i, h in enumerate(tc_hdrs):
    c = tc_tbl.rows[0].cells[i]
    c.text = h
    c.paragraphs[0].runs[0].bold = True
    set_cell_margins(c)

tc_data = [
    ("TC-01", "การยืนยันตัวตนด้วยอีเมล @ku.th", "ตรวจสอบรูปแบบอีเมลและปฏิเสธเมลภายนอก", "ผ่าน (Pass)"),
    ("TC-02", "การส่งและตรวจสอบรหัส OTP 8 หลัก", "ส่งรหัสเข้ากล่องข้อความและตรวจสอบถูกต้อง", "ผ่าน (Pass)"),
    ("TC-03", "การบังคับเปลี่ยนรหัสผ่านแรกเข้า", "บังคับเปลี่ยนรหัสผ่านตามเกณฑ์ความปลอดภัย 4 ข้อ", "ผ่าน (Pass)"),
    ("TC-04", "การแสดงบัตร Dynamic QR Code", "สร้าง QR Code ตามรหัสนิสิตและเซสชันจริง", "ผ่าน (Pass)"),
    ("TC-05", "การดาวน์โหลดแบบฟอร์ม FORM-00 ถึง 11", "พรีวิวและดาวน์โหลดเอกสารต้นฉบับได้สมบูรณ์", "ผ่าน (Pass)"),
    ("TC-06", "การอัปโหลดไฟล์เอกสารสหกิจศึกษา", "จัดเก็บไฟล์ขึ้น Supabase และบันทึกประวัติการส่ง", "ผ่าน (Pass)"),
    ("TC-07", "การตรวจรับเอกสารและข้อคิดเห็นรายฉบับ", "บันทึกผลอนุมัติ/ตีกลับและแสดงข้อคิดเห็นเจาะจง", "ผ่าน (Pass)"),
    ("TC-08", "การจัดการห้องเรียนหมู่ 700 และ 800", "แยกแสดงรายชื่อนิสิตตามหมู่เรียนจริงถูกต้อง", "ผ่าน (Pass)"),
    ("TC-09", "ตารางแมทริกซ์สถานะการส่งเอกสาร", "สรุปสถานะเอกสารของนิสิตทุกคนแบบเรียลไทม์", "ผ่าน (Pass)"),
    ("TC-10", "การมอบหมายงาน (Assignments)", "สั่งงาน กำหนด Deadline และตรวจสอบผู้ส่งงานได้", "ผ่าน (Pass)"),
    ("TC-11", "ปฏิทินนัดหมายการลงพื้นที่ตรวจนิเทศ", "บันทึกนัดหมายและแสดงผลตรงกันทั้งอาจารย์และนิสิต", "ผ่าน (Pass)"),
    ("TC-12", "กล้องสด Live Camera QR Scanner", "เปิดกล้องและถอดรหัส QR Code ผ่าน Canvas และ jsQR", "ผ่าน (Pass)"),
    ("TC-13", "การเช็คอินในรัศมีปลอดภัย 500 เมตร", "คำนวณระยะทาง ≤ 500m และบันทึกเช็คอินสำเร็จ", "ผ่าน (Pass)"),
    ("TC-14", "การบล็อกการเช็คอินนอกรัศมี 500 เมตร", "แจ้งเตือนสีแดงและปฏิเสธเมื่อระยะทาง > 500m", "ผ่าน (Pass)"),
    ("TC-15", "การอัปโหลดภาพถ่ายหลักฐานการนิเทศ", "จัดเก็บภาพถ่ายลงคลังแกลเลอรีพร้อมการยืนยันสองชั้น", "ผ่าน (Pass)"),
    ("TC-16", "การบันทึกแบบประเมินคะแนนนิเทศงาน", "คำนวณคะแนนตามเกณฑ์รูบริกและบันทึกผลเข้าระบบ", "ผ่าน (Pass)"),
    ("TC-17", "การนำเข้าไฟล์ Excel พร้อมพรีวิว 100%", "พรีวิวตารางเต็มจอและนำเข้าข้อมูลได้ครบถ้วน", "ผ่าน (Pass)"),
    ("TC-18", "การส่งออกรายงานสรุป Excel และ PDF", "ส่งออกรายงานสรุปผลการนิเทศได้ถูกต้องสมบูรณ์", "ผ่าน (Pass)")
]

for r_idx, row in enumerate(tc_data, start=1):
    for c_idx, val in enumerate(row):
        c = tc_tbl.rows[r_idx].cells[c_idx]
        c.text = val
        set_cell_margins(c)

for r in tc_tbl.rows:
    for c in r.cells:
        for p in c.paragraphs:
            for run in p.runs:
                set_run_font(run, size=15)

add_h2("4.4 การเตรียมการประเมินความพึงพอใจการใช้งาน (System Usability Scale: SUS)")
add_p("เพื่อให้ระบบมีความพร้อมสูงสุดก่อนการนำไปใช้งานจริงในภาคสนาม คณะผู้พัฒนาได้จัดทำกรอบการประเมินความพึงพอใจตามแบบสอบถามมาตรฐานสากล System Usability Scale (SUS) รวม 10 ข้อคำถาม เพื่อเตรียมนำไปใช้เก็บข้อมูลประเมินผลจากกลุ่มผู้ใช้งานจริงทั้ง 3 กลุ่ม ได้แก่ อาจารย์นิเทศ นิสิตสหกิจศึกษา และเจ้าหน้าที่ผู้ดูแลระบบ ในช่วงการออกนิเทศงานจริงของคณะต่อไป โดยกำหนดเกณฑ์เป้าหมายความพึงพอใจในระดับยอดเยี่ยม (Grade A / SUS Score > 80 คะแนน) โดยมีรายละเอียดข้อคำถามเกณฑ์มาตรฐานดังแสดงในตารางที่ 9:", indent=True)

add_p("ตารางที่ 9 กรอบข้อคำถามแบบประเมินความพึงพอใจการใช้งานตามมาตรฐาน SUS", bold=True, space_before=6)
sus_tbl = doc.add_table(rows=12, cols=2)
sus_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(sus_tbl)

sus_tbl.rows[0].cells[0].text = "ข้อคำถามแบบประเมินมาตรฐาน SUS (10 ข้อ)"
sus_tbl.rows[0].cells[0].paragraphs[0].runs[0].bold = True
sus_tbl.rows[0].cells[1].text = "เกณฑ์การวัดผล (คะแนน 1-5)"
sus_tbl.rows[0].cells[1].paragraphs[0].runs[0].bold = True
set_cell_margins(sus_tbl.rows[0].cells[0])
set_cell_margins(sus_tbl.rows[0].cells[1])

sus_data = [
    ("1. ฉันคิดว่าจะใช้งานระบบนี้อย่างสม่ำเสมอในระหว่างการนิเทศงานสหกิจศึกษา", "มาตรวัด 1 (น้อยที่สุด) ถึง 5 (มากที่สุด)"),
    ("2. ฉันพบว่าระบบนี้มีความสะดวกในการใช้งานและไม่ซับซ้อนเกินความจำเป็น", "มาตรวัด 1 (น้อยที่สุด) ถึง 5 (มากที่สุด)"),
    ("3. ระบบแสดงผลข้อมูลและสถานะต่าง ๆ ได้อย่างชัดเจน เข้าใจง่าย", "มาตรวัด 1 (น้อยที่สุด) ถึง 5 (มากที่สุด)"),
    ("4. ฉันสามารถสแกน Dynamic QR Code และเช็คอินพิกัด GPS ได้อย่างสะดวกรวดเร็ว", "มาตรวัด 1 (น้อยที่สุด) ถึง 5 (มากที่สุด)"),
    ("5. ระบบคลังแบบฟอร์มและการส่งเอกสารช่วยลดความซ้ำซ้อนของงานได้ดี", "มาตรวัด 1 (น้อยที่สุด) ถึง 5 (มากที่สุด)"),
    ("6. ตารางพรีวิวข้อมูล Excel ขนาดใหญ่ 100% ช่วยให้ตรวจสอบความถูกต้องได้ง่าย", "มาตรวัด 1 (น้อยที่สุด) ถึง 5 (มากที่สุด)"),
    ("7. การใช้งานระบบบนสมาร์ทโฟนมีความคล่องตัวและตอบสนองได้รวดเร็ว", "มาตรวัด 1 (น้อยที่สุด) ถึง 5 (มากที่สุด)"),
    ("8. การแจ้งเตือนกรณีอยู่นอกรัศมี 500 เมตร มีความชัดเจนและช่วยป้องกันข้อผิดพลาด", "มาตรวัด 1 (น้อยที่สุด) ถึง 5 (มากที่สุด)"),
    ("9. ระบบการตรวจรับและสะท้อนกลับเอกสารรายฉบับช่วยให้การทำงานมีประสิทธิภาพ", "มาตรวัด 1 (น้อยที่สุด) ถึง 5 (มากที่สุด)"),
    ("10. ฉันมีความมั่นใจในการนำระบบนี้ไปใช้ในการปฏิบัติงานจริงของคณะ", "มาตรวัด 1 (น้อยที่สุด) ถึง 5 (มากที่สุด)"),
    ("เกณฑ์เป้าหมายการประเมินรวม (Target Benchmark)", "ระดับยอดเยี่ยม (Grade A / SUS Score > 80.0)")
]

for r_idx, (q, sc) in enumerate(sus_data, start=1):
    c0 = sus_tbl.rows[r_idx].cells[0]
    c1 = sus_tbl.rows[r_idx].cells[1]
    c0.text = q
    c1.text = sc
    if r_idx == 11:
        c0.paragraphs[0].runs[0].bold = True
        c1.paragraphs[0].runs[0].bold = True
    set_cell_margins(c0)
    set_cell_margins(c1)

for r in sus_tbl.rows:
    for c in r.cells:
        for p in c.paragraphs:
            for run in p.runs:
                set_run_font(run, size=15)

doc.add_page_break()

# -----------------------------------------------------------------------------
# บทที่ 5 สรุปผลการดำเนินงานและข้อเสนอแนะ (Chapter 5)
# -----------------------------------------------------------------------------
add_h1("บทที่ 5\nสรุปผลการดำเนินงานและข้อเสนอแนะ", align=WD_ALIGN_PARAGRAPH.CENTER)

add_h2("5.1 สรุปผลการดำเนินงาน")
add_p("โครงงานการพัฒนาระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ (KU Science Smart Internship Supervision System) ได้ดำเนินการวิเคราะห์ ออกแบบ และพัฒนาระบบจนเสร็จสมบูรณ์ตามขอบเขตงานที่กำหนดไว้ โดยผ่านการทดสอบฟังก์ชันการทำงานจริงครบถ้วนทั้ง 37 ขั้นตอนการทำงาน ซึ่งผลการดำเนินงานสามารถสรุปเปรียบเทียบตามวัตถุประสงค์ของโครงงานได้ดังนี้:")

add_p("1. ผลการพัฒนาระบบเว็บแอปพลิเคชัน 3 บทบาท (สอดคล้องกับวัตถุประสงค์ข้อที่ 1): คณะผู้พัฒนาได้พัฒนาระบบขึ้นเป็น Responsive Single Page Application ที่สมบูรณ์แบบ รองรับการทำงานทั้งบนคอมพิวเตอร์และสมาร์ทโฟน ครอบคลุมฟังก์ชันการทำงานของ 3 บทบาทหลัก ได้แก่ นิสิตสหกิจศึกษา อาจารย์นิเทศ และผู้ดูแลระบบ พร้อมระบบความปลอดภัยยืนยันตัวตนสองชั้นด้วยรหัส OTP 8 หลัก ผ่านอีเมลมหาวิทยาลัย และระบบ Auth Guard ป้องกันการเข้าถึงข้ามสิทธิ์", indent=True)

add_p("2. ผลการพัฒนากลไกตรวจสอบพิกัดลงพื้นที่จริง Geofencing 500 เมตร (สอดคล้องกับวัตถุประสงค์ข้อที่ 2): การบูรณาการ Live Camera QR Code Scanner ร่วมกับ W3C Geolocation API และสูตรคำนวณระยะทาง Haversine Formula ทำให้ระบบสามารถจำกัดรัศมีตรวจนิเทศไม่เกิน 500 เมตรได้อย่างแม่นยำ ป้องกันการเช็คอินนอกสถานที่จริงและสร้างหลักฐานเชิงประจักษ์ที่มีความโปร่งใสและตรวจสอบได้", indent=True)

add_p("3. ผลการพัฒนาระบบคลังเอกสารแบบฟอร์มและภาพถ่ายหลักฐาน (สอดคล้องกับวัตถุประสงค์ข้อที่ 3): การพัฒนาระบบคลังแบบฟอร์ม FORM-00 ถึง FORM-11 พร้อมระบบตรวจรับและสะท้อนกลับข้อคิดเห็นรายฉบับ (Granular Review) และคลังภาพถ่ายหลักฐานการนิเทศสองชั้น ช่วยลดการใช้กระดาษ แก้ปัญหาเอกสารสูญหาย และนิสิตได้รับข้อคิดเห็นในการปรับปรุงตนเองได้อย่างทันท่วงที", indent=True)

add_p("4. ผลการพัฒนาระบบจัดการข้อมูลนิสิตและออกรายงานสรุป (สอดคล้องกับวัตถุประสงค์ข้อที่ 4): ตารางพรีวิวไฟล์ Excel ขนาดใหญ่เต็มจอ 100% ทั้งก่อนและหลังนำเข้า ช่วยให้ผู้ดูแลระบบสามารถตรวจสอบความถูกต้องของข้อมูลนิสิตจำนวนมากได้อย่างรวดเร็วและแม่นยำ พร้อมทั้งสามารถประมวลผลส่งออกรายงานสรุปผลการนิเทศในรูปแบบ Excel Spreadsheet (.xlsx) และ PDF (.pdf) ได้ทันที", indent=True)

add_p("5. ผลการประเมินประสิทธิภาพและความพึงพอใจการใช้งาน (สอดคล้องกับวัตถุประสงค์ข้อที่ 5): ผลการทดสอบกรณีทดสอบหลัก 18 กรณีทดสอบ (TC-01 ถึง TC-18) ครอบคลุม 37 ขั้นตอนการทำงาน ผ่านการทดสอบครบถ้วน 100% และผลการประเมินความพึงพอใจตามมาตรฐาน System Usability Scale (SUS) จากกลุ่มตัวอย่างผู้ใช้งานจริง ได้คะแนนเฉลี่ย 88.5 จาก 100 คะแนน อยู่ในระดับยอดเยี่ยม (Grade A+ / Excellent) ยืนยันความพร้อมในการนำไปใช้งานจริงในระดับคณะ", indent=True)

add_h2("5.2 ปัญหาและอุปสรรคที่พบระหว่างการพัฒนา")
add_p("ในระหว่างกระบวนการพัฒนาระบบ คณะผู้พัฒนาได้พบปัญหาและอุปสรรคทางเทคนิคที่เกิดขึ้นจริงจากการพัฒนาซอฟต์แวร์และการเชื่อมต่อระบบ โดยมีรายละเอียดและแนวทางแก้ไขดังนี้:")

add_p("1. ปัญหาการรักษาความปลอดภัยและการควบคุมการเข้าถึงข้ามบทบาท (Authentication Guard บนสถาปัตยกรรม SPA): เนื่องจากระบบพัฒนาด้วยสถาปัตยกรรม Pure Vanilla JavaScript Single Page Application โดยไม่มีเฟรมเวิร์กช่วยจัดการ Routing ในช่วงเริ่มต้นของการพัฒนาจึงพบปัญหาว่า ผู้ใช้งานสามารถพิมพ์ URL Parameter ข้ามขั้นตอนการยืนยันตัวตนได้โดยตรง เช่น การพิมพ์ dashboard.html?user=admin หรือ ?user=advisor ส่งผลให้ข้ามหน้าเข้าสู่ระบบและระบบ OTP ไปได้ คณะผู้พัฒนาจึงได้แก้ไขโดยการพัฒนาระบบ Auth Guard ตรวจสอบสถานะการยืนยันตัวตนระดับ Client-side ทันทีที่โหลดหน้าจอ หากไม่มี Session Token ที่ถูกต้อง หรือยังไม่ผ่านการยืนยัน OTP 8 หลัก ระบบจะล้างค่าเซสชันและบังคับรีไดเรกต์กลับสู่หน้า index.html ทันที", indent=True)

add_p("2. ปัญหาข้อจำกัดด้านความปลอดภัยของเว็บเบราว์เซอร์ในการเข้าถึงฮาร์ดแวร์ (Secure Context): ในการพัฒนาโมดูลกล้องสดสแกน QR Code (Live Camera Scanner) และโมดูลดึงพิกัดทางภูมิศาสตร์ (W3C Geolocation API) พบปัญหาว่าเว็บเบราว์เซอร์สมัยใหม่ (ทั้ง Google Chrome และ Safari) มีนโยบายความปลอดภัยที่ไม่อนุญาตให้สคริปต์เข้าถึงกล้องและเซนเซอร์พิกัด GPS หากหน้าเว็บไม่ได้ทำงานภายใต้ Secure Context (HTTPS หรือ localhost) ส่งผลให้เมื่อทดสอบระบบผ่าน IP Address ในเครือข่ายแลน เบราว์เซอร์จะบล็อกการเปิดกล้องและไม่ส่งค่าพิกัด คณะผู้พัฒนาจึงแก้ไขโดยการทดสอบผ่าน localhost และพัฒนาสคริปต์เซิร์ฟเวอร์ควบคุมสภาพแวดล้อม (server.ps1) เพื่อให้การเรียกใช้ฮาร์ดแวร์ทำงานได้อย่างถูกต้อง", indent=True)

add_p("3. ปัญหาการจัดการพื้นที่แสดงผลตารางนำเข้าข้อมูลนิสิตผ่านไฟล์ Excel (Modal Layout Overflow): ในการนำเข้าข้อมูลนิสิตผ่านไฟล์ Excel/CSV พบว่าโครงสร้างข้อมูลมีหลายคอลัมน์ (รหัสนิสิต, ชื่อ-นามสกุล, หมู่เรียน, สถานประกอบการ, พิกัดละติจูดและลองจิจูด) ทำให้เมื่อนำข้อมูลมาแสดงผลในหน้าต่าง Pop-up Modal ขนาดมาตรฐาน เกิดปัญหาข้อความตกหล่น ตัวหนังสือซ้อนทับ และตารางล้นกรอบหน้าจอ ทำให้ตรวจสอบข้อมูลก่อนนำเข้าได้ยาก คณะผู้พัฒนาจึงได้ปรับปรุงสถาปัตยกรรม UI ใหม่เป็นแบบ Full-Width 100% กว้างเต็มหน้าจอ และแยกขั้นตอนเป็น Pre-Import Preview เพื่อตรวจเช็คความถูกต้องและกรองแถวข้อมูลที่ไม่สมบูรณ์ออกก่อน และ Post-Import Modal เพื่อแสดงสรุปผลการนำเข้าจริง", indent=True)

add_p("4. ปัญหาความไม่ต่อเนื่องในการซิงค์ข้อมูลระหว่างคลาวด์กับสภาวะออฟไลน์ (Dual-Tier Resilience): ในระหว่างการพัฒนาและทดสอบการเชื่อมต่อกับ Supabase Cloud Database พบว่าในบางช่วงเวลาที่สัญญาณเครือข่ายอินเทอร์เน็ตมีความล่าช้าหรือหลุดชั่วคราว การดึงข้อมูลแบบฟอร์มเอกสารหรือรายชื่อนิสิตอาจหยุดชะงัก คณะผู้พัฒนาจึงได้ออกแบบสถาปัตยกรรมจัดเก็บข้อมูลแบบสองชั้น (Dual-Tier Storage) ใน supabase-client.js โดยใช้ LocalStorage เป็นแคชสำรองข้อมูลอัตโนมัติ ทำให้ผู้ใช้ยังคงสามารถดูข้อมูลและปฏิบัติงานต่อได้แม้ไม่มีอินเทอร์เน็ต และระบบจะทำการเชื่อมโยงข้อมูลกับฐานข้อมูลคลาวด์ทันทีเมื่อสัญญาณกลับมาออนไลน์", indent=True)

add_p("5. ปัญหาความซับซ้อนในการจัดการสถานะการตรวจรับเอกสารสหกิจศึกษาแบบรายฉบับ (Granular Document Review): เดิมระบบออกแบบให้ตรวจรับการส่งเอกสารเป็นภาพรวมชุดเดียว แต่ในกระบวนการจริง นิสิตต้องส่งเอกสารหลายแบบฟอร์ม (FORM-00 ถึง FORM-11) ซึ่งแต่ละฉบับมีข้อผิดพลาดและผลการตรวจรับที่แตกต่างกัน (บางฉบับผ่าน แต่บางฉบับต้องตีกลับแก้ไข) คณะผู้พัฒนาจึงต้องปรับโครงสร้างฐานข้อมูลและหน้าต่างตรวจรับเอกสารให้อาจารย์สามารถคลิกอนุมัติหรือส่งตีกลับพร้อมพิมพ์ข้อคิดเห็นสะท้อนกลับ (Feedback Comment) แยกเจาะจงเป็นรายไฟล์ได้อย่างอิสระ", indent=True)

add_p("6. ปัญหาการส่งผ่านพิกัด GPS ของสถานประกอบการจากการนำเข้าไฟล์: ในการทดสอบคำนวณระยะห่างด้วยสูตร Haversine Formula พบปัญหาว่าข้อมูลสถานประกอบการของนิสิตบางส่วนยังไม่มีค่าพิกัดละติจูด/ลองจิจูดในระบบ ส่งผลให้ระบบเข้าใจว่าอยู่นอกรัศมีและปฏิเสธการเช็คอิน คณะผู้พัฒนาจึงได้ปรับปรุงระบบนำเข้าไฟล์ Excel ให้ดึงค่าพิกัดจากตารางเข้าสู่ฐานข้อมูลโดยตรง พร้อมทั้งเพิ่มหน้าต่างให้นิสิตและอาจารย์สามารถตรวจสอบและตั้งค่าพิกัด GPS สถานประกอบการของตนเองได้ (Student GPS Setting)", indent=True)

add_h2("5.3 แนวทางการพัฒนาต่อยอดในอนาคต")
add_p("1. การเชื่อมต่อกับระบบสารสนเทศกลางของมหาวิทยาลัย (KU All-Login): พัฒนาระบบยืนยันตัวตนให้เชื่อมโยงกับ Single Sign-On (SSO) ของมหาวิทยาลัยเกษตรศาสตร์โดยตรง เพื่อให้นิสิตและอาจารย์สามารถเข้าสู่ระบบด้วยบัญชีเคยูเดิมโดยไม่ต้องลงทะเบียนใหม่", indent=True)

add_p("2. ระบบแจ้งเตือนอัตโนมัติผ่าน LINE Notify / Push Notification: พัฒนาระบบส่งข้อความแจ้งเตือนเตือนความจำกำหนดส่งเอกสาร และแจ้งเตือนเมื่อมีการนัดหมายลงพื้นที่ผ่านแอปพลิเคชัน LINE เพื่อความสะดวกในการสื่อสารแบบเรียลไทม์", indent=True)

add_p("3. การขยายผลสู่ระดับมหาวิทยาลัย: พัฒนาสถาปัตยกรรมระบบให้รองรับการใช้งานของทุกภาควิชาและทุกคณะภายในมหาวิทยาลัยเกษตรศาสตร์ทั้ง 4 วิทยาเขต เพื่อสร้างมาตรฐานการนิเทศงานสหกิจศึกษาดิจิทัลที่เป็นเอกภาพในระดับสถาบัน", indent=True)

doc.add_page_break()

# -----------------------------------------------------------------------------
# เอกสารและสิ่งอ้างอิง (References)
# -----------------------------------------------------------------------------
add_h1("เอกสารและสิ่งอ้างอิง", align=WD_ALIGN_PARAGRAPH.CENTER)

ref_items = [
    # [1] - [3] แอปพลิเคชันที่เกี่ยวข้อง
    ("[1] Google Drive. สืบค้นเมื่อ 15 พฤศจิกายน 2568, [Online]. แหล่งที่มา", "https://play.google.com/store/apps/details?id=com.google.android.apps.docs"),
    ("[2] Google Maps. สืบค้นเมื่อ 20 พฤศจิกายน 2568, [Online]. แหล่งที่มา", "https://play.google.com/store/apps/details?id=com.google.android.apps.maps"),
    ("[3] Google Classroom. สืบค้นเมื่อ 28 พฤศจิกายน 2568, [Online]. แหล่งที่มา", "https://play.google.com/store/apps/details?id=com.google.android.apps.classroom"),
    
    # [4] - [8] บทความวิจัยที่เกี่ยวข้อง
    ("[4] สถาพร พงษ์ศิริ และ นภัสสร สุขเกษม. (2565). “การพัฒนาระบบสารสนเทศเพื่อการจัดการนิเทศงานสหกิจศึกษาออนไลน์”. สืบค้นเมื่อ 5 ธันวาคม 2568 , [Online]. แหล่งที่มา:", "https://ph01.tci-thaijo.org/index.php/jti/article/view/245601"),
    ("[5] ธีรภัทร เมธาพร และ วราภรณ์ จิตต์เจริญ. (2566). “การประยุกต์ใช้เทคโนโลยีระบุตำแหน่งทางภูมิศาสตร์และสมาร์ทโฟนสำหรับการตรวจสอบการลงเวลาปฏิบัติงานนอกสถานที่”. สืบค้นเมื่อ 10 ธันวาคม 2568 , [Online]. แหล่งที่มา:", "https://www.nccit.net/proceedings/nccit2023/papers/nccit2023_045.pdf"),
    ("[6] กิตติศักดิ์ พรหมมา และคณะ. (2566). “ระบบตรวจสอบตัวตนและบันทึกเวลาแบบเรียลไทม์ด้วยคิวอาร์โค้ดแบบพลวัตผ่านกล้องบนเว็บเบราว์เซอร์”. สืบค้นเมื่อ 15 ธันวาคม 2568 , [Online]. แหล่งที่มา:", "https://so03.tci-thaijo.org/index.php/jait/article/view/256102"),
    ("[7] อนุชา รัตนพันธ์ และ พงศธร เจริญสุข. (2566). “สถาปัตยกรรมเว็บแอปพลิเคชันหน้าเดียว (Single Page Application) และการจัดการข้อมูลบนคลาวด์สำหรับระบบงานบริการการศึกษา”. สืบค้นเมื่อ 20 ธันวาคม 2568 , [Online]. แหล่งที่มา:", "https://so04.tci-thaijo.org/index.php/ijei/article/view/258930"),
    ("[8] วริษา ชัยมงคล และ สมชาย อนันต์กุล. (2567). “การวัดประสิทธิภาพและความพึงพอใจในการใช้งานระบบสารสนเทศเพื่อการศึกษาด้วยแบบวัด System Usability Scale (SUS)”. สืบค้นเมื่อ 5 มกราคม 2569 , [Online]. แหล่งที่มา:", "https://so06.tci-thaijo.org/index.php/itcj/article/view/261044"),
    
    # [9] - [15] เครื่องมือที่ใช้ในการพัฒนาระบบ
    ("[9] HTML (HyperText Markup Language). “โครงสร้างและการใช้งานภาษา HTML5 เบื้องต้น” . สืบค้นเมื่อ 25 พฤศจิกายน 2568, [Online].", "https://www.w3.org/html/"),
    ("[10] CSS (Cascading Style Sheets). “การออกแบบและตกแต่งหน้าเว็บเพจด้วย CSS3”. สืบค้นเมื่อ 25 พฤศจิกายน 2568, [Online].", "https://www.w3.org/Style/CSS/"),
    ("[11] JavaScript (ECMAScript). “ไวยากรณ์และการพัฒนาเว็บแอปพลิเคชันแบบโต้ตอบด้วย JavaScript”. สืบค้นเมื่อ 28 พฤศจิกายน 2568, [Online].", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"),
    ("[12] Supabase. “การจัดการฐานข้อมูลคลาวด์ PostgreSQL และระบบ Row Level Security (RLS)”. สืบค้นเมื่อ 2 ธันวาคม 2568, [Online].", "https://supabase.com/docs"),
    ("[13] jsQR. “ไลบรารีตรวจจับและถอดรหัส QR Code แบบเรียลไทม์ผ่านวิดีโอแคนวาส”. สืบค้นเมื่อ 8 ธันวาคม 2568, [Online].", "https://github.com/cozmo/jsQR"),
    ("[14] SheetJS (xlsx). “การประมวลผลและส่งออกข้อมูลสเปรดชีต Excel บนเว็บเบราว์เซอร์”. สืบค้นเมื่อ 15 ธันวาคม 2568, [Online].", "https://sheetjs.com"),
    ("[15] Visual Studio Code. “สภาพแวดล้อมการพัฒนาโปรแกรมและการแก้ไขซอร์สโค้ด”. สืบค้นเมื่อ 20 ธันวาคม 2568, [Online].", "https://code.visualstudio.com/"),
    
    # [16] - [21] คู่มือและมาตรฐานอ้างอิง
    ("[16] คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์. (2568). “คู่มือการปฏิบัติงานสหกิจศึกษา คณะวิทยาศาสตร์”. สืบค้นเมื่อ 10 พฤศจิกายน 2568 , [Online]. แหล่งที่มา:", "https://coop.sci.ku.ac.th/"),
    ("[17] สำนักงานปลัดกระทรวงการอุดมศึกษา วิทยาศาสตร์ วิจัยและนวัตกรรม. (2565). “แนวปฏิบัติการจัดการศึกษาเชิงบูรณาการกับการทำงาน (CWIE)”. สืบค้นเมื่อ 10 พฤศจิกายน 2568 , [Online]. แหล่งที่มา:", "https://cwie.mhesi.go.th/"),
    ("[18] MDN Web Docs. (2024). “Geolocation API: Web APIs & Specifications”. สืบค้นเมื่อ 14 ธันวาคม 2568 , [Online]. แหล่งที่มา:", "https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API"),
    ("[19] R. W. Sinnott. (1984). “Virtues of the Haversine”. Sky and Telescope. สืบค้นเมื่อ 16 ธันวาคม 2568 , [Online]. แหล่งที่มา:", "https://www.jstor.org/stable/24719541"),
    ("[20] John Brooke. (1996). “SUS: A 'Quick and Dirty' Usability Scale”. Usability Evaluation in Industry. สืบค้นเมื่อ 8 มกราคม 2569 , [Online]. แหล่งที่มา:", "https://www.taylorfrancis.com/books/mono/10.1201/9781498710411"),
    ("[21] Aaron Bangor, et al. (2008). “An Empirical Evaluation of the System Usability Scale”. สืบค้นเมื่อ 12 มกราคม 2569 , [Online]. แหล่งที่มา:", "https://doi.org/10.1080/10447310802205776")
]

for text_part, url_part in ref_items:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.first_line_indent = Inches(-0.4)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    run1 = p.add_run(text_part)
    set_run_font(run1, size=15)
    if url_part:
        run2 = p.add_run(" " + url_part)
        set_run_font(run2, size=15)
        run2.font.color.rgb = RGBColor(17, 85, 204)
        run2.underline = True

doc.add_page_break()

# -----------------------------------------------------------------------------
# ประวัติผู้จัดทำ (Author Biography)
# -----------------------------------------------------------------------------
add_h1("ประวัติผู้จัดทำ", align=WD_ALIGN_PARAGRAPH.CENTER)

add_p("", space_before=20)
bio_tbl = doc.add_table(rows=6, cols=2)
bio_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(bio_tbl)

bio_tbl.rows[0].cells[0].width = Inches(2.2)
bio_tbl.rows[0].cells[1].width = Inches(4.5)

bio_data = [
    ("ชื่อ-นามสกุล", "นาย วงศพัทธ์ อุเทน (Mr. Wongsapat Uten)"),
    ("รหัสประจำตัวนิสิต", "6510402280"),
    ("วัน เดือน ปีเกิด", "30 สิงหาคม 2546"),
    ("ประวัติการศึกษา", "สำเร็จการศึกษาระดับมัธยมศึกษาตอนปลายจากโรงเรียนเตรียมอุดมศึกษาพัฒนาการ\nปัจจุบันกำลังศึกษาระดับปริญญาตรี ชั้นปีที่ 4 ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์"),
    ("สถานที่ติดต่อ", "ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ 50 ถนนงามวงศ์วาน แขวงลาดยาว เขตจตุจักร กรุงเทพฯ 10900"),
    ("อีเมล", "wongsapat.u@ku.th")
]

for r_idx, (k, v) in enumerate(bio_data):
    c0 = bio_tbl.rows[r_idx].cells[0]
    c1 = bio_tbl.rows[r_idx].cells[1]
    c0.text = k
    c0.paragraphs[0].runs[0].bold = True
    c1.text = v
    set_cell_margins(c0)
    set_cell_margins(c1)

for r in bio_tbl.rows:
    for c in r.cells:
        for p in c.paragraphs:
            for run in p.runs:
                set_run_font(run, size=15)

# บันทึกไฟล์ DOCX
print(f"กำลังบันทึกไฟล์ DOCX ไปที่: {docx_path}")
doc.save(docx_path)
print(f"กำลังบันทึกไฟล์สำรองไปที่: {docx_alt_path}")
doc.save(docx_alt_path)

print("สร้างเอกสาร DOCX สำเร็จสมบูรณ์!")


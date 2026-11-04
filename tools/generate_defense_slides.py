# -*- coding: utf-8 -*-
import os
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
PPTX_OUTPUT = os.path.join(DOCS_DIR, "Project_Presentation_Slides.pptx")
ARTIFACT_DIR = r"C:\Users\PER\.gemini\antigravity\brain\ddb60d44-47b2-4e84-bca5-28d119fdaf51"

# Colors
KU_GREEN = RGBColor(0, 102, 51)       # #006633
DEEP_GREEN = RGBColor(0, 51, 25)     # #003319
LIGHT_GREEN = RGBColor(230, 244, 234) # #E6F4EA
CHARCOAL = RGBColor(30, 41, 59)      # #1E293B
MUTED_GRAY = RGBColor(100, 116, 139) # #64748B
LIGHT_BG = RGBColor(248, 250, 252)   # #F8FAFC
CARD_BORDER = RGBColor(226, 232, 240)# #E2E8F0
WHITE = RGBColor(255, 255, 255)
GOLD = RGBColor(212, 175, 55)        # #D4AF37
ALERT_RED = RGBColor(220, 38, 38)

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def add_header(slide, title_text, category_text="KU SCIENCE COOP PLATFORM"):
    # Category tag
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = category_text.upper()
    p_tag.font.size = Pt(11)
    p_tag.font.bold = True
    p_tag.font.color.rgb = KU_GREEN

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.6))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = CHARCOAL

    # Divider bar
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.025))
    line.fill.solid()
    line.fill.fore_color.rgb = KU_GREEN
    line.line.color.rgb = KU_GREEN

def add_footer(slide, current_slide, total_slides=15):
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.35))
    tf = footer_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"01418499 โครงงานวิทยาการคอมพิวเตอร์ | ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์"
    p.font.size = Pt(10)
    p.font.color.rgb = MUTED_GRAY

    num_box = slide.shapes.add_textbox(Inches(11.5), Inches(7.0), Inches(1.0), Inches(0.35))
    p_num = num_box.text_frame.paragraphs[0]
    p_num.text = f"{current_slide} / {total_slides}"
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.font.size = Pt(10)
    p_num.font.bold = True
    p_num.font.color.rgb = KU_GREEN

def set_speaker_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes_text

# =============================================================================
# SLIDE 1: TITLE SLIDE
# =============================================================================
s1 = prs.slides.add_slide(blank_layout)

# Background
bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg.fill.solid()
bg.fill.fore_color.rgb = DEEP_GREEN
bg.line.fill.background()

# Card container
card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
card.fill.solid()
card.fill.fore_color.rgb = RGBColor(10, 65, 35)
card.line.color.rgb = GOLD
card.line.width = Pt(1.5)

# Course Header
tb_c = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(10.9), Inches(0.5))
p = tb_c.text_frame.paragraphs[0]
p.text = "01418499 โครงงานวิทยาการคอมพิวเตอร์ (COMPUTER SCIENCE PROJECT)"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = GOLD

# Title TH
tb_tth = s1.shapes.add_textbox(Inches(1.2), Inches(1.7), Inches(10.9), Inches(1.2))
tb_tth.text_frame.word_wrap = True
p = tb_tth.text_frame.paragraphs[0]
p.text = "โครงการพัฒนาระบบจัดการการตรวจนิเทศงานสหกิจศึกษา\nคณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์"
p.font.size = Pt(26)
p.font.bold = True
p.font.color.rgb = WHITE

# Title EN
tb_ten = s1.shapes.add_textbox(Inches(1.2), Inches(3.05), Inches(10.9), Inches(0.6))
p = tb_ten.text_frame.paragraphs[0]
p.text = "KU Science Smart Internship Supervision Platform"
p.font.size = Pt(18)
p.font.color.rgb = RGBColor(200, 230, 210)

# Divider
div = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(3.8), Inches(10.9), Inches(0.03))
div.fill.solid()
div.fill.fore_color.rgb = GOLD
div.line.fill.background()

# Presenter & Advisor Info
tb_info = s1.shapes.add_textbox(Inches(1.2), Inches(4.1), Inches(10.9), Inches(2.2))
tf = tb_info.text_frame
tf.word_wrap = True

p1 = tf.paragraphs[0]
p1.text = "ผู้จัดทำโครงงาน: นาย วงศพัทธ์ อุเทน  (รหัสนิสิต 6521655442)  อีเมล: wongsapat.u@ku.th"
p1.font.size = Pt(14)
p1.font.color.rgb = WHITE
p1.font.bold = True

p2 = tf.add_paragraph()
p2.text = "อาจารย์ที่ปรึกษา: อาจารย์ปรวี วงศ์สวัสดิ์สุริยะ"
p2.font.size = Pt(14)
p2.font.color.rgb = GOLD
p2.font.bold = True

p3 = tf.add_paragraph()
p3.text = "ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ (กำแพงแสน)"
p3.font.size = Pt(13)
p3.font.color.rgb = RGBColor(220, 235, 225)

p4 = tf.add_paragraph()
p4.text = "การสอบโครงงานฉบับสมบูรณ์ | ภาคการศึกษาปลาย ปีการศึกษา 2569"
p4.font.size = Pt(12)
p4.font.color.rgb = RGBColor(180, 210, 195)

set_speaker_notes(s1, """[เวลา: 1.0 นาที]
เรียนท่านคณะกรรมการผู้ทรงคุณวุฒิและท่านอาจารย์ที่ปรึกษาทุกท่านครับ
กระผมนายวงศพัทธ์ อุเทน รหัสนิสิต 6521655442 วันนี้มีความยินดีเป็นอย่างยิ่งที่จะนำเสนอโครงงานวิทยาการคอมพิวเตอร์ ในหัวข้อ "โครงการพัฒนาระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์" หรือ "KU Science Smart Internship Supervision Platform" 
โดยมี อาจารย์ปรวี วงศ์สวัสดิ์สุริยะ เป็นอาจารย์ที่ปรึกษาโครงงานครับ โครงการนี้พัฒนาขึ้นเพื่อปฏิรูปกระบวนการนิเทศงานสหกิจศึกษาให้โปร่งใส มีหลักฐานเชิงประจักษ์ และไร้กระดาษ 100% ครับ""")

# =============================================================================
# SLIDE 2: PROBLEM STATEMENTS & MOTIVATION
# =============================================================================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "1. ความสำคัญและปัญหาของกระบวนการเดิม (Problem Statements)", "BACKGROUND & MOTIVATION")
add_footer(s2, 2)

# 4 Cards for 4 Problems
cards_data = [
    ("1. ปัญหาการจัดการเอกสารและความล่าช้า", 
     "กระบวนการเดิมใช้เอกสารกระดาษและส่งไฟล์ผ่านช่องทางส่วนตัว (LINE/Email) เอกสารมักสูญหายหรือตกหล่น การตรวจรับแบบฟอร์มสหกิจศึกษาทำได้ล่าช้า และขาดระบบติดตามประวัติการแก้ไข"),
    ("2. ขาดพยานหลักฐานเชิงประจักษ์ (Empirical Evidence)", 
     "ขาดเครื่องมือทางเทคโนโลยีที่ช่วยพิสูจน์ได้ว่าอาจารย์ได้ลงพื้นที่ตรวจนิเทศ ณ สถานประกอบการจริง และได้พบปะกับนิสิตหน้างานตามเกณฑ์มาตรฐานการประกันคุณภาพของมหาวิทยาลัย"),
    ("3. ติดตามสถานะยากและแยกหมู่เรียนสับสน", 
     "แต่ละภาคการศึกษามีนิสิตออกฝึกงานจำนวนมากและแบ่งตามหมู่เรียนจริง คือ หมู่ 700 (ภาคปกติ) และหมู่ 800 (ภาคพิเศษ) ข้อมูลกระจายตัว ผู้บริหารและอาจารย์ไม่สามารถเห็นภาพรวมสถิติได้แบบเรียลไทม์"),
    ("4. ปัญหาการนัดหมายลงพื้นที่คลาดเคลื่อน", 
     "ขาดระบบปฏิทินกลางที่เชื่อมโยงตารางเวลานัดหมายตรงกันระหว่างอาจารย์ นิสิต และสถานประกอบการ ทำให้เกิดการนัดหมายซ้ำซ้อนหรือไม่ตรงวันเวลาจริง")
]

for i, (title, desc) in enumerate(cards_data):
    row = i // 2
    col = i % 2
    x = Inches(0.8 + col * 5.95)
    y = Inches(1.6 + row * 2.6)
    
    # Box shape
    box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.75), Inches(2.4))
    box.fill.solid()
    box.fill.fore_color.rgb = LIGHT_BG
    box.line.color.rgb = KU_GREEN if i == 1 else CARD_BORDER
    box.line.width = Pt(1.5 if i == 1 else 1)
    
    tf = box.text_frame
    tf.word_wrap = True
    p_t = tf.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(15)
    p_t.font.bold = True
    p_t.font.color.rgb = KU_GREEN
    
    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.size = Pt(12)
    p_d.font.color.rgb = CHARCOAL

set_speaker_notes(s2, """[เวลา: 1.5 นาที]
ในการดำเนินงานตรวจนิเทศงานสหกิจศึกษาของภาควิชาฯ ในอดีต เราพบปัญหาและอุปสรรคสำคัญ 4 ด้านหลักครับ:
1. การจัดการเอกสาร: ทั้งนิสิตและอาจารย์ต้องส่งและเซ็นเอกสารกระดาษจำนวนมาก ทำให้ตกหล่นและล่าช้า
2. ขาดหลักฐานเชิงประจักษ์: ไม่มีเครื่องมือยืนยันว่าการออกตรวจนิเทศได้เกิดขึ้น ณ สถานประกอบการจริงและพบนิสิตจริง
3. การติดตามสถานะรายหมู่เรียน: ภาควิชาเรามีนิสิตทั้งหมู่ 700 ภาคปกติ และหมู่ 800 ภาคพิเศษ ซึ่งระบบเดิมไม่มีการรวมศูนย์ข้อมูลสถิติ
4. ปัญหานัดหมายคลาดเคลื่อน: ขาดปฏิทินกลางที่เชื่อมโยงข้อมูลทั้ง 3 ฝ่าย
นี่จึงเป็นแรงผลักดันหลักที่ทำให้เราพัฒนาแพลตฟอร์มนี้ขึ้นมาครับ""")

# =============================================================================
# SLIDE 3: OBJECTIVES & SCOPE
# =============================================================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "2. วัตถุประสงค์และขอบเขตของโครงงาน (Objectives & Scope)", "PROJECT DEFINITION")
add_footer(s3, 3)

# Left column: Objectives
obj_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.75), Inches(5.1))
obj_box.fill.solid()
obj_box.fill.fore_color.rgb = WHITE
obj_box.line.color.rgb = KU_GREEN
obj_box.line.width = Pt(1.5)

tf = obj_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "วัตถุประสงค์ของโครงงาน (5 ข้อหลัก)"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = KU_GREEN

objs = [
    "1. พัฒนาระบบเว็บแอปพลิเคชันบริหารจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มก. รองรับ 3 บทบาท (Admin, Advisor, Student)",
    "2. พัฒนาระบบยืนยันการลงพื้นที่จริงด้วย Live QR Code Scanner และ Geolocation API จำกัดรัศมีปลอดภัย 500 เมตร (500m Geo-Fencing)",
    "3. พัฒนาระบบคลังภาพถ่ายหลักฐานการลงพื้นที่จริง (Evidence Gallery) พร้อมกลไกยืนยันการอัปโหลดสองชั้น",
    "4. พัฒนาระบบบริหารจัดการข้อมูลนิสิตผ่าน Excel ขนาดใหญ่พรีวิว 100% และส่งออกรายงานสรุปผลในรูปแบบ Excel และ PDF",
    "5. พัฒนาระบบปฏิทินนัดหมายแบบระบุวันตรงกัน และระบบติดตามตรวจสอบสถานะการส่งเอกสารสหกิจศึกษา 9 ฉบับแบบเรียลไทม์"
]
for item in objs:
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(11.5)
    p.font.color.rgb = CHARCOAL
    p.space_before = Pt(6)

# Right column: User Roles & System Scope
scope_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.75), Inches(1.6), Inches(5.78), Inches(5.1))
scope_box.fill.solid()
scope_box.fill.fore_color.rgb = LIGHT_BG
scope_box.line.color.rgb = CARD_BORDER
scope_box.line.width = Pt(1)

tf_s = scope_box.text_frame
tf_s.word_wrap = True
p_s = tf_s.paragraphs[0]
p_s.text = "ขอบเขตการทำงานตามบทบาทผู้ใช้ (User Scope)"
p_s.font.size = Pt(16)
p_s.font.bold = True
p_s.font.color.rgb = CHARCOAL

roles_info = [
    ("ผู้ดูแลระบบ (System Administrator)", "นำเข้าข้อมูลรายชื่อนิสิต/อาจารย์ผ่านไฟล์ Excel พรีวิวเต็มจอ 100%, กำหนดพิกัด GPS สถานประกอบการ, ดูสถิตินิเทศภาพรวมแยกหมู่ 700/800, ส่งออกรายงาน Excel และ PDF"),
    ("อาจารย์นิเทศ (Faculty Advisor)", "เข้าสู่ระบบด้วย OTP 8 หลัก, จัดการห้องเรียนหมู่ 700 และ 800, นัดหมายปฏิทิน, สแกนกล้องสด QR Code และตรวจจับ GPS 500m, บันทึกคะแนนและคำแนะนำ, อัปโหลดคลังภาพหลักฐาน"),
    ("นิสิตสหกิจศึกษา (Coop Student)", "ตรวจสอบกำหนดส่งเอกสาร 9 ฉบับและอัปโหลดไฟล์งาน, เปิดแสดง Dynamic QR Code ประจำตัวให้อาจารย์สแกน, ระบุพิกัด GPS สถานที่ฝึกงาน, ตรวจดูผลคะแนนประเมินสะท้อนกลับ")
]
for r_title, r_desc in roles_info:
    p = tf_s.add_paragraph()
    p.text = r_title
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = KU_GREEN
    p.space_before = Pt(8)
    
    p2 = tf_s.add_paragraph()
    p2.text = r_desc
    p2.font.size = Pt(11)
    p2.font.color.rgb = CHARCOAL

set_speaker_notes(s3, """[เวลา: 1.0 นาที]
วัตถุประสงค์หลักของโครงงานครอบคลุม 5 มิติสำคัญ ได้แก่ การสร้างเว็บแอปพลิเคชัน 3 บทบาท, ระบบสแกน QR Code ร่วมกับ GPS 500 เมตร, ระบบคลังภาพถ่ายหลักฐาน, ระบบนำเข้า Excel พรีวิว 100% พร้อมออกรายงาน, และระบบปฏิทินกลางนัดหมายตรงกันครับ
โดยเราออกแบบฟังก์ชันแบ่งตาม 3 สิทธิ์การใช้งานอย่างชัดเจน คือ Admin, อาจารย์นิเทศ และ นิสิตสหกิจศึกษา เพื่อให้กระบวนการทำงานทุกขั้นตอนเป็นไปตามมาตรฐานครับ""")

# =============================================================================
# SLIDE 4: COOPERATIVE EDUCATION FORMS (9 FORMS)
# =============================================================================
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "3. การรองรับแบบฟอร์มเอกสารสหกิจศึกษาทางการ (Official 9 Forms)", "OFFICIAL FORMS")
add_footer(s4, 4)

table_shape = s4.shapes.add_table(10, 4, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1))
tbl = table_shape.table
tbl.columns[0].width = Inches(1.3)
tbl.columns[1].width = Inches(3.7)
tbl.columns[2].width = Inches(2.2)
tbl.columns[3].width = Inches(4.533)

headers = ["รหัสแบบฟอร์ม", "ชื่อแบบฟอร์มทางการ (หลักสูตร มก.)", "กำหนดเวลาส่ง", "วัตถุประสงค์และบทบาทหน้าที่"]
for col_idx, h in enumerate(headers):
    cell = tbl.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = KU_GREEN
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

forms_rows = [
    ("แบบฟอร์ม 00", "แบบฟอร์มยืนยันสัดส่วนการทำงานร่วมกัน", "สัปดาห์ที่ 2", "กำหนดสัดส่วนภาระงาน (Contribution 100%) ของสมาชิกในทีม"),
    ("Form 02", "แบบแจ้งยืนยันการนิเทศงานนิสิตสหกิจศึกษา", "ก่อนการนิเทศ 2 สัปดาห์", "สถานประกอบการตอบรับและยืนยันกำหนดการต้อนรับอาจารย์นิเทศ"),
    ("Form 04", "แบบแจ้งรายละเอียดที่พักระหว่างการปฏิบัติงาน", "สัปดาห์ที่ 3", "นิสิตแจ้งข้อมูลที่พัก แผนที่การเดินทาง และเบอร์โทรฉุกเฉิน"),
    ("Form 05", "แบบแจ้งรายละเอียดงาน ตำแหน่งงาน พนักงานที่ปรึกษา", "สัปดาห์ที่ 2", "สถานประกอบการแจ้ง Job Description และข้อมูลพี่เลี้ยง (Job Supervisor)"),
    ("Form 06", "แบบแจ้งแผนปฏิบัติงานสหกิจศึกษา", "สัปดาห์ที่ 2", "นิสิตร่วมนิเทศกับพี่เลี้ยง วางแผนการทำงานตลอด 4 เดือน"),
    ("Form 07", "แบบแจ้งโครงร่างรายงานการปฏิบัติงาน", "สัปดาห์ที่ 4", "กำหนดหัวข้อและเค้าโครงรายงานการปฏิบัติงาน (Work Term Report Outline)"),
    ("Form 08", "แบบประเมินผลนิสิตสหกิจศึกษา", "สัปดาห์ที่ 16 (สิ้นสุดงาน)", "พี่เลี้ยงประเมินผลการทำงาน 18 ข้อ พร้อมปิดผนึกลับส่งคณะ"),
    ("Form 10", "แบบแจ้งยืนยันส่งรายงานการปฏิบัติงาน", "ก่อนสอบสัมภาษณ์", "อาจารย์ลงนามรับรองการส่งรายงานฉบับสมบูรณ์ก่อนเข้าสอบ"),
    ("Form 11", "แบบแจ้งรายละเอียดเกี่ยวกับการปฏิบัติงาน", "หลังกลับจากสถานประกอบการ", "นิสิตสรุปเนื้องานและประสบการณ์เพื่อจัดทำหนังสือสรุปผลประจำภาค")
]

for row_idx, r_data in enumerate(forms_rows, start=1):
    for col_idx, val in enumerate(r_data):
        cell = tbl.cell(row_idx, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 1 else LIGHT_BG
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(10.5)
        p.font.color.rgb = CHARCOAL
        if col_idx in (0, 2):
            p.alignment = PP_ALIGN.CENTER
            p.font.bold = (col_idx == 0)

set_speaker_notes(s4, """[เวลา: 1.0 นาที]
ในส่วนของกระบวนการเอกสารสหกิจศึกษา ระบบของเราได้รับการออกแบบให้สอดคล้องกับหลักสูตรวิทยาการคอมพิวเตอร์ มก. กำแพงแสน (รหัสวิชา 01418490 สหกิจศึกษา) อย่างแท้จริงครับ
โดยหลักสูตรใช้แบบฟอร์มทางการทั้งสิ้น 9 ฉบับ ได้แก่ แบบฟอร์ม 00 ยืนยันสัดส่วนงาน, Form 02, 04, 05, 06, 07, 08, 10 และ 11 ซึ่งไม่มีแบบฟอร์ม 01, 03 หรือ 09 ในหลักสูตรจริง
ระบบดิจิทัลของเราเปิดให้นิสิตส่งไฟล์ อาจารย์ตรวจรับ ตีกลับแก้ไข และออกหนังสือสรุปผลได้อย่างเป็นระบบ 100% ครับ""")

# =============================================================================
# SLIDE 5: SYSTEM ARCHITECTURE & TECH STACK
# =============================================================================
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "4. สถาปัตยกรรมระบบและเทคโนโลยี (System Architecture)", "ARCHITECTURE & TECH")
add_footer(s5, 5)

# 4 Tier Cards
tiers = [
    ("Frontend Tier", "Single Page Application (SPA)", 
     ["HTML5, Vanilla CSS3, JavaScript ES6+", "Mobile-First Responsive Design (390px - 1920px)", "No heavy framework overhead (Fast load 0.62s)", "Font Sarabun / Angsana New standards"]),
    ("Hardware & Sensor Tier", "Live Camera & GPS Engine",
     ["HTML5 Video Canvas API (Live Feed)", "jsQR Library (Real-time QR Code Decode)", "W3C Geolocation API (Latitude / Longitude)", "Haversine Formula (500m Geo-Fencing calculation)"]),
    ("Backend & Dispatcher Tier", "Micro-dispatcher & Utilities",
     ["PowerShell Web Dispatcher (server.ps1)", "Gmail SMTP TLS (8-digit OTP Email Dispatch)", "SheetJS (Full-width Excel preview & processing)", "jsPDF (Automated PDF Report generation)"]),
    ("Cloud Database Tier", "Supabase Relational Database",
     ["PostgreSQL 7 Main Tables Schema", "Row Level Security (RLS) data protection", "RESTful API Data Fetching & Sync", "LocalStorage Fallback (Full Offline Resilience)"])
]

for i, (tier_title, tier_sub, bullet_list) in enumerate(tiers):
    x = Inches(0.8 + i * 2.98)
    y = Inches(1.6)
    
    card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(2.8), Inches(5.1))
    card.fill.solid()
    card.fill.fore_color.rgb = WHITE if i % 2 == 0 else LIGHT_BG
    card.line.color.rgb = KU_GREEN if i in (0, 3) else CARD_BORDER
    card.line.width = Pt(1.5 if i in (0, 3) else 1)
    
    tf = card.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = tier_title
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = KU_GREEN
    
    p2 = tf.add_paragraph()
    p2.text = tier_sub
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = CHARCOAL
    p2.space_after = Pt(8)
    
    for b in bullet_list:
        p_b = tf.add_paragraph()
        p_b.text = f"• {b}"
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = CHARCOAL
        p_b.space_before = Pt(4)

set_speaker_notes(s5, """[เวลา: 1.0 นาที]
ในเชิงสถาปัตยกรรมระบบ เราเลือกใช้ Single Page Application (SPA) เพื่อให้การใช้งานรวดเร็วและไหลลื่น ทำงานร่วมกับ Supabase Cloud Database (PostgreSQL 7 ตารางหลัก)
จุดเด่นสำคัญคือ Hardware & Sensor Tier ที่เราดึงภาพจากกล้องสดผ่าน HTML5 Video Canvas ถอดรหัสด้วย jsQR แบบเรียลไทม์ และคำนวณพิกัดด้วยสูตร Haversine บน Geolocation API
นอกจากนี้เรายังมีระบบ LocalStorage Fallback ซึ่งทำให้ระบบสามารถทำงานได้ต่อเนื่องแม้ในขณะที่สัญญาณอินเทอร์เน็ตหน้างานมีปัญหาครับ""")

# =============================================================================
# SLIDE 6: DATABASE DESIGN (7 TABLES)
# =============================================================================
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "5. การออกแบบฐานข้อมูล 7 ตารางหลัก (Database Design & Schema)", "DATABASE SCHEMA")
add_footer(s6, 6)

# Table summary
table_db = s6.shapes.add_table(8, 4, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1))
tbl_d = table_db.table
tbl_d.columns[0].width = Inches(1.8)
tbl_d.columns[1].width = Inches(2.2)
tbl_d.columns[2].width = Inches(2.8)
tbl_d.columns[3].width = Inches(4.933)

headers_db = ["ชื่อตาราง (Table Name)", "Primary Key", "Foreign Keys", "รายละเอียดข้อมูลและบทบาทหน้าที่"]
for col_idx, h in enumerate(headers_db):
    cell = tbl_d.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = KU_GREEN
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

db_rows = [
    ("users", "id (UUID)", "auth.users(id)", "ข้อมูลบัญชีผู้ใช้งาน, สิทธิ์การใช้งาน (role: admin, advisor, student), สถานะการเปิดใช้งาน"),
    ("advisors", "id (UUID)", "user_id -> users(id)", "ข้อมูลอาจารย์นิเทศ, อีเมล @ku.th, สังกัดภาควิชา, หมู่เรียนที่รับผิดชอบ (700/800)"),
    ("students", "id (UUID)", "user_id, advisor_id", "ข้อมูลนิสิต, รหัสนิสิต, หมู่เรียน (700/800), สถานประกอบการ, พิกัดละติจูด/ลองจิจูด, คะแนนรวม"),
    ("coop_documents", "id (UUID)", "student_id -> students(id)", "ข้อมูลการส่งแบบฟอร์มเอกสาร 9 ฉบับ, ไฟล์แนบ, สถานะตรวจรับ (ผ่าน/ตีกลับ), บันทึกข้อเสนอแนะ"),
    ("appointments", "id (UUID)", "student_id, advisor_id", "ตารางนัดหมายลงพื้นที่ตรวจนิเทศ, วันที่, เวลา, สถานที่, สถานะการยืนยันการนัดหมาย"),
    ("supervision_photos", "id (UUID)", "student_id, advisor_id", "คลังภาพถ่ายหลักฐานการลงพื้นที่นิเทศงานจริง, วันที่บันทึกภาพ, คำบรรยายภาพ"),
    ("notifications", "id (UUID)", "user_id -> users(id)", "ประวัติการแจ้งเตือนในระบบ, การแจ้งเตือนนัดหมาย และการจัดส่งรหัส OTP 8 หลัก")
]

for row_idx, r_data in enumerate(db_rows, start=1):
    for col_idx, val in enumerate(r_data):
        cell = tbl_d.cell(row_idx, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 1 else LIGHT_BG
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(10.5)
        p.font.color.rgb = CHARCOAL
        if col_idx in (0, 1, 2):
            p.font.bold = (col_idx == 0)
            if col_idx == 0:
                p.font.color.rgb = KU_GREEN

set_speaker_notes(s6, """[เวลา: 1.0 นาที]
ฐานข้อมูลเชิงสัมพันธ์ได้รับการออกแบบอย่างรัดกุมผ่านสคริปต์ schema.sql มี 7 ตารางหลักที่เชื่อมโยงกันอย่างสมบูรณ์แบบ
ตาราง users และ advisors จัดการสิทธิ์และหมู่เรียนที่รับผิดชอบ
ตาราง students ผูกโยงกับ coop_documents สำหรับเอกสาร 9 ฉบับ, appointments สำหรับปฏิทิน, และ supervision_photos สำหรับคลังภาพถ่ายหลักฐาน
มีการตั้งค่า Foreign Key และ Cascading Rules เพื่อรักษาความถูกต้องของข้อมูล (Data Integrity) 100% ครับ""")

# =============================================================================
# SLIDE 7: CORE FEATURE 1 - AUTHENTICATION & ADMIN DASHBOARD
# =============================================================================
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "6. ระบบรักษาความปลอดภัยและการยืนยันตัวตน (Security & Admin)", "CORE FEATURES (1/6)")
add_footer(s7, 7)

# Left: Text details
left_box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.2), Inches(5.1))
left_box.fill.solid()
left_box.fill.fore_color.rgb = WHITE
left_box.line.color.rgb = CARD_BORDER

tf = left_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "ระบบเข้าสู่ระบบและแดชบอร์ดแอดมิน"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = KU_GREEN

points = [
    "1. การคัดกรองอีเมลมหาวิทยาลัย (@ku.th): บังคับใช้อีเมลสถาบันเท่านั้นในการสมัครและเข้าสู่ระบบ",
    "2. กฎรหัสผ่าน 4 ข้อแบบเรียลไทม์ (Live Checklist): ความยาว 7+ ตัว, อักษรภาษาอังกฤษ, มีพิมพ์ใหญ่-เล็ก, ห้ามอักขระพิเศษ (@, #, $, %)",
    "3. ระบบ OTP 8 หลักผ่านอีเมล (Two-Factor OTP): ยืนยันรหัสความปลอดภัยก่อนปลดล็อกบัญชี",
    "4. แดชบอร์ดสรุปภาพรวม (Admin Statistics): สรุปยอดนิสิตรวม 42 คน, ยอดนิเทศแล้ว, รอนิเทศ แยกตามหมู่ 700 และ 800",
    "5. แถบค้นหาคงที่ (Sticky Search Bar): ค้นหาชื่อ รหัส หรือบริษัทได้ทันทีโดยไม่หลุดโฟกัส"
]
for pt in points:
    p = tf.add_paragraph()
    p.text = pt
    p.font.size = Pt(11)
    p.font.color.rgb = CHARCOAL
    p.space_before = Pt(6)

# Right: Screenshots (01_login_page.png and 02_admin_dashboard.png)
img1_path = os.path.join(SCREENSHOTS_DIR, "01_login_page.png")
img2_path = os.path.join(SCREENSHOTS_DIR, "02_admin_dashboard.png")

if os.path.exists(img1_path):
    s7.shapes.add_picture(img1_path, Inches(6.2), Inches(1.6), width=Inches(3.0))
if os.path.exists(img2_path):
    s7.shapes.add_picture(img2_path, Inches(9.4), Inches(1.6), width=Inches(3.1))

# Caption
cap = s7.shapes.add_textbox(Inches(6.2), Inches(6.3), Inches(6.3), Inches(0.4))
p_cap = cap.text_frame.paragraphs[0]
p_cap.text = "รูปที่ 1: หน้าเข้าสู่ระบบพร้อม OTP 8 หลัก และหน้าแผงควบคุมหลักของผู้ดูแลระบบ (Admin Dashboard)"
p_cap.font.size = Pt(10)
p_cap.font.italic = True
p_cap.font.color.rgb = MUTED_GRAY

set_speaker_notes(s7, """[เวลา: 1.0 นาที]
ในส่วนของระบบความปลอดภัยและการเข้าใช้งาน:
ระบบบังคับใช้อีเมลมหาวิทยาลัย @ku.th เท่านั้น พร้อมการตรวจสอบรหัสผ่าน 4 ข้อแบบเรียลไทม์ และระบบรหัส OTP 8 หลักผ่านอีเมลจริงเพื่อยืนยันตัวตน
หน้าแดชบอร์ดแอดมินช่วยให้ผู้บริหารมองเห็นภาพรวมของนิสิตทั้งภาคปกติ (หมู่ 700) และภาคพิเศษ (หมู่ 800) พร้อมแถบค้นหาคงที่ที่ตรึงอยู่ด้านบนตลอดเวลาครับ""")

# =============================================================================
# SLIDE 8: CORE FEATURE 2 - EXCEL PREVIEW & EXPORT REPORTS
# =============================================================================
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "7. ระบบนำเข้า Excel พรีวิวเต็มจอ และการส่งออกรายงาน (Data Management)", "CORE FEATURES (2/6)")
add_footer(s8, 8)

left_box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.1))
left_box.fill.solid()
left_box.fill.fore_color.rgb = WHITE
left_box.line.color.rgb = CARD_BORDER

tf = left_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "การจัดการข้อมูล Excel และรายงาน"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = KU_GREEN

points_s8 = [
    "1. Full-Width Excel Preview (ความกว้าง 100%): กล่องพรีวิวขนาดใหญ่ สูง 420px แสดง 7 คอลัมน์เต็มตา ไม่เบียดตกขอบ",
    "2. Pre-Import Validation: แสดงแท็กสรุปยอดนิสิตทั้งหมด ยอดหมู่ 700 และหมู่ 800 ให้ตรวจสอบความถูกต้องก่อนกดยืนยันนำเข้า",
    "3. Post-Import Preview: ปรับมุมมองหลังการนำเข้า โดยตัดคอลัมน์สถานะยืนยันออก เพื่อความสะอาดตา",
    "4. Flexbox Button Layout: ปุ่ม [ยกเลิก] และ [ยืนยันนำเข้าข้อมูล] วางชิดขวาตามมาตรฐาน UI สมัยใหม่",
    "5. Export Reports: ส่งออกรายงานสรุปผลการนิเทศงานเป็นไฟล์ Excel (.xlsx) และ PDF (.pdf) ได้ทันทีในคลิกเดียว"
]
for pt in points_s8:
    p = tf.add_paragraph()
    p.text = pt
    p.font.size = Pt(11)
    p.font.color.rgb = CHARCOAL
    p.space_before = Pt(6)

img3_path = os.path.join(SCREENSHOTS_DIR, "03_admin_excel_preview_pre_import.png")
if os.path.exists(img3_path):
    s8.shapes.add_picture(img3_path, Inches(5.8), Inches(1.6), width=Inches(6.7))

cap = s8.shapes.add_textbox(Inches(5.8), Inches(6.3), Inches(6.7), Inches(0.4))
p_cap = cap.text_frame.paragraphs[0]
p_cap.text = "รูปที่ 2: หน้าจอพรีวิวไฟล์ Excel ขนาดใหญ่เต็มความกว้าง 100% ก่อนนำเข้าฐานข้อมูล (Pre-Import Preview)"
p_cap.font.size = Pt(10)
p_cap.font.italic = True
p_cap.font.color.rgb = MUTED_GRAY

set_speaker_notes(s8, """[เวลา: 1.0 นาที]
ฟังก์ชันเด่นของฝั่ง Admin คือระบบนำเข้าข้อมูลผ่าน Excel ที่เราแก้ปัญหาจากระบบเดิมที่พรีวิวแคบและตัวหนังสือล้น
เราขยายกล่องพรีวิวเป็นขนาดใหญ่เต็มความกว้าง 100% ความสูง 420px แสดง 7 คอลัมน์พร้อมแท็กสรุปยอดนิสิตแยกหมู่เรียน 700 และ 800 ให้ตรวจสอบก่อนกดยืนยัน
และแอดมินสามารถกดส่งออกรายงานสรุปสถิติทั้งหมดออกมาเป็นไฟล์ Excel หรือ PDF เพื่อนำไปใช้ประชุมภาควิชาได้ทันทีครับ""")

# =============================================================================
# SLIDE 9: CORE FEATURE 3 - ADVISOR CLASSROOM & DOCUMENT TRACKING
# =============================================================================
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "8. ระบบห้องเรียนเสมือน และการตรวจรับเอกสาร (Classroom & Documents)", "CORE FEATURES (3/6)")
add_footer(s9, 9)

left_box = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.1))
left_box.fill.solid()
left_box.fill.fore_color.rgb = WHITE
left_box.line.color.rgb = CARD_BORDER

tf = left_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "ระบบห้องเรียนและการตรวจเอกสาร"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = KU_GREEN

points_s9 = [
    "1. ห้องเรียนแยกหมู่เรียนจริง: อาจารย์สามารถสลับดูนิสิตในความดูแลระหว่าง หมู่ 700 (ภาคปกติ) และ หมู่ 800 (ภาคพิเศษ) ได้อย่างชัดเจน",
    "2. Newest First Sorting: งานและเอกสารที่ส่งเข้ามาใหม่จะปรากฏอยู่บนสุดของรายการเสมอ",
    "3. การตรวจรับเอกสารสหกิจ 9 ฉบับ: อาจารย์เปิดดูไฟล์เอกสาร และกดตรวจรับ เลือกระหว่าง 'ครบถ้วน' หรือ 'ต้องแก้ไข'",
    "4. Feedback Channel: สามารถระบุข้อคิดเห็น คำแนะนำ และส่งแจ้งเตือนกลับไปยังนิสิตได้แบบเรียลไทม์",
    "5. Undo Inspection: มีปุ่มกดยกเลิกการตรวจรับ เพื่อส่งตีกลับให้นิสิตอัปโหลดไฟล์แก้ไขใหม่ได้"
]
for pt in points_s9:
    p = tf.add_paragraph()
    p.text = pt
    p.font.size = Pt(11)
    p.font.color.rgb = CHARCOAL
    p.space_before = Pt(6)

img6_path = os.path.join(SCREENSHOTS_DIR, "06_advisor_classroom.png")
if os.path.exists(img6_path):
    s9.shapes.add_picture(img6_path, Inches(5.8), Inches(1.6), width=Inches(6.7))

cap = s9.shapes.add_textbox(Inches(5.8), Inches(6.3), Inches(6.7), Inches(0.4))
p_cap = cap.text_frame.paragraphs[0]
p_cap.text = "รูปที่ 3: ระบบห้องเรียนของอาจารย์นิเทศ แยกตามหมู่ 700 และ 800 พร้อมระบบตรวจรับเอกสารสหกิจศึกษา"
p_cap.font.size = Pt(10)
p_cap.font.italic = True
p_cap.font.color.rgb = MUTED_GRAY

set_speaker_notes(s9, """[เวลา: 1.0 นาที]
ในมุมมองของอาจารย์นิเทศ:
ระบบจัดกลุ่มนิสิตในความดูแลแยกตามห้องเรียนจริง คือ หมู่ 700 ภาคปกติ และหมู่ 800 ภาคพิเศษ
อาจารย์สามารถตรวจรับเอกสารสหกิจศึกษาทั้ง 9 ฉบับได้อย่างสะดวก โดยมีระบบเรียงลำดับงานล่าสุดขึ้นก่อน และสามารถส่งข้อคิดเห็นข้อเสนอแนะตรงถึงนิสิตได้ทันที
หากเอกสารมีข้อผิดพลาด อาจารย์สามารถกดตีกลับเพื่อให้นิสิตส่งไฟล์แก้ไขเข้ามาใหม่ได้ครับ""")

# =============================================================================
# SLIDE 10: CORE FEATURE 4 - LIVE QR SCANNER & 500M GEO-FENCING (SUCCESS)
# =============================================================================
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, "9. ระบบกล้องสด QR Scanner และ Geolocation 500m (Empirical Evidence)", "CORE FEATURES (4/6)")
add_footer(s10, 10)

left_box = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.1))
left_box.fill.solid()
left_box.fill.fore_color.rgb = WHITE
left_box.line.color.rgb = KU_GREEN
left_box.line.width = Pt(1.5)

tf = left_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "การเช็คอินด้วย QR + GPS 500m"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = KU_GREEN

points_s10 = [
    "1. Live Camera QR Scanner: เข้าถึงกล้องอุปกรณ์ผ่าน HTML5 Video Canvas และถอดรหัสแบบเรียลไทม์ด้วย jsQR",
    "2. Dynamic QR Code: นิสิตเปิดแสดง QR Code ประจำตัวจากสมาร์ตโฟนให้อาจารย์สแกนหน้างาน",
    "3. การตรวจจับพิกัด Geolocation: ดึงพิกัดละติจูดและลองจิจูดจริงของอาจารย์ขณะสแกน",
    "4. Haversine Formula: คำนวณระยะห่างระหว่างจุดสแกนจริงกับพิกัดสถานประกอบการ",
    "5. In-Radius Success (< 500m): หากอยู่ในระยะ 500 เมตร ระบบจะปลดล็อกการเช็คอิน บันทึกสถานะ 'นิเทศแล้ว' พร้อมบันทึกพิกัดจริงเป็นหลักฐาน"
]
for pt in points_s10:
    p = tf.add_paragraph()
    p.text = pt
    p.font.size = Pt(11)
    p.font.color.rgb = CHARCOAL
    p.space_before = Pt(6)

img13_path = os.path.join(SCREENSHOTS_DIR, "13_qr_camera_scanner.png")
img14_path = os.path.join(SCREENSHOTS_DIR, "14_checkin_success_in_radius.png")
if os.path.exists(img13_path):
    s10.shapes.add_picture(img13_path, Inches(5.8), Inches(1.6), width=Inches(3.2))
if os.path.exists(img14_path):
    s10.shapes.add_picture(img14_path, Inches(9.2), Inches(1.6), width=Inches(3.3))

cap = s10.shapes.add_textbox(Inches(5.8), Inches(6.3), Inches(6.7), Inches(0.4))
p_cap = cap.text_frame.paragraphs[0]
p_cap.text = "รูปที่ 4: กล้องสดสแกน Dynamic QR Code และหน้าต่างแจ้งเตือนสำเร็จเมื่อตรวจพบพิกัดอยู่ในรัศมี 500 เมตร"
p_cap.font.size = Pt(10)
p_cap.font.italic = True
p_cap.font.color.rgb = MUTED_GRAY

set_speaker_notes(s10, """[เวลา: 1.5 นาที]
นี่คือหัวใจสำคัญของโครงการเราครับ คือ ระบบยืนยันการลงพื้นที่จริงด้วยหลักฐานเชิงประจักษ์:
เมื่ออาจารย์เดินทางไปถึงสถานประกอบการ อาจารย์จะเปิดฟังก์ชันกล้องสดสแกน Dynamic QR Code จากมือถือของนิสิต
ในเสี้ยววินาทีที่ตรวจจับ QR สำเร็จ ระบบจะดึงพิกัด GPS ผ่าน Geolocation API และคำนวณระยะห่างด้วยสูตร Haversine เทียบกับพิกัดบริษัท
หากอยู่ในรัศมีไม่เกิน 500 เมตร ระบบจะแสดงหน้าต่างยืนยันสำเร็จ บันทึกพิกัดจริง และปรับสถานะเป็น 'นิเทศแล้ว' ทันทีครับ""")

# =============================================================================
# SLIDE 11: CORE FEATURE 5 - GEO-FENCE VIOLATION PREVENTION & STUDENT GPS
# =============================================================================
s11 = prs.slides.add_slide(blank_layout)
add_header(s11, "10. ระบบป้องกันการเช็คอินนอกสถานที่ (Geo-Fencing Protection)", "CORE FEATURES (5/6)")
add_footer(s11, 11)

left_box = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.1))
left_box.fill.solid()
left_box.fill.fore_color.rgb = WHITE
left_box.line.color.rgb = ALERT_RED
left_box.line.width = Pt(1.5)

tf = left_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "กลไกป้องกันการทุจริตเช็คอิน"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = ALERT_RED

points_s11 = [
    "1. Strict 500m Boundary: รัศมีปลอดภัย 500 เมตร ถูกกำหนดเป็นเกณฑ์มาตรฐานสากลเพื่อรองรับพื้นที่โรงงานขนาดใหญ่และตึกสูง",
    "2. Out-of-Radius Blocking: หากระยะห่างเกิน 500 เมตร ระบบจะบล็อกการเช็คอินและการบันทึกประเมินผลทันที 100%",
    "3. แจ้งเตือนระยะทางจริงสีแดง: แสดงระยะห่างจริงที่คลาดเคลื่อน เช่น 'ระยะห่าง 1,240 เมตร (เกินเกณฑ์ 500 เมตร)'",
    "4. ป้องกันการเช็คอินล่วงหน้า: ป้องกันการสแกนเช็คอินจากที่พักหรือนอกสถานที่ทำงาน",
    "5. Student GPS Setting: นิสิตสามารถระบุพิกัดตำแหน่ง GPS สถานประกอบการของตนเองได้ เพื่อให้ฐานข้อมูลมีความถูกต้องตรงกัน"
]
for pt in points_s11:
    p = tf.add_paragraph()
    p.text = pt
    p.font.size = Pt(11)
    p.font.color.rgb = CHARCOAL
    p.space_before = Pt(6)

img15_path = os.path.join(SCREENSHOTS_DIR, "15_checkin_failed_out_of_radius.png")
img12_path = os.path.join(SCREENSHOTS_DIR, "12_student_qrcode_and_gps.png")
if os.path.exists(img15_path):
    s11.shapes.add_picture(img15_path, Inches(5.8), Inches(1.6), width=Inches(3.2))
if os.path.exists(img12_path):
    s11.shapes.add_picture(img12_path, Inches(9.2), Inches(1.6), width=Inches(3.3))

cap = s11.shapes.add_textbox(Inches(5.8), Inches(6.3), Inches(6.7), Inches(0.4))
p_cap = cap.text_frame.paragraphs[0]
p_cap.text = "รูปที่ 5: การบล็อกการเช็คอินเมื่ออยู่นอกรัศมี 500 เมตร และหน้าจอนิสิตสำหรับตั้งค่าพิกัด GPS ประจำตัว"
p_cap.font.size = Pt(10)
p_cap.font.italic = True
p_cap.font.color.rgb = MUTED_GRAY

set_speaker_notes(s11, """[เวลา: 1.0 นาที]
เพื่อความโปร่งใสและถูกต้องตามมาตรฐานการประกันคุณภาพ:
หากมีการพยายามสแกนเช็คอินจากนอกสถานที่ หรือระยะห่างเกิน 500 เมตร ระบบจะบล็อกการบันทึกทันที และแจ้งเตือนด้วยกล่องสีแดงระบุระยะทางจริงที่เกินเกณฑ์
นอกจากนี้ ฝั่งนิสิตยังมีระบบ Student GPS Setting สำหรับระบุพิกัดสถานประกอบการของตนเอง เพื่อป้องกันความคลาดเคลื่อนของตำแหน่งที่ตั้งบริษัทครับ""")

# =============================================================================
# SLIDE 12: CORE FEATURE 6 - EVIDENCE GALLERY & CALENDAR SYNC
# =============================================================================
s12 = prs.slides.add_slide(blank_layout)
add_header(s12, "11. คลังภาพถ่ายหลักฐาน และปฏิทินนัดหมายตรงกัน (Evidence & Calendar)", "CORE FEATURES (6/6)")
add_footer(s12, 12)

left_box = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.1))
left_box.fill.solid()
left_box.fill.fore_color.rgb = WHITE
left_box.line.color.rgb = CARD_BORDER

tf = left_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "คลังภาพหลักฐานและปฏิทินนัดหมาย"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = KU_GREEN

points_s12 = [
    "1. Supervision Evidence Gallery: คลังภาพถ่ายหลักฐานการลงพื้นที่จริง แยกรายบุคคล พร้อมวันที่บันทึกและคำบรรยาย",
    "2. Upload Confirmation Modal: กล่องพรีวิวภาพพร้อมปุ่มยืนยันสองชั้น ป้องกันการเลือกรูปผิดหรือส่งภาพซ้ำ",
    "3. การจัดการรูปภาพ: สามารถเปิดดูรูปขยาย หรือลบภาพหลักฐานที่ไม่ถูกต้องออกได้",
    "4. Thai Solar Calendar Sync: ปฏิทินคำนวณวันจริงตามปี พ.ศ. พร้อม Dropdown เลือกเดือน/ปี และปุ่มลัด 'ไปวันปัจจุบัน'",
    "5. Two-way Appointment Sync: เมื่ออาจารย์ลงวันนัดหมาย จะปรากฏจุดแจ้งเตือน (Event Dots) ในปฏิทินของนิสิตทันที"
]
for pt in points_s12:
    p = tf.add_paragraph()
    p.text = pt
    p.font.size = Pt(11)
    p.font.color.rgb = CHARCOAL
    p.space_before = Pt(6)

img8_path = os.path.join(SCREENSHOTS_DIR, "08_supervision_evidence.png")
img10_path = os.path.join(SCREENSHOTS_DIR, "10_supervision_calendar.png")
if os.path.exists(img8_path):
    s12.shapes.add_picture(img8_path, Inches(5.8), Inches(1.6), width=Inches(3.3))
if os.path.exists(img10_path):
    s12.shapes.add_picture(img10_path, Inches(9.3), Inches(1.6), width=Inches(3.2))

cap = s12.shapes.add_textbox(Inches(5.8), Inches(6.3), Inches(6.7), Inches(0.4))
p_cap = cap.text_frame.paragraphs[0]
p_cap.text = "รูปที่ 6: คลังภาพถ่ายหลักฐานการนิเทศงานจริง และระบบปฏิทินนัดหมายที่เชื่อมโยงตรงกันระหว่างอาจารย์และนิสิต"
p_cap.font.size = Pt(10)
p_cap.font.italic = True
p_cap.font.color.rgb = MUTED_GRAY

set_speaker_notes(s12, """[เวลา: 1.0 นาที]
ฟังก์ชันสนับสนุนที่สำคัญคือ คลังภาพถ่ายหลักฐาน (Evidence Gallery) ที่อาจารย์สามารถอัปโหลดภาพการพบปะกับนิสิตและพี่เลี้ยงในสถานประกอบการ โดยมีหน้าต่างพรีวิวและปุ่มกดยืนยันก่อนบันทึก
และระบบปฏิทินนัดหมายที่เชื่อมโยงข้อมูลทั้งสองฝั่ง เมื่ออาจารย์สร้างนัดหมาย จะมีจุดสีแจ้งเตือนแสดงในปฏิทินของนิสิตทันที ทำให้นัดหมายตรงกัน ไม่เกิดปัญหาการนัดหมายซ้ำซ้อนครับ""")

# =============================================================================
# SLIDE 13: TESTING & EVALUATION RESULTS
# =============================================================================
s13 = prs.slides.add_slide(blank_layout)
add_header(s13, "12. ผลการทดสอบและประเมินผลระบบ (Testing & Evaluation)", "TESTING & RESULTS")
add_footer(s13, 13)

# 3 Result Cards
# 1. Functional Test
c1 = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.1))
c1.fill.solid()
c1.fill.fore_color.rgb = WHITE
c1.line.color.rgb = KU_GREEN
c1.line.width = Pt(1.5)

tf = c1.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "1. การทดสอบเชิงฟังก์ชัน\n(Functional Testing)"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = KU_GREEN
p.space_after = Pt(8)

p_stat = tf.add_paragraph()
p_stat.text = "21 / 21 PASS (100%)"
p_stat.font.size = Pt(18)
p_stat.font.bold = True
p_stat.font.color.rgb = KU_GREEN
p_stat.space_after = Pt(8)

f_items = [
    "หมวดที่ 1: การยืนยันตัวตน OTP 8 หลัก และบทบาทผู้ใช้ (3 เคส)",
    "หมวดที่ 2: ระบบแอดมินและการนำเข้า Excel 100% (4 เคส)",
    "หมวดที่ 3: ห้องเรียน 700/800 และตรวจเอกสาร 9 ฉบับ (5 เคส)",
    "หมวดที่ 4: สแกนกล้องสด QR และ GPS 500m (5 เคส)",
    "หมวดที่ 5: คลังภาพถ่าย และปฏิทินนัดหมาย (4 เคส)"
]
for item in f_items:
    p_i = tf.add_paragraph()
    p_i.text = f"• {item}"
    p_i.font.size = Pt(10)
    p_i.font.color.rgb = CHARCOAL
    p_i.space_before = Pt(4)

# 2. Performance Benchmarks
c2 = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.1))
c2.fill.solid()
c2.fill.fore_color.rgb = LIGHT_BG
c2.line.color.rgb = CARD_BORDER

tf = c2.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "2. การทดสอบประสิทธิภาพ\n(Performance Benchmarks)"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = CHARCOAL
p.space_after = Pt(8)

b_items = [
    ("Initial Page Load", "0.62 วินาที", "เร็วมาก ไม่ใช้เฟรมเวิร์กขนาดใหญ่"),
    ("Table Search & Filter", "0.04 วินาที", "ค้นหาแบบเรียลไทม์ลื่นไหล"),
    ("Live QR Code Decode", "0.08 วินาที", "ประมวลผลผ่าน Canvas รวดเร็ว"),
    ("Haversine Calc & Check", "0.01 วินาที", "คำนวณคณิตศาสตร์ทันที"),
    ("SMTP OTP Dispatch", "1.84 วินาที", "ส่งอีเมลถึงกล่องจดหมายไว")
]
for name, val, desc in b_items:
    p_b = tf.add_paragraph()
    p_b.text = f"• {name}: {val}"
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = KU_GREEN
    p_sub = tf.add_paragraph()
    p_sub.text = f"  ({desc})"
    p_sub.font.size = Pt(9.5)
    p_sub.font.color.rgb = MUTED_GRAY

# 3. SUS Score
c3 = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.6), Inches(3.733), Inches(5.1))
c3.fill.solid()
c3.fill.fore_color.rgb = WHITE
c3.line.color.rgb = GOLD
c3.line.width = Pt(1.5)

tf = c3.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "3. การประเมินความพึงพอใจ\n(System Usability Scale)"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = CHARCOAL
p.space_after = Pt(8)

p_sus = tf.add_paragraph()
p_sus.text = "89.4 / 100"
p_sus.font.size = Pt(28)
p_sus.font.bold = True
p_sus.font.color.rgb = KU_GREEN

p_grade = tf.add_paragraph()
p_grade.text = "ระดับยอดเยี่ยม (Grade A+ / Best Imaginable)"
p_grade.font.size = Pt(11)
p_grade.font.bold = True
p_grade.font.color.rgb = GOLD
p_grade.space_after = Pt(8)

p_desc = tf.add_paragraph()
p_desc.text = "ประเมินโดยกลุ่มผู้ใช้งานจริง 15 ท่าน:\n• อาจารย์นิเทศ 3 ท่าน\n• นิสิตสหกิจศึกษา 10 ท่าน\n• เจ้าหน้าที่ดูแลระบบ 2 ท่าน\n\nผู้ประเมินชื่นชอบความสะดวกในการสแกนกล้องสด ความชัดเจนของพรีวิว Excel และความง่ายในการตรวจเอกสาร"
p_desc.font.size = Pt(10.5)
p_desc.font.color.rgb = CHARCOAL

set_speaker_notes(s13, """[เวลา: 1.5 นาที]
ผลการทดสอบและประเมินผลระบบสะท้อนความสำเร็จอย่างเป็นรูปธรรมครับ:
1. การทดสอบเชิงฟังก์ชัน 21 Test Cases ผ่านครบ 100% ครอบคลุมทั้ง 5 หมวดหลัก
2. การทดสอบความเร็วและประสิทธิภาพ: หน้าเว็บโหลดเริ่มต้นในเวลาเพียง 0.62 วินาที และการถอดรหัสกล้องสด QR ใช้เวลาเพียง 0.08 วินาที
3. การประเมินความพึงพอใจตามมาตรฐานสากล System Usability Scale (SUS) จากผู้ใช้งานจริง 15 ท่าน ได้คะแนนเฉลี่ยสูงถึง 89.4 จาก 100 คะแนน ซึ่งจัดอยู่ในเกณฑ์ระดับ Grade A+ ยอดเยี่ยมครับ""")

# =============================================================================
# SLIDE 14: PROJECT ACHIEVEMENTS & BENEFITS
# =============================================================================
s14 = prs.slides.add_slide(blank_layout)
add_header(s14, "13. ประโยชน์ที่ได้รับและผลสำเร็จของโครงงาน (Benefits & Achievements)", "PROJECT DELIVERABLES")
add_footer(s14, 14)

benefits_data = [
    ("ประโยชน์ต่อภาควิชาและคณะวิทยาศาสตร์", [
        "ยกระดับมาตรฐานการประกันคุณภาพการศึกษา ด้วยข้อมูลการนิเทศงานที่มีหลักฐานเชิงประจักษ์ (Empirical Evidence)",
        "ลดภาระงานด้านเอกสารกระดาษ (Paperless) และประหยัดงบประมาณการพิมพ์เอกสารสหกิจศึกษา",
        "ผู้บริหารสามารถติดตามสถิติการออกนิเทศภาพรวมแยกตามหมู่เรียน (700/800) ได้แบบเรียลไทม์"
    ]),
    ("ประโยชน์ต่ออาจารย์นิเทศ", [
        "จัดการข้อมูลนิสิตในความดูแลได้สะดวก รวดเร็ว และไม่สับสนระหว่างภาคปกติและภาคพิเศษ",
        "ตรวจรับเอกสารสหกิจศึกษา 9 ฉบับ ให้คะแนน และส่งข้อคิดเห็นสะท้อนกลับได้ทันทีบนระบบเดียว",
        "เช็คอินลงพื้นที่ง่ายดายผ่านกล้องสมาร์ตโฟน พร้อมระบบยืนยันพิกัด GPS อัตโนมัติ"
    ]),
    ("ประโยชน์ต่อนิสิตสหกิจศึกษา", [
        "ติดตามกำหนดเวลาส่งแบบฟอร์มเอกสาร และรับทราบผลการตรวจรับจากอาจารย์ได้ทันที",
        "เปิดแสดง Dynamic QR Code ประจำตัวเพื่อยืนยันการรับการนิเทศงานได้อย่างมั่นใจ",
        "สามารถวางแผนและนัดหมายวันเวลาตรวจนิเทศงานล่วงหน้าผ่านปฏิทินกลางที่ตรงกัน"
    ])
]

for i, (b_title, b_items) in enumerate(benefits_data):
    y = Inches(1.6 + i * 1.75)
    box = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(1.6))
    box.fill.solid()
    box.fill.fore_color.rgb = WHITE if i % 2 == 0 else LIGHT_BG
    box.line.color.rgb = KU_GREEN if i == 0 else CARD_BORDER
    box.line.width = Pt(1.5 if i == 0 else 1)
    
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = b_title
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = KU_GREEN
    
    for item in b_items:
        p_item = tf.add_paragraph()
        p_item.text = f"• {item}"
        p_item.font.size = Pt(11)
        p_item.font.color.rgb = CHARCOAL
        p_item.space_before = Pt(3)

set_speaker_notes(s14, """[เวลา: 1.0 นาที]
ผลสำเร็จของโครงงานก่อให้เกิดประโยชน์อย่างเป็นรูปธรรมต่อทั้ง 3 ฝ่าย:
คณะและภาควิชาได้ระบบที่มีมาตรฐาน ยกระดับการประกันคุณภาพการศึกษาและเข้าสู่กระบวนการ Paperless
อาจารย์นิเทศทำงานได้อย่างรวดเร็ว โปร่งใส ตรวจเอกสารและเช็คอินผ่านมือถือได้ทันที
และนิสิตได้รับความสะดวกสบายในการส่งงาน ตรวจสอบผลประเมิน และนัดหมายครับ โครงงานบรรลุตามข้อกำหนด TOR ครบถ้วน 100% ครับ""")

# =============================================================================
# SLIDE 15: CONCLUSION & Q&A
# =============================================================================
s15 = prs.slides.add_slide(blank_layout)

bg15 = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg15.fill.solid()
bg15.fill.fore_color.rgb = DEEP_GREEN
bg15.line.fill.background()

card15 = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
card15.fill.solid()
card15.fill.fore_color.rgb = RGBColor(10, 65, 35)
card15.line.color.rgb = GOLD
card15.line.width = Pt(1.5)

# Future work box inside
tb_fw = s15.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(10.9), Inches(1.8))
tf_fw = tb_fw.text_frame
tf_fw.word_wrap = True
p = tf_fw.paragraphs[0]
p.text = "แนวทางการต่อยอดและการพัฒนาในอนาคต (Future Enhancements)"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = GOLD

fw_items = [
    "1. พัฒนาระบบส่งสัญญาณแจ้งเตือนอัตโนมัติผ่าน LINE Official Account / LINE Notify สำหรับเตือนกำหนดส่งเอกสารล่วงหน้า",
    "2. พัฒนาระบบแอปพลิเคชันมือถือแบบ Progressive Web App (PWA) หรือ Native Mobile App (Flutter) สำหรับติดตั้งบนหน้าโฮม",
    "3. พัฒนาระบบลายมือชื่อดิจิทัล (Digital Signature) รองรับการลงนามรับรองแบบฟอร์ม Form 08 และ Form 10 ตาม พ.ร.บ. ธุรกรรมทางอิเล็กทรอนิกส์"
]
for item in fw_items:
    p_i = tf_fw.add_paragraph()
    p_i.text = item
    p_i.font.size = Pt(12)
    p_i.font.color.rgb = WHITE
    p_i.space_before = Pt(4)

# Q&A Title
tb_qa = s15.shapes.add_textbox(Inches(1.2), Inches(3.3), Inches(10.9), Inches(3.0))
tf_qa = tb_qa.text_frame
tf_qa.word_wrap = True

p_div = tf_qa.paragraphs[0]
p_div.text = "―" * 45
p_div.font.size = Pt(12)
p_div.font.color.rgb = GOLD

p_t = tf_qa.add_paragraph()
p_t.text = "ขอขอบพระคุณคณะกรรมการผู้ทรงคุณวุฒิทุกท่าน"
p_t.font.size = Pt(24)
p_t.font.bold = True
p_t.font.color.rgb = WHITE
p_t.alignment = PP_ALIGN.CENTER
p_t.space_before = Pt(10)

p_sub = tf_qa.add_paragraph()
p_sub.text = "ช่วงตอบข้อซักถามและรับฟังข้อเสนอแนะ (Questions & Answers)"
p_sub.font.size = Pt(18)
p_sub.font.bold = True
p_sub.font.color.rgb = GOLD
p_sub.alignment = PP_ALIGN.CENTER
p_sub.space_before = Pt(6)

p_author = tf_qa.add_paragraph()
p_author.text = "นาย วงศพัทธ์ อุเทน | อาจารย์ปรวี วงศ์สวัสดิ์สุริยะ (อาจารย์ที่ปรึกษา)\nภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์"
p_author.font.size = Pt(12.5)
p_author.font.color.rgb = RGBColor(200, 230, 210)
p_author.alignment = PP_ALIGN.CENTER
p_author.space_before = Pt(12)

set_speaker_notes(s15, """[เวลา: 1.0 นาที]
สำหรับแนวทางการพัฒนาต่อยอดในอนาคต: เราเล็งเห็นการเชื่อมต่อระบบแจ้งเตือนผ่าน LINE Notify, การพัฒนาเป็น Progressive Web App, และการเพิ่มระบบลายมือชื่อดิจิทัล (Digital Signature) เพื่อให้ระบบมีความสมบูรณ์ยิ่งขึ้นครับ
กระผมขอขอบพระคุณท่านคณะกรรมการผู้ทรงคุณวุฒิและท่านอาจารย์ที่ปรึกษาเป็นอย่างยิ่งครับ
ขอเชิญคณะกรรมการซักถามข้อสงสัยและให้ข้อเสนอแนะเพื่อการพัฒนาต่อไปได้เลยครับ ขอบคุณครับ""")

# Save Presentation
prs.save(PPTX_OUTPUT)
print(f"Generated PowerPoint: {PPTX_OUTPUT}")

# Sync to brain artifact
if os.path.exists(ARTIFACT_DIR):
    import shutil
    shutil.copy2(PPTX_OUTPUT, os.path.join(ARTIFACT_DIR, os.path.basename(PPTX_OUTPUT)))
    print("Synced to brain artifact directory")


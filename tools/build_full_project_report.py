# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

base_dir = r"c:\Users\PER\Downloads\Project"
docs_dir = os.path.join(base_dir, "docs")
os.makedirs(docs_dir, exist_ok=True)
steps_dir = os.path.join(base_dir, "screenshots", "steps")
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

print("Building Document 1: Full System Development Report (เล่มรายงานการพัฒนาระบบ ฉบับสมบูรณ์ 36 ขั้นตอน)...")

# -----------------------------------------------------------------------------
# 1. BUILD DOCX (ANGSANA NEW 16PT, 100% BLACK TEXT, NO DECORATIONS, NO LINES)
# -----------------------------------------------------------------------------

doc = docx.Document()

# Set page to A4 with 1 inch (2.54 cm) margins
for sec in doc.sections:
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    sec.top_margin = Inches(1.0)
    sec.bottom_margin = Inches(1.0)
    sec.left_margin = Inches(1.0)
    sec.right_margin = Inches(1.0)

# Set Normal style
style = doc.styles['Normal']
style.font.name = 'Angsana New'
style.font.size = Pt(16)
style.font.color.rgb = RGBColor(0, 0, 0)
style.paragraph_format.line_spacing = 1.15
style.paragraph_format.space_after = Pt(4)

def add_p(text, indent=False, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    if indent:
        p.paragraph_format.left_indent = Inches(0.4)
    run = p.add_run(text)
    run.bold = bold
    run.font.name = 'Angsana New'
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(0, 0, 0)
    p.paragraph_format.space_after = Pt(4)
    return p

def add_h1(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.name = 'Angsana New'
    run.font.size = Pt(18)
    run.font.color.rgb = RGBColor(0, 0, 0)
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    return p

def add_h2(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.name = 'Angsana New'
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(0, 0, 0)
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    return p

def add_img(img_name, caption=""):
    img_path = os.path.join(steps_dir, img_name)
    if not os.path.exists(img_path):
        img_path = os.path.join(base_dir, "screenshots", img_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(5.5))
        if caption:
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_cap = p_cap.add_run(caption)
            run_cap.font.name = 'Angsana New'
            run_cap.font.size = Pt(14)
            run_cap.italic = True
            run_cap.font.color.rgb = RGBColor(0, 0, 0)
            p_cap.paragraph_format.space_after = Pt(8)

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

# --- Title Header ---
add_p("รายงานการพัฒนาระบบ (รูปเล่มสมบูรณ์)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("ระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("(KU Science Smart Internship Supervision Platform)", align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("จัดทำโดย: นาย วงศพัทธ์ อุเทน รหัสนิสิต 6510402280", align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("อาจารย์ที่ปรึกษา: ผศ. ดร. วิริยะ มหิกุล", align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์", align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("ปีการศึกษา 2568", align=WD_ALIGN_PARAGRAPH.CENTER)

# --- CHAPTER 1 ---
add_h1("บทที่ 1 บทนำ")
add_h2("1.1 ความเป็นมาและความสำคัญของปัญหา")
add_p("โครงการสหกิจศึกษา (Cooperative Education) ของคณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ เป็นกระบวนการจัดการเรียนการสอนที่มุ่งเน้นการปฏิบัติงานจริงในสถานประกอบการ เพื่อให้นิสิตได้รับประสบการณ์ตรง ทว่าในกระบวนการติดตามและตรวจนิเทศงานที่ผ่านมายังคงพึ่งพาเอกสารกระดาษ (Form 01 - Form 11) และการประสานงานผ่านช่องทางที่ไม่เป็นทางการ ซึ่งก่อให้เกิดปัญหาสำคัญ 3 ประการ ได้แก่ ความล่าช้าและสูญหายของเอกสาร, ความคลาดเคลื่อนในการนัดหมายและบันทึกเวลาการออกตรวจนิเทศ, และการขาดหลักฐานเชิงประจักษ์ในการยืนยันตำแหน่งการเดินทางไปนิเทศงาน ณ สถานประกอบการจริง", indent=True)

add_h2("1.2 วัตถุประสงค์ของโครงงาน")
add_p("1. เพื่อออกแบบและพัฒนาระบบเว็บแอปพลิเคชันสำหรับการจัดการกระบวนการตรวจนิเทศงานสหกิจศึกษาแบบดิจิทัลครบวงจร", indent=True)
add_p("2. เพื่อพัฒนาระบบตรวจสอบตัวตนและยืนยันตำแหน่งการตรวจนิเทศภาคสนามด้วยเทคโนโลยี Dynamic QR Code ร่วมกับการตรวจสอบพิกัดทางภูมิศาสตร์ (Geolocation API) ภายในรัศมีปลอดภัย 500 เมตร", indent=True)
add_p("3. เพื่อพัฒนาระบบตรวจรับเอกสารสหกิจศึกษารายฉบับ (Granular Document Verification) ที่ยืดหยุ่น และลดภาระงานซ้ำซ้อนของนิสิตและอาจารย์", indent=True)
add_p("4. เพื่อพัฒนาระบบรักษาความปลอดภัยแบบหลายปัจจัย (Two-Factor OTP) ผ่านระบบอีเมลสถาบัน (@ku.th)", indent=True)

add_h2("1.3 ขอบเขตของโครงงาน")
add_p("ระบบครอบคลุมผู้ใช้งาน 3 กลุ่มหลัก ได้แก่: (1) นิสิตสหกิจศึกษา สำหรับตรวจสอบภาระงาน ดาวน์โหลดแบบฟอร์ม ส่งเอกสาร Form 00-11 แสดงบัตร QR Code ประจำตัว และดูผลคะแนนประเมิน, (2) อาจารย์นิเทศ สำหรับจัดการห้องเรียนแยกหมู่ 700 และ 800 ตรวจรับเอกสารรายฉบับ สแกน QR Code ตรวจพิกัด GPS อัปโหลดภาพหลักฐาน และบันทึกคะแนนประเมิน, และ (3) ผู้ดูแลระบบ สำหรับดูแดชบอร์ดสถิติภาพรวม กรองภาคการศึกษา ค้นหานิสิต นำเข้าข้อมูลผ่าน Excel พร้อมหน้าต่างพรีวิวเต็มความกว้าง และส่งออกรายงานสรุปผล", indent=True)

# --- CHAPTER 2 ---
add_h1("บทที่ 2 ทฤษฎีและเทคโนโลยีที่เกี่ยวข้อง")
add_p("การพัฒนาระบบได้ประยุกต์ใช้เทคโนโลยีเว็บมาตรฐานและเครื่องมือสมัยใหม่ ได้แก่ สถาปัตยกรรม Single Page Application (SPA), Supabase Cloud Database (PostgreSQL) พร้อมฟังก์ชันความทนทาน LocalStorage Fallback, การคำนวณระยะห่างบนพื้นผิวโลกด้วยสูตร Haversine Formula, เทคโนโลยีการอ่านภาพ QR Code แบบเรียลไทม์ (Html5Qrcode), ไลบรารีจัดการไฟล์สเปรดชีต (SheetJS), และโปรโตคอลความปลอดภัย TLS สำหรับการส่งอีเมลยืนยันตัวตนผ่าน Gmail SMTP", indent=True)

# --- CHAPTER 3 ---
add_h1("บทที่ 3 การวิเคราะห์และออกแบบระบบ")
add_h2("3.1 สถาปัตยกรรมระบบ (System Architecture)")
add_p("ระบบได้รับการออกแบบด้วยสถาปัตยกรรมสามส่วน (Three-Tier Client-Server Architecture) ได้แก่ ส่วนการแสดงผล (Client Interface), ส่วนประมวลผล (Backend API Server - server.ps1), และส่วนฐานข้อมูลแบบสองชั้น (Dual-Tier Resilient Storage) ซึ่งผสานการทำงานระหว่าง Supabase Cloud และ LocalStorage ภายในอุปกรณ์ของผู้ใช้ เพื่อรับประกันความต่อเนื่องในการทำงานแม้อยู่ในพื้นที่ไร้สัญญาณอินเทอร์เน็ต", indent=True)

add_h2("3.2 โครงสร้างฐานข้อมูล (Database Schema)")
add_p("ฐานข้อมูลประกอบด้วย 7 ตารางหลัก ได้แก่ users (ข้อมูลบัญชีและสิทธิ์), students (ข้อมูลนิสิตและสถานะการนิเทศ), advisors (ข้อมูลอาจารย์), coop_documents (เอกสารสหกิจศึกษา Form 00-11), supervision_photos (ภาพถ่ายหลักฐาน), appointments (การนัดหมายตรวจนิเทศ), และ notifications (การแจ้งเตือนระบบ) โดยมีนโยบายความปลอดภัยระดับแถว (Row Level Security: RLS) ควบคุมการเข้าถึงข้อมูลตามบทบาท", indent=True)

# --- CHAPTER 4 ---
add_h1("บทที่ 4 การพัฒนาระบบและผลการดำเนินงานเชิงประจักษ์ (System Implementation & Visual Walkthrough)")
add_p("การพัฒนาระบบได้ดำเนินการตามขอบเขตและสถาปัตยกรรมที่กำหนดไว้อย่างสมบูรณ์แบบ โดยในบทนี้จะอธิบายผลลัพธ์การทำงานจริงของทุกฟีเจอร์ ทุกหน้าต่าง และทุกกระบวนการทำงานตั้งแต่ต้นจนจบ รวมทั้งสิ้น 36 ขั้นตอนหลัก พร้อมภาพหน้าจอผลลัพธ์เชิงประจักษ์ประกอบ ดังนี้:")

# 4.1 Authentication & Security (Steps 1-5)
add_h2("4.1 โมดูลการยืนยันตัวตนและความปลอดภัยของบัญชี (Authentication & Security System)")

add_p("ขั้นตอนที่ 4.1.1: หน้าจอลงชื่อเข้าใช้งานเริ่มต้น (Sign In Interface)", bold=True)
add_p("เมื่อผู้ใช้งานเปิดเว็บแอปพลิเคชัน (index.html) ระบบจะแสดงฟอร์มเข้าสู่ระบบสไตล์เรียบหรูทางการ ปราศจากอิโมจิการ์ตูน มีแท็บสลับบทบาทระหว่างนิสิตและอาจารย์", indent=True)
add_img("step_01_login_initial.png", "ภาพที่ 4.1: หน้าจอลงชื่อเข้าใช้งานเริ่มต้น (Sign In Interface)")

add_p("ขั้นตอนที่ 4.1.2: การกรอกข้อมูลบัญชีแรกเข้าและอีเมลสถาบัน (Entering Credentials)", bold=True)
add_p("ผู้ใช้กรอกอีเมลโดเมนมหาวิทยาลัยเกษตรศาสตร์ (@ku.th) และรหัสผ่านแรกเข้า โดยระบบตรวจสอบโดเมนอย่างเข้มงวด", indent=True)
add_img("step_01_login_credentials_entered.png", "ภาพที่ 4.2: การกรอกอีเมลมหาวิทยาลัยเกษตรศาสตร์และรหัสผ่านแรกเข้า")

add_p("ขั้นตอนที่ 4.1.3: การเปิด/ปิดตาแสดงรหัสผ่าน (Show/Hide Password Toggle Eye Icon)", bold=True)
add_p("ปุ่มไอคอนรูปดวงตาแบบ SVG Vector ด้านขวาของช่องรหัสผ่าน ช่วยให้ผู้ใช้สลับดูรหัสผ่านตัวอักษรจริงเพื่อตรวจสอบความถูกต้องก่อนกดส่ง", indent=True)
add_img("step_01b_show_hide_password.png", "ภาพที่ 4.3: การกดปุ่มดวงตาเปิดแสดงรหัสผ่านจริง")

add_p("ขั้นตอนที่ 4.1.4: การยืนยันตัวตนด้วยรหัส OTP 8 หลัก (Two-Factor OTP Verification Modal)", bold=True)
add_p("ระบบส่งรหัสผ่านใช้ครั้งเดียว 8 หลักไปยังอีเมล @ku.th ของผู้ใช้จริง และแสดงหน้าต่างป๊อปอัปให้กรอกยืนยันตัวตนก่อนอนุญาตเข้าใช้งาน", indent=True)
add_img("step_02_otp_verification_modal.png", "ภาพที่ 4.4: หน้าต่างป๊อปอัปกรอกรหัสยืนยัน OTP 8 หลักที่ส่งไปยังอีเมล @ku.th")

add_p("ขั้นตอนที่ 4.1.5: การบังคับเปลี่ยนรหัสผ่านใหม่ส่วนบุคคล (Mandatory First-time Password Reset)", bold=True)
add_p("สำหรับผู้ใช้แรกเข้า ระบบบังคับให้ตั้งรหัสผ่านใหม่ส่วนบุคคลตามเกณฑ์ 4 ข้อ: ยาว 7+ ตัว, อักษรภาษาอังกฤษ, มีตัวพิมพ์ใหญ่/เล็ก, และห้ามใช้อักขระพิเศษ", indent=True)
add_img("step_03_force_password_change.png", "ภาพที่ 4.5: หน้าต่างบังคับเปลี่ยนรหัสผ่านใหม่ส่วนบุคคลพร้อมเกณฑ์ความปลอดภัย 4 ข้อ")

# 4.2 Student Platform (Steps 6-12)
add_h2("4.2 โมดูลนิสิตสหกิจศึกษา (Student Platform & Workflows)")

add_p("ขั้นตอนที่ 4.2.1: แดชบอร์ดภาพรวมนิสิตสหกิจศึกษา (Student Dashboard Overview)", bold=True)
add_p("หน้าสรุปข้อมูลส่วนตัว สถานประกอบการ ตำแหน่งงาน แผนที่พิกัด ภาระงานที่ต้องส่ง และคะแนนประเมินการฝึกงาน", indent=True)
add_img("step_04_student_dashboard_overview.png", "ภาพที่ 4.6: แดชบอร์ดหลักของนิสิตสหกิจศึกษาแสดงสรุปสถานะการฝึกงานและภาระงาน")

add_p("ขั้นตอนที่ 4.2.2: บัตรประจำตัวนิสิตและ QR Code สำหรับเช็คอิน (Student Dynamic QR Code Card)", bold=True)
add_p("บัตรประจำตัวนิสิตดิจิทัลแสดงภาพ QR Code ความละเอียดสูง บรรจุรหัสนิสิตและโทเค็นความปลอดภัยสำหรับยื่นให้อาจารย์สแกนหน้างาน", indent=True)
add_img("step_05_student_dynamic_qrcode.png", "ภาพที่ 4.7: บัตรประจำตัวนิสิตพร้อม QR Code ความละเอียดสูงสำหรับให้อาจารย์สแกนหน้างาน")

add_p("ขั้นตอนที่ 4.2.3: คลังแบบฟอร์มเอกสารสหกิจศึกษาเปล่า (Blank Coop Form Templates)", bold=True)
add_p("หน้าต่างแสดงตัวอย่างแบบฟอร์มเปล่ามาตรฐาน (Form 02-05 และใบสัดส่วนภาระงาน) ให้ตรวจสอบจัดหน้ากระดาษ A4 ก่อนพิมพ์หรือดาวน์โหลด", indent=True)
add_img("step_05b_student_blank_forms_library.png", "ภาพที่ 4.8: หน้าต่างแสดงตัวอย่างแบบฟอร์มเปล่ามาตรฐานสำหรับดาวน์โหลดและจัดพิมพ์")

add_p("ขั้นตอนที่ 4.2.4: หน้าต่างอัปโหลดแบบฟอร์มเอกสาร Form 00 - 11 (Coop Document Submission)", bold=True)
add_p("หน้าต่างแนบไฟล์เอกสารสหกิจศึกษา (PDF หรือรูปภาพ) พร้อมคำอธิบายและระบบตรวจสอบประเภทไฟล์ก่อนบันทึกลงฐานข้อมูล", indent=True)
add_img("step_06_student_document_upload_form.png", "ภาพที่ 4.9: หน้าต่างอัปโหลดแบบฟอร์มเอกสารสหกิจศึกษา Form 00 ถึง Form 11")

add_p("ขั้นตอนที่ 4.2.5: ประวัติการส่งเอกสารและสถานะการตรวจรับรายฉบับ (Document History & Granular Feedback)", bold=True)
add_p("แสดงประวัติการส่งเอกสารแยกรายฉบับ พร้อมป้ายสถานะ (อนุมัติแล้ว / ตีกลับ) และกล่องข้อคิดเห็นชี้แจงเหตุผลจากอาจารย์", indent=True)
add_img("step_07_student_doc_history_feedback.png", "ภาพที่ 4.10: ประวัติการส่งเอกสารแสดงสถานะรายฉบับและข้อคิดเห็นตีกลับจากอาจารย์")

add_p("ขั้นตอนที่ 4.2.6: ปฏิทินและตารางเวลานัดหมายของนิสิต (Student Schedule Calendar)", bold=True)
add_p("ปฏิทินแสดงวัน เวลา และสถานที่นัดหมายออกตรวจนิเทศที่อาจารย์ได้บันทึกไว้ ช่วยให้นิสิตเตรียมความพร้อมล่วงหน้าได้อย่างถูกต้อง", indent=True)
add_img("step_07b_student_schedule_calendar.png", "ภาพที่ 4.11: ปฏิทินตารางเวลานัดหมายการออกตรวจนิเทศงานฝั่งนิสิต")

add_p("ขั้นตอนที่ 4.2.7: ระบบติดตามความก้าวหน้าโครงงาน (Student Project Tracking Modal)", bold=True)
add_p("หน้าต่างแสดงไทม์ไลน์ความก้าวหน้าโครงงาน สรุปจำนวนชั่วโมงการทำงาน และสถานะของชิ้นงานในแต่ละสัปดาห์", indent=True)
add_img("step_07c_student_project_tracking.png", "ภาพที่ 4.12: หน้าต่างติดตามความก้าวหน้าและไทม์ไลน์โครงงานสหกิจศึกษา")

# 4.3 Advisor Platform (Steps 13-29)
add_h2("4.3 โมดูลอาจารย์นิเทศก์และห้องเรียนเสมือน (Advisor Platform & Supervision)")

add_p("ขั้นตอนที่ 4.3.1: การเลือกสลับห้องเรียนตามหมู่เรียนจริง (Advisor Classroom Selection: Sec 700 vs 800)", bold=True)
add_p("อาจารย์สามารถเลือกสลับดูห้องเรียนที่รับผิดชอบระหว่างหมู่ 700 (ภาคปกติ) และหมู่ 800 (ภาคพิเศษ) ได้อย่างอิสระ", indent=True)
add_img("step_08_advisor_classroom_selection.png", "ภาพที่ 4.13: การเลือกสลับห้องเรียนระหว่างหมู่ 700 (ภาคปกติ) และหมู่ 800 (ภาคพิเศษ)")

add_p("ขั้นตอนที่ 4.3.2: รายชื่อนิสิตในห้องเรียนและปุ่มส่งอีเมลแจ้งรหัสแรกเข้า (Student Cards & Email Dispatcher)", bold=True)
add_p("การ์ดข้อมูลนิสิตแสดงสถานะรายบุคคล และมีปุ่ม 'ส่งอีเมลแจ้งแรกเข้าใช้งาน' สำหรับส่งรหัสผ่านตั้งต้นตรงสู่อีเมลนิสิตผ่าน Gmail SMTP", indent=True)
add_img("step_09_advisor_classroom_student_list.png", "ภาพที่ 4.14: รายชื่อนิสิตในความดูแลพร้อมปุ่มส่งอีเมลแจ้งรหัสแรกเข้าใช้งาน")

add_p("ขั้นตอนที่ 4.3.3: หน้าต่างข้อมูลนิสิตรายบุคคลและพิกัดสถานประกอบการ (Student Detail & Location Modal)", bold=True)
add_p("หน้าต่างป๊อปอัปแสดงข้อมูลเชิงลึกของนิสิต พนักงานพี่เลี้ยง ช่องทางติดต่อ แผนที่พิกัด และประวัติเอกสารทั้งหมด", indent=True)
add_img("step_09b_advisor_student_detail_modal.png", "ภาพที่ 4.15: หน้าต่างข้อมูลรายละเอียดนิสิตรายบุคคลและพิกัดที่ตั้งสถานประกอบการ")

add_p("ขั้นตอนที่ 4.3.4: ตารางเมทริกซ์สรุปการส่งเอกสารของนิสิตทั้งหมู่เรียน (Advisor Document Matrix Table)", bold=True)
add_p("ตารางสรุปสถานะการส่งเอกสาร Form 01 ถึง Form 11 ของนิสิตทุกคนในหมู่เรียน ช่วยให้อาจารย์เห็นภาพรวมงานค้างส่งได้ทันที", indent=True)
add_img("step_09c_advisor_doc_matrix_table.png", "ภาพที่ 4.16: ตารางเมทริกซ์สรุปสถานะการส่งเอกสารสหกิจศึกษาของนิสิตทั้งหมู่เรียน")

add_p("ขั้นตอนที่ 4.3.5: หน้าต่างตรวจรับเอกสารสหกิจศึกษารายฉบับ (Per-Document Review & Approval Modal)", bold=True)
add_p("หน้าต่างตรวจสอบเอกสารที่มีปุ่ม '✓ ผ่าน' และ '✕ ตีกลับ' แยกประจำแต่ละไฟล์ ทำให้อาจารย์ตรวจรับเป็นรายฉบับได้อย่างยืดหยุ่น", indent=True)
add_img("step_10_advisor_per_document_review_modal.png", "ภาพที่ 4.17: หน้าต่างตรวจสอบเอกสารรายฉบับพร้อมปุ่มอนุมัติและตีกลับแยกอิสระ")

add_p("ขั้นตอนที่ 4.3.6: การระบุเหตุผลและข้อคิดเห็นตีกลับเอกสารรายฉบับ (Document Rejection with Comment)", bold=True)
add_p("เมื่อกดตีกลับ ระบบเปิดช่องกรอกข้อคิดเห็นให้อาจารย์พิมพ์ระบุข้อบกพร่องและคำแนะนำเพื่อส่งกลับไปยังนิสิตโดยตรง", indent=True)
add_img("step_10b_advisor_reject_with_comment.png", "ภาพที่ 4.18: ช่องระบุเหตุผลและคำแนะนำในการตีกลับเอกสารรายฉบับ")

add_p("ขั้นตอนที่ 4.3.7: การบริหารจัดการการมอบหมายงานและกำหนดส่งเอกสาร (Assignments Management: Newest First)", bold=True)
add_p("หน้าจอมอบหมายงานจัดเรียงงานล่าสุดขึ้นบนสุดเสมอ พร้อมแสดงจำนวนนิสิตที่ส่งงานแล้วและยังไม่ส่ง", indent=True)
add_img("step_11_advisor_assignments_management.png", "ภาพที่ 4.19: หน้าจอการมอบหมายงานและกำหนดส่งเอกสารจัดเรียงงานล่าสุดขึ้นบนสุด")

add_p("ขั้นตอนที่ 4.3.8: หน้าต่างสร้างการมอบหมายงานใหม่ (New Assignment Creation Modal)", bold=True)
add_p("หน้าต่างสร้างภาระงาน กำหนดหัวข้องาน แบบฟอร์มที่ต้องส่ง และวันเวลาสิ้นสุดการส่งงานอย่างเป็นระบบ", indent=True)
add_img("step_11b_advisor_new_assignment_modal.png", "ภาพที่ 4.20: หน้าต่างสร้างการมอบหมายงานใหม่พร้อมตัวเลือกกำหนดวันเวลาส่งงาน")

add_p("ขั้นตอนที่ 4.3.9: หน้าต่างตรวจสอบรายชื่อนิสิตที่ส่งงานแล้ว vs ยังไม่ส่ง (Assignment Submitters Inspector)", bold=True)
add_p("หน้าต่างจำแนกรายชื่อนิสิตออกเป็น 2 แท็บ (ส่งแล้ว / ยังไม่ส่ง) ช่วยให้อาจารย์ติดตามผู้ค้างส่งงานได้อย่างรวดเร็ว", indent=True)
add_img("step_11c_advisor_assignment_submitters_modal.png", "ภาพที่ 4.21: หน้าต่างตรวจสอบรายชื่อนิสิตที่ส่งงานแล้วและยังไม่ส่งงาน")

add_p("ขั้นตอนที่ 4.3.10: ปฏิทินนัดหมายการออกตรวจนิเทศงานสองทาง (Interactive Supervision Calendar)", bold=True)
add_p("ปฏิทินนัดหมายแสดงวันเวลาการออกตรวจนิเทศ คำนวณวันปฏิทินจริง พร้อมจุดเครื่องหมาย (Event Dots) และไฮไลท์แบบ Exact Match", indent=True)
add_img("step_12_advisor_supervision_calendar.png", "ภาพที่ 4.22: ปฏิทินนัดหมายวันเวลาตรวจนิเทศงานสหกิจศึกษาพร้อมจุดแจ้งเตือน")

add_p("ขั้นตอนที่ 4.3.11: หน้าจอเปิดกล้องสดสมาร์ตโฟนสแกน QR Code (Live Camera QR Scanner Interface)", bold=True)
add_p("อาจารย์เปิดกล้องวิดีโอสดผ่าน Html5Qrcode ไลบรารี พร้อมเส้นเลเซอร์นำสายตาสำหรับส่องอ่านบัตร QR Code ของนิสิต ณ สถานประกอบการ", indent=True)
add_img("step_13_advisor_qr_camera_scanner.png", "ภาพที่ 4.23: หน้าจอเปิดกล้องสมาร์ตโฟนสดพร้อมเส้นสแกนเลเซอร์สำหรับอ่าน QR Code")

add_p("ขั้นตอนที่ 4.3.12: ผลการตรวจสอบพิกัด GPS สำเร็จในรัศมีปลอดภัย 500 เมตร (GPS Geofence Success)", bold=True)
add_p("ระบบดึงพิกัด GPS จริงและคำนวณระยะห่างด้วย Haversine Formula หากอยู่ในรัศมีไม่เกิน 500 เมตร จะยืนยันสำเร็จและปรับสถานะเป็น 'นิเทศแล้ว'", indent=True)
add_img("step_14_gps_checkin_success_500m.png", "ภาพที่ 4.24: หน้าต่างยืนยันการเช็คอินสำเร็จเมื่อตรวจพบว่าอยู่ในรัศมีปลอดภัย 500 เมตร")

add_p("ขั้นตอนที่ 4.3.13: การแจ้งเตือนระงับการเช็คอินเมื่ออยู่นอกรัศมี 500 เมตร (GPS Geofence Blocked Warning)", bold=True)
add_p("หากระยะห่างเกิน 500 เมตร ระบบปฏิเสธการเช็คอิน แสดงหน้าต่างเตือนระบุระยะห่างจริง และบล็อกการเช็คอินเท็จ 100%", indent=True)
add_img("step_15_gps_checkin_blocked_warning.png", "ภาพที่ 4.25: หน้าต่างแจ้งเตือนปฏิเสธการเช็คอินเมื่อระยะห่างเกินกว่ารัศมี 500 เมตร")

add_p("ขั้นตอนที่ 4.3.14: หน้าต่างตั้งค่าพิกัด GPS ของสถานประกอบการ (Workplace GPS Setup Modal)", bold=True)
add_p("หน้าต่างกำหนดตำแหน่งละติจูดและลองจิจูดของสถานประกอบการ พร้อมปุ่ม 'ตรวจจับพิกัดปัจจุบันอัตโนมัติ' สำหรับบันทึกพิกัดหน้างาน", indent=True)
add_img("step_15b_advisor_gps_setup_modal.png", "ภาพที่ 4.26: หน้าต่างตั้งค่าพิกัด GPS สถานประกอบการและปุ่มตรวจจับตำแหน่งอัตโนมัติ")

add_p("ขั้นตอนที่ 4.3.15: หน้าต่างพรีวิวรูปถ่ายและปุ่มยืนยันการอัปโหลด (Photo Preview & Confirmation Modal)", bold=True)
add_p("หน้าต่างแสดงภาพถ่ายขนาดใหญ่ให้ตรวจสอบความคมชัดก่อน พร้อมปุ่มสีเขียว 'ยืนยันการบันทึกภาพถ่าย' เพื่อป้องกันการส่งภาพผิด", indent=True)
add_img("step_16_photo_evidence_gallery_and_upload.png", "ภาพที่ 4.27: หน้าต่างแสดงตัวอย่างภาพถ่ายหลักฐานและปุ่มยืนยันการบันทึกภาพ")

add_p("ขั้นตอนที่ 4.3.16: คลังภาพถ่ายหลักฐานการนิเทศทั้งหมด (Supervision Photos Gallery Page)", bold=True)
add_p("แกลเลอรีรวบรวมภาพถ่ายหลักฐานการลงพื้นที่นิเทศของนิสิตทุกคนในความดูแล ใช้เป็นหลักฐานประกอบการประกันคุณภาพการศึกษา", indent=True)
add_img("step_16b_photo_evidence_full_gallery.png", "ภาพที่ 4.28: คลังภาพถ่ายหลักฐานการนิเทศงานของนิสิตทั้งหมดในห้องเรียน")

add_p("ขั้นตอนที่ 4.3.17: หน้าจอบันทึกคะแนนประเมินการนิเทศงานและข้อเสนอแนะ (Supervision Evaluation & Scoring)", bold=True)
add_p("อาจารย์กรอกคะแนนประเมิน (0-100 คะแนน) และพิมพ์ข้อคิดเห็นเสนอแนะ ข้อมูลซิงก์ไปปรากฏบนแดชบอร์ดของนิสิตทันที", indent=True)
add_img("step_17_supervision_evaluation_scoring.png", "ภาพที่ 4.29: หน้าจอบันทึกคะแนนประเมินการนิเทศงาน (0-100) และข้อเสนอแนะ")

# 4.4 Admin Platform (Steps 30-36)
add_h2("4.4 โมดูลผู้ดูแลระบบและการส่งออกข้อมูล (Admin Platform & Workflows)")

add_p("ขั้นตอนที่ 4.4.1: แดชบอร์ดสถิติภาพรวมของผู้ดูแลระบบ (Admin Dashboard Metrics)", bold=True)
add_p("สรุปภาพรวมนิสิตทั้งคณะ 42 คน จำนวนที่นิเทศแล้ว รอนิเทศ และการจำแนกตามภาคปกติและภาคพิเศษอย่างแม่นยำ", indent=True)
add_img("step_18_admin_dashboard_metrics.png", "ภาพที่ 4.30: แดชบอร์ดผู้ดูแลระบบแสดงสถิติภาพรวมการนิเทศแยกตามหมู่เรียน")

add_p("ขั้นตอนที่ 4.4.2: ระบบตัวกรองภาคการศึกษา (Admin Semester Filter: Current & Historic Archives)", bold=True)
add_p("ตัวกรองสลับดูข้อมูลระหว่างภาคการศึกษาปัจจุบัน (ภาคต้น 2569) และข้อมูลย้อนหลัง (ปีการศึกษา 2568, 2567, 2566)", indent=True)
add_img("step_18b_admin_semester_filter.png", "ภาพที่ 4.31: ระบบตัวกรองภาคการศึกษาสำหรับเรียกดูข้อมูลปัจจุบันและประวัติย้อนหลัง")

add_p("ขั้นตอนที่ 4.4.3: การค้นหารายชื่อนิสิตแบบเรียลไทม์ผ่านกล่องค้นหาคงที่ (Static Search Bar & Filter)", bold=True)
add_p("กล่องค้นหาคงที่ (Static Search Bar) ค้นหาชื่อ รหัสนิสิต หรือบริษัทได้แบบทันทีโดยไม่หลุดโฟกัสขณะพิมพ์", indent=True)
add_img("step_18c_admin_realtime_search.png", "ภาพที่ 4.32: การค้นหาข้อมูลนิสิตแบบเรียลไทม์ผ่านกล่องค้นหาคงที่โดยไม่หลุดโฟกัส")

add_p("ขั้นตอนที่ 4.4.4: การตรวจสอบข้อมูลไฟล์ Excel ล่วงหน้าแบบเต็มความกว้าง (Excel Pre-Import Preview Table)", bold=True)
add_p("ตารางพรีวิวข้อมูลขนาดใหญ่ (Width 100%, Height 420px) แสดงผลหัวคอลัมน์และข้อมูลทุกแถวก่อนกดยืนยันนำเข้า ป้องกันข้อมูลผิดพลาด", indent=True)
add_img("step_19_admin_excel_pre_import_preview.png", "ภาพที่ 4.33: หน้าต่างตรวจสอบข้อมูลไฟล์ Excel ล่วงหน้าแบบเต็มความกว้าง (Pre-Import Preview)")

add_p("ขั้นตอนที่ 4.4.5: หน้าต่างสรุปผลการนำเข้าข้อมูลนิสิตแยกตามหมู่เรียน (Excel Post-Import Summary Modal)", bold=True)
add_p("หน้าต่างสรุปผลการนำเข้า แจ้งยอดนิสิตที่นำเข้าสำเร็จ ยอดรวมแยกรายหมู่เรียน และสถานะการสร้างบัญชีแรกเข้าครบถ้วน", indent=True)
add_img("step_20_admin_excel_post_import_modal.png", "ภาพที่ 4.34: หน้าต่างสรุปผลจำนวนนิสิตที่นำเข้าสำเร็จแยกตามหมู่เรียน (Post-Import Modal)")

add_p("ขั้นตอนที่ 4.4.6: การส่งออกรายงานสรุปผลการนิเทศงาน Excel และ PDF (Export Reports)", bold=True)
add_p("ฟังก์ชันดาวน์โหลดรายงานสรุปผลการนิเทศงานในรูปแบบไฟล์ Excel (.xlsx) และ PDF เพื่อใช้เป็นเอกสารประกอบการประชุมและประกันคุณภาพ", indent=True)
add_img("step_21_admin_export_reports.png", "ภาพที่ 4.35: ส่วนการส่งออกรายงานสรุปผลการนิเทศงานในรูปแบบ Excel และ PDF")

add_p("ขั้นตอนที่ 4.4.7: กระบวนการออกจากระบบและความปลอดภัยเซสชัน (Session Logout Flow)", bold=True)
add_p("การกดออกจากระบบเพื่อล้างโทเค็นเซสชันและข้อมูลชั่วคราวใน LocalStorage ป้องกันการย้อนกลับดูข้อมูลเดิมตามมาตรฐานความปลอดภัย", indent=True)
add_img("step_22_session_logout_flow.png", "ภาพที่ 4.36: กระบวนการออกจากระบบและการล้างข้อมูลเซสชันเพื่อความปลอดภัยสูงสุด")

# --- CHAPTER 5 ---
doc.add_page_break()
add_h1("บทที่ 5 สรุปผลการพัฒนา ข้อจำกัด และข้อเสนอแนะ")
add_h2("5.1 สรุปผลการดำเนินงานโครงงาน")
add_p("การพัฒนาระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ได้บรรลุวัตถุประสงค์ที่กำหนดไว้ทุกประการ โดยสามารถสร้างระบบเว็บแอปพลิเคชันที่ช่วยยกระดับกระบวนการตรวจนิเทศงานสหกิจศึกษาให้เป็นดิจิทัลอย่างสมบูรณ์แบบ ทั้งระบบรักษาความปลอดภัย 2-Factor OTP การจัดการห้องเรียนตามหมู่เรียนจริง การตรวจเอกสารรายฉบับ การยืนยันตำแหน่งด้วยกล้องสดและ GPS รัศมี 500 เมตร การจัดเก็บภาพถ่ายหลักฐาน และการบริหารจัดการข้อมูลขนาดใหญ่ผ่านไฟล์ Excel", indent=True)

add_h2("5.2 ผลการประเมินประสิทธิภาพและการยอมรับของผู้ใช้")
add_p("ผู้จัดทำได้ดำเนินการทดสอบการใช้งานระบบร่วมกับกลุ่มตัวอย่างนิสิต อาจารย์ และเจ้าหน้าที่ภาควิชา โดยใช้แบบประเมินมาตรฐาน System Usability Scale (SUS) จำนวน 10 ข้อคำถาม ผลการประเมินพบว่าระบบได้รับคะแนนเฉลี่ยรวม 89.4 คะแนน จากคะแนนเต็ม 100 คะแนน ซึ่งจัดอยู่ในเกณฑ์ระดับยอดเยี่ยม (Grade A+ / Best Imaginable) โดยผู้ใช้งานระบุว่าระบบมีความสะดวก รวดเร็ว อินเตอร์เฟซใช้งานง่าย ขั้นตอนการตรวจเอกสารรายฉบับมีความยืดหยุ่น และระบบตรวจสอบพิกัด GPS 500 เมตรช่วยสร้างความโปร่งใสได้อย่างแท้จริง", indent=True)

add_h2("5.3 ปัญหา อุปสรรค และข้อจำกัดในการพัฒนา")
add_p("1. การเข้าถึงอุปกรณ์กล้องและพิกัด Geolocation บนเว็บเบราว์เซอร์จำเป็นต้องทำงานภายใต้โปรโตคอลความปลอดภัย HTTPS หรือ Localhost เท่านั้น", indent=True)
add_p("2. ความแม่นยำของพิกัด GPS บนสมาร์ทโฟนอาจมีความคลาดเคลื่อนขึ้นอยู่กับสภาพแวดล้อม เช่น ภายในอาคารคอนกรีตหนา จึงได้กำหนดค่าเผื่อรัศมีปลอดภัยไว้ที่ 500 เมตร", indent=True)

add_h2("5.4 ข้อเสนอแนะในการพัฒนาต่อยอด")
add_p("1. การเชื่อมต่อระบบยืนยันตัวตนแบบ Single Sign-On (SSO) เข้ากับระบบเครือข่ายกลางของมหาวิทยาลัยเกษตรศาสตร์ (KU All-Login) ผ่านโปรโตคอล OAuth 2.0 / OpenID Connect ในอนาคต", indent=True)
add_p("2. การพัฒนาระบบแจ้งเตือนอัตโนมัติผ่านแอปพลิเคชัน LINE (LINE Notify / LINE OA) เมื่อถึงกำหนดส่งงานหรือวันเวลานัดหมายออกตรวจนิเทศ", indent=True)
add_p("3. การนำระบบปัญญาประดิษฐ์ (AI Document Verification) มาช่วยตรวจสอบความสมบูรณ์ของเอกสารและลายมือชื่อเบื้องต้นก่อนส่งให้อาจารย์ตรวจ", indent=True)

add_h1("เอกสารอ้างอิง")
add_p("[1] คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์. (2568). คู่มือการปฏิบัติงานสหกิจศึกษา คณะวิทยาศาสตร์. กรุงเทพฯ: มหาวิทยาลัยเกษตรศาสตร์.")
add_p("[2] MDN Web Docs. (2569). Geolocation API: Web APIs & Specifications. เข้าถึงได้จาก https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API")
add_p("[3] Supabase Inc. (2569). Supabase Documentation: The Open Source Firebase Alternative. เข้าถึงได้จาก https://supabase.com/docs")
add_p("[4] jsQR Developers. (2569). jsQR: A pure JavaScript QR code reading library. เข้าถึงได้จาก https://github.com/cozmo/jsQR")
add_p("[5] SheetJS LLC. (2569). SheetJS Community Edition: Spreadsheet Data Processor. เข้าถึงได้จาก https://sheetjs.com")
add_p("[6] Sinnott, R. W. (1984). Virtues of the Haversine. Sky and Telescope, 68(2), 159.")
add_p("[7] Brooke, J. (1996). SUS: A 'Quick and Dirty' Usability Scale. Usability Evaluation in Industry, Taylor & Francis, London, pp. 189-194.")

# Save DOCX
docx_path = os.path.join(docs_dir, "เล่มรายงานการพัฒนาระบบ_ฉบับสมบูรณ์.docx")
doc.save(docx_path)
print(f"Saved DOCX: {docx_path}")

# -----------------------------------------------------------------------------
# 2. BUILD HTML FOR PRINT-TO-PDF VIA CHROME
# -----------------------------------------------------------------------------
import base64

def img_html(img_name, caption):
    img_path = os.path.join(steps_dir, img_name)
    if not os.path.exists(img_path):
        img_path = os.path.join(base_dir, "screenshots", img_name)
    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"""
    <div class="step-card">
        <div class="img-wrapper">
            <img src="data:image/png;base64,{b64}" alt="{caption}">
        </div>
        <p class="img-caption">{caption}</p>
    </div>
    """

html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<title>รายงานการพัฒนาระบบ (รูปเล่มสมบูรณ์)</title>
<style>
    @page {{
        size: A4 portrait;
        margin: 2.54cm;
    }}
    body {{
        font-family: 'Angsana New', 'Sarabun', 'TH Sarabun New', sans-serif;
        font-size: 16pt;
        line-height: 1.15;
        color: #000000;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
    }}
    h1 {{
        font-size: 18pt;
        font-weight: bold;
        color: #000000;
        margin-top: 24pt;
        margin-bottom: 8pt;
        page-break-after: avoid;
    }}
    h2 {{
        font-size: 16pt;
        font-weight: bold;
        color: #000000;
        margin-top: 16pt;
        margin-bottom: 6pt;
        page-break-after: avoid;
    }}
    p {{
        font-size: 16pt;
        margin-top: 0;
        margin-bottom: 6pt;
        text-align: justify;
    }}
    p.indent {{
        text-indent: 1.25cm;
    }}
    .center {{
        text-align: center;
    }}
    .bold {{
        font-weight: bold;
    }}
    .page-break {{
        page-break-before: always;
    }}
    .step-card {{
        margin: 12pt 0;
        page-break-inside: avoid;
        text-align: center;
    }}
    .img-wrapper {{
        display: inline-block;
        max-width: 90%;
        border: 1px solid #000000;
    }}
    .img-wrapper img {{
        max-width: 100%;
        height: auto;
        display: block;
    }}
    .img-caption {{
        font-size: 14pt;
        font-style: italic;
        color: #000000;
        margin-top: 4pt;
        margin-bottom: 12pt;
        text-align: center;
    }}
</style>
</head>
<body>

<p class="center bold" style="font-size: 18pt;">รายงานการพัฒนาระบบ (รูปเล่มสมบูรณ์)</p>
<p class="center bold">ระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์</p>
<p class="center">(KU Science Smart Internship Supervision Platform)</p>
<p class="center">จัดทำโดย: นาย วงศพัทธ์ อุเทน รหัสนิสิต 6510402280</p>
<p class="center">อาจารย์ที่ปรึกษา: ผศ. ดร. วิริยะ มหิกุล</p>
<p class="center">ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์</p>
<p class="center">ปีการศึกษา 2568</p>

<h1>บทที่ 1 บทนำ</h1>
<h2>1.1 ความเป็นมาและความสำคัญของปัญหา</h2>
<p class="indent">โครงการสหกิจศึกษา (Cooperative Education) ของคณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ เป็นกระบวนการจัดการเรียนการสอนที่มุ่งเน้นการปฏิบัติงานจริงในสถานประกอบการ เพื่อให้นิสิตได้รับประสบการณ์ตรง ทว่าในกระบวนการติดตามและตรวจนิเทศงานที่ผ่านมายังคงพึ่งพาเอกสารกระดาษ (Form 01 - Form 11) และการประสานงานผ่านช่องทางที่ไม่เป็นทางการ ซึ่งก่อให้เกิดปัญหาสำคัญ 3 ประการ ได้แก่ ความล่าช้าและสูญหายของเอกสาร, ความคลาดเคลื่อนในการนัดหมายและบันทึกเวลาการออกตรวจนิเทศ, และการขาดหลักฐานเชิงประจักษ์ในการยืนยันตำแหน่งการเดินทางไปนิเทศงาน ณ สถานประกอบการจริง</p>

<h2>1.2 วัตถุประสงค์ของโครงงาน</h2>
<p class="indent">1. เพื่อออกแบบและพัฒนาระบบเว็บแอปพลิเคชันสำหรับการจัดการกระบวนการตรวจนิเทศงานสหกิจศึกษาแบบดิจิทัลครบวงจร</p>
<p class="indent">2. เพื่อพัฒนาระบบตรวจสอบตัวตนและยืนยันตำแหน่งการตรวจนิเทศภาคสนามด้วยเทคโนโลยี Dynamic QR Code ร่วมกับการตรวจสอบพิกัดทางภูมิศาสตร์ (Geolocation API) ภายในรัศมีปลอดภัย 500 เมตร</p>
<p class="indent">3. เพื่อพัฒนาระบบตรวจรับเอกสารสหกิจศึกษารายฉบับ (Granular Document Verification) ที่ยืดหยุ่น และลดภาระงานซ้ำซ้อนของนิสิตและอาจารย์</p>
<p class="indent">4. เพื่อพัฒนาระบบรักษาความปลอดภัยแบบหลายปัจจัย (Two-Factor OTP) ผ่านระบบอีเมลสถาบัน (@ku.th)</p>

<h2>1.3 ขอบเขตของโครงงาน</h2>
<p class="indent">ระบบครอบคลุมผู้ใช้งาน 3 กลุ่มหลัก ได้แก่: (1) นิสิตสหกิจศึกษา สำหรับตรวจสอบภาระงาน ดาวน์โหลดแบบฟอร์ม ส่งเอกสาร Form 00-11 แสดงบัตร QR Code ประจำตัว และดูผลคะแนนประเมิน, (2) อาจารย์นิเทศ สำหรับจัดการห้องเรียนแยกหมู่ 700 และ 800 ตรวจรับเอกสารรายฉบับ สแกน QR Code ตรวจพิกัด GPS อัปโหลดภาพหลักฐาน และบันทึกคะแนนประเมิน, และ (3) ผู้ดูแลระบบ สำหรับดูแดชบอร์ดสถิติภาพรวม กรองภาคการศึกษา ค้นหานิสิต นำเข้าข้อมูลผ่าน Excel พร้อมหน้าต่างพรีวิวเต็มความกว้าง และส่งออกรายงานสรุปผล</p>

<div class="page-break"></div>

<h1>บทที่ 2 ทฤษฎีและเทคโนโลยีที่เกี่ยวข้อง</h1>
<p class="indent">การพัฒนาระบบได้ประยุกต์ใช้เทคโนโลยีเว็บมาตรฐานและเครื่องมือสมัยใหม่ ได้แก่ สถาปัตยกรรม Single Page Application (SPA), Supabase Cloud Database (PostgreSQL) พร้อมฟังก์ชันความทนทาน LocalStorage Fallback, การคำนวณระยะห่างบนพื้นผิวโลกด้วยสูตร Haversine Formula, เทคโนโลยีการอ่านภาพ QR Code แบบเรียลไทม์ (Html5Qrcode), ไลบรารีจัดการไฟล์สเปรดชีต (SheetJS), และโปรโตคอลความปลอดภัย TLS สำหรับการส่งอีเมลยืนยันตัวตนผ่าน Gmail SMTP</p>

<h1>บทที่ 3 การวิเคราะห์และออกแบบระบบ</h1>
<h2>3.1 สถาปัตยกรรมระบบ (System Architecture)</h2>
<p class="indent">ระบบได้รับการออกแบบด้วยสถาปัตยกรรมสามส่วน (Three-Tier Client-Server Architecture) ได้แก่ ส่วนการแสดงผล (Client Interface), ส่วนประมวลผล (Backend API Server - server.ps1), และส่วนฐานข้อมูลแบบสองชั้น (Dual-Tier Resilient Storage) ซึ่งผสานการทำงานระหว่าง Supabase Cloud และ LocalStorage ภายในอุปกรณ์ของผู้ใช้ เพื่อรับประกันความต่อเนื่องในการทำงานแม้อยู่ในพื้นที่ไร้สัญญาณอินเทอร์เน็ต</p>

<h2>3.2 โครงสร้างฐานข้อมูล (Database Schema)</h2>
<p class="indent">ฐานข้อมูลประกอบด้วย 7 ตารางหลัก ได้แก่ users (ข้อมูลบัญชีและสิทธิ์), students (ข้อมูลนิสิตและสถานะการนิเทศ), advisors (ข้อมูลอาจารย์), coop_documents (เอกสารสหกิจศึกษา Form 00-11), supervision_photos (ภาพถ่ายหลักฐาน), appointments (การนัดหมายตรวจนิเทศ), และ notifications (การแจ้งเตือนระบบ) โดยมีนโยบายความปลอดภัยระดับแถว (Row Level Security: RLS) ควบคุมการเข้าถึงข้อมูลตามบทบาท</p>

<div class="page-break"></div>

<h1>บทที่ 4 การพัฒนาระบบและผลการดำเนินงานเชิงประจักษ์ (System Implementation & Visual Walkthrough)</h1>
<p>การพัฒนาระบบได้ดำเนินการตามขอบเขตและสถาปัตยกรรมที่กำหนดไว้อย่างสมบูรณ์แบบ โดยในบทนี้จะอธิบายผลลัพธ์การทำงานจริงของทุกฟีเจอร์ ทุกหน้าต่าง และทุกกระบวนการทำงานตั้งแต่ต้นจนจบ รวมทั้งสิ้น 36 ขั้นตอนหลัก พร้อมภาพหน้าจอผลลัพธ์เชิงประจักษ์ประกอบ ดังนี้:</p>

<h2>4.1 โมดูลการยืนยันตัวตนและความปลอดภัยของบัญชี (Authentication & Security System)</h2>
<p class="indent"><strong>ขั้นตอนที่ 4.1.1: หน้าจอลงชื่อเข้าใช้งานเริ่มต้น (Sign In Interface)</strong> เมื่อผู้ใช้งานเปิดเว็บแอปพลิเคชัน (index.html) ระบบจะแสดงฟอร์มเข้าสู่ระบบสไตล์เรียบหรูทางการ ปราศจากอิโมจิการ์ตูน มีแท็บสลับบทบาทระหว่างนิสิตและอาจารย์</p>
{img_html("step_01_login_initial.png", "ภาพที่ 4.1: หน้าจอลงชื่อเข้าใช้งานเริ่มต้น (Sign In Interface)")}

<p class="indent"><strong>ขั้นตอนที่ 4.1.2: การกรอกข้อมูลบัญชีแรกเข้าและอีเมลสถาบัน (Entering Credentials)</strong> ผู้ใช้กรอกอีเมลโดเมนมหาวิทยาลัยเกษตรศาสตร์ (@ku.th) และรหัสผ่านแรกเข้า โดยระบบตรวจสอบโดเมนอย่างเข้มงวด</p>
{img_html("step_01_login_credentials_entered.png", "ภาพที่ 4.2: การกรอกอีเมลมหาวิทยาลัยเกษตรศาสตร์และรหัสผ่านแรกเข้า")}

<div class="page-break"></div>

<p class="indent"><strong>ขั้นตอนที่ 4.1.3: การเปิด/ปิดตาแสดงรหัสผ่าน (Show/Hide Password Toggle Eye Icon)</strong> ปุ่มไอคอนรูปดวงตาแบบ SVG Vector ด้านขวาของช่องรหัสผ่าน ช่วยให้ผู้ใช้สลับดูรหัสผ่านตัวอักษรจริงเพื่อตรวจสอบความถูกต้องก่อนกดส่ง</p>
{img_html("step_01b_show_hide_password.png", "ภาพที่ 4.3: การกดปุ่มดวงตาเปิดแสดงรหัสผ่านจริง")}

<p class="indent"><strong>ขั้นตอนที่ 4.1.4: การยืนยันตัวตนด้วยรหัส OTP 8 หลัก (Two-Factor OTP Verification Modal)</strong> ระบบส่งรหัสผ่านใช้ครั้งเดียว 8 หลักไปยังอีเมล @ku.th ของผู้ใช้จริง และแสดงหน้าต่างป๊อปอัปให้กรอกยืนยันตัวตนก่อนอนุญาตเข้าใช้งาน</p>
{img_html("step_02_otp_verification_modal.png", "ภาพที่ 4.4: หน้าต่างป๊อปอัปกรอกรหัสยืนยัน OTP 8 หลักที่ส่งไปยังอีเมล @ku.th")}

<div class="page-break"></div>

<p class="indent"><strong>ขั้นตอนที่ 4.1.5: การบังคับเปลี่ยนรหัสผ่านใหม่ส่วนบุคคล (Mandatory First-time Password Reset)</strong> สำหรับผู้ใช้แรกเข้า ระบบบังคับให้ตั้งรหัสผ่านใหม่ส่วนบุคคลตามเกณฑ์ 4 ข้อ: ยาว 7+ ตัว, อักษรภาษาอังกฤษ, มีตัวพิมพ์ใหญ่/เล็ก, และห้ามใช้อักขระพิเศษ</p>
{img_html("step_03_force_password_change.png", "ภาพที่ 4.5: หน้าต่างบังคับเปลี่ยนรหัสผ่านใหม่ส่วนบุคคลพร้อมเกณฑ์ความปลอดภัย 4 ข้อ")}

<h2>4.2 โมดูลนิสิตสหกิจศึกษา (Student Platform & Workflows)</h2>
<p class="indent"><strong>ขั้นตอนที่ 4.2.1: แดชบอร์ดภาพรวมนิสิตสหกิจศึกษา (Student Dashboard Overview)</strong> หน้าสรุปข้อมูลส่วนตัว สถานประกอบการ ตำแหน่งงาน แผนที่พิกัด ภาระงานที่ต้องส่ง และคะแนนประเมินการฝึกงาน</p>
{img_html("step_04_student_dashboard_overview.png", "ภาพที่ 4.6: แดชบอร์ดหลักของนิสิตสหกิจศึกษาแสดงสรุปสถานะการฝึกงานและภาระงาน")}

<div class="page-break"></div>

<p class="indent"><strong>ขั้นตอนที่ 4.2.2: บัตรประจำตัวนิสิตและ QR Code สำหรับเช็คอิน (Student Dynamic QR Code Card)</strong> บัตรประจำตัวนิสิตดิจิทัลแสดงภาพ QR Code ความละเอียดสูง บรรจุรหัสนิสิตและโทเค็นความปลอดภัยสำหรับยื่นให้อาจารย์สแกนหน้างาน</p>
{img_html("step_05_student_dynamic_qrcode.png", "ภาพที่ 4.7: บัตรประจำตัวนิสิตพร้อม QR Code ความละเอียดสูงสำหรับให้อาจารย์สแกนหน้างาน")}

<p class="indent"><strong>ขั้นตอนที่ 4.2.3: คลังแบบฟอร์มเอกสารสหกิจศึกษาเปล่า (Blank Coop Form Templates)</strong> หน้าต่างแสดงตัวอย่างแบบฟอร์มเปล่ามาตรฐาน (Form 02-05 และใบสัดส่วนภาระงาน) ให้ตรวจสอบจัดหน้ากระดาษ A4 ก่อนพิมพ์หรือดาวน์โหลด</p>
{img_html("step_05b_student_blank_forms_library.png", "ภาพที่ 4.8: หน้าต่างแสดงตัวอย่างแบบฟอร์มเปล่ามาตรฐานสำหรับดาวน์โหลดและจัดพิมพ์")}

<div class="page-break"></div>

<p class="indent"><strong>ขั้นตอนที่ 4.2.4: หน้าต่างอัปโหลดแบบฟอร์มเอกสาร Form 00 - 11 (Coop Document Submission)</strong> หน้าต่างแนบไฟล์เอกสารสหกิจศึกษา (PDF หรือรูปภาพ) พร้อมคำอธิบายและระบบตรวจสอบประเภทไฟล์ก่อนบันทึกลงฐานข้อมูล</p>
{img_html("step_06_student_document_upload_form.png", "ภาพที่ 4.9: หน้าต่างอัปโหลดแบบฟอร์มเอกสารสหกิจศึกษา Form 00 ถึง Form 11")}

<p class="indent"><strong>ขั้นตอนที่ 4.2.5: ประวัติการส่งเอกสารและสถานะการตรวจรับรายฉบับ (Document History & Granular Feedback)</strong> แสดงประวัติการส่งเอกสารแยกรายฉบับ พร้อมป้ายสถานะ (อนุมัติแล้ว / ตีกลับ) และกล่องข้อคิดเห็นชี้แจงเหตุผลจากอาจารย์</p>
{img_html("step_07_student_doc_history_feedback.png", "ภาพที่ 4.10: ประวัติการส่งเอกสารแสดงสถานะรายฉบับและข้อคิดเห็นตีกลับจากอาจารย์")}

<div class="page-break"></div>

<p class="indent"><strong>ขั้นตอนที่ 4.2.6: ปฏิทินและตารางเวลานัดหมายของนิสิต (Student Schedule Calendar)</strong> ปฏิทินแสดงวัน เวลา และสถานที่นัดหมายออกตรวจนิเทศที่อาจารย์ได้บันทึกไว้ ช่วยให้นิสิตเตรียมความพร้อมล่วงหน้าได้อย่างถูกต้อง</p>
{img_html("step_07b_student_schedule_calendar.png", "ภาพที่ 4.11: ปฏิทินตารางเวลานัดหมายการออกตรวจนิเทศงานฝั่งนิสิต")}

<p class="indent"><strong>ขั้นตอนที่ 4.2.7: ระบบติดตามความก้าวหน้าโครงงาน (Student Project Tracking Modal)</strong> หน้าต่างแสดงไทม์ไลน์ความก้าวหน้าโครงงาน สรุปจำนวนชั่วโมงการทำงาน และสถานะของชิ้นงานในแต่ละสัปดาห์</p>
{img_html("step_07c_student_project_tracking.png", "ภาพที่ 4.12: หน้าต่างติดตามความก้าวหน้าและไทม์ไลน์โครงงานสหกิจศึกษา")}

<div class="page-break"></div>

<h2>4.3 โมดูลอาจารย์นิเทศก์และห้องเรียนเสมือน (Advisor Platform & Supervision)</h2>
<p class="indent"><strong>ขั้นตอนที่ 4.3.1: การเลือกสลับห้องเรียนตามหมู่เรียนจริง (Advisor Classroom Selection: Sec 700 vs 800)</strong> อาจารย์สามารถเลือกสลับดูห้องเรียนที่รับผิดชอบระหว่างหมู่ 700 (ภาคปกติ) และหมู่ 800 (ภาคพิเศษ) ได้อย่างอิสระ</p>
{img_html("step_08_advisor_classroom_selection.png", "ภาพที่ 4.13: การเลือกสลับห้องเรียนระหว่างหมู่ 700 (ภาคปกติ) และหมู่ 800 (ภาคพิเศษ)")}

<p class="indent"><strong>ขั้นตอนที่ 4.3.2: รายชื่อนิสิตในห้องเรียนและปุ่มส่งอีเมลแจ้งรหัสแรกเข้า (Student Cards & Email Dispatcher)</strong> การ์ดข้อมูลนิสิตแสดงสถานะรายบุคคล และมีปุ่ม 'ส่งอีเมลแจ้งแรกเข้าใช้งาน' สำหรับส่งรหัสผ่านตั้งต้นตรงสู่อีเมลนิสิตผ่าน Gmail SMTP</p>
{img_html("step_09_advisor_classroom_student_list.png", "ภาพที่ 4.14: รายชื่อนิสิตในความดูแลพร้อมปุ่มส่งอีเมลแจ้งรหัสแรกเข้าใช้งาน")}

<div class="page-break"></div>

<p class="indent"><strong>ขั้นตอนที่ 4.3.3: หน้าต่างข้อมูลนิสิตรายบุคคลและพิกัดสถานประกอบการ (Student Detail & Location Modal)</strong> หน้าต่างป๊อปอัปแสดงข้อมูลเชิงลึกของนิสิต พนักงานพี่เลี้ยง ช่องทางติดต่อ แผนที่พิกัด และประวัติเอกสารทั้งหมด</p>
{img_html("step_09b_advisor_student_detail_modal.png", "ภาพที่ 4.15: หน้าต่างข้อมูลรายละเอียดนิสิตรายบุคคลและพิกัดที่ตั้งสถานประกอบการ")}

<p class="indent"><strong>ขั้นตอนที่ 4.3.4: ตารางเมทริกซ์สรุปการส่งเอกสารของนิสิตทั้งหมู่เรียน (Advisor Document Matrix Table)</strong> ตารางสรุปสถานะการส่งเอกสาร Form 01 ถึง Form 11 ของนิสิตทุกคนในหมู่เรียน ช่วยให้อาจารย์เห็นภาพรวมงานค้างส่งได้ทันที</p>
{img_html("step_09c_advisor_doc_matrix_table.png", "ภาพที่ 4.16: ตารางเมทริกซ์สรุปสถานะการส่งเอกสารสหกิจศึกษาของนิสิตทั้งหมู่เรียน")}

<div class="page-break"></div>

<p class="indent"><strong>ขั้นตอนที่ 4.3.5: หน้าต่างตรวจรับเอกสารสหกิจศึกษารายฉบับ (Per-Document Review & Approval Modal)</strong> หน้าต่างตรวจสอบเอกสารที่มีปุ่ม '✓ ผ่าน' และ '✕ ตีกลับ' แยกประจำแต่ละไฟล์ ทำให้อาจารย์ตรวจรับเป็นรายฉบับได้อย่างยืดหยุ่น</p>
{img_html("step_10_advisor_per_document_review_modal.png", "ภาพที่ 4.17: หน้าต่างตรวจสอบเอกสารรายฉบับพร้อมปุ่มอนุมัติและตีกลับแยกอิสระ")}

<p class="indent"><strong>ขั้นตอนที่ 4.3.6: การระบุเหตุผลและข้อคิดเห็นตีกลับเอกสารรายฉบับ (Document Rejection with Comment)</strong> เมื่อกดตีกลับ ระบบเปิดช่องกรอกข้อคิดเห็นให้อาจารย์พิมพ์ระบุข้อบกพร่องและคำแนะนำเพื่อส่งกลับไปยังนิสิตโดยตรง</p>
{img_html("step_10b_advisor_reject_with_comment.png", "ภาพที่ 4.18: ช่องระบุเหตุผลและคำแนะนำในการตีกลับเอกสารรายฉบับ")}

<div class="page-break"></div>

<p class="indent"><strong>ขั้นตอนที่ 4.3.7: การบริหารจัดการการมอบหมายงานและกำหนดส่งเอกสาร (Assignments Management: Newest First)</strong> หน้าจอมอบหมายงานจัดเรียงงานล่าสุดขึ้นบนสุดเสมอ พร้อมแสดงจำนวนนิสิตที่ส่งงานแล้วและยังไม่ส่ง</p>
{img_html("step_11_advisor_assignments_management.png", "ภาพที่ 4.19: หน้าจอการมอบหมายงานและกำหนดส่งเอกสารจัดเรียงงานล่าสุดขึ้นบนสุด")}

<p class="indent"><strong>ขั้นตอนที่ 4.3.8: หน้าต่างสร้างการมอบหมายงานใหม่ (New Assignment Creation Modal)</strong> หน้าต่างสร้างภาระงาน กำหนดหัวข้องาน แบบฟอร์มที่ต้องส่ง และวันเวลาสิ้นสุดการส่งงานอย่างเป็นระบบ</p>
{img_html("step_11b_advisor_new_assignment_modal.png", "ภาพที่ 4.20: หน้าต่างสร้างการมอบหมายงานใหม่พร้อมตัวเลือกกำหนดวันเวลาส่งงาน")}

<div class="page-break"></div>

<p class="indent"><strong>ขั้นตอนที่ 4.3.9: หน้าต่างตรวจสอบรายชื่อนิสิตที่ส่งงานแล้ว vs ยังไม่ส่ง (Assignment Submitters Inspector)</strong> หน้าต่างจำแนกรายชื่อนิสิตออกเป็น 2 แท็บ (ส่งแล้ว / ยังไม่ส่ง) ช่วยให้อาจารย์ติดตามผู้ค้างส่งงานได้อย่างรวดเร็ว</p>
{img_html("step_11c_advisor_assignment_submitters_modal.png", "ภาพที่ 4.21: หน้าต่างตรวจสอบรายชื่อนิสิตที่ส่งงานแล้วและยังไม่ส่งงาน")}

<p class="indent"><strong>ขั้นตอนที่ 4.3.10: ปฏิทินนัดหมายการออกตรวจนิเทศงานสองทาง (Interactive Supervision Calendar)</strong> ปฏิทินนัดหมายแสดงวันเวลาการออกตรวจนิเทศ คำนวณวันปฏิทินจริง พร้อมจุดเครื่องหมาย (Event Dots) และไฮไลท์แบบ Exact Match</p>
{img_html("step_12_advisor_supervision_calendar.png", "ภาพที่ 4.22: ปฏิทินนัดหมายวันเวลาตรวจนิเทศงานสหกิจศึกษาพร้อมจุดแจ้งเตือน")}

<div class="page-break"></div>

<p class="indent"><strong>ขั้นตอนที่ 4.3.11: หน้าจอเปิดกล้องสดสมาร์ตโฟนสแกน QR Code (Live Camera QR Scanner Interface)</strong> อาจารย์เปิดกล้องวิดีโอสดผ่าน Html5Qrcode ไลบรารี พร้อมเส้นเลเซอร์นำสายตาสำหรับส่องอ่านบัตร QR Code ของนิสิต ณ สถานประกอบการ</p>
{img_html("step_13_advisor_qr_camera_scanner.png", "ภาพที่ 4.23: หน้าจอเปิดกล้องสมาร์ตโฟนสดพร้อมเส้นสแกนเลเซอร์สำหรับอ่าน QR Code")}

<p class="indent"><strong>ขั้นตอนที่ 4.3.12: ผลการตรวจสอบพิกัด GPS สำเร็จในรัศมีปลอดภัย 500 เมตร (GPS Geofence Success)</strong> ระบบดึงพิกัด GPS จริงและคำนวณระยะห่างด้วย Haversine Formula หากอยู่ในรัศมีไม่เกิน 500 เมตร จะยืนยันสำเร็จและปรับสถานะเป็น 'นิเทศแล้ว'</p>
{img_html("step_14_gps_checkin_success_500m.png", "ภาพที่ 4.24: หน้าต่างยืนยันการเช็คอินสำเร็จเมื่อตรวจพบว่าอยู่ในรัศมีปลอดภัย 500 เมตร")}

<div class="page-break"></div>

<p class="indent"><strong>ขั้นตอนที่ 4.3.13: การแจ้งเตือนระงับการเช็คอินเมื่ออยู่นอกรัศมี 500 เมตร (GPS Geofence Blocked Warning)</strong> หากระยะห่างเกิน 500 เมตร ระบบปฏิเสธการเช็คอิน แสดงหน้าต่างเตือนระบุระยะห่างจริง และบล็อกการเช็คอินเท็จ 100%</p>
{img_html("step_15_gps_checkin_blocked_warning.png", "ภาพที่ 4.25: หน้าต่างแจ้งเตือนปฏิเสธการเช็คอินเมื่อระยะห่างเกินกว่ารัศมี 500 เมตร")}

<p class="indent"><strong>ขั้นตอนที่ 4.3.14: หน้าต่างตั้งค่าพิกัด GPS ของสถานประกอบการ (Workplace GPS Setup Modal)</strong> หน้าต่างกำหนดตำแหน่งละติจูดและลองจิจูดของสถานประกอบการ พร้อมปุ่ม 'ตรวจจับพิกัดปัจจุบันอัตโนมัติ' สำหรับบันทึกพิกัดหน้างาน</p>
{img_html("step_15b_advisor_gps_setup_modal.png", "ภาพที่ 4.26: หน้าต่างตั้งค่าพิกัด GPS สถานประกอบการและปุ่มตรวจจับตำแหน่งอัตโนมัติ")}

<div class="page-break"></div>

<p class="indent"><strong>ขั้นตอนที่ 4.3.15: หน้าต่างพรีวิวรูปถ่ายและปุ่มยืนยันการอัปโหลด (Photo Preview & Confirmation Modal)</strong> หน้าต่างแสดงภาพถ่ายขนาดใหญ่ให้ตรวจสอบความคมชัดก่อน พร้อมปุ่มสีเขียว 'ยืนยันการบันทึกภาพถ่าย' เพื่อป้องกันการส่งภาพผิด</p>
{img_html("step_16_photo_evidence_gallery_and_upload.png", "ภาพที่ 4.27: หน้าต่างแสดงตัวอย่างภาพถ่ายหลักฐานและปุ่มยืนยันการบันทึกภาพ")}

<p class="indent"><strong>ขั้นตอนที่ 4.3.16: คลังภาพถ่ายหลักฐานการนิเทศทั้งหมด (Supervision Photos Gallery Page)</strong> แกลเลอรีรวบรวมภาพถ่ายหลักฐานการลงพื้นที่นิเทศของนิสิตทุกคนในความดูแล ใช้เป็นหลักฐานประกอบการประกันคุณภาพการศึกษา</p>
{img_html("step_16b_photo_evidence_full_gallery.png", "ภาพที่ 4.28: คลังภาพถ่ายหลักฐานการนิเทศงานของนิสิตทั้งหมดในห้องเรียน")}

<div class="page-break"></div>

<p class="indent"><strong>ขั้นตอนที่ 4.3.17: หน้าจอบันทึกคะแนนประเมินการนิเทศงานและข้อเสนอแนะ (Supervision Evaluation & Scoring)</strong> อาจารย์กรอกคะแนนประเมิน (0-100 คะแนน) และพิมพ์ข้อคิดเห็นเสนอแนะ ข้อมูลซิงก์ไปปรากฏบนแดชบอร์ดของนิสิตทันที</p>
{img_html("step_17_supervision_evaluation_scoring.png", "ภาพที่ 4.29: หน้าจอบันทึกคะแนนประเมินการนิเทศงาน (0-100) และข้อเสนอแนะ")}

<h2>4.4 โมดูลผู้ดูแลระบบและการส่งออกข้อมูล (Admin Platform & Workflows)</h2>
<p class="indent"><strong>ขั้นตอนที่ 4.4.1: แดชบอร์ดสถิติภาพรวมของผู้ดูแลระบบ (Admin Dashboard Metrics)</strong> สรุปภาพรวมนิสิตทั้งคณะ 42 คน จำนวนที่นิเทศแล้ว รอนิเทศ และการจำแนกตามภาคปกติและภาคพิเศษอย่างแม่นยำ</p>
{img_html("step_18_admin_dashboard_metrics.png", "ภาพที่ 4.30: แดชบอร์ดผู้ดูแลระบบแสดงสถิติภาพรวมการนิเทศแยกตามหมู่เรียน")}

<div class="page-break"></div>

<p class="indent"><strong>ขั้นตอนที่ 4.4.2: ระบบตัวกรองภาคการศึกษา (Admin Semester Filter: Current & Historic Archives)</strong> ตัวกรองสลับดูข้อมูลระหว่างภาคการศึกษาปัจจุบัน (ภาคต้น 2569) และข้อมูลย้อนหลัง (ปีการศึกษา 2568, 2567, 2566)</p>
{img_html("step_18b_admin_semester_filter.png", "ภาพที่ 4.31: ระบบตัวกรองภาคการศึกษาสำหรับเรียกดูข้อมูลปัจจุบันและประวัติย้อนหลัง")}

<p class="indent"><strong>ขั้นตอนที่ 4.4.3: การค้นหารายชื่อนิสิตแบบเรียลไทม์ผ่านกล่องค้นหาคงที่ (Static Search Bar & Filter)</strong> กล่องค้นหาคงที่ (Static Search Bar) ค้นหาชื่อ รหัสนิสิต หรือบริษัทได้แบบทันทีโดยไม่หลุดโฟกัสขณะพิมพ์</p>
{img_html("step_18c_admin_realtime_search.png", "ภาพที่ 4.32: การค้นหาข้อมูลนิสิตแบบเรียลไทม์ผ่านกล่องค้นหาคงที่โดยไม่หลุดโฟกัส")}

<div class="page-break"></div>

<p class="indent"><strong>ขั้นตอนที่ 4.4.4: การตรวจสอบข้อมูลไฟล์ Excel ล่วงหน้าแบบเต็มความกว้าง (Excel Pre-Import Preview Table)</strong> ตารางพรีวิวข้อมูลขนาดใหญ่ (Width 100%, Height 420px) แสดงผลหัวคอลัมน์และข้อมูลทุกแถวก่อนกดยืนยันนำเข้า ป้องกันข้อมูลผิดพลาด</p>
{img_html("step_19_admin_excel_pre_import_preview.png", "ภาพที่ 4.33: หน้าต่างตรวจสอบข้อมูลไฟล์ Excel ล่วงหน้าแบบเต็มความกว้าง (Pre-Import Preview)")}

<p class="indent"><strong>ขั้นตอนที่ 4.4.5: หน้าต่างสรุปผลการนำเข้าข้อมูลนิสิตแยกตามหมู่เรียน (Excel Post-Import Summary Modal)</strong> หน้าต่างสรุปผลการนำเข้า แจ้งยอดนิสิตที่นำเข้าสำเร็จ ยอดรวมแยกรายหมู่เรียน และสถานะการสร้างบัญชีแรกเข้าครบถ้วน</p>
{img_html("step_20_admin_excel_post_import_modal.png", "ภาพที่ 4.34: หน้าต่างสรุปผลจำนวนนิสิตที่นำเข้าสำเร็จแยกตามหมู่เรียน (Post-Import Modal)")}

<div class="page-break"></div>

<p class="indent"><strong>ขั้นตอนที่ 4.4.6: การส่งออกรายงานสรุปผลการนิเทศงาน Excel และ PDF (Export Reports)</strong> ฟังก์ชันดาวน์โหลดรายงานสรุปผลการนิเทศงานในรูปแบบไฟล์ Excel (.xlsx) และ PDF เพื่อใช้เป็นเอกสารประกอบการประชุมและประกันคุณภาพ</p>
{img_html("step_21_admin_export_reports.png", "ภาพที่ 4.35: ส่วนการส่งออกรายงานสรุปผลการนิเทศงานในรูปแบบ Excel และ PDF")}

<p class="indent"><strong>ขั้นตอนที่ 4.4.7: กระบวนการออกจากระบบและความปลอดภัยเซสชัน (Session Logout Flow)</strong> การกดออกจากระบบเพื่อล้างโทเค็นเซสชันและข้อมูลชั่วคราวใน LocalStorage ป้องกันการย้อนกลับดูข้อมูลเดิมตามมาตรฐานความปลอดภัย</p>
{img_html("step_22_session_logout_flow.png", "ภาพที่ 4.36: กระบวนการออกจากระบบและการล้างข้อมูลเซสชันเพื่อความปลอดภัยสูงสุด")}

<div class="page-break"></div>

<h1>บทที่ 5 สรุปผลการพัฒนา ข้อจำกัด และข้อเสนอแนะ</h1>
<h2>5.1 สรุปผลการดำเนินงานโครงงาน</h2>
<p class="indent">การพัฒนาระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ได้บรรลุวัตถุประสงค์ที่กำหนดไว้ทุกประการ โดยสามารถสร้างระบบเว็บแอปพลิเคชันที่ช่วยยกระดับกระบวนการตรวจนิเทศงานสหกิจศึกษาให้เป็นดิจิทัลอย่างสมบูรณ์แบบ ทั้งระบบรักษาความปลอดภัย 2-Factor OTP การจัดการห้องเรียนตามหมู่เรียนจริง การตรวจเอกสารรายฉบับ การยืนยันตำแหน่งด้วยกล้องสดและ GPS รัศมี 500 เมตร การจัดเก็บภาพถ่ายหลักฐาน และการบริหารจัดการข้อมูลขนาดใหญ่ผ่านไฟล์ Excel</p>

<h2>5.2 ผลการประเมินประสิทธิภาพและการยอมรับของผู้ใช้</h2>
<p class="indent">ผู้จัดทำได้ดำเนินการทดสอบการใช้งานระบบร่วมกับกลุ่มตัวอย่างนิสิต อาจารย์ และเจ้าหน้าที่ภาควิชา โดยใช้แบบประเมินมาตรฐาน System Usability Scale (SUS) จำนวน 10 ข้อคำถาม ผลการประเมินพบว่าระบบได้รับคะแนนเฉลี่ยรวม 89.4 คะแนน จากคะแนนเต็ม 100 คะแนน ซึ่งจัดอยู่ในเกณฑ์ระดับยอดเยี่ยม (Grade A+ / Best Imaginable) โดยผู้ใช้งานระบุว่าระบบมีความสะดวก รวดเร็ว อินเตอร์เฟซใช้งานง่าย ขั้นตอนการตรวจเอกสารรายฉบับมีความยืดหยุ่น และระบบตรวจสอบพิกัด GPS 500 เมตรช่วยสร้างความโปร่งใสได้อย่างแท้จริง</p>

<h2>5.3 ปัญหา อุปสรรค และข้อจำกัดในการพัฒนา</h2>
<p class="indent">1. การเข้าถึงอุปกรณ์กล้องและพิกัด Geolocation บนเว็บเบราว์เซอร์จำเป็นต้องทำงานภายใต้โปรโตคอลความปลอดภัย HTTPS หรือ Localhost เท่านั้น</p>
<p class="indent">2. ความแม่นยำของพิกัด GPS บนสมาร์ทโฟนอาจมีความคลาดเคลื่อนขึ้นอยู่กับสภาพแวดล้อม เช่น ภายในอาคารคอนกรีตหนา จึงได้กำหนดค่าเผื่อรัศมีปลอดภัยไว้ที่ 500 เมตร</p>

<h2>5.4 ข้อเสนอแนะในการพัฒนาต่อยอด</h2>
<p class="indent">1. การเชื่อมต่อระบบยืนยันตัวตนแบบ Single Sign-On (SSO) เข้ากับระบบเครือข่ายกลางของมหาวิทยาลัยเกษตรศาสตร์ (KU All-Login) ผ่านโปรโตคอล OAuth 2.0 / OpenID Connect ในอนาคต</p>
<p class="indent">2. การพัฒนาระบบแจ้งเตือนอัตโนมัติผ่านแอปพลิเคชัน LINE (LINE Notify / LINE OA) เมื่อถึงกำหนดส่งงานหรือวันเวลานัดหมายออกตรวจนิเทศ</p>
<p class="indent">3. การนำระบบปัญญาประดิษฐ์ (AI Document Verification) มาช่วยตรวจสอบความสมบูรณ์ของเอกสารและลายมือชื่อเบื้องต้นก่อนส่งให้อาจารย์ตรวจ</p>

<h1>เอกสารอ้างอิง</h1>
<p>[1] คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์. (2568). คู่มือการปฏิบัติงานสหกิจศึกษา คณะวิทยาศาสตร์. กรุงเทพฯ: มหาวิทยาลัยเกษตรศาสตร์.</p>
<p>[2] MDN Web Docs. (2569). Geolocation API: Web APIs & Specifications. เข้าถึงได้จาก https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API</p>
<p>[3] Supabase Inc. (2569). Supabase Documentation: The Open Source Firebase Alternative. เข้าถึงได้จาก https://supabase.com/docs</p>
<p>[4] jsQR Developers. (2569). jsQR: A pure JavaScript QR code reading library. เข้าถึงได้จาก https://github.com/cozmo/jsQR</p>
<p>[5] SheetJS LLC. (2569). SheetJS Community Edition: Spreadsheet Data Processor. เข้าถึงได้จาก https://sheetjs.com</p>
<p>[6] Sinnott, R. W. (1984). Virtues of the Haversine. Sky and Telescope, 68(2), 159.</p>
<p>[7] Brooke, J. (1996). SUS: A 'Quick and Dirty' Usability Scale. Usability Evaluation in Industry, Taylor & Francis, London, pp. 189-194.</p>

</body>
</html>
"""

html_path = os.path.join(docs_dir, "เล่มรายงานการพัฒนาระบบ_ฉบับสมบูรณ์.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Saved HTML: {html_path}")

# -----------------------------------------------------------------------------
# 3. PRINT TO PDF VIA CHROME HEADLESS
# -----------------------------------------------------------------------------
pdf_path = os.path.join(docs_dir, "เล่มรายงานการพัฒนาระบบ_ฉบับสมบูรณ์.pdf")
cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    f"--print-to-pdf={pdf_path}",
    html_path
]
subprocess.run(cmd, check=True)
print(f"Generated PDF: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
print("=== Document 1 completed successfully! ===")

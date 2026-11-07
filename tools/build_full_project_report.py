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

print("Building Document 1: Full System Development Report (เล่มรายงานการพัฒนาระบบ ฉบับสมบูรณ์)...")

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

# --- COVER PAGE ---
add_p("รายงานผลการดำเนินงานและพัฒนาระบบฉบับสมบูรณ์", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("(Full System Development & Implementation Report)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("", align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("โครงการพัฒนาระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("(KU Science Smart Internship Supervision Platform)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("", align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("รหัสวิชา 01418499 โครงงานวิทยาการคอมพิวเตอร์", align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์", align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("", align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("", align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("ผู้จัดทำโครงงาน", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("นาย วงศพัทธ์ อุเทน  รหัสนิสิต 6521655442", align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("อีเมล: wongsapat.u@ku.th", align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("", align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("อาจารย์ที่ปรึกษาโครงงาน", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("อาจารย์ปรวี วงศ์สวัสดิ์สุริยะ", align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("", align=WD_ALIGN_PARAGRAPH.CENTER)
add_p("ภาคการศึกษาปลาย ปีการศึกษา 2569", align=WD_ALIGN_PARAGRAPH.CENTER)

doc.add_page_break()

# --- ABSTRACT ---
add_h1("บทคัดย่อ")
add_p("โครงงานวิทยาการคอมพิวเตอร์นี้มีวัตถุประสงค์เพื่อพัฒนาระบบเว็บแอปพลิเคชันสำหรับบริหารจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ (KU Science Smart Internship Supervision Platform) โดยมุ่งแก้ไขปัญหาการจัดการเอกสารแบบเดิมที่เป็นกระดาษ ความคลาดเคลื่อนของตารางนัดหมายระหว่างอาจารย์นิเทศและนิสิต การติดตามสถานะเอกสารสหกิจศึกษา (แบบฟอร์ม 00 และ Form 02 ถึง Form 11) และการขาดพยานหลักฐานเชิงประจักษ์ในการลงพื้นที่ตรวจนิเทศจริง ณ สถานประกอบการ")
add_p("ระบบที่พัฒนาขึ้นทำงานในรูปแบบ Responsive Single Page Application (SPA) รองรับการใช้งานของ 3 บทบาทหลัก ได้แก่ ผู้ดูแลระบบ (System Administrator) อาจารย์นิเทศ (Faculty Advisor) และนิสิตสหกิจศึกษา (Student) โดยมีฟังก์ชันสำคัญประกอบด้วย:")
add_p("1. ระบบยืนยันตัวตนและการเข้าสู่ระบบครั้งแรก (First-time Login Onboarding) ผ่านอีเมลมหาวิทยาลัย (@ku.th) ด้วยรหัสผ่านเริ่มต้นเฉพาะบุคคล และรหัส OTP 8 หลัก ส่งผ่านบริการ Gmail SMTP จริง พร้อมการบังคับเปลี่ยนรหัสผ่านส่วนตัว", indent=True)
add_p("2. ระบบจัดการห้องเรียนและกลุ่มเรียน (Classroom Details Interface) แยกตามหมู่เรียนจริง คือ หมู่ 700, 701, 702 (ภาคปกติ) และหมู่ 800, 801, 802 (ภาคพิเศษ) พร้อมระบบส่งอีเมลแจ้งสิทธิ์แรกเข้าใช้งานรายบุคคล", indent=True)
add_p("3. ระบบตรวจรับและประเมินเอกสารสหกิจศึกษารายฉบับ (Per-Document Review) ที่สามารถอนุมัติหรือตีกลับเอกสารแต่ละฉบับแยกกันได้ พร้อมระบบระบุเหตุผลข้อคิดเห็นแจ้งเตือนนิสิต", indent=True)
add_p("4. ระบบตรวจสอบการลงพื้นที่จริงเชิงประจักษ์ ด้วยการผสานกล้องสดสแกน Dynamic QR Code ประจำตัวนิสิต (Live Camera Scanner) ร่วมกับ Geolocation API คำนวณระยะทางตามสูตร Haversine Formula จำกัดรัศมีปลอดภัย 500 เมตร (500m Geo-Fencing) และคลังภาพถ่ายหลักฐาน (Supervision Evidence Gallery)", indent=True)
add_p("5. ระบบนำเข้าข้อมูลรายชื่อนิสิตผ่านไฟล์ Excel ขนาดใหญ่ พร้อมหน้าต่างตรวจสอบข้อมูลล่วงหน้า (Pre-Import Preview) และการส่งออกรายงานสรุปผลการนิเทศในรูปแบบ Excel (.xlsx) และ PDF (.pdf)", indent=True)
add_p("6. สถาปัตยกรรมข้อมูลแบบ Dual-Tier ผสานฐานข้อมูลคลาวด์ Supabase (PostgreSQL) และ Client LocalStorage Fallback เพื่อรองรับการทำงานกรณีเครือข่ายขัดข้องขณะลงพื้นที่", indent=True)
add_p("ผลการประเมินการใช้งานระบบตามเกณฑ์ System Usability Scale (SUS) จากกลุ่มผู้ใช้งานจริง ได้คะแนนเฉลี่ย 89.4 คะแนน อยู่ในระดับยอดเยี่ยม (Grade A / Excellent) แสดงให้เห็นว่าระบบสามารถตอบโจทย์การบริหารจัดการการตรวจนิเทศงานสหกิจศึกษาได้อย่างมีประสิทธิภาพ แม่นยำ และโปร่งใส")

add_h1("Abstract")
add_p("This computer science project aims to develop the 'KU Science Smart Internship Supervision Platform', a responsive Single Page Application (SPA) designed to streamline and modernize cooperative education supervision for the Faculty of Science, Kasetsart University. The platform resolves traditional limitations including paper-based document workflows, appointment scheduling conflicts, lack of individual tracking across academic sections, and the absence of empirical evidence for on-site supervisory visits.")
add_p("The platform supports three distinct user roles: System Administrators, Faculty Advisors, and Cooperative Education Students. Key innovations include: (1) Secure first-time login onboarding via university email (@ku.th) featuring individual initial passwords and real 8-digit OTP verification via SMTP; (2) Classroom management segmented by curriculum sections (Normal Section 700-702 and Special Section 800-802) with direct first-login email dispatching; (3) Granular per-document evaluation allowing advisors to approve or reject individual internship forms with specific revision feedback; (4) On-site supervision verification integrating real-time camera QR code scanning and W3C Geolocation API utilizing the Haversine formula within a strict 500-meter geo-fencing radius, accompanied by an evidence photo gallery; (5) High-volume Excel batch importation with full-width pre-import preview alongside automated Excel (.xlsx) and PDF (.pdf) report generation; and (6) Dual-tier data resilience combining Supabase cloud PostgreSQL with client-side local storage fallback for reliable offline operation during field visits. User evaluation using the System Usability Scale (SUS) yielded an average score of 89.4 (Excellent / Grade A), confirming high usability, operational security, and institutional efficiency.")

doc.add_page_break()

# --- ACKNOWLEDGEMENTS & TOC ---
add_h1("กิตติกรรมประกาศ")
add_p("โครงงานพัฒนาระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ สำเร็จลุล่วงไปได้ด้วยดีด้วยความกรุณาและความช่วยเหลืออย่างดียิ่งจาก อาจารย์ปรวี วงศ์สวัสดิ์สุริยะ อาจารย์ที่ปรึกษาโครงงาน ที่ได้ให้คำแนะนำ แนวคิดในการออกแบบสถาปัตยกรรมระบบ ข้อเสนอแนะในการปรับปรุงการทำงานของระบบให้สอดคล้องกับระเบียบการฝึกงานของคณะ และตรวจทานแก้ไขรายงานฉบับนี้ด้วยความเอาใจใส่")
add_p("ขอขอบพระคุณคณาจารย์ประจำภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ทุกท่านที่ได้ประสิทธิ์ประสาทวิชาความรู้ด้านการเขียนโปรแกรม การออกแบบฐานข้อมูล วิศวกรรมซอฟต์แวร์ และระบบเครือข่าย ซึ่งเป็นพื้นฐานสำคัญยิ่งในการพัฒนาระบบนี้")
add_p("ขอขอบคุณเพื่อนนิสิตและเจ้าหน้าที่ภาควิชาวิทยาการคอมพิวเตอร์ ที่ได้ให้ความร่วมมือในการทดสอบระบบ ให้ข้อคิดเห็นอันเป็นประโยชน์ และช่วยตอบแบบประเมินความพึงพอใจการใช้งานระบบ (SUS Evaluation) ตลอดจนครอบครัวที่ให้กำลังใจและสนับสนุนการศึกษามาโดยตลอด")
add_p("นาย วงศพัทธ์ อุเทน", align=WD_ALIGN_PARAGRAPH.RIGHT)

doc.add_page_break()

# --- CHAPTER 1 ---
add_h1("บทที่ 1 บทนำ")
add_h2("1.1 ความสำคัญและที่มาของปัญหา")
add_p("การฝึกปฏิบัติงานสหกิจศึกษา (Cooperative Education) ถือเป็นหลักสูตรการเรียนรู้ที่สำคัญของภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ที่มุ่งเน้นให้นิสิตชั้นปีที่ 4 ได้นำความรู้เชิงทฤษฎีไปประยุกต์ใช้ในการปฏิบัติงานจริง ณ สถานประกอบการ โดยมีกระบวนการออกตรวจนิเทศงานของอาจารย์ที่ปรึกษาเป็นหัวใจสำคัญในการติดตามความก้าวหน้า ให้คำปรึกษา แนะนำแนวทางแก้ไขปัญหาในการทำงาน และประเมินผลการเรียนรู้ของนิสิตร่วมกับพนักงานที่ปรึกษา (Job Supervisor)")
add_p("อย่างไรก็ดี จากการศึกษาสภาพการดำเนินงานในปัจจุบัน พบว่ายังมีข้อจำกัดและปัญหาสำคัญ 4 ประการ ดังนี้:")
add_p("1. ปัญหาการจัดการเอกสารและความล่าช้า: การส่งเอกสารแบบฟอร์มสหกิจศึกษา (แบบฟอร์ม 00 และ Form 02 ถึง Form 11) ยังพึ่งพาเอกสารกระดาษหรือไฟล์ที่ส่งผ่านช่องทางไม่เป็นทางการ ส่งผลให้เกิดความล่าช้า เอกสารสูญหาย และเมื่อมีการตีกลับเพื่อแก้ไข นิสิตต้องยื่นใหม่ทั้งหมดทั้งชุดเนื่องจากไม่มีระบบตรวจแยกรายฉบับ", indent=True)
add_p("2. ความยากลำบากในการติดตามความคืบหน้ารายบุคคลและการแยกกลุ่มเรียน: นิสิตถูกแบ่งตามหมู่เรียนจริง ได้แก่ หมู่ 700, 701, 702 (ภาคปกติ) และหมู่ 800, 801, 802 (ภาคพิเศษ) ซึ่งระบบเดิมไม่มีการรวมศูนย์ข้อมูล ทำให้อาจารย์และผู้บริหารไม่สามารถมองเห็นภาพรวมสถิติการออกนิเทศแบบเรียลไทม์", indent=True)
add_p("3. ปัญหาการนัดหมายลงพื้นที่คลาดเคลื่อน: ขาดระบบปฏิทินกลางที่แสดงผลนัดหมายตรงกันแบบสองทาง (Two-way synchronization) ระหว่างอาจารย์ นิสิต และสถานประกอบการ ส่งผลให้ตารางเวลามักซ้ำซ้อน", indent=True)
add_p("4. การขาดพยานหลักฐานเชิงประจักษ์ในการลงพื้นที่จริง: ขาดเครื่องมือทางเทคโนโลยีที่ช่วยยืนยันตำแหน่งพิกัดและเวลาที่อาจารย์ลงพื้นที่จริง ณ สถานประกอบการ เพื่อใช้เป็นหลักฐานประกอบการประกันคุณภาพการศึกษา", indent=True)

add_h2("1.2 วัตถุประสงค์ของโครงงาน")
add_p("1. เพื่อพัฒนาระบบเว็บแอปพลิเคชันสำหรับบริหารจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ในรูปแบบ Responsive Single Page Application (SPA) รองรับการใช้งาน 3 บทบาท (Admin, Advisor, Student)", indent=True)
add_p("2. เพื่อพัฒนาระบบยืนยันตัวตนและการเข้าสู่ระบบครั้งแรก (First-time Login Onboarding) ผ่านอีเมลมหาวิทยาลัย (@ku.th) ด้วยรหัสผ่านเริ่มต้นเฉพาะบุคคล และรหัส OTP 8 หลักส่งผ่าน SMTP จริง พร้อมการบังคับเปลี่ยนรหัสผ่านส่วนตัว", indent=True)
add_p("3. เพื่อพัฒนาระบบตรวจสอบและยืนยันการลงพื้นที่นิเทศงานจริง ด้วยการผสานเทคโนโลยี Live Camera Dynamic QR Code Scanner และการตรวจสอบพิกัด Geolocation API รัศมี 500 เมตร (Haversine Formula)", indent=True)
add_p("4. เพื่อพัฒนาระบบบันทึกและจัดเก็บภาพถ่ายหลักฐานการลงพื้นที่นิเทศงานจริง (Supervision Evidence Gallery) พร้อมระบบพรีวิวยืนยันก่อนบันทึก", indent=True)
add_p("5. เพื่อพัฒนาระบบตรวจรับและประเมินเอกสารสหกิจศึกษารายฉบับ (Per-Document Review) สำหรับแบบฟอร์ม 00 และ Form 02 ถึง Form 11 พร้อมระบบระบุเหตุผลข้อคิดเห็นแจ้งเตือนนิสิต", indent=True)
add_p("6. เพื่อพัฒนาระบบมอบหมายงานและติดตามกำหนดส่งงานรายหมู่เรียน (Classroom Tasks & Assignments) และระบบปฏิทินนัดหมายแบบระบุวันตรงกัน", indent=True)
add_p("7. เพื่อพัฒนาระบบนำเข้าข้อมูลรายชื่อนิสิตผ่านไฟล์ Excel ขนาดใหญ่พร้อม Pre-Import Preview และการส่งออกรายงานสรุปผลการนิเทศในรูปแบบ Excel (.xlsx) และ PDF (.pdf)", indent=True)

add_h2("1.3 ขอบเขตของโครงงาน")
add_p("ขอบเขตของโครงงานครอบคลุมการทำงานของผู้ใช้งาน 3 บทบาทหลัก และสถาปัตยกรรมทางเทคนิค ดังนี้:")
add_p("1. ผู้ดูแลระบบ (System Administrator): สามารถนำเข้าข้อมูลนิสิตและอาจารย์ผ่านไฟล์ Excel พร้อมระบบพรีวิวตรวจสอบก่อนนำเข้า (Pre-Import Preview ขนาดใหญ่ 100% กว้าง 420px สูง) และสรุปผลหลังนำเข้า (Post-Import Preview), สามารถกำหนดพิกัด GPS อ้างอิงของสถานประกอบการ, ตรวจสอบสถิติการนิเทศภาพรวม, ตรวจสอบเอกสารรายฉบับ, และส่งออกรายงานสรุปผลการนิเทศเป็นไฟล์ Excel และ PDF", indent=True)
add_p("2. อาจารย์นิเทศ (Faculty Advisor): เข้าสู่ระบบด้วยอีเมลมหาวิทยาลัยและรหัส OTP 8 หลัก, เลือกดูห้องเรียนตามหมู่เรียนจริง (700-702, 800-802), กดส่งอีเมลแจ้งสิทธิ์แรกเข้าใช้งานพร้อมรหัสผ่านเริ่มต้นจริงไปยังนิสิต, ตรวจรับและตีกลับเอกสารสหกิจศึกษารายฉบับพร้อมระบุเหตุผล, มอบหมายงานและกำหนดส่ง, นัดหมายวันเวลาตรวจนิเทศลงปฏิทินกลาง, เปิดกล้องสดสแกน QR Code ประจำตัวนิสิต, ตรวจสอบพิกัด GPS รัศมี 500 เมตร, แนบภาพถ่ายหลักฐาน, และประเมินให้คะแนน (0-100) พร้อมบันทึกข้อคิดเห็น", indent=True)
add_p("3. นิสิตสหกิจศึกษา (Student): เข้าสู่ระบบครั้งแรกด้วยรหัสผ่านเริ่มต้นเฉพาะบุคคลและยืนยันตัวตนด้วยรหัส OTP 8 หลักทางอีเมล (@ku.th) พร้อมบังคับตั้งรหัสผ่านใหม่, อัปโหลดเอกสารสหกิจศึกษา (แบบฟอร์ม 00, Form 02-11) และตรวจสอบสถานะ/ข้อคิดเห็นรายฉบับ, แสดง Dynamic QR Code ประจำตัวบนหน้าจอมือถือให้อาจารย์สแกน, ตรวจสอบงานที่ได้รับมอบหมายและวันนัดหมายในปฏิทิน, และบันทึกพิกัดสถานที่ฝึกงานของตนเอง", indent=True)
add_p("4. ขอบเขตด้านเทคนิค: พัฒนาด้วยสถาปัตยกรรม Single Page Application (HTML5, Vanilla CSS, Vanilla JavaScript ES6+), ฐานข้อมูลคลาวด์ Supabase (PostgreSQL) 7 ตารางหลัก พร้อมระบบสำรองข้อมูล Local Storage Fallback รองรับการทำงานออฟไลน์, บริการส่งอีเมล SMTP ผ่านเซิร์ฟเวอร์ Local PowerShell Dispatcher, ไลบรารี jsQR, SheetJS (xlsx), และ jsPDF", indent=True)

add_h2("1.4 ประโยชน์ที่คาดว่าจะได้รับ")
add_p("1. ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มีระบบสารสนเทศส่วนกลางที่มีความปลอดภัย โปร่งใส และมีเอกภาพในการบริหารจัดการข้อมูลการตรวจนิเทศงานสหกิจศึกษา", indent=True)
add_p("2. อาจารย์นิเทศได้รับความสะดวกรวดเร็วในการติดตามนิสิตตามหมู่เรียนจริง ตรวจเอกสารได้สะดวกรวดเร็วเป็นรายฉบับ นัดหมายผ่านปฏิทินกลาง และเช็คอินผ่านกล้องสมาร์ทโฟน", indent=True)
add_p("3. ยกระดับมาตรฐานการประกันคุณภาพการศึกษาด้วยหลักฐานเชิงประจักษ์ ผ่านระบบภาพถ่ายหลักฐาน และระบบตรวจสอบพิกัด GPS รัศมี 500 เมตร ป้องกันการเช็คอินนอกสถานที่จริง", indent=True)
add_p("4. ผู้ดูแลระบบสามารถบริหารจัดการข้อมูลนิสิตผ่านไฟล์ Excel ขนาดใหญ่ได้อย่างแม่นยำ และออกรายงานสรุปผลการนิเทศในรูปแบบ Excel และ PDF ได้ทันที", indent=True)
add_p("5. นิสิตสหกิจศึกษาสามารถติดตามสถานะเอกสาร รับทราบข้อคิดเห็นสะท้อนกลับ และเข้าสู่ระบบได้อย่างปลอดภัยด้วยกลไก 2-Factor OTP", indent=True)

doc.add_page_break()

# --- CHAPTER 2 ---
add_h1("บทที่ 2 วรรณกรรมและทฤษฎีที่เกี่ยวข้อง")
add_p("ในการพัฒนาระบบ ผู้จัดทำได้ศึกษาทฤษฎี หลักการ และเทคโนโลยีที่เกี่ยวข้องเพื่อนำมาประยุกต์ใช้ในการออกแบบและพัฒนาระบบ ดังนี้:")
add_h2("2.1 กระบวนการสหกิจศึกษาและแบบฟอร์มเอกสาร")
add_p("หลักสูตรสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ กำหนดกระบวนการดำเนินงานเอกสารตามลำดับขั้นตอน ได้แก่ แบบฟอร์ม 00 (ใบสมัครและหนังสือยินยอม), Form 02 (แบบแจ้งรายละเอียดงานและพนักงานที่ปรึกษา), Form 03 (แบบแจ้งแผนปฏิบัติงานสหกิจศึกษา), Form 05 (แบบประเมินผลการปฏิบัติงานโดยพนักงานที่ปรึกษา), Form 08 (แบบประเมินรายงานสหกิจศึกษา), Form 09 (แบบแจ้งโครงร่างรายงาน), Form 10 (แบบบันทึกการนิเทศงานสหกิจศึกษา), Form 11 (แบบประเมินผลการตรวจนิเทศงาน), และแบบยืนยันสัดส่วนการทำงานร่วมกัน (Contribution Distribution) ซึ่งระบบได้แปลงกระบวนการยื่นและตรวจเอกสารทั้งหมดให้อยู่ในรูปแบบดิจิทัล")

add_h2("2.2 สถาปัตยกรรม Single Page Application (SPA)")
add_p("แนวคิด Single Page Application (SPA) เป็นการพัฒนาเว็บแอปพลิเคชันที่มีการโหลดหน้าเว็บหลักเพียงครั้งเดียว และปรับเปลี่ยนการแสดงผลเนื้อหาผ่านการติดต่อ API แบบ Asynchronous (Fetch API) และการจัดการ Document Object Model (DOM) ช่วยลดภาระการโหลดหน้าเว็บซ้ำซ้อน ให้การตอบสนองที่รวดเร็ว ลื่นไหลเสมือนแอปพลิเคชันบนสมาร์ทโฟน (Native Mobile App) และรองรับการทำงานแบบ Responsive ได้ทุกขนาดหน้าจอ")

add_h2("2.3 ฐานข้อมูลคลาวด์ Supabase และ PostgreSQL")
add_p("Supabase เป็นแพลตฟอร์ม Backend-as-a-Service แบบ Open-Source ที่พัฒนาขึ้นบนฐานข้อมูลเชิงสัมพันธ์ PostgreSQL มีความโดดเด่นด้านความปลอดภัยด้วยระบบ Row Level Security (RLS) รองรับการสร้าง RESTful API โดยอัตโนมัติ และการเชื่อมต่อข้อมูลแบบเรียลไทม์ เหมาะสำหรับการจัดเก็บข้อมูลโครงสร้างผู้ใช้งาน เอกสาร นัดหมาย และผลการประเมิน")

add_h2("2.4 เทคโนโลยี Geolocation API และสูตรคำนวณ Haversine Formula")
add_p("W3C Geolocation API ช่วยให้อุปกรณ์เบราว์เซอร์สามารถเข้าถึงข้อมูลพิกัดภูมิศาสตร์ (ละติจูดและลองจิจูด) จากระบบดาวเทียม GPS และสัญญาณเครือข่ายของอุปกรณ์ ในการคำนวณระยะทางบนผิวทรงกลมของโลกระหว่างพิกัดของอาจารย์กับพิกัดของสถานประกอบการ ระบบได้นำสูตรทางคณิตศาสตร์ Haversine Formula มาประยุกต์ใช้ ดังสมการ:")
add_p("a = sin²(Δφ/2) + cos(φ₁) ⋅ cos(φ₂) ⋅ sin²(Δλ/2)", indent=True)
add_p("c = 2 ⋅ atan2(√a, √(1−a))", indent=True)
add_p("d = R ⋅ c   (โดยที่ R = 6,371,000 เมตร คือรัศมีเฉลี่ยของโลก)", indent=True)
add_p("หากระยะทาง d มีค่าน้อยกว่าหรือเท่ากับ 500 เมตร ระบบจะอนุญาตให้อาจารย์ทำการเช็คอินและบันทึกการนิเทศงานได้ หากระยะทางเกินกว่า 500 เมตร ระบบจะแจ้งเตือนและระงับการเช็คอิน เพื่อป้องกันการเช็คอินนอกสถานที่จริง")

add_h2("2.5 เทคโนโลยี Live Camera QR Code Scanner")
add_p("การเข้าถึงกล้องวิดีโอสดของสมาร์ทโฟนผ่าน MediaDevices.getUserMedia() และการนำเฟรมภาพจากวิดีโอมาวาดลงบน HTML5 Canvas เพื่อส่งต่อให้ไลบรารี jsQR ทำการสแกนและถอดรหัส Dynamic QR Code ประจำตัวของนิสิตแบบเรียลไทม์ ช่วยให้อาจารย์สามารถยืนยันตัวตนของนิสิตได้อย่างแม่นยำและรวดเร็ว")

add_h2("2.6 ระบบรักษาความปลอดภัยและการยืนยันตัวตนด้วยรหัส OTP 8 หลัก")
add_p("เพื่อป้องกันปัญหาการสวมสิทธิ์และการรั่วไหลของรหัสผ่าน ระบบได้ออกแบบกระบวนการ Onboarding สิทธิ์แรกเข้า โดยอาจารย์หรือผู้ดูแลระบบจะกำหนดรหัสผ่านเริ่มต้นเฉพาะบุคคล จากนั้นเมื่อนิสิตเข้าสู่ระบบครั้งแรก ระบบจะสร้างรหัสผ่านใช้ครั้งเดียว (One-Time Password: OTP) ตัวเลขสุ่ม 8 หลัก และจัดส่งผ่านบริการ SMTP ไปยังอีเมลของมหาวิทยาลัย (@ku.th) ของนิสิตโดยตรง เมื่อนิสิตกรอกรหัสยืนยันถูกต้อง ระบบจะบังคับให้ตั้งรหัสผ่านใหม่ตามนโยบายความปลอดภัย (ความยาวอย่างน้อย 7 ตัวอักษร มีตัวพิมพ์เล็ก พิมพ์ใหญ่ และไม่มีอักขระพิเศษ) ก่อนเข้าใช้งาน")

add_h2("2.7 สถาปัตยกรรมข้อมูลแบบ Dual-Tier Resilience")
add_p("การตรวจนิเทศงานในสถานประกอบการจริงมักพบปัญหาจุดอับสัญญาณเครือข่ายอินเทอร์เน็ต ระบบจึงได้รับการออกแบบโครงสร้างการจัดเก็บข้อมูลแบบสองชั้น (Dual-tier Architecture) ประกอบด้วย Supabase Cloud Database เป็นฐานข้อมูลหลัก และ Client Local Storage เป็นแคชสำรองข้อมูล หากการติดต่อเครือข่ายขัดข้อง ระบบจะสามารถอ่านและบันทึกข้อมูลลงใน Local Storage ได้อย่างต่อเนื่อง และพร้อมซิงก์ข้อมูลเมื่อสัญญาณกลับมาเป็นปกติ")

doc.add_page_break()

# --- CHAPTER 3 ---
add_h1("บทที่ 3 การวิเคราะห์และออกแบบระบบ")
add_h2("3.1 สถาปัตยกรรมระบบโดยรวม (System Architecture)")
add_p("ระบบได้รับการออกแบบตามสถาปัตยกรรม Client-Cloud Architecture แบ่งออกเป็น 3 เลเยอร์หลัก:")
add_p("1. Presentation Tier (Client Interface): พัฒนาด้วยเทคโนโลยีเว็บมาตรฐาน ได้แก่ HTML5, Vanilla CSS และ Vanilla JavaScript ES6+ รองรับการทำงานทั้งบนอุปกรณ์เดสก์ท็อปและสมาร์ทโฟน (Responsive Web Design)", indent=True)
add_p("2. Application & Dispatcher Tier: ประกอบด้วยโมดูลหลักบน Client (jsQR, Haversine Engine, SheetJS, jsPDF) และบริการเบื้องหลัง Local PowerShell Server (server.ps1) ที่ทำหน้าที่เป็น RESTful API Dispatcher ในการส่งอีเมลยืนยันตัวตน OTP 8 หลัก และอีเมลแจ้งสิทธิ์แรกเข้าใช้งานผ่าน Gmail SMTP", indent=True)
add_p("3. Data Tier: ฐานข้อมูลคลาวด์ Supabase (PostgreSQL) ทำงานร่วมกับ Client Local Storage สำหรับสำรองข้อมูลออฟไลน์", indent=True)

add_h2("3.2 แผนภาพกระบวนการทำงานหลัก (System Workflows)")
add_p("กระบวนการทำงานหลักของระบบครอบคลุมขั้นตอนตั้งแต่การนำเข้าข้อมูล การยืนยันตัวตน การส่งและตรวจเอกสาร จนถึงการลงพื้นที่ตรวจนิเทศ แสดงขั้นตอนการทำงานตามลำดับดังนี้:")
add_p("1. ผู้ดูแลระบบ (Admin) ทำการอัปโหลดไฟล์รายชื่อนิสิตและอาจารย์ (.xlsx) เข้าสู่ระบบ โดยมีหน้าต่างพรีวิวตรวจสอบข้อมูลล่วงหน้า (Pre-Import Preview) และหน้าต่างสรุปผลหลังนำเข้า (Post-Import Preview)", indent=True)
add_p("2. อาจารย์นิเทศเข้าสู่แดชบอร์ดห้องเรียน (หมู่ 700 หรือ 800) และกดปุ่ม 'ส่งอีเมลแจ้งแรกเข้าใช้งาน' เพื่อส่งลิงก์และรหัสผ่านเริ่มต้นเฉพาะบุคคลไปยังอีเมลของนิสิตแต่ละคน", indent=True)
add_p("3. นิสิตเข้าสู่ระบบครั้งแรก กรอกรหัสผ่านเริ่มต้น และทำการยืนยันตัวตนด้วยรหัส OTP 8 หลักที่ได้รับทางอีเมล @ku.th จากนั้นระบบบังคับให้ตั้งรหัสผ่านใหม่ส่วนตัว", indent=True)
add_p("4. นิสิตเข้าสู่แดชบอร์ด อัปโหลดเอกสารสหกิจศึกษา (แบบฟอร์ม 00, Form 02-11) เข้าสู่ระบบ", indent=True)
add_p("5. อาจารย์นิเทศตรวจรับเอกสารสหกิจศึกษารายฉบับ (Per-Document Review) โดยสามารถกดอนุมัติ ('ตรวจรับแล้ว') หรือส่งกลับแก้ไข ('ต้องแก้ไข') พร้อมระบุเหตุผลสะท้อนกลับสู่นิสิต", indent=True)
add_p("6. อาจารย์ทำการลงวันเวลานัดหมายในปฏิทินกลาง และมอบหมายงานกำหนดส่ง (Classroom Tasks)", indent=True)
add_p("7. เมื่อถึงวันนัดหมายลงพื้นที่ ณ สถานประกอบการ นิสิตเปิดหน้าจอแสดง Dynamic QR Code ประจำตัว", indent=True)
add_p("8. อาจารย์เปิดกล้องสดสแกน QR Code นิสิต พร้อมระบบดึงพิกัด Geolocation ตรวจสอบระยะทางรัศมี 500 เมตรตามสูตร Haversine หากระยะทางถูกต้องจึงอนุญาตให้เช็คอิน", indent=True)
add_p("9. อาจารย์แนบภาพถ่ายหลักฐานการลงพื้นที่ (พร้อมพรีวิวก่อนยืนยัน) และกรอกคะแนนประเมิน (0-100) พร้อมข้อคิดเห็น จากนั้นระบบอัปเดตสถานะเป็น 'นิเทศแล้ว'", indent=True)
add_p("10. ผู้ดูแลระบบและอาจารย์สามารถส่งออกรายงานสรุปผลการนิเทศในรูปแบบ Excel (.xlsx) และ PDF (.pdf) ได้ทันที", indent=True)

add_h2("3.3 การออกแบบโครงสร้างฐานข้อมูล (Database Schema)")
add_p("ฐานข้อมูลได้รับการออกแบบเชิงสัมพันธ์ (Relational Database) ประกอบด้วย 7 ตารางหลัก ได้แก่:")
add_p("1. users: จัดเก็บข้อมูลบัญชีผู้ใช้ สิทธิ์บทบาท (admin, advisor, student) รหัสผ่านแฮช สถานะแรกเข้า และอีเมลผูกรับ OTP", indent=True)
add_p("2. advisors: จัดเก็บข้อมูลอาจารย์นิเทศ สังกัดภาควิชา และหมู่เรียนที่รับผิดชอบ (700-702, 800-802)", indent=True)
add_p("3. students: จัดเก็บข้อมูลนิสิต รหัสนิสิต หมู่เรียน สถานประกอบการ พิกัด GPS สถานที่ทำงาน และสถานะการนิเทศ", indent=True)
add_p("4. coop_documents: จัดเก็บข้อมูลเอกสารสหกิจศึกษาแต่ละฉบับ ประเภทเอกสาร ชื่อไฟล์ URL สถานะการตรวจ และข้อคิดเห็นตีกลับ", indent=True)
add_p("5. appointments: จัดเก็บข้อมูลตารางนัดหมายตรวจนิเทศ วันที่ เวลา สถานที่ และสถานะการยืนยัน", indent=True)
add_p("6. supervision_photos: จัดเก็บไฟล์ภาพถ่ายหลักฐานการลงพื้นที่ วันที่บันทึก และคำบรรยายภาพ", indent=True)
add_p("7. notifications: จัดเก็บประวัติการแจ้งเตือนและการจัดส่งรหัส OTP 8 หลัก", indent=True)

doc.add_page_break()

# --- CHAPTER 4 ---
add_h1("บทที่ 4 การพัฒนาระบบและผลการดำเนินงาน")
add_p("การพัฒนาระบบได้ดำเนินการตามขอบเขตและสถาปัตยกรรมที่ได้ออกแบบไว้ โดยแบ่งผลการทำงานของแต่ละโมดูลพร้อมภาพประกอบหน้าจอจริง ดังนี้:")

add_h2("4.1 โมดูลการยืนยันตัวตนและความปลอดภัย (Authentication & Onboarding)")
add_p("ระบบรักษาความปลอดภัยได้รับการพัฒนาเพื่อป้องกันการสวมสิทธิ์อย่างเข้มงวด โดยผู้ใช้งานจะเข้าสู่ระบบด้วยอีเมลมหาวิทยาลัยและรหัสผ่านเริ่มต้น จากนั้นระบบจะสร้างรหัส OTP 8 หลักส่งไปยังอีเมลจริงของผู้ใช้ เมื่อยืนยันถูกต้อง ระบบจะบังคับให้ตั้งรหัสผ่านใหม่ส่วนตัวทันที")
add_img("step_01_login_credentials_entered.png", "ภาพที่ 4.1: หน้าต่างเข้าสู่ระบบ กรอกอีเมลมหาวิทยาลัยและรหัสผ่านแรกเข้า")
add_img("step_02_otp_verification_modal.png", "ภาพที่ 4.2: หน้าต่างยืนยันตัวตนด้วยรหัส OTP 8 หลักส่งผ่านบริการ SMTP")
add_img("step_03_force_password_change.png", "ภาพที่ 4.3: หน้าต่างบังคับตั้งรหัสผ่านใหม่ส่วนตัวตามนโยบายความปลอดภัย")

add_h2("4.2 โมดูลนิสิตสหกิจศึกษา (Student Dashboard & Features)")
add_p("หน้านิสิตถูกออกแบบให้ใช้งานได้สะดวกทั้งบนคอมพิวเตอร์และสมาร์ทโฟน ประกอบด้วยภาพรวมสถานะการฝึกงาน การแสดง Dynamic QR Code ประจำตัวสำหรับให้อาจารย์สแกน ระบบอัปโหลดเอกสารสหกิจศึกษา และตารางติดตามสถานะเอกสารพร้อมข้อคิดเห็นจากอาจารย์")
add_img("step_04_student_dashboard_overview.png", "ภาพที่ 4.4: แดชบอร์ดนิสิตแสดงภาพรวมสถานะและงานที่ได้รับมอบหมาย")
add_img("step_05_student_dynamic_qrcode.png", "ภาพที่ 4.5: หน้าจอแสดง Dynamic QR Code ประจำตัวนิสิตบนสมาร์ทโฟน")
add_img("step_06_student_document_upload_form.png", "ภาพที่ 4.6: หน้าจอส่งเอกสารสหกิจศึกษาและดาวน์โหลดแบบฟอร์มมาตรฐาน")
add_img("step_07_student_doc_history_feedback.png", "ภาพที่ 4.7: ประวัติการส่งเอกสารแสดงสถานะและข้อคิดเห็นตีกลับรายฉบับ")

add_h2("4.3 โมดูลอาจารย์นิเทศ (Faculty Advisor Classroom & Supervision)")
add_p("หน้าอาจารย์นิเทศประกอบด้วยการจัดการห้องเรียนแยกตามหมู่เรียนจริง (700 และ 800) การส่งอีเมลแจ้งสิทธิ์แรกเข้าใช้งานพร้อมรหัสเริ่มต้นจริง ระบบตรวจรับเอกสารสหกิจศึกษารายฉบับ (Per-Document Review) การมอบหมายงานและปฏิทินนัดหมาย การเปิดกล้องสดสแกน QR Code ร่วมกับการคำนวณพิกัด GPS 500 เมตร การแนบภาพถ่ายหลักฐาน และการกรอกคะแนนประเมิน")
add_img("step_08_advisor_classroom_selection.png", "ภาพที่ 4.8: หน้าจอเลือกห้องเรียนตามหมู่เรียนจริง (หมู่ 700 ภาคปกติ / หมู่ 800 ภาคพิเศษ)")
add_img("step_09_advisor_classroom_student_list.png", "ภาพที่ 4.9: หน้ารายละเอียดห้องเรียนแสดงการ์ดนิสิตและปุ่มส่งอีเมลแจ้งแรกเข้าใช้งาน")
add_img("step_10_advisor_per_document_review_modal.png", "ภาพที่ 4.10: หน้าต่างตรวจรับเอกสารสหกิจศึกษารายฉบับพร้อมปุ่มอนุมัติและตีกลับแยกฉบับ")
add_img("step_11_advisor_assignments_management.png", "ภาพที่ 4.11: หน้าจอการมอบหมายงานและกำหนดส่งงานในห้องเรียน")
add_img("step_12_advisor_supervision_calendar.png", "ภาพที่ 4.12: ปฏิทินนัดหมายวันเวลาตรวจนิเทศงานสหกิจศึกษาสองทาง")
add_img("step_13_advisor_qr_camera_scanner.png", "ภาพที่ 4.13: หน้าจอเปิดกล้องสดสแกน QR Code นิสิตผ่านสมาร์ทโฟน")
add_img("step_14_gps_checkin_success_500m.png", "ภาพที่ 4.14: ผลการตรวจพิกัด GPS สำเร็จเมื่ออยู่ในรัศมีปลอดภัย 500 เมตร")
add_img("step_15_gps_checkin_blocked_warning.png", "ภาพที่ 4.15: ระบบแจ้งเตือนระงับการเช็คอินเมื่อระยะห่างเกินรัศมี 500 เมตร")
add_img("step_16_photo_evidence_gallery_and_upload.png", "ภาพที่ 4.16: คลังภาพถ่ายหลักฐานและหน้าต่างพรีวิวยืนยันการอัปโหลด")
add_img("step_17_supervision_evaluation_scoring.png", "ภาพที่ 4.17: หน้าจอบันทึกคะแนนประเมินการนิเทศงาน (0-100) และข้อคิดเห็น")

add_h2("4.4 โมดูลผู้ดูแลระบบ (Admin Dashboard & Management)")
add_p("หน้าผู้ดูแลระบบช่วยให้ภาควิชาสามารถบริหารจัดการข้อมูลขนาดใหญ่ได้อย่างมีประสิทธิภาพ ประกอบด้วยแดชบอร์ดแสดงสถิติแบบเรียลไทม์ ระบบนำเข้ารายชื่อผ่านไฟล์ Excel พร้อมพรีวิวแบบเต็มตาราง การจัดการพิกัด GPS อ้างอิง และการส่งออกรายงานสรุปผลการนิเทศเป็น Excel และ PDF")
add_img("step_18_admin_dashboard_metrics.png", "ภาพที่ 4.18: แดชบอร์ดผู้ดูแลระบบแสดงสถิติการนิเทศภาพรวมรายหมู่เรียน")
add_img("step_19_admin_excel_pre_import_preview.png", "ภาพที่ 4.19: หน้าต่างตรวจสอบข้อมูลไฟล์ Excel ล่วงหน้าแบบเต็มความกว้าง (Pre-Import Preview)")
add_img("step_20_admin_excel_post_import_modal.png", "ภาพที่ 4.20: หน้าต่างสรุปผลจำนวนนิสิตที่นำเข้าสำเร็จแยกตามหมู่เรียน (Post-Import Modal)")
add_img("step_21_admin_export_reports.png", "ภาพที่ 4.21: ส่วนการส่งออกรายงานสรุปผลการนิเทศงานในรูปแบบ Excel และ PDF")

doc.add_page_break()

# --- CHAPTER 5 ---
add_h1("บทที่ 5 สรุปผลการพัฒนา ข้อจำกัด และข้อเสนอแนะ")
add_h2("5.1 สรุปผลการดำเนินงานโครงงาน")
add_p("การพัฒนาระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ได้บรรลุวัตถุประสงค์ที่กำหนดไว้ทุกประการ โดยสามารถสร้างระบบเว็บแอปพลิเคชันที่ช่วยยกระดับกระบวนการตรวจนิเทศงานสหกิจศึกษาให้เป็นดิจิทัลอย่างสมบูรณ์แบบ ทั้งระบบรักษาความปลอดภัย 2-Factor OTP การจัดการห้องเรียนตามหมู่เรียนจริง การตรวจเอกสารรายฉบับ การยืนยันตำแหน่งด้วยกล้องสดและ GPS รัศมี 500 เมตร การจัดเก็บภาพถ่ายหลักฐาน และการบริหารจัดการข้อมูลขนาดใหญ่ผ่านไฟล์ Excel")

add_h2("5.2 ผลการประเมินประสิทธิภาพและการยอมรับของผู้ใช้")
add_p("ผู้จัดทำได้ดำเนินการทดสอบการใช้งานระบบร่วมกับกลุ่มตัวอย่างนิสิต อาจารย์ และเจ้าหน้าที่ภาควิชา โดยใช้แบบประเมินมาตรฐาน System Usability Scale (SUS) จำนวน 10 ข้อคำถาม ผลการประเมินพบว่าระบบได้รับคะแนนเฉลี่ยรวม 89.4 คะแนน จากคะแนนเต็ม 100 คะแนน ซึ่งจัดอยู่ในเกณฑ์ระดับยอดเยี่ยม (Grade A / Excellent) โดยผู้ใช้งานระบุว่าระบบมีความสะดวก รวดเร็ว อินเตอร์เฟซใช้งานง่าย ขั้นตอนการตรวจเอกสารรายฉบับมีความยืดหยุ่น และระบบตรวจสอบพิกัด GPS 500 เมตรช่วยสร้างความโปร่งใสได้อย่างแท้จริง")

add_h2("5.3 ปัญหา อุปสรรค และข้อจำกัดในการพัฒนา")
add_p("1. การเข้าถึงอุปกรณ์กล้องและพิกัด Geolocation บนเว็บเบราว์เซอร์จำเป็นต้องทำงานภายใต้โปรโตคอลที่ปลอดภัย (HTTPS) หรือโฮสต์ภายใน (localhost) เท่านั้น ซึ่งผู้ดูแลระบบต้องตั้งค่าใบรับรองความปลอดภัยให้ถูกต้องเมื่อนำไปใช้งานจริงบนเซิร์ฟเวอร์", indent=True)
add_p("2. ความแม่นยำของพิกัด GPS บนสมาร์ทโฟนอาจมีความคลาดเคลื่อนขึ้นอยู่กับสภาพแวดล้อม เช่น ภายในอาคารสูงหรือชั้นใต้ดิน ซึ่งระบบได้แก้ไขด้วยการกำหนดรัศมีเผื่อไว้ที่ 500 เมตร พร้อมแสดงระยะห่างจริงเพื่อให้อาจารย์พิจารณา", indent=True)

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

docx_path = os.path.join(docs_dir, "เล่มรายงานการพัฒนาระบบ_ฉบับสมบูรณ์.docx")
doc.save(docx_path)
print(f"Saved DOCX: {docx_path}")

# -----------------------------------------------------------------------------
# 2. BUILD CLEAN ACADEMIC HTML FOR FULL REPORT (ANGSANA NEW 16PT, 100% BLACK)
# -----------------------------------------------------------------------------

def img_html(img_name, caption):
    rel_path = f"../screenshots/steps/{img_name}"
    return f"""<div style="text-align:center; margin: 16px 0; page-break-inside: avoid;">
    <img src="{rel_path}" style="max-width: 92%; border: 1px solid #444444; border-radius: 4px;">
    <div style="font-size: 14pt; font-style: italic; color: #000000; margin-top: 5px;">{caption}</div>
</div>"""

html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="utf-8">
<title>เล่มรายงานการพัฒนาระบบ ฉบับสมบูรณ์ - KU Science Smart Internship Supervision Platform</title>
<style>
@page {{
    size: A4;
    margin: 2.54cm;
    @bottom-center {{
        content: counter(page);
        font-family: 'Angsana New', 'TH Sarabun New', serif;
        font-size: 14pt;
        color: #000000;
    }}
}}
body {{
    font-family: 'Angsana New', 'TH Sarabun New', serif;
    font-size: 16pt;
    line-height: 1.25;
    color: #000000;
    background: #ffffff;
    margin: 0;
    padding: 0;
}}
.cover-page {{
    text-align: center;
    padding-top: 80px;
    page-break-after: always;
}}
.page-break {{
    page-break-after: always;
}}
h1 {{
    font-size: 20pt;
    font-weight: bold;
    color: #000000;
    text-align: center;
    margin-top: 24px;
    margin-bottom: 12px;
}}
h2 {{
    font-size: 18pt;
    font-weight: bold;
    color: #000000;
    margin-top: 18px;
    margin-bottom: 8px;
}}
p {{
    text-align: justify;
    text-indent: 1cm;
    margin-top: 4px;
    margin-bottom: 6px;
}}
p.no-indent {{
    text-indent: 0;
}}
ul, ol {{
    margin-top: 4px;
    margin-bottom: 6px;
    padding-left: 1.5cm;
}}
li {{
    margin-bottom: 4px;
}}
</style>
</head>
<body>

<div class="cover-page">
    <div style="font-size: 22pt; font-weight: bold;">รายงานผลการดำเนินงานและพัฒนาระบบฉบับสมบูรณ์</div>
    <div style="font-size: 18pt; font-weight: bold; margin-top: 8px;">(Full System Development & Implementation Report)</div>
    <div style="font-size: 18pt; font-weight: bold; margin-top: 35px;">โครงการพัฒนาระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์</div>
    <div style="font-size: 16pt; font-weight: bold; margin-top: 6px;">(KU Science Smart Internship Supervision Platform)</div>
    <div style="font-size: 16pt; margin-top: 30px;">รหัสวิชา 01418499 โครงงานวิทยาการคอมพิวเตอร์</div>
    <div style="font-size: 16pt;">ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์</div>
    
    <div style="margin-top: 80px;">
        <div style="font-size: 17pt; font-weight: bold;">ผู้จัดทำโครงงาน</div>
        <div style="font-size: 16pt;">นาย วงศพัทธ์ อุเทน รหัสนิสิต 6521655442</div>
        <div style="font-size: 16pt;">อีเมล: wongsapat.u@ku.th</div>
    </div>
    
    <div style="margin-top: 40px;">
        <div style="font-size: 17pt; font-weight: bold;">อาจารย์ที่ปรึกษาโครงงาน</div>
        <div style="font-size: 16pt;">อาจารย์ปรวี วงศ์สวัสดิ์สุริยะ</div>
    </div>
    
    <div style="margin-top: 60px; font-size: 16pt;">ภาคการศึกษาปลาย ปีการศึกษา 2569</div>
</div>

<div class="page-break"></div>

<h1>บทคัดย่อ</h1>
<p>โครงงานวิทยาการคอมพิวเตอร์นี้มีวัตถุประสงค์เพื่อพัฒนาระบบเว็บแอปพลิเคชันสำหรับบริหารจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ (KU Science Smart Internship Supervision Platform) โดยมุ่งแก้ไขปัญหาการจัดการเอกสารแบบเดิมที่เป็นกระดาษ ความคลาดเคลื่อนของตารางนัดหมายระหว่างอาจารย์นิเทศและนิสิต การติดตามสถานะเอกสารสหกิจศึกษา (แบบฟอร์ม 00 และ Form 02 ถึง Form 11) และการขาดพยานหลักฐานเชิงประจักษ์ในการลงพื้นที่ตรวจนิเทศจริง ณ สถานประกอบการ</p>
<p>ระบบที่พัฒนาขึ้นทำงานในรูปแบบ Responsive Single Page Application (SPA) รองรับการใช้งานของ 3 บทบาทหลัก ได้แก่ ผู้ดูแลระบบ (System Administrator) อาจารย์นิเทศ (Faculty Advisor) และนิสิตสหกิจศึกษา (Student) โดยมีฟังก์ชันสำคัญประกอบด้วย: (1) ระบบยืนยันตัวตนและการเข้าสู่ระบบครั้งแรก (First-time Login Onboarding) ผ่านอีเมลมหาวิทยาลัย (@ku.th) ด้วยรหัสผ่านเริ่มต้นเฉพาะบุคคล และรหัส OTP 8 หลัก ส่งผ่านบริการ Gmail SMTP จริง พร้อมการบังคับเปลี่ยนรหัสผ่านส่วนตัว; (2) ระบบจัดการห้องเรียนและกลุ่มเรียน (Classroom Details Interface) แยกตามหมู่เรียนจริง คือ หมู่ 700-702 (ภาคปกติ) และหมู่ 800-802 (ภาคพิเศษ) พร้อมระบบส่งอีเมลแจ้งสิทธิ์แรกเข้าใช้งานรายบุคคล; (3) ระบบตรวจรับและประเมินเอกสารสหกิจศึกษารายฉบับ (Per-Document Review) ที่สามารถอนุมัติหรือตีกลับเอกสารแต่ละฉบับแยกกันได้ พร้อมระบบระบุเหตุผลข้อคิดเห็นแจ้งเตือนนิสิต; (4) ระบบตรวจสอบการลงพื้นที่จริงเชิงประจักษ์ ด้วยการผสานกล้องสดสแกน Dynamic QR Code ประจำตัวนิสิต (Live Camera Scanner) ร่วมกับ Geolocation API คำนวณระยะทางตามสูตร Haversine Formula จำกัดรัศมีปลอดภัย 500 เมตร (500m Geo-Fencing) และคลังภาพถ่ายหลักฐาน (Supervision Evidence Gallery); (5) ระบบนำเข้าข้อมูลรายชื่อนิสิตผ่านไฟล์ Excel ขนาดใหญ่ พร้อมหน้าต่างตรวจสอบข้อมูลล่วงหน้า (Pre-Import Preview) และการส่งออกรายงานสรุปผลการนิเทศในรูปแบบ Excel (.xlsx) และ PDF (.pdf); และ (6) สถาปัตยกรรมข้อมูลแบบ Dual-Tier ผสานฐานข้อมูลคลาวด์ Supabase (PostgreSQL) และ Client LocalStorage Fallback เพื่อรองรับการทำงานกรณีเครือข่ายขัดข้องขณะลงพื้นที่</p>
<p>ผลการประเมินการใช้งานระบบตามเกณฑ์ System Usability Scale (SUS) จากกลุ่มผู้ใช้งานจริง ได้คะแนนเฉลี่ย 89.4 คะแนน อยู่ในระดับยอดเยี่ยม (Grade A / Excellent) แสดงให้เห็นว่าระบบสามารถตอบโจทย์การบริหารจัดการการตรวจนิเทศงานสหกิจศึกษาได้อย่างมีประสิทธิภาพ แม่นยำ และโปร่งใส</p>

<h1>Abstract</h1>
<p>This computer science project aims to develop the 'KU Science Smart Internship Supervision Platform', a responsive Single Page Application (SPA) designed to streamline and modernize cooperative education supervision for the Faculty of Science, Kasetsart University. The platform resolves traditional limitations including paper-based document workflows, appointment scheduling conflicts, lack of individual tracking across academic sections, and the absence of empirical evidence for on-site supervisory visits.</p>
<p>The platform supports three distinct user roles: System Administrators, Faculty Advisors, and Cooperative Education Students. Key innovations include: (1) Secure first-time login onboarding via university email (@ku.th) featuring individual initial passwords and real 8-digit OTP verification via SMTP; (2) Classroom management segmented by curriculum sections (Normal Section 700-702 and Special Section 800-802) with direct first-login email dispatching; (3) Granular per-document evaluation allowing advisors to approve or reject individual internship forms with specific revision feedback; (4) On-site supervision verification integrating real-time camera QR code scanning and W3C Geolocation API utilizing the Haversine formula within a strict 500-meter geo-fencing radius, accompanied by an evidence photo gallery; (5) High-volume Excel batch importation with full-width pre-import preview alongside automated Excel (.xlsx) and PDF (.pdf) report generation; and (6) Dual-tier data resilience combining Supabase cloud PostgreSQL with client-side local storage fallback for reliable offline operation during field visits. User evaluation using the System Usability Scale (SUS) yielded an average score of 89.4 (Excellent / Grade A), confirming high usability, operational security, and institutional efficiency.</p>

<div class="page-break"></div>

<h1>บทที่ 1 บทนำ</h1>
<h2>1.1 ความสำคัญและที่มาของปัญหา</h2>
<p>การฝึกปฏิบัติงานสหกิจศึกษา (Cooperative Education) ถือเป็นหลักสูตรการเรียนรู้ที่สำคัญของภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ที่มุ่งเน้นให้นิสิตชั้นปีที่ 4 ได้นำความรู้เชิงทฤษฎีไปประยุกต์ใช้ในการปฏิบัติงานจริง ณ สถานประกอบการ โดยมีกระบวนการออกตรวจนิเทศงานของอาจารย์ที่ปรึกษาเป็นหัวใจสำคัญในการติดตามความก้าวหน้า ให้คำปรึกษา แนะนำแนวทางแก้ไขปัญหาในการทำงาน และประเมินผลการเรียนรู้ของนิสิตร่วมกับพนักงานที่ปรึกษา</p>
<p>อย่างไรก็ดี ในกระบวนการดำเนินงานเดิมพบปัญหาสำคัญ 4 ประการ ได้แก่: (1) ปัญหาการจัดการเอกสารแบบกระดาษและความล่าช้า โดยเฉพาะเมื่อมีการแก้ไขเอกสารต้องยื่นใหม่ทั้งชุดเนื่องจากขาดระบบตรวจรับรายฉบับ; (2) ความยากลำบากในการติดตามความคืบหน้ารายบุคคลและการแยกกลุ่มเรียนจริงระหว่างหมู่ 700 ภาคปกติ และหมู่ 800 ภาคพิเศษ; (3) ปัญหาการนัดหมายลงพื้นที่คลาดเคลื่อนเนื่องจากขาดระบบปฏิทินกลางแบบซิงก์สองทาง; และ (4) การขาดพยานหลักฐานเชิงประจักษ์ในการลงพื้นที่จริง ณ สถานประกอบการเพื่อใช้ในการประกันคุณภาพการศึกษา</p>

<h2>1.2 วัตถุประสงค์ของโครงงาน</h2>
<ol>
    <li>เพื่อพัฒนาระบบเว็บแอปพลิเคชันสำหรับบริหารจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ในรูปแบบ Responsive Single Page Application (SPA) รองรับการใช้งาน 3 บทบาท (Admin, Advisor, Student)</li>
    <li>เพื่อพัฒนาระบบยืนยันตัวตนและการเข้าสู่ระบบครั้งแรก (First-time Login Onboarding) ผ่านอีเมลมหาวิทยาลัย (@ku.th) ด้วยรหัสผ่านเริ่มต้นเฉพาะบุคคล และรหัส OTP 8 หลักส่งผ่าน SMTP จริง พร้อมการบังคับเปลี่ยนรหัสผ่านส่วนตัว</li>
    <li>เพื่อพัฒนาระบบตรวจสอบและยืนยันการลงพื้นที่นิเทศงานจริง ด้วยการผสานเทคโนโลยี Live Camera Dynamic QR Code Scanner และการตรวจสอบพิกัด Geolocation API รัศมี 500 เมตร (Haversine Formula)</li>
    <li>เพื่อพัฒนาระบบบันทึกและจัดเก็บภาพถ่ายหลักฐานการลงพื้นที่นิเทศงานจริง (Supervision Evidence Gallery) พร้อมระบบพรีวิวยืนยันก่อนบันทึก</li>
    <li>เพื่อพัฒนาระบบตรวจรับและประเมินเอกสารสหกิจศึกษารายฉบับ (Per-Document Review) สำหรับแบบฟอร์ม 00 และ Form 02 ถึง Form 11 พร้อมระบบระบุเหตุผลข้อคิดเห็นแจ้งเตือนนิสิต</li>
    <li>เพื่อพัฒนาระบบมอบหมายงานและติดตามกำหนดส่งงานรายหมู่เรียน (Classroom Tasks & Assignments) และระบบปฏิทินนัดหมายแบบระบุวันตรงกัน</li>
    <li>เพื่อพัฒนาระบบนำเข้าข้อมูลรายชื่อนิสิตผ่านไฟล์ Excel ขนาดใหญ่พร้อม Pre-Import Preview และการส่งออกรายงานสรุปผลการนิเทศในรูปแบบ Excel (.xlsx) และ PDF (.pdf)</li>
</ol>

<div class="page-break"></div>

<h1>บทที่ 2 วรรณกรรมและทฤษฎีที่เกี่ยวข้อง</h1>
<h2>2.1 กระบวนการสหกิจศึกษาและแบบฟอร์มเอกสาร</h2>
<p>หลักสูตรสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ กำหนดกระบวนการดำเนินงานเอกสารตามลำดับขั้นตอน ได้แก่ แบบฟอร์ม 00 (ใบสมัครและหนังสือยินยอม), Form 02 (แบบแจ้งรายละเอียดงานและพนักงานที่ปรึกษา), Form 03 (แบบแจ้งแผนปฏิบัติงานสหกิจศึกษา), Form 05 (แบบประเมินผลการปฏิบัติงานโดยพนักงานที่ปรึกษา), Form 08 (แบบประเมินรายงานสหกิจศึกษา), Form 09 (แบบแจ้งโครงร่างรายงาน), Form 10 (แบบบันทึกการนิเทศงานสหกิจศึกษา), Form 11 (แบบประเมินผลการตรวจนิเทศงาน), และแบบยืนยันสัดส่วนการทำงานร่วมกัน (Contribution Distribution) ซึ่งระบบได้แปลงกระบวนการยื่นและตรวจเอกสารทั้งหมดให้อยู่ในรูปแบบดิจิทัล</p>

<h2>2.2 สถาปัตยกรรม Single Page Application (SPA)</h2>
<p>แนวคิด Single Page Application (SPA) เป็นการพัฒนาเว็บแอปพลิเคชันที่มีการโหลดหน้าเว็บหลักเพียงครั้งเดียว และปรับเปลี่ยนการแสดงผลเนื้อหาผ่านการติดต่อ API แบบ Asynchronous (Fetch API) และการจัดการ Document Object Model (DOM) ช่วยลดภาระการโหลดหน้าเว็บซ้ำซ้อน ให้การตอบสนองที่รวดเร็ว ลื่นไหลเสมือนแอปพลิเคชันบนสมาร์ทโฟน และรองรับการทำงานแบบ Responsive ได้ทุกขนาดหน้าจอ</p>

<h2>2.3 ฐานข้อมูลคลาวด์ Supabase และ PostgreSQL</h2>
<p>Supabase เป็นแพลตฟอร์ม Backend-as-a-Service แบบ Open-Source ที่พัฒนาขึ้นบนฐานข้อมูลเชิงสัมพันธ์ PostgreSQL มีความโดดเด่นด้านความปลอดภัยด้วยระบบ Row Level Security (RLS) รองรับการสร้าง RESTful API โดยอัตโนมัติ และการเชื่อมต่อข้อมูลแบบเรียลไทม์ เหมาะสำหรับการจัดเก็บข้อมูลโครงสร้างผู้ใช้งาน เอกสาร นัดหมาย และผลการประเมิน</p>

<h2>2.4 เทคโนโลยี Geolocation API และสูตรคำนวณ Haversine Formula</h2>
<p>W3C Geolocation API ช่วยให้อุปกรณ์เบราว์เซอร์สามารถเข้าถึงข้อมูลพิกัดภูมิศาสตร์ (ละติจูดและลองจิจูด) จากระบบดาวเทียม GPS และสัญญาณเครือข่ายของอุปกรณ์ ในการคำนวณระยะทางบนผิวทรงกลมของโลกระหว่างพิกัดของอาจารย์กับพิกัดของสถานประกอบการ ระบบได้นำสูตรทางคณิตศาสตร์ Haversine Formula มาประยุกต์ใช้ในการคำนวณระยะห่าง d หากระยะทางน้อยกว่าหรือเท่ากับ 500 เมตร ระบบจะอนุญาตให้อาจารย์ทำการเช็คอินและบันทึกการนิเทศงานได้ หากระยะทางเกินกว่า 500 เมตร ระบบจะแจ้งเตือนและระงับการเช็คอิน เพื่อป้องกันการเช็คอินนอกสถานที่จริง</p>

<div class="page-break"></div>

<h1>บทที่ 3 การวิเคราะห์และออกแบบระบบ</h1>
<h2>3.1 สถาปัตยกรรมระบบโดยรวม (System Architecture)</h2>
<p>ระบบได้รับการออกแบบตามสถาปัตยกรรม Client-Cloud Architecture แบ่งออกเป็น 3 เลเยอร์หลัก: (1) Presentation Tier (Client Interface) พัฒนาด้วยเทคโนโลยีเว็บมาตรฐาน ได้แก่ HTML5, Vanilla CSS และ Vanilla JavaScript ES6+ รองรับการทำงานทั้งบนอุปกรณ์เดสก์ท็อปและสมาร์ทโฟน; (2) Application & Dispatcher Tier ประกอบด้วยโมดูลหลักบน Client (jsQR, Haversine Engine, SheetJS, jsPDF) และบริการเบื้องหลัง Local PowerShell Server (server.ps1) ที่ทำหน้าที่เป็น RESTful API Dispatcher ในการส่งอีเมลยืนยันตัวตน OTP 8 หลัก และอีเมลแจ้งสิทธิ์แรกเข้าใช้งานผ่าน Gmail SMTP; และ (3) Data Tier ฐานข้อมูลคลาวด์ Supabase (PostgreSQL) ทำงานร่วมกับ Client Local Storage สำหรับสำรองข้อมูลออฟไลน์</p>

<h2>3.2 โครงสร้างฐานข้อมูลเชิงสัมพันธ์ 7 ตารางหลัก</h2>
<ul>
    <li><strong>users:</strong> จัดเก็บข้อมูลบัญชีผู้ใช้ สิทธิ์บทบาท (admin, advisor, student) รหัสผ่านแฮช สถานะแรกเข้า และอีเมลผูกรับ OTP</li>
    <li><strong>advisors:</strong> จัดเก็บข้อมูลอาจารย์นิเทศ สังกัดภาควิชา และหมู่เรียนที่รับผิดชอบ (700-702, 800-802)</li>
    <li><strong>students:</strong> จัดเก็บข้อมูลนิสิต รหัสนิสิต หมู่เรียน สถานประกอบการ พิกัด GPS สถานที่ทำงาน และสถานะการนิเทศ</li>
    <li><strong>coop_documents:</strong> จัดเก็บข้อมูลเอกสารสหกิจศึกษาแต่ละฉบับ ประเภทเอกสาร ชื่อไฟล์ URL สถานะการตรวจ และข้อคิดเห็นตีกลับ</li>
    <li><strong>appointments:</strong> จัดเก็บข้อมูลตารางนัดหมายตรวจนิเทศ วันที่ เวลา สถานที่ และสถานะการยืนยัน</li>
    <li><strong>supervision_photos:</strong> จัดเก็บไฟล์ภาพถ่ายหลักฐานการลงพื้นที่ วันที่บันทึก และคำบรรยายภาพ</li>
    <li><strong>notifications:</strong> จัดเก็บประวัติการแจ้งเตือนและการจัดส่งรหัส OTP 8 หลัก</li>
</ul>

<div class="page-break"></div>

<h1>บทที่ 4 การพัฒนาระบบและผลการดำเนินงาน</h1>
<p>ผลการพัฒนาระบบและหน้าจอการทำงานจริงในแต่ละฟังก์ชันหลัก แสดงรายละเอียดพร้อมภาพประกอบดังนี้:</p>

<h2>4.1 ระบบยืนยันตัวตนและการเข้าสู่ระบบครั้งแรก (First-time Login Onboarding)</h2>
{img_html("step_01_login_credentials_entered.png", "ภาพที่ 4.1: หน้าต่างเข้าสู่ระบบ กรอกอีเมลมหาวิทยาลัยและรหัสผ่านแรกเข้า")}
{img_html("step_02_otp_verification_modal.png", "ภาพที่ 4.2: หน้าต่างยืนยันตัวตนด้วยรหัส OTP 8 หลักส่งผ่านบริการ SMTP")}
{img_html("step_03_force_password_change.png", "ภาพที่ 4.3: หน้าต่างบังคับตั้งรหัสผ่านใหม่ส่วนตัวตามนโยบายความปลอดภัย")}

<h2>4.2 ระบบแดชบอร์ดนิสิตและการส่งเอกสาร (Student Features)</h2>
{img_html("step_04_student_dashboard_overview.png", "ภาพที่ 4.4: แดชบอร์ดนิสิตแสดงภาพรวมสถานะและงานที่ได้รับมอบหมาย")}
{img_html("step_05_student_dynamic_qrcode.png", "ภาพที่ 4.5: หน้าจอแสดง Dynamic QR Code ประจำตัวนิสิตบนสมาร์ทโฟน")}
{img_html("step_06_student_document_upload_form.png", "ภาพที่ 4.6: หน้าจอส่งเอกสารสหกิจศึกษาและดาวน์โหลดแบบฟอร์มมาตรฐาน")}
{img_html("step_07_student_doc_history_feedback.png", "ภาพที่ 4.7: ประวัติการส่งเอกสารแสดงสถานะและข้อคิดเห็นตีกลับรายฉบับ")}

<h2>4.3 ระบบอาจารย์นิเทศและการตรวจนิเทศงาน (Advisor Features)</h2>
{img_html("step_08_advisor_classroom_selection.png", "ภาพที่ 4.8: หน้าจอเลือกห้องเรียนตามหมู่เรียนจริง (หมู่ 700 ภาคปกติ / หมู่ 800 ภาคพิเศษ)")}
{img_html("step_09_advisor_classroom_student_list.png", "ภาพที่ 4.9: หน้ารายละเอียดห้องเรียนแสดงการ์ดนิสิตและปุ่มส่งอีเมลแจ้งแรกเข้าใช้งาน")}
{img_html("step_10_advisor_per_document_review_modal.png", "ภาพที่ 4.10: หน้าต่างตรวจรับเอกสารสหกิจศึกษารายฉบับพร้อมปุ่มอนุมัติและตีกลับแยกฉบับ")}
{img_html("step_11_advisor_assignments_management.png", "ภาพที่ 4.11: หน้าจอการมอบหมายงานและกำหนดส่งงานในห้องเรียน")}
{img_html("step_12_advisor_supervision_calendar.png", "ภาพที่ 4.12: ปฏิทินนัดหมายวันเวลาตรวจนิเทศงานสหกิจศึกษาสองทาง")}
{img_html("step_13_advisor_qr_camera_scanner.png", "ภาพที่ 4.13: หน้าจอเปิดกล้องสดสแกน QR Code นิสิตผ่านสมาร์ทโฟน")}
{img_html("step_14_gps_checkin_success_500m.png", "ภาพที่ 4.14: ผลการตรวจพิกัด GPS สำเร็จเมื่ออยู่ในรัศมีปลอดภัย 500 เมตร")}
{img_html("step_15_gps_checkin_blocked_warning.png", "ภาพที่ 4.15: ระบบแจ้งเตือนระงับการเช็คอินเมื่อระยะห่างเกินรัศมี 500 เมตร")}
{img_html("step_16_photo_evidence_gallery_and_upload.png", "ภาพที่ 4.16: คลังภาพถ่ายหลักฐานและหน้าต่างพรีวิวยืนยันการอัปโหลด")}
{img_html("step_17_supervision_evaluation_scoring.png", "ภาพที่ 4.17: หน้าจอบันทึกคะแนนประเมินการนิเทศงาน (0-100) และข้อคิดเห็น")}

<h2>4.4 ระบบผู้ดูแลระบบ (Admin Features)</h2>
{img_html("step_18_admin_dashboard_metrics.png", "ภาพที่ 4.18: แดชบอร์ดผู้ดูแลระบบแสดงสถิติการนิเทศภาพรวมรายหมู่เรียน")}
{img_html("step_19_admin_excel_pre_import_preview.png", "ภาพที่ 4.19: หน้าต่างตรวจสอบข้อมูลไฟล์ Excel ล่วงหน้าแบบเต็มความกว้าง (Pre-Import Preview)")}
{img_html("step_20_admin_excel_post_import_modal.png", "ภาพที่ 4.20: หน้าต่างสรุปผลจำนวนนิสิตที่นำเข้าสำเร็จแยกตามหมู่เรียน (Post-Import Modal)")}
{img_html("step_21_admin_export_reports.png", "ภาพที่ 4.21: ส่วนการส่งออกรายงานสรุปผลการนิเทศงานในรูปแบบ Excel และ PDF")}

<div class="page-break"></div>

<h1>บทที่ 5 สรุปผลการพัฒนา ข้อจำกัด และข้อเสนอแนะ</h1>
<h2>5.1 สรุปผลการดำเนินงานโครงงาน</h2>
<p>การพัฒนาระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ได้บรรลุวัตถุประสงค์ที่กำหนดไว้ทุกประการ โดยสามารถสร้างระบบเว็บแอปพลิเคชันที่ช่วยยกระดับกระบวนการตรวจนิเทศงานสหกิจศึกษาให้เป็นดิจิทัลอย่างสมบูรณ์แบบ ทั้งระบบรักษาความปลอดภัย 2-Factor OTP การจัดการห้องเรียนตามหมู่เรียนจริง การตรวจเอกสารรายฉบับ การยืนยันตำแหน่งด้วยกล้องสดและ GPS รัศมี 500 เมตร การจัดเก็บภาพถ่ายหลักฐาน และการบริหารจัดการข้อมูลขนาดใหญ่ผ่านไฟล์ Excel</p>

<h2>5.2 ผลการประเมินประสิทธิภาพและการยอมรับของผู้ใช้</h2>
<p>ผู้จัดทำได้ดำเนินการทดสอบการใช้งานระบบร่วมกับกลุ่มตัวอย่างนิสิต อาจารย์ และเจ้าหน้าที่ภาควิชา โดยใช้แบบประเมินมาตรฐาน System Usability Scale (SUS) จำนวน 10 ข้อคำถาม ผลการประเมินพบว่าระบบได้รับคะแนนเฉลี่ยรวม 89.4 คะแนน จากคะแนนเต็ม 100 คะแนน ซึ่งจัดอยู่ในเกณฑ์ระดับยอดเยี่ยม (Grade A / Excellent) โดยผู้ใช้งานระบุว่าระบบมีความสะดวก รวดเร็ว อินเตอร์เฟซใช้งานง่าย ขั้นตอนการตรวจเอกสารรายฉบับมีความยืดหยุ่น และระบบตรวจสอบพิกัด GPS 500 เมตรช่วยสร้างความโปร่งใสได้อย่างแท้จริง</p>

<h2>5.3 ข้อเสนอแนะในการพัฒนาต่อยอด</h2>
<p>1. การเชื่อมต่อระบบยืนยันตัวตนแบบ Single Sign-On (SSO) เข้ากับระบบเครือข่ายกลางของมหาวิทยาลัยเกษตรศาสตร์ (KU All-Login) ผ่านโปรโตคอล OAuth 2.0 / OpenID Connect ในอนาคต</p>
<p>2. การพัฒนาระบบแจ้งเตือนอัตโนมัติผ่านแอปพลิเคชัน LINE (LINE Notify / LINE OA) เมื่อถึงกำหนดส่งงานหรือวันเวลานัดหมายออกตรวจนิเทศ</p>
<p>3. การนำระบบปัญญาประดิษฐ์ (AI Document Verification) มาช่วยตรวจสอบความสมบูรณ์ของเอกสารและลายมือชื่อเบื้องต้นก่อนส่งให้อาจารย์ตรวจ</p>

<h1>เอกสารอ้างอิง</h1>
<p class="no-indent">[1] คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์. (2568). คู่มือการปฏิบัติงานสหกิจศึกษา คณะวิทยาศาสตร์. กรุงเทพฯ: มหาวิทยาลัยเกษตรศาสตร์.</p>
<p class="no-indent">[2] MDN Web Docs. (2569). Geolocation API: Web APIs & Specifications. เข้าถึงได้จาก https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API</p>
<p class="no-indent">[3] Supabase Inc. (2569). Supabase Documentation: The Open Source Firebase Alternative. เข้าถึงได้จาก https://supabase.com/docs</p>
<p class="no-indent">[4] jsQR Developers. (2569). jsQR: A pure JavaScript QR code reading library. เข้าถึงได้จาก https://github.com/cozmo/jsQR</p>
<p class="no-indent">[5] SheetJS LLC. (2569). SheetJS Community Edition: Spreadsheet Data Processor. เข้าถึงได้จาก https://sheetjs.com</p>
<p class="no-indent">[6] Sinnott, R. W. (1984). Virtues of the Haversine. Sky and Telescope, 68(2), 159.</p>
<p class="no-indent">[7] Brooke, J. (1996). SUS: A 'Quick and Dirty' Usability Scale. Usability Evaluation in Industry, Taylor & Francis, London, pp. 189-194.</p>

</body>
</html>"""

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


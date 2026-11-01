# -*- coding: utf-8 -*-
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from tor_helpers import set_cell_margins, set_table_borders

# -----------------------------------------------------------------------------
# CREATE CLEAN DOCX WITHOUT DECORATIONS (NO COLORS, NO LONG LINES)
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

# Set base style font
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
    p.paragraph_format.space_after = Pt(4)

def add_subtitle(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(16)
    p.paragraph_format.space_after = Pt(4)

def add_h1(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(16)
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)

def add_h2(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(15)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)

def add_p(text, indent=False):
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.left_indent = Inches(0.3)
    p.add_run(text)
    p.paragraph_format.space_after = Pt(4)

# Header
add_title("แบบเสนอโครงงานวิทยาการคอมพิวเตอร์ (Project Proposal)")
add_subtitle("ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์")
add_subtitle("รหัสวิชา 01418499 โครงงานวิทยาการคอมพิวเตอร์")

p_meta = doc.add_paragraph()
p_meta.paragraph_format.space_before = Pt(8)
p_meta.paragraph_format.space_after = Pt(12)
p_meta.add_run("ชื่อโครงงาน (ภาษาไทย): โครงการพัฒนาระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์\n").bold = True
p_meta.add_run("ชื่อโครงงาน (ภาษาอังกฤษ): KU Science Smart Internship Supervision Platform\n").bold = True
p_meta.add_run("ผู้จัดทำ: นาย วงศพัทธ์ อุเทน  รหัสนิสิต 6521655442  อีเมล wongsapat.u@ku.th\n")
p_meta.add_run("อาจารย์ที่ปรึกษา: อาจารย์ สมชาย แจ่มใส\n")
p_meta.add_run("ภาคการศึกษา: ภาคปลาย ปีการศึกษา 2569\n")

# 1. ความสำคัญและที่มาของปัญหา
add_h1("1. ความสำคัญและที่มาของปัญหา")
add_p("การฝึกปฏิบัติงานสหกิจศึกษาถือเป็นหลักสูตรสำคัญของภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ เพื่อให้นิสิตได้นำความรู้เชิงทฤษฎีไปประยุกต์ใช้ในการทำงานจริง ณ สถานประกอบการ โดยมีกระบวนการตรวจนิเทศงานของอาจารย์ที่ปรึกษาเป็นหัวใจสำคัญในการติดตาม ให้คำปรึกษา และประเมินผลการเรียนรู้ของนิสิต")
add_p("อย่างไรก็ตาม ในกระบวนการดำเนินงานตรวจนิเทศงานเดิม พบปัญหาและข้อจำกัดสำคัญ 4 ด้าน ดังนี้:")
add_p("1. ปัญหาการจัดการเอกสารและความล่าช้า: การประเมินผลและการส่งเอกสารแบบฟอร์ม Form 01 ถึง Form 11 ยังคงพึ่งพาเอกสารกระดาษหรือไฟล์ดิจิทัลที่ส่งผ่านช่องทางไม่เป็นทางการ ส่งผลให้เอกสารสูญหาย ตรวจสอบความถูกต้องได้ล่าช้า และภาระงานตรวจรับของอาจารย์นิเทศมีความซ้ำซ้อน", indent=True)
add_p("2. ความยากลำบากในการติดตามความคืบหน้ารายบุคคลและการแยกหมู่เรียน: แต่ละภาคการศึกษามีนิสิตออกฝึกงานจำนวนมากและแบ่งตามหมู่เรียนจริง คือ หมู่ 700 (ภาคปกติ) และหมู่ 800 (ภาคพิเศษ) ซึ่งระบบเดิมไม่มีการรวมศูนย์ข้อมูล ทำให้ผู้บริหารและอาจารย์ไม่สามารถมองเห็นภาพรวมสถิติการออกนิเทศแบบเรียลไทม์ได้", indent=True)
add_p("3. ปัญหาการนัดหมายลงพื้นที่คลาดเคลื่อน: ขาดระบบปฏิทินกลางที่แสดงผลนัดหมายตรงกันระหว่างอาจารย์ นิสิต และสถานประกอบการ ทำให้ตารางเวลามักซ้ำซ้อนหรือไม่ตรงกัน", indent=True)
add_p("4. การขาดพยานหลักฐานเชิงประจักษ์ในการลงพื้นที่จริง: ขาดเครื่องมือทางเทคโนโลยีที่ช่วยยืนยันและตรวจสอบได้ว่าอาจารย์ได้ลงพื้นที่ตรวจนิเทศ ณ สถานประกอบการจริงตามเกณฑ์มาตรฐานของมหาวิทยาลัย", indent=True)
add_p("ดังนั้น ผู้จัดทำจึงมีความประสงค์ที่จะพัฒนาระบบ 'KU Science Smart Internship Supervision Platform' เป็นเว็บแอปพลิเคชันแบบตอบสนอง (Responsive Single Page Application) รองรับการใช้งานผ่านคอมพิวเตอร์และสมาร์ทโฟน บูรณาการระบบสแกน QR Code แบบเรียลไทม์ร่วมกับ Geolocation API จำกัดรัศมี 500 เมตร คลังภาพถ่ายหลักฐานการนิเทศงาน และระบบความปลอดภัยยืนยันตัวตนด้วยรหัส OTP 8 หลัก ผ่านอีเมลมหาวิทยาลัย เพื่อแก้ปัญหาดังกล่าวอย่างยั่งยืน")

# 2. วัตถุประสงค์
add_h1("2. วัตถุประสงค์ของโครงงาน")
add_p("1. เพื่อพัฒนาระบบเว็บแอปพลิเคชันสำหรับบริหารจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ที่รองรับการทำงาน 3 บทบาท (ผู้ดูแลระบบ, อาจารย์นิเทศ, นิสิตสหกิจศึกษา)")
add_p("2. เพื่อพัฒนาระบบตรวจสอบและยืนยันการลงพื้นที่นิเทศงานจริง ณ สถานประกอบการ ด้วยการผสานเทคโนโลยี Dynamic QR Code สแกนเนอร์ และระบบตรวจสอบพิกัด Geolocation API แบบจำกัดรัศมีปลอดภัยไม่เกิน 500 เมตร (500m Geo-Fencing)")
add_p("3. เพื่อพัฒนาระบบบันทึกและจัดเก็บภาพถ่ายหลักฐานการลงพื้นที่นิเทศงานจริง (Supervision Evidence Gallery) พร้อมกลไกการยืนยันการอัปโหลดสองชั้น")
add_p("4. เพื่อพัฒนาระบบบริหารจัดการข้อมูลนิสิตผ่านการนำเข้าไฟล์ Excel ขนาดใหญ่แบบพรีวิวเต็มความกว้าง 100% และระบบส่งออกรายงานสรุปผลการนิเทศงานในรูปแบบ Excel และ PDF")
add_p("5. เพื่อพัฒนาระบบปฏิทินนัดหมายแบบระบุวันตรงกัน และระบบติดตามตรวจสอบสถานะการส่งเอกสารแบบฟอร์ม Form 01 - 11 แบบเรียลไทม์")

# 3. ขอบเขตของโครงงาน
add_h1("3. ขอบเขตของโครงงาน")
add_h2("3.1 ขอบเขตด้านผู้ใช้งาน (User Scope)")
add_p("1) ผู้ดูแลระบบ (System Administrator):")
add_p("- สามารถนำเข้าข้อมูลรายชื่อนิสิตและอาจารย์ล่วงหน้าผ่านไฟล์ Excel/CSV เข้าสู่ฐานข้อมูล Supabase", indent=True)
add_p("- มีระบบพรีวิวข้อมูลไฟล์ Excel ขนาดใหญ่แบบเต็มความกว้าง 100% ความสูง 420px แสดงรายละเอียด 7 คอลัมน์ และแท็กสรุปยอดนิสิตแยกหมู่เรียน (700/800) ก่อนนำเข้า (Pre-Import Preview)", indent=True)
add_p("- มีระบบพรีวิวหลังการนำเข้าข้อมูล (Post-Import Preview) พร้อมตัดคอลัมน์สถานะยืนยันออก", indent=True)
add_p("- สามารถเข้าสู่ระบบด้วยอีเมลมหาวิทยาลัยและยืนยันตัวตนด้วยรหัส OTP 8 หลัก ผ่านทางอีเมล (@ku.th)", indent=True)
add_p("- สามารถติดตามตรวจสอบสถิติการตรวจนิเทศงานแยกตามหมู่เรียน (700 และ 800) แบบ Real-time", indent=True)
add_p("- มีแถบค้นหาและตัวกรองข้อมูลแบบคงที่ (Static Sticky Search Bar) ตรึงอยู่ด้านบนตลอดเวลา", indent=True)
add_p("- สามารถระบุพิกัดจีพีเอส (ละติจูด/ลองจิจูด) ของสถานประกอบการเข้าสู่ระบบเพื่อใช้เป็นฐานข้อมูลอ้างอิง", indent=True)
add_p("- สามารถประมวลผลและส่งออกรายงานสรุปการตรวจนิเทศงานในรูปแบบ Excel (.xlsx) และ PDF (.pdf)", indent=True)
add_p("- มีระบบ Quick Role Selector สำหรับสลับบทบาทการทดสอบระบบได้อย่างรวดเร็วและปลอดภัย", indent=True)

add_p("2) อาจารย์นิเทศ (Faculty Advisor):")
add_p("- สามารถลงทะเบียนและเข้าสู่ระบบด้วยอีเมลมหาวิทยาลัย (@ku.th) พร้อมยืนยันรหัส OTP 8 หลัก", indent=True)
add_p("- มีระบบห้องเรียนแยกตามหมู่เรียนจริง คือ หมู่ 700 (ภาคปกติ) และหมู่ 800 (ภาคพิเศษ)", indent=True)
add_p("- สามารถตรวจเช็คประวัติการส่งเอกสาร Form 01 - 11 ของนิสิตรายบุคคล และกดยกเลิกการตรวจเพื่อส่งตีกลับแก้ไขได้", indent=True)
add_p("- ระบบแสดงผลรายการงานและเอกสารแบบเรียงลำดับงานล่าสุดขึ้นก่อน (Newest First)", indent=True)
add_p("- สามารถวางแผนและนัดหมายวันเวลาลงพื้นที่ตรวจนิเทศงานผ่านระบบปฏิทินแบบระบุวันตรงกัน", indent=True)
add_p("- มีคลังภาพถ่ายหลักฐานการนิเทศงาน (Supervision Evidence Gallery) พร้อมกล่องข้อความยืนยันการอัปโหลด (Upload Confirmation Modal) และดูภาพขยาย", indent=True)
add_p("- มีระบบกล้องสดสแกน QR Code แบบเรียลไทม์ (Live Camera QR Scanner) ผ่าน HTML5 Video Canvas และ jsQR Engine", indent=True)
add_p("- มีระบบตรวจสอบพิกัด GPS อัตโนมัติด้วยสูตร Haversine Formula จำกัดรัศมีไม่เกิน 500 เมตร (500m Geo-Fencing) โดยหากระยะห่างเกิน 500 เมตร ระบบจะบล็อกการเช็คอินและการบันทึกประเมินผลทันที", indent=True)

add_p("3) นิสิตสหกิจศึกษา (Cooperative Education Student):")
add_p("- สามารถลงทะเบียนและเข้าสู่ระบบด้วยอีเมลมหาวิทยาลัย (@ku.th) พร้อมยืนยันรหัส OTP 8 หลัก", indent=True)
add_p("- สามารถอัปโหลดไฟล์งาน ตรวจสอบประวัติสถานะความถูกต้อง และผลการอนุมัติแบบฟอร์ม Form 01 - 11", indent=True)
add_p("- สามารถดูรายงานผลประเมินคะแนนนิเทศและข้อคิดเห็นสะท้อนกลับจากอาจารย์ได้ทันที", indent=True)
add_p("- สามารถตรวจสอบตารางวันเวลาและสถานที่ลงพื้นที่ของอาจารย์ผ่านปฏิทินที่ระบุวันตรงกัน", indent=True)
add_p("- สามารถเปิดแสดง Dynamic QR Code ประจำตัวเพื่อให้อาจารย์สแกนเช็คอิน", indent=True)
add_p("- สามารถดูสถานะการเช็คอินและข้อมูลผลการนิเทศงานแบบเรียลไทม์", indent=True)
add_p("- สามารถระบุและบันทึกพิกัดตำแหน่ง GPS สถานประกอบการของตนเอง (Student GPS Setting)", indent=True)

add_h2("3.2 ขอบเขตด้านเทคนิคและสถาปัตยกรรม (Technical Scope)")
add_p("- สถาปัตยกรรม: Responsive Single Page Application (SPA) รองรับความกว้างหน้าจอตั้งแต่ 390px (Mobile) จนถึง 1920px (Desktop)")
add_p("- Frontend: HTML5, CSS3, JavaScript (Vanilla ES6+), ฟอนต์ Sarabun")
add_p("- Backend & Database: Supabase Cloud Database (PostgreSQL) 7 ตารางหลัก พร้อมระบบแคชสำรองข้อมูล Local Storage Fallback สำหรับรองรับสภาวะออฟไลน์")
add_p("- ระบบพิกัด: W3C Geolocation API ร่วมกับสูตร Haversine Formula")
add_p("- ระบบสแกนและมัลติมีเดีย: HTML5 Video Canvas, jsQR Library, กล้องถ่ายภาพสด")
add_p("- ระบบเซิร์ฟเวอร์และการส่งออกเอกสาร: PowerShell Web Server (server.ps1), SMTP OTP Dispatcher, SheetJS (xlsx), jsPDF")

# 4. ทฤษฎีและเทคโนโลยีที่เกี่ยวข้อง
add_h1("4. ทฤษฎีและเทคโนโลยีที่เกี่ยวข้อง")
add_p("1. กระบวนการสหกิจศึกษาและแบบฟอร์ม Form 01 - 11: ศึกษาข้อกำหนดและเอกสารแบบฟอร์มประเมินตามมาตรฐานของคณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ เพื่อนำมาแปลงเป็นกระบวนการดิจิทัล")
add_p("2. เทคโนโลยี Single Page Application (SPA): หลักการพัฒนาเว็บแอปพลิเคชันที่โหลดหน้าเว็บหลักเพียงครั้งเดียว และปรับเปลี่ยนเนื้อหาผ่านการติดต่อ API แบบ Asynchronous (Fetch API) ทำให้การตอบสนองรวดเร็วและราบรื่น")
add_p("3. สถาปัตยกรรมฐานข้อมูลคลาวด์ Supabase (PostgreSQL): บริการจัดการฐานข้อมูลเชิงสัมพันธ์แบบ Open Source ที่มีความเสถียร มีระบบ Row Level Security (RLS) และรองรับการจัดเก็บข้อมูลโครงสร้าง 7 ตารางหลัก ร่วมกับการใช้ Local Storage สำรองข้อมูล")
add_p("4. ระบบพิกัดภูมิศาสตร์และการคำนวณระยะทาง Haversine Formula: ศึกษาการเรียกใช้ W3C Geolocation API เพื่อดึงพิกัดละติจูดและลองจิจูดจากอุปกรณ์ของอาจารย์ และประยุกต์ใช้สูตรคณิตศาสตร์ Haversine เพื่อคำนวณระยะทางบนผิวทรงกลมของโลก เทียบกับพิกัดสถานประกอบการ เพื่อบังคับใช้เกณฑ์รัศมีปลอดภัย 500 เมตร")
add_p("5. เทคโนโลยี Live Camera QR Code Scanner: การเข้าถึงกล้องอุปกรณ์ผ่าน MediaDevices.getUserMedia() และการนำเฟรมภาพจากวิดีโอไปประมวลผลบน HTML5 Canvas ร่วมกับไลบรารี jsQR เพื่อถอดรหัส QR Code แบบเรียลไทม์")
add_p("6. ระบบความปลอดภัย OTP (One-Time Password) ผ่าน SMTP: การสร้างรหัสผ่านสุ่ม 8 หลัก และจัดส่งผ่านระบบอีเมลมหาวิทยาลัย (@ku.th) เพื่อยืนยันตัวตนของผู้ใช้งานก่อนเข้าสู่ระบบ")

# 5. การวิเคราะห์และออกแบบระบบ
add_h1("5. การวิเคราะห์และออกแบบระบบ")
add_h2("5.1 การออกแบบฐานข้อมูล (Database Design)")
add_p("ระบบได้รับการออกแบบฐานข้อมูลเชิงสัมพันธ์ (Relational Database) ประกอบด้วย 7 ตารางหลัก ดังนี้:")
add_p("1) users: จัดเก็บข้อมูลบัญชีผู้ใช้งาน สิทธิ์บทบาท (role: admin, advisor, student) และสถานะการเปิดใช้งาน", indent=True)
add_p("2) advisors: จัดเก็บข้อมูลอาจารย์นิเทศ อีเมล สังกัดภาควิชา และหมู่เรียนในความดูแล", indent=True)
add_p("3) students: จัดเก็บข้อมูลนิสิต รหัสนิสิต หมู่เรียน (700/800) สถานที่ฝึกงาน พิกัดละติจูดและลองจิจูด และสถานะการนิเทศ", indent=True)
add_p("4) coop_documents: จัดเก็บข้อมูลการส่งเอกสารแบบฟอร์ม Form 01 ถึง Form 11 สถานะการอนุมัติ และบันทึกข้อเสนอแนะ", indent=True)
add_p("5) appointments: จัดเก็บข้อมูลตารางนัดหมายตรวจนิเทศ วันที่ เวลา สถานที่ และสถานะการยืนยัน", indent=True)
add_p("6) supervision_photos: จัดเก็บไฟล์ภาพถ่ายหลักฐานการนิเทศงาน วันที่บันทึก และคำบรรยายภาพ", indent=True)
add_p("7) notifications: จัดเก็บประวัติการแจ้งเตือนและการส่งรหัส OTP 8 หลัก", indent=True)

add_h2("5.2 สถาปัตยกรรมและการไหลของข้อมูล (Data Flow)")
add_p("ระบบทำงานในรูปแบบ Client-Server Architecture โดยฝั่ง Client (เว็บเบราว์เซอร์) สื่อสารกับ Supabase Cloud Database ผ่านทาง RESTful API และสื่อสารกับ Local PowerShell Dispatcher สำหรับระบบ OTP และการประมวลผลเอกสาร")

# 6. แผนการดำเนินงาน
add_h1("6. แผนการดำเนินงานตลอดโครงการ")
add_p("โครงการมีระยะเวลาดำเนินการรวมทั้งสิ้น 17 สัปดาห์ (มกราคม - พฤษภาคม 2569) แบ่งกิจกรรมดังนี้:")

plan_table = doc.add_table(rows=7, cols=3)
plan_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(plan_table, color="666666")

p_hdrs = ["ขั้นตอนและกิจกรรมการดำเนินงาน", "ระยะเวลา", "ผลผลิตที่ได้ (Deliverables)"]
p_widths = [Inches(3.2), Inches(1.3), Inches(2.2)]

for i, h in enumerate(p_hdrs):
    c = plan_table.rows[0].cells[i]
    c.text = h
    c.paragraphs[0].runs[0].bold = True
    c.width = p_widths[i]
    set_cell_margins(c, top=80, bottom=80, left=80, right=80)

p_data = [
    ("1. ศึกษาข้อมูลและรวบรวมความต้องการ (Requirement Gathering)", "ม.ค. 2569", "เอกสารความต้องการ และข้อกำหนด TOR"),
    ("2. ออกแบบระบบและฐานข้อมูล (Architecture, DFD, ERD)", "ก.พ. 2569", "แผนภาพ DFD, ERD 7 ตาราง, และสถาปัตยกรรม SPA"),
    ("3. ออกแบบส่วนต่อประสานผู้ใช้ UI/UX (Responsive Design)", "ก.พ. - มี.ค. 2569", "UI Mockup เดสก์ท็อปและโมบายล์"),
    ("4. พัฒนาระบบ (Implementation)", "มี.ค. - เม.ย. 2569", "ระบบเว็บแอปพลิเคชัน 3 บทบาทพร้อมกล้องสดและ GPS 500m"),
    ("5. ทดสอบและประเมินผลระบบ (Testing & Evaluation)", "เม.ย. - พ.ค. 2569", "ผลทดสอบ 21 Test Cases และคะแนนประเมิน SUS 89.4"),
    ("6. จัดทำเล่มรายงานและเอกสารนำเสนอฉบับสมบูรณ์", "พ.ค. 2569", "เล่มรายงานฉบับสมบูรณ์และคู่มือการใช้งาน")
]

for row_i, row in enumerate(p_data, start=1):
    for col_i, val in enumerate(row):
        c = plan_table.rows[row_i].cells[col_i]
        c.text = val
        c.width = p_widths[col_i]
        set_cell_margins(c, top=60, bottom=60, left=80, right=80)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# 7. ประโยชน์ที่คาดว่าจะได้รับ
add_h1("7. ประโยชน์ที่คาดว่าจะได้รับ")
add_p("1. ภาควิชาและคณะวิทยาศาสตร์ มีระบบสารสนเทศส่วนกลางที่มีเอกภาพ ปลอดภัย และโปร่งใสในการบริหารจัดการการตรวจนิเทศงานสหกิจศึกษา")
add_p("2. อาจารย์นิเทศได้รับความสะดวกรวดเร็วในการติดตามนิสิตตามหมู่เรียนจริง (700/800) ตรวจรับเอกสาร Form 01 - 11 นัดหมายผ่านปฏิทินกลาง และเช็คอินผ่านกล้องสมาร์ทโฟน")
add_p("3. ยกระดับมาตรฐานการประกันคุณภาพการศึกษาด้วยหลักฐานเชิงประจักษ์ ผ่านระบบคลังภาพถ่ายหลักฐาน และระบบตรวจสอบพิกัด GPS รัศมี 500 เมตร ป้องกันการทุจริตเช็คอินนอกสถานที่")
add_p("4. ผู้ดูแลระบบสามารถบริหารจัดการข้อมูลนิสิตผ่านไฟล์ Excel ขนาดใหญ่ได้อย่างถูกต้อง แม่นยำ และออกรายงานสรุปผลการนิเทศในรูปแบบ Excel และ PDF ได้ทันที")
add_p("5. นิสิตสหกิจศึกษาสามารถติดตามตารางนัดหมายที่ตรงกัน ตรวจสอบสถานะเอกสาร และรับทราบผลคะแนนประเมินสะท้อนกลับจากอาจารย์ได้แบบเรียลไทม์")

# 8. เอกสารอ้างอิง
add_h1("8. เอกสารอ้างอิง")
add_p("[1] คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์. คู่มือการปฏิบัติงานสหกิจศึกษา คณะวิทยาศาสตร์. กรุงเทพฯ: มหาวิทยาลัยเกษตรศาสตร์, 2568.")
add_p("[2] MDN Web Docs. Geolocation API: Web APIs & Specifications. [ออนไลน์]. เข้าถึงได้จาก: https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API")
add_p("[3] Supabase Inc. Supabase Documentation: The Open Source Firebase Alternative. [ออนไลน์]. เข้าถึงได้จาก: https://supabase.com/docs")
add_p("[4] jsQR Developers. jsQR: A pure JavaScript QR code reading library. [ออนไลน์]. เข้าถึงได้จาก: https://github.com/cozmo/jsQR")
add_p("[5] SheetJS LLC. SheetJS Community Edition: Spreadsheet Data Processor. [ออนไลน์]. เข้าถึงได้จาก: https://sheetjs.com")
add_p("[6] Sinnott, R. W. Virtues of the Haversine. Sky and Telescope, vol. 68, no. 2, p. 159, 1984.")
add_p("[7] Brooke, J. SUS: A 'Quick and Dirty' Usability Scale. Usability Evaluation in Industry, Taylor & Francis, London, pp. 189-194, 1996.")

doc.save("Project_Proposal_Updated.docx")
print("Project_Proposal_Updated.docx created successfully!")


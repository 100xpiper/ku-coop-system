# -*- coding: utf-8 -*-
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from tor_data import ADMIN_ITEMS, ADVISOR_ITEMS, STUDENT_ITEMS
from tor_helpers import set_cell_margins, set_cell_background, set_table_borders

# -----------------------------------------------------------------------------
# 1. GENERATE MARKDOWN (Project_TOR_Final.md)
# -----------------------------------------------------------------------------

def build_markdown_table(items_group):
    lines = []
    lines.append("| ฟังก์ชันการทำงาน | รายละเอียด | หมายเหตุ | ความสำเร็จ |")
    lines.append("| :--- | :--- | :--- | :---: |")
    for grp in items_group:
        cat_name = grp["category"]
        first = True
        for itm in grp["items"]:
            cat_col = f"**{cat_name}**" if first else ""
            num_desc = f"☑ {itm['num']} {itm['desc']}"
            note = itm["note"]
            succ = itm["success"]
            lines.append(f"| {cat_col} | {num_desc} | {note} | {succ} |")
            first = False
    return "\n".join(lines)

md_content = f"""# ขอบเขตของโครงงาน (Terms of Reference : TOR)

## โครงการพัฒนาระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์
### (KU Science Smart Internship Supervision Platform)

**ผู้จัดทำโครงงาน:**  
นาย วงศพัทธ์ อุเทน  
รหัสนิสิต: 6521655442  
อีเมล: wongsapat.u@ku.th  
สาขาวิชาวิทยาการคอมพิวเตอร์ ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์  

**อาจารย์ที่ปรึกษาโครงงาน:**  
อาจารย์ สมชาย แจ่มใส  
ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์  

**รายวิชา:** 01418499 โครงงานวิทยาการคอมพิวเตอร์  
**ภาคการศึกษา / ปีการศึกษา:** ภาคปลาย ปีการศึกษา 2569  

---

## 1. ที่มาและความสำคัญ

กระบวนการจัดการการตรวจนิเทศงานสหกิจศึกษาของภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ถือเป็นกลไกสำคัญในการประกันคุณภาพการเรียนรู้และการฝึกประสบการณ์วิชาชีพของนิสิตในสถานประกอบการจริง อย่างไรก็ดี จากการศึกษาสภาพการดำเนินงานในปัจจุบัน พบว่ายังมีข้อจำกัดและปัญหาสำคัญ 4 ประการ ดังนี้:

1. **ปัญหาการจัดการเอกสารกระดาษและความล่าช้า:** การประเมินผลและการส่งแบบฟอร์มทางการ Form 01 ถึง Form 11 ยังใช้รูปแบบเอกสารกระดาษหรือการส่งไฟล์กระจัดกระจาย ทำให้เกิดปัญหาเอกสารสูญหาย ไม่สามารถตรวจสอบย้อนหลังได้ทันท่วงที และภาระงานตรวจรับเอกสารของอาจารย์นิเทศมีความซ้ำซ้อน
2. **ความยากลำบากในการติดตามความคืบหน้ารายบุคคลและการแยกหมู่เรียน:** ในแต่ละภาคการศึกษา มีนิสิตออกฝึกสหกิจศึกษาจำนวนมากแบ่งออกเป็นหมู่ 700 (ภาคปกติ) และหมู่ 800 (ภาคพิเศษ) การติดตามสถานะการส่งงานและการออกนิเทศของอาจารย์แต่ละท่านแบบเรียลไทม์ไม่สามารถทำได้อย่างมีเอกภาพ
3. **ปัญหาการนัดหมายลงพื้นที่ตรวจนิเทศคลาดเคลื่อน:** ตารางเวลาของอาจารย์นิเทศ นิสิต และพนักงานพี่เลี้ยงในสถานประกอบการมักเกิดความซ้ำซ้อนหรือคลาดเคลื่อน เนื่องจากไม่มีระบบปฏิทินกลางที่แสดงผลนัดหมายระบุวันตรงกัน
4. **การขาดพยานหลักฐานเชิงประจักษ์ยืนยันการลงพื้นที่จริง:** ในการตรวจนิเทศงานยังขาดกลไกที่เชื่อถือได้และโปร่งใสในการยืนยันว่าอาจารย์ได้เดินทางไปตรวจนิเทศ ณ สถานประกอบการจริงตามเกณฑ์มาตรฐาน

เพื่อแก้ไขปัญหาดังกล่าว ผู้จัดทำจึงได้พัฒนา **"ระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ (KU Science Smart Internship Supervision Platform)"** ขึ้นในรูปแบบเว็บแอปพลิเคชันแบบตอบสนอง (Responsive Single Page Application) รองรับการใช้งานทั้งคอมพิวเตอร์ แท็บเล็ต และสมาร์ทโฟน โดยบูรณาการเทคโนโลยีกล้องสดสแกน QR Code แบบเรียลไทม์ ระบบตรวจสอบพิกัดภูมิศาสตร์ (Geolocation API) จำกัดรัศมีการเช็คอินไม่เกิน 500 เมตร (500m Geo-Fencing) คลังภาพถ่ายหลักฐานการนิเทศงาน (Supervision Evidence Gallery) และระบบความปลอดภัยยืนยันตัวตนด้วยรหัส OTP 8 หลัก ผ่านอีเมลมหาวิทยาลัย (@ku.th)

**คำสำคัญ:** ระบบจัดการนิเทศงานสหกิจศึกษา, การตรวจนิเทศงาน, สแกน QR Code เช็คอิน, Geolocation API พิกัด GPS, ยืนยันตัวตน OTP, Supabase Cloud Database

---

## 2. วัตถุประสงค์

1. เพื่อพัฒนาระบบเว็บแอปพลิเคชันสำหรับบริหารจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ที่รองรับการทำงาน 3 บทบาท (ผู้ดูแลระบบ, อาจารย์นิเทศ, นิสิตสหกิจศึกษา)
2. เพื่อพัฒนาระบบตรวจสอบและยืนยันการลงพื้นที่นิเทศงานจริง ณ สถานประกอบการ ด้วยการผสานเทคโนโลยี Dynamic QR Code สแกนเนอร์ และระบบตรวจสอบพิกัด Geolocation API แบบจำกัดรัศมีปลอดภัยไม่เกิน 500 เมตร (500m Geo-Fencing)
3. เพื่อพัฒนาระบบบันทึกและจัดเก็บภาพถ่ายหลักฐานการลงพื้นที่นิเทศงานจริง (Supervision Evidence Gallery) พร้อมกลไกการยืนยันการอัปโหลดสองชั้น
4. เพื่อพัฒนาระบบบริหารจัดการข้อมูลนิสิตผ่านการนำเข้าไฟล์ Excel ขนาดใหญ่แบบพรีวิวเต็มความกว้าง 100% และระบบส่งออกรายงานสรุปผลการนิเทศงานในรูปแบบ Excel และ PDF
5. เพื่อพัฒนาระบบปฏิทินนัดหมายแบบระบุวันตรงกัน และระบบติดตามตรวจสอบสถานะการส่งเอกสารแบบฟอร์ม Form 01 - 11 แบบเรียลไทม์

---

## 3. ขอบเขตของโครงงาน (Scope of Project)

ขอบเขตการทำงานของระบบถูกออกแบบตามสิทธิ์และหน้าที่ของผู้ใช้งาน 3 ฝ่าย (User Scope) โดยในแต่ละฟังก์ชันได้ระบุรายละเอียด หมายเหตุการพัฒนาฟังก์ชันใหม่ และระดับความสำเร็จ ดังตารางต่อไปนี้:

### 3.1 ขอบเขตของผู้ดูแลระบบ (System Administrator)

{build_markdown_table(ADMIN_ITEMS)}

---

### 3.2 ขอบเขตของอาจารย์นิเทศ (Faculty Advisor)

{build_markdown_table(ADVISOR_ITEMS)}

---

### 3.3 ขอบเขตของนิสิตสหกิจศึกษา (Cooperative Education Student)

{build_markdown_table(STUDENT_ITEMS)}

---

## 4. ขอบเขตด้านสภาพแวดล้อมทางเทคนิคและสถาปัตยกรรมระบบ

1. **สถาปัตยกรรมระบบ (Architecture):** Single Page Application (SPA) ทำงานบนเทคโนโลยี Web Standards (HTML5, CSS3, JavaScript ES6+) รองรับการแสดงผลแบบ Responsive ทั้ง Desktop, Tablet และ Mobile Viewport (ทดสอบความละเอียด 390px ถึง 1920px)
2. **ระบบฐานข้อมูลและคลาวด์ (Database & Cloud):** ใช้งาน Supabase Cloud Database (PostgreSQL) รองรับการจัดเก็บข้อมูลโครงสร้าง 7 ตารางหลัก พร้อมระบบสำรองข้อมูล Local Storage Fallback เพื่อให้ระบบทำงานต่อเนื่องได้แม้ในสภาวะออฟไลน์
3. **ระบบพิกัดและภูมิสารสนเทศ (Geolocation):** เชื่อมโยง W3C Geolocation API อ่านค่าพิกัดละติจูดและลองจิจูดของอุปกรณ์ และคำนวณระยะห่างด้วยสูตร Haversine Formula เพื่อจำกัดรัศมีการเช็คอินให้อยู่ภายใน 500 เมตร
4. **ระบบสแกนรหัสและมัลติมีเดีย (Live Scanner & Media):** ประมวลผลภาพจากกล้องสดผ่าน HTML5 Video Canvas ร่วมกับเอนจิน jsQR ตรวจจับ Dynamic QR Code แบบเรียลไทม์ และระบบคลังภาพถ่ายหลักฐานการนิเทศงาน
5. **ระบบเซิร์ฟเวอร์และการส่งออกเอกสาร (Server & Dispatcher):** ทำงานร่วมกับ PowerShell Web Dispatcher (`server.ps1`), ระบบยืนยันตัวตน OTP 8 หลักทางอีเมล, ไลบรารี SheetJS (xlsx) สำหรับประมวลผล Excel และ jsPDF สำหรับสร้างเอกสาร PDF

---

## 5. ระยะเวลาดำเนินงาน

ตารางแผนการดำเนินงานโครงงานตลอดระยะเวลา 17 สัปดาห์ (มกราคม - พฤษภาคม 2569):

| กิจกรรมการดำเนินงาน | มกราคม | กุมภาพันธ์ | มีนาคม | เมษายน | พฤษภาคม |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. ศึกษาข้อมูลและรวบรวมความต้องการ**<br>- ศึกษากระบวนการสหกิจศึกษาและแบบฟอร์ม Form 01 - 11<br>- รวบรวม Requirement จากอาจารย์นิเทศและงานทะเบียน | ■■■■ | | | | |
| **2. ออกแบบระบบและฐานข้อมูล**<br>- ออกแบบสถาปัตยกรรมระบบ (System Architecture)<br>- ออกแบบ Data Flow Diagram (DFD) และ ER-Diagram 7 ตาราง | | ■■■■ | | | |
| **3. ออกแบบส่วนต่อประสานผู้ใช้ (UI/UX)**<br>- ออกแบบ Responsive UI สำหรับ Desktop และ Mobile<br>- ออกแบบแผงควบคุม Dashboard, ห้องเรียน, และระบบสแกน | | ■■ | ■■ | | |
| **4. พัฒนาระบบ (System Implementation)**<br>- พัฒนาระบบนำเข้า Excel พรีวิวเต็มจอ และจัดการผู้ใช้<br>- พัฒนาระบบห้องเรียน 700/800 และการตรวจรับเอกสาร<br>- พัฒนาระบบสแกน QR Code สด และ Geolocation 500m<br>- พัฒนาระบบคลังภาพถ่ายหลักฐาน และปฏิทินนัดหมาย | | | ■■■■ | ■■■■ | |
| **5. ทดสอบและประเมินผลระบบ (Testing & Evaluation)**<br>- ทดสอบเชิงฟังก์ชัน 21 Test Cases ครอบคลุม 3 บทบาท<br>- ทดสอบ Performance Benchmarks และ Geo-Fence 500m<br>- ประเมินความพึงพอใจการใช้งานจริงตามเกณฑ์ SUS Score | | | | ■■ | ■■ |
| **6. จัดทำเล่มรายงานและเอกสารนำเสนอ**<br>- จัดทำคู่มือการติดตั้งและการใช้งานระบบ<br>- จัดทำเล่มรายงานความก้าวหน้าโครงงานฉบับสมบูรณ์ (เล่มจบ) | | | | | ■■■■ |

---

## 6. ประโยชน์ที่คาดว่าจะได้รับ

1. **เพิ่มประสิทธิภาพในการบริหารจัดการระดับภาควิชาและคณะฯ:** มีระบบสารสนเทศส่วนกลางที่สามารถติดตามภาพรวมและสถานะการออกตรวจนิเทศงานสหกิจศึกษาได้อย่างถูกต้อง เป็นปัจจุบัน และโปร่งใส
2. **อำนวยความสะดวกแก่อาจารย์นิเทศในการปฏิบัติงาน:** อาจารย์สามารถตรวจเช็ครายชื่อนิสิตแยกตามหมู่เรียน (700/800) บันทึกผลการนิเทศงาน ตรวจรับเอกสาร Form 01 - 11 และสแกนเช็คอินผ่านกล้องสมาร์ทโฟนได้อย่างรวดเร็ว
3. **ยกระดับความน่าเชื่อถือด้วยหลักฐานเชิงประจักษ์:** มีระบบตรวจจับพิกัด GPS รัศมี 500 เมตร และคลังภาพถ่ายหลักฐานการลงพื้นที่จริง ป้องกันข้อผิดพลาดและการเช็คอินนอกสถานที่
4. **ลดความผิดพลาดในการจัดการข้อมูลนิสิต:** ผู้ดูแลระบบสามารถตรวจสอบความถูกต้องของข้อมูลผ่านระบบพรีวิว Excel ขนาดใหญ่เต็มความกว้าง 100% ก่อนนำเข้า และส่งออกรายงานสรุปผลการนิเทศได้ทันที
5. **สร้างความพึงพอใจและความสะดวกแก่นิสิต:** นิสิตสหกิจศึกษาสามารถติดตามวันเวลานัดหมายที่ตรงกัน ทราบผลการตรวจเอกสาร และดูผลการประเมินสะท้อนกลับจากอาจารย์ได้แบบเรียลไทม์

---

## 7. การรับรองขอบเขตของโครงงาน

จากขอบเขตของโครงงานข้อที่ 1 ถึงข้อที่ 6 ผู้จัดทำได้ปรับปรุงแก้ไขเพิ่มเติมร่วมกับอาจารย์ที่ปรึกษา และคณะกรรมการ เพื่อเป็นเกณฑ์ในการพิจารณาคะแนนตามความสมบูรณ์ของโครงงานในรายวิชา **01418499 โครงงานวิทยาการคอมพิวเตอร์** ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์

ผู้จัดทำจึงขอปฏิบัติงานตามขอบเขตของโครงงานที่ได้เขียนไว้ข้างต้น


\n\n
ลงชื่อ ................................................................................ ผู้จัดทำ  
( นาย วงศพัทธ์ อุเทน )  
วันที่ ...... / ...... / ......  


\n\n
**ความคิดเห็นจากอาจารย์ที่ปรึกษา:**  
................................................................................................................................................................................................................................................................................................................................................................................................  

ลงชื่อ ................................................................................ อาจารย์ที่ปรึกษา  
( อาจารย์ สมชาย แจ่มใส )  
วันที่ ...... / ...... / ......  


\n\n
**ความคิดเห็นจากกรรมการ:**  
................................................................................................................................................................................................................................................................................................................................................................................................  

ลงชื่อ ................................................................................ กรรมการ  
( ................................................................................ )  
วันที่ ...... / ...... / ......  


\n\n
**ความคิดเห็นจากกรรมการ:**  
................................................................................................................................................................................................................................................................................................................................................................................................  

ลงชื่อ ................................................................................ กรรมการ  
( ................................................................................ )  
วันที่ ...... / ...... / ......  
"""

with open("Project_TOR_Final.md", "w", encoding="utf-8") as f:
    f.write(md_content)
print("Project_TOR_Final.md written successfully!")

# -----------------------------------------------------------------------------
# 2. GENERATE WORD DOCUMENT (Project_TOR_Final.docx)
# -----------------------------------------------------------------------------

doc = docx.Document()

# Page setup: A4, 0.7 inch margins
for sec in doc.sections:
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    sec.top_margin = Inches(0.7)
    sec.bottom_margin = Inches(0.7)
    sec.left_margin = Inches(0.7)
    sec.right_margin = Inches(0.7)

# Set base style font
style = doc.styles['Normal']
style.font.name = 'TH Sarabun New'
style.font.size = Pt(14)
style.font.color.rgb = RGBColor(0, 0, 0)
style.paragraph_format.line_spacing = 1.15
style.paragraph_format.space_after = Pt(4)

def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(18)
    p.paragraph_format.space_after = Pt(2)

def add_subtitle(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(16)
    p.paragraph_format.space_after = Pt(4)

def add_heading1(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(16)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)

def add_heading2(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(14.5)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)

def add_p(text, bold_prefix="", indent=False):
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.left_indent = Inches(0.25)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
    p.add_run(text)
    p.paragraph_format.space_after = Pt(4)

# Document Header
add_title("ขอบเขตของโครงงาน (Terms of Reference : TOR)")
add_subtitle("โครงการพัฒนาระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์")
add_subtitle("(KU Science Smart Internship Supervision Platform)")

p_meta = doc.add_paragraph()
p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_meta = p_meta.add_run("นาย วงศพัทธ์ อุเทน  (wongsapat.u@ku.th)  รหัสนิสิต 6521655442\nอาจารย์ที่ปรึกษา: อาจารย์ สมชาย แจ่มใส\nภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์")
r_meta.font.size = Pt(13)
p_meta.paragraph_format.space_after = Pt(10)

# Section 1
add_heading1("1. ที่มาและความสำคัญ")
add_p("กระบวนการจัดการการตรวจนิเทศงานสหกิจศึกษาของภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ถือเป็นกลไกสำคัญในการประกันคุณภาพการเรียนรู้และการฝึกประสบการณ์วิชาชีพของนิสิตในสถานประกอบการจริง อย่างไรก็ดี จากการศึกษาสภาพการดำเนินงานในปัจจุบัน พบว่ายังมีข้อจำกัดและปัญหาสำคัญ 4 ประการ ได้แก่:")
add_p("1) ปัญหาเอกสารกระดาษสูญหายและความล่าช้าในการส่งแบบฟอร์มประเมินทางการ Form 01 ถึง Form 11 ทำให้ไม่สามารถตรวจสอบย้อนหลังได้ทันท่วงที", indent=True)
add_p("2) ความยากลำบากในการติดตามความคืบหน้ารายบุคคลและการแยกหมู่เรียน (หมู่ 700 ภาคปกติ และหมู่ 800 ภาคพิเศษ) ของนิสิตจำนวนมาก", indent=True)
add_p("3) ปัญหาการนัดหมายลงพื้นที่ตรวจนิเทศที่คลาดเคลื่อนระหว่างอาจารย์ นิสิต และพนักงานพี่เลี้ยง เนื่องจากขาดระบบปฏิทินกลางที่แสดงผลตรงกัน", indent=True)
add_p("4) การขาดพยานหลักฐานเชิงประจักษ์ยืนยันว่าอาจารย์ได้เดินทางไปตรวจนิเทศ ณ สถานประกอบการจริงตามเกณฑ์มาตรฐาน", indent=True)
add_p("เพื่อแก้ไขปัญหาดังกล่าว ผู้จัดทำจึงได้พัฒนาระบบ 'KU Science Smart Internship Supervision Platform' ในรูปแบบเว็บแอปพลิเคชันแบบตอบสนอง (Responsive Single Page Application) รองรับทั้งคอมพิวเตอร์และสมาร์ทโฟน โดยมีระบบกล้องสดสแกน QR Code แบบเรียลไทม์ ระบบตรวจสอบพิกัด Geolocation API จำกัดรัศมี 500 เมตร คลังภาพถ่ายหลักฐานการนิเทศงาน และระบบความปลอดภัยยืนยันตัวตนด้วยรหัส OTP 8 หลัก ผ่านอีเมลมหาวิทยาลัย (@ku.th)")
add_p("คำสำคัญ : ระบบจัดการนิเทศงานสหกิจศึกษา, การตรวจนิเทศงาน, สแกน QR Code เช็คอิน, Geolocation API พิกัด GPS, ยืนยันตัวตน OTP, Supabase Cloud Database")

# Section 2
add_heading1("2. วัตถุประสงค์")
add_p("2.1 เพื่อพัฒนาระบบเว็บแอปพลิเคชันสำหรับบริหารจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ที่รองรับการทำงาน 3 บทบาท (ผู้ดูแลระบบ, อาจารย์นิเทศ, นิสิตสหกิจศึกษา)")
add_p("2.2 เพื่อพัฒนาระบบตรวจสอบและยืนยันการลงพื้นที่นิเทศงานจริง ณ สถานประกอบการ ด้วยการผสานเทคโนโลยี Dynamic QR Code สแกนเนอร์ และระบบตรวจสอบพิกัด Geolocation API แบบจำกัดรัศมีปลอดภัยไม่เกิน 500 เมตร (500m Geo-Fencing)")
add_p("2.3 เพื่อพัฒนาระบบบันทึกและจัดเก็บภาพถ่ายหลักฐานการลงพื้นที่นิเทศงานจริง (Supervision Evidence Gallery) พร้อมกลไกการยืนยันการอัปโหลดสองชั้น")
add_p("2.4 เพื่อพัฒนาระบบบริหารจัดการข้อมูลนิสิตผ่านการนำเข้าไฟล์ Excel ขนาดใหญ่แบบพรีวิวเต็มความกว้าง 100% และระบบส่งออกรายงานสรุปผลการนิเทศงานในรูปแบบ Excel และ PDF")
add_p("2.5 เพื่อพัฒนาระบบปฏิทินนัดหมายแบบระบุวันตรงกัน และระบบติดตามตรวจสอบสถานะการส่งเอกสารแบบฟอร์ม Form 01 - 11 แบบเรียลไทม์")

# Section 3
add_heading1("3. ขอบเขตของโครงงาน (Scope of Project)")
add_p("ขอบเขตการทำงานของระบบถูกออกแบบตามสิทธิ์และหน้าที่ของผู้ใช้งาน 3 ฝ่าย (User Scope) ดังนี้:")

def add_scope_table_to_docx(items_group, subhead):
    add_heading2(subhead)
    
    # Calculate row count
    total_rows = 1
    for grp in items_group:
        total_rows += len(grp["items"])
        
    table = doc.add_table(rows=total_rows, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="555555")
    
    # Header row
    hdr_cells = table.rows[0].cells
    headers = ["ฟังก์ชันการทำงาน", "รายละเอียด", "หมายเหตุ", "ความสำเร็จ"]
    col_widths = [Inches(1.4), Inches(2.4), Inches(2.3), Inches(0.77)]
    
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(13)
        set_cell_background(hdr_cells[i], "F1F5F9")
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=100, right=100)
        hdr_cells[i].width = col_widths[i]
        
    row_idx = 1
    for grp in items_group:
        cat_name = grp["category"]
        first_item = True
        for itm in grp["items"]:
            row_cells = table.rows[row_idx].cells
            
            # Col 0: Category
            if first_item:
                row_cells[0].text = cat_name
                p0 = row_cells[0].paragraphs[0]
                for r in p0.runs:
                    r.bold = True
                    r.font.size = Pt(12.5)
            else:
                row_cells[0].text = ""
            row_cells[0].width = col_widths[0]
            set_cell_margins(row_cells[0], top=80, bottom=80, left=80, right=80)
            
            # Col 1: Detail
            row_cells[1].text = f"☑ {itm['num']} {itm['desc']}"
            p1 = row_cells[1].paragraphs[0]
            for r in p1.runs:
                r.font.size = Pt(12)
            row_cells[1].width = col_widths[1]
            set_cell_margins(row_cells[1], top=80, bottom=80, left=80, right=80)
            
            # Col 2: Note
            row_cells[2].text = itm["note"]
            p2 = row_cells[2].paragraphs[0]
            for r in p2.runs:
                r.font.size = Pt(11.5)
                if "เป็นการปรับปรุง" in itm["note"] or "พัฒนาขึ้น" in itm["note"]:
                    r.font.color.rgb = RGBColor(15, 23, 42)
            row_cells[2].width = col_widths[2]
            set_cell_margins(row_cells[2], top=80, bottom=80, left=80, right=80)
            
            # Col 3: Success
            row_cells[3].text = itm["success"]
            p3 = row_cells[3].paragraphs[0]
            p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p3.runs:
                r.bold = True
                r.font.size = Pt(12)
                r.font.color.rgb = RGBColor(22, 101, 52)
            row_cells[3].width = col_widths[3]
            set_cell_margins(row_cells[3], top=80, bottom=80, left=80, right=80)
            
            first_item = False
            row_idx += 1
            
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

add_scope_table_to_docx(ADMIN_ITEMS, "3.1 ขอบเขตของผู้ดูแลระบบ (System Administrator)")
add_scope_table_to_docx(ADVISOR_ITEMS, "3.2 ขอบเขตของอาจารย์นิเทศ (Faculty Advisor)")
add_scope_table_to_docx(STUDENT_ITEMS, "3.3 ขอบเขตของนิสิตสหกิจศึกษา (Cooperative Education Student)")

# Section 4
add_heading1("4. ขอบเขตด้านสภาพแวดล้อมทางเทคนิคและสถาปัตยกรรมระบบ")
add_p("1) สถาปัตยกรรมระบบ: Single Page Application (SPA) ทำงานบนเทคโนโลยี Web Standards (HTML5, CSS3, JavaScript ES6+) รองรับการแสดงผลแบบ Responsive ทั้ง Desktop, Tablet และ Mobile")
add_p("2) ระบบฐานข้อมูลและคลาวด์: ใช้งาน Supabase Cloud Database (PostgreSQL) รองรับการจัดเก็บข้อมูลโครงสร้าง 7 ตารางหลัก พร้อมระบบสำรองข้อมูล Local Storage Fallback เพื่อให้ระบบทำงานต่อเนื่องได้แม้ออฟไลน์")
add_p("3) ระบบพิกัดและภูมิสารสนเทศ: เชื่อมโยง W3C Geolocation API คำนวณระยะห่างด้วยสูตร Haversine Formula เพื่อจำกัดรัศมีการเช็คอินให้อยู่ภายใน 500 เมตร")
add_p("4) ระบบสแกนรหัสและมัลติมีเดีย: ประมวลผลภาพจากกล้องสดผ่าน HTML5 Video Canvas ร่วมกับเอนจิน jsQR ตรวจจับ Dynamic QR Code แบบเรียลไทม์ และระบบคลังภาพถ่ายหลักฐานการนิเทศงาน")
add_p("5) ระบบเซิร์ฟเวอร์และการส่งออกเอกสาร: ทำงานร่วมกับ PowerShell Web Dispatcher (server.ps1), ระบบยืนยันตัวตน OTP 8 หลักทางอีเมล, ไลบรารี SheetJS (xlsx) และ jsPDF")

# Section 5
add_heading1("5. ระยะเวลาดำเนินงาน")
add_p("ตารางแผนการดำเนินงานโครงงานตลอดระยะเวลา 17 สัปดาห์ (มกราคม - พฤษภาคม 2569):")

gantt_table = doc.add_table(rows=7, cols=6)
gantt_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(gantt_table, color="555555")

g_headers = ["กิจกรรมการดำเนินงาน", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม"]
g_widths = [Inches(3.3), Inches(0.7), Inches(0.7), Inches(0.7), Inches(0.7), Inches(0.7)]

for i, h in enumerate(g_headers):
    c = gantt_table.rows[0].cells[i]
    c.text = h
    c.width = g_widths[i]
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs:
        r.bold = True
        r.font.size = Pt(12)
    set_cell_background(c, "F1F5F9")
    set_cell_margins(c, top=80, bottom=80, left=80, right=80)

g_rows = [
    ("1. ศึกษาข้อมูลและรวบรวมความต้องการ", [True, False, False, False, False]),
    ("2. ออกแบบระบบและฐานข้อมูล (Architecture, DFD, ERD)", [False, True, False, False, False]),
    ("3. ออกแบบส่วนต่อประสานผู้ใช้ UI/UX (Responsive)", [False, True, True, False, False]),
    ("4. พัฒนาระบบ (Frontend, Supabase, Geolocation, QR Scanner)", [False, False, True, True, False]),
    ("5. ทดสอบและประเมินผลระบบ (21 Test Cases, Benchmarks, SUS)", [False, False, False, True, True]),
    ("6. จัดทำเล่มรายงานความก้าวหน้าฉบับสมบูรณ์และคู่มือ", [False, False, False, False, True])
]

for row_i, (act, checks) in enumerate(g_rows, start=1):
    c0 = gantt_table.rows[row_i].cells[0]
    c0.text = act
    c0.width = g_widths[0]
    set_cell_margins(c0, top=60, bottom=60, left=80, right=80)
    for col_i, chk in enumerate(checks, start=1):
        cell = gantt_table.rows[row_i].cells[col_i]
        cell.text = "■" if chk else ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(13)
            r.font.color.rgb = RGBColor(2, 132, 199)
        cell.width = g_widths[col_i]
        set_cell_margins(cell, top=60, bottom=60, left=60, right=60)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 6
add_heading1("6. ประโยชน์ที่คาดว่าจะได้รับ")
add_p("1) เพิ่มประสิทธิภาพในการบริหารจัดการระดับภาควิชาและคณะฯ โดยมีระบบสารสนเทศส่วนกลางที่สามารถติดตามภาพรวมและสถานะการออกตรวจนิเทศงานสหกิจศึกษาได้อย่างถูกต้อง เป็นปัจจุบัน และโปร่งใส")
add_p("2) อำนวยความสะดวกแก่อาจารย์นิเทศในการปฏิบัติงาน โดยสามารถตรวจเช็ครายชื่อนิสิตแยกตามหมู่เรียน (700/800) บันทึกผลการนิเทศ ตรวจรับเอกสาร Form 01 - 11 และสแกนเช็คอินผ่านกล้องสมาร์ทโฟนได้อย่างรวดเร็ว")
add_p("3) ยกระดับความน่าเชื่อถือด้วยหลักฐานเชิงประจักษ์ มีระบบตรวจจับพิกัด GPS รัศมี 500 เมตร และคลังภาพถ่ายหลักฐานการลงพื้นที่จริง ป้องกันข้อผิดพลาดและการเช็คอินนอกสถานที่")
add_p("4) ลดความผิดพลาดในการจัดการข้อมูลนิสิต โดยผู้ดูแลระบบสามารถตรวจสอบความถูกต้องของข้อมูลผ่านระบบพรีวิว Excel ขนาดใหญ่เต็มความกว้าง 100% ก่อนนำเข้า และส่งออกรายงานสรุปผลการนิเทศได้ทันที")
add_p("5) สร้างความพึงพอใจและความสะดวกแก่นิสิต นิสิตสหกิจศึกษาสามารถติดตามวันเวลานัดหมายที่ตรงกัน ทราบผลการตรวจเอกสาร และดูผลการประเมินสะท้อนกลับจากอาจารย์ได้แบบเรียลไทม์")

# Section 7
add_heading1("7. การรับรองขอบเขตของโครงงาน")
add_p("จากขอบเขตของโครงงานข้อที่ 1 ถึงข้อที่ 6 ผู้จัดทำได้ปรับปรุงแก้ไขเพิ่มเติมร่วมกับอาจารย์ที่ปรึกษา และคณะกรรมการ เพื่อเป็นเกณฑ์ในการพิจารณาคะแนนตามความสมบูรณ์ของโครงงานในรายวิชา 01418499 โครงงานวิทยาการคอมพิวเตอร์ ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์")
add_p("ผู้จัดทำจึงขอปฏิบัติงานตามขอบเขตของโครงงานที่ได้เขียนไว้ข้างต้น")

p_sign = doc.add_paragraph()
p_sign.paragraph_format.space_before = Pt(16)
p_sign.add_run("ลงชื่อ ................................................................................ ผู้จัดทำ\n( นาย วงศพัทธ์ อุเทน )\nวันที่ ...... / ...... / ......\n\n")

p_sign.add_run("ความคิดเห็นจากอาจารย์ที่ปรึกษา:\n................................................................................................................................................................................................................................................................................................................................................................................................\n\n")
p_sign.add_run("ลงชื่อ ................................................................................ อาจารย์ที่ปรึกษา\n( อาจารย์ สมชาย แจ่มใส )\nวันที่ ...... / ...... / ......\n\n")

p_sign.add_run("ความคิดเห็นจากกรรมการ:\n................................................................................................................................................................................................................................................................................................................................................................................................\n\n")
p_sign.add_run("ลงชื่อ ................................................................................ กรรมการ\n( ................................................................................ )\nวันที่ ...... / ...... / ......\n\n")

p_sign.add_run("ความคิดเห็นจากกรรมการ:\n................................................................................................................................................................................................................................................................................................................................................................................................\n\n")
p_sign.add_run("ลงชื่อ ................................................................................ กรรมการ\n( ................................................................................ )\nวันที่ ...... / ...... / ......\n")

doc.save("Project_TOR_Final.docx")
print("Project_TOR_Final.docx created successfully!")

# -----------------------------------------------------------------------------
# 3. GENERATE HTML (Project_TOR_Final.html)
# -----------------------------------------------------------------------------

def html_table(items_group):
    rows_html = []
    for grp in items_group:
        cat_name = grp["category"]
        first = True
        for itm in grp["items"]:
            cat_td = f'<td style="font-weight: bold; vertical-align: top; background: #fafafa; border: 1px solid #cbd5e1; padding: 10px;">{cat_name}</td>' if first else '<td style="border: 1px solid #cbd5e1; background: #fafafa;"></td>'
            note_content = itm["note"]
            if note_content:
                note_badge = '<span style="display: inline-block; background: #eff6ff; color: #1e40af; border: 1px solid #bfdbfe; font-size: 11px; padding: 1px 6px; border-radius: 4px; font-weight: bold; margin-bottom: 4px;">ฟังก์ชันพัฒนาใหม่/ปรับปรุง</span><br/>' if ("เป็นการปรับปรุง" in note_content or "พัฒนาขึ้น" in note_content) else ''
                note_td = f'<td style="vertical-align: top; border: 1px solid #cbd5e1; padding: 10px; font-size: 13.5px; line-height: 1.5; color: #334155;">{note_badge}{note_content}</td>'
            else:
                note_td = '<td style="border: 1px solid #cbd5e1; padding: 10px; text-align: center; color: #94a3b8;">-</td>'
                
            rows_html.append(f'''<tr>
                {cat_td}
                <td style="vertical-align: top; border: 1px solid #cbd5e1; padding: 10px; font-size: 14px;">
                    <span style="color: #0284c7; font-weight: bold;">☑ {itm['num']}</span> {itm['desc']}
                </td>
                {note_td}
                <td style="vertical-align: top; text-align: center; border: 1px solid #cbd5e1; padding: 10px; font-weight: bold; color: #16a34a; font-size: 14px;">{itm['success']}</td>
            </tr>''')
            first = False
    return "\\n".join(rows_html)

html_template = f'''<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="utf-8">
<title>ขอบเขตของโครงงาน (Terms of Reference : TOR) - โครงการพัฒนาระบบจัดการการตรวจนิเทศงานสหกิจศึกษา</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap');
    body {{
        font-family: 'Sarabun', 'TH Sarabun New', Tahoma, sans-serif;
        line-height: 1.6;
        color: #1e293b;
        background-color: #f8fafc;
        margin: 0;
        padding: 30px 20px;
    }}
    .container {{
        max-width: 1050px;
        margin: 0 auto;
        background: #ffffff;
        padding: 50px 60px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }}
    .action-bar {{
        position: sticky;
        top: 20px;
        display: flex;
        justify-content: flex-end;
        gap: 12px;
        margin-bottom: 25px;
        z-index: 100;
    }}
    .btn {{
        background: #0284c7;
        color: white;
        border: none;
        padding: 10px 18px;
        font-size: 14px;
        font-weight: 600;
        border-radius: 8px;
        cursor: pointer;
        box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3);
        transition: all 0.2s;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }}
    .btn:hover {{
        background: #0369a1;
        transform: translateY(-1px);
    }}
    .btn-green {{
        background: #16a34a;
        box-shadow: 0 2px 6px rgba(22, 163, 74, 0.3);
    }}
    .btn-green:hover {{
        background: #15803d;
    }}
    h1 {{
        text-align: center;
        font-size: 26px;
        color: #0f172a;
        margin-bottom: 6px;
    }}
    h2.project-title {{
        text-align: center;
        font-size: 20px;
        color: #1e3a8a;
        margin-top: 0;
        margin-bottom: 4px;
    }}
    h3.project-eng {{
        text-align: center;
        font-size: 16px;
        color: #64748b;
        font-weight: normal;
        margin-top: 0;
        margin-bottom: 24px;
    }}
    .meta-box {{
        text-align: center;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 14px;
        border-radius: 8px;
        font-size: 14.5px;
        margin-bottom: 35px;
        line-height: 1.6;
    }}
    h2.section-title {{
        font-size: 19px;
        color: #0f172a;
        border-bottom: 2px solid #0284c7;
        padding-bottom: 6px;
        margin-top: 36px;
        margin-bottom: 16px;
    }}
    h3.sub-title {{
        font-size: 16.5px;
        color: #1e40af;
        margin-top: 24px;
        margin-bottom: 12px;
    }}
    p, li {{
        font-size: 15px;
        color: #334155;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0 24px 0;
        font-size: 14px;
    }}
    th {{
        background: #f1f5f9;
        color: #0f172a;
        font-weight: 700;
        border: 1px solid #cbd5e1;
        padding: 12px 10px;
        text-align: left;
    }}
    .sign-section {{
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #e2e8f0;
    }}
    .sign-box {{
        margin: 25px 0;
        line-height: 1.8;
    }}
    @media print {{
        body {{ background: white; padding: 0; }}
        .container {{ border: none; box-shadow: none; padding: 0; }}
        .action-bar {{ display: none; }}
    }}
</style>
</head>
<body>

<div class="container" id="printable-content">
    <div class="action-bar">
        <button class="btn btn-green" onclick="copyDocument()">📋 คัดลอกเนื้อหาทั้งหมด (สำหรับวางใน Google Docs)</button>
        <button class="btn" onclick="window.print()">🖨️ สั่งพิมพ์ / บันทึกเป็น PDF</button>
        <a href="Project_TOR_Final.docx" class="btn" style="background: #2563eb;" download>📥 ดาวน์โหลดไฟล์ Word (.docx)</a>
    </div>

    <h1>ขอบเขตของโครงงาน (Terms of Reference : TOR)</h1>
    <h2 class="project-title">โครงการพัฒนาระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์</h2>
    <h3 class="project-eng">(KU Science Smart Internship Supervision Platform)</h3>

    <div class="meta-box">
        <strong>ผู้จัดทำ:</strong> นาย วงศพัทธ์ อุเทน (wongsapat.u@ku.th) รหัสนิสิต 6521655442<br/>
        <strong>อาจารย์ที่ปรึกษาโครงงาน:</strong> อาจารย์ สมชาย แจ่มใส<br/>
        ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์<br/>
        <strong>รายวิชา:</strong> 01418499 โครงงานวิทยาการคอมพิวเตอร์ (ภาคปลาย ปีการศึกษา 2569)
    </div>

    <h2 class="section-title">1. ที่มาและความสำคัญ</h2>
    <p>กระบวนการจัดการการตรวจนิเทศงานสหกิจศึกษาของภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ถือเป็นกลไกสำคัญในการประกันคุณภาพการเรียนรู้และการฝึกประสบการณ์วิชาชีพของนิสิตในสถานประกอบการจริง อย่างไรก็ดี จากการศึกษาสภาพการดำเนินงานในปัจจุบัน พบว่ายังมีข้อจำกัดและปัญหาสำคัญ 4 ประการ ดังนี้:</p>
    <ul>
        <li><strong>ปัญหาการจัดการเอกสารกระดาษและความล่าช้า:</strong> การประเมินผลและการส่งแบบฟอร์มทางการ Form 01 ถึง Form 11 ยังใช้รูปแบบเอกสารกระดาษหรือการส่งไฟล์กระจัดกระจาย ทำให้เกิดปัญหาเอกสารสูญหาย ไม่สามารถตรวจสอบย้อนหลังได้ทันท่วงที และภาระงานตรวจรับเอกสารของอาจารย์นิเทศมีความซ้ำซ้อน</li>
        <li><strong>ความยากลำบากในการติดตามความคืบหน้ารายบุคคลและการแยกหมู่เรียน:</strong> ในแต่ละภาคการศึกษา มีนิสิตออกฝึกสหกิจศึกษาจำนวนมากแบ่งออกเป็นหมู่ 700 (ภาคปกติ) และหมู่ 800 (ภาคพิเศษ) การติดตามสถานะการส่งงานและการออกนิเทศของอาจารย์แต่ละท่านแบบเรียลไทม์ไม่สามารถทำได้อย่างมีเอกภาพ</li>
        <li><strong>ปัญหาการนัดหมายลงพื้นที่ตรวจนิเทศคลาดเคลื่อน:</strong> ตารางเวลาของอาจารย์นิเทศ นิสิต และพนักงานพี่เลี้ยงในสถานประกอบการมักเกิดความซ้ำซ้อนหรือคลาดเคลื่อน เนื่องจากไม่มีระบบปฏิทินกลางที่แสดงผลนัดหมายระบุวันตรงกัน</li>
        <li><strong>การขาดพยานหลักฐานเชิงประจักษ์ยืนยันการลงพื้นที่จริง:</strong> ในการตรวจนิเทศงานยังขาดกลไกที่เชื่อถือได้และโปร่งใสในการยืนยันว่าอาจารย์ได้เดินทางไปตรวจนิเทศ ณ สถานประกอบการจริงตามเกณฑ์มาตรฐาน</li>
    </ul>
    <p>เพื่อแก้ไขปัญหาดังกล่าว ผู้จัดทำจึงได้พัฒนา <strong>"ระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ (KU Science Smart Internship Supervision Platform)"</strong> ขึ้นในรูปแบบเว็บแอปพลิเคชันแบบตอบสนอง (Responsive Single Page Application) รองรับการใช้งานทั้งคอมพิวเตอร์ แท็บเล็ต และสมาร์ทโฟน โดยบูรณาการเทคโนโลยีกล้องสดสแกน QR Code แบบเรียลไทม์ ระบบตรวจสอบพิกัดภูมิศาสตร์ (Geolocation API) จำกัดรัศมีการเช็คอินไม่เกิน 500 เมตร (500m Geo-Fencing) คลังภาพถ่ายหลักฐานการนิเทศงาน (Supervision Evidence Gallery) และระบบความปลอดภัยยืนยันตัวตนด้วยรหัส OTP 8 หลัก ผ่านอีเมลมหาวิทยาลัย (@ku.th)</p>
    <p><strong>คำสำคัญ :</strong> ระบบจัดการนิเทศงานสหกิจศึกษา, การตรวจนิเทศงาน, สแกน QR Code เช็คอิน, Geolocation API พิกัด GPS, ยืนยันตัวตน OTP, Supabase Cloud Database</p>

    <h2 class="section-title">2. วัตถุประสงค์</h2>
    <ol>
        <li>เพื่อพัฒนาระบบเว็บแอปพลิเคชันสำหรับบริหารจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ ที่รองรับการทำงาน 3 บทบาท (ผู้ดูแลระบบ, อาจารย์นิเทศ, นิสิตสหกิจศึกษา)</li>
        <li>เพื่อพัฒนาระบบตรวจสอบและยืนยันการลงพื้นที่นิเทศงานจริง ณ สถานประกอบการ ด้วยการผสานเทคโนโลยี Dynamic QR Code สแกนเนอร์ และระบบตรวจสอบพิกัด Geolocation API แบบจำกัดรัศมีปลอดภัยไม่เกิน 500 เมตร (500m Geo-Fencing)</li>
        <li>เพื่อพัฒนาระบบบันทึกและจัดเก็บภาพถ่ายหลักฐานการลงพื้นที่นิเทศงานจริง (Supervision Evidence Gallery) พร้อมกลไกการยืนยันการอัปโหลดสองชั้น</li>
        <li>เพื่อพัฒนาระบบบริหารจัดการข้อมูลนิสิตผ่านการนำเข้าไฟล์ Excel ขนาดใหญ่แบบพรีวิวเต็มความกว้าง 100% และระบบส่งออกรายงานสรุปผลการนิเทศงานในรูปแบบ Excel และ PDF</li>
        <li>เพื่อพัฒนาระบบปฏิทินนัดหมายแบบระบุวันตรงกัน และระบบติดตามตรวจสอบสถานะการส่งเอกสารแบบฟอร์ม Form 01 - 11 แบบเรียลไทม์</li>
    </ol>

    <h2 class="section-title">3. ขอบเขตของโครงงาน (Scope of Project)</h2>
    <p>ขอบเขตการทำงานของระบบถูกออกแบบตามสิทธิ์และหน้าที่ของผู้ใช้งาน 3 ฝ่าย (User Scope) โดยในแต่ละฟังก์ชันได้ระบุรายละเอียด หมายเหตุการพัฒนาฟังก์ชันใหม่ และระดับความสำเร็จ ดังตารางต่อไปนี้:</p>

    <h3 class="sub-title">3.1 ขอบเขตของผู้ดูแลระบบ (System Administrator)</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 22%;">ฟังก์ชันการทำงาน</th>
                <th style="width: 38%;">รายละเอียด</th>
                <th style="width: 30%;">หมายเหตุ</th>
                <th style="width: 10%; text-align: center;">ความสำเร็จ</th>
            </tr>
        </thead>
        <tbody>
            {html_table(ADMIN_ITEMS)}
        </tbody>
    </table>

    <h3 class="sub-title">3.2 ขอบเขตของอาจารย์นิเทศ (Faculty Advisor)</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 22%;">ฟังก์ชันการทำงาน</th>
                <th style="width: 38%;">รายละเอียด</th>
                <th style="width: 30%;">หมายเหตุ</th>
                <th style="width: 10%; text-align: center;">ความสำเร็จ</th>
            </tr>
        </thead>
        <tbody>
            {html_table(ADVISOR_ITEMS)}
        </tbody>
    </table>

    <h3 class="sub-title">3.3 ขอบเขตของนิสิตสหกิจศึกษา (Cooperative Education Student)</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 22%;">ฟังก์ชันการทำงาน</th>
                <th style="width: 38%;">รายละเอียด</th>
                <th style="width: 30%;">หมายเหตุ</th>
                <th style="width: 10%; text-align: center;">ความสำเร็จ</th>
            </tr>
        </thead>
        <tbody>
            {html_table(STUDENT_ITEMS)}
        </tbody>
    </table>

    <h2 class="section-title">4. ขอบเขตด้านสภาพแวดล้อมทางเทคนิคและสถาปัตยกรรมระบบ</h2>
    <ul>
        <li><strong>สถาปัตยกรรมระบบ:</strong> Single Page Application (SPA) ทำงานบนเทคโนโลยี Web Standards (HTML5, CSS3, JavaScript ES6+) รองรับการแสดงผลแบบ Responsive ทั้ง Desktop, Tablet และ Mobile</li>
        <li><strong>ระบบฐานข้อมูลและคลาวด์:</strong> ใช้งาน Supabase Cloud Database (PostgreSQL) รองรับการจัดเก็บข้อมูลโครงสร้าง 7 ตารางหลัก พร้อมระบบสำรองข้อมูล Local Storage Fallback เพื่อให้ระบบทำงานต่อเนื่องได้แม้ออฟไลน์</li>
        <li><strong>ระบบพิกัดและภูมิสารสนเทศ:</strong> เชื่อมโยง W3C Geolocation API คำนวณระยะห่างด้วยสูตร Haversine Formula เพื่อจำกัดรัศมีการเช็คอินให้อยู่ภายใน 500 เมตร</li>
        <li><strong>ระบบสแกนรหัสและมัลติมีเดีย:</strong> ประมวลผลภาพจากกล้องสดผ่าน HTML5 Video Canvas ร่วมกับเอนจิน jsQR ตรวจจับ Dynamic QR Code แบบเรียลไทม์ และระบบคลังภาพถ่ายหลักฐานการนิเทศงาน</li>
        <li><strong>ระบบเซิร์ฟเวอร์และการส่งออกเอกสาร:</strong> ทำงานร่วมกับ PowerShell Web Dispatcher (server.ps1), ระบบยืนยันตัวตน OTP 8 หลักทางอีเมล, ไลบรารี SheetJS (xlsx) และ jsPDF</li>
    </ul>

    <h2 class="section-title">5. ระยะเวลาดำเนินงาน</h2>
    <p>ตารางแผนการดำเนินงานโครงงานตลอดระยะเวลา 17 สัปดาห์ (มกราคม - พฤษภาคม 2569):</p>
    <table>
        <thead>
            <tr>
                <th style="width: 50%;">กิจกรรมการดำเนินงาน</th>
                <th style="width: 10%; text-align: center;">มกราคม</th>
                <th style="width: 10%; text-align: center;">กุมภาพันธ์</th>
                <th style="width: 10%; text-align: center;">มีนาคม</th>
                <th style="width: 10%; text-align: center;">เมษายน</th>
                <th style="width: 10%; text-align: center;">พฤษภาคม</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>1. ศึกษาข้อมูลและรวบรวมความต้องการ</strong><br/>- ศึกษากระบวนการสหกิจศึกษาและแบบฟอร์ม Form 01 - 11<br/>- รวบรวม Requirement จากอาจารย์นิเทศและงานทะเบียน</td>
                <td style="text-align: center; font-weight: bold; color: #0284c7;">■■■■</td>
                <td></td><td></td><td></td><td></td>
            </tr>
            <tr>
                <td><strong>2. ออกแบบระบบและฐานข้อมูล</strong><br/>- ออกแบบสถาปัตยกรรมระบบ (System Architecture)<br/>- ออกแบบ Data Flow Diagram (DFD) และ ER-Diagram 7 ตาราง</td>
                <td></td>
                <td style="text-align: center; font-weight: bold; color: #0284c7;">■■■■</td>
                <td></td><td></td><td></td>
            </tr>
            <tr>
                <td><strong>3. ออกแบบส่วนต่อประสานผู้ใช้ (UI/UX)</strong><br/>- ออกแบบ Responsive UI สำหรับ Desktop และ Mobile<br/>- ออกแบบแผงควบคุม Dashboard, ห้องเรียน, และระบบสแกน</td>
                <td></td>
                <td style="text-align: center; font-weight: bold; color: #0284c7;">■■</td>
                <td style="text-align: center; font-weight: bold; color: #0284c7;">■■</td>
                <td></td><td></td>
            </tr>
            <tr>
                <td><strong>4. พัฒนาระบบ (System Implementation)</strong><br/>- พัฒนาระบบนำเข้า Excel พรีวิวเต็มจอ และจัดการผู้ใช้<br/>- พัฒนาระบบห้องเรียน 700/800 และการตรวจรับเอกสาร<br/>- พัฒนาระบบสแกน QR Code สด และ Geolocation 500m<br/>- พัฒนาระบบคลังภาพถ่ายหลักฐาน และปฏิทินนัดหมาย</td>
                <td></td><td></td>
                <td style="text-align: center; font-weight: bold; color: #0284c7;">■■■■</td>
                <td style="text-align: center; font-weight: bold; color: #0284c7;">■■■■</td>
                <td></td>
            </tr>
            <tr>
                <td><strong>5. ทดสอบและประเมินผลระบบ (Testing & Evaluation)</strong><br/>- ทดสอบเชิงฟังก์ชัน 21 Test Cases ครอบคลุม 3 บทบาท<br/>- ทดสอบ Performance Benchmarks และ Geo-Fence 500m<br/>- ประเมินความพึงพอใจการใช้งานจริงตามเกณฑ์ SUS Score</td>
                <td></td><td></td><td></td>
                <td style="text-align: center; font-weight: bold; color: #0284c7;">■■</td>
                <td style="text-align: center; font-weight: bold; color: #0284c7;">■■</td>
            </tr>
            <tr>
                <td><strong>6. จัดทำเล่มรายงานและเอกสารนำเสนอ</strong><br/>- จัดทำคู่มือการติดตั้งและการใช้งานระบบ<br/>- จัดทำเล่มรายงานความก้าวหน้าโครงงานฉบับสมบูรณ์ (เล่มจบ)</td>
                <td></td><td></td><td></td><td></td>
                <td style="text-align: center; font-weight: bold; color: #0284c7;">■■■■</td>
            </tr>
        </tbody>
    </table>

    <h2 class="section-title">6. ประโยชน์ที่คาดว่าจะได้รับ</h2>
    <ol>
        <li><strong>เพิ่มประสิทธิภาพในการบริหารจัดการระดับภาควิชาและคณะฯ:</strong> มีระบบสารสนเทศส่วนกลางที่สามารถติดตามภาพรวมและสถานะการออกตรวจนิเทศงานสหกิจศึกษาได้อย่างถูกต้อง เป็นปัจจุบัน และโปร่งใส</li>
        <li><strong>อำนวยความสะดวกแก่อาจารย์นิเทศในการปฏิบัติงาน:</strong> อาจารย์สามารถตรวจเช็ครายชื่อนิสิตแยกตามหมู่เรียน (700/800) บันทึกผลการนิเทศงาน ตรวจรับเอกสาร Form 01 - 11 และสแกนเช็คอินผ่านกล้องสมาร์ทโฟนได้อย่างรวดเร็ว</li>
        <li><strong>ยกระดับความน่าเชื่อถือด้วยหลักฐานเชิงประจักษ์:</strong> มีระบบตรวจจับพิกัด GPS รัศมี 500 เมตร และคลังภาพถ่ายหลักฐานการลงพื้นที่จริง ป้องกันข้อผิดพลาดและการเช็คอินนอกสถานที่</li>
        <li><strong>ลดความผิดพลาดในการจัดการข้อมูลนิสิต:</strong> ผู้ดูแลระบบสามารถตรวจสอบความถูกต้องของข้อมูลผ่านระบบพรีวิว Excel ขนาดใหญ่เต็มความกว้าง 100% ก่อนนำเข้า และส่งออกรายงานสรุปผลการนิเทศได้ทันที</li>
        <li><strong>สร้างความพึงพอใจและความสะดวกแก่นิสิต:</strong> นิสิตสหกิจศึกษาสามารถติดตามวันเวลานัดหมายที่ตรงกัน ทราบผลการตรวจเอกสาร และดูผลการประเมินสะท้อนกลับจากอาจารย์ได้แบบเรียลไทม์</li>
    </ol>

    <div class="sign-section">
        <h2 class="section-title">7. การรับรองขอบเขตของโครงงาน</h2>
        <p>จากขอบเขตของโครงงานข้อที่ 1 ถึงข้อที่ 6 ผู้จัดทำได้ปรับปรุงแก้ไขเพิ่มเติมร่วมกับอาจารย์ที่ปรึกษา และคณะกรรมการ เพื่อเป็นเกณฑ์ในการพิจารณาคะแนนตามความสมบูรณ์ของโครงงานในรายวิชา <strong>01418499 โครงงานวิทยาการคอมพิวเตอร์</strong> ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์</p>
        <p>ผู้จัดทำจึงขอปฏิบัติงานตามขอบเขตของโครงงานที่ได้เขียนไว้ข้างต้น</p>

        <div class="sign-box">
            ลงชื่อ ................................................................................ ผู้จัดทำ<br/>
            ( นาย วงศพัทธ์ อุเทน )<br/>
            วันที่ ...... / ...... / ......
        </div>

        <div class="sign-box">
            <strong>ความคิดเห็นจากอาจารย์ที่ปรึกษา:</strong><br/>
            ................................................................................................................................................................................................................................................................................................................................................................................................<br/><br/>
            ลงชื่อ ................................................................................ อาจารย์ที่ปรึกษา<br/>
            ( อาจารย์ สมชาย แจ่มใส )<br/>
            วันที่ ...... / ...... / ......
        </div>

        <div class="sign-box">
            <strong>ความคิดเห็นจากกรรมการ:</strong><br/>
            ................................................................................................................................................................................................................................................................................................................................................................................................<br/><br/>
            ลงชื่อ ................................................................................ กรรมการ<br/>
            ( ................................................................................ )<br/>
            วันที่ ...... / ...... / ......
        </div>

        <div class="sign-box">
            <strong>ความคิดเห็นจากกรรมการ:</strong><br/>
            ................................................................................................................................................................................................................................................................................................................................................................................................<br/><br/>
            ลงชื่อ ................................................................................ กรรมการ<br/>
            ( ................................................................................ )<br/>
            วันที่ ...... / ...... / ......
        </div>
    </div>
</div>

<script>
function copyDocument() {{
    const el = document.getElementById('printable-content');
    // Select HTML content
    const range = document.createRange();
    range.selectNode(el);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    try {{
        document.execCommand('copy');
        alert('คัดลอกเนื้อหาขอบเขตของโครงงาน (TOR) ทั้งหมดเรียบร้อยแล้ว! สามารถนำไปกดวาง (Ctrl+V) ใน Google Docs ได้ทันทีครับ');
    }} catch (err) {{
        alert('กรุณากด Ctrl+A แล้ว Ctrl+C เพื่อคัดลอกด้วยตนเอง');
    }}
    window.getSelection().removeAllRanges();
}}
</script>

</body>
</html>
'''

with open("Project_TOR_Final.html", "w", encoding="utf-8") as f:
    f.write(html_template)
print("Project_TOR_Final.html written successfully!")

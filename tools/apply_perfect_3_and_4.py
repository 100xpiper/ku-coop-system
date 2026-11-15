# -*- coding: utf-8 -*-
"""
apply_perfect_3_and_4.py
1. แก้เลขอ้างอิงในบทที่ 2 จาก [9]-[15] เป็น [6]-[12]
2. ปรับปรุงรายการบรรณานุกรม [1]-[12] ท้ายเล่มให้ตรงกันแบบ 1-to-1
3. ปรับชื่อภาพในบทที่ 2 เป็น ภาพที่ 1, 2, 3
4. ปรับสารบัญเนื้อหา สารบัญรูปภาพ สารบัญตาราง และตัวเลขหน้าจริง 100%
5. ปกป้อง Page Breaks เดิมทั้งหมด ไม่ให้สูญหาย
"""

import os
import re
import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

SRC_PATH = r'docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs_backup.docx'
doc = docx.Document(SRC_PATH)

def format_run(run, font_name='Angsana New', size_pt=15, bold=False, color_rgb=(0, 0, 0)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.color.rgb = RGBColor(*color_rgb)
    run.bold = bold
    rPr = run._element.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    rFonts.set(qn('w:eastAsia'), font_name)
    rPr.append(rFonts)

def set_para_line(p, text, font_name='Angsana New', size_pt=15, bold=False, space_after_pt=2):
    p.text = text
    for r in p.runs:
        format_run(r, font_name=font_name, size_pt=size_pt, bold=bold)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(space_after_pt)

print("Starting precise update...")

# =============================================================================
# 1. ITEM 3: REFERENCE CITATIONS IN CHAPTER 2
# =============================================================================
ref_map = [
    ("2.3.1 HTML (HyperText Markup Language) [9]", "2.3.1 HTML (HyperText Markup Language) [6]"),
    ("2.3.2 CSS (Cascading Style Sheets) [10]", "2.3.2 CSS (Cascading Style Sheets) [7]"),
    ("2.3.3 JavaScript [11]", "2.3.3 JavaScript [8]"),
    ("2.3.4 Supabase [12]", "2.3.4 Supabase [9]"),
    ("2.3.5 ไลบรารี jsQR [13]", "2.3.5 ไลบรารี jsQR [10]"),
    ("2.3.6 ไลบรารี SheetJS [14]", "2.3.6 ไลบรารี SheetJS [11]"),
    ("2.3.7 Visual Studio Code [15]", "2.3.7 Visual Studio Code [12]")
]

for p in doc.paragraphs:
    for old_t, new_t in ref_map:
        if old_t in p.text:
            p.text = p.text.replace(old_t, new_t)
            for r in p.runs:
                format_run(r, font_name='Angsana New', size_pt=16, bold=True)
            print(f"Updated: {new_t}")

# =============================================================================
# 2. ITEM 3: BIBLIOGRAPHY AT END OF BOOK
# =============================================================================
bib_items = [
    "[1] Google Classroom. สืบค้นเมื่อ 8 กรกฎาคม 2569, [Online]. แหล่งที่มา https://classroom.google.com",
    "[2] Microsoft Teams. สืบค้นเมื่อ 8 กรกฎาคม 2569, [Online]. แหล่งที่มา https://teams.live.com/",
    "[3] ResearchGate. \"QR Code Based Smart Attendance System using Mobile Application \". สืบค้นเมื่อ 10 กรกฎาคม 2569, [Online]. แหล่งที่มา https://www.researchgate.net/publication/342998634_QR_Code_Based_Smart_Attendance_System_Using_Mobile_Application",
    "[4] Location-Based Student Attendance Tracking System Using GPS and Geofencing. สืบค้นเมื่อ 10 กรกฎาคม 2569, [Online]. แหล่งที่มา https://www.researchgate.net/publication/362547160_Location_Based_Student_Attendance_Tracking_System_Using_GPS_and_Geofencing",
    "[5] Development of Mobile Information System for Cooperative Education. สืบค้นเมื่อ 10 กรกฎาคม 2569, [Online]. แหล่งที่มา https://so05.tci-thaijo.org/index.php/jtir/article/view/253689",
    "[6] HTML (HyperText Markup Language). “โครงสร้างและการใช้งานภาษา HTML5 เบื้องต้น”. สืบค้นเมื่อ 25 พฤศจิกายน 2568, [Online]. แหล่งที่มา https://www.w3.org/html/",
    "[7] CSS (Cascading Style Sheets). “การออกแบบและตกแต่งหน้าเว็บเพจด้วย CSS3”. สืบค้นเมื่อ 25 พฤศจิกายน 2568, [Online]. แหล่งที่มา https://www.w3schools.com/css/",
    "[8] BorntoDev. \"JavaScript คืออะไร ? ภาษาที่นักพัฒนาเว็บทุกคนต้องรู้\". สืบค้นเมื่อ 11 กรกฎาคม 2569, [Online]. แหล่งที่มา https://www.borntodev.com/2020/02/28/javascript-%E0%B8%84%E0%B8%B7%E0%B8%AD%E0%B8%AD%E0%B8%B0%E0%B8%B9%E0%B9%84%E0%B8%A3/",
    "[9] BorntoDev. \"รู้จักกับ Supabase แพลตฟอร์ม Backend-as-a-Service แบบ Open-source\". สืบค้นเมื่อ 11 กรกฎาคม 2569, [Online]. แหล่งที่มา https://www.borntodev.com/2023/10/24/getting-started-with-supabase/",
    "[10] jsQR Developers. \"jsQR: A pure JavaScript QR code reading library\". สืบค้นเมื่อ 11 กรกฎาคม 2569, [Online]. แหล่งที่มา https://github.com/cozmo/jsQR",
    "[11] DevAhoy. \"การจัดการไฟล์ Spreadsheet บนเบราว์เซอร์ด้วย SheetJS (xlsx)\". สืบค้นเมื่อ 11 กรกฎาคม 2569, [Online]. แหล่งที่มา https://devahoy.com/posts/read-and-write-excel-file-with-javascript/",
    "[12] Visual Studio Code. \"สภาพแวดล้อมการพัฒนาโปรแกรมและการแก้ไขซอร์สโค้ด\". สืบค้นเมื่อ 11 กรกฎาคม 2569, [Online]. แหล่งที่มา https://code.visualstudio.com/"
]

bib_header_idx = -1
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "เอกสารและสิ่งอ้างอิง":
        bib_header_idx = i
        break

print(f"Bibliography header at: {bib_header_idx}")
for idx, text in enumerate(bib_items):
    p_idx = bib_header_idx + 1 + idx
    set_para_line(doc.paragraphs[p_idx], text, font_name='Angsana New', size_pt=15, space_after_pt=4)

# Clear old [13] paragraph (p456)
old_13_idx = bib_header_idx + 1 + len(bib_items) # 443 + 1 + 12 = 456
if old_13_idx < len(doc.paragraphs):
    # Only clear text in runs, preserving paragraph structure
    p = doc.paragraphs[old_13_idx]
    for r in p.runs:
        r.text = ""
    print(f"Cleared text of old [13] at paragraph {old_13_idx}")

# =============================================================================
# 3. ITEM 4: FIGURE CAPTIONS IN CHAPTER 2
# =============================================================================
ch2_captions = {
    "ภาพหน้าหลักของแอปพลิเคชัน": "ภาพที่ 1 หน้าแรกและส่วนห้องเรียนของแอปพลิเคชัน Google Classroom",
    "ภาพหน้าหลักของ Microsoft team": "ภาพที่ 2 หน้าแรกของแอปพลิเคชัน Microsoft Teams แสดงการสื่อสาร",
    "ภาพหน้าปฏิทิน": "ภาพที่ 3 ระบบปฏิทินนัดหมายของแอปพลิเคชัน Microsoft Teams"
}

for p in doc.paragraphs:
    t = p.text.strip()
    if t in ch2_captions:
        new_c = ch2_captions[t]
        p.text = new_c
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            format_run(r, font_name='Angsana New', size_pt=15)
        print(f"Updated caption: {new_c}")

# Clear text in classroom drawing paragraph
for p in doc.paragraphs:
    if "ภาพส่วนของห้องเรียนในclassroom" in p.text:
        for r in p.runs:
            if "ภาพส่วนของห้องเรียนในclassroom" in r.text:
                r.text = r.text.replace("ภาพส่วนของห้องเรียนในclassroom", "").strip()

# =============================================================================
# 4. ITEM 4: TABLE OF CONTENTS (สารบัญ)
# =============================================================================
new_toc = [
    "บทคัดย่อภาษาไทย ............................................. ก",
    "Abstract ........................................................... ค",
    "กิตติกรรมประกาศ ............................................. จ",
    "สารบัญ ............................................................... ฉ",
    "สารบัญรูปภาพ ................................................... ซ",
    "สารบัญตาราง ..................................................... ญ",
    "บทที่ 1 บทนำ ................................................... 1",
    "  1.1 ที่มาและความสำคัญของปัญหา ............. 1",
    "  1.2 วัตถุประสงค์ของโครงงาน ................... 2",
    "  1.3 ขอบเขตของโครงงาน ............................... 2",
    "  1.4 ประโยชน์ที่คาดว่าจะได้รับ ............. 4",
    "บทที่ 2 ทบทวนวรรณกรรม ................................. 5",
    "  2.1 ศึกษาข้อมูลแอปพลิเคชันและระบบที่เกี่ยวข้อง ..... 5",
    "    2.1.1 แอปพลิเคชัน Google Classroom ..... 5",
    "    2.1.2 แอปพลิเคชัน Microsoft Teams ..... 7",
    "  2.2 ศึกษาข้อมูลบทความที่เกี่ยวข้อง ..... 9",
    "  2.3 เครื่องมือที่ใช้ในการพัฒนาระบบ ..... 15",
    "บทที่ 3 แนวคิดการออกแบบระบบ ..................... 17",
    "  3.1 work flow แนวคิดในการออกแบบระบบ ..... 17",
    "    3.1.1 ขั้นตอนการทำงานของนิสิตสหกิจศึกษา (Student Workflow) ..... 17",
    "    3.1.2 ขั้นตอนการทำงานของอาจารย์นิเทศ (Advisor Workflow) ..... 19",
    "    3.1.3 ขั้นตอนการทำงานของผู้ดูแลระบบ (Admin Workflow) ..... 21",
    "    3.1.4 ขั้นตอนการสแกนและตรวจสอบพิกัด Geofencing 500 เมตร ..... 23",
    "  3.2 การออกแบบฐานข้อมูล (Database Design) ..... 23",
    "บทที่ 4 ผลการดำเนินงานและการทดสอบระบบ ..... 27",
    "  4.1 ขอบเขตการทำงานและสิทธิ์การใช้งานของแต่ละบทบาท ..... 27",
    "  4.2 การทำงานจริงของระบบและส่วนต่อประสานผู้ใช้งาน (37 ขั้นตอน) ..... 27",
    "  4.3 ผลการทดสอบการทำงานของระบบ (System Testing) ..... 57",
    "บทที่ 5 สรุปผลการดำเนินงานและข้อเสนอแนะ ..... 60",
    "  5.1 สรุปผลการดำเนินงาน ........................... 60",
    "  5.2 ปัญหาและอุปสรรคที่พบระหว่างการพัฒนา ..... 61",
    "  5.3 แนวทางการพัฒนาต่อยอดในอนาคต ......... 63",
    "เอกสารและสิ่งอ้างอิง ................................... 64",
    "ประวัติผู้จัดทำ ............................................. 66"
]

toc_header_idx = 57 # 'สารบัญ'
print(f"Updating TOC from p{toc_header_idx + 1} to p{toc_header_idx + len(new_toc)}...")
for idx, line in enumerate(new_toc):
    p_idx = toc_header_idx + 1 + idx # 58 to 91
    set_para_line(doc.paragraphs[p_idx], line, font_name='Angsana New', size_pt=15, space_after_pt=2)

# Paragraph 92 was the 35th TOC line in original. We clear its text.
# Paragraph 93 is the page break before สารบัญรูปภาพ - DO NOT TOUCH p93!
p92 = doc.paragraphs[92]
for r in p92.runs:
    r.text = ""

# =============================================================================
# 5. ITEM 4: LIST OF FIGURES (สารบัญรูปภาพ)
# =============================================================================
new_figures = [
    "ภาพที่ 1 หน้าแรกและส่วนห้องเรียนของแอปพลิเคชัน Google Classroom ..... 5",
    "ภาพที่ 2 หน้าแรกของแอปพลิเคชัน Microsoft Teams แสดงการสื่อสาร ..... 7",
    "ภาพที่ 3 ระบบปฏิทินนัดหมายของแอปพลิเคชัน Microsoft Teams ..... 8",
    "ภาพที่ 4 Workflow ขั้นตอนการทำงานของนิสิตสหกิจศึกษา (Student Workflow) ..... 17",
    "ภาพที่ 5 Workflow ขั้นตอนการทำงานของอาจารย์นิเทศ (Advisor Workflow) ..... 19",
    "ภาพที่ 6 Workflow ขั้นตอนการทำงานของผู้ดูแลระบบ (Admin Workflow) ..... 21",
    "ภาพที่ 7 หน้าจอเข้าสู่ระบบเริ่มต้น (Login Initial View) ..... 28",
    "ภาพที่ 8 การกรอกข้อมูลบัญชีผู้ใช้งานอีเมลมหาวิทยาลัยและรหัสผ่าน ..... 29",
    "ภาพที่ 9 การเปิด-ปิดการแสดงผลรหัสผ่านเพื่อตรวจสอบความถูกต้อง ..... 29",
    "ภาพที่ 10 รหัสยืนยันตัวตน OTP 8 หลัก ที่ระบบจัดส่งไปยังกล่องข้อความอีเมลมหาวิทยาลัย ..... 30",
    "ภาพที่ 11 หน้าต่างยืนยันตัวตนและกรอกรหัส OTP 8 หลัก เข้าสู่ระบบ ..... 31",
    "ภาพที่ 12 หน้าต่างบังคับเปลี่ยนรหัสผ่านครั้งแรกตามเกณฑ์ความปลอดภัย ..... 31",
    "ภาพที่ 13 แดชบอร์ดภาพรวมของนิสิตสหกิจศึกษา (Student Dashboard) ..... 32",
    "ภาพที่ 14 บัตรประจำตัว Dynamic QR Code ของนิสิตสหกิจศึกษา ..... 33",
    "ภาพที่ 15 คลังแบบฟอร์มเปล่าสหกิจศึกษา (FORM-00 ถึง FORM-11) ..... 34",
    "ภาพที่ 16 หน้าต่างอัปโหลดเอกสารสหกิจศึกษา ..... 34",
    "ภาพที่ 17 ประวัติการส่งเอกสารและผลการตรวจรับ/ข้อคิดเห็นสะท้อนกลับรายฉบับ ..... 35",
    "ภาพที่ 18 ปฏิทินกำหนดการและนัดหมายการออกตรวจนิเทศของนิสิต ..... 36",
    "ภาพที่ 19 ระบบบันทึกและติดตามความก้าวหน้าโครงงาน (Project Tracking) ..... 37",
    "ภาพที่ 20 การเลือกห้องเรียนของอาจารย์นิเทศ (หมู่ 700 และ หมู่ 800) ..... 38",
    "ภาพที่ 21 หน้ารายชื่อนิสิตในห้องเรียนและข้อมูลสถานที่ฝึกงาน ..... 38",
    "ภาพที่ 22 รายละเอียดนิสิต ข้อมูลพี่เลี้ยง และพิกัดสถานที่ฝึกงาน ..... 39",
    "ภาพที่ 23 ตารางแมทริกซ์สรุปสถานะการส่งเอกสารของนิสิตทุกคน ..... 40",
    "ภาพที่ 24 หน้าต่างตรวจรับเอกสารรายฉบับและผลการอนุมัติ ..... 40",
    "ภาพที่ 25 การปฏิเสธเอกสารพร้อมระบุข้อคิดเห็นตีกลับแก้ไข ..... 41",
    "ภาพที่ 26 ระบบจัดการภาระงานและการมอบหมายงาน (Assignments) ..... 42",
    "ภาพที่ 27 หน้าต่างสร้างและสั่งงานใหม่แก่นิสิต ..... 42",
    "ภาพที่ 28 ตรวจสอบรายชื่อนิสิตที่ส่งงานและการส่งไฟล์ ..... 43",
    "ภาพที่ 29 ปฏิทินนัดหมายการลงพื้นที่ตรวจนิเทศของอาจารย์ ..... 44",
    "ภาพที่ 30 หน้าจอกล้องสด Live Camera Scanner สำหรับสแกน QR Code ..... 45",
    "ภาพที่ 31 การเช็คอินสำเร็จเมื่ออยู่ในรัศมีปลอดภัย 500 เมตร (การ์ดเขียว) ..... 46",
    "ภาพที่ 32 การแจ้งเตือนปฏิเสธการเช็คอินเมื่ออยู่นอกรัศมี 500 เมตร (การ์ดแดง) ..... 47",
    "ภาพที่ 33 หน้าต่างตั้งค่าและปรับปรุงพิกัด GPS สถานประกอบการ ..... 47",
    "ภาพที่ 34 การอัปโหลดภาพถ่ายหลักฐานการนิเทศพร้อมการยืนยันสองชั้น ..... 48",
    "ภาพที่ 35 คลังภาพถ่ายหลักฐานการนิเทศงานรวมทุกรายการ ..... 49",
    "ภาพที่ 36 แบบฟอร์มประเมินคะแนนนิเทศงานตามเกณฑ์รูบริกและข้อเสนอแนะ ..... 50",
    "ภาพที่ 37 แดชบอร์ดสรุปสถิตินิสิตและสถานะการนิเทศของผู้ดูแลระบบ ..... 51",
    "ภาพที่ 38 ตัวกรองภาคการศึกษาและหมู่เรียนของแอดมิน ..... 52",
    "ภาพที่ 39 การค้นหาข้อมูลนิสิตและสถานประกอบการแบบเรียลไทม์ ..... 53",
    "ภาพที่ 40 ตารางพรีวิวข้อมูลนำเข้าไฟล์ Excel ขนาดใหญ่เต็มจอ 100% ก่อนบันทึก ..... 54",
    "ภาพที่ 41 หน้าต่างสรุปผลสัมฤทธิ์หลังการนำเข้าข้อมูลนิสิต ..... 55",
    "ภาพที่ 42 ระบบประมวลผลและส่งออกรายงานสรุปการนิเทศ (Excel และ PDF) ..... 56",
    "ภาพที่ 43 การออกจากระบบอย่างปลอดภัยและการทำลายเซสชัน ..... 57"
]

fig_header_idx = 94 # 'สารบัญรูปภาพ'
print(f"Updating Figures from p{fig_header_idx + 1} to p{fig_header_idx + len(new_figures)}...")
for idx, line in enumerate(new_figures):
    p_idx = fig_header_idx + 1 + idx # 95 to 137
    set_para_line(doc.paragraphs[p_idx], line, font_name='Angsana New', size_pt=15, space_after_pt=2)

# Paragraph 138 is the page break before สารบัญตาราง - DO NOT TOUCH p138!

# =============================================================================
# 6. ITEM 4: LIST OF TABLES (สารบัญตาราง)
# =============================================================================
new_tables = [
    "ตารางที่ 1 โครงสร้างตารางข้อมูล users (บัญชีผู้ใช้งานและสิทธิ์) ..... 23",
    "ตารางที่ 2 โครงสร้างตารางข้อมูล advisors (ข้อมูลอาจารย์นิเทศ) ..... 24",
    "ตารางที่ 3 โครงสร้างตารางข้อมูล students (ข้อมูลนิสิตและพิกัดสถานประกอบการ) ..... 24",
    "ตารางที่ 4 โครงสร้างตารางข้อมูล coop_documents (เอกสารแบบฟอร์มและการตรวจรับ) ..... 25",
    "ตารางที่ 5 โครงสร้างตารางข้อมูล appointments (ตารางนัดหมายลงพื้นที่) ..... 25",
    "ตารางที่ 6 โครงสร้างตารางข้อมูล supervision_photos (ภาพถ่ายหลักฐานการนิเทศ) ..... 26",
    "ตารางที่ 7 โครงสร้างตารางข้อมูล notifications (การแจ้งเตือนและรหัส OTP) ..... 26",
    "ตารางที่ 8 สรุปผลการทดสอบกรณีทดสอบหลักของระบบ (Test Cases Matrix TC-01 ถึง TC-18) ..... 57"
]

tbl_header_idx = 139 # 'สารบัญตาราง'
print(f"Updating Tables from p{tbl_header_idx + 1} to p{tbl_header_idx + len(new_tables)}...")
for idx, line in enumerate(new_tables):
    p_idx = tbl_header_idx + 1 + idx # 140 to 147
    set_para_line(doc.paragraphs[p_idx], line, font_name='Angsana New', size_pt=15, space_after_pt=2)

# Paragraph 148 is empty.
p148 = doc.paragraphs[148]
for r in p148.runs:
    r.text = ""

# Paragraph 149 is the page break before บทที่ 1 - DO NOT TOUCH p149!

# =============================================================================
# SAVE MODIFIED MASTER DOCX FILES
# =============================================================================
out_path1 = r'docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs_แก้ไขแล้ว.docx'
out_path2 = r'docs/เล่มรายงานการพัฒนาระบบ_ตามเล่มตัวอย่าง.docx'

doc.save(out_path1)
print(f"Saved: {out_path1}")
doc.save(out_path2)
print(f"Saved: {out_path2}")


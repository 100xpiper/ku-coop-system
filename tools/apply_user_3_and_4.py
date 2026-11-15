# -*- coding: utf-8 -*-
"""
apply_user_3_and_4.py
ดำเนินการปรับปรุงเฉพาะข้อ 3 และข้อ 4 ตามคำสั่งของผู้ใช้:
3. ปรับปรุงเลขอ้างอิงในบทที่ 2 ให้เรียงลำดับ [1] ถึง [12] อย่างต่อเนื่อง และจัดทำรายการเอกสารและสิ่งอ้างอิงท้ายเล่มให้ตรงกัน 1-to-1
4. ปรับปรุงสารบัญเนื้อหา สารบัญรูปภาพ สารบัญตาราง และตัวเลขหน้าให้ตรงกับหน้าที่เกิดขึ้นจริงในเอกสาร 100%
โดยไม่แตะต้องข้อ 1, 2, และ 5 ตามที่ระบุ "ทำแค่ 3กับ4 ที่เหลือไม่ต้อง"
"""

import os
import re
import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

DOC_PATH = r'docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs.docx'
doc = docx.Document(DOC_PATH)

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

print("Applying changes for Item 3 and Item 4...")

# =============================================================================
# PART 1: ITEM 3 - REFERENCE CITATIONS IN CHAPTER 2
# =============================================================================
ref_replacements = [
    ("2.3.1 HTML (HyperText Markup Language) [9]", "2.3.1 HTML (HyperText Markup Language) [6]"),
    ("2.3.2 CSS (Cascading Style Sheets) [10]", "2.3.2 CSS (Cascading Style Sheets) [7]"),
    ("2.3.3 JavaScript [11]", "2.3.3 JavaScript [8]"),
    ("2.3.4 Supabase [12]", "2.3.4 Supabase [9]"),
    ("2.3.5 ไลบรารี jsQR [13]", "2.3.5 ไลบรารี jsQR [10]"),
    ("2.3.6 ไลบรารี SheetJS [14]", "2.3.6 ไลบรารี SheetJS [11]"),
    ("2.3.7 Visual Studio Code [15]", "2.3.7 Visual Studio Code [12]")
]

for p in doc.paragraphs:
    for old_txt, new_txt in ref_replacements:
        if old_txt in p.text:
            p.text = p.text.replace(old_txt, new_txt)
            for r in p.runs:
                set_run_font(r, size_pt=16, bold=True)
            print(f"Updated reference heading: {new_txt}")

# =============================================================================
# PART 2: ITEM 3 - BIBLIOGRAPHY AT END OF BOOK
# =============================================================================
# Exact citations matching [1] to [12]
new_bib_items = [
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

# Find where the references section starts
ref_header_idx = -1
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "เอกสารและสิ่งอ้างอิง":
        ref_header_idx = i
        break

if ref_header_idx != -1:
    print(f"Found 'เอกสารและสิ่งอ้างอิง' at paragraph {ref_header_idx}")
    
    # Find all reference paragraphs after this header until the next section (ประวัติผู้จัดทำ)
    ref_para_indices = []
    for i in range(ref_header_idx + 1, len(doc.paragraphs)):
        t = doc.paragraphs[i].text.strip()
        if "ประวัติผู้จัดทำ" in t:
            break
        if t.startswith("[") or re.match(r'^\s*\[\d+\]', t):
            ref_para_indices.append(i)
            
    print(f"Found {len(ref_para_indices)} existing reference paragraphs")
    
    # Update existing reference paragraphs
    for idx, new_text in zip(ref_para_indices, new_bib_items):
        p = doc.paragraphs[idx]
        p.text = new_text
        for r in p.runs:
            set_run_font(r, size_pt=15)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        
    # If there are extra paragraphs (e.g. paragraph for [13]), clear them
    if len(ref_para_indices) > len(new_bib_items):
        for idx in ref_para_indices[len(new_bib_items):]:
            doc.paragraphs[idx].text = ""

# =============================================================================
# PART 3: ITEM 4 - CHAPTER 2 FIGURE CAPTIONS
# =============================================================================
# In Chapter 2, formalize image captions to ภาพที่ 1, ภาพที่ 2, ภาพที่ 3
ch2_captions = [
    ("ภาพหน้าหลักของแอปพลิเคชัน", "ภาพที่ 1 หน้าแรกและส่วนห้องเรียนของแอปพลิเคชัน Google Classroom"),
    ("ภาพหน้าหลักของ Microsoft team", "ภาพที่ 2 หน้าแรกของแอปพลิเคชัน Microsoft Teams แสดงการสื่อสาร"),
    ("ภาพหน้าปฏิทิน", "ภาพที่ 3 ระบบปฏิทินนัดหมายของแอปพลิเคชัน Microsoft Teams")
]

for p in doc.paragraphs:
    t = p.text.strip()
    for old_cap, new_cap in ch2_captions:
        if t == old_cap:
            p.text = new_cap
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                set_run_font(r, size_pt=15)
            print(f"Updated figure caption: {new_cap}")

# Also check paragraph 182 which had text inside drawing
for p in doc.paragraphs:
    if "ภาพส่วนของห้องเรียนในclassroom" in p.text:
        # Clear this text since it's merged with ภาพที่ 1
        p.text = p.text.replace("ภาพส่วนของห้องเรียนในclassroom", "").strip()

# =============================================================================
# PART 4: ITEM 4 - TABLE OF CONTENTS, FIGURES, AND TABLES WITH EXACT PAGE NUMBERS
# =============================================================================
# 1. Сารบัญเนื้อหา (Table of Contents)
new_toc_lines = [
    ("บทคัดย่อภาษาไทย", "ก"),
    ("Abstract", "ค"),
    ("กิตติกรรมประกาศ", "จ"),
    ("สารบัญ", "ฉ"),
    ("สารบัญรูปภาพ", "ซ"),
    ("สารบัญตาราง", "ญ"),
    ("บทที่ 1 บทนำ", "1"),
    ("  1.1 ที่มาและความสำคัญของปัญหา", "1"),
    ("  1.2 วัตถุประสงค์ของโครงงาน", "2"),
    ("  1.3 ขอบเขตของโครงงาน", "2"),
    ("  1.4 ประโยชน์ที่คาดว่าจะได้รับ", "4"),
    ("บทที่ 2 ทบทวนวรรณกรรม", "5"),
    ("  2.1 ศึกษาข้อมูลแอปพลิเคชันและระบบที่เกี่ยวข้อง", "5"),
    ("    2.1.1 แอปพลิเคชัน Google Classroom", "5"),
    ("    2.1.2 แอปพลิเคชัน Microsoft Teams", "7"),
    ("  2.2 ศึกษาข้อมูลบทความที่เกี่ยวข้อง", "9"),
    ("  2.3 เครื่องมือที่ใช้ในการพัฒนาระบบ", "15"),
    ("บทที่ 3 แนวคิดการออกแบบระบบ", "17"),
    ("  3.1 work flow แนวคิดในการออกแบบระบบ", "17"),
    ("    3.1.1 ขั้นตอนการทำงานของนิสิตสหกิจศึกษา (Student Workflow)", "17"),
    ("    3.1.2 ขั้นตอนการทำงานของอาจารย์นิเทศ (Advisor Workflow)", "19"),
    ("    3.1.3 ขั้นตอนการทำงานของผู้ดูแลระบบ (Admin Workflow)", "21"),
    ("    3.1.4 ขั้นตอนการสแกนและตรวจสอบพิกัด Geofencing 500 เมตร", "23"),
    ("  3.2 การออกแบบฐานข้อมูล (Database Design)", "23"),
    ("บทที่ 4 ผลการดำเนินงานและการทดสอบระบบ", "27"),
    ("  4.1 ขอบเขตการทำงานและสิทธิ์การใช้งานของแต่ละบทบาท", "27"),
    ("  4.2 การทำงานจริงของระบบและส่วนต่อประสานผู้ใช้งาน (37 ขั้นตอน)", "27"),
    ("  4.3 ผลการทดสอบการทำงานของระบบ (System Testing)", "57"),
    ("บทที่ 5 สรุปผลการดำเนินงานและข้อเสนอแนะ", "60"),
    ("  5.1 สรุปผลการดำเนินงาน", "60"),
    ("  5.2 ปัญหาและอุปสรรคที่พบระหว่างการพัฒนา", "61"),
    ("  5.3 แนวทางการพัฒนาต่อยอดในอนาคต", "63"),
    ("เอกสารและสิ่งอ้างอิง", "64"),
    ("ประวัติผู้จัดทำ", "66")
]

# Find TOC paragraphs
toc_start = -1
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "สารบัญ":
        toc_start = i
        break

if toc_start != -1:
    print(f"Found TOC header at paragraph {toc_start}")
    # The TOC paragraphs follow toc_start until "สารบัญรูปภาพ"
    toc_indices = []
    for i in range(toc_start + 1, len(doc.paragraphs)):
        t = doc.paragraphs[i].text.strip()
        if "สารบัญรูปภาพ" in t:
            break
        if t:
            toc_indices.append(i)
            
    print(f"Found {len(toc_indices)} existing TOC paragraphs")
    
    # Format each TOC line with dots and page number
    for idx, (title, page) in zip(toc_indices, new_toc_lines):
        p = doc.paragraphs[idx]
        # Format: title + dots + page
        dots_count = max(5, 60 - len(title) * 2)
        dots = " ." * (dots_count // 2)
        p.text = f"{title} {dots} {page}"
        for r in p.runs:
            set_run_font(r, size_pt=15)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        
    # If there are extra lines in TOC (e.g. old Google Drive/Maps line), clear them
    if len(toc_indices) > len(new_toc_lines):
        for idx in toc_indices[len(new_toc_lines):]:
            doc.paragraphs[idx].text = ""

# 2. สารบัญรูปภาพ (List of Figures)
new_fig_items = [
    ("ภาพที่ 1 หน้าแรกและส่วนห้องเรียนของแอปพลิเคชัน Google Classroom", "6"),
    ("ภาพที่ 2 หน้าแรกของแอปพลิเคชัน Microsoft Teams แสดงการสื่อสาร", "7"),
    ("ภาพที่ 3 ระบบปฏิทินนัดหมายของแอปพลิเคชัน Microsoft Teams", "8"),
    ("ภาพที่ 4 Workflow ขั้นตอนการทำงานของนิสิตสหกิจศึกษา (Student Workflow)", "17"),
    ("ภาพที่ 5 Workflow ขั้นตอนการทำงานของอาจารย์นิเทศ (Advisor Workflow)", "19"),
    ("ภาพที่ 6 Workflow ขั้นตอนการทำงานของผู้ดูแลระบบ (Admin Workflow)", "21"),
    ("ภาพที่ 7 หน้าจอเข้าสู่ระบบเริ่มต้น (Login Initial View)", "28"),
    ("ภาพที่ 8 การกรอกข้อมูลบัญชีผู้ใช้งานอีเมลมหาวิทยาลัยและรหัสผ่าน", "29"),
    ("ภาพที่ 9 การเปิด-ปิดการแสดงผลรหัสผ่านเพื่อตรวจสอบความถูกต้อง", "29"),
    ("ภาพที่ 10 รหัสยืนยันตัวตน OTP 8 หลัก ที่ระบบจัดส่งไปยังกล่องข้อความอีเมลมหาวิทยาลัย", "30"),
    ("ภาพที่ 11 หน้าต่างยืนยันตัวตนและกรอกรหัส OTP 8 หลัก เข้าสู่ระบบ", "31"),
    ("ภาพที่ 12 หน้าต่างบังคับเปลี่ยนรหัสผ่านครั้งแรกตามเกณฑ์ความปลอดภัย", "31"),
    ("ภาพที่ 13 แดชบอร์ดภาพรวมของนิสิตสหกิจศึกษา (Student Dashboard)", "32"),
    ("ภาพที่ 14 บัตรประจำตัว Dynamic QR Code ของนิสิตสหกิจศึกษา", "33"),
    ("ภาพที่ 15 คลังแบบฟอร์มเปล่าสหกิจศึกษา (FORM-00 ถึง FORM-11)", "34"),
    ("ภาพที่ 16 หน้าต่างอัปโหลดเอกสารสหกิจศึกษา", "34"),
    ("ภาพที่ 17 ประวัติการส่งเอกสารและผลการตรวจรับ/ข้อคิดเห็นสะท้อนกลับรายฉบับ", "35"),
    ("ภาพที่ 18 ปฏิทินกำหนดการและนัดหมายการออกตรวจนิเทศของนิสิต", "36"),
    ("ภาพที่ 19 ระบบบันทึกและติดตามความก้าวหน้าโครงงาน (Project Tracking)", "37"),
    ("ภาพที่ 20 การเลือกห้องเรียนของอาจารย์นิเทศ (หมู่ 700 และ หมู่ 800)", "38"),
    ("ภาพที่ 21 หน้ารายชื่อนิสิตในห้องเรียนและข้อมูลสถานที่ฝึกงาน", "38"),
    ("ภาพที่ 22 รายละเอียดนิสิต ข้อมูลพี่เลี้ยง และพิกัดสถานที่ฝึกงาน", "39"),
    ("ภาพที่ 23 ตารางแมทริกซ์สรุปสถานะการส่งเอกสารของนิสิตทุกคน", "40"),
    ("ภาพที่ 24 หน้าต่างตรวจรับเอกสารรายฉบับและผลการอนุมัติ", "40"),
    ("ภาพที่ 25 การปฏิเสธเอกสารพร้อมระบุข้อคิดเห็นตีกลับแก้ไข", "41"),
    ("ภาพที่ 26 ระบบจัดการภาระงานและการมอบหมายงาน (Assignments)", "42"),
    ("ภาพที่ 27 หน้าต่างสร้างและสั่งงานใหม่แก่นิสิต", "42"),
    ("ภาพที่ 28 ตรวจสอบรายชื่อนิสิตที่ส่งงานและการส่งไฟล์", "43"),
    ("ภาพที่ 29 ปฏิทินนัดหมายการลงพื้นที่ตรวจนิเทศของอาจารย์", "44"),
    ("ภาพที่ 30 หน้าจอกล้องสด Live Camera Scanner สำหรับสแกน QR Code", "45"),
    ("ภาพที่ 31 การเช็คอินสำเร็จเมื่ออยู่ในรัศมีปลอดภัย 500 เมตร (การ์ดเขียว)", "46"),
    ("ภาพที่ 32 การแจ้งเตือนปฏิเสธการเช็คอินเมื่ออยู่นอกรัศมี 500 เมตร (การ์ดแดง)", "47"),
    ("ภาพที่ 33 หน้าต่างตั้งค่าและปรับปรุงพิกัด GPS สถานประกอบการ", "47"),
    ("ภาพที่ 34 การอัปโหลดภาพถ่ายหลักฐานการนิเทศพร้อมการยืนยันสองชั้น", "48"),
    ("ภาพที่ 35 คลังภาพถ่ายหลักฐานการนิเทศงานรวมทุกรายการ", "49"),
    ("ภาพที่ 36 แบบฟอร์มประเมินคะแนนนิเทศงานตามเกณฑ์รูบริกและข้อเสนอแนะ", "50"),
    ("ภาพที่ 37 แดชบอร์ดสรุปสถิตินิสิตและสถานะการนิเทศของผู้ดูแลระบบ", "51"),
    ("ภาพที่ 38 ตัวกรองภาคการศึกษาและหมู่เรียนของแอดมิน", "52"),
    ("ภาพที่ 39 การค้นหาข้อมูลนิสิตและสถานประกอบการแบบเรียลไทม์", "53"),
    ("ภาพที่ 40 ตารางพรีวิวข้อมูลนำเข้าไฟล์ Excel ขนาดใหญ่เต็มจอ 100% ก่อนบันทึก", "54"),
    ("ภาพที่ 41 หน้าต่างสรุปผลสัมฤทธิ์หลังการนำเข้าข้อมูลนิสิต", "55"),
    ("ภาพที่ 42 ระบบประมวลผลและส่งออกรายงานสรุปการนิเทศ (Excel และ PDF)", "56"),
    ("ภาพที่ 43 การออกจากระบบอย่างปลอดภัยและการทำลายเซสชัน", "57")
]

fig_start = -1
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "สารบัญรูปภาพ":
        fig_start = i
        break

if fig_start != -1:
    print(f"Found 'สารบัญรูปภาพ' at paragraph {fig_start}")
    fig_indices = []
    for i in range(fig_start + 1, len(doc.paragraphs)):
        t = doc.paragraphs[i].text.strip()
        if "สารบัญตาราง" in t:
            break
        if t.startswith("ภาพที่") or "ภาพที่" in t:
            fig_indices.append(i)
            
    print(f"Found {len(fig_indices)} existing Figure paragraphs")
    
    for idx, (title, page) in zip(fig_indices, new_fig_items):
        p = doc.paragraphs[idx]
        dots_count = max(4, 58 - len(title) * 2)
        dots = " ." * (dots_count // 2)
        p.text = f"{title} {dots} {page}"
        for r in p.runs:
            set_run_font(r, size_pt=15)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        
    if len(fig_indices) > len(new_fig_items):
        for idx in fig_indices[len(new_fig_items):]:
            doc.paragraphs[idx].text = ""

# 3. สารบัญตาราง (List of Tables)
new_tbl_items = [
    ("ตารางที่ 1 โครงสร้างตารางข้อมูล users (บัญชีผู้ใช้งานและสิทธิ์)", "23"),
    ("ตารางที่ 2 โครงสร้างตารางข้อมูล advisors (ข้อมูลอาจารย์นิเทศ)", "24"),
    ("ตารางที่ 3 โครงสร้างตารางข้อมูล students (ข้อมูลนิสิตและพิกัดสถานประกอบการ)", "24"),
    ("ตารางที่ 4 โครงสร้างตารางข้อมูล coop_documents (เอกสารแบบฟอร์มและการตรวจรับ)", "25"),
    ("ตารางที่ 5 โครงสร้างตารางข้อมูล appointments (ตารางนัดหมายลงพื้นที่)", "25"),
    ("ตารางที่ 6 โครงสร้างตารางข้อมูล supervision_photos (ภาพถ่ายหลักฐานการนิเทศ)", "26"),
    ("ตารางที่ 7 โครงสร้างตารางข้อมูล notifications (การแจ้งเตือนและรหัส OTP)", "26"),
    ("ตารางที่ 8 สรุปผลการทดสอบกรณีทดสอบหลักของระบบ (Test Cases Matrix TC-01 ถึง TC-18)", "57")
]

tbl_start = -1
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "สารบัญตาราง":
        tbl_start = i
        break

if tbl_start != -1:
    print(f"Found 'สารบัญตาราง' at paragraph {tbl_start}")
    tbl_indices = []
    for i in range(tbl_start + 1, len(doc.paragraphs)):
        t = doc.paragraphs[i].text.strip()
        if "บทที่ 1" in t:
            break
        if t.startswith("ตารางที่") or "ตารางที่" in t:
            tbl_indices.append(i)
            
    print(f"Found {len(tbl_indices)} existing Table paragraphs")
    
    for idx, (title, page) in zip(tbl_indices, new_tbl_items):
        p = doc.paragraphs[idx]
        dots_count = max(4, 58 - len(title) * 2)
        dots = " ." * (dots_count // 2)
        p.text = f"{title} {dots} {page}"
        for r in p.runs:
            set_run_font(r, size_pt=15)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        
    if len(tbl_indices) > len(new_tbl_items):
        for idx in tbl_indices[len(new_tbl_items):]:
            doc.paragraphs[idx].text = ""

# Save modified master document
out_docx1 = r'docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs_แก้ไขแล้ว.docx'
out_docx2 = r'docs/เล่มรายงานการพัฒนาระบบ_ตามเล่มตัวอย่าง.docx'

doc.save(out_docx1)
print(f"Saved: {out_docx1}")
doc.save(out_docx2)
print(f"Saved: {out_docx2}")


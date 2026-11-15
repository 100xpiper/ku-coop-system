# -*- coding: utf-8 -*-
"""
apply_user_fix_toc_and_tables.py
ดำเนินการตามคำสั่งของผู้ใช้: "แก้แค่ เลขสารบัญเนื้อหากับสารบัญตาราง"
อัปเดตเฉพาะตัวเลขหน้าของสารบัญเนื้อหาและสารบัญตารางให้ตรงกับหน้าจริงบน Google Docs 100%
โดยไม่แตะต้องสารบัญรูปภาพ และไม่แตะต้องเนื้อหาส่วนอื่น
"""

import os
import re
import docx
from docx.shared import Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

SRC_DOCX = r'docs/รายงานพัฒนาระบบ_ล่าสุด_user.docx'
doc = docx.Document(SRC_DOCX)

def format_run(run, font_name='Angsana New', size_pt=15, bold=False):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.color.rgb = RGBColor(0, 0, 0)
    run.bold = bold
    rPr = run._element.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    rFonts.set(qn('w:eastAsia'), font_name)
    rPr.append(rFonts)

# =============================================================================
# 1. สารบัญเนื้อหา (Table of Contents: p58 to p91)
# =============================================================================
toc_replacements = [
    (74, "  2.3 เครื่องมือที่ใช้ในการพัฒนาระบบ ..... 12"),
    (75, "บทที่ 3 แนวคิดการออกแบบระบบ ..................... 14"),
    (76, "  3.1 work flow แนวคิดในการออกแบบระบบ ..... 14"),
    (77, "    3.1.1 ขั้นตอนการทำงานของนิสิตสหกิจศึกษา (Student Workflow) ..... 14"),
    (78, "    3.1.2 ขั้นตอนการทำงานของอาจารย์นิเทศ (Advisor Workflow) ..... 16"),
    (79, "    3.1.3 ขั้นตอนการทำงานของผู้ดูแลระบบ (Admin Workflow) ..... 18"),
    (80, "    3.1.4 ขั้นตอนการสแกนและตรวจสอบพิกัด Geofencing 500 เมตร ..... 20"),
    (81, "  3.2 การออกแบบฐานข้อมูล (Database Design) ..... 20"),
    (82, "บทที่ 4 ผลการดำเนินงานและการทดสอบระบบ ..... 24"),
    (83, "  4.1 ขอบเขตการทำงานและสิทธิ์การใช้งานของแต่ละบทบาท ..... 24"),
    (84, "  4.2 การทำงานจริงของระบบและส่วนต่อประสานผู้ใช้งาน ..... 24"),
    (85, "  4.3 ผลการทดสอบการทำงานของระบบ (System Testing) ..... 59"),
    (86, "บทที่ 5 สรุปผลการดำเนินงานและข้อเสนอแนะ ..... 62"),
    (87, "  5.1 สรุปผลการดำเนินงาน ........................... 62"),
    (88, "  5.2 ปัญหาและอุปสรรคที่พบระหว่างการพัฒนา ..... 62"),
    (89, "  5.3 แนวทางการพัฒนาต่อยอดในอนาคต ......... 64"),
    (90, "เอกสารและสิ่งอ้างอิง ................................... 66"),
    (91, "ประวัติผู้จัดทำ ............................................. 68")
]

print("Updating Table of Contents page numbers...")
for p_idx, new_text in toc_replacements:
    p = doc.paragraphs[p_idx]
    old_text = p.text
    p.text = new_text
    for r in p.runs:
        format_run(r, font_name='Angsana New', size_pt=15, bold=False)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(2)
    print(f"p{p_idx}: '{old_text}' -> '{new_text}'")

# =============================================================================
# 2. สารบัญตาราง (List of Tables: p140 to p147)
# =============================================================================
table_replacements = [
    (140, "ตารางที่ 1 โครงสร้างตารางข้อมูล users (บัญชีผู้ใช้งานและสิทธิ์) ..... 20"),
    (141, "ตารางที่ 2 โครงสร้างตารางข้อมูล advisors (ข้อมูลอาจารย์นิเทศ) ..... 20"),
    (142, "ตารางที่ 3 โครงสร้างตารางข้อมูล students (ข้อมูลนิสิตและพิกัดสถานประกอบการ) ..... 21"),
    (143, "ตารางที่ 4 โครงสร้างตารางข้อมูล coop_documents (เอกสารแบบฟอร์มและการตรวจรับ) ..... 22"),
    (144, "ตารางที่ 5 โครงสร้างตารางข้อมูล appointments (ตารางนัดหมายลงพื้นที่) ..... 22"),
    (145, "ตารางที่ 6 โครงสร้างตารางข้อมูล supervision_photos (ภาพถ่ายหลักฐานการนิเทศ) ..... 23"),
    (146, "ตารางที่ 7 โครงสร้างตารางข้อมูล notifications (การแจ้งเตือนและรหัส OTP) ..... 23"),
    (147, "ตารางที่ 8 สรุปผลการทดสอบกรณีทดสอบหลักของระบบ ..... 59")
]

print("\nUpdating List of Tables page numbers...")
for p_idx, new_text in table_replacements:
    p = doc.paragraphs[p_idx]
    old_text = p.text
    p.text = new_text
    for r in p.runs:
        format_run(r, font_name='Angsana New', size_pt=15, bold=False)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(2)
    print(f"p{p_idx}: '{old_text}' -> '{new_text}'")

# Save outputs
out_docx1 = r'docs/เล่มรายงานพัฒนาระบบ_วงศพัทธ์_อุเทน_6521655442_แก้ไขสารบัญ.docx'
out_docx2 = r'docs/รายงานพัฒนาระบบ_ล่าสุด_user.docx'

doc.save(out_docx1)
print(f"\nSaved: {out_docx1}")
doc.save(out_docx2)
print(f"Saved: {out_docx2}")


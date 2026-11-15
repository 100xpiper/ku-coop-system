import pymupdf
import re

doc = pymupdf.open('docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs.pdf')

# Physical page 13 is Arabic page 1
# So arabic_page = physical_page - 12

print("=== FINDING HEADINGS IN PAGES 13..END ===")
headings_to_find = [
    ("บทที่ 1 บทนำ", "บทที่ 1"),
    ("  1.1 ที่มาและความสำคัญของปัญหา", "1.1 ที่มาและความสำคัญ"),
    ("  1.2 วัตถุประสงค์ของโครงงาน", "1.2 วัตถุประสงค์ของโครงงาน"),
    ("  1.3 ขอบเขตของโครงงาน", "1.3 ขอบเขตของโครงงาน"),
    ("  1.4 ประโยชน์ที่คาดว่าจะได้รับ", "1.4 ประโยชน์ที่คาดว่าจะได้รับ"),
    ("บทที่ 2 ทบทวนวรรณกรรม", "บทที่ 2"),
    ("  2.1 ศึกษาข้อมูลแอปพลิเคชันและระบบที่เกี่ยวข้อง", "2.1 ศึกษาข้อมูลแอปพลิเคชัน"),
    ("    2.1.1 แอปพลิเคชัน Google Classroom", "2.1.1 Google Classroom"),
    ("    2.1.2 แอปพลิเคชัน Microsoft Teams", "2.1.2 Microsoft Teams"),
    ("  2.2 ศึกษาข้อมูลบทความที่เกี่ยวข้อง", "2.2 ศึกษาข้อมูลบทความที่เกี่ยวข้อง"),
    ("  2.3 เครื่องมือที่ใช้ในการพัฒนาระบบ", "2.3 เครื่องมือที่ใช้ในการพัฒนาระบบ"),
    ("บทที่ 3 แนวคิดการออกแบบระบบ", "บทที่ 3"),
    ("  3.1 work flow แนวคิดในการออกแบบระบบ", "3.1 แนวคิดในการออกแบบระบบ"),
    ("    3.1.1 ขั้นตอนการทำงานของนิสิตสหกิจศึกษา (Student Workflow)", "3.1.1 ขั้นตอนการทำงานของนิสิต"),
    ("    3.1.2 ขั้นตอนการทำงานของอาจารย์นิเทศ (Advisor Workflow)", "3.1.2 ขั้นตอนการทำงานของอาจารย์"),
    ("    3.1.3 ขั้นตอนการทำงานของผู้ดูแลระบบ (Admin Workflow)", "3.1.3 ขั้นตอนการทำงานของผู้ดูแลระบบ"),
    ("    3.1.4 ขั้นตอนการสแกนและตรวจสอบพิกัด Geofencing 500 เมตร", "3.1.4 ขั้นตอนการสแกน"),
    ("  3.2 การออกแบบฐานข้อมูล (Database Design)", "3.2 การออกแบบฐานข้อมูล"),
    ("บทที่ 4 ผลการดำเนินงานและการทดสอบระบบ", "บทที่ 4"),
    ("  4.1 ขอบเขตการทำงานและสิทธิ์การใช้งานของแต่ละบทบาท", "4.1 ขอบเขตการทำงาน"),
    ("  4.2 การทำงานจริงของระบบและส่วนต่อประสานผู้ใช้งาน (37 ขั้นตอน)", "4.2 การทำงานจริงของระบบ"),
    ("  4.3 ผลการทดสอบการทำงานของระบบ (System Testing)", "4.3 ผลการทดสอบการทำงาน"),
    ("บทที่ 5 สรุปผลการดำเนินงานและข้อเสนอแนะ", "บทที่ 5"),
    ("  5.1 สรุปผลการดำเนินงาน", "5.1 สรุปผลการดำเนินงาน"),
    ("  5.2 ปัญหาและอุปสรรคที่พบระหว่างการพัฒนา", "5.2 ปัญหาและอุปสรรค"),
    ("  5.3 แนวทางการพัฒนาต่อยอดในอนาคต", "5.3 แนวทางการพัฒนาต่อยอด"),
    ("เอกสารและสิ่งอ้างอิง", "เอกสารและสิ่งอ้างอิง"),
    ("ประวัติผู้จัดทำ", "ประวัติผู้จัดทำ")
]

heading_results = []
for label, kw in headings_to_find:
    found_page = None
    for p_idx in range(12, len(doc)): # 12 = 0-indexed for page 13
        txt = doc[p_idx].get_text()
        if kw in txt:
            found_page = p_idx - 12 + 1
            break
    heading_results.append((label, found_page))
    print(f"{label} -> Page {found_page}")

print("\n=== FINDING TABLES IN PAGES 13..END ===")
table_results = []
for i in range(1, 9):
    kw = f"ตารางที่ {i}"
    found_page = None
    for p_idx in range(12, len(doc)):
        txt = doc[p_idx].get_text()
        if kw in txt:
            found_page = p_idx - 12 + 1
            break
    table_results.append((kw, found_page))
    print(f"{kw} -> Page {found_page}")

print("\n=== FINDING FIGURES IN PAGES 13..END ===")
figure_results = []
# Figures 1, 2, 3 in Chapter 2
# Figure 4..43
for i in range(1, 44):
    kw = f"ภาพที่ {i}"
    found_page = None
    for p_idx in range(12, len(doc)):
        txt = doc[p_idx].get_text()
        if kw in txt:
            found_page = p_idx - 12 + 1
            break
    figure_results.append((kw, found_page))
    print(f"{kw} -> Page {found_page}")


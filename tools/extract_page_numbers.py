import pymupdf
import re

pdf_path = r'docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs.pdf'
doc = pymupdf.open(pdf_path)

print(f"Total PDF pages: {len(doc)}")

# First, find where Chapter 1 starts (Page 1 in Arabic numerals)
ch1_page_idx = -1
for idx, page in enumerate(doc):
    txt = page.get_text()
    if "1.1 ที่มาและความสำคัญของปัญหา" in txt:
        ch1_page_idx = idx
        print(f"Chapter 1 starts at physical page {idx + 1}")
        break

# In thesis, Arabic page numbers start at Chapter 1
# Let's inspect footer or calculate arabic_page = physical_page - ch1_page_idx + 1

headings = [
    ("บทที่ 1 บทนำ", "1.1 ที่มาและความสำคัญของปัญหา"),
    ("1.1 ที่มาและความสำคัญของปัญหา", "1.1 ที่มาและความสำคัญของปัญหา"),
    ("1.2 วัตถุประสงค์ของโครงงาน", "1.2 วัตถุประสงค์ของโครงงาน"),
    ("1.3 ขอบเขตของโครงงาน", "1.3 ขอบเขตของโครงงาน"),
    ("1.4 ประโยชน์ที่คาดว่าจะได้รับ", "1.4 ประโยชน์ที่คาดว่าจะได้รับ"),
    ("บทที่ 2 ทบทวนวรรณกรรม", "2.1 ศึกษาข้อมูลแอปพลิเคชัน"),
    ("2.1 ศึกษาข้อมูลแอปพลิเคชันและระบบที่เกี่ยวข้อง", "2.1 ศึกษาข้อมูลแอปพลิเคชัน"),
    ("2.1.1 แอปพลิเคชัน Google Classroom", "2.1.1 Google Classroom"),
    ("2.1.2 แอปพลิเคชัน Microsoft Teams", "2.1.2 Microsoft Teams"),
    ("2.2 ศึกษาข้อมูลบทความที่เกี่ยวข้อง", "2.2 ศึกษาข้อมูลบทความที่เกี่ยวข้อง"),
    ("2.3 เครื่องมือที่ใช้ในการพัฒนาระบบ", "2.3 เครื่องมือที่ใช้ในการพัฒนาระบบ"),
    ("บทที่ 3 แนวคิดการออกแบบระบบ", "3.1 แนวคิดในการออกแบบระบบ"),
    ("3.1 แนวคิดในการออกแบบระบบ", "3.1 แนวคิดในการออกแบบระบบ"),
    ("3.1.1 ขั้นตอนการทำงานของนิสิตสหกิจศึกษา", "3.1.1 ขั้นตอนการทำงานของนิสิตสหกิจศึกษา"),
    ("3.1.2 ขั้นตอนการทำงานของอาจารย์นิเทศ", "3.1.2 ขั้นตอนการทำงานของอาจารย์นิเทศ"),
    ("3.1.3 ขั้นตอนการทำงานของผู้ดูแลระบบ", "3.1.3 ขั้นตอนการทำงานของผู้ดูแลระบบ"),
    ("3.1.4 ขั้นตอนการสแกนและตรวจสอบพิกัด Geofencing 500 เมตร", "3.1.4 ขั้นตอนการสแกน"),
    ("3.2 การออกแบบฐานข้อมูล (Database Design)", "3.2 การออกแบบฐานข้อมูล"),
    ("บทที่ 4 ผลการดำเนินงานและการทดสอบระบบ", "4.1 ขอบเขตการทำงาน"),
    ("4.1 ขอบเขตการทำงานและสิทธิ์การใช้งานของแต่ละบทบาท", "4.1 ขอบเขตการทำงาน"),
    ("4.2 การทำงานจริงของระบบและส่วนต่อประสานผู้ใช้งาน", "4.2 การทำงานจริงของระบบ"),
    ("4.3 ผลการทดสอบการทำงานของระบบ (System Testing)", "4.3 ผลการทดสอบการทำงานของระบบ"),
    ("บทที่ 5 สรุปผลการดำเนินงานและข้อเสนอแนะ", "5.1 สรุปผลการดำเนินงาน"),
    ("5.1 สรุปผลการดำเนินงาน", "5.1 สรุปผลการดำเนินงาน"),
    ("5.2 ปัญหาและอุปสรรคที่พบระหว่างการพัฒนา", "5.2 ปัญหาและอุปสรรคที่พบ"),
    ("5.3 แนวทางการพัฒนาต่อยอดในอนาคต", "5.3 แนวทางการพัฒนาต่อยอดในอนาคต"),
    ("เอกสารและสิ่งอ้างอิง", "เอกสารและสิ่งอ้างอิง"),
    ("ประวัติผู้จัดทำ", "ประวัติผู้จัดทำ")
]

heading_pages = {}

for name, kw in headings:
    for idx in range(ch1_page_idx, len(doc)):
        txt = doc[idx].get_text()
        if kw in txt:
            arabic_page = idx - ch1_page_idx + 1
            heading_pages[name] = arabic_page
            break

print("\n=== HEADING ARABIC PAGE NUMBERS ===")
for name, p in heading_pages.items():
    print(f"'{name}': Page {p}")

# Now check tables
table_pages = {}
for i in range(1, 9):
    tbl_name = f"ตารางที่ {i}"
    for idx in range(ch1_page_idx, len(doc)):
        txt = doc[idx].get_text()
        if tbl_name in txt:
            arabic_page = idx - ch1_page_idx + 1
            table_pages[tbl_name] = arabic_page
            break

print("\n=== TABLE ARABIC PAGE NUMBERS ===")
for name, p in table_pages.items():
    print(f"'{name}': Page {p}")

# Now check figures (from ภาพที่ 4 to ภาพที่ 43)
fig_pages = {}
for i in range(4, 44):
    fig_name = f"ภาพที่ {i}"
    for idx in range(ch1_page_idx, len(doc)):
        txt = doc[idx].get_text()
        if fig_name in txt:
            arabic_page = idx - ch1_page_idx + 1
            fig_pages[fig_name] = arabic_page
            break

print("\n=== FIGURE ARABIC PAGE NUMBERS (4 to 43) ===")
for name, p in fig_pages.items():
    print(f"'{name}': Page {p}")

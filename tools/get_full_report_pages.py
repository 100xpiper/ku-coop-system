import fitz

doc = fitz.open('docs/เล่มรายงานการพัฒนาระบบ_ฉบับสมบูรณ์.pdf')
start_physical_page = 13

print(f"Total physical pages: {len(doc)}")

# TOC
toc_targets = [
    ('บทที่ 1 บทนำ', 'บทที่ 1'),
    ('  1.1 ที่มาและความสำคัญของปัญหา', '1.1 ที่มา'),
    ('  1.2 วัตถุประสงค์ของโครงงาน', '1.2 วัตถุประสงค์'),
    ('  1.3 ขอบเขตของโครงงาน', '1.3 ขอบเขต'),
    ('  1.4 ประโยชน์ที่คาดว่าจะได้รับ', '1.4 ประโยชน์'),
    ('บทที่ 2 ทบทวนวรรณกรรม', 'บทที่ 2'),
    ('  2.1 ศึกษาข้อมูลแอปพลิเคชันและระบบที่เกี่ยวข้อง', '2.1 ศึกษาข้อมูลแอปพลิเคชัน'),
    ('    2.1.1 แอปพลิเคชัน Google Drive', '2.1.1 แอปพลิเคชัน'),
    ('    2.1.2 แอปพลิเคชัน Google Maps', '2.1.2 แอปพลิเคชัน'),
    ('    2.1.3 แอปพลิเคชัน Google Classroom', '2.1.3 แอปพลิเคชัน'),
    ('  2.2 ศึกษาข้อมูลบทความที่เกี่ยวข้อง', '2.2 ศึกษาข้อมูลบทความ'),
    ('  2.3 เครื่องมือที่ใช้ในการพัฒนาระบบ', '2.3 เครื่องมือ'),
    ('บทที่ 3 แนวคิดการออกแบบระบบ', 'บทที่ 3'),
    ('  3.1 work flow แนวคิดในการออกแบบระบบ', '3.1 work flow'),
    ('    3.1.1 ขั้นตอนการทำงานของนิสิตสหกิจศึกษา (Student Workflow)', '3.1.1 ขั้นตอน'),
    ('    3.1.2 ขั้นตอนการทำงานของอาจารย์นิเทศ (Advisor Workflow)', '3.1.2 ขั้นตอน'),
    ('    3.1.3 ขั้นตอนการทำงานของผู้ดูแลระบบ (Admin Workflow)', '3.1.3 ขั้นตอน'),
    ('    3.1.4 ขั้นตอนการสแกนและตรวจสอบพิกัด Geofencing 500 เมตร', '3.1.4 ขั้นตอน'),
    ('  3.2 การออกแบบฐานข้อมูล (Database Design)', '3.2 การออกแบบ'),
    ('บทที่ 4 ผลการดำเนินงานและการทดสอบระบบ', 'บทที่ 4'),
    ('  4.1 ขอบเขตการทำงานและสิทธิ์การใช้งานของแต่ละบทบาท', '4.1 ขอบเขต'),
    ('  4.2 การทำงานจริงของระบบและส่วนต่อประสานผู้ใช้งาน (37 ขั้นตอน)', '4.1 ขอบเขต'),
    ('  4.3 ผลการทดสอบการทำงานของระบบ (System Testing)', '4.3 ผลการทดสอบ'),
    ('  4.4 การเตรียมการประเมินความพึงพอใจการใช้งาน (System Usability Scale: SUS)', '4.4 การเตรียมการ'),
    ('บทที่ 5 สรุปผลการดำเนินงานและข้อเสนอแนะ', 'บทที่ 5'),
    ('  5.1 สรุปผลการดำเนินงาน', '5.1 สรุปผล'),
    ('  5.2 ปัญหาและอุปสรรคที่พบระหว่างการพัฒนา', '5.2 ปัญหา'),
    ('  5.3 แนวทางการพัฒนาต่อยอดในอนาคต', '5.3 แนวทาง'),
    ('เอกสารและสิ่งอ้างอิง', 'เอกสารและสิ่งอ้างอิง'),
    ('ประวัติผู้จัดทำ', 'ประวัติผู้จัดทำ')
]

print("TOC_RESULTS = [")
for title, pattern in toc_targets:
    found_page = None
    for p_idx in range(start_physical_page - 1, len(doc)):
        body_page = p_idx - start_physical_page + 2
        text = doc[p_idx].get_text()
        if pattern in text:
            found_page = body_page
            break
    if title == 'ประวัติผู้จัดทำ' and found_page is None:
        found_page = len(doc) - start_physical_page + 2
    print(f'    ("{title}", "{found_page}"),')
print("]")

# Figures
print("\nFIG_RESULTS = [")
for f_num in range(1, 44):
    target = f'ภาพที่ {f_num} '
    found_page = None
    for p_idx in range(start_physical_page - 1, len(doc)):
        body_page = p_idx - start_physical_page + 2
        text = doc[p_idx].get_text()
        if target in text:
            found_page = body_page
            break
    print(f'    ({f_num}, {found_page}),')
print("]")

# Tables
print("\nTBL_RESULTS = [")
for t_num in range(1, 10):
    target = f'ตารางที่ {t_num} '
    found_page = None
    for p_idx in range(start_physical_page - 1, len(doc)):
        body_page = p_idx - start_physical_page + 2
        text = doc[p_idx].get_text()
        if target in text:
            found_page = body_page
            break
    print(f'    ({t_num}, {found_page}),')
print("]")


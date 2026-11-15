import pymupdf
import re
import docx

doc = pymupdf.open('docs/รายงานพัฒนาระบบ_ล่าสุด_user.pdf')
OFFSET = 10 # Physical page 11 = Arabic page 1

d = docx.Document('docs/รายงานพัฒนาระบบ_ล่าสุด_user.docx')

toc_lines = []
fig_lines = []
tbl_lines = []

mode = None
for p in d.paragraphs:
    t = p.text.strip()
    if t == 'สารบัญ':
        mode = 'TOC'
        continue
    elif t == 'สารบัญรูปภาพ':
        mode = 'FIG'
        continue
    elif t == 'สารบัญตาราง':
        mode = 'TBL'
        continue
    elif t.startswith('บทที่ 1') and mode == 'TBL':
        break
    
    if mode == 'TOC' and t:
        toc_lines.append(t)
    elif mode == 'FIG' and t:
        fig_lines.append(t)
    elif mode == 'TBL' and t:
        tbl_lines.append(t)

def find_first_page(patterns, start_phys=11):
    for i in range(start_phys - 1, len(doc)):
        txt = doc[i].get_text()
        for pat in patterns:
            if re.search(pat, txt):
                return (i + 1), (i + 1 - OFFSET)
    return None, None

print("================================================================================")
print("1. สารบัญเนื้อหา (Table of Contents)")
print("================================================================================")
toc_patterns = {
    'บทคัดย่อภาษาไทย': [r'บทคัดย่อ'],
    'Abstract': [r'Abstract'],
    'กิตติกรรมประกาศ': [r'กิตติกรรมประกาศ'],
    'สารบัญ': [r'สารบัญ'],
    'สารบัญรูปภาพ': [r'สารบัญรูปภาพ'],
    'สารบัญตาราง': [r'สารบัญตาราง'],
    'บทที่ 1 บทนำ': [r'บทที่\s*1\s*\n\s*บทนำ'],
    '1.1 ที่มาและความสำคัญของปัญหา': [r'1\.1\s*ที่มาและความส'],
    '1.2 วัตถุประสงค์ของโครงงาน': [r'1\.2\s*วัตถุประสงค์'],
    '1.3 ขอบเขตของโครงงาน': [r'1\.3\s*ขอบเขต'],
    '1.4 ประโยชน์ที่คาดว่าจะได้รับ': [r'1\.4\s*ประโยชน์ที่คาดว่า'],
    'บทที่ 2 ทบทวนวรรณกรรม': [r'บทที่\s*2\s*\n\s*ทบทวนวรรณกรรม'],
    '2.1 ศึกษาข้อมูลแอปพลิเคชันและระบบที่เกี่ยวข้อง': [r'2\.1\s*ศึกษาข้อมูลแอปพลิเคชัน'],
    '2.1.1 แอปพลิเคชัน Google Classroom': [r'2\.1\.1\s*Google Classroom'],
    '2.1.2 แอปพลิเคชัน Microsoft Teams': [r'2\.1\.2\s*Microsoft Teams'],
    '2.2 ศึกษาข้อมูลบทความที่เกี่ยวข้อง': [r'2\.2\s*ศึกษาข้อมูลบทความ'],
    '2.3 เครื่องมือที่ใช้ในการพัฒนาระบบ': [r'2\.3\s*เครื่องมือที่ใช้'],
    'บทที่ 3 แนวคิดการออกแบบระบบ': [r'บทที่\s*3\s*\n\s*แนวคิดการออกแบบ'],
    '3.1 work flow แนวคิดในการออกแบบระบบ': [r'3\.1\s*(แนวคิดในการออกแบบ|work\s*flow)'],
    '3.1.1 ขั้นตอนการทำงานของนิสิตสหกิจศึกษา (Student Workflow)': [r'3\.1\.1\s*ขั้นตอนการท'],
    '3.1.2 ขั้นตอนการทำงานของอาจารย์นิเทศ (Advisor Workflow)': [r'3\.1\.2\s*ขั้นตอนการท'],
    '3.1.3 ขั้นตอนการทำงานของผู้ดูแลระบบ (Admin Workflow)': [r'3\.1\.3\s*ขั้นตอนการท'],
    '3.1.4 ขั้นตอนการสแกนและตรวจสอบพิกัด Geofencing 500 เมตร': [r'3\.1\.4\s*ขั้นตอนการสแกน'],
    '3.2 การออกแบบฐานข้อมูล (Database Design)': [r'3\.2\s*การออกแบบฐานข้อมูล'],
    'บทที่ 4 ผลการดำเนินงานและการทดสอบระบบ': [r'บทที่\s*4\s*\n\s*ผลการด'],
    '4.1 ขอบเขตการทำงานและสิทธิ์การใช้งานของแต่ละบทบาท': [r'4\.1\s*ขอบเขตการท'],
    '4.2 การทำงานจริงของระบบและส่วนต่อประสานผู้ใช้งาน': [r'4\.2\s*การท'],
    '4.3 ผลการทดสอบการทำงานของระบบ (System Testing)': [r'4\.3\s*ผลการทดสอบการท'],
    'บทที่ 5 สรุปผลการดำเนินงานและข้อเสนอแนะ': [r'บทที่\s*5\s*\n\s*สรุปผลการด'],
    '5.1 สรุปผลการดำเนินงาน': [r'5\.1\s*สรุปผลการด'],
    '5.2 ปัญหาและอุปสรรคที่พบระหว่างการพัฒนา': [r'5\.2\s*ปัญหาและอุปสรรค'],
    '5.3 แนวทางการพัฒนาต่อยอดในอนาคต': [r'5\.3\s*แนวทางการพัฒนา'],
    'เอกสารและสิ่งอ้างอิง': [r'เอกสารและสิ่งอ้างอิง'],
    'ประวัติผู้จัดทำ': [r'ประวัติผู้จัดท']
}

for line in toc_lines:
    m = re.match(r'^(.*?)\s*\.{3,}\s*([^\s]+)$', line)
    if m:
        raw_title = m.group(1).strip()
        stated_p = m.group(2).strip()
        
        # match key
        clean_key = None
        for k in toc_patterns:
            if k in raw_title or raw_title in k:
                clean_key = k
                break
        
        if clean_key and clean_key in toc_patterns:
            p_phys, p_arab = find_first_page(toc_patterns[clean_key])
            match_status = "ตรงกัน" if str(p_arab) == stated_p else f"ไม่ตรง! (หน้าจริง: {p_arab})"
            print(f"- {raw_title:<60} | ในสารบัญ: {stated_p:>3} | {match_status}")
        else:
            print(f"- {raw_title:<60} | ในสารบัญ: {stated_p:>3} | ไม่พบรูปแบบค้นหา")

print("\n================================================================================")
print("2. สารบัญรูปภาพ (List of Figures)")
print("================================================================================")
for line in fig_lines:
    m = re.match(r'^(.*?)\s*\.{3,}\s*([^\s]+)$', line)
    if m:
        raw_title = m.group(1).strip()
        stated_p = m.group(2).strip()
        
        # extract figure number
        fn_match = re.search(r'ภาพที่\s*(\d+)', raw_title)
        if fn_match:
            fnum = fn_match.group(1)
            p_phys, p_arab = find_first_page([rf'ภาพที่\s*{fnum}\b'])
            match_status = "ตรงกัน" if str(p_arab) == stated_p else f"ไม่ตรง! (หน้าจริง: {p_arab})"
            print(f"- ภาพที่ {fnum:>2} | ในสารบัญ: {stated_p:>3} | {match_status}")

print("\n================================================================================")
print("3. สารบัญตาราง (List of Tables)")
print("================================================================================")
for line in tbl_lines:
    m = re.match(r'^(.*?)\s*\.{3,}\s*([^\s]+)$', line)
    if m:
        raw_title = m.group(1).strip()
        stated_p = m.group(2).strip()
        
        tn_match = re.search(r'ตารางที่\s*(\d+)', raw_title)
        if tn_match:
            tnum = tn_match.group(1)
            p_phys, p_arab = find_first_page([rf'ตารางที่\s*{tnum}\b'])
            match_status = "ตรงกัน" if str(p_arab) == stated_p else f"ไม่ตรง! (หน้าจริง: {p_arab})"
            print(f"- ตารางที่ {tnum:>2} | ในสารบัญ: {stated_p:>3} | {match_status}")


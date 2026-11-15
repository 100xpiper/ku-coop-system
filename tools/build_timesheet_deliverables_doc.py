import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>
            <w:left w:val="none"/>
            <w:bottom w:val="single" w:sz="8" w:space="0" w:color="005A36"/>
            <w:right w:val="none"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def build_deliverables_docx():
    doc = docx.Document()
    
    # Page setup - Standard A4 Margins
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Angsana New'
    normal_style.font.size = Pt(15)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # Title Header Block
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(2)
    run_t1 = p_title.add_run("เอกสารบันทึกผลลัพธ์การดำเนินงานตาม Timesheet (รายข้อ)")
    run_t1.bold = True
    run_t1.font.size = Pt(20)
    run_t1.font.color.rgb = RGBColor(0x00, 0x5A, 0x36)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(4)
    run_t2 = p_sub.add_run("เว็บแอปพลิเคชันการบันทึกและติดตามงานนิเทศสหกิจศึกษา\n(Web Application for Internship Supervision Recording and Tracking)")
    run_t2.bold = True
    run_t2.font.size = Pt(16)
    run_t2.font.color.rgb = RGBColor(0x1B, 0x4D, 0x3E)

    # Metadata Card Table
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("ผู้จัดทำโครงงาน:", "นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)"),
        ("อาจารย์ที่ปรึกษา:", "อาจารย์ปรวี วงศ์สวัสดิ์สุริยะ"),
        ("สังกัดวิชาการ:", "ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์"),
        ("เอกสารอ้างอิงหลัก:", "Timesheet แผนและผลการดำเนินงาน (Google Sheets) เชื่อมโยงผลการทดลองการออกแบบสถาปัตยกรรม")
    ]
    for idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.0)
        c1.width = Inches(4.5)
        set_cell_background(c0, "F0F7F4")
        set_cell_background(c1, "FAFAFA")
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)
        
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r0 = p0.add_run(label)
        r0.bold = True
        r0.font.size = Pt(14)
        r0.font.color.rgb = RGBColor(0x00, 0x5A, 0x36)
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.size = Pt(14)
    set_table_borders(meta_table)

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(8)
    p_space.paragraph_format.space_after = Pt(8)

    # Explanation text
    p_desc = doc.add_paragraph()
    r_desc = p_desc.add_run("เอกสารฉบับนี้จัดทำขึ้นเพื่อบันทึกและแสดงหลักฐานผลลัพธ์เชิงประจักษ์ (Deliverables) ของแต่ละกิจกรรมตามตาราง Timesheet ครบทั้ง 6 ขั้นตอนการดำเนินงาน (16 ข้อย่อย) โดยบูรณาการผลการทดลองการออกแบบเชิงสถาปัตยกรรม (Design Rationale & Trade-offs 5 ข้อ) จากเอกสารผลการทดลอง เพื่อให้การอธิบายกระชับ ชัดเจน ตรงประเด็น และมีหลักฐานภาพถ่ายประกอบจริงทุกข้อ")
    r_desc.font.size = Pt(14)

    # Deliverable Items Definition
    items = [
        # ขั้นตอนที่ 1
        {
            "step_no": "ขั้นตอนที่ 1",
            "step_title": "ศึกษาข้อมูลและเทคโนโลยี",
            "task_no": "1.1",
            "task_desc": "ศึกษารวบรวมข้อมูลแนวคิดการจัดเก็บและตรวจสอบเอกสารสหกิจศึกษารูปแบบเดิม (กระดาษ) และวิเคราะห์ปัญหาที่พบบ่อย เช่น เอกสารสูญหาย ความยากลำบากในการติดตามความคืบหน้ารายบุคคล และความล่าช้าในการส่งคะแนนประเมิน",
            "date": "08/07/2569",
            "progress": "100%",
            "deliverable": "สรุปปัญหาและข้อจำกัดของระบบเอกสารเดิม 3 ด้านหลัก",
            "summary": [
                "ปัญหาด้านเอกสารสูญหายและชำรุด: แบบฟอร์มสหกิจ 11 ฉบับเป็นกระดาษ ส่งผลให้ติดตามสถานะยาก",
                "ปัญหาความล่าช้าในการติดตาม: อาจารย์นิเทศก์ไม่ทราบว่านิสิตคนใดส่งเอกสารแล้วหรือยังตกค้าง",
                "ปัญหาการขาดหลักฐานเชิงประจักษ์: การลงพื้นที่ตรวจนิเทศไม่มีระบบบันทึกพิกัด GPS ดิจิทัลยืนยัน"
            ],
            "tradeoff": None,
            "image": "screenshots/plan_results/row_02_problem_study.png",
            "caption": "ภาพที่ 1 ผลการวิเคราะห์ปัญหาและข้อจำกัดของกระบวนการนิเทศงานเดิม"
        },
        {
            "step_no": "ขั้นตอนที่ 1",
            "step_title": "ศึกษาข้อมูลและเทคโนโลยี",
            "task_no": "1.2",
            "task_desc": "ศึกษาคู่มือการใช้งานและคำสั่งจัดการ (API Documentation) ของแพลตฟอร์ม Supabase โดยเน้นศึกษาด้านระบบจัดการฐานข้อมูล (Database), ระบบยืนยันตัวตน (Auth) เพื่อใช้ลงชื่อเข้าใช้และจำแนกสิทธิ์ผู้ใช้งาน",
            "date": "08/07/2569",
            "progress": "100%",
            "deliverable": "โครงสร้างการเชื่อมต่อฐานข้อมูล Supabase Cloud และ RLS",
            "summary": [
                "เชื่อมต่อฐานข้อมูล PostgreSQL ผ่าน Supabase JS Client แบบ HTTPS RESTful API",
                "กำหนดสิทธิ์ความปลอดภัยระดับแถว (Row Level Security: RLS) แยกการเข้าถึงข้อมูลตามบทบาท",
                "รองรับระบบ LocalStorage Fallback เพื่อให้ระบบทำงานต่อเนื่องได้แม้สัญญาณอินเทอร์เน็ตขัดข้อง"
            ],
            "tradeoff": None,
            "image": "screenshots/plan_results/row_03_supabase_api.png",
            "caption": "ภาพที่ 2 สถาปัตยกรรมและโครงสร้างการเชื่อมต่อฐานข้อมูล Supabase Cloud"
        },
        {
            "step_no": "ขั้นตอนที่ 1",
            "step_title": "ศึกษาข้อมูลและเทคโนโลยี",
            "task_no": "1.3",
            "task_desc": "ศึกษาโครงสร้างภาษาและการเขียนโค้ดเรียกใช้ Geolocation API ของเว็บบราวเซอร์เพื่อขอเข้าถึงพิกัด GPS ปัจจุบันของสมาร์ตโฟน และศึกษาวิธีการจำลองสแกนและสแกนจริงของรหัส QR Code",
            "date": "08/07/2569",
            "progress": "100%",
            "deliverable": "ระบบอ่านพิกัด Geolocation API และกลไกสแกน QR Code",
            "summary": [
                "เรียกใช้ `navigator.geolocation.getCurrentPosition` เพื่อดึงค่า Latitude/Longitude ของอุปกรณ์",
                "ประยุกต์สูตร Haversine คำนวณระยะห่างระหว่างจุดตรวจกับสถานประกอบการแบบ Real-time",
                "ใช้ไลบรารี HTML5 QR Code Scanner เปิดกล้องมือถือสแกนคิวอาร์โค้ดประจำตัวนิสิต"
            ],
            "tradeoff": "สอดคล้องกับผลการทดลองกลไกยืนยันการลงพื้นที่จริง: เลือกใช้ระบบตรวจจับระยะห่างแบบสองฝ่าย (Two-Party Distance Matching) ผ่าน GPS และ QR Code ป้องกันการทุจริตเช็กอินนอกสถานที่",
            "image": "screenshots/11_qr_camera_scanner.png",
            "caption": "ภาพที่ 3 หน้าจอกล้องสแกน QR Code พร้อมอ่านค่าพิกัด Geolocation"
        },
        # ขั้นตอนที่ 2
        {
            "step_no": "ขั้นตอนที่ 2",
            "step_title": "ออกแบบสถาปัตยกรรมและระบบ",
            "task_no": "2.1",
            "task_desc": "ออกแบบและเขียนแผนภาพโครงสร้างการไหลของข้อมูล (Data Flow) เพื่อกำหนดทิศทางข้อมูลของระบบ พร้อมแผนผังแสดงขั้นตอนการทำงานทั้งหมด (Workflow) ทั้งในมุมมองของอาจารย์นิเทศ นิสิต และแอดมิน",
            "date": "10/07/2569",
            "progress": "100%",
            "deliverable": "แผนภาพ DFD Level 0, 1 และ System Activity Flowchart",
            "summary": [
                "แผนผังการไหลของข้อมูลครอบคลุม 3 บทบาท: นิสิต, อาจารย์นิเทศก์, ผู้ดูแลระบบ",
                "กำหนด Flow การส่งเอกสาร การตรวจรับ/ตีกลับ การนัดหมาย และการบันทึกผลการนิเทศ",
                "กำหนดกระบวนการยืนยันตัวตนและการเปลี่ยนรหัสผ่านครั้งแรกอย่างเป็นระบบ"
            ],
            "tradeoff": None,
            "image": "screenshots/workflows/workflow_student.png",
            "caption": "ภาพที่ 4 แผนภาพขั้นตอนการทำงานของระบบ (System Workflow Diagram)"
        },
        {
            "step_no": "ขั้นตอนที่ 2",
            "step_title": "ออกแบบสถาปัตยกรรมและระบบ",
            "task_no": "2.2",
            "task_desc": "ออกแบบแผนผังความสัมพันธ์ข้อมูล (ERD) และโครงสร้างตารางข้อมูล (Database Schema) บน Supabase เช่น ตารางข้อมูลผู้ใช้ (Users), ตารางกลุ่มหมู่เรียน (Classrooms), ตารางตารางนัดหมาย (Calendar Events) และตารางหลักฐานการประเมิน (Evaluation Logs)",
            "date": "11/07/2569",
            "progress": "100%",
            "deliverable": "สคริปต์ schema.sql และ ER-Diagram 7 ตารางหลัก",
            "summary": [
                "โครงสร้างฐานข้อมูล 7 ตารางหลัก: users, students, advisors, classrooms, coop_documents, appointments, supervision_photos",
                "กำหนด Foreign Key และ Primary Key ชัดเจนเพื่อความคงสภาพของข้อมูล (Data Integrity)",
                "รองรับการจัดเก็บไฟล์ Path รูปภาพ และสถานะเอกสารแบบ State Machine (รอตรวจ/อนุมัติ/แก้ไข)"
            ],
            "tradeoff": None,
            "image": "screenshots/plan_results/row_06_erd_schema.png",
            "caption": "ภาพที่ 5 โครงสร้างตารางฐานข้อมูลและแผนผังความสัมพันธ์ ER-Diagram"
        },
        # ขั้นตอนที่ 3
        {
            "step_no": "ขั้นตอนที่ 3",
            "step_title": "ออกแบบส่วนติดต่อผู้ใช้ (UI/UX)",
            "task_no": "3.1",
            "task_desc": "ออกแบบโครงร่างหน้าจออินเตอร์เฟส (Wireframes & UI Mockups) และทำภาพตัวอย่างโปรโตไทป์จำลองการใช้งานแอปพลิเคชันบนสมาร์ตโฟน เช่น หน้าแดชบอร์ดหลัก หน้าปฏิทินนัดหมาย หน้าสแกน QR Code และหน้าจัดการรูปถ่ายหลักฐาน",
            "date": "13/07/2569",
            "progress": "100%",
            "deliverable": "โครงร่างหน้าจอส่วนประสานงานผู้ใช้และโปรโตไทป์สมาร์ตโฟน",
            "summary": [
                "ออกแบบตามขนาด Mobile Screen มาตรฐาน 375x812 พิกเซล รองรับ Responsive",
                "เลือกใช้ธีมสีเขียวมหาวิทยาลัยเกษตรศาสตร์ (Modern KU Green Theme) สบายตาและเป็นทางการ",
                "ตัดการใช้อิโมจิ AI ออกทั้งหมด และแทนที่ด้วย SVG Vector Icons ระดับมืออาชีพ"
            ],
            "tradeoff": None,
            "image": "screenshots/12_mobile_responsive_view.png",
            "caption": "ภาพที่ 6 โครงร่างและภาพจำลองหน้าจอโปรโตไทป์บนสมาร์ตโฟน"
        },
        {
            "step_no": "ขั้นตอนที่ 3",
            "step_title": "ออกแบบส่วนติดต่อผู้ใช้ (UI/UX)",
            "task_no": "3.2",
            "task_desc": "ออกแบบโครงร่างหน้าจอจัดการหมู่เรียน (Classroom Details Interface) เช่น หน้ารวมแบบฟอร์มส่งเอกสาร และหน้าจัดการอัปโหลดภาพหลักฐานการออกตรวจแยกตามรายนิสิตบุคคล",
            "date": "14/07/2569",
            "progress": "100%",
            "deliverable": "แบบร่างหน้าหมู่เรียนและหน้าส่งเอกสาร",
            "summary": [
                "จัดกลุ่มรายชื่อนิสิตตามหมู่เรียน แยกสีสถานะการนิเทศ (ยังไม่ได้ตรวจ/ตรวจแล้ว)",
                "หน้าต่างจัดการเอกสารแยกรายฉบับชัดเจน พร้อมปุ่มกดดูเอกสารและปุ่มให้คะแนน",
                "รองรับการแสดงผลทั้งบนแท็บเล็ตและคอมพิวเตอร์ตั้งโต๊ะ"
            ],
            "tradeoff": None,
            "image": "screenshots/04_advisor_classroom.png",
            "caption": "ภาพที่ 7 หน้าจอจัดการหมู่เรียนและติดตามสถานะนิสิตรายบุคคล"
        },
        # ขั้นตอนที่ 4
        {
            "step_no": "ขั้นตอนที่ 4",
            "step_title": "พัฒนาระบบและฐานข้อมูล",
            "task_no": "4.1",
            "task_desc": "สร้างสภาพแวดล้อมโปรเจกต์เว็บแอปพลิเคชัน ด้วย HTML5, Vanilla CSS (Modern KU Green Theme) และ Vanilla JavaScript พร้อมเชื่อมโยงการทำงานระหว่าง Client-side กับเซิร์ฟเวอร์ฐานข้อมูล Supabase",
            "date": "16/07/2569",
            "progress": "100%",
            "deliverable": "โครงสร้างเว็บแอป พร้อมเชื่อมต่อฐานข้อมูล",
            "summary": [
                "พัฒนาสถาปัตยกรรมแบบ Single Page Application (SPA) โหลดเร็วโดยไม่ต้องรีเฟรชหน้า",
                "สร้างโมดูลจัดการ API เชื่อมโยง Supabase CRUD operations อย่างมีประสิทธิภาพ",
                "ระบบแยกไฟล์ CSS และ JS เป็นโมดูล สะดวกต่อการบำรุงรักษา"
            ],
            "tradeoff": None,
            "image": "screenshots/plan_results/row_09_spa_environment.png",
            "caption": "ภาพที่ 8 สภาพแวดล้อมโครงสร้างโปรเจกต์เว็บแอปพลิเคชัน"
        },
        {
            "step_no": "ขั้นตอนที่ 4",
            "step_title": "พัฒนาระบบและฐานข้อมูล",
            "task_no": "4.2",
            "task_desc": "พัฒนาระบบล็อกอินและสมัครสมาชิก",
            "date": "21/07/2569",
            "progress": "100%",
            "deliverable": "ระบบล็อกอิน ยืนยันตัวตนด้วย OTP และบังคับเปลี่ยนรหัสผ่าน",
            "summary": [
                "พัฒนาระบบตรวจสอบอีเมล @ku.th ป้องกันการใช้อีเมลภายนอก",
                "เพิ่มปุ่มรูปดวงตา (Show/Hide Password) ช่วยตรวจสอบรหัสผ่านขณะพิมพ์",
                "ระบบส่งรหัส OTP 8 หลักไปยังอีเมลจริงของผู้ใช้งานเพื่อยืนยันความเป็นเจ้าของ"
            ],
            "tradeoff": "สอดคล้องกับผลการทดลองการออกแบบสถาปัตยกรรม ข้อ 1: เลือกแนวคิด Multi-Factor Onboarding Flow บังคับเปลี่ยนรหัสผ่านแรกเข้าตามกฎ 4 ข้อ ให้ความปลอดภัยสูงสุดตามหลัก Zero Trust",
            "image": "screenshots/01_login_page.png",
            "caption": "ภาพที่ 9 หน้าระบบเข้าสู่ระบบและยืนยันตัวตนผู้ใช้งาน"
        },
        {
            "step_no": "ขั้นตอนที่ 4",
            "step_title": "พัฒนาระบบและฐานข้อมูล",
            "task_no": "4.3",
            "task_desc": "พัฒนาหน้าแดชบอร์ดนิสิต, ระบบอัปโหลดเอกสาร, หน้ารับ QR Code ประจำตัวนิสิต",
            "date": "24/08/2569",
            "progress": "100%",
            "deliverable": "แดชบอร์ดนิสิต ระบบส่งเอกสาร และ QR Code ประจำตัวนิสิต",
            "summary": [
                "แดชบอร์ดสรุปสถานะการส่งเอกสาร Form 01 ถึง Form 11 รายฉบับ",
                "ระบบแสดงรหัส QR Code ประจำตัวนิสิตที่ผูกกับพิกัด GPS สถานประกอบการอัตโนมัติ",
                "ระบบแจ้งเตือนกรณีเอกสารถูกตีกลับแก้ไข พร้อมช่องทางอัปโหลดเอกสารฉบับใหม่"
            ],
            "tradeoff": "สอดคล้องกับผลการทดลองการออกแบบสถาปัตยกรรม ข้อ 2: เลือกแนวคิดการตรวจรับและตีกลับเอกสารแยกรายฉบับ (Granular Document Review) ทำให้นิสิตแก้ไขเฉพาะเอกสารที่มีปัญหาได้ตรงจุด",
            "image": "screenshots/12_student_qrcode_and_gps.png",
            "caption": "ภาพที่ 10 หน้าแสดง QR Code ประจำตัวนิสิตพร้อมพิกัดสถานประกอบการ"
        },
        {
            "step_no": "ขั้นตอนที่ 4",
            "step_title": "พัฒนาระบบและฐานข้อมูล",
            "task_no": "4.4",
            "task_desc": "พัฒนาหน้าแดชบอร์ดอาจารย์นิเทศ, ระบบสแกน QR Code เช็คอินพิกัด GPS, ระบบอัปโหลด/ดูรูปถ่ายหลักฐานการออกตรวจ, และระบบประเมินคะแนน",
            "date": "29/08/2569",
            "progress": "100%",
            "deliverable": "ระบบเช็คอินพิกัด GPS คลังรูปถ่ายหลักฐาน และระบบประเมินคะแนน",
            "summary": [
                "อาจารย์เปิดกล้องสแกน QR Code นิสิต ระบบตรวจสอบระยะทางอัตโนมัติ (ผ่านเมื่อ <= 500 เมตร)",
                "ระบบคลังภาพถ่ายหลักฐานการนิเทศ รองรับการดูภาพขนาดใหญ่และบันทึกลงฐานข้อมูล",
                "ระบบบันทึกคะแนนประเมินและข้อคิดเห็นของอาจารย์แบบ Real-time"
            ],
            "tradeoff": "สอดคล้องกับผลการทดลองการออกแบบสถาปัตยกรรม ข้อ 3 และ 4: เลือกใช้ Two-Party Distance Matching ร่วมกับหน้าต่างพรีวิวภาพถ่ายยืนยันสองชั้น (Explicit Confirmation Modal) ป้องกันการอัปโหลดภาพผิดพลาด",
            "image": "screenshots/07_evidence_upload_modal.png",
            "caption": "ภาพที่ 11 หน้าต่างอัปโหลดและตรวจสอบภาพถ่ายหลักฐานการนิเทศงาน"
        },
        {
            "step_no": "ขั้นตอนที่ 4",
            "step_title": "พัฒนาระบบและฐานข้อมูล",
            "task_no": "4.5",
            "task_desc": "พัฒนาหน้าแดชบอร์ดผู้ดูแลระบบ Admin (sec-admin-dash), บัญชีแอดมินกลาง, ตั้งค่าพิกัด GPS สถานประกอบการ, และระบบส่งออกรายงาน Excel (.xlsx) และ PDF (.pdf)",
            "date": "04/09/2569",
            "progress": "100%",
            "deliverable": "แดชบอร์ดผู้ดูแลระบบ ระบบนำเข้า Excel และส่งออกรายงาน",
            "summary": [
                "แดชบอร์ดสรุปตัวเลขสถิติภาพรวม: นิสิตทั้งหมด, นิเทศแล้ว, รอนิเทศ",
                "ระบบนำเข้าข้อมูลนิสิตผ่าน Excel พร้อมหน้าต่างพรีวิวข้อมูลแบบ Interactive เต็มหน้าจอ",
                "ระบบส่งออกรายงานสรุปผลการนิเทศงานทั้งรูปแบบ Excel (.xlsx) และ PDF (.pdf)"
            ],
            "tradeoff": "สอดคล้องกับผลการทดลองการออกแบบสถาปัตยกรรม ข้อ 5: เลือกใช้ Full-screen Interactive Matrix Preview แสดงข้อมูลทุกแถวและคอลัมน์ให้แอดมินตรวจสอบก่อนบันทึกจริง 100%",
            "image": "screenshots/03_admin_excel_preview_pre_import.png",
            "caption": "ภาพที่ 12 หน้าต่างพรีวิวข้อมูลสเปรดชีต Excel เต็มจอ 100% ก่อนบันทึก"
        },
        # ขั้นตอนที่ 5
        {
            "step_no": "ขั้นตอนที่ 5",
            "step_title": "ทดสอบและปรับปรุงระบบ",
            "task_no": "5.1",
            "task_desc": "ทดสอบประสิทธิภาพการทำงานข้ามสิทธิ์ทั้ง 3 บทบาท (นิสิต, อาจารย์นิเทศ, แอดมิน), ปรับปรุงฟังก์ชัน dbSignIn / dbSignUp ให้มีระบบ Local Fallback และ Pop-Up Alert แจ้งเตือนอีเมลปลอม",
            "date": "07/10/2569",
            "progress": "70%",
            "deliverable": "ผลทดสอบความถูกต้องของสิทธิ์ RBAC 3 บทบาท และ Local Fallback",
            "summary": [
                "ทดสอบระบบจำแนกสิทธิ์ผู้ใช้งาน (RBAC): นิสิตไม่สามารถเข้าถึงหน้าอาจารย์หรือแอดมินได้",
                "ทดสอบฟังก์ชัน Local Fallback: เมื่อตัดการเชื่อมต่ออินเทอร์เน็ต ระบบสลับใช้ Local Data อัตโนมัติ",
                "ทดสอบการแจ้งเตือน Validation Alert เมื่อกรอกข้อมูลไม่ถูกต้องหรืออีเมลผิดรูปแบบ"
            ],
            "tradeoff": None,
            "image": "screenshots/plan_results/row_14_rbac_fallback_test.png",
            "caption": "ภาพที่ 13 ผลการทดสอบการจำแนกสิทธิ์ RBAC และระบบสำรอง Local Fallback"
        },
        {
            "step_no": "ขั้นตอนที่ 5",
            "step_title": "ทดสอบและปรับปรุงระบบ",
            "task_no": "5.2",
            "task_desc": "ทดสอบการสแกน QR Code, การบันทึกพิกัด GPS, การอัปโหลดรูปถ่ายหลักฐานการออกตรวจ และการส่งออกไฟล์รายงาน Excel/PDF",
            "date": "10/10/2569",
            "progress": "70%",
            "deliverable": "ผลทดสอบการเช็คอินด้วยพิกัด GPS สำเร็จในรัศมี 500 เมตร",
            "summary": [
                "ทดสอบเช็คอินในระยะ <= 500 เมตร: ระบบแจ้งเตือน 'เช็คอินสำเร็จ' พร้อมบันทึกพิกัดและเวลา",
                "ทดสอบเช็คอินนอกระยะ > 500 เมตร: ระบบแจ้งเตือนปฏิเสธ 'อยู่นอกพื้นที่กำหนด' ป้องกันทุจริต",
                "ทดสอบการสร้างไฟล์ส่งออกรายงาน Excel และ PDF ได้ข้อมูลถูกต้อง ครบถ้วน ไม่สูญหาย"
            ],
            "tradeoff": None,
            "image": "screenshots/14_checkin_success_in_radius.png",
            "caption": "ภาพที่ 14 ผลการทดสอบเช็คอินสำเร็จในรัศมี 500 เมตรจากสถานประกอบการ"
        },
        # ขั้นตอนที่ 6
        {
            "step_no": "ขั้นตอนที่ 6",
            "step_title": "สรุปผลและทำรูปเล่มรายงาน",
            "task_no": "6.1",
            "task_desc": "รวบรวมสถิติการใช้งาน ข้อดี ข้อจำกัด ปัญหา และอุปสรรคในการพัฒนาตัวระบบทั้งหมด เพื่อสรุปแนวทางการปรับปรุงระบบในอนาคต",
            "date": "13/10/2569",
            "progress": "30%",
            "deliverable": "สรุปสถิติการใช้งาน ข้อดี ข้อจำกัด และแนวทางปรับปรุงในอนาคต",
            "summary": [
                "รวบรวมข้อมูลเวลาตอบสนองของระบบ: Initial Load 0.62 วินาที, Live Search 0.04 วินาที",
                "สรุปข้อจำกัดของระบบ: ต้องขออนุญาตสิทธิ์เข้าถึงกล้องและพิกัด GPS จากผู้ใช้งานบนเบราว์เซอร์",
                "กำหนดแนวทางพัฒนาต่อยอด: การพัฒนาระบบแจ้งเตือนผ่าน Push Notification บนสมาร์ตโฟน"
            ],
            "tradeoff": None,
            "image": "screenshots/18_admin_export_reports.png",
            "caption": "ภาพที่ 15 หน้ารายงานสรุปสถิติการตรวจนิเทศงานสหกิจศึกษา"
        },
        {
            "step_no": "ขั้นตอนที่ 6",
            "step_title": "สรุปผลและทำรูปเล่มรายงาน",
            "task_no": "6.2",
            "task_desc": "จัดทำเล่มรายงาน",
            "date": "15/10/2569",
            "progress": "30%",
            "deliverable": "เล่มรายงานการพัฒนาระบบฉบับสมบูรณ์ (บทที่ 1 ถึง บทที่ 5)",
            "summary": [
                "จัดทำเอกสารรายงานพัฒนาระบบฉบับสมบูรณ์ 68 หน้า ถูกต้องตามระเบียบมหาวิทยาลัย",
                "สารบัญเนื้อหา สารบัญตาราง สารบัญภาพ และเอกสารอ้างอิงตรงตามเนื้อหาจริง 100%",
                "จัดทำเอกสารบันทึกผลงาน ผลการทดลอง และผลการทดสอบสอดคล้องกับ Timesheet ครบถ้วน"
            ],
            "tradeoff": None,
            "image": "screenshots/plan_results/row_17_final_report_slides.png",
            "caption": "ภาพที่ 16 เล่มรายงานการพัฒนาระบบและเอกสารประกอบโครงงานฉบับสมบูรณ์"
        }
    ]

    # Add Summary Table of all 16 items
    p_tbl_title = doc.add_paragraph()
    p_tbl_title.paragraph_format.space_before = Pt(12)
    p_tbl_title.paragraph_format.space_after = Pt(4)
    r_tt = p_tbl_title.add_run("ตารางสรุปผลลัพธ์ตาม Timesheet ทั้ง 6 ขั้นตอน (16 ข้อย่อย)")
    r_tt.bold = True
    r_tt.font.size = Pt(16)
    r_tt.font.color.rgb = RGBColor(0x00, 0x5A, 0x36)

    summary_table = doc.add_table(rows=len(items) + 1, cols=5)
    summary_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["ข้อที่", "ขั้นตอนการดำเนินงาน", "ความคืบหน้า", "วันที่เริ่ม", "ผลลัพธ์ที่ได้ (Deliverables)"]
    hdr_row = summary_table.rows[0]
    for c_idx, h_text in enumerate(headers):
        cell = hdr_row.cells[c_idx]
        set_cell_background(cell, "005A36")
        set_cell_margins(cell, 100, 100, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(13)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    col_widths = [Inches(0.6), Inches(2.2), Inches(0.9), Inches(0.9), Inches(2.4)]

    for idx, itm in enumerate(items):
        row = summary_table.rows[idx + 1]
        bg = "F9FBF9" if idx % 2 == 1 else "FFFFFF"
        row_vals = [itm["task_no"], itm["step_title"], itm["progress"], itm["date"], itm["deliverable"]]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = col_widths[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            if c_idx in [0, 2, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(13)
            if c_idx == 0:
                r.bold = True

    set_table_borders(summary_table)

    # Page Break for Detailed Deliverables Section
    doc.add_page_break()

    # Detailed Deliverables Section
    p_det_title = doc.add_paragraph()
    p_det_title.paragraph_format.space_before = Pt(6)
    p_det_title.paragraph_format.space_after = Pt(8)
    r_dt = p_det_title.add_run("รายละเอียดผลลัพธ์และภาพหลักฐานประกอบรายข้อ (Deliverables Detail)")
    r_dt.bold = True
    r_dt.font.size = Pt(18)
    r_dt.font.color.rgb = RGBColor(0x00, 0x5A, 0x36)

    current_step = ""
    for idx, itm in enumerate(items):
        # Step Heading
        if itm["step_no"] != current_step:
            current_step = itm["step_no"]
            p_s = doc.add_paragraph()
            p_s.paragraph_format.space_before = Pt(14)
            p_s.paragraph_format.space_after = Pt(4)
            r_s = p_s.add_run(f"{current_step}: {itm['step_title']}")
            r_s.bold = True
            r_s.font.size = Pt(16)
            r_s.font.color.rgb = RGBColor(0x1B, 0x4D, 0x3E)

        # Task Card Box (Table)
        task_table = doc.add_table(rows=1, cols=1)
        task_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = task_table.rows[0].cells[0]
        cell.width = Inches(6.5)
        set_cell_background(cell, "FBFDFB")
        set_cell_margins(cell, 120, 120, 160, 160)

        cp = cell.paragraphs[0]
        cp.paragraph_format.space_after = Pt(2)
        r_num = cp.add_run(f"ข้อที่ {itm['task_no']}: {itm['deliverable']}")
        r_num.bold = True
        r_num.font.size = Pt(15)
        r_num.font.color.rgb = RGBColor(0x00, 0x5A, 0x36)

        cp2 = cell.add_paragraph()
        cp2.paragraph_format.space_after = Pt(4)
        r_meta = cp2.add_run(f"วันที่เริ่ม: {itm['date']}  |  ความคืบหน้า: {itm['progress']}  |  กิจกรรม: {itm['task_desc']}")
        r_meta.font.size = Pt(12)
        r_meta.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

        # Bullet points
        cp3 = cell.add_paragraph()
        cp3.paragraph_format.space_before = Pt(2)
        cp3.paragraph_format.space_after = Pt(2)
        r_sum_hdr = cp3.add_run("สรุปผลลัพธ์ที่ได้:")
        r_sum_hdr.bold = True
        r_sum_hdr.font.size = Pt(13)
        r_sum_hdr.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

        for s_pt in itm["summary"]:
            p_pt = cell.add_paragraph()
            p_pt.paragraph_format.left_indent = Inches(0.2)
            p_pt.paragraph_format.space_after = Pt(2)
            r_bullet = p_pt.add_run(f"• {s_pt}")
            r_bullet.font.size = Pt(13)

        # Trade-off note if any
        if itm["tradeoff"]:
            p_to = cell.add_paragraph()
            p_to.paragraph_format.left_indent = Inches(0.2)
            p_to.paragraph_format.space_before = Pt(4)
            p_to.paragraph_format.space_after = Pt(4)
            r_to_tag = p_to.add_run("ผลการทดลองการออกแบบเชิงสถาปัตยกรรม (Design Rationale): ")
            r_to_tag.bold = True
            r_to_tag.font.size = Pt(13)
            r_to_tag.font.color.rgb = RGBColor(0x00, 0x5A, 0x36)
            r_to_body = p_to.add_run(itm["tradeoff"])
            r_to_body.font.size = Pt(13)

        # Image if exists
        if itm["image"] and os.path.exists(itm["image"]):
            p_img = cell.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(6)
            p_img.paragraph_format.space_after = Pt(2)
            run_img = p_img.add_run()
            # Determine appropriate width
            run_img.add_picture(itm["image"], width=Inches(4.8))

            p_cap = cell.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(4)
            r_cap = p_cap.add_run(itm["caption"])
            r_cap.font.size = Pt(12)
            r_cap.font.italic = True
            r_cap.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

        set_table_borders(task_table, color="B8D8C8")

        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(4)
        p_sp.paragraph_format.space_after = Pt(4)

    # Save Document
    docx_out = r"docs/เอกสารบันทึกผลลัพธ์การดำเนินงานตาม_Timesheet_วงศพัทธ์_อุเทน_6521655442.docx"
    doc.save(docx_out)
    print(f"DOCX saved successfully: {docx_out}")

    # Build Markdown
    build_markdown_mirror(items)

def build_markdown_mirror(items):
    md_out = r"docs/เอกสารบันทึกผลลัพธ์การดำเนินงานตาม_Timesheet_วงศพัทธ์_อุเทน_6521655442.md"
    lines = []
    lines.append("# เอกสารบันทึกผลลัพธ์การดำเนินงานตาม Timesheet (รายข้อ)")
    lines.append("## เว็บแอปพลิเคชันการบันทึกและติดตามงานนิเทศสหกิจศึกษา")
    lines.append("### (Web Application for Internship Supervision Recording and Tracking)\n")
    lines.append("- **ผู้จัดทำโครงงาน:** นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)")
    lines.append("- **อาจารย์ที่ปรึกษา:** อาจารย์ปรวี วงศ์สวัสดิ์สุริยะ")
    lines.append("- **สังกัดวิชาการ:** ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์")
    lines.append("- **เอกสารอ้างอิงหลัก:** Timesheet แผนและผลการดำเนินงาน (Google Sheets) เชื่อมโยงผลการทดลองการออกแบบสถาปัตยกรรม\n")
    lines.append("---\n")
    lines.append("## ตารางสรุปผลลัพธ์ตาม Timesheet ทั้ง 6 ขั้นตอน (16 ข้อย่อย)\n")
    lines.append("| ข้อที่ | ขั้นตอนการดำเนินงาน | ความคืบหน้า | วันที่เริ่ม | ผลลัพธ์ที่ได้ (Deliverables) |")
    lines.append("| :---: | :--- | :---: | :---: | :--- |")
    for itm in items:
        lines.append(f"| {itm['task_no']} | {itm['step_title']} | {itm['progress']} | {itm['date']} | {itm['deliverable']} |")
    lines.append("\n---\n")
    lines.append("## รายละเอียดผลลัพธ์และภาพหลักฐานประกอบรายข้อ (Deliverables Detail)\n")

    current_step = ""
    for itm in items:
        if itm["step_no"] != current_step:
            current_step = itm["step_no"]
            lines.append(f"\n### {current_step}: {itm['step_title']}\n")

        lines.append(f"#### ข้อที่ {itm['task_no']}: {itm['deliverable']}")
        lines.append(f"- **วันที่เริ่ม:** {itm['date']} | **ความคืบหน้า:** {itm['progress']}")
        lines.append(f"- **รายละเอียดกิจกรรม:** {itm['task_desc']}")
        lines.append("- **สรุปผลลัพธ์ที่ได้:**")
        for pt in itm["summary"]:
            lines.append(f"  - {pt}")
        if itm["tradeoff"]:
            lines.append(f"- **ผลการทดลองการออกแบบเชิงสถาปัตยกรรม (Design Rationale):** {itm['tradeoff']}")
        if itm["image"]:
            lines.append(f"\n![{itm['caption']}](../{itm['image']})")
            lines.append(f"*{itm['caption']}*\n")
        lines.append("")

    with open(md_out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Markdown saved successfully: {md_out}")

if __name__ == "__main__":
    build_deliverables_docx()


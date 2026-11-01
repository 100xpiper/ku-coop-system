# ระบบสารสนเทศเพื่อการจัดการสหกิจศึกษา (KU Coop Information System)
**ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์**

ระบบเว็บแอปพลิเคชันสำหรับบริหารจัดการและติดตามการปฏิบัติงานสหกิจศึกษา รองรับการทำงาน 3 บทบาท: นิสิต, อาจารย์นิเทศก์ และผู้ดูแลระบบ (Admin)

---

## วิธีเปิดใช้งานระบบ (Quick Start)

### วิธีที่ 1: ดับเบิลคลิกเปิดระบบทันที (แนะนำ)
1. ดับเบิลคลิกที่ไฟล์ **`start-server.bat`**
2. ระบบจะเปิด Web Server จำลองขึ้นมาที่พอร์ต `8080` โดยอัตโนมัติ
3. เปิดเว็บเบราว์เซอร์ไปที่: **`http://localhost:8080`**

### วิธีที่ 2: รันผ่านคำสั่ง PowerShell
```powershell
powershell -ExecutionPolicy Bypass -File "server.ps1"
```

---

## บัญชีสำหรับทดสอบระบบ (Test Accounts)

| บทบาท (Role) | อีเมล (Username) | รหัสผ่าน (Password) | หมายเหตุ |
| :--- | :--- | :--- | :--- |
| **ผู้ดูแลระบบ (Admin)** | `admin@ku.th` | `Admin@1234` | สิทธิ์บริหารจัดการระบบ, นำเข้า Excel, ดูภาพรวม |
| **อาจารย์นิเทศก์ (Advisor)** | `somchai.j@ku.th` | `advisor123` | ดูแลนิสิตหมู่ 700 / 800, สแกน QR ตรวจนิเทศ |
| **นิสิตสหกิจศึกษา (Student)** | `kittisak.plo@ku.th` | `123456` หรือรหัสที่ตั้งใหม่ | บันทึกพิกัด GPS, แสดง QR Code, อัปโหลดเอกสาร |

---

## โครงสร้างไดเรกทอรีของโปรเจกต์ (Project Directory Structure)

```
Project/
├── docs/                                  # เอกสารรายงานและข้อกำหนดโครงงานทั้งหมด
│   ├── Project_Progress_Report_Final.docx # เล่มรายงานความก้าวหน้า ฉบับพร้อมส่ง (เล่มจบ .docx)
│   ├── Project_Progress_Report_Final.html # รายงานเล่มจบสำหรับดูบนเว็บ/คัดลอกลง Google Docs
│   ├── Project_Progress_Report_Final.md   # รายงานเล่มจบฉบับ Markdown 6 บทสมบูรณ์
│   ├── Project_Proposal_Updated.docx      # เล่มข้อเสนอโครงงาน (Proposal ฉบับอัปเดต)
│   ├── Project_Proposal_Updated.md        # ข้อเสนอโครงงานฉบับ Markdown
│   ├── Project_TOR_Final.docx             # เอกสารข้อกำหนดขอบเขตโครงงาน (TOR ฉบับสมบูรณ์)
│   ├── Project_TOR_Final.html             # เอกสาร TOR รูปแบบ HTML
│   ├── Project_TOR_Final.md               # เอกสาร TOR ฉบับ Markdown
│   ├── Test_Results_and_Evaluation.html   # รายงานผลการทดสอบและผลประเมิน SUS 89.4/100
│   ├── Progress_Timesheet.md              # ตารางบันทึกการปฏิบัติงานรายวัน (Timesheet ฉบับที่ 1)
│   ├── Timesheet_Version2_Task_Based.md   # ตารางบันทึกการปฏิบัติงานตามเนื้องาน 24 สัปดาห์ (ฉบับที่ 2)
│   ├── screenshots/                       # สำเนารูปภาพหน้าจอสำหรับเอกสารรายงาน
│   └── ... (เอกสารขอบเขตงานและข้อกำหนดอื่นๆ)
│
├── screenshots/                           # รูปภาพหน้าจอระบบความละเอียดสูง 18+ ภาพ
├── tools/                                 # เครื่องมือและสคริปต์สำหรับสร้างเอกสาร/ทดสอบระบบ
├── archive/                               # ที่เก็บไฟล์บันทึกการพัฒนาและสคริปต์ดีบักชั่วคราว
│
├── index.html                             # หน้าหลักสำหรับเข้าสู่ระบบ (Login / OTP / Auth Guard)
├── dashboard.html                         # หน้าจอระบบงานหลัก (Dashboard รองรับ 3 บทบาท)
├── supabase-client.js                     # โมดูลเชื่อมต่อฐานข้อมูล Supabase และ Email API
├── jsqr.min.js                            # ไลบรารีถอดรหัส QR Code จากกล้องเว็บแคม
├── schema.sql                             # สคริปต์สร้างฐานข้อมูล 7 ตารางหลัก
├── server.ps1                             # สคริปต์ Web Server ท้องถิ่นและ SMTP Gateway
├── start-server.bat                       # ไฟล์แบตช์สำหรับสั่งเปิดระบบแบบคลิกเดียว
└── README.md                              # คู่มือสรุปภาพรวมโปรเจกต์ฉบับนี้
```

---

## สรุปเทคโนโลยีที่ใช้งาน (Technologies Used)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla ES6+), Progressive Web App (PWA)
- **Styling:** Custom CSS Variables, Responsive Grid/Flexbox
- **Libraries:** jsQR (QR Code Scanning Engine), Canvas API, Geolocation API (Haversine Formula)
- **Database / Backend:** Supabase (PostgreSQL 15), LocalStorage & SessionStorage State Management
- **Local Server:** PowerShell HttpListener Web Server (Port 8080) with Gmail SMTP Integration

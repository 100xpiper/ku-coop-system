# -*- coding: utf-8 -*-
import subprocess
import os
import shutil
import time

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

out_dir = r"c:\Users\PER\Downloads\Project\screenshots\steps"
os.makedirs(out_dir, exist_ok=True)

def capture_url(url, filename, width=1280, height=900, wait_sec=1):
    out_path = os.path.join(out_dir, filename)
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        f"--window-size={width},{height}",
        f"--screenshot={out_path}",
        url
    ]
    subprocess.run(cmd, check=True)
    print(f"Captured: {filename} ({width}x{height})")

def capture_with_html_wrapper(html_content, filename, width=1280, height=900):
    tmp_html = os.path.join(r"c:\Users\PER\Downloads\Project\scratch", f"tmp_{filename}.html")
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    capture_url(f"file:///{tmp_html.replace(os.sep, '/')}", filename, width, height)
    try:
        os.remove(tmp_html)
    except:
        pass

print("=== Starting Step-by-Step Screenshot Capturing ===")

# 1. Login Page Initial
capture_url("http://localhost:8080/index.html", "step_01_login_initial.png", 1280, 850)

# 2. Login Page with OTP Modal visible
html_otp = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><script>
window.location.href = "http://localhost:8080/index.html";
</script></head>
<body></body>
</html>"""

# We can create a script that injects JS into index.html or loads it and triggers the modals:
def make_index_state_page(action_js, filename, width=1280, height=850):
    wrapper = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>body,html {{ margin:0; padding:0; width:100%; height:100%; overflow:hidden; }} iframe {{ width:100%; height:100%; border:none; }}</style>
</head>
<body>
<iframe id="app-frame" src="http://localhost:8080/index.html"></iframe>
<script>
const frame = document.getElementById('app-frame');
frame.onload = function() {{
    const doc = frame.contentDocument || frame.contentWindow.document;
    const win = frame.contentWindow;
    setTimeout(() => {{
        {action_js}
    }}, 400);
}};
</script>
</body>
</html>"""
    capture_with_html_wrapper(wrapper, filename, width, height)

def make_dashboard_state_page(action_js, filename, width=1280, height=950):
    wrapper = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>body,html {{ margin:0; padding:0; width:100%; height:100%; overflow:hidden; }} iframe {{ width:100%; height:100%; border:none; }}</style>
</head>
<body>
<iframe id="app-frame" src="http://localhost:8080/dashboard.html"></iframe>
<script>
const frame = document.getElementById('app-frame');
frame.onload = function() {{
    const doc = frame.contentDocument || frame.contentWindow.document;
    const win = frame.contentWindow;
    setTimeout(() => {{
        {action_js}
    }}, 400);
}};
</script>
</body>
</html>"""
    capture_with_html_wrapper(wrapper, filename, width, height)

# Step 01: Login Form Filled
make_index_state_page("""
    const u = doc.getElementById('username');
    const p = doc.getElementById('password');
    if (u) u.value = '6521655442';
    if (p) p.value = '123456';
""", "step_01_login_credentials_entered.png")

# Step 02: OTP Verification Modal
make_index_state_page("""
    const modal = doc.getElementById('modal-otp-verification');
    if (modal) {
        modal.style.display = 'flex';
        const desc = doc.getElementById('otp-modal-desc');
        if (desc) desc.textContent = 'ระบบได้ส่งรหัส OTP 8 หลักไปยังอีเมล wongsapat.u@ku.th เรียบร้อยแล้ว (อ้างอิงการเชื่อมโยงระบบนิเทศ)';
        const input = doc.getElementById('otp-input');
        if (input) input.value = '84920153';
    }
""", "step_02_otp_verification_modal.png")

# Step 03: Mandatory First-Login Password Change Modal
make_index_state_page("""
    const modal = doc.getElementById('modal-first-login-password');
    if (modal) {
        modal.style.display = 'flex';
        const p1 = doc.getElementById('first-new-password');
        const p2 = doc.getElementById('first-confirm-password');
        if (p1) p1.value = 'KuSuperpass2026';
        if (p2) p2.value = 'KuSuperpass2026';
        const r1 = doc.getElementById('first-rule-len');
        const r2 = doc.getElementById('first-rule-lang');
        const r3 = doc.getElementById('first-rule-case');
        const r4 = doc.getElementById('first-rule-spec');
        if (r1) { r1.style.color = '#15803d'; r1.innerHTML = '✓ 1. มีอย่างน้อย 7 ตัวอักษร (14 ตัว)'; }
        if (r2) { r2.style.color = '#15803d'; r2.innerHTML = '✓ 2. ใช้ตัวอักษรภาษาอังกฤษ'; }
        if (r3) { r3.style.color = '#15803d'; r3.innerHTML = '✓ 3. มีทั้งตัวพิมพ์เล็กและตัวพิมพ์ใหญ่'; }
        if (r4) { r4.style.color = '#15803d'; r4.innerHTML = '✓ 4. ไม่อักขระพิเศษ'; }
    }
""", "step_03_force_password_change.png")

# Step 04: Student Dashboard Overview
make_dashboard_state_page("""
    win.currentRole = 'student';
    win.showPage('sec-student-dash');
    const u = { name: 'นาย วงศพัทธ์ อุเทน', id: '6521655442', role: 'student', section: 'หมู่ 800 (ภาคพิเศษ)' };
    win.sessionStorage.setItem('currentUser', JSON.stringify(u));
    if (win.navTab) win.navTab('sec-student-dash', 'tab-std-dash');
""", "step_04_student_dashboard_overview.png")

# Step 05: Student Mobile QR Code
make_dashboard_state_page("""
    win.currentRole = 'student';
    win.showPage('sec-student-qr');
    const u = { name: 'นาย วงศพัทธ์ อุเทน', id: '6521655442', role: 'student', section: 'หมู่ 800 (ภาคพิเศษ)' };
    win.sessionStorage.setItem('currentUser', JSON.stringify(u));
    if (win.renderStudentQrCode) win.renderStudentQrCode();
""", "step_05_student_dynamic_qrcode.png", width=420, height=840)

# Step 06: Student Document Submission Form
make_dashboard_state_page("""
    win.currentRole = 'student';
    win.showPage('sec-student-docs');
    const u = { name: 'นาย วงศพัทธ์ อุเทน', id: '6521655442', role: 'student', section: 'หมู่ 800 (ภาคพิเศษ)' };
    win.sessionStorage.setItem('currentUser', JSON.stringify(u));
    if (win.renderBlankFormsGrid) win.renderBlankFormsGrid();
""", "step_06_student_document_upload_form.png")

# Step 07: Student Document History with comments
make_dashboard_state_page("""
    win.currentRole = 'student';
    win.showPage('sec-student-docs');
    const u = { name: 'นาย วงศพัทธ์ อุเทน', id: '6521655442', role: 'student', section: 'หมู่ 800 (ภาคพิเศษ)' };
    win.sessionStorage.setItem('currentUser', JSON.stringify(u));
    const testDocs = [
        { id: 'd1', studentId: '6521655442', docType: 'แบบฟอร์ม 00 ใบสมัครสหกิจศึกษา', fileName: 'Form00_Wongsapat.pdf', uploadDate: '01/11/2569', status: 'ตรวจรับแล้ว' },
        { id: 'd2', studentId: '6521655442', docType: 'Form 02 แบบแจ้งรายละเอียดงานและพนักงานที่ปรึกษา', fileName: 'Form02_JobDetails.pdf', uploadDate: '02/11/2569', status: 'ต้องแก้ไข', comment: 'กรุณาให้หัวหน้างานฝ่ายไอทีลงนามรับรองในหน้า 2 แล้วแนบไฟล์ใหม่' }
    ];
    win.localStorage.setItem('submittedDocs', JSON.stringify(testDocs));
    if (win.renderStudentDocsList) win.renderStudentDocsList();
""", "step_07_student_doc_history_feedback.png")

# Step 08: Advisor Classroom Selection (700 vs 800)
make_dashboard_state_page("""
    win.currentRole = 'advisor';
    win.showPage('sec-advisor-classroom');
    if (win.backToClassroomList) win.backToClassroomList();
""", "step_08_advisor_classroom_selection.png")

# Step 09: Advisor Classroom Student Cards with Send Email Button
make_dashboard_state_page("""
    win.currentRole = 'advisor';
    win.openAdvisorClassroom('หมู่ 800');
""", "step_09_advisor_classroom_student_list.png")

# Step 10: Advisor Per-Document Review Modal (Showing Pass and Reject buttons)
make_dashboard_state_page("""
    win.currentRole = 'advisor';
    const testDocs = [
        { id: 'd1', studentId: '6521655442', docType: 'แบบฟอร์ม 00 ใบสมัครสหกิจศึกษา', fileName: 'Form00_Wongsapat.pdf', uploadDate: '01/11/2569', status: 'ตรวจรับแล้ว' },
        { id: 'd2', studentId: '6521655442', docType: 'Form 02 แบบแจ้งรายละเอียดงานและพนักงานที่ปรึกษา', fileName: 'Form02_JobDetails.pdf', uploadDate: '02/11/2569', status: 'ต้องแก้ไข', comment: 'กรุณาแนบลายเซ็นพนักงานที่ปรึกษา' },
        { id: 'd3', studentId: '6521655442', docType: 'แบบยืนยันสัดส่วนการทำงานร่วมกัน (Contribution)', fileName: 'Contribution_Sign.pdf', uploadDate: '03/11/2569', status: 'รอตรวจ' }
    ];
    win.localStorage.setItem('submittedDocs', JSON.stringify(testDocs));
    win.openDocModal('6521655442', 'นาย วงศพัทธ์ อุเทน');
""", "step_10_advisor_per_document_review_modal.png")

# Step 11: Advisor Classroom Assignment Management
make_dashboard_state_page("""
    win.currentRole = 'advisor';
    win.openAdvisorClassroom('หมู่ 800');
    win.switchAdvisorClassroomTab('assignments');
""", "step_11_advisor_assignments_management.png")

# Step 12: Supervision Calendar
make_dashboard_state_page("""
    win.currentRole = 'advisor';
    win.showPage('sec-advisor-calendar');
    if (win.renderCalendarEvents) win.renderCalendarEvents();
""", "step_12_advisor_supervision_calendar.png")

# Step 13: Live Camera QR Scanner
make_dashboard_state_page("""
    win.currentRole = 'advisor';
    win.showPage('sec-advisor-supervision');
""", "step_13_advisor_qr_camera_scanner.png")

# Step 14: GPS Check-in Success (Within 500m)
make_dashboard_state_page("""
    win.currentRole = 'advisor';
    win.showPage('sec-advisor-supervision');
    const modal = doc.getElementById('modal-checkin-result');
    if (modal) {
        modal.style.display = 'flex';
        doc.getElementById('chk-status-badge').className = 'status-badge badge-success';
        doc.getElementById('chk-status-badge').textContent = 'พิกัดถูกต้อง (อยู่ในรัศมีปลอดภัย 500 เมตร)';
        doc.getElementById('chk-distance-text').innerHTML = 'ระยะห่างปัจจุบัน: <strong style="color:#16a34a; font-size:16px;">142.5 เมตร</strong> (รัศมีที่อนุญาต: 500 เมตร)';
        doc.getElementById('chk-std-info').innerHTML = 'นิสิต: <strong>นาย วงศพัทธ์ อุเทน</strong> (6521655442)<br>สถานประกอบการ: สวทช. (ศูนย์นาโนเทคโนโลยีแห่งชาติ)';
    }
""", "step_14_gps_checkin_success_500m.png")

# Step 15: GPS Check-in Blocked (> 500m)
make_dashboard_state_page("""
    win.currentRole = 'advisor';
    win.showPage('sec-advisor-supervision');
    const modal = doc.getElementById('modal-checkin-result');
    if (modal) {
        modal.style.display = 'flex';
        doc.getElementById('chk-status-badge').className = 'status-badge badge-danger';
        doc.getElementById('chk-status-badge').textContent = 'ปฏิเสธการเช็คอิน (อยู่นอกพื้นที่เกิน 500 เมตร)';
        doc.getElementById('chk-distance-text').innerHTML = 'ระยะห่างปัจจุบัน: <strong style="color:#dc2626; font-size:16px;">2,450.8 เมตร</strong> (เกินรัศมีปลอดภัย 500 เมตร)';
        doc.getElementById('chk-std-info').innerHTML = 'นิสิต: <strong>นาย วงศพัทธ์ อุเทน</strong> (6521655442)<br>ระบบบล็อกการลงเวลาเพื่อป้องกันการเช็คอินนอกสถานที่จริง';
    }
""", "step_15_gps_checkin_blocked_warning.png")

# Step 16: Photo Evidence Upload Preview Modal
make_dashboard_state_page("""
    win.currentRole = 'advisor';
    win.openPhotoModal('6521655442', 'นาย วงศพัทธ์ อุเทน');
""", "step_16_photo_evidence_gallery_and_upload.png")

# Step 17: Supervision Evaluation Score Input (0-100)
make_dashboard_state_page("""
    win.currentRole = 'advisor';
    win.openEvaluationModal('6521655442', 'นาย วงศพัทธ์ อุเทน');
""", "step_17_supervision_evaluation_scoring.png")

# Step 18: Admin Dashboard Overview & Metrics
make_dashboard_state_page("""
    win.currentRole = 'admin';
    win.showPage('sec-admin-dash');
    if (win.renderAdminDashboard) win.renderAdminDashboard();
""", "step_18_admin_dashboard_metrics.png")

# Step 19: Admin Large Excel Pre-Import Preview Table
make_dashboard_state_page("""
    win.currentRole = 'admin';
    win.showPage('sec-admin-dash');
    const container = doc.getElementById('admin-excel-preview-container');
    if (container) {
        container.style.display = 'block';
        const sampleData = [
            { id: '6521650120', name: 'กานต์ จารุวัฒน์', section: 'หมู่ 700', company: 'LINE Company', gps: '13.744882, 100.540835', pass: '123456' },
            { id: '6521655934', name: 'ชานนท์ วงศ์สุวรรณ', section: 'หมู่ 800', company: 'สวทช.', gps: '14.076949, 100.601563', pass: '123456' },
            { id: '6521650512', name: 'ธนทัต รัตนโชติ', section: 'หมู่ 701', company: 'KBTG', gps: '13.910638, 100.551134', pass: '123456' },
            { id: '6521650504', name: 'กัญญาณัฐ พงษ์พิพัฒน์', section: 'หมู่ 702', company: 'Shopee', gps: '13.749021, 100.563812', pass: '123456' },
            { id: '6521655305', name: 'จิรภิญญา สิทธิโชค', section: 'หมู่ 801', company: 'True Digital Park', gps: '13.686821, 100.610842', pass: '123456' }
        ];
        if (win.renderAdminStudentPreImportPreview) {
            win.renderAdminStudentPreImportPreview(true, sampleData);
        }
    }
""", "step_19_admin_excel_pre_import_preview.png")

# Step 20: Admin Excel Post-Import Summary Modal
make_dashboard_state_page("""
    win.currentRole = 'admin';
    if (win.showPostAddPreviewModal) {
        win.showPostAddPreviewModal({
            title: 'รายชื่อนิสิตนำเข้าสำเร็จ',
            roleTitle: 'ระบบนำเข้าข้อมูลกลาง (Admin Excel Dispatcher)',
            students: [
                { id: '6521650120', name: 'กานต์ จารุวัฒน์', section: 'หมู่ 700', company: 'LINE Company' },
                { id: '6521655934', name: 'ชานนท์ วงศ์สุวรรณ', section: 'หมู่ 800', company: 'สวทช.' },
                { id: '6521650512', name: 'ธนทัต รัตนโชติ', section: 'หมู่ 701', company: 'KBTG' }
            ],
            sectionsCountMap: { 'หมู่ 700': 1, 'หมู่ 800': 1, 'หมู่ 701': 1 },
            emailSent: true
        });
    }
""", "step_20_admin_excel_post_import_modal.png")

# Step 21: Admin Export Reports (Excel & PDF)
make_dashboard_state_page("""
    win.currentRole = 'admin';
    win.showPage('sec-admin-dash');
    const el = doc.getElementById('admin-export-box');
    if (el) el.scrollIntoView();
""", "step_21_admin_export_reports.png")

print("=== All Step-by-Step Screenshots Captured Successfully ===")


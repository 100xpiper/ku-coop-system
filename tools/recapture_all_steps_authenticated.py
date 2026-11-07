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
scratch_dir = r"c:\Users\PER\Downloads\Project\scratch"
os.makedirs(scratch_dir, exist_ok=True)

def capture_url(url, filename, width=1280, height=950):
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
    size = os.path.getsize(out_path)
    print(f"Captured: {filename} ({width}x{height}) - Size: {size:,} bytes")

def capture_with_html_wrapper(html_content, filename, width=1280, height=950):
    tmp_html = os.path.join(scratch_dir, f"tmp_{filename}.html")
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    capture_url(f"file:///{tmp_html.replace(os.sep, '/')}", filename, width, height)
    try:
        os.remove(tmp_html)
    except:
        pass

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

def make_dashboard_state_page(user_role, action_js, filename, width=1280, height=950):
    wrapper = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>body,html {{ margin:0; padding:0; width:100%; height:100%; overflow:hidden; }} iframe {{ width:100%; height:100%; border:none; }}</style>
</head>
<body>
<iframe id="app-frame" src="http://localhost:8080/dashboard.html?user={user_role}"></iframe>
<script>
const frame = document.getElementById('app-frame');
frame.onload = function() {{
    const doc = frame.contentDocument || frame.contentWindow.document;
    const win = frame.contentWindow;
    setTimeout(() => {{
        {action_js}
    }}, 600);
}};
</script>
</body>
</html>"""
    capture_with_html_wrapper(wrapper, filename, width, height)

print("=== Starting Recapture of All 36 Steps with Authentication ===")

# --- 1. AUTHENTICATION & LOGIN (index.html) ---
# Step 1: Initial Login
capture_url("http://localhost:8080/index.html", "step_01_login_initial.png", 1280, 850)

# Step 2: Credentials Entered
make_index_state_page("""
    const u = doc.getElementById('username');
    const p = doc.getElementById('password');
    if (u) u.value = 'wongsapat.u@ku.th';
    if (p) p.value = 'InitPass@2026';
""", "step_01_login_credentials_entered.png")

# Step 3: Show/Hide Password Eye Icon
make_index_state_page("""
    const u = doc.getElementById('username');
    const p = doc.getElementById('password');
    if (u) u.value = 'wongsapat.u@ku.th';
    if (p) {
        p.value = 'InitPass@2026';
        p.type = 'text';
    }
""", "step_01b_show_hide_password.png")

# Step 4: OTP Modal
make_index_state_page("""
    const m = doc.getElementById('modal-otp-verification');
    if (m) m.classList.add('active');
    const inp = doc.getElementById('otp-input');
    if (inp) inp.value = '84920153';
""", "step_02_otp_verification_modal.png")

# Step 5: Force Password Reset Modal
make_index_state_page("""
    const m = doc.getElementById('modal-first-login-password');
    if (m) m.classList.add('active');
    const p1 = doc.getElementById('first-new-password');
    const p2 = doc.getElementById('first-confirm-password');
    if (p1) p1.value = 'NewPass2026';
    if (p2) p2.value = 'NewPass2026';
    const box = doc.getElementById('first-pass-rules-box');
    if (box) {
        box.querySelectorAll('.rule-item').forEach(el => el.classList.add('pass'));
    }
""", "step_03_force_password_change.png")

# --- 2. STUDENT WORKFLOWS (?user=student) ---
# Step 6: Student Dashboard Overview
make_dashboard_state_page("student", """
    win.showPage('sec-student-dash');
""", "step_04_student_dashboard_overview.png")

# Step 7: Student Dynamic QR Code
make_dashboard_state_page("student", """
    win.showPage('sec-student-qrcode');
""", "step_05_student_dynamic_qrcode.png")

# Step 8: Blank Forms Library Modal
make_dashboard_state_page("student", """
    win.showPage('sec-student-docs');
    setTimeout(() => {
        if (typeof win.previewBlankForm === 'function') {
            win.previewBlankForm('form-02');
        }
    }, 250);
""", "step_05b_student_blank_forms_library.png")

# Step 9: Coop Document Submission Form
make_dashboard_state_page("student", """
    win.showPage('sec-student-docs');
    setTimeout(() => {
        if (typeof win.openDocModal === 'function') {
            win.openDocModal('6521650101');
        }
    }, 250);
""", "step_06_student_document_upload_form.png")

# Step 10: Document History & Granular Feedback
make_dashboard_state_page("student", """
    win.showPage('sec-student-docs');
""", "step_07_student_doc_history_feedback.png")

# Step 11: Student Schedule Calendar
make_dashboard_state_page("student", """
    win.showPage('sec-student-schedule');
""", "step_07b_student_schedule_calendar.png")

# Step 12: Student Project Tracking
make_dashboard_state_page("student", """
    win.showPage('sec-student-dash');
    setTimeout(() => {
        if (typeof win.openProjectTrackingModal === 'function') {
            win.openProjectTrackingModal('6521650101');
        }
    }, 250);
""", "step_07c_student_project_tracking.png")

# --- 3. ADVISOR WORKFLOWS (?user=advisor) ---
# Step 13: Advisor Classroom Selection
make_dashboard_state_page("advisor", """
    win.showPage('sec-advisor-classroom');
""", "step_08_advisor_classroom_selection.png")

# Step 14: Student Cards & Email Dispatcher
make_dashboard_state_page("advisor", """
    win.showPage('sec-advisor-classroom');
    setTimeout(() => {
        if (typeof win.switchAdvisorClassroomTab === 'function') {
            win.switchAdvisorClassroomTab('700');
        }
    }, 250);
""", "step_09_advisor_classroom_student_list.png")

# Step 15: Student Detail & Location Modal
make_dashboard_state_page("advisor", """
    win.showPage('sec-advisor-classroom');
    setTimeout(() => {
        const stdCards = doc.querySelectorAll('.student-card');
        if (stdCards.length > 0) stdCards[0].click();
    }, 300);
""", "step_09b_advisor_student_detail_modal.png")

# Step 16: Advisor Document Matrix Table
make_dashboard_state_page("advisor", """
    win.showPage('sec-advisor-classroom');
    setTimeout(() => {
        if (typeof win.switchAdvisorDocOverviewTab === 'function') {
            win.switchAdvisorDocOverviewTab('matrix');
        }
    }, 250);
""", "step_09c_advisor_doc_matrix_table.png")

# Step 17: Per-Document Review Modal
make_dashboard_state_page("advisor", """
    win.showPage('sec-advisor-classroom');
    setTimeout(() => {
        if (typeof win.openDocModal === 'function') {
            win.openDocModal('6521650101');
        }
    }, 250);
""", "step_10_advisor_per_document_review_modal.png")

# Step 18: Reject with Granular Comment
make_dashboard_state_page("advisor", """
    win.showPage('sec-advisor-classroom');
    setTimeout(() => {
        if (typeof win.openDocModal === 'function') {
            win.openDocModal('6521650101');
            setTimeout(() => {
                const commentBox = doc.querySelector('.doc-reject-reason');
                if (commentBox) {
                    commentBox.style.display = 'block';
                    commentBox.value = 'กรุณาแนบลายมือชื่ออาจารย์ที่ปรึกษาและตราประทับบริษัทในหน้า 3 ให้ครบถ้วนก่อนส่งอีกครั้ง';
                }
            }, 300);
        }
    }, 250);
""", "step_10b_advisor_reject_with_comment.png")

# Step 19: Assignments Management
make_dashboard_state_page("advisor", """
    win.showPage('sec-advisor-assignments');
""", "step_11_advisor_assignments_management.png")

# Step 20: New Assignment Modal
make_dashboard_state_page("advisor", """
    win.showPage('sec-advisor-assignments');
    setTimeout(() => {
        if (typeof win.openNewAssignmentModal === 'function') {
            win.openNewAssignmentModal();
        }
    }, 250);
""", "step_11b_advisor_new_assignment_modal.png")

# Step 21: Assignment Submitters Inspector
make_dashboard_state_page("advisor", """
    win.showPage('sec-advisor-assignments');
    setTimeout(() => {
        if (typeof win.openAssignmentSubmittersModal === 'function') {
            win.openAssignmentSubmittersModal('asg-01');
        }
    }, 250);
""", "step_11c_advisor_assignment_submitters_modal.png")

# Step 22: Interactive Supervision Calendar
make_dashboard_state_page("advisor", """
    win.showPage('sec-advisor-calendar');
""", "step_12_advisor_supervision_calendar.png")

# Step 23: Live Camera QR Scanner Interface
make_dashboard_state_page("advisor", """
    win.showPage('sec-advisor-qr');
""", "step_13_advisor_qr_camera_scanner.png")

# Step 24: GPS Geofence Success (500m)
make_dashboard_state_page("advisor", """
    win.showPage('sec-advisor-qr');
    setTimeout(() => {
        const modal = doc.getElementById('modal-gps-success') || doc.querySelector('.checkin-success-modal');
        if (modal) modal.classList.add('active');
    }, 250);
""", "step_14_gps_checkin_success_500m.png")

# Step 25: GPS Geofence Blocked Warning
make_dashboard_state_page("advisor", """
    win.showPage('sec-advisor-qr');
    setTimeout(() => {
        const modal = doc.getElementById('modal-gps-blocked') || doc.querySelector('.checkin-blocked-modal');
        if (modal) modal.classList.add('active');
    }, 250);
""", "step_15_gps_checkin_blocked_warning.png")

# Step 26: Workplace GPS Setup Modal
make_dashboard_state_page("advisor", """
    win.showPage('sec-advisor-classroom');
    setTimeout(() => {
        if (typeof win.openGpsSetupModal === 'function') {
            win.openGpsSetupModal('6521650101');
        }
    }, 250);
""", "step_15b_advisor_gps_setup_modal.png")

# Step 27: Photo Preview & Confirmation Modal
make_dashboard_state_page("advisor", """
    win.showPage('sec-advisor-classroom');
    setTimeout(() => {
        if (typeof win.openPhotoModal === 'function') {
            win.openPhotoModal('6521650101');
        }
    }, 250);
""", "step_16_photo_evidence_gallery_and_upload.png")

# Step 28: Full Supervision Photos Gallery
make_dashboard_state_page("advisor", """
    win.showPage('sec-advisor-photos');
""", "step_16b_photo_evidence_full_gallery.png")

# Step 29: Supervision Evaluation & Scoring Modal
make_dashboard_state_page("advisor", """
    win.showPage('sec-advisor-classroom');
    setTimeout(() => {
        if (typeof win.openEvalModalFromResult === 'function') {
            win.openEvalModalFromResult('6521650101');
        }
    }, 250);
""", "step_17_supervision_evaluation_scoring.png")

# --- 4. ADMIN WORKFLOWS (?user=admin) ---
# Step 30: Admin Dashboard Metrics
make_dashboard_state_page("admin", """
    win.showPage('sec-admin-dash');
""", "step_18_admin_dashboard_metrics.png")

# Step 31: Admin Semester Filter
make_dashboard_state_page("admin", """
    win.showPage('sec-admin-dash');
    setTimeout(() => {
        const sem = doc.getElementById('adv-semester-select-tab');
        if (sem) {
            sem.value = '2568-1';
            sem.dispatchEvent(new Event('change'));
        }
    }, 250);
""", "step_18b_admin_semester_filter.png")

# Step 32: Admin Realtime Search Filter
make_dashboard_state_page("admin", """
    win.showPage('sec-admin-dash');
    setTimeout(() => {
        const inp = doc.querySelector('#admin-search-filter-bar input');
        if (inp) {
            inp.value = 'กิตติศักดิ์';
            inp.dispatchEvent(new Event('input'));
        }
    }, 250);
""", "step_18c_admin_realtime_search.png")

# Step 33: Excel Pre-Import Preview Table
make_dashboard_state_page("admin", """
    win.showPage('sec-admin-dash');
    setTimeout(() => {
        const previewSec = doc.getElementById('admin-excel-preview-section');
        if (previewSec) previewSec.style.display = 'block';
    }, 250);
""", "step_19_admin_excel_pre_import_preview.png")

# Step 34: Excel Post-Import Summary Modal
make_dashboard_state_page("admin", """
    win.showPage('sec-admin-dash');
    setTimeout(() => {
        const m = doc.getElementById('modal-post-add-preview');
        if (m) m.classList.add('active');
    }, 250);
""", "step_20_admin_excel_post_import_modal.png")

# Step 35: Export Reports (Excel & PDF)
make_dashboard_state_page("admin", """
    win.showPage('sec-admin-dash');
    setTimeout(() => {
        const expBox = doc.querySelector('.export-actions') || doc.querySelector('#admin-export-box');
        if (expBox) expBox.scrollIntoView();
    }, 250);
""", "step_21_admin_export_reports.png")

# Step 36: Session Logout Flow
make_dashboard_state_page("student", """
    const logoutBtn = doc.querySelector('.logout-btn') || doc.querySelector('#btn-logout') || doc.querySelector('[onclick*="logout"]');
    if (logoutBtn) logoutBtn.click();
""", "step_22_session_logout_flow.png")

print("=== Finished Recapturing All 36 Steps with Authentication! ===")


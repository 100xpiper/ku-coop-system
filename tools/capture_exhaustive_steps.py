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

def capture_url(url, filename, width=1280, height=900):
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
    }}, 450);
}};
</script>
</body>
</html>"""
    capture_with_html_wrapper(wrapper, filename, width, height)

print("=== Starting Capture of Additional Exhaustive Steps ===")

# 1. Show/Hide Password Eye Icon
make_index_state_page("""
    const u = doc.getElementById('username');
    const p = doc.getElementById('password');
    if (u) u.value = 'wongsapat.u@ku.th';
    if (p) {
        p.value = 'InitPass@2026';
        p.type = 'text'; // simulate eye open
    }
""", "step_01b_show_hide_password.png")

# 2. Student Blank Form Preview
make_dashboard_state_page("""
    win.showPage('sec-student-docs');
    setTimeout(() => {
        if (typeof win.previewBlankForm === 'function') {
            win.previewBlankForm('form-02');
        }
    }, 200);
""", "step_05b_student_blank_forms_library.png")

# 3. Student Schedule / Calendar
make_dashboard_state_page("""
    win.showPage('sec-student-schedule');
""", "step_07b_student_schedule_calendar.png")

# 4. Student Project Tracking Modal
make_dashboard_state_page("""
    win.showPage('sec-student-dash');
    setTimeout(() => {
        if (typeof win.openProjectTrackingModal === 'function') {
            win.openProjectTrackingModal('std-001');
        }
    }, 200);
""", "step_07c_student_project_tracking.png")

# 5. Advisor Student Detail Modal
make_dashboard_state_page("""
    win.showPage('sec-advisor-classroom');
    setTimeout(() => {
        const stdCards = doc.querySelectorAll('.student-card');
        if (stdCards.length > 0) {
            stdCards[0].click();
        }
    }, 250);
""", "step_09b_advisor_student_detail_modal.png")

# 6. Advisor Document Matrix Table
make_dashboard_state_page("""
    win.showPage('sec-advisor-classroom');
    setTimeout(() => {
        if (typeof win.switchAdvisorDocOverviewTab === 'function') {
            win.switchAdvisorDocOverviewTab('matrix');
        }
    }, 200);
""", "step_09c_advisor_doc_matrix_table.png")

# 7. Advisor Rejection with Granular Comment
make_dashboard_state_page("""
    win.showPage('sec-advisor-classroom');
    setTimeout(() => {
        if (typeof win.openDocModal === 'function') {
            win.openDocModal('std-001');
            setTimeout(() => {
                const commentBox = doc.querySelector('.doc-reject-reason');
                if (commentBox) {
                    commentBox.style.display = 'block';
                    commentBox.value = 'กรุณาแนบลายมือชื่ออาจารย์ที่ปรึกษาและตราประทับบริษัทในหน้า 3 ให้ครบถ้วนก่อนส่งอีกครั้ง';
                }
            }, 250);
        }
    }, 200);
""", "step_10b_advisor_reject_with_comment.png")

# 8. Advisor New Assignment Modal
make_dashboard_state_page("""
    win.showPage('sec-advisor-assignments');
    setTimeout(() => {
        if (typeof win.openNewAssignmentModal === 'function') {
            win.openNewAssignmentModal();
        }
    }, 200);
""", "step_11b_advisor_new_assignment_modal.png")

# 9. Advisor Assignment Submitters Inspector
make_dashboard_state_page("""
    win.showPage('sec-advisor-assignments');
    setTimeout(() => {
        if (typeof win.openAssignmentSubmittersModal === 'function') {
            win.openAssignmentSubmittersModal('asg-01');
        }
    }, 200);
""", "step_11c_advisor_assignment_submitters_modal.png")

# 10. Workplace GPS Setup & Auto-detect Modal
make_dashboard_state_page("""
    win.showPage('sec-advisor-classroom');
    setTimeout(() => {
        if (typeof win.openGpsSetupModal === 'function') {
            win.openGpsSetupModal('std-001');
        }
    }, 200);
""", "step_15b_advisor_gps_setup_modal.png")

# 11. Supervision Full Photos Gallery Page
make_dashboard_state_page("""
    win.showPage('sec-advisor-photos');
""", "step_16b_photo_evidence_full_gallery.png")

# 12. Admin Semester Filter
make_dashboard_state_page("""
    win.showPage('sec-admin-dash');
    setTimeout(() => {
        const semSelect = doc.getElementById('adv-semester-select-tab');
        if (semSelect) {
            semSelect.value = '2568-1';
            semSelect.dispatchEvent(new Event('change'));
        }
    }, 200);
""", "step_18b_admin_semester_filter.png")

# 13. Admin Real-time Search Filter
make_dashboard_state_page("""
    win.showPage('sec-admin-dash');
    setTimeout(() => {
        const searchInput = doc.querySelector('#admin-search-filter-bar input');
        if (searchInput) {
            searchInput.value = 'วงศพัทธ์';
            searchInput.dispatchEvent(new Event('input'));
        }
    }, 200);
""", "step_18c_admin_realtime_search.png")

# 14. Session Logout Flow
make_dashboard_state_page("""
    const logoutBtn = doc.querySelector('.logout-btn') || doc.querySelector('#btn-logout') || doc.querySelector('[onclick*="logout"]');
    if (logoutBtn) {
        logoutBtn.click();
    }
""", "step_22_session_logout_flow.png")

print("=== Finished capturing additional exhaustive steps! ===")


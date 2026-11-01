# -*- coding: utf-8 -*-
import shutil
import os

brain_dir = r"C:\Users\PER\.gemini\antigravity\brain\ddb60d44-47b2-4e84-bca5-28d119fdaf51\screenshots"
os.makedirs("screenshots", exist_ok=True)
os.makedirs(brain_dir, exist_ok=True)

mapping = [
    ("01_login_page.png", "01_login_page.png"),
    ("02_admin_dashboard.png", "02_admin_dashboard.png"),
    ("17_admin_excel_preview_pre_import.png", "03_admin_excel_preview_pre_import.png"),
    ("18_admin_excel_preview_post_import.png", "04_admin_excel_preview_post_import.png"),
    ("03_advisor_dashboard.png", "05_advisor_dashboard.png"),
    ("04_advisor_classroom.png", "06_advisor_classroom.png"),
    ("05_advisor_assignments.png", "07_advisor_assignments.png"),
    ("06_supervision_evidence.png", "08_supervision_evidence.png"),
    ("07_evidence_upload_modal.png", "09_evidence_upload_modal.png"),
    ("08_supervision_calendar.png", "10_supervision_calendar.png"),
    ("09_student_submission.png", "11_student_submission.png"),
    ("15_student_set_gps.png", "12_student_qrcode_and_gps.png"),
    ("11_qr_camera_scanner.png", "13_qr_camera_scanner.png"),
    ("14_checkin_success_in_radius.png", "14_checkin_success_in_radius.png"),
    ("15_checkin_failed_out_of_radius.png", "15_checkin_failed_out_of_radius.png"),
    ("12_mobile_responsive_view.png", "16_mobile_responsive_view.png"),
    ("13_mobile_qr_scanner.png", "17_mobile_qr_scanner.png"),
    ("19_admin_export_reports.png", "18_admin_export_reports.png"),
]

for src_name, dst_name in mapping:
    src_local = os.path.join("screenshots", src_name)
    src_brain = os.path.join(brain_dir, src_name)
    target_src = src_local if os.path.exists(src_local) else src_brain
    if os.path.exists(target_src):
        dst_local = os.path.join("screenshots", dst_name)
        dst_brain = os.path.join(brain_dir, dst_name)
        if os.path.abspath(target_src) != os.path.abspath(dst_local):
            shutil.copy(target_src, dst_local)
        if os.path.abspath(target_src) != os.path.abspath(dst_brain):
            shutil.copy(target_src, dst_brain)
        print(f"Mapped {src_name} -> {dst_name}")
    else:
        print(f"Warning: could not find source for {src_name}")

print("Screenshot sequence organized successfully.")

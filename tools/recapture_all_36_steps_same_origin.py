# -*- coding: utf-8 -*-
import subprocess
import os
import hashlib
import time
from PIL import Image

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

out_dir = r"c:\Users\PER\Downloads\Project\screenshots\steps"
os.makedirs(out_dir, exist_ok=True)

steps = [
    # 1. Auth & Login (index.html)
    ("step_01_login_initial", 1280, 850),
    ("step_01_login_credentials_entered", 1280, 850),
    ("step_01b_show_hide_password", 1280, 850),
    ("step_02_otp_verification_modal", 1280, 850),
    ("step_03_force_password_change", 1280, 850),
    
    # 2. Student Workflows (dashboard.html?user=student)
    ("step_04_student_dashboard_overview", 1280, 950),
    ("step_05_student_dynamic_qrcode", 1280, 950),
    ("step_05b_student_blank_forms_library", 1280, 950),
    ("step_06_student_document_upload_form", 1280, 950),
    ("step_07_student_doc_history_feedback", 1280, 950),
    ("step_07b_student_schedule_calendar", 1280, 950),
    ("step_07c_student_project_tracking", 1280, 950),
    
    # 3. Advisor Workflows (dashboard.html?user=advisor)
    ("step_08_advisor_classroom_selection", 1280, 950),
    ("step_09_advisor_classroom_student_list", 1280, 950),
    ("step_09b_advisor_student_detail_modal", 1280, 950),
    ("step_09c_advisor_doc_matrix_table", 1280, 950),
    ("step_10_advisor_per_document_review_modal", 1280, 950),
    ("step_10b_advisor_reject_with_comment", 1280, 950),
    ("step_11_advisor_assignments_management", 1280, 950),
    ("step_11b_advisor_new_assignment_modal", 1280, 950),
    ("step_11c_advisor_assignment_submitters_modal", 1280, 950),
    ("step_12_advisor_supervision_calendar", 1280, 950),
    ("step_13_advisor_qr_camera_scanner", 1280, 950),
    ("step_14_gps_checkin_success_500m", 1280, 950),
    ("step_15_gps_checkin_blocked_warning", 1280, 950),
    ("step_15b_advisor_gps_setup_modal", 1280, 950),
    ("step_16_photo_evidence_gallery_and_upload", 1280, 950),
    ("step_16b_photo_evidence_full_gallery", 1280, 950),
    ("step_17_supervision_evaluation_scoring", 1280, 950),
    
    # 4. Admin Workflows (dashboard.html?user=admin)
    ("step_18_admin_dashboard_metrics", 1280, 950),
    ("step_18b_admin_semester_filter", 1280, 950),
    ("step_18c_admin_realtime_search", 1280, 950),
    ("step_19_admin_excel_pre_import_preview", 1280, 950),
    ("step_20_admin_excel_post_import_modal", 1280, 950),
    ("step_21_admin_export_reports", 1280, 950),
    
    # 5. Session Logout Flow
    ("step_22_session_logout_flow", 1280, 850)
]

print(f"=== Starting Recapture of All {len(steps)} Steps via Same-Origin Runner ===")

hashes = {}
duplicates = []

for idx, (step_name, w, h) in enumerate(steps, 1):
    url = f"http://localhost:8080/scratch/runner.html?step={step_name}"
    out_file = os.path.join(out_dir, f"{step_name}.png")
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        f"--window-size={w},{h}",
        "--virtual-time-budget=2000",
        f"--screenshot={out_file}",
        url
    ]
    subprocess.run(cmd, check=True)
    size = os.path.getsize(out_file)
    with open(out_file, "rb") as f:
        md5 = hashlib.md5(f.read()).hexdigest()
    
    img = Image.open(out_file)
    is_blank = (img.getextrema() == ((255, 255), (255, 255), (255, 255)))
    
    if md5 in hashes:
        print(f"[{idx:02d}/{len(steps)}] WARNING DUPLICATE: {step_name} matches {hashes[md5]}")
        duplicates.append((step_name, hashes[md5]))
    else:
        hashes[md5] = step_name
        blank_str = " [BLANK!]" if is_blank else ""
        print(f"[{idx:02d}/{len(steps)}] OK: {step_name} ({w}x{h}) -> {size:,} bytes | MD5: {md5[:8]}{blank_str}")

print("\n=== Verification Summary ===")
print(f"Total steps captured: {len(steps)}")
print(f"Unique screenshots: {len(hashes)}")
print(f"Duplicates: {len(duplicates)}")
if duplicates:
    print("Duplicate pairs:")
    for d1, d2 in duplicates:
        print(f"  - {d1} == {d2}")
else:
    print("ALL SCREENSHOTS ARE 100% UNIQUE AND NON-DUPLICATED!")

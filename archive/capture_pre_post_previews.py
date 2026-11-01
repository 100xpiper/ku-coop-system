# -*- coding: utf-8 -*-
import subprocess
import time
import os
import shutil

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

os.makedirs("screenshots", exist_ok=True)
brain_dir = r"C:\Users\PER\.gemini\antigravity\brain\ddb60d44-47b2-4e84-bca5-28d119fdaf51\screenshots"
os.makedirs(brain_dir, exist_ok=True)

# 1. Capture Pre-import Preview (Before Adding File)
url_pre = "http://localhost:8080/dashboard.html?user=admin&page=sec-admin-dash&test_pre_import=1"
out_pre = os.path.abspath("screenshots/17_admin_excel_preview_pre_import.png")
cmd1 = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--window-size=1280,1400",
    f"--screenshot={out_pre}",
    url_pre
]
print("Capturing Pre-import Excel preview...")
subprocess.run(cmd1, check=True)
print("Saved:", out_pre)

# 2. Capture Post-import Preview (After Adding File)
url_post = "http://localhost:8080/dashboard.html?user=admin&page=sec-admin-dash&test_post_import=1"
out_post = os.path.abspath("screenshots/18_admin_excel_preview_post_import.png")
cmd2 = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--window-size=1280,1400",
    f"--screenshot={out_post}",
    url_post
]
print("Capturing Post-import Excel preview...")
subprocess.run(cmd2, check=True)
print("Saved:", out_post)

# Copy to brain artifact directory
shutil.copy(out_pre, os.path.join(brain_dir, "17_admin_excel_preview_pre_import.png"))
shutil.copy(out_post, os.path.join(brain_dir, "18_admin_excel_preview_post_import.png"))
print("Copied both screenshots to brain directory successfully.")

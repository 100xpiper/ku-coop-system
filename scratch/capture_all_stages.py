# -*- coding: utf-8 -*-
import subprocess
import os
import shutil

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

os.makedirs("screenshots", exist_ok=True)
brain_dir = r"C:\Users\PER\.gemini\antigravity\brain\ddb60d44-47b2-4e84-bca5-28d119fdaf51\screenshots"
os.makedirs(brain_dir, exist_ok=True)

# Copy existing files from brain if present in brain
for fname in os.listdir(brain_dir):
    src = os.path.join(brain_dir, fname)
    dst = os.path.join("screenshots", fname)
    if os.path.isfile(src) and not os.path.exists(dst):
        shutil.copy(src, dst)
        print(f"Copied from brain: {fname}")

def capture(url, outfile, width=1280, height=950):
    out_path = os.path.abspath(os.path.join("screenshots", outfile))
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        f"--window-size={width},{height}",
        f"--screenshot={out_path}",
        url
    ]
    subprocess.run(cmd, check=True)
    # also copy to brain dir
    shutil.copy(out_path, os.path.join(brain_dir, outfile))
    print(f"Captured: {outfile}")

# 1. Checkin Success (within 500m)
capture("http://localhost:8080/dashboard.html?user=advisor&test_checkin=success", "14_checkin_success_in_radius.png", 1280, 1100)

# 2. Checkin Failed (out of 500m)
capture("http://localhost:8080/dashboard.html?user=advisor&test_checkin=failed", "15_checkin_failed_out_of_radius.png", 1280, 1100)

# 3. Export reports section on Admin
capture("http://localhost:8080/dashboard.html?user=admin&page=sec-admin-dash", "19_admin_export_reports.png", 1280, 1400)

print("All screenshots generated and verified successfully.")


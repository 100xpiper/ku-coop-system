# -*- coding: utf-8 -*-
import subprocess
import time
import os

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

os.makedirs("screenshots", exist_ok=True)

# 1. Capture QR Scanner page on desktop
url_qr = "http://localhost:8080/dashboard.html?user=advisor&page=sec-advisor-qr"
out_qr = os.path.abspath("screenshots/11_qr_camera_scanner.png")
cmd1 = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--window-size=1280,850",
    f"--screenshot={out_qr}",
    url_qr
]
print("Capturing QR Scanner page...")
subprocess.run(cmd1, check=True)
print("QR Scanner screenshot saved:", out_qr)

# 2. Capture mobile view (iPhone viewport 390x844)
url_mobile = "http://localhost:8080/dashboard.html?user=advisor"
out_mobile = os.path.abspath("screenshots/12_mobile_responsive_view.png")
cmd2 = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--window-size=390,844",
    f"--screenshot={out_mobile}",
    url_mobile
]
print("Capturing Mobile Responsive page...")
subprocess.run(cmd2, check=True)
print("Mobile screenshot saved:", out_mobile)

# 3. Capture mobile view of QR Scanner (iPhone viewport 390x844)
out_mobile_qr = os.path.abspath("screenshots/13_mobile_qr_scanner.png")
cmd3 = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--window-size=390,844",
    f"--screenshot={out_mobile_qr}",
    url_qr
]
print("Capturing Mobile QR Scanner...")
subprocess.run(cmd3, check=True)
print("Mobile QR screenshot saved:", out_mobile_qr)


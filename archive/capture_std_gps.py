import subprocess
import os

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out_img = os.path.abspath("screenshots/15_student_set_gps.png")

cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--window-size=1280,950",
    f"--screenshot={out_img}",
    "http://localhost:8080/dashboard.html?user=student&page=sec-student-qrcode"
]

subprocess.run(cmd, check=True)
print("Captured student GPS setting page to:", out_img)


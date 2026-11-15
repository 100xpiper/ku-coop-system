"""
capture_related_systems.py
แคปภาพหน้าจอระบบที่เกี่ยวข้องสำหรับบทที่ 2 (วรรณกรรม)
ระบบ:
  1. Google Forms - ตัวอย่างแบบฟอร์มรายงานการนิเทศงาน
  2. Microsoft Teams - ฟีเจอร์ Assignments/Assignment tracking
  3. QR Attendance - ตัวอย่างระบบสแกน QR เช็คชื่อของมหาวิทยาลัยอื่น
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

OUTPUT_DIR = r"c:\Users\per30\OneDrive\เดสก์ท็อป\Project ปี5\Project\screenshots\related_systems"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def make_driver():
    opts = Options()
    opts.add_argument("--window-size=1280,900")
    opts.add_argument("--lang=th-TH")
    # ไม่ใช้ headless เพื่อให้ภาพสมจริง (มีหัว browser)
    opts.add_argument("--disable-infobars")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    # ปิด "Chrome is being controlled by automated software"
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    return webdriver.Chrome(options=opts)

def capture(driver, url, filename, wait_sec=5, scroll_to=0):
    """เปิด URL แล้วแคปหน้าจอบันทึกลงไฟล์"""
    print(f"  -> เปิด: {url}")
    driver.get(url)
    time.sleep(wait_sec)
    if scroll_to > 0:
        driver.execute_script(f"window.scrollTo(0, {scroll_to});")
        time.sleep(1)
    path = os.path.join(OUTPUT_DIR, filename)
    driver.save_screenshot(path)
    print(f"  -> บันทึก: {path}")
    return path

def main():
    driver = make_driver()
    try:
        # ======================================================
        # ภาพที่ 1: Google Forms — หน้า Template Gallery (Education)
        # แสดงให้เห็นว่า Google Forms เป็นเครื่องมือทั่วไปที่ใช้สร้างแบบฟอร์ม
        # ======================================================
        print("\n[1] แคป Google Forms Template Gallery...")
        capture(
            driver,
            "https://docs.google.com/forms/u/0/?tgif=d",
            "01_google_forms_home.png",
            wait_sec=6
        )

        # ======================================================
        # ภาพที่ 2: Google Forms — ตัวอย่างแบบฟอร์มสาธิต (Template Contact Information)
        # ======================================================
        print("\n[2] แคป Google Forms - Template สาธารณะ...")
        capture(
            driver,
            "https://docs.google.com/forms/d/e/1FAIpQLSdqwS_1kDLTKCBVOkFSK0DpD6gHXdaJGww-4vQULYRpBdEZ_A/viewform",
            "02_google_forms_sample.png",
            wait_sec=6
        )

        # ======================================================
        # ภาพที่ 3: Microsoft Teams — หน้าแนะนำ Assignments feature
        # ======================================================
        print("\n[3] แคป Microsoft Teams Assignments overview...")
        capture(
            driver,
            "https://support.microsoft.com/en-us/topic/assignments-in-microsoft-teams-for-education-overview-4fb0ece5-3291-4b32-bd0d-18498e02e703",
            "03_teams_assignments_overview.png",
            wait_sec=7
        )

        # ======================================================
        # ภาพที่ 4: Microsoft Teams — Assignments สำหรับการศึกษา
        # ======================================================
        print("\n[4] แคป Microsoft Teams Education page...")
        capture(
            driver,
            "https://www.microsoft.com/en-us/education/products/teams",
            "04_teams_education.png",
            wait_sec=7
        )

        # ======================================================
        # ภาพที่ 5: QR Attendance — ตัวอย่างระบบ QR เช็คชื่อ
        # ใช้ Giggster/Eventbrite หรือ GitHub README ที่เป็นสาธารณะ
        # ======================================================
        print("\n[5] แคป QR Attendance System example...")
        capture(
            driver,
            "https://attendanceapp.com/",
            "05_qr_attendance_example.png",
            wait_sec=6
        )

        # ======================================================
        # ภาพที่ 6: QR Code Attendance — อีกตัวอย่าง (แอปบน iOS/Android)
        # ======================================================
        print("\n[6] แคป QR Attendance alternative...")
        capture(
            driver,
            "https://www.tracktime24.com/attendance-tracking",
            "06_qr_attendance_app.png",
            wait_sec=6
        )

        print("\nแคปภาพครบทั้งหมดแล้ว!")
        print(f"ไฟล์บันทึกที่: {OUTPUT_DIR}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()


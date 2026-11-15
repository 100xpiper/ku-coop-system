"""
capture_qr_attendance.py
แคปภาพระบบ QR Attendance เพิ่มเติมสำหรับบทที่ 2
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

OUTPUT_DIR = r"c:\Users\per30\OneDrive\เดสก์ท็อป\Project ปี5\Project\screenshots\related_systems"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def make_driver():
    opts = Options()
    opts.add_argument("--window-size=1280,900")
    opts.add_argument("--disable-infobars")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    return webdriver.Chrome(options=opts)

def capture(driver, url, filename, wait_sec=6, scroll_to=0):
    print(f"  -> เปิด: {url}")
    driver.get(url)
    time.sleep(wait_sec)
    if scroll_to > 0:
        driver.execute_script(f"window.scrollTo(0, {scroll_to});")
        time.sleep(1.5)
    path = os.path.join(OUTPUT_DIR, filename)
    driver.save_screenshot(path)
    size = os.path.getsize(path)
    print(f"  -> บันทึก: {path} ({size:,} bytes)")
    return path

def main():
    driver = make_driver()
    try:
        # ภาพ QR Attendance — ใช้ attendify.com (ระบบลงทะเบียนและเช็คชื่อ)
        print("\n[5] แคป QR Attendance - Eventbrite Check-in App...")
        capture(
            driver,
            "https://www.eventbrite.com/organizer/check-in-app/",
            "05_qr_attendance_eventbrite.png",
            wait_sec=8
        )

        # ภาพ QR Attendance — ใช้ YouTube thumbnail preview หรือ Google Play
        print("\n[6] แคป QR Attendance - Google Play (Attendance Manager App)...")
        capture(
            driver,
            "https://play.google.com/store/apps/details?id=com.attendance.qr",
            "06_qr_attendance_app.png",
            wait_sec=8
        )

        print("\nแคปภาพ QR Attendance เสร็จแล้ว!")

    except Exception as e:
        print(f"\nError: {e}")
        # ลอง fallback
        try:
            print("\n[Fallback] แคป QR Code Attendance บน Wikipedia / GitHub...")
            capture(
                driver,
                "https://github.com/topics/qr-code-attendance",
                "05_qr_attendance_github.png",
                wait_sec=6
            )
        except Exception as e2:
            print(f"Fallback ก็ล้มเหลว: {e2}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()


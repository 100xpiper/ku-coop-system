@echo off
chcp 65001 >nul
title เชื่อมต่อโทรศัพท์มือถือผ่านสาย USB (เปิด localhost บนมือถือ)
echo ========================================================
echo  ตั้งค่าพอร์ตให้โทรศัพท์เปิด localhost:8080 ได้ผ่านสาย USB
echo ========================================================
echo.

set "ADB=C:\Users\per30\AppData\Local\Android\Sdk\platform-tools\adb.exe"
if not exist "%ADB%" (
    where adb >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set "ADB=adb"
    ) else (
        echo [ข้อผิดพลาด] ไม่พบ adb ในเครื่อง
        pause
        exit /b 1
    )
)

echo ตรวจสอบสถานะการเชื่อมต่อโทรศัพท์มือถือ...
"%ADB%" devices
echo.

"%ADB%" reverse tcp:8080 tcp:8080
"%ADB%" reverse tcp:3000 tcp:3000

echo ========================================================
echo  ตั้งค่าส่งต่อพอร์ต (Port Forwarding) เรียบร้อยแล้ว!
echo.
echo  ขั้นตอนการเปิดบนโทรศัพท์มือถือ:
echo  1. ตรวจสอบว่าเสียบสาย USB และเปิด "การแก้ไขข้อบกพร่อง USB (USB Debugging)" แล้ว
echo  2. เปิดแอป Google Chrome บนโทรศัพท์มือถือ
echo  3. พิมพ์ที่อยู่เว็บ:
echo     http://localhost:8080
echo ========================================================
echo.
pause

@echo off
chcp 65001 >nul
title เชื่อมต่อโทรศัพท์มือถือผ่านสาย USB (เปิด localhost บนมือถือ)
echo ========================================================
echo  กำลังตั้งค่าพอร์ตให้โทรศัพท์เปิด localhost:8080 ได้ผ่านสาย USB...
echo ========================================================

set "ADB=C:\Users\per30\AppData\Local\Android\Sdk\platform-tools\adb.exe"
if exist "%ADB%" (
    "%ADB%" reverse tcp:8080 tcp:8080
    "%ADB%" reverse tcp:3000 tcp:3000
    echo.
    echo ========================================================
    echo  เชื่อมต่อพอร์ตสำเร็จ!
    echo  เปิดเบราว์เซอร์ Chrome บนโทรศัพท์ แล้วพิมพ์:
    echo  http://localhost:8080
    echo ========================================================
) else (
    echo ไม่พบ adb ในเครื่อง
)
echo.
pause

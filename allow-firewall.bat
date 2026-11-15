@echo off
chcp 65001 >nul
title ปลดล็อก Windows Firewall สำหรับเปิดระบบบนโทรศัพท์มือถือ
echo ========================================================
echo  กำลังเพิ่มกฎปลดล็อก Firewall พอร์ต 8080, 8081, 3000...
echo ========================================================

netsh advfirewall firewall add rule name="KU-Coop-Web-Server" dir=in action=allow protocol=TCP localport=8080,8081,3000 profile=any
netsh advfirewall firewall set rule name="python.exe" new action=allow >nul 2>nul
netsh advfirewall firewall set rule name="Windows PowerShell" new action=allow >nul 2>nul

echo.
if %ERRORLEVEL% equ 0 (
    echo ========================================================
    echo  ปลดล็อก Firewall สำเร็จเรียบร้อยแล้ว!
    echo  โทรศัพท์มือถือในวง Wi-Fi เดียวกันสามารถเข้าใช้งานได้ที่:
    echo  http://192.168.1.103:8080
    echo ========================================================
) else (
    echo [คำเตือน] กรุณาคลิกขวาที่ไฟล์นี้ แล้วเลือก "Run as administrator"
)
echo.
pause

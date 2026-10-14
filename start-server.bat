@echo off
chcp 65001 >nul
title KU Coop Web Server
echo ========================================================
echo  กำลังเริ่มต้นเว็บเซิร์ฟเวอร์ ระบบนิเทศสหกิจศึกษา มก.
echo  เข้าใช้งานได้ที่: http://localhost:8080
echo ========================================================
start http://localhost:8080
powershell -ExecutionPolicy Bypass -File "%~dp0server.ps1"
pause

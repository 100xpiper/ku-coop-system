@echo off
chcp 65001 >nul
title KU Coop Web Server
echo ========================================================
echo  กำลังเริ่มต้นเว็บเซิร์ฟเวอร์ ระบบนิเทศสหกิจศึกษา มก.
echo ========================================================
powershell -ExecutionPolicy Bypass -File "%~dp0server.ps1"
pause

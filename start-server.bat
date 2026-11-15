@echo off
chcp 65001 >nul
title KU Coop Web Server
echo ========================================================
echo  กำลังเริ่มต้นเว็บเซิร์ฟเวอร์ ระบบนิเทศสหกิจศึกษา มก.
echo ========================================================

if exist "%USERPROFILE%\AppData\Roaming\uv\python\cpython-3.12.16-windows-x86_64-none\ku_coop_server.exe" (
    "%USERPROFILE%\AppData\Roaming\uv\python\cpython-3.12.16-windows-x86_64-none\ku_coop_server.exe" "%~dp0server.py"
    goto :end
)

if exist "%USERPROFILE%\.local\bin\ku_coop_server.exe" (
    "%USERPROFILE%\.local\bin\ku_coop_server.exe" "%~dp0server.py"
    goto :end
)

if exist "%USERPROFILE%\.local\bin\python3.12.exe" (
    "%USERPROFILE%\.local\bin\python3.12.exe" "%~dp0server.py"
    goto :end
)

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python "%~dp0server.py"
    goto :end
)

if exist "%USERPROFILE%\.local\bin\uv.exe" (
    "%USERPROFILE%\.local\bin\uv.exe" run python "%~dp0server.py"
    goto :end
)

powershell -ExecutionPolicy Bypass -File "%~dp0server.ps1"

:end
pause

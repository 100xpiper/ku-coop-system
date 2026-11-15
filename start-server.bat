@echo off
title KU Coop Web Server
cd /d "%~dp0"
echo ========================================================
echo  Starting KU Coop Web Server...
echo ========================================================

if exist "%USERPROFILE%\.local\bin\python3.12.exe" (
    "%USERPROFILE%\.local\bin\python3.12.exe" "%~dp0server.py"
    goto :done
)

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python "%~dp0server.py"
    goto :done
)

powershell -ExecutionPolicy Bypass -File "%~dp0server.ps1"

:done
pause

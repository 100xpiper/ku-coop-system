@echo off
title Connect Android Phone via USB (Port Forwarding)
cd /d "%~dp0"
echo ========================================================
echo  Forwarding Port 8080 to Android Phone via USB Cable...
echo ========================================================
echo.

set "ADB=%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe"
if not exist "%ADB%" (
    where adb >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set "ADB=adb"
    ) else (
        echo [ERROR] adb.exe not found on this computer.
        pause
        exit /b 1
    )
)

echo Checking connected Android devices...
"%ADB%" devices
echo.

"%ADB%" reverse tcp:8080 tcp:8080
"%ADB%" reverse tcp:3000 tcp:3000

echo.
echo ========================================================
echo  Port forwarding setup complete!
echo.
echo  1. Make sure your phone has USB Debugging enabled.
echo  2. Open Chrome on your phone and go to:
echo     http://localhost:8080
echo ========================================================
echo.
pause

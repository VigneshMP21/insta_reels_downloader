@echo off
title Install Instagram Downloader Dependencies
cd /d "%~dp0"

echo ============================================================
echo   Installing Dependencies for Instagram Video Downloader
echo ============================================================
echo.

where python >nul 2>&1
if %errorlevel% equ 0 (
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    goto finish
)

where py >nul 2>&1
if %errorlevel% equ 0 (
    py -m pip install --upgrade pip
    py -m pip install -r requirements.txt
    goto finish
)

echo [ERROR] Python is not installed or not added to PATH!
echo Please download and install Python from https://www.python.org/
echo (Make sure to check "Add Python to PATH" during installation)
echo.
pause
exit /b 1

:finish
echo.
echo ============================================================
echo   Dependencies installed successfully!
echo   You can now run "run_insta_downloader.bat".
echo ============================================================
echo.
pause

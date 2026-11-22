@echo off
title Instagram Reels and Posts Downloader
cd /d "%~dp0"

:: Check if python is available in PATH
where python >nul 2>&1
if %errorlevel% equ 0 (
    python insta_video_downloader.py %*
    goto check_exit
)

:: Fallback to Python 3.13
if exist "C:\Users\ADMIN\AppData\Local\Programs\Python\Python313\python.exe" (
    "C:\Users\ADMIN\AppData\Local\Programs\Python\Python313\python.exe" insta_video_downloader.py %*
    goto check_exit
)

:: Fallback to Python 3.10
if exist "C:\Users\ADMIN\AppData\Local\Programs\Python\Python310\python.exe" (
    "C:\Users\ADMIN\AppData\Local\Programs\Python\Python310\python.exe" insta_video_downloader.py %*
    goto check_exit
)

:: Fallback to Python Launcher (py)
where py >nul 2>&1
if %errorlevel% equ 0 (
    py insta_video_downloader.py %*
    goto check_exit
)

echo [ERROR] Python was not found on your system!
echo Please make sure Python is installed and added to your PATH.
echo Download Python: https://www.python.org/downloads/
echo.
pause
exit /b 1

:check_exit
if %errorlevel% neq 0 (
    echo.
    echo [!] Program exited with an error.
    echo If modules are missing, please double-click "install_dependencies.bat" first.
    echo.
    pause
)

:done

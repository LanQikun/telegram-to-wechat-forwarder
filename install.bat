@echo off
title Telegram to WeChat Forwarder - Installation
color 0A

echo ========================================
echo  Telegram to WeChat Forwarder Setup
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo [INFO] Python found
python --version

:: Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created
) else (
    echo [INFO] Virtual environment already exists
)

:: Activate virtual environment and install dependencies
echo [INFO] Installing dependencies...
call .venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [SUCCESS] Dependencies installed successfully

:: Copy config template if config.py doesn't exist
if not exist "config.py" (
    echo [INFO] Creating config.py from template...
    copy config_template.py config.py >nul
    echo [SUCCESS] config.py created
    echo [WARNING] Please edit config.py with your credentials before running
) else (
    echo [INFO] config.py already exists
)

echo.
echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit config.py with your credentials
echo 2. Make sure WeChat PC app is running
echo 3. Run: python telegram_to_wechat.py
echo.
echo Press any key to open config.py for editing...
pause >nul

:: Open config.py in default editor
start config.py

echo.
echo Setup complete! You can now run the forwarder.
pause
@echo off
REM Educational Decryption Tool - Windows Batch File
REM WARNING: This is for educational purposes only!

echo ================================================
echo     Educational File Decryption Tool
echo ================================================
echo WARNING: This is for educational purposes only!
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again.
    pause
    exit /b 1
)

REM Check if cryptography module is available
python -c "import cryptography" >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: cryptography module is not installed
    echo Installing cryptography...
    pip install cryptography
    if %errorlevel% neq 0 (
        echo Failed to install cryptography. Please install it manually:
        echo pip install cryptography
        pause
        exit /b 1
    )
)

REM Run the decryption script with all arguments passed to this batch file
python modern_decrypt.py %*

pause
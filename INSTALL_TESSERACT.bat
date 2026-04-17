@echo off
echo ========================================
echo Tesseract OCR Installation Guide
echo ========================================
echo.
echo Step 1: Download Tesseract
echo ----------------------------------------
echo Opening download page in browser...
echo.
start https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo Please download: tesseract-ocr-w64-setup-5.3.3.20231005.exe
echo (or latest version)
echo.
echo Step 2: Install Tesseract
echo ----------------------------------------
echo IMPORTANT during installation:
echo 1. Check "Additional language data"
echo 2. Select: Indonesian (ind)
echo 3. Select: English (eng)
echo 4. Install location: C:\Program Files\Tesseract-OCR
echo.
pause
echo.
echo Step 3: Verify Installation
echo ----------------------------------------
echo Checking if Tesseract is installed...
echo.

if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo [SUCCESS] Tesseract found!
    echo.
    echo Version:
    "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
    echo.
    echo Available languages:
    "C:\Program Files\Tesseract-OCR\tesseract.exe" --list-langs
    echo.
    echo ========================================
    echo Installation SUCCESSFUL!
    echo ========================================
    echo.
    echo Next steps:
    echo 1. Restart your Laravel server
    echo 2. Test OCR at: http://127.0.0.1:8000/dashboard-ga.html
    echo.
) else (
    echo [ERROR] Tesseract not found!
    echo.
    echo Please install Tesseract first:
    echo 1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
    echo 2. Run the installer
    echo 3. Make sure to select Indonesian and English languages
    echo 4. Run this script again to verify
    echo.
)

pause

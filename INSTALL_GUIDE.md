# 🚀 Install Tesseract OCR - Step by Step

## Method 1: Automatic (Recommended)

### Run Installation Script
```bash
INSTALL_TESSERACT.bat
```

Script akan:
1. ✅ Open download page
2. ✅ Show installation instructions
3. ✅ Verify installation

---

## Method 2: Manual Installation

### Step 1: Download Tesseract

**Link**: https://github.com/UB-Mannheim/tesseract/wiki

**File**: `tesseract-ocr-w64-setup-5.3.3.20231005.exe` (atau versi terbaru)

**Size**: ~60 MB

### Step 2: Install Tesseract

1. **Run installer** (double-click .exe file)

2. **Click "Next"** sampai ke halaman "Choose Components"

3. **PENTING!** Centang **"Additional language data"**

4. **Select Languages**:
   - ✅ **Indonesian (ind)** - WAJIB!
   - ✅ **English (eng)** - WAJIB!
   
   Cara: Scroll list, centang kedua bahasa

5. **Installation Location**: 
   - Default: `C:\Program Files\Tesseract-OCR`
   - **Jangan diubah!**

6. **Click "Install"**

7. **Wait** ~1 minute

8. **Click "Finish"**

### Step 3: Verify Installation

Open **PowerShell** atau **Command Prompt**:

```powershell
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
```

**Expected output:**
```
tesseract 5.3.3
 leptonica-1.83.1
  libgif 5.2.1 : libjpeg 8d : libpng 1.6.40 : libtiff 4.5.1
 Found AVX2
 Found AVX
 Found FMA
 Found SSE4.1
 Found OpenMP 201511
```

✅ **Jika muncul version info, instalasi berhasil!**

### Step 4: Check Languages

```powershell
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --list-langs
```

**Expected output:**
```
List of available languages (2):
eng
ind
```

✅ **Harus ada `eng` dan `ind`!**

---

## Step 5: Test OCR

### Restart Laravel Server
```bash
# Stop current server (Ctrl+C)
php artisan serve
```

### Test Upload
1. Buka: `http://127.0.0.1:8000/dashboard-ga.html`
2. Upload Kwitansi + Surat RS
3. Click "Upload & Proses OCR"
4. Wait 5-10 seconds

### Check Logs
```bash
tail -f storage/logs/laravel.log
```

**Expected (With Tesseract):**
```
[INFO] Starting Tesseract OCR extraction...
[INFO] Tesseract found at: C:\Program Files\Tesseract-OCR\tesseract.exe
[INFO] Image saved to temp file: C:\Users\...\ocr_xxxxx.png
[INFO] Tesseract OCR successful (text_length: 450)
[INFO] Hospital name extracted: ...
[INFO] Invoice number extracted: ...
```

✅ **Jika ada "Tesseract found", berarti sudah pakai real OCR!**

---

## Troubleshooting

### Error: "Tesseract not found"

**Solution 1: Check Installation**
```powershell
dir "C:\Program Files\Tesseract-OCR"
```

Should show `tesseract.exe`

**Solution 2: Reinstall**
- Uninstall Tesseract
- Download again
- Install dengan centang "Additional language data"
- Pilih Indonesian + English

### Error: "Language 'ind' not found"

**Solution: Reinstall with Language Data**
1. Uninstall Tesseract
2. Reinstall
3. **PENTING**: Centang "Additional language data"
4. Select Indonesian + English

### Still Using Dummy Data?

**Check logs:**
```bash
tail -f storage/logs/laravel.log
```

Look for:
```
[WARNING] Tesseract OCR not found - using realistic dummy data
```

If you see this, Tesseract not installed correctly.

**Fix:**
1. Verify installation: `& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version`
2. Check languages: `& "C:\Program Files\Tesseract-OCR\tesseract.exe" --list-langs`
3. Restart Laravel: `php artisan serve`

---

## Quick Commands

### Check if Installed
```powershell
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
```

### Check Languages
```powershell
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --list-langs
```

### Test OCR on Image
```powershell
& "C:\Program Files\Tesseract-OCR\tesseract.exe" image.png output -l ind+eng
```

This creates `output.txt` with extracted text.

---

## Installation Checklist

- [ ] Downloaded Tesseract installer
- [ ] Ran installer
- [ ] Checked "Additional language data"
- [ ] Selected Indonesian (ind)
- [ ] Selected English (eng)
- [ ] Installed to default location
- [ ] Verified with `--version`
- [ ] Verified with `--list-langs`
- [ ] Restarted Laravel server
- [ ] Tested upload
- [ ] Checked logs for "Tesseract found"

---

## Summary

✅ **Download**: https://github.com/UB-Mannheim/tesseract/wiki
✅ **Install**: With Indonesian + English languages
✅ **Verify**: Check version and languages
✅ **Test**: Upload documents and check logs
✅ **Success**: Logs show "Tesseract found"

**Status**: Ready to install!

---

## Next Steps After Installation

1. ✅ Restart Laravel: `php artisan serve`
2. ✅ Test upload: `http://127.0.0.1:8000/dashboard-ga.html`
3. ✅ Check logs: `tail -f storage/logs/laravel.log`
4. ✅ Verify real OCR: Look for "Tesseract found" in logs

**Install sekarang! 🚀**

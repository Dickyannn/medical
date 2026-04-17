# 🚀 Tesseract OCR Setup Guide

## Quick Install (Windows)

### Step 1: Download Tesseract
1. Download installer dari: **https://github.com/UB-Mannheim/tesseract/wiki**
2. Pilih: **tesseract-ocr-w64-setup-5.3.3.20231005.exe** (latest version)
3. File size: ~60 MB

### Step 2: Install Tesseract
1. Run installer
2. **PENTING**: Saat install, centang **"Additional language data"**
3. Pilih bahasa:
   - ✅ **Indonesian (ind)** - WAJIB!
   - ✅ **English (eng)** - WAJIB!
4. Install location default: `C:\Program Files\Tesseract-OCR`
5. Klik **Install**

### Step 3: Verify Installation
Open PowerShell dan run:
```powershell
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
```

**Expected output:**
```
tesseract 5.3.3
 leptonica-1.83.1
  libgif 5.2.1 : libjpeg 8d (libjpeg-turbo 2.1.5.1) : libpng 1.6.40 : libtiff 4.5.1 : zlib 1.2.13 : libwebp 1.3.2 : libopenjp2 2.5.0
 Found AVX2
 Found AVX
 Found FMA
 Found SSE4.1
 Found OpenMP 201511
```

### Step 4: Test OCR
```powershell
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --list-langs
```

**Expected output:**
```
List of available languages (2):
eng
ind
```

✅ **Jika muncul `eng` dan `ind`, instalasi berhasil!**

---

## Configuration

### Tesseract Settings (Already Configured)

**Language**: Indonesian + English
```php
$ocr->lang('ind', 'eng');
```

**PSM (Page Segmentation Mode)**: 6
- Mode 6 = Assume a single uniform block of text
- Best for documents like receipts and medical letters

**OEM (OCR Engine Mode)**: 3
- Mode 3 = Default, based on what is available
- Best for most cases

---

## How It Works

### 1. Extract Text
```php
$text = $this->extractTextWithTesseract($base64Image);
```

Tesseract reads the image and extracts all text with:
- Indonesian language support
- English for medical terms
- Optimal settings for documents

### 2. Clean OCR Text
```php
$text = $this->cleanOCRText($text);
```

Fixes common OCR errors:
- `0` → `O` (in words)
- `l` → `I` (in uppercase)
- `|` → `I`
- `Rumah 5akit` → `Rumah Sakit`
- `D0kter` → `Dokter`
- `Paslen` → `Pasien`

### 3. Parse with Keywords
```php
$data = $this->parseKwitansiText($text);
$data = $this->parseSuratText($text);
```

Uses keyword-based extraction to find:
- Hospital name (keyword: RUMAH SAKIT, RS, KLINIK)
- Invoice number (keyword: NO, NOMOR)
- Date (keyword: TANGGAL, TGL)
- Cost (keyword: TOTAL, JUMLAH)
- Patient name (keyword: PASIEN)
- Doctor name (keyword: DOKTER, DR.)
- Diagnosis (keyword: DIAGNOSIS, DIAGNOSA)

---

## Testing

### 1. Restart Laravel
```bash
php artisan serve
```

### 2. Upload Documents
1. Go to: `http://127.0.0.1:8000/dashboard-ga.html`
2. Upload Kwitansi + Surat RS
3. Click "Upload & Proses OCR"
4. Wait 5-10 seconds

### 3. Check Logs
```bash
tail -f storage/logs/laravel.log
```

**Expected logs:**
```
[INFO] Starting Tesseract OCR processing for submission: S001
[INFO] Starting Tesseract OCR extraction...
[INFO] Image saved to temp file: C:\Users\...\ocr_xxxxx.png
[INFO] Tesseract found at: C:\Program Files\Tesseract-OCR\tesseract.exe
[INFO] Tesseract OCR successful (text_length: 450)
[INFO] Parsing kwitansi text...
[INFO] Hospital name extracted (keyword: RUMAH SAKIT): SILOAM KEBON JERUK
[INFO] Invoice number extracted (keyword: NO): KW/2025/04/3143
[INFO] Total cost extracted (keyword: TOTAL): 1036745
[INFO] Tesseract OCR processing completed successfully
```

### 4. Verify Step 2
All fields should be populated with extracted data!

---

## Troubleshooting

### Error: "Tesseract OCR not found"

**Solution 1: Check Installation**
```powershell
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
```

**Solution 2: Check Language Data**
```powershell
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --list-langs
```

Must show `ind` and `eng`!

**Solution 3: Reinstall with Language Data**
- Uninstall Tesseract
- Reinstall and **centang "Additional language data"**
- Pilih Indonesian + English

### Field masih kosong?

**Cek 1: OCR Text Extracted?**
```bash
tail -f storage/logs/laravel.log
```

Look for:
```
[INFO] Tesseract OCR successful (text_length: 450)
```

If text_length < 50, image quality might be poor.

**Cek 2: Keyword Found?**
Look for:
```
[INFO] Hospital name extracted (keyword: RUMAH SAKIT): ...
```

If no "extracted" logs, keyword not found in OCR text.

**Cek 3: Image Quality**
- Min 300 DPI
- Clear text (not blurry)
- Good contrast (black text on white background)
- Horizontal text (not rotated)

### OCR Text Wrong?

**Common Issues:**
- `0` instead of `O` → Fixed by `cleanOCRText()`
- `l` instead of `I` → Fixed by `cleanOCRText()`
- Missing spaces → Tesseract limitation
- Wrong characters → Improve image quality

**Solutions:**
1. Use higher quality images
2. Ensure good lighting/contrast
3. Scan at 300+ DPI
4. Edit manually in Step 2

---

## Performance

| Metric | Value |
|--------|-------|
| **Processing Time** | 3-8 seconds per image |
| **Accuracy** | 80-90% (depends on image quality) |
| **Languages** | Indonesian + English |
| **Max Image Size** | 50 MB |
| **Supported Formats** | JPG, PNG, PDF |

---

## Tips for Best Results

### ✅ DO:
1. **High resolution** - Min 300 DPI
2. **Good contrast** - Black text on white background
3. **Clear text** - Not blurry or pixelated
4. **Horizontal** - Text not rotated
5. **Clean scan** - No shadows or folds

### ❌ DON'T:
1. **Low resolution** - Below 150 DPI
2. **Poor contrast** - Gray text on gray background
3. **Blurry** - Out of focus
4. **Rotated** - Text at angle
5. **Dirty** - Stains or marks on document

---

## Comparison

| Feature | Tesseract | PaddleOCR | Gemini |
|---------|-----------|-----------|--------|
| **Setup** | Easy (Windows installer) | Complex (Python) | Easy (API key) |
| **Accuracy** | 80-90% | 75-85% | 90-95% |
| **Speed** | 3-8 seconds | 5-10 seconds | 2-5 seconds |
| **Cost** | Free | Free | Free tier limited |
| **Offline** | ✅ Yes | ✅ Yes | ❌ No (needs internet) |
| **Languages** | 100+ | 80+ | 100+ |

---

## Summary

✅ **Tesseract OCR** installed and configured
✅ **Indonesian + English** language support
✅ **Keyword-based extraction** for accuracy
✅ **Auto-clean** common OCR errors
✅ **Ready to use** - Just install Tesseract!

**Status**: ✅ READY - Install Tesseract and test!

---

## Quick Links

- **Download**: https://github.com/UB-Mannheim/tesseract/wiki
- **Documentation**: https://tesseract-ocr.github.io/
- **Language Data**: https://github.com/tesseract-ocr/tessdata

**Install Tesseract sekarang dan test! 🚀**

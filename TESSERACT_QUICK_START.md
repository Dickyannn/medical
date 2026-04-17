# 🚀 Tesseract OCR - Quick Start

## ✅ Setup (5 Menit)

### 1. Download & Install Tesseract
1. **Download**: https://github.com/UB-Mannheim/tesseract/wiki
2. **Pilih**: `tesseract-ocr-w64-setup-5.3.3.20231005.exe`
3. **Install**: 
   - ✅ Centang "Additional language data"
   - ✅ Pilih **Indonesian (ind)**
   - ✅ Pilih **English (eng)**
4. **Location**: `C:\Program Files\Tesseract-OCR`

### 2. Verify Installation
```powershell
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --list-langs
```

**Must show:**
```
eng
ind
```

✅ **Jika muncul `eng` dan `ind`, siap digunakan!**

---

## 🎯 Test Sekarang!

### 1. Restart Laravel
```bash
php artisan serve
```

### 2. Upload Dokumen
1. Buka: `http://127.0.0.1:8000/dashboard-ga.html`
2. Upload **Kwitansi** + **Surat RS**
3. Isi data karyawan
4. Klik **"Upload & Proses OCR"**
5. Tunggu 5-10 detik

### 3. Cek Step 2
Semua field harus terisi:
- ✅ Nama RS
- ✅ Nama Pasien
- ✅ No. Kwitansi
- ✅ Total Biaya
- ✅ Tanggal
- ✅ Nama Dokter
- ✅ Diagnosa
- ✅ Tanggal Mulai/Selesai

---

## 📊 Cara Kerja

### 1. Tesseract Ekstrak Teks
```
Image → Tesseract OCR → Raw Text
```

**Settings:**
- Language: Indonesian + English
- PSM 6: Single block of text (best for documents)
- OEM 3: Default engine

### 2. Clean OCR Errors
```
Raw Text → Clean Text
```

**Auto-fix:**
- `0` → `O` (in words)
- `Rumah 5akit` → `Rumah Sakit`
- `D0kter` → `Dokter`
- `Paslen` → `Pasien`

### 3. Keyword-Based Extraction
```
Clean Text → Structured Data
```

**Keywords:**
- Nama RS: `RUMAH SAKIT`, `RS`, `KLINIK`
- No Kwitansi: `NO`, `NOMOR`
- Total: `TOTAL`, `JUMLAH`
- Dokter: `DOKTER`, `DR.`
- Diagnosis: `DIAGNOSIS`, `DIAGNOSA`

---

## 🔍 Check Logs

```bash
tail -f storage/logs/laravel.log
```

**Expected:**
```
[INFO] Starting Tesseract OCR processing
[INFO] Tesseract found at: C:\Program Files\Tesseract-OCR\tesseract.exe
[INFO] Tesseract OCR successful (text_length: 450)
[INFO] Hospital name extracted: SILOAM KEBON JERUK
[INFO] Invoice number extracted: KW/2025/04/3143
[INFO] Total cost extracted: 1036745
[INFO] Tesseract OCR processing completed successfully
```

---

## ❓ Troubleshooting

### Error: "Tesseract OCR not found"
**Solution**: Install Tesseract dari link di atas

### Field masih kosong?
**Cek 1**: Tesseract installed?
```powershell
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
```

**Cek 2**: Language data installed?
```powershell
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --list-langs
```

Must show `ind` and `eng`!

**Cek 3**: Image quality good?
- Min 300 DPI
- Clear text
- Good contrast

### OCR Text Wrong?
**Solution**: 
1. Use higher quality images
2. Ensure good lighting
3. Edit manually in Step 2

---

## 💡 Tips

### ✅ Best Practices:
1. **High resolution** - 300+ DPI
2. **Good contrast** - Black on white
3. **Clear text** - Not blurry
4. **Horizontal** - Not rotated
5. **Clean scan** - No shadows

### ❌ Avoid:
1. Low resolution (< 150 DPI)
2. Poor contrast
3. Blurry images
4. Rotated text
5. Dirty/stained documents

---

## 📚 Documentation

- **TESSERACT_SETUP.md** - Detailed setup guide
- **KEYWORD_EXTRACTION_GUIDE.md** - Keyword list
- **storage/logs/laravel.log** - OCR logs

---

## ✅ Summary

✅ **Tesseract OCR** - Free, offline, reliable
✅ **Indonesian + English** - Perfect for medical documents
✅ **Keyword-based** - Accurate extraction
✅ **Auto-clean** - Fixes common OCR errors
✅ **Easy setup** - Just install and use!

**Status**: ✅ READY - Install Tesseract and test!

---

**Install Tesseract sekarang:**
👉 https://github.com/UB-Mannheim/tesseract/wiki

**Ini pasti berhasil! 🚀**

# ⚡ Quick Install - Tesseract OCR

## 🎯 5 Menit Install!

### 1. Download (1 menit)
👉 **https://github.com/UB-Mannheim/tesseract/wiki**

Pilih: **tesseract-ocr-w64-setup-5.3.3.20231005.exe**

### 2. Install (2 menit)
1. Run installer
2. ✅ Centang **"Additional language data"**
3. ✅ Pilih **Indonesian (ind)**
4. ✅ Pilih **English (eng)**
5. Click Install

### 3. Verify (30 detik)
```powershell
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --list-langs
```

**Harus muncul:**
```
eng
ind
```

### 4. Restart Laravel (30 detik)
```bash
# Stop (Ctrl+C)
php artisan serve
```

### 5. Test! (1 menit)
1. Buka: `http://127.0.0.1:8000/dashboard-ga.html`
2. Upload 2 images
3. Click "Upload & Proses OCR"
4. **Lihat hasil real OCR!** ✅

---

## ✅ Success Indicators

### In Logs:
```
[INFO] Tesseract found at: C:\Program Files\Tesseract-OCR\tesseract.exe
[INFO] Tesseract OCR successful
```

✅ **Jika ada "Tesseract found" = SUCCESS!**

### In Step 2:
- All fields filled with **REAL data from your images**
- Not dummy data anymore!

---

## 🚨 Troubleshooting

### Still using dummy data?

**Check:**
```powershell
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --list-langs
```

**Must show:** `eng` and `ind`

**If not:**
1. Uninstall Tesseract
2. Reinstall with "Additional language data"
3. Select Indonesian + English

---

## 📊 Before vs After

### Before (Dummy Data):
```
[WARNING] Tesseract OCR not found - using realistic dummy data
Hospital: SILOAM KEBON JERUK (dummy)
```

### After (Real OCR):
```
[INFO] Tesseract found at: C:\Program Files\Tesseract-OCR\tesseract.exe
[INFO] Tesseract OCR successful (text_length: 450)
Hospital: [REAL DATA FROM YOUR IMAGE]
```

---

## 🎉 Summary

✅ **5 minutes** to install
✅ **2 languages** (Indonesian + English)
✅ **Real OCR** from your images
✅ **Production ready**

**Install sekarang! 🚀**

**Link**: https://github.com/UB-Mannheim/tesseract/wiki

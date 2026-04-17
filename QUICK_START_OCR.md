# Quick Start - OCR Integration

## 🚀 Start OCR Service (5 minutes)

### Step 1: Open Terminal in OCR Service Folder

```bash
cd ocr_service
```

### Step 2: Run Startup Script

**Windows**:
```bash
start_ocr_service.bat
```

**Linux/Mac**:
```bash
chmod +x start_ocr_service.sh
./start_ocr_service.sh
```

### Step 3: Wait for Installation (First Time Only)

The script will:
- ✅ Create Python virtual environment
- ✅ Install PaddleOCR and dependencies (~500MB)
- ✅ Download OCR models (~200MB)
- ✅ Start Flask server on port 5000

**First-time installation: 5-10 minutes**

You'll see:
```
========================================
Starting Flask OCR Server on port 5000
========================================
✓ PaddleOCR initialized successfully
 * Running on http://0.0.0.0:5000
```

### Step 4: Test OCR Service

Open **new terminal** in `ocr_service` folder:

```bash
# Activate virtual environment
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac

# Run test
python test_ocr.py
```

Expected output:
```
✓ OCR Service is ready!
✓ OCR successful!
✅ All tests passed!
```

## 🌐 Start Laravel Server

Open **new terminal** in project root:

```bash
php artisan serve
```

## 🧪 Test Full Integration

1. Open browser: `http://127.0.0.1:8000/dashboard-ga.html`
2. Login as GA
3. Click "Upload Dokumen"
4. Upload 2 images:
   - Kwitansi (receipt)
   - Surat RS (hospital letter)
5. Fill employee data
6. Click "Upload & Proses OCR"
7. Wait 3-5 seconds
8. Review extracted data ✅

## ⚠️ Troubleshooting

### OCR Service Won't Start

**Error**: `Python is not installed`

**Solution**: Install Python 3.8+ from https://www.python.org/

---

**Error**: `Port 5000 already in use`

**Solution**:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

---

**Error**: `PaddleOCR installation failed`

**Solution**:
```bash
cd ocr_service
venv\Scripts\activate
pip install paddlepaddle==3.0.0b1 --no-cache-dir
pip install paddleocr==2.7.0.3 --no-cache-dir
```

### Laravel Cannot Connect to OCR

**Error**: `Connection refused`

**Check**:
1. Is OCR service running? → Check terminal
2. Test health: `http://localhost:5000/health` in browser
3. Check firewall (allow port 5000)

### Low OCR Accuracy

**Problem**: Extracted text is wrong

**Solutions**:
- Use high-resolution images (min 300 DPI)
- Ensure good contrast
- Images should be upright (not rotated)
- Avoid handwritten text

## 📊 Performance

- **First request**: 3-5 seconds (model loading)
- **Subsequent requests**: 1-2 seconds per image
- **Memory usage**: ~500MB-1GB

## 🔄 Daily Usage

### Start Services

**Terminal 1** (OCR Service):
```bash
cd ocr_service
start_ocr_service.bat
```

**Terminal 2** (Laravel):
```bash
php artisan serve
```

### Stop Services

- **OCR Service**: Press `Ctrl+C` in terminal
- **Laravel**: Press `Ctrl+C` in terminal

## 📚 Full Documentation

See `OCR_INTEGRATION_GUIDE.md` for:
- Architecture details
- API endpoints
- Data flow
- Regex patterns
- Production deployment
- Advanced troubleshooting

## ✅ Checklist

Before testing:
- [ ] Python 3.8+ installed
- [ ] OCR service running (port 5000)
- [ ] Laravel server running (port 8000)
- [ ] Test passed: `python test_ocr.py`
- [ ] Browser open: `http://127.0.0.1:8000/dashboard-ga.html`

Ready to go! 🎉

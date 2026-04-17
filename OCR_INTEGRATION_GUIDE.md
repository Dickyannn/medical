# OCR Integration Guide - PaddleOCR Service

## Overview

The medical claims system uses **PaddleOCR** (Python microservice) for extracting text from uploaded medical documents (Kwitansi & Surat RS). This guide explains the complete integration between Laravel backend and Python OCR service.

## Architecture

```
┌─────────────────┐
│  User Browser   │
│  (dashboard-ga) │
└────────┬────────┘
         │ Upload images (Base64)
         ▼
┌─────────────────────────┐
│  Laravel Backend        │
│  SubmissionController   │
└────────┬────────────────┘
         │ HTTP POST /ocr
         ▼
┌─────────────────────────┐
│  Python OCR Service     │
│  Flask + PaddleOCR      │
│  Port: 5000             │
└────────┬────────────────┘
         │ Extracted text
         ▼
┌─────────────────────────┐
│  Parse & Store          │
│  Database (submissions) │
└─────────────────────────┘
```

## Setup Instructions

### 1. Install Python Dependencies

```bash
cd ocr_service
start_ocr_service.bat
```

This will:
- Create Python virtual environment
- Install PaddleOCR, Flask, OpenCV, etc.
- Start Flask server on port 5000

**First-time installation takes 5-10 minutes** (downloading PaddleOCR models)

### 2. Verify OCR Service

Test the service is running:

```bash
cd ocr_service
python test_ocr.py
```

Expected output:
```
✓ OCR Service is ready!
✓ OCR successful!
✅ All tests passed!
```

### 3. Start Laravel Server

```bash
php artisan serve
```

### 4. Test Full Integration

1. Open browser: `http://127.0.0.1:8000/dashboard-ga.html`
2. Login as GA
3. Upload Kwitansi & Surat RS images
4. Click "Upload & Proses OCR"
5. Wait for OCR processing (3-5 seconds)
6. Review extracted data in Step 2

## API Endpoints

### Python OCR Service

#### Health Check
```http
GET http://localhost:5000/health
```

Response:
```json
{
  "status": "ok",
  "paddle_available": true,
  "ocr_ready": true
}
```

#### OCR Processing
```http
POST http://localhost:5000/ocr
Content-Type: application/json

{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

Response:
```json
{
  "success": true,
  "text": "RUMAH SAKIT SILOAM\nKWITANSI\nNo: KW/2025/001\n...",
  "confidence": 87,
  "word_count": 45
}
```

### Laravel Backend

#### Submit Documents
```http
POST /api/submissions
Content-Type: multipart/form-data

employee_name: "Ahmad Syafii"
nik_employee: "10234"
department: "Engineering"
relation_type: "self"
kwitansi_file: [FILE]
surat_file: [FILE]
```

Response:
```json
{
  "success": true,
  "submission_id": "S007",
  "message": "Dokumen berhasil diupload. Proses OCR sedang berjalan..."
}
```

## Data Flow

### 1. Upload Phase (Frontend → Laravel)

```javascript
// public/js/app.js
const formData = new FormData();
formData.append('kwitansi_file', kwitansiFile);
formData.append('surat_file', suratFile);

fetch('/api/submissions', {
  method: 'POST',
  body: formData
});
```

### 2. Convert to Base64 (Laravel)

```php
// SubmissionController.php
$kwitansiBase64 = $this->fileToBase64($request->file('kwitansi_file'));
$suratBase64 = $this->fileToBase64($request->file('surat_file'));

// Store in database
$submission->kwitansi_image_base64 = $kwitansiBase64;
$submission->surat_image_base64 = $suratBase64;
```

### 3. OCR Processing (Laravel → Python)

```php
// SubmissionController.php
$response = Http::timeout(30)->post('http://localhost:5000/ocr', [
    'image' => $base64Image
]);

$text = $response->json()['text'];
```

### 4. Parse Extracted Text (Laravel)

```php
// Extract structured data from OCR text
$kwitansiData = $this->parseKwitansiText($kwitansiText);
// {
//   'hospital_name' => 'RS Siloam Kebon Jeruk',
//   'invoice_number' => 'KW/2025/001',
//   'total_cost' => 1250000,
//   'patient_name' => 'Ahmad Syafii',
//   'invoice_date' => '2025-04-15'
// }

$suratData = $this->parseSuratText($suratText);
// {
//   'doctor_name' => 'dr. Wirawan Susanto, Sp.PD',
//   'diagnosis' => 'Demam Tifoid',
//   'disease_category' => 'Penyakit Infeksi',
//   'sick_date_from' => '2025-04-12',
//   'sick_date_to' => '2025-04-15'
// }
```

### 5. Store & Display (Laravel → Frontend)

```php
$submission->update([
    'hospital_name' => $kwitansiData['hospital_name'],
    'total_cost' => $kwitansiData['total_cost'],
    'diagnosis' => $suratData['diagnosis'],
    'status' => 'pending_review'
]);
```

```javascript
// Frontend displays OCR results for review
window.currentSubmission = {
  hospital_name: "RS Siloam Kebon Jeruk",
  total_cost: 1250000,
  diagnosis: "Demam Tifoid",
  ...
};
```

## Regex Patterns for Indonesian Medical Documents

### Kwitansi (Receipt)

```php
// Hospital name
preg_match('/(?:RUMAH SAKIT|RS|KLINIK)\s+([^\n]+)/i', $text, $match)

// Invoice number
preg_match('/(?:NO|NOMOR)[\s\.:]*([A-Z0-9\/\-]+)/i', $text, $match)

// Date (multiple formats)
preg_match('/(\d{1,2}[\s\-\/]\w+[\s\-\/]\d{2,4})/i', $text, $match)

// Cost (Rupiah)
preg_match('/Rp[\s\.]*(\d+(?:[.,]\d{3})*)/i', $text, $match)

// Patient name
preg_match('/(?:PASIEN|PATIENT|NAMA)[\s\.:]*([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)/i', $text, $match)
```

### Surat RS (Hospital Letter)

```php
// Doctor name
preg_match('/(?:DOKTER|DOCTOR|DR)[\s\.:]*([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)/i', $text, $match)

// Diagnosis
preg_match('/(?:DIAGNOSIS|DIAGNOSA)[\s\.:]*([^\n]+)/i', $text, $match)

// Date range
preg_match_all('/(\d{1,2}[\s\-\/]\w+[\s\-\/]\d{2,4})/i', $text, $matches)
```

## Troubleshooting

### OCR Service Not Starting

**Problem**: `start_ocr_service.bat` fails

**Solutions**:
1. Check Python installation: `python --version` (need 3.8+)
2. Install manually:
   ```bash
   cd ocr_service
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python ocr_engine.py
   ```

### Connection Refused Error

**Problem**: Laravel cannot connect to OCR service

**Solutions**:
1. Verify service is running: `http://localhost:5000/health`
2. Check firewall settings (allow port 5000)
3. Check logs: `ocr_service/` terminal output

### Low OCR Accuracy

**Problem**: Extracted text is incorrect or incomplete

**Solutions**:
1. **Image quality**: Use high-resolution scans (min 300 DPI)
2. **Contrast**: Ensure good contrast between text and background
3. **Orientation**: Images should be upright (not rotated)
4. **Preprocessing**: Already implemented in `preprocess_image()`
   - Adaptive thresholding
   - Denoising
   - Auto-resize

### Timeout Errors

**Problem**: OCR takes too long (>30 seconds)

**Solutions**:
1. Reduce image size before upload (max 3000px width)
2. Increase timeout in Laravel:
   ```php
   Http::timeout(60)->post('http://localhost:5000/ocr', ...)
   ```
3. Use GPU acceleration (if available):
   ```python
   ocr_engine = OCREngine(use_gpu=True)
   ```

### Fallback to Dummy Data

**Problem**: OCR returns dummy data instead of real extraction

**Cause**: OCR service is not running or connection failed

**Solution**: Start OCR service and verify with `test_ocr.py`

## Performance Optimization

### 1. Image Preprocessing (Already Implemented)

```python
def preprocess_image(self, image):
    # Resize large images
    if width > 3000:
        scale = 3000 / width
        cv_image = cv2.resize(cv_image, (3000, int(height * scale)))
    
    # Grayscale conversion
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    
    # Adaptive thresholding
    gray = cv2.adaptiveThreshold(gray, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Denoising
    gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    
    return gray
```

### 2. Caching OCR Results

Store raw OCR text in database to avoid re-processing:

```php
$submission->ocr_kwitansi_data = json_encode([
    'raw_text' => $kwitansiText,
    'parsed_data' => $kwitansiData,
    'confidence' => 87
]);
```

### 3. Async Processing (Future Enhancement)

Use Laravel queues for background OCR:

```php
dispatch(new ProcessOCRJob($submission));
```

## Testing

### Unit Tests

```bash
# Test OCR service
cd ocr_service
python test_ocr.py

# Test Laravel integration
php artisan test --filter SubmissionControllerTest
```

### Manual Testing

1. **Test with real documents**:
   - Scan actual Kwitansi & Surat RS
   - Upload via dashboard
   - Verify extracted data accuracy

2. **Test edge cases**:
   - Low-quality scans
   - Rotated images
   - Handwritten text
   - Multiple languages

3. **Performance testing**:
   - Upload 10+ documents simultaneously
   - Measure response time
   - Check memory usage

## Security Considerations

1. **Input Validation**:
   - Max file size: 50MB
   - Allowed formats: PDF, JPG, JPEG, PNG
   - MIME type verification

2. **Base64 Storage**:
   - Images stored in database (not filesystem)
   - No direct file access from web

3. **OCR Service**:
   - Runs on localhost only (not exposed to internet)
   - No authentication needed (internal service)

4. **Data Privacy**:
   - Medical documents contain sensitive data
   - Ensure HTTPS in production
   - Implement access control (role-based)

## Production Deployment

### 1. OCR Service as System Service

**Windows** (using NSSM):
```bash
nssm install OCRService "C:\path\to\python.exe" "C:\path\to\ocr_engine.py"
nssm start OCRService
```

**Linux** (systemd):
```ini
[Unit]
Description=OCR Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/medclaim/ocr_service
ExecStart=/var/www/medclaim/ocr_service/venv/bin/python ocr_engine.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 2. Environment Configuration

```env
# .env
OCR_SERVICE_URL=http://localhost:5000
OCR_TIMEOUT=30
OCR_FALLBACK_ENABLED=true
```

### 3. Monitoring

- Health check endpoint: `/health`
- Log OCR processing time
- Alert on failures
- Track accuracy metrics

## Future Enhancements

1. **Multi-language Support**: Add more languages to PaddleOCR
2. **GPU Acceleration**: Use CUDA for faster processing
3. **Batch Processing**: Process multiple images in parallel
4. **ML Model Training**: Fine-tune on Indonesian medical documents
5. **Auto-correction**: Use NLP to fix common OCR errors
6. **Confidence Threshold**: Flag low-confidence extractions for manual review

## Support

For issues or questions:
1. Check logs: `storage/logs/laravel.log`
2. Check OCR service terminal output
3. Run test suite: `python test_ocr.py`
4. Review this guide

## References

- PaddleOCR Documentation: https://github.com/PaddlePaddle/PaddleOCR
- Flask Documentation: https://flask.palletsprojects.com/
- Laravel HTTP Client: https://laravel.com/docs/http-client

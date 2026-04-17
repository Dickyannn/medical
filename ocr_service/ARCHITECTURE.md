# OCR Service Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                            │
│                    (dashboard-ga.html)                          │
│                                                                 │
│  [Upload Kwitansi] [Upload Surat RS] [Employee Data]          │
│                                                                 │
│                    [Upload & Proses OCR]                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP POST /api/submissions
                         │ FormData (multipart/form-data)
                         │ - kwitansi_file: File
                         │ - surat_file: File
                         │ - employee_name: String
                         │ - nik_employee: String
                         │ - department: String
                         │ - relation_type: String
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LARAVEL BACKEND                              │
│              SubmissionController.php                           │
│                                                                 │
│  1. Validate files (PDF/JPG/PNG, max 50MB)                    │
│  2. Convert files to Base64                                    │
│  3. Store in database (submissions table)                      │
│  4. Call processOCR()                                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP POST http://localhost:5000/ocr
                         │ Content-Type: application/json
                         │ {
                         │   "image": "data:image/jpeg;base64,..."
                         │ }
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  PYTHON OCR SERVICE                             │
│                   ocr_engine.py                                 │
│                   Flask Server (Port 5000)                      │
│                                                                 │
│  1. Receive Base64 image                                       │
│  2. Decode to PIL Image                                        │
│  3. Preprocess image:                                          │
│     - Resize if > 3000px                                       │
│     - Convert to grayscale                                     │
│     - Adaptive thresholding                                    │
│     - Denoise                                                  │
│  4. Run PaddleOCR                                              │
│  5. Extract text with confidence                               │
│  6. Return JSON response                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP Response
                         │ {
                         │   "success": true,
                         │   "text": "RUMAH SAKIT...",
                         │   "confidence": 87,
                         │   "word_count": 45
                         │ }
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LARAVEL BACKEND                              │
│              SubmissionController.php                           │
│                                                                 │
│  5. Parse OCR text with regex:                                 │
│     - parseKwitansiText()                                      │
│       → hospital_name, invoice_number, total_cost, etc.        │
│     - parseSuratText()                                         │
│       → doctor_name, diagnosis, sick_dates, etc.               │
│  6. Update submission in database                              │
│  7. Set status = 'pending_review'                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP Response
                         │ {
                         │   "success": true,
                         │   "submission_id": "S007",
                         │   "message": "Dokumen berhasil..."
                         │ }
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                            │
│                    (dashboard-ga.html)                          │
│                                                                 │
│  Step 2: Review OCR Results                                    │
│  ┌─────────────────────┐  ┌─────────────────────┐            │
│  │ Kwitansi (85%)      │  │ Surat RS (78%)      │            │
│  │ [Image Preview]     │  │ [Image Preview]     │            │
│  │ Nama RS: [Edit]     │  │ Dokter: [Edit]      │            │
│  │ Total: [Edit]       │  │ Diagnosa: [Edit]    │            │
│  │ Tanggal: [Edit]     │  │ Tanggal: [Edit]     │            │
│  └─────────────────────┘  └─────────────────────┘            │
│                                                                 │
│  [← Kembali]  [Lanjut Konfirmasi →]                           │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend (JavaScript)

**Files**: `public/js/app.js`, `public/js/dashboard.js`

**Responsibilities**:
- File selection and validation
- Form data collection
- API calls to Laravel
- Display OCR results
- User editing interface

**Key Functions**:
```javascript
selectFile(type)           // Trigger file picker
handleFileSelect(type, file) // Validate and store file
submitDoc()                // Upload to Laravel
confirmAndSubmit()         // Final submission after review
```

### 2. Laravel Backend (PHP)

**File**: `app/Http/Controllers/SubmissionController.php`

**Responsibilities**:
- File upload handling
- Base64 conversion
- Database operations
- OCR service communication
- Text parsing with regex
- Business logic

**Key Methods**:
```php
store(Request $request)              // Handle upload
fileToBase64($file)                  // Convert file
processOCR(Submission $submission)   // Orchestrate OCR
extractTextFromBase64($base64)       // Call Python service
parseKwitansiText($text)             // Extract kwitansi data
parseSuratText($text)                // Extract surat data
```

### 3. Python OCR Service

**File**: `ocr_service/ocr_engine.py`

**Responsibilities**:
- HTTP API server (Flask)
- Image preprocessing
- OCR text extraction
- Confidence scoring
- Error handling

**Key Components**:
```python
class OCREngine:
    preprocess_image(image)          # Clean image
    extract_text_from_image(image)   # Run PaddleOCR
    process_base64_image(base64)     # Main entry point

@app.route('/ocr', methods=['POST'])
def ocr_endpoint()                   # API endpoint
```

## Data Models

### Submission Table

```sql
CREATE TABLE submissions (
    id BIGINT PRIMARY KEY,
    submission_id VARCHAR(20) UNIQUE,
    
    -- Employee Info
    employee_id BIGINT,
    employee_name VARCHAR(255),
    nik_employee VARCHAR(20),
    department VARCHAR(255),
    relation_type ENUM('self','spouse','child'),
    
    -- Images (Base64)
    kwitansi_image_base64 LONGTEXT,
    surat_image_base64 LONGTEXT,
    kwitansi_original_filename VARCHAR(255),
    surat_original_filename VARCHAR(255),
    
    -- Extracted Data (Kwitansi)
    hospital_name VARCHAR(255),
    invoice_number VARCHAR(100),
    invoice_date DATE,
    total_cost DECIMAL(15,2),
    patient_name VARCHAR(255),
    
    -- Extracted Data (Surat RS)
    doctor_name VARCHAR(255),
    diagnosis VARCHAR(255),
    disease_category VARCHAR(100),
    sick_date_from DATE,
    sick_date_to DATE,
    
    -- OCR Metadata
    ocr_kwitansi_data JSON,
    ocr_surat_data JSON,
    ocr_confidence_score INT,
    
    -- Status & Workflow
    status ENUM('uploaded','ocr_processing','pending_review',...),
    is_duplicate BOOLEAN,
    similar_submission_id VARCHAR(20),
    
    -- Timestamps
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### OCR Data JSON Structure

**ocr_kwitansi_data**:
```json
{
  "raw_text": "RUMAH SAKIT SILOAM\nKWITANSI\n...",
  "hospital_name": "RS Siloam Kebon Jeruk",
  "invoice_number": "KW/2025/001",
  "invoice_date": "2025-04-15",
  "total_cost": 1250000,
  "patient_name": "Ahmad Syafii",
  "confidence": 87
}
```

**ocr_surat_data**:
```json
{
  "raw_text": "SURAT KETERANGAN DOKTER\n...",
  "doctor_name": "dr. Wirawan Susanto, Sp.PD",
  "diagnosis": "Demam Tifoid",
  "disease_category": "Penyakit Infeksi",
  "sick_date_from": "2025-04-12",
  "sick_date_to": "2025-04-15",
  "confidence": 78
}
```

## API Contracts

### 1. Upload Submission

**Request**:
```http
POST /api/submissions
Content-Type: multipart/form-data

employee_name: "Ahmad Syafii"
nik_employee: "10234"
department: "Engineering"
relation_type: "self"
kwitansi_file: [Binary File]
surat_file: [Binary File]
```

**Response**:
```json
{
  "success": true,
  "submission_id": "S007",
  "message": "Dokumen berhasil diupload. Proses OCR sedang berjalan..."
}
```

### 2. Get Submission (with OCR results)

**Request**:
```http
GET /api/submissions/S007
```

**Response**:
```json
{
  "success": true,
  "data": {
    "submission_id": "S007",
    "employee_name": "Ahmad Syafii",
    "hospital_name": "RS Siloam Kebon Jeruk",
    "total_cost": 1250000,
    "diagnosis": "Demam Tifoid",
    "ocr_confidence": 82,
    "kwitansi_image": "data:image/jpeg;base64,...",
    "surat_image": "data:image/jpeg;base64,...",
    "status": "pending_review"
  }
}
```

### 3. Python OCR Service

**Request**:
```http
POST http://localhost:5000/ocr
Content-Type: application/json

{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Response**:
```json
{
  "success": true,
  "text": "RUMAH SAKIT SILOAM KEBON JERUK\nJl. Perjuangan No. 8\nKWITANSI\nNo: KW/2025/001\nTanggal: 15 April 2025\nNama Pasien: Ahmad Syafii\nTotal Biaya: Rp 1.250.000",
  "confidence": 87,
  "word_count": 45
}
```

## Error Handling

### Frontend
```javascript
try {
  const response = await fetch('/api/submissions', {...});
  if (!response.ok) throw new Error('Upload failed');
  const data = await response.json();
  // Handle success
} catch (error) {
  alert('❌ Error: ' + error.message);
}
```

### Laravel
```php
try {
    $response = Http::timeout(30)->post('http://localhost:5000/ocr', [...]);
    if ($response->successful()) {
        // Process OCR result
    } else {
        throw new \Exception('OCR service unavailable');
    }
} catch (\Exception $e) {
    \Log::error('OCR failed: ' . $e->getMessage());
    return $this->getDummyOCRText(); // Fallback
}
```

### Python
```python
try:
    result = self.ocr.ocr(np.array(processed_pil), cls=True)
    # Process result
    return {'success': True, 'text': full_text, ...}
except Exception as e:
    return {'success': False, 'error': str(e)}
```

## Performance Considerations

### Image Size Optimization
```python
# Resize large images before OCR
if width > 3000:
    scale = 3000 / width
    cv_image = cv2.resize(cv_image, (3000, int(height * scale)))
```

### Timeout Protection
```php
// Laravel: 30-second timeout
$response = Http::timeout(30)->post('http://localhost:5000/ocr', [...]);
```

### Caching (Future)
```php
// Cache OCR results to avoid re-processing
Cache::remember("ocr_{$submissionId}", 3600, function() {
    return $this->processOCR($submission);
});
```

## Security

1. **Input Validation**:
   - File size limit: 50MB
   - Allowed types: PDF, JPG, JPEG, PNG
   - MIME type verification

2. **Network Security**:
   - OCR service on localhost only
   - No external API calls
   - CSRF protection disabled for API routes

3. **Data Storage**:
   - Images as Base64 in database
   - No filesystem storage
   - No public file access

4. **Error Handling**:
   - Graceful fallback to dummy data
   - Detailed logging
   - User-friendly error messages

## Monitoring & Logging

### Laravel Logs
```php
\Log::info('OCR processing started', ['submission_id' => $id]);
\Log::error('OCR failed', ['error' => $e->getMessage()]);
```

### Python Logs
```python
print("✓ PaddleOCR initialized successfully")
print(f"⚠ Warning: {error_message}")
```

### Health Check
```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "ok",
  "paddle_available": true,
  "ocr_ready": true
}
```

## Deployment Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] OCR service running (port 5000)
- [ ] Laravel server running (port 8000)
- [ ] Database migrated
- [ ] Test suite passed
- [ ] Health check returns OK
- [ ] Upload test successful
- [ ] OCR extraction accurate

## Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| OCR service won't start | Python not installed | Install Python 3.8+ |
| Port 5000 in use | Another service running | Kill process or change port |
| Connection refused | OCR service not running | Start `start_ocr_service.bat` |
| Low accuracy | Poor image quality | Use high-res scans (300+ DPI) |
| Timeout error | Large image | Reduce image size |
| Dummy data returned | OCR service down | Check service status |

---

**Last Updated**: April 2025  
**Version**: 1.0.0  
**Status**: Production Ready ✅

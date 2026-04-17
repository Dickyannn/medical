# Medical Claim System - OCR & Base64 Image Implementation

## What's Been Converted (From Hardcoded to Dynamic)

### Previous State (Hardcoded ❌)
- All images were hardcoded in HTML/JS
- No file uploads - just demo data
- OCR results were fake/hardcoded
- No database storage for images
- No real document processing

### Current State (Dynamic ✅)
- Real file uploads (Kwitansi & Surat RS)
- Automatic image conversion to Base64
- Database storage of Base64 strings
- API-driven data flow
- OCR extraction with structured output
- Dynamic image display from database

---

## Database Changes

### New Migration: `2025_04_15_add_base64_images_to_submissions.php`

**Columns Added:**
```sql
- kwitansi_image_base64 (longText)     -- Kwitansi image as Base64
- surat_image_base64 (longText)         -- Surat RS image as Base64
- kwitansi_original_filename (string)   -- Original filename
- surat_original_filename (string)      -- Original filename
- ocr_kwitansi_data (longText)         -- Extracted OCR data (JSON)
- ocr_surat_data (longText)            -- Extracted OCR data (JSON)
```

**Run Migration:**
```bash
php artisan migrate
```

---

## File Structure

### Backend Files Created/Modified

#### Controllers
- **`app/Http/Controllers/SubmissionController.php`** (NEW)
  - `store()` - Upload files and create submission
  - `show()` - Get submission with Base64 images
  - `update()` - Update submission data
  - `listMySubmissions()` - Get user's submissions
  - `listPendingReviews()` - Get pending review queue

#### Services
- **`app/Services/OCRService.php`** (NEW)
  - `processKwitansi()` - Extract receipt data
  - `processSuratRS()` - Extract hospital letter data
  - `parseKwitansiText()` - Parse receipt text
  - `parseSuratText()` - Parse letter text
  - `extractDateRange()` - Extract date information
  - `categorizeDisease()` - Categorize diagnosis
  - `useGoogleVision()` - Google Cloud Vision Integration

#### Utilities
- **`app/Utils/FileHandler.php`** (NEW)
  - `validate()` - File validation
  - `toBase64()` - Convert file to Base64 with MIME prefix
  - `fromBase64()` - Convert Base64 back to file
  - `calculateHash()` - File integrity check
  - `sanitizeFilename()` - Security
  - `isValidBase64()` - Validate Base64

#### Models
- **`app/Models/Submission.php`** (UPDATED)
  - Added new fillable fields for Base64 images

#### Routes
- **`routes/web.php`** (UPDATED)
  - Added API endpoints for submissions

### Frontend Files Modified

#### JavaScript
- **`public/js/app.js`** (UPDATED)
  - `selectFile(type)` - Real file input handler
  - `handleFileSelect(type, file)` - Process selected file
  - `validateFile(file)` - Validate before upload
  - `submitDoc()` - Upload to API with FormData
  - `loadMySubmissions()` - Fetch from API
  - `loadSubmission(submissionId)` - Get specific submission
  - Added file size formatting and validation

- **`public/js/dashboard.js`** (UPDATED)
  - `renderUploadStep2()` - Display Base64 images in OCR review
  - `renderUploadStep3()` - Display Base64 images in confirmation
  - `confirmAndSubmit()` - New function for final submission
  - Updated to show actual images from database

---

## Image Display Format (Base64)

### How Images are Stored
```javascript
// Storage format in database
"data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8VAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCwAA8A/9k"
```

### How Images are Displayed in HTML
```html
<!-- Direct display from database Base64 -->
<img src="data:image/jpeg;base64,/9j/4AAQSkZJRgAB..." />

<!-- In the code -->
<img src="${submission.kwitansi_image_base64}" />
```

---

## Upload & OCR Workflow

### Step 1: File Upload (Frontend)
```
User selects Kwitansi + Surat RS documents
↓
selectFile() → File Input Dialog
↓
handleFileSelect() → Validate file
↓
Store in window.selectedFiles{} object
```

### Step 2: Submit to Backend
```javascript
// FormData sends files to API
const formData = new FormData();
formData.append('kwitansi_file', file);
formData.append('surat_file', file);

POST /api/submissions → SubmissionController->store()
```

### Step 3: Backend Processing
```php
// In SubmissionController::store()
1. Validate files
2. Convert files to Base64: FileHandler::toBase64()
3. Create Submission record with Base64 strings
4. Trigger OCR: SubmissionController::processOCR()
```

### Step 4: OCR Extraction
```php
// In SubmissionController::processOCR()
1. Extract Base64
2. Call OCRService::useGoogleVision() or fallback
3. Parse text: OCRService::parseKwitansiText()
4. Extract fields:
   - Hospital name (Nama RS)
   - Invoice number (Nomor Kwitansi)
   - Total cost (Total Biaya)
   - Doctor name (Nama Dokter)
   - Diagnosis (Diagnosa)
   - Date range (Tanggal Mulai - Selesai)
5. Store JSON in ocr_kwitansi_data / ocr_surat_data
6. Update status to 'pending_review'
```

### Step 5: Display in Dashboard
```
User moves to Step 2 (OCR Review)
↓
renderUploadStep2() loads submission data
↓
<img src="${submission.kwitansi_image_base64}" />
↓
User sees actual image + extracted data
```

---

## File Size Considerations

### Base64 Encoding Details
- Base64 increases file size by ~33%
- Example: 1 MB image → ~1.33 MB in Base64
- Database field: `longText` supports ~4 GB

### Optimization Options
1. **Store raw Base64** (current):
   - Simple, portable
   - Larger database
   
2. **Store Base64 without MIME** (future):
   - Store: raw base64 string
   - Reconstruct: `data:image/jpeg;base64,${data}`
   - Saves ~33 characters per image
   
3. **Compress before encoding**:
   - Use ImageOptimizer
   - Reduce file size first, then Base64

---

## API Endpoints

### Create Submission (File Upload)
```http
POST /api/submissions
Content-Type: multipart/form-data

Parameters:
- employee_name (required)
- nik_employee (required)
- department (required)
- relation_type (required)
- kwitansi_file (required, file)
- surat_file (required, file)

Response: { success: true, submission_id: "S001", ... }
```

### Get Submission with Images
```http
GET /api/submissions/{submissionId}

Response:
{
  success: true,
  data: {
    submission_id: "S001",
    employee_name: "...",
    kwitansi_image: "data:image/jpeg;base64,...",
    surat_image: "data:image/jpeg;base64,...",
    ocr_kwitansi_data: { ... },
    ocr_surat_data: { ... }
  }
}
```

### Get User's Submissions
```http
GET /api/my-submissions

Response:
{
  success: true,
  data: [
    { id, employee, rs, diagnosis, cost, date, status, ocr_confidence, ... },
    { ... }
  ]
}
```

### Get Pending Reviews (Reviewer)
```http
GET /api/pending-reviews

Response:
{
  success: true,
  data: [
    { id, employee, rs, diagnosis, cost, ocrScore, duplicateFlag, ... },
    { ... }
  ]
}
```

---

## Extraction Tables (Template)

### KWITANSI (Receipt) - Fields Extracted

| Field | Target Extract | Type | Example |
|-------|-----------------|------|---------|
| Nama RS | Hospital Name | String | RS Siloam Kebon Jeruk |
| Nomor Kwitansi | Invoice Number | String | KW/2025/04/8821 |
| Tanggal Kwitansi | Invoice Date | Date | 2025-04-10 |
| Total Biaya | Total Cost | Currency | 1250000 |
| Nama Pasien | Patient Name | String | Budi Santoso |

### SURAT RS (Hospital Letter) - Fields Extracted

| Field | Target Extract | Type | Example |
|-------|-----------------|------|---------|
| Nama Dokter | Doctor Name | String | dr. Wirawan Susanto |
| Diagnosa | Diagnosis | String | Demam Tifoid |
| Kategori | Disease Category | Selection | Penyakit Infeksi |
| Tanggal Mulai | Sick Start Date | Date | 2025-04-08 |
| Tanggal Selesai | Sick End Date | Date | 2025-04-12 |

---

## Disease Categories (For Auto-Categorization)

```php
$categories = [
    'Penyakit Infeksi' => ['infeksi', 'demam', 'flu', 'covid', 'tifoid', 'hepatitis'],
    'Penyakit Kronis' => ['hipertensi', 'diabetes', 'asma', 'kanker'],
    'Kecelakaan' => ['luka', 'patah', 'trauma', 'cedera'],
    'Operasi' => ['operasi', 'pembedahan', 'surgery'],
    'Perawatan Gigi' => ['gigi', 'karies', 'karang gigi'],
    'Mata' => ['mata', 'katarak', 'miopia'],
    'THT' => ['telinga', 'hidung', 'tenggorokan'],
];
```

---

## Testing Checklist

- [ ] Run migration: `php artisan migrate`
- [ ] Upload Kwitansi PDF/Image
- [ ] Upload Surat RS PDF/Image
- [ ] Verify images appear in Step 2 review
- [ ] Check OCR confidence scores
- [ ] Verify database stores Base64 strings
- [ ] Load submission from DB → display images
- [ ] Test file validation (size, format)
- [ ] Test duplicate detection
- [ ] Test reviewer view with images

---

## Google Vision API Setup (Optional)

To use real OCR instead of demo:

1. **Setup Google Cloud Project**
   ```bash
   # Install package
   composer require google/cloud-vision
   ```

2. **Configure .env**
   ```env
   GOOGLE_VISION_API_KEY=your_api_key
   GOOGLE_VISION_PROJECT_ID=your_project_id
   ```

3. **Use in code**
   ```php
   $result = OCRService::useGoogleVision($base64Image, 'kwitansi');
   ```

---

## Security Considerations

✅ **Implemented:**
- File type validation (PDF, JPG, JPEG, PNG only)
- File size limits (50 MB max)
- MIME type checking
- Base64 validation
- File hash for integrity

✅ **Production Recommendations:**
- Store images in encrypted database
- Use field-level encryption for Base64
- Implement rate limiting on uploads
- Add virus scanning for uploaded files
- Log all file operations
- Restrict access to Base64 images by role

---

## Performance Notes

### Database Query Optimization
```php
// When loading submission with Base64 (large field)
// Use select() to avoid loading full image in list views
Submission::select(['id', 'submission_id', 'employee_name', '...'])
    ->where('created_by', Auth::id())
    ->get();

// Only load full Base64 when displaying single submission
Submission::where('submission_id', $id)->first();
```

### Client-Side Performance
- Images cached in browser
- Base64 strings included in response (no separate requests)
- Lazy load images only when needed

---

## Next Steps / Future Enhancements

1. **Real OCR Integration**
   - [ ] Google Cloud Vision API
   - [ ] AWS Textract
   - [ ] Tesseract with better training

2. **Image Optimization**
   - [ ] Compress images before Base64 encoding
   - [ ] Support WebP format
   - [ ] Progressive image loading

3. **Data Security**
   - [ ] Field-level encryption
   - [ ] Separate image storage service
   - [ ] Audit trail for access

4. **User Experience**
   - [ ] Drag & drop file uploads
   - [ ] Real-time OCR progress
   - [ ] Manual field editing interface

5. **Advanced Features**
   - [ ] Batch file uploads
   - [ ] Template matching for better OCR
   - [ ] Handwriting recognition
   - [ ] Document comparison

---

## Troubleshooting

### Images Not Displaying
```javascript
// Check if Base64 is valid
if (submission.kwitansi_image.startsWith('data:')) {
  // Valid format
  img.src = submission.kwitansi_image;
} else {
  console.error('Invalid Base64 format');
}
```

### Large File Upload Errors
```php
// Check PHP configuration in php.ini
upload_max_filesize = 50M
post_max_size = 50M
memory_limit = 256M
```

### OCR Confidence Too Low
- Ensure image quality is good (300+ DPI for scans)
- Try different document angles
- Ensure text is not blurry
- Google Vision works best with clean, straight documents

---

## Version Info

- **Created**: 2025-04-15
- **System**: Medical Claim Management
- **Database**: Laravel Eloquent
- **Frontend**: Vanilla JavaScript (No Framework)
- **Image Format**: Base64 (Data URI)
- **OCR Backend**: Configurable (Google Vision / Tesseract / etc)

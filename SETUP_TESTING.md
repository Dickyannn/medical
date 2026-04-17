# 🚀 Quick Setup & Testing Guide

## Installation Steps

### 1. Run Database Migration
```bash
cd c:\laragon\www\medical

# Run the migration to create Base64 image columns
php artisan migrate

# Check if successful:
# ✅ Migration 2025_04_15_add_base64_images_to_submissions created successfully
```

### 2. Clear Cache (if needed)
```bash
php artisan config:cache
php artisan route:cache
php artisan view:cache
```

### 3. Start Development Server
```bash
# If not already running, start Laravel
php artisan serve

# Default: http://127.0.0.1:8000
```

---

## Testing the Implementation

### Test 1: Access Dashboard
1. Go to `http://127.0.0.1:8000/dashboard-ga.html`
2. Login/Initialize as GA role
3. Click "Upload Dokumen" tab

### Test 2: Upload Files
1. Click on "Kwitansi Biaya" upload area
2. Select a PDF, JPG, or PNG file (max 50MB)
3. File info should appear with checkmark
4. Repeat for "Surat Keterangan RS"

### Test 3: Submit & View OCR
1. Fill in employee details (Name, NIK, Department, Relation)
2. Click "Proses OCR →" button
3. Should move to Step 2 showing OCR results with **actual images** displayed

### Test 4: Verify Database Storage
```php
// In php artisan tinker:
>>> $submission = Submission::latest()->first();
>>> strlen($submission->kwitansi_image_base64); // Should be large number (Base64 encoded)
>>> $submission->kwitansi_image_base64; // Should start with "data:image/..."
```

### Test 5: View Uploaded Images
1. In browser DevTools (F12 → Console):
```javascript
// Check if images are stored
fetch('/api/my-submissions')
  .then(r => r.json())
  .then(d => console.log(d.data[0]))

// You should see:
// - id, employee_name, rs, diagnosis, etc.
```

---

## File Upload Scenarios

### ✅ Valid Uploads
- PDF documents
- JPEG/JPG images (300+ DPI recommended for scans)
- PNG images
- Size: up to 50MB
- Formats: .pdf, .jpg, .jpeg, .png

### ❌ Invalid Uploads (Will Show Error)
- File size > 50MB
- Wrong format (.doc, .docx, .bmp, etc)
- Corrupted files
- Executable files

---

## Database Check Commands

### Check if columns exist
```bash
php artisan tinker

>>> Schema::getColumnListing('submissions');
// Should include: kwitansi_image_base64, surat_image_base64, ...
```

### View stored Base64 sample
```php
>>> $s = Submission::latest()->first();
>>> substr($s->kwitansi_image_base64, 0, 50);
// Should show: "data:image/jpeg;base64,/9j/4AAQSkZJRgABA..."
```

### Format check
```php
>>> $s->kwitansi_image_base64;  // Complete Base64 data
>>> json_decode($s->ocr_kwitansi_data)  // OCR extracted data
```

---

## API Endpoint Testing

### Test File Upload via cURL
```bash
curl -X POST http://127.0.0.1:8000/api/submissions \
  -F "employee_name=Budi Santoso" \
  -F "nik_employee=10234" \
  -F "department=Engineering" \
  -F "relation_type=self" \
  -F "kwitansi_file=@C:\path\to\kwitansi.pdf" \
  -F "surat_file=@C:\path\to\surat.pdf"

# Response:
# {
#   "success": true,
#   "submission_id": "S001",
#   "message": "Dokumen berhasil diupload. Proses OCR sedang berjalan..."
# }
```

### Test Get Submission
```bash
curl http://127.0.0.1:8000/api/submissions/S001

# Response shows:
# - submission_id
# - kwitansi_image (Base64 data)
# - surat_image (Base64 data)
# - ocr_kwitansi_data (JSON)
# - ocr_surat_data (JSON)
```

---

## Debugging Issues

### Issue: "File terlalu besar"
**Solution:** 
- Check file size
- Update PHP limits in `php.ini`:
```ini
upload_max_filesize = 50M
post_max_size = 50M
```

### Issue: "Format file tidak didukung"
**Solution:**
- Only use: PDF, JPG, JPEG, PNG
- Check MIME type with:
```php
file_get_contents($file->getRealPath());
mime_content_type($file->getRealPath());
```

### Issue: Database migration fails
**Solution:**
```bash
# Check if migrations already exist
php artisan migrate:status

# If needed, rollback and migrate again
php artisan migrate:rollback
php artisan migrate
```

### Issue: Images not displaying
**Solution:**
```javascript
// In browser console:
// Check if Base64 is valid
const img = document.querySelector('img');
console.log(img.src); // Should start with "data:image/..."

// Test image decoding
const response = await fetch(img.src);
const blob = await response.blob();
console.log(blob.size); // Should show file size
```

---

## Performance Testing

### Monitor Database Size Growth
```php
// Check submission table size
>>> DB::table('information_schema.TABLES')
     ->where('TABLE_SCHEMA', 'database_name')
     ->where('TABLE_NAME', 'submissions')
     ->select('DATA_LENGTH', 'INDEX_LENGTH')
     ->first();

// Base64 increases size by ~33%
// 100 submissions × 2 MB images = 200 MB
// In Base64: 200 MB × 1.33 = 266 MB
```

### Test Upload Speed
```javascript
// JavaScript timing
const start = performance.now();

// Upload file
await fetch('/api/submissions', { ... });

const end = performance.now();
console.log(`Upload took: ${end - start}ms`);
```

---

## Browser Compatibility

✅ **Supported:**
- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

❌ **Base64 Data URI Limits:**
- IE11: Some browsers limit data URI size
- Mobile: Generally supports large Base64 strings in DOM

---

## Rollback/Cleanup

### If you need to undo changes:
```bash
# Rollback last migration
php artisan migrate:rollback --step=1

# This will remove:
# - kwitansi_image_base64
# - surat_image_base64
# - All extracted data columns
```

### To reset database:
```bash
# Warning: This deletes all data!
php artisan migrate:reset
php artisan migrate
```

---

## Next Steps for Production

1. **Set up real OCR service**
   - Configure Google Vision API
   - Or implement Tesseract integration

2. **Optimize storage**
   - Consider separate blob storage (S3, etc)
   - Compress images before encoding

3. **Add security**
   - Implement file scanning (virus check)
   - Add field-level encryption
   - Implement rate limiting

4. **Monitor performance**
   - Set up query monitoring
   - Track upload speeds
   - Monitor database growth

---

## Support Files

- 📄 **OCR_IMPLEMENTATION.md** - Complete technical specification
- 📝 **This guide** - Setup & testing
- 🔧 **Controller** - `app/Http/Controllers/SubmissionController.php`
- 🎨 **Frontend** - `public/js/app.js`, `public/js/dashboard.js`
- 🗄️ **Database** - Migration & Model

---

## Quick Checklist

- [ ] Migration ran successfully
- [ ] Files upload without errors
- [ ] Images display in Step 2 & 3
- [ ] OCR data extracted from images
- [ ] Base64 stored in database
- [ ] API endpoints responding
- [ ] No console errors in browser
- [ ] Date fields populated correctly
- [ ] File validation working
- [ ] Performance acceptable

---

**Last Updated:** 2025-04-15  
**Status:** Ready for Testing ✅

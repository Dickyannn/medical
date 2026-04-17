# Testing Guide - OCR System

## Quick Test Steps

### 1. Verify OCR Service is Running

Open PowerShell and run:
```powershell
curl http://localhost:5000/health
```

✅ **Expected**: JSON response showing `"paddle": true`

❌ **If not running**: 
```bash
cd ocr_service
start_ocr_service.bat
```

### 2. Test the Upload Flow

1. **Open Dashboard GA**:
   ```
   http://127.0.0.1:8000/dashboard-ga.html
   ```

2. **Upload Documents**:
   - Click on "Kwitansi Biaya" area
   - Select a receipt image (JPG/PNG/PDF)
   - Click on "Surat Keterangan RS" area
   - Select a medical letter image

3. **Fill Employee Data**:
   - Nama Karyawan: `Test User`
   - NIK: `12345`
   - Departemen: `Engineering`
   - Hubungan: `Karyawan sendiri`

4. **Click "Upload & Proses OCR"**
   - Wait 5-10 seconds
   - Watch browser console for logs

5. **Review OCR Results (Step 2)**:
   - Check if fields are populated with real data (not hardcoded)
   - Verify images display correctly
   - Edit any incorrect fields
   - Click "Lanjut Konfirmasi"

6. **Confirm Submission (Step 3)**:
   - Review summary
   - Click "Kirim ke Reviewer"

### 3. Check Laravel Logs

Open a new terminal:
```bash
tail -f storage/logs/laravel.log
```

Look for these log entries:
```
[timestamp] local.INFO: Starting OCR processing for submission: S001
[timestamp] local.INFO: Calling PaddleOCR service for text extraction...
[timestamp] local.INFO: PaddleOCR extraction successful {"text_length":450,"confidence":85}
[timestamp] local.INFO: Hospital name extracted: SILOAM KEBON JERUK
[timestamp] local.INFO: Invoice number extracted: KW/2025/04/3143
[timestamp] local.INFO: Total cost extracted: 1036745
[timestamp] local.INFO: OCR processing completed successfully
```

### 4. Check Database

```bash
php artisan tinker
```

Then run:
```php
$submission = App\Models\Submission::latest()->first();
echo "Hospital: " . $submission->hospital_name . "\n";
echo "Invoice: " . $submission->invoice_number . "\n";
echo "Cost: " . $submission->total_cost . "\n";
echo "Diagnosis: " . $submission->diagnosis . "\n";
echo "Doctor: " . $submission->doctor_name . "\n";
echo "Status: " . $submission->status . "\n";
```

✅ **Expected**: Real data from OCR, not hardcoded values

## Common Issues & Solutions

### Issue 1: "OCR service tidak tersedia"
**Cause**: OCR service not running
**Solution**:
```bash
cd ocr_service
start_ocr_service.bat
```

### Issue 2: Empty fields in Step 2
**Cause**: OCR couldn't extract text from images
**Solutions**:
- Use higher quality images (min 300 DPI)
- Ensure text is horizontal (not rotated)
- Check image has good contrast
- Try different image format (PNG instead of JPG)

### Issue 3: Wrong data extracted
**Cause**: Document format not recognized
**Solutions**:
- Check Laravel logs for parsing details
- Manually edit fields in Step 2
- Report document format for pattern improvement

### Issue 4: Dates not extracted
**Cause**: Date format not recognized
**Solutions**:
- Check if date is in supported format:
  - `14 April 2025` ✅
  - `14/04/2025` ✅
  - `14-04-2025` ✅
- Manually enter date in Step 2

### Issue 5: Cost shows 0
**Cause**: Cost format not recognized
**Solutions**:
- Check if cost has "Rp" prefix
- Ensure numbers are readable in image
- Manually enter cost in Step 2

## Browser Console Debugging

Open browser console (F12) and look for:

✅ **Success logs**:
```
✓ renderGAUpload completed
Step 2 - Current Submission: {hospital_name: "...", ...}
Updating submission with: {patient_name: "...", ...}
```

❌ **Error logs**:
```
✗ Error in renderGAUpload: ...
Submit error: ...
```

## Performance Benchmarks

| Operation | Expected Time |
|-----------|---------------|
| Upload files | < 1 second |
| OCR processing (first time) | 5-10 seconds |
| OCR processing (subsequent) | 2-5 seconds |
| Display Step 2 | < 1 second |
| Submit to reviewer | < 1 second |

## Test Checklist

- [ ] OCR service is running on port 5000
- [ ] Can upload Kwitansi image
- [ ] Can upload Surat RS image
- [ ] Can fill employee data
- [ ] OCR extracts hospital name
- [ ] OCR extracts invoice number
- [ ] OCR extracts date
- [ ] OCR extracts cost
- [ ] OCR extracts patient name
- [ ] OCR extracts doctor name
- [ ] OCR extracts diagnosis
- [ ] OCR extracts sick dates
- [ ] Disease category auto-selected
- [ ] Images display correctly in Step 2
- [ ] Can edit OCR results
- [ ] Can submit to reviewer
- [ ] Data saved to database
- [ ] Status changes to `pending_review`

## Success Criteria

✅ **All fields populated with real data** (not hardcoded)
✅ **OCR accuracy > 70%** for good quality images
✅ **Processing time < 10 seconds** per submission
✅ **No errors in Laravel logs**
✅ **No errors in browser console**
✅ **Data correctly saved to database**

## Need Help?

Check these files for detailed information:
- `OCR_IMPROVEMENTS_COMPLETE.md` - Full implementation details
- `ocr_service/README.md` - OCR service documentation
- `storage/logs/laravel.log` - Laravel application logs

## Report Issues

If you find issues, please provide:
1. Screenshot of the error
2. Laravel log entries (last 50 lines)
3. Browser console logs
4. Sample image (if possible)
5. Expected vs actual results

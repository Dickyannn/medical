# Flow Update Complete - Upload → OCR → Review → Save with Duplicate Check

## Summary of Changes

### 1. **Date Fields Changed to Date Pickers** ✅
- **Tanggal** (Kwitansi): Changed to `<input type="date">`
- **Tanggal Mulai** (Surat): Changed to `<input type="date">`
- **Tanggal Selesai** (Surat): Changed to `<input type="date">`

Users can now use native date picker instead of text input.

---

### 2. **New Flow Implementation** ✅

#### OLD FLOW (Before):
```
Step 1: Upload files + employee data
   ↓
Click "Upload & Proses OCR"
   ↓
Save to DB immediately + Run OCR
   ↓
Step 2: Review OCR results (already in DB)
   ↓
Step 3: Confirm and update DB
```

#### NEW FLOW (After):
```
Step 1: Upload files + employee data
   ↓
Click "Upload & Proses OCR"
   ↓
Process OCR ONLY (NO DB save)
   ↓
Step 2: Review & Edit OCR results (in memory only)
   ↓
Click "Lanjut Konfirmasi"
   ↓
Step 3: Preview final data
   ↓
Click "Kirim ke Reviewer"
   ↓
Save to DB + Duplicate Check + Show duplicate percentage
```

---

### 3. **Duplicate Detection Algorithm** ✅

The system now checks for duplicates based on:

| Field | Weight | Criteria |
|-------|--------|----------|
| **NIK** | 20% | Exact match |
| **Nama Pasien** | 15% | >80% similarity |
| **Diagnosa** | 20% | >70% similarity |
| **Nama Dokter** | 15% | >70% similarity |
| **Nama RS** | 10% | >70% similarity |
| **Tanggal Berobat** | 20% | Within 7-14 days |

**Total Score**: 100%

**Duplicate Threshold**: ≥70% similarity = Flagged as duplicate

#### Example Duplicate Detection:
```
Submission A:
- NIK: 10234
- Patient: Budi Santoso
- Diagnosis: Demam Tifoid
- Doctor: dr. Andi Pratama
- Hospital: RS Siloam
- Date: 2026-03-04

Submission B (New):
- NIK: 10234 ✓ (20%)
- Patient: Budi Santoso ✓ (15%)
- Diagnosis: Tifoid ✓ (20%)
- Doctor: dr. Andi ✓ (15%)
- Hospital: RS Siloam ✓ (10%)
- Date: 2026-03-06 ✓ (20%)

Total: 100% → DUPLICATE DETECTED
```

---

### 4. **Files Modified**

#### Frontend (JavaScript):
1. **`public/js/app.js`**:
   - `submitDoc()`: Now calls `/api/ocr-process` instead of `/api/submissions`
   - Stores OCR results in `window.currentSubmission` (memory only)
   - `confirmAndSubmit()`: Now saves to DB with duplicate check
   - Shows duplicate percentage in alert

2. **`public/js/dashboard.js`**:
   - Changed date inputs to `type="date"` in Step 2
   - Updated duplicate warning to show percentage

#### Backend (PHP):
3. **`app/Http/Controllers/SubmissionController.php`**:
   - **NEW**: `processOCROnly()` - Process OCR without DB save
   - **UPDATED**: `store()` - Now accepts JSON data and performs duplicate check
   - **NEW**: `checkDuplicate()` - Duplicate detection algorithm
   - **NEW**: `similarText()` - Text similarity helper
   - **RENAMED**: Old `store()` → `storeOld()` (deprecated)

4. **`routes/web.php`**:
   - Added route: `POST /api/ocr-process`

---

### 5. **API Endpoints**

#### New Endpoint:
```
POST /api/ocr-process
```
**Purpose**: Process OCR without saving to database
**Input**: FormData with files + employee data
**Output**: JSON with OCR results (images, extracted data, confidence)

#### Updated Endpoint:
```
POST /api/submissions
```
**Purpose**: Save submission to DB with duplicate check
**Input**: JSON with all data (from Step 2 review)
**Output**: JSON with submission_id, duplicate info

---

### 6. **User Experience Flow**

#### Step 1: Upload
- User uploads Kwitansi + Surat
- Fills employee data
- Clicks "Upload & Proses OCR"
- **Loading**: "⏳ Memproses OCR..."

#### Step 2: Review (NEW - Data NOT in DB yet)
- OCR results displayed with **date pickers**
- User can edit all fields
- Images shown for reference
- Clicks "Lanjut Konfirmasi"

#### Step 3: Confirm
- Preview all data
- Clicks "Kirim ke Reviewer"
- **Loading**: "⏳ Menyimpan & Cek Duplikasi..."
- **If duplicate detected**: Alert shows percentage
  ```
  ⚠️ Duplikasi terdeteksi (85% kesamaan)!
  
  Pengajuan serupa: S001
  Dokumen tetap disimpan dan akan direview secara manual.
  ```
- **If no duplicate**: Success message
  ```
  ✓ Dokumen berhasil disimpan dan dikirim ke Reviewer!
  ```

---

### 7. **Duplicate Detection Details**

#### Checked Against:
- Recent submissions (last 90 days)
- Same NIK only

#### Matching Criteria:
1. **NIK**: Exact match (20 points)
2. **Patient Name**: >80% similar (15 points)
3. **Diagnosis**: >70% similar (20 points)
4. **Doctor Name**: >70% similar (15 points)
5. **Hospital**: >70% similar (10 points)
6. **Date Range**: 
   - Within 7 days: 20 points
   - Within 14 days: 10 points

#### Status After Detection:
- **If duplicate (≥70%)**: Status = `duplicate_flagged`
- **If not duplicate (<70%)**: Status = `pending_review`

---

### 8. **Database Fields Used**

```php
$table->boolean('is_duplicate')->default(false);
$table->string('similar_submission_id', 20)->nullable();
$table->integer('similarity_score')->nullable(); // Stores percentage
```

---

### 9. **Testing the New Flow**

1. **Upload first submission**:
   - Upload Kwitansi + Surat
   - Review OCR results (edit if needed)
   - Confirm and save
   - Should show: "✓ Dokumen berhasil disimpan"

2. **Upload duplicate submission**:
   - Upload same/similar documents
   - Same NIK, similar diagnosis, similar dates
   - Review OCR results
   - Confirm and save
   - Should show: "⚠️ Duplikasi terdeteksi (XX% kesamaan)!"

3. **Check in Riwayat**:
   - Duplicate submission should have status: `duplicate_flagged`
   - Badge: "⚠ Duplikat Terdeteksi"

---

### 10. **Benefits of New Flow**

✅ **No premature DB saves**: Data only saved after user confirms
✅ **User can edit OCR results**: Before saving to DB
✅ **Duplicate detection**: Prevents duplicate claims
✅ **Better UX**: Date pickers instead of text input
✅ **Transparency**: Shows duplicate percentage to user
✅ **Reviewer workflow**: Flagged duplicates go to manual review

---

### 11. **Next Steps (Optional Enhancements)**

1. **Add duplicate preview**: Show similar submission details in Step 3
2. **Duplicate history**: Show all similar submissions, not just highest match
3. **Adjustable threshold**: Allow admin to configure 70% threshold
4. **Duplicate resolution**: Allow reviewer to merge or reject duplicates
5. **Notification**: Email user when duplicate is detected

---

## Quick Test Commands

```bash
# Clear cache
php artisan cache:clear
php artisan config:clear

# Check routes
php artisan route:list | grep ocr

# Test OCR endpoint
curl -X POST http://127.0.0.1:8000/api/ocr-process \
  -F "employee_name=Test User" \
  -F "nik_employee=12345" \
  -F "department=Engineering" \
  -F "relation_type=self" \
  -F "kwitansi_file=@/path/to/kwitansi.jpg" \
  -F "surat_file=@/path/to/surat.jpg"
```

---

## Summary

✅ Date fields changed to date pickers
✅ New flow: Upload → OCR (no DB) → Review → Save with duplicate check
✅ Duplicate detection algorithm implemented (70% threshold)
✅ Duplicate percentage shown to user
✅ Status automatically set based on duplicate detection
✅ All changes tested and ready to use

**Test it now**: Upload a document, review the OCR results, then upload a similar document to see the duplicate detection in action!

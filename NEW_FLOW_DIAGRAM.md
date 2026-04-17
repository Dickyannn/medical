# New Upload Flow Diagram

## Visual Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         STEP 1: UPLOAD                          │
│                                                                 │
│  📤 Upload Kwitansi (PDF/JPG/PNG)                              │
│  📤 Upload Surat RS (PDF/JPG/PNG)                              │
│                                                                 │
│  👤 Nama Karyawan: [________________]                          │
│  🆔 NIK Karyawan:  [________________]                          │
│  🏢 Departemen:    [▼ Pilih Dept   ]                          │
│  👨‍👩‍👧 Hubungan:      [▼ Pilih Relasi ]                          │
│                                                                 │
│              [Upload & Proses OCR →]                           │
└─────────────────────────────────────────────────────────────────┘
                            ↓
                    ⏳ Processing OCR...
                    (NO DATABASE SAVE)
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    STEP 2: REVIEW & EDIT                        │
│                                                                 │
│  ℹ️ OCR Selesai! Periksa dan edit data jika diperlukan         │
│                                                                 │
│  ┌──────────────────────┐  ┌──────────────────────┐           │
│  │ Hasil OCR - Kwitansi │  │ Hasil OCR - Surat RS │           │
│  │ Confidence: 85%      │  │ Confidence: 71%      │           │
│  ├──────────────────────┤  ├──────────────────────┤           │
│  │ [Image Preview]      │  │ [Image Preview]      │           │
│  │                      │  │                      │           │
│  │ Nama RS:             │  │ Nama Dokter:         │           │
│  │ [Klinik Sehat___]    │  │ [dr. Andi Pratama]   │           │
│  │                      │  │                      │           │
│  │ Nama Pasien:         │  │ Diagnosa:            │           │
│  │ [Budi Santoso___]    │  │ [Influenza (Flu)_]   │           │
│  │                      │  │                      │           │
│  │ No. Kwitansi:        │  │ Tanggal Mulai:       │           │
│  │ [012/KWT/KSS/___]    │  │ [📅 2026-03-04]      │           │
│  │                      │  │                      │           │
│  │ Total Biaya:         │  │ Tanggal Selesai:     │           │
│  │ [Rp 150.000_____]    │  │ [📅 2026-03-06]      │           │
│  │                      │  │                      │           │
│  │ Tanggal:             │  │ Kategori:            │           │
│  │ [📅 2026-03-04]      │  │ [▼ Penyakit Infeksi] │           │
│  └──────────────────────┘  └──────────────────────┘           │
│                                                                 │
│         [← Kembali]  [Lanjut Konfirmasi →]                     │
└─────────────────────────────────────────────────────────────────┘
                            ↓
                    User clicks "Lanjut"
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    STEP 3: KONFIRMASI                           │
│                                                                 │
│  ┌──────────────────────┐  ┌──────────────────────┐           │
│  │ Ringkasan Pengajuan  │  │ Preview Kwitansi     │           │
│  ├──────────────────────┤  ├──────────────────────┤           │
│  │ Nama Karyawan:       │  │ [Image Preview]      │           │
│  │ Ahmad Syafii         │  │                      │           │
│  │                      │  │ ┌──────────────────┐ │           │
│  │ Nama RS:             │  │ │ KLINIK SEHAT     │ │           │
│  │ Klinik Sehat Sentosa │  │ │ Kwitansi Resmi   │ │           │
│  │                      │  │ ├──────────────────┤ │           │
│  │ Diagnosa:            │  │ │ Pasien: Budi     │ │           │
│  │ Influenza (Flu)      │  │ │ Diagnosa: Flu    │ │           │
│  │                      │  │ │ Tanggal: 4 Mar   │ │           │
│  │ Periode Sakit:       │  │ │ Total: Rp 150K   │ │           │
│  │ 4 Mar - 6 Mar 2026   │  │ └──────────────────┘ │           │
│  │                      │  │                      │           │
│  │ Total Biaya:         │  │                      │           │
│  │ Rp 150.000           │  │                      │           │
│  └──────────────────────┘  └──────────────────────┘           │
│                                                                 │
│  ℹ️ Setelah dikirim, pengajuan akan masuk ke antrian Reviewer  │
│                                                                 │
│         [← Kembali]  [Kirim ke Reviewer ✓]                     │
└─────────────────────────────────────────────────────────────────┘
                            ↓
              User clicks "Kirim ke Reviewer"
                            ↓
                ⏳ Menyimpan & Cek Duplikasi...
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DUPLICATE CHECK PROCESS                      │
│                                                                 │
│  🔍 Checking against recent submissions (last 90 days)...      │
│                                                                 │
│  Comparing with existing submissions:                          │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ S001: Budi Santoso - Demam Tifoid - 2 Mar 2026         │  │
│  │ ├─ NIK Match: ✓ (20%)                                  │  │
│  │ ├─ Patient Name: ✓ (15%)                               │  │
│  │ ├─ Diagnosis: ✓ (20%)                                  │  │
│  │ ├─ Doctor: ✓ (15%)                                     │  │
│  │ ├─ Hospital: ✓ (10%)                                   │  │
│  │ └─ Date Range: ✓ (20%)                                 │  │
│  │ TOTAL SIMILARITY: 100% ⚠️ DUPLICATE!                   │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│  S002: Different patient - No match (15%)                      │
│  S003: Different diagnosis - No match (35%)                    │
│                                                                 │
│  Highest Match: S001 (100%)                                    │
│  Threshold: 70%                                                │
│  Result: DUPLICATE DETECTED ⚠️                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
                    SAVE TO DATABASE
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE RECORD                            │
│                                                                 │
│  submission_id: S007                                           │
│  status: duplicate_flagged ⚠️                                  │
│  is_duplicate: true                                            │
│  similar_submission_id: S001                                   │
│  similarity_score: 100                                         │
│  created_at: 2026-04-17 10:30:00                              │
└─────────────────────────────────────────────────────────────────┘
                            ↓
                    SHOW ALERT TO USER
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                         USER ALERT                              │
│                                                                 │
│  ⚠️ Duplikasi terdeteksi (100% kesamaan)!                      │
│                                                                 │
│  Pengajuan serupa: S001                                        │
│  Dokumen tetap disimpan dan akan direview secara manual.       │
│                                                                 │
│                        [OK]                                     │
└─────────────────────────────────────────────────────────────────┘
                            ↓
                  Redirect to Riwayat Page
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                      RIWAYAT PENGAJUAN                          │
│                                                                 │
│  ┌─────┬──────────┬─────────┬──────────┬────────┬─────────┐  │
│  │ ID  │ Karyawan │ RS      │ Diagnosa │ Biaya  │ Status  │  │
│  ├─────┼──────────┼─────────┼──────────┼────────┼─────────┤  │
│  │ S007│ Ahmad S. │ Klinik  │ Flu      │ 150K   │ ⚠ Dup   │  │
│  │ S001│ Budi S.  │ Siloam  │ Tifoid   │ 1.2M   │ ✓ Done  │  │
│  └─────┴──────────┴─────────┴──────────┴────────┴─────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Key Differences from Old Flow

### OLD FLOW:
```
Upload → Save to DB → OCR → Review → Update DB
         ^^^^^^^^
         Premature save!
```

### NEW FLOW:
```
Upload → OCR (memory) → Review → Save to DB + Duplicate Check
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                  Only saves after user confirms!
```

## Duplicate Detection Scoring

```
┌──────────────────────────────────────────────────────────┐
│                  DUPLICATE SCORING                       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  NIK Match (Exact)              ████████████ 20%        │
│  Patient Name (>80% similar)    ███████      15%        │
│  Diagnosis (>70% similar)       ████████████ 20%        │
│  Doctor Name (>70% similar)     ███████      15%        │
│  Hospital (>70% similar)        █████        10%        │
│  Date Range (within 7 days)     ████████████ 20%        │
│                                 ─────────────────        │
│  TOTAL                          ████████████ 100%       │
│                                                          │
│  Threshold: ≥70% = DUPLICATE                            │
└──────────────────────────────────────────────────────────┘
```

## Date Picker Enhancement

### Before:
```
Tanggal: [4 Maret 2026________]  ← Text input (manual typing)
```

### After:
```
Tanggal: [📅 2026-03-04 ▼]  ← Date picker (calendar popup)
```

Benefits:
✅ No typing errors
✅ Consistent format (YYYY-MM-DD)
✅ Easy date selection
✅ Mobile-friendly
✅ Validation built-in

## Testing Scenarios

### Scenario 1: First Upload (No Duplicate)
```
1. Upload Kwitansi + Surat
2. OCR extracts data
3. Review in Step 2
4. Confirm in Step 3
5. Save to DB
6. Result: ✓ "Dokumen berhasil disimpan"
7. Status: pending_review
```

### Scenario 2: Duplicate Upload (High Similarity)
```
1. Upload similar documents
2. OCR extracts data
3. Review in Step 2
4. Confirm in Step 3
5. Save to DB + Duplicate check
6. Result: ⚠️ "Duplikasi terdeteksi (85% kesamaan)!"
7. Status: duplicate_flagged
8. Reviewer will manually verify
```

### Scenario 3: Similar but Not Duplicate
```
1. Upload documents with same NIK
2. But different diagnosis, dates, hospital
3. Similarity score: 45%
4. Result: ✓ "Dokumen berhasil disimpan"
5. Status: pending_review (not flagged)
```

## Summary

✅ **3-Step Flow**: Upload → Review → Confirm
✅ **No Premature Saves**: Data only saved after user confirms
✅ **Date Pickers**: Better UX for date input
✅ **Duplicate Detection**: Automatic checking with 70% threshold
✅ **Transparency**: Shows duplicate percentage to user
✅ **Smart Flagging**: Duplicates go to manual review

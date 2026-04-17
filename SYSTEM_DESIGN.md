# 📋 MEDICAL CLAIM MANAGEMENT SYSTEM — Design Document

**Tanggal**: April 2025  
**Status**: Ready for Development  
**Version**: 1.0

---

## 📌 1. SISTEM OVERVIEW

### Nama Sistem
**Medical Management System** (MedClaim)

### Tujuan
Mengotomasi ekstraksi surat izin dokter dan kwitansi biaya rumah sakit, verifikasi duplikat, dan mengelola workflow approval dari karyawan hingga Finance & Accounting.

### Business Value
- ✅ **Mengurangi waktu proses**: OCR otomatis mengganti entry manual
- ✅ **Deteksi duplikat pintar**: Mencegah klaim ganda berdasarkan nama + tanggal + RS
- ✅ **Workflow terstruktur**: GA upload → Reviewer approve/reject → F&A proses pembayaran
- ✅ **Audit trail transparan**: Setiap perubahan tercatat dengan timestamp
- ✅ **Akses role-based**: Setiap pengguna hanya lihat data yang relevan

---

## 👥 2. USER TYPES (4 Tipe User)

### Type 1: **GA (Karyawan/General Staff)** 
**Peran**: Upload dokumen & beri stempel

| Menu | Akses | Deskripsi |
|------|-------|-----------|
| **Upload Dokumen** | Read + Write | Upload 2 dokumen (kwitansi + surat RS), preview OCR hasil |
| **Riwayat** | Read Only | Lihat status semua pengajuan mereka |
| **Stempel & Kirim** | Read + Write | Print dokumen yang approved, beri stempel fisik, upload ulang |

**Notifikasi**: 
- ✓ Dokumen disetujui reviewer
- ✗ Dokumen ditolak + alasan

---

### Type 2: **HR Officer (Reviewer)**
**Peran**: Review, approve/reject, verifikasi duplikasi

| Menu | Akses | Deskripsi |
|------|-------|-----------|
| **Antrian Review** | Read + Write | Lihat semua pending + flagged duplikasi, approve/reject |
| **Riwayat Review** | Read Only | Laporan dokumen yang sudah di-review |

**Fitur Spesial**:
- 🔍 Sidebar list dokumen pending
- ⚠️ Alert jika ada duplikasi terdeteksi
- 📝 Edit field OCR jika ada kesalahan
- ✓/✗ Approve atau Reject dengan alasan

---

### Type 3: **HR Manager**
**Peran**: Monitor analytics & reporting

| Menu | Akses | Deskripsi |
|------|-------|-----------|
| **Analytics** | Read Only | 5 chart: klaim per dept, trend, diagnosis category, distribution, metrics |
| **Export** | Read Only | Download report Excel per periode |

---

### Type 4: **System Admin (Future)**
**Peran**: Setup & maintenance

| Menu | Akses | Deskripsi |
|------|-------|-----------|
| **User Management** | Read + Write | CRUD user, assign role |
| **Settings** | Read + Write | Konfigurasi OCR provider, duplikasi rules |
| **Logs** | Read Only | Audit trail semua aksi |

---

## 📤 3. UPLOAD REQUIREMENTS

### Format File yang Diterima
- **PDF** (.pdf)
- **Image** (.jpg, .jpeg, .png)

### Ukuran Maksimal
- **50 MB** per file

### Dokumen yang Diperlukan (2 file)

#### File 1: Kwitansi Biaya (Wajib)
Dokumen dari rumah sakit berisi:
- Invoice/receipt number
- Tanggal pembayaran
- Nama pasien
- Nama institusi medis
- Jumlah biaya
- Tanda tangan/cap RS

#### File 2: Surat Keterangan RS (Wajib)
Dokumen resmi dari RS berisi:
- Nama pasien
- Nama dokter yang merawat
- Diagnosis medis
- Tanggal mulai sakit
- Tanggal selesai/pulang
- Nama institusi medis
- Rekomendasi istirahat (jika ada)

### Workflow Upload
```
1. GA masuk ke halaman "Upload Dokumen"
2. Upload file 1 (Kwitansi) — accept via drag-drop atau click
3. Upload file 2 (Surat RS) — accept via drag-drop atau click
4. Isi data manual: nama karyawan, NIK, dept, relasi
5. Click "Proses OCR" → sistem extract text dari kedua dokumen
6. Preview hasil OCR → GA bisa edit jika ada kesalahan
7. Confirm & kirim ke Reviewer
```

---

## 🔄 4. DATA EXTRACTION (9 STEPS)

```
┌─────────────────────────────────────────────────────────┐
│ 1. UPLOAD                                               │
│    GA upload 2 dokumen (kwitansi + surat RS)           │
└────────────────┬────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────┐
│ 2. FILE VALIDATION                                      │
│    Check format, size, readability                     │
└────────────────┬────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────┐
│ 3. OCR (Optical Character Recognition)                 │
│    Extract text dari image/PDF (Google Vision, Tesseract) │
└────────────────┬────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────┐
│ 4. EXTRACT STRUCTURED DATA                             │
│    Parsing text → structured fields (name, date, etc) │
└────────────────┬────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────┐
│ 5. NORMALIZE                                            │
│    Standardize format (date, currency, text case)     │
└────────────────┬────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────┐
│ 6. CLASSIFY                                             │
│    Assign disease category, verify fields              │
└────────────────┬────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────┐
│ 7. DEDUPLICATE (Similarity Check)                       │
│    Compare with existing records (name + date + RS)    │
└────────────────┬────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────┐
│ 8. STORE TO DATABASE                                    │
│    Save extracted data + metadata + OCR confidence    │
└────────────────┬────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────┐
│ 9. ROUTE TO REVIEWER/QUEUE                              │
│    Send to HR Officer untuk approval/rejection        │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 5. EXTRACTED FIELDS (12 Fields)

### Dari Kwitansi (6 fields)
| Field | Tipe | Required | Contoh | OCR Source |
|-------|------|----------|--------|-----------|
| `patient_name` | String | ✓ | Budi Santoso | Nama Pasien di kwitansi |
| `hospital_name` | String | ✓ | RS Siloam Kebon Jeruk | Header/footer RS |
| `invoice_number` | String | ✗ | KW/2025/04/8821 | Receipt number |
| `invoice_date` | Date | ✓ | 2025-04-10 | Tanggal invoice |
| `total_cost` | Decimal | ✓ | 1250000 | Amount Rp/USD |
| `document_hash` | String | Auto | sha256(...) | Auto-generated MD5 hash |

### Dari Surat RS (6 fields)
| Field | Tipe | Required | Contoh | OCR Source |
|-------|------|----------|--------|-----------|
| `doctor_name` | String | ✓ | dr. Wirawan Sp.PD | Nama dokter di surat |
| `diagnosis` | String | ✓ | Demam Tifoid | Diagnosis di surat |
| `disease_category` | String | ✓ | Penyakit Infeksi | Category dropdown |
| `sick_date_from` | Date | ✓ | 2025-04-08 | Tanggal mulai sakit |
| `sick_date_to` | Date | ✓ | 2025-04-12 | Tanggal selesai |
| `ocr_confidence_score` | Integer | Auto | 92 | 0-100 (%) |

### Additional Metadata
| Field | Tipe | Deskripsi |
|-------|------|-----------|
| `duplicate_detected` | Boolean | Flag jika ada kesamaan |
| `similar_submission_ids` | JSON | ID submission yang serupa |
| `similarity_score` | Integer | 0-100 (%) match rate |

---

## 🎨 6. DASHBOARD FEATURES

### Page 1: Upload (GA)
- **Left Panel**: Upload area dengan drag-drop untuk 2 dokumen
- **Right Panel**: Preview hasil OCR dari kedua dokumen
- **Bottom**: Edit fields yang tidak akurat, lalu submit
- **Steps indicator**: Upload → OCR → Confirm

### Page 2: Review (HR Officer)
- **Left Sidebar**: List dokumen pending, flagged duplicate
- **Main Panel**: Document viewer (side-by-side kwitansi + surat)
- **Detail Section**: Extracted fields (editable), OCR confidence
- **Alert**: Duplikasi warning jika ada match
- **Actions**: Approve atau Reject button

### Page 3: F&A Dashboard (Finance)
- **Top Cards**: Total klaim bulan ini, total biaya, rata-rata, pending
- **Main Table**: Tabel semua dokumen approved + distempel
- **Columns**: 
  - ID, Nama Karyawan, Diagnosis, RS, Tanggal, **Total Biaya**, **Kwitansi Link**, Status Bayar
  - ⚠️ **Surat RS TIDAK ditampilkan** untuk F&A (privacy/compliance)
- **Fitur**: Filter per bulan, export Excel

### Page 4: Analytics (HR Manager)
- **Chart 1**: Bar chart klaim per departemen
- **Chart 2**: Line chart trend klaim 3 bulan
- **Chart 3**: Pie chart diagnosis category
- **Chart 4**: Pie chart rejection rate
- **Card 5**: Metric approval rate, avg cost, top diagnosis

---

## 🗄️ 7. DATABASE SCHEMA

```sql
-- ════════════════════════════════════════════
-- TABLE: submissions
-- Catatan: Setiap upload dokumen = 1 record
-- ════════════════════════════════════════════
CREATE TABLE submissions (
  id INT PRIMARY KEY AUTO_INCREMENT,
  
  -- IDENTIFIKASI
  submission_id VARCHAR(20) UNIQUE NOT NULL,  -- S001, S002, dll
  employee_id INT NOT NULL,
  employee_name VARCHAR(255) NOT NULL,
  nik_employee VARCHAR(20) NOT NULL,
  department VARCHAR(100) NOT NULL,
  relation_type ENUM('self', 'spouse', 'child') NOT NULL,  -- Hubungan ke pasien
  
  -- DARI KWITANSI
  patient_name VARCHAR(255) NOT NULL,
  hospital_name VARCHAR(255) NOT NULL,
  invoice_number VARCHAR(100),
  invoice_date DATE NOT NULL,
  total_cost DECIMAL(12, 2) NOT NULL,
  
  -- DARI SURAT RS
  doctor_name VARCHAR(255),
  diagnosis VARCHAR(500) NOT NULL,
  disease_category VARCHAR(100),  -- Penyakit Infeksi, Kronis, dll
  sick_date_from DATE NOT NULL,
  sick_date_to DATE NOT NULL,
  
  -- FILE & METADATA
  kwitansi_file_path VARCHAR(500) NOT NULL,
  surat_file_path VARCHAR(500) NOT NULL,
  kwitansi_hash VARCHAR(64),  -- SHA256 untuk duplikasi detection
  surat_hash VARCHAR(64),
  ocr_confidence_score INT DEFAULT 90,  -- 0-100
  
  -- DUPLIKASI DETECTION
  is_duplicate BOOLEAN DEFAULT FALSE,
  similar_submission_id VARCHAR(20),  -- Reference ke dokumen serupa
  similarity_score INT,  -- 0-100
  
  -- STATUS WORKFLOW
  status ENUM(
    'uploaded',           -- Baru upload
    'ocr_processing',     -- Proses OCR
    'pending_review',     -- Menunggu Reviewer approve/reject
    'duplicate_flagged',  -- Ada duplikasi terdeteksi
    'approved',           -- Reviewer approve
    'rejected',           -- Reviewer reject
    'pending_stamp',      -- Menunggu GA beri stempel
    'stamped',            -- Sudah diberi stempel
    'completed',          -- F&A selesai proses
    'paid'                -- Sudah dibayar
  ) NOT NULL DEFAULT 'uploaded',
  
  rejection_reason TEXT,  -- Alasan jika ditolak
  
  -- STAMP STATUS
  has_stamp BOOLEAN DEFAULT FALSE,
  stamped_file_path VARCHAR(500),
  stamped_at DATETIME,
  
  -- AUDIT
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT NOT NULL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  updated_by INT,
  reviewed_at DATETIME,
  reviewed_by INT,
  
  FOREIGN KEY (employee_id) REFERENCES users(id),
  FOREIGN KEY (created_by) REFERENCES users(id),
  FOREIGN KEY (reviewed_by) REFERENCES users(id),
  
  INDEX idx_status (status),
  INDEX idx_employee (employee_id),
  INDEX idx_date (invoice_date),
  INDEX idx_hospital (hospital_name),
  INDEX idx_duplicate (is_duplicate)
);

-- ════════════════════════════════════════════
-- TABLE: users
-- ════════════════════════════════════════════
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  role ENUM('ga', 'reviewer', 'manager', 'admin') NOT NULL,
  department VARCHAR(100),
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_role (role),
  INDEX idx_email (email)
);

-- ════════════════════════════════════════════
-- TABLE: deduplication_rules
-- Mencatat rules untuk deteksi duplikasi
-- ════════════════════════════════════════════
CREATE TABLE deduplication_rules (
  id INT PRIMARY KEY AUTO_INCREMENT,
  rule_name VARCHAR(100) NOT NULL,
  
  -- Field yang di-compare
  match_patient_name BOOLEAN DEFAULT TRUE,
  match_invoice_date BOOLEAN DEFAULT TRUE,
  match_hospital_name BOOLEAN DEFAULT TRUE,
  match_diagnosis BOOLEAN DEFAULT FALSE,
  
  -- Threshold similarity
  similarity_threshold INT DEFAULT 90,  -- Minimum % untuk dianggap duplikasi
  
  -- Time window (e.g., duplikasi dalam 30 hari terakhir)
  time_window_days INT DEFAULT 30,
  
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ════════════════════════════════════════════
-- TABLE: audit_logs
-- Mencatat setiap perubahan
-- ════════════════════════════════════════════
CREATE TABLE audit_logs (
  id INT PRIMARY KEY AUTO_INCREMENT,
  submission_id VARCHAR(20) NOT NULL,
  action_type ENUM('created', 'updated', 'approved', 'rejected', 'stamped') NOT NULL,
  old_value TEXT,
  new_value TEXT,
  actor_id INT NOT NULL,
  actor_role VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (actor_id) REFERENCES users(id),
  INDEX idx_submission (submission_id),
  INDEX idx_date (created_at)
);

-- ════════════════════════════════════════════
-- TABLE: notifications
-- Notifikasi untuk setiap user
-- ════════════════════════════════════════════
CREATE TABLE notifications (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  submission_id VARCHAR(20),
  notification_type ENUM(
    'approved', 'rejected', 'pending_stamp', 
    'new_pending', 'duplicate_alert'
  ) NOT NULL,
  title VARCHAR(255) NOT NULL,
  message TEXT,
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (user_id) REFERENCES users(id),
  INDEX idx_user (user_id),
  INDEX idx_unread (is_read)
);
```

---

## 🚀 8. WORKFLOW DETAIL (GA → Reviewer → F&A)

### Step 1: GA Upload
```
GA Login
  ↓
GA masuk "Upload Dokumen"
  ↓
Upload Kwitansi + Surat RS
  ↓
Isi data manual (nama, NIK, dept, relasi)
  ↓
System proses OCR → extract 12 fields
  ↓
System cek duplikasi (nama + tanggal + RS)
  ├─ Jika ADA DUPLIKASI:
  │  ├─ Flag submission status = "duplicate_flagged"
  │  ├─ Tampilkan warning di halaman GA
  │  ├─ Tetap lanjut ke Reviewer (untuk verifikasi manual)
  │
  └─ Jika TIDAK ADA:
     ├─ Status = "pending_review"
     
GA preview hasil OCR → bisa edit fields yang salah
  ↓
GA click "Kirim ke Reviewer"
  ↓
Status = "pending_review"
Submission masuk ke antrian Reviewer

┌─ NOTIFIKASI ─────────────────────┐
│ GA mendapat notif:               │
│ "Dokumen berhasil dikirim        │
│  Reviewer akan segera meninjaunya"│
└──────────────────────────────────┘
```

### Step 2: Reviewer Review & Approve/Reject
```
Reviewer Login
  ↓
Reviewer masuk "Antrian Review"
  ↓
Lihat list dokumen pending + flagged duplikasi
  ├─ Jika ada duplikasi flag:
  │  ├─ Tampil alert: "Kesamaan dengan S001 (95% match)"
  │  ├─ Reviewer bisa buka S001 untuk compare
  │  ├─ Reviewer verifikasi manual apakah benar duplikasi
  │
  └─ Normal approval flow:
     
Reviewer klik dokumen dari list
  ↓
Sidebar jadikan active
  ↓
Main panel tampil:
  ├─ Document viewer (kwitansi + surat side-by-side)
  ├─ Extracted fields (editable)
  ├─ OCR confidence score
  ├─ Duplikasi alert (jika ada)
  
Reviewer review data & dokumen
  ↓
OPSI A: APPROVE
  ├─ Click "✓ Setujui"
  ├─ Modal confirm: "Setuju hasil OCR dan duplikasi check?"
  ├─ Status → "approved"
  ├─ Reviewer notif sent
  ├─ GA get notif: "Dokumen disetujui! Silakan print, stempel, upload "
  
  OPSI B: REJECT
  ├─ Click "✗ Tolak"
  ├─ Modal prompt: "Alasan penolakan?"
  ├─ GA input alasan (e.g., "Kwitansi tidak jelas")
  ├─ Status → "rejected"
  ├─ rejection_reason saved
  ├─ GA get notif: "Dokumen ditolak. Alasan: [reason]"
```

### Step 3: GA Stamp & Send to F&A
```
GA dapet notif "Dokumen disetujui"
  ↓
GA masuk "Stempel & Kirim"
  ↓
Lihat list dokumen status "approved" & belum distempel
  ↓
Untuk setiap dokumen:
  ├─ Tampil instruksi: 
  │  1. Download kwitansi
  │  2. Print dokumen
  │  3. Beri stempel fisik perusahaan
  │  4. Scan/foto kwitansi distempel
  │  5. Upload di sini
  │
  ├─ Preview kwitansi (mock)
  │  ├─ Tampil preview dokumen
  │  ├─ Overlay stamp visual ("STEMPEL PERUSAHAAN")
  │
  └─ Upload area
     ├─ GA upload file kwitansi yang sudah distempel
     ├─ Status → "stamped"
     ├─ stamped_file_path saved
     ├─ has_stamp = TRUE
     ├─ Submission ready untuk F&A

F&A automatic dapat notif: "Dokumen siap untuk proses pembayaran"
```

### Step 4: F&A Finance Processing
```
F&A Login
  ↓
F&A masuk "Laporan Klaim"
  ↓
Lihat tabel HANYA dokumen yang:
  ├─ Status = "stamped" atau "completed"
  ├─ has_stamp = TRUE
  
Tabel columns: ID | Nama | Diagnosis | RS | Tgl | Biaya | Kwitansi | Status Bayar
  ├─ Biaya = total_cost dari kwitansi
  ├─ Kwitansi column = link/button "📎 Lihat"
  │  ├─ Click → preview kwitansi distempel
  │  ├─ Preview TIDAK tampil surat RS (F&A tidak perlu lihat)
  ├─ Status Bayar = "Belum Dibayar" / "Sudah Dibayar"

F&A bisa:
  ├─ Filter per bulan
  ├─ Export ke Excel (untuk accounting system)
  ├─ Lihat detail kwitansi distempel saja
  └─ Process pembayaran ke employee account

⚠️ ACCESS RESTRICTION:
  └─ F&A TIDAK bisa lihat "Surat Keterangan RS"
     (Privacy & Compliance - hanya untuk internal HR)
```

---

## 🔒 DUPLICATION DETECTION LOGIC

### Algorithm: 3-Factor Matching

```javascript
function detectDuplication(newSubmission) {
  // FACTOR 1: Nama Pasien (Exact or Fuzzy)
  const nameMatch = similarityScore(
    newSubmission.patient_name,
    existingSubmission.patient_name,
    { algorithm: 'levenshtein', threshold: 90 }
  );
  
  // FACTOR 2: Tanggal Invoice (Window 30 hari)
  const dateDiff = Math.abs(daysBetween(
    newSubmission.invoice_date,
    existingSubmission.invoice_date
  ));
  const dateMatch = dateDiff <= 30 ? 100 : 0;
  
  // FACTOR 3: Nama RS (Fuzzy matching)
  const hospitalMatch = similarityScore(
    newSubmission.hospital_name,
    existingSubmission.hospital_name,
    { algorithm: 'levenshtein', threshold: 85 }
  );
  
  // Combined SCORE (weighted average)
  const finalScore = (
    (nameMatch * 0.4) +      // 40% nama
    (dateMatch * 0.4) +      // 40% tanggal
    (hospitalMatch * 0.2)    // 20% RS
  );
  
  // DECISION
  if (finalScore >= 90) {
    return {
      isDuplicate: true,
      similarityScore: finalScore,
      status: 'duplicate_flagged',
      message: `Match dengan dokumen lain (${finalScore}%)`
    };
  }
  
  return { isDuplicate: false };
}
```

### Example Duplikasi Cases

| Case | Nama | Tgl | RS | Match Score | Flag? |
|------|------|-----|----|----|-------|
| **Exact match** | Budi Santoso | 10 Apr | RS Siloam | 100% | ✅ YES |
| **Typo nama** | Budi Santosa | 10 Apr | RS Siloam | 98% | ✅ YES |
| **Different date** | Budi Santoso | 15 Apr | RS Siloam | 75% | ❌ NO |
| **Different RS** | Budi Santoso | 10 Apr | RSUD Tarakan | 80% | ❌ NO |
| **Similar semua** | Budi Santosa | 12 Apr | RS Siloem | 92% | ✅ YES |

---

## 📊 9. FEATURE MATRIX

| Fitur | GA | Reviewer | F&A Manager | Admin |
|-------|----|----------|------------|-------|
| **Upload Dokumen** | ✓ | - | - | - |
| **OCR Preview & Edit** | ✓ | ✓ | - | - |
| **Review & Approve** | - | ✓ | - | - |
| **Detect Duplikasi** | ✓ (warning) | ✓ (alert+verify) | - | - |
| **Lihat Kwitansi** | ✓ | ✓ | ✓ | ✓ |
| **Lihat Surat RS** | ✓ | ✓ | ✗ | ✓ |
| **Stempel & Kirim** | ✓ | - | - | - |
| **Analytics** | - | - | ✓ | ✓ |
| **Export Excel** | - | - | ✓ | ✓ |
| **Manage Users** | - | - | - | ✓ |

---

## 🤖 10. AI DEVELOPMENT PROMPT (Ready-to-Use)

### Untuk Frontend Developer (Next.js / React)

```
Buatkan UI untuk Medical Claim Management System dengan spec:

FRAMEWORK: React / Next.js + TypeScript
STYLING: Tailwind CSS

PAGES YANG HARUS DIBUAT:
1. Login page (demo roles: GA, Reviewer, F&A)
2. GA Dashboard:
   - Upload dokumen (drag-drop, 2 files required)
   - OCR result preview & edit form
   - Riwayat semua pengajuan (table dengan status badge)
   - Stempel & kirim (approved dokumen → upload kwitansi distempel)

3. Reviewer Dashboard:
   - Sidebar: list dokumen pending + duplicate-flagged (sortable, searchable)
   - Main: dokumen detail, extracted fields (editable), duplicasi alert
   - Actions: Approve / Reject buttons dengan confirmation modal

4. F&A Dashboard:
   - Top metrics: total klaim, total biaya, avg cost, pending
   - Table: all stamped submissions dengan columns (ID, Name, Diagnosis, RS, Date, Cost, Kwitansi link, Pay Status)
   - Filter: by month, department
   - Export: Excel button
   - ⚠️ Surat RS TIDAK ditampilkan

5. Topbar: brand, role badge, nav links (per role), user info, logout btn

COMPONENTS:
- Card (header + body)
- Table dengan hover effect
- Badge (status: pending, approved, rejected, duplicate, stamped)
- Modal (approve confirmation, reject reason)
- Upload area (drag-drop)
- OCR field (label + editable input + confidence meter)
- Sidebar + main content layout (for Reviewer)
- Document preview mockup (kwitansi preview)

COLOR SCHEME:
- Primary: Dark green (#1A4D3E)
- Secondary: Amber (#7A4F00)
- Danger: Dark red (#8B1A1A)
- Info: Dark blue (#1A3A6B)
- Light backgrounds: Off-white (#F5F3EE)

STATE MANAGEMENT: React Context atau Zustand
API INTEGRATION: Axios dengan endpoints (TBD by backend team)

RESPONSIVE: Mobile, Tablet, Desktop
ACCESSIBILITY: WCAG 2.1 Level AA
```

### Untuk Backend Developer (Laravel / Node.js)

```
Buatkan API endpoints untuk Medical Claim Management System:

TECHNOLOGIES:
- Framework: Laravel 11 / Node.js + Express
- Database: MySQL / PostgreSQL
- OCR Service: Google Vision API / Tesseract.js

API ENDPOINTS:

AUTH:
- POST /api/auth/login (email, password) → token, user, role
- POST /api/auth/logout

SUBMISSIONS (GA):
- POST /api/submissions/upload
  ├─ Input: file kwitansi, file surat RS, employee data
  ├─ Process: OCR → extract fields → dupli check → save DB
  ├─ Output: submission_id, extracted_data, duplicate_flag

- GET /api/submissions/history (my submissions)
  ├─ Query params: status, date_from, date_to
  ├─ Output: submissions array

- GET /api/submissions/:id (detail satu submission)

- POST /api/submissions/:id/stamp
  ├─ Input: stamped_file (kwitansi distempel)
  ├─ Output: success, status=stamped

REVIEW (HR Officer):
- GET /api/review/queue (pending + duplicate-flagged)
  ├─ Sort by: status, date
  ├─ Include: duplicate_detected flag, similar_submission_ids

- GET /api/review/:id (detail dokumen)
  ├─ Include: OCR fields, doc preview, duplicasi alert

- POST /api/review/:id/approve
  ├─ Update: status=approved
  ├─ Send notif to GA

- POST /api/review/:id/reject
  ├─ Input: rejection_reason
  ├─ Update: status=rejected, rejection_reason

- GET /api/review/history

REPORTING (F&A):
- GET /api/reports/claims
  ├─ Filter: month, department
  ├─ Return: ONLY stamped submissions
  ├─ Fields: submission_id, patient, diagnosis, rs, date, cost, kwitansi_url

- GET /api/reports/kwitansi/:id (preview kwitansi distempel)
  ├─ Output: file URL / base64

- GET /api/reports/export-excel
  ├─ Output: Excel file

ANALYTICS (HR Manager):
- GET /api/analytics/summary (total, avg, pending metrics)

- GET /api/analytics/by-department (chart data)

- GET /api/analytics/trend (last 3 months)

- GET /api/analytics/diagnosis-category (pie chart)

DEDUPLICATION:
- POST /api/deduplication/check
  ├─ Input: patient_name, invoice_date, hospital_name
  ├─ Output: is_duplicate, similar_ids, similarity_score

- GET /api/deduplication/rules (get rules)

- POST /api/deduplication/rules (admin set rules)

SECURITY:
- Auth: JWT token in Authorization header
- Role-based access control (middleware)
- Field access restrictions (F&A cannot see surat RS)
- All endpoints require authentication
- Audit logs untuk setiap aksi
```

### Untuk Full-Stack Implementation (Parallel Development)

```
TIMELINE REKOMENDASI:

MINGGU 1 (Frontend):
- ✓ Setup React project + structure
- ✓ Create login page + tab navigation shell
- ✓ GA upload page (step 1-3)
- ✓ Reviewer queue + detail panel

MINGGU 2 (Backend):
- ✓ Setup Laravel + DB migrations
- ✓ Auth endpoints (login/logout)
- ✓ OCR integration (Google Vision or Tesseract)
- ✓ Submission upload endpoint
- ✓ Duplication detection logic

MINGGU 3 (Integration + Testing):
- ✓ Connect frontend to backend APIs
- ✓ Reviewer approve/reject flow
- ✓ GA stamp & send flow
- ✓ F&A report page
- ✓ Unit + E2E tests

MINGGU 4 (Deployment + Polish):
- ✓ Production deployment
- ✓ Security audit
- ✓ Performance optimization
- ✓ Documentation
```

---

## 📝 NOTES FOR DEVELOPERS

### Important Implementation Details

1. **File Storage**
   - Store files secara terpisah (tidak di DB)
   - Gunakan private storage path
   - Implement file encryption untuk security
   - Backup strategy needed

2. **OCR Accuracy**
   - Google Vision API: ~95% accuracy untuk receipt/invoice
   - Fallback: Manual review jika confidence < 70%
   - Always allow manual editing by user

3. **Duplikasi Detection**
   - Use string similarity library (Levenshtein distance)
   - Adjust threshold berdasarkan testing
   - False positive mungkin → let Reviewer verify

4. **Performance**
   - Async OCR processing (background job)
   - Cache hasil OCR per dokumen
   - Paginate table di 50 items

5. **Privacy & Compliance**
   - Strict role-based access (F&A tidak bisa lihat surat RS)
   - Detailed audit logs untuk compliance
   - PII handling sesuai GDPR/CCPA

6. **Testing**
   - Unit test: duplication logic
   - E2E test: GA upload → Reviewer approve → F&A report
   - Mock OCR results untuk testing

---

**Siap untuk development! Contact backend team untuk API spec lebih detail.**

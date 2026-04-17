# Keyword-Based OCR Extraction Guide

## Konsep Keyword-Based Extraction

Sistem OCR sekarang menggunakan **keyword-based extraction** - mencari keyword tertentu di dalam teks OCR, lalu mengambil data yang ada di sekitar keyword tersebut.

### Keuntungan:
✅ **Lebih akurat** - tidak perlu menebak posisi data
✅ **Lebih fleksibel** - bisa handle berbagai format dokumen
✅ **Lebih mudah debug** - tahu keyword mana yang berhasil/gagal

---

## KWITANSI (Receipt) - Keywords

### 1. NAMA RS (Hospital Name)
**Keywords yang dicari:**
- `RUMAH SAKIT`
- `RS`
- `KLINIK`
- `CLINIC`
- `HOSPITAL`
- `PUSKESMAS`

**Contoh dokumen:**
```
RUMAH SAKIT SILOAM KEBON JERUK
Jl. Perjuangan No. 8
```
→ Ekstrak: `SILOAM KEBON JERUK`

```
RS PONDOK INDAH
Jakarta Selatan
```
→ Ekstrak: `PONDOK INDAH`

```
KLINIK PRATAMA SEHAT
```
→ Ekstrak: `PRATAMA SEHAT`

**Cara kerja:**
1. Cari keyword (e.g., "RUMAH SAKIT")
2. Ambil teks setelah keyword (3-50 karakter)
3. Stop di newline atau separator (Jl., KWITANSI, NOMOR, dll)

---

### 2. NO KWITANSI (Invoice Number)
**Keywords yang dicari:**
- `NO. KWITANSI`
- `NOMOR KWITANSI`
- `NO.`
- `NOMOR`
- `INVOICE`
- `NO INV`
- `RECEIPT`

**Contoh dokumen:**
```
NO. KWITANSI: KW/2025/04/3143
```
→ Ekstrak: `KW/2025/04/3143`

```
NOMOR: 045/KWT/KRS/III/2026
```
→ Ekstrak: `045/KWT/KRS/III/2026`

```
Invoice No: ABC-12345
```
→ Ekstrak: `ABC-12345`

**Cara kerja:**
1. Cari keyword (e.g., "NO.", "NOMOR")
2. Skip separator (`:`, `.`)
3. Ambil kombinasi huruf/angka/slash (3-50 karakter)

---

### 3. TANGGAL (Date)
**Keywords yang dicari:**
- `TANGGAL`
- `TGL`
- `DATE`
- `TANGGAL KWITANSI`

**Contoh dokumen:**
```
TANGGAL: 14 April 2025
```
→ Ekstrak: `2025-04-14`

```
Tgl: 14/04/2025
```
→ Ekstrak: `2025-04-14`

```
Date: 14 Apr 2025
```
→ Ekstrak: `2025-04-14`

**Format tanggal yang didukung:**
- `14 April 2025` (nama bulan penuh)
- `14 Apr 2025` (nama bulan singkat)
- `14/04/2025` (slash)
- `14-04-2025` (dash)
- `14.04.2025` (dot)

---

### 4. TOTAL BIAYA (Total Cost)
**Keywords yang dicari:**
- `TOTAL BIAYA`
- `TOTAL`
- `JUMLAH`
- `BIAYA`
- `BAYAR`
- `GRAND TOTAL`
- `AMOUNT`

**Contoh dokumen:**
```
TOTAL BIAYA: Rp 1.036.745
```
→ Ekstrak: `1036745`

```
Total: Rp. 1,036,745,-
```
→ Ekstrak: `1036745`

```
Jumlah Bayar: Rp 1036745
```
→ Ekstrak: `1036745`

**Cara kerja:**
1. Cari keyword (e.g., "TOTAL", "JUMLAH")
2. Cari "Rp" setelah keyword
3. Ambil angka (hapus separator `.`, `,`)
4. **Fallback**: Jika tidak ada keyword, ambil angka Rp terbesar di dokumen

---

### 5. NAMA PASIEN (Patient Name)
**Keywords yang dicari:**
- `NAMA PASIEN`
- `PASIEN`
- `PATIENT NAME`
- `PATIENT`
- `ATAS NAMA`

**Contoh dokumen:**
```
NAMA PASIEN: Dimas Dickson
```
→ Ekstrak: `Dimas Dickson`

```
Pasien: John Doe
```
→ Ekstrak: `John Doe`

```
Patient Name: Jane Smith
```
→ Ekstrak: `Jane Smith`

**Cara kerja:**
1. Cari keyword (e.g., "NAMA PASIEN", "PASIEN")
2. Ambil nama (huruf kapital di awal, 2-50 karakter)
3. Stop di separator (NIK, UMUR, TTL, ALAMAT, dll)

---

## SURAT RS (Medical Letter) - Keywords

### 1. NAMA DOKTER (Doctor Name)
**Keywords yang dicari:**
- `DOKTER PEMERIKSA`
- `DOKTER`
- `DOCTOR`
- `DR.`
- `PERIKSA OLEH`
- `DIPERIKSA OLEH`

**Contoh dokumen:**
```
DOKTER: dr. Wirawan Susanto, Sp.PD
```
→ Ekstrak: `Wirawan Susanto`

```
Dokter Pemeriksa: dr. Jane Smith
```
→ Ekstrak: `Jane Smith`

```
Diperiksa oleh: Dr. Ahmad
```
→ Ekstrak: `Ahmad`

**Cara kerja:**
1. Cari keyword (e.g., "DOKTER", "DR.")
2. Ambil nama (bisa dengan/tanpa "dr." prefix)
3. Hapus spesialisasi (Sp.PD, Sp.OG, dll)
4. **Fallback**: Cari "dr." di mana saja dalam teks

---

### 2. DIAGNOSIS (Diagnosis)
**Keywords yang dicari:**
- `DIAGNOSIS`
- `DIAGNOSA`
- `PENYAKIT`
- `KELUHAN`
- `SAKIT`

**Contoh dokumen:**
```
DIAGNOSIS: Demam Tifoid
```
→ Ekstrak: `Demam Tifoid`

```
Diagnosa: Infeksi Saluran Napas Atas
```
→ Ekstrak: `Infeksi Saluran Napas Atas`

```
Keluhan: Gastritis Akut
```
→ Ekstrak: `Gastritis Akut`

**Cara kerja:**
1. Cari keyword (e.g., "DIAGNOSIS", "DIAGNOSA")
2. Ambil teks diagnosis (3-100 karakter)
3. Stop di newline dengan huruf kapital (section baru) atau separator (Dokter, Tanggal, dll)

---

### 3. TANGGAL SAKIT (Sick Leave Dates)
**Keywords yang dicari untuk RANGE:**
- `PERIODE SAKIT`
- `PERIODE ISTIRAHAT`
- `TANGGAL SAKIT`
- `ISTIRAHAT DARI`
- `SAKIT DARI`
- `DARI TANGGAL`

**Keywords untuk MULAI (Start):**
- `MULAI`
- `DARI TANGGAL`
- `TANGGAL MULAI`
- `START`

**Keywords untuk SELESAI (End):**
- `SELESAI`
- `SAMPAI TANGGAL`
- `TANGGAL SELESAI`
- `HINGGA`
- `END`

**Contoh dokumen:**

**Format 1: Range dengan separator**
```
PERIODE SAKIT: 14 April 2025 - 17 April 2025
```
→ Ekstrak: `2025-04-14` sampai `2025-04-17`

```
Istirahat dari: 14/04/2025 s/d 17/04/2025
```
→ Ekstrak: `2025-04-14` sampai `2025-04-17`

**Format 2: Mulai dan Selesai terpisah**
```
TANGGAL MULAI: 14 April 2025
TANGGAL SELESAI: 17 April 2025
```
→ Ekstrak: `2025-04-14` sampai `2025-04-17`

**Format 3: Fallback (ambil 2 tanggal pertama)**
```
Pasien sakit pada 14 April 2025
Diperbolehkan istirahat hingga 17 April 2025
```
→ Ekstrak: `2025-04-14` sampai `2025-04-17`

**Cara kerja:**
1. **Prioritas 1**: Cari keyword range + separator (`-`, `s/d`, `sampai`, `hingga`)
2. **Prioritas 2**: Cari keyword "MULAI" dan "SELESAI" terpisah
3. **Prioritas 3**: Ambil 2 tanggal pertama yang ditemukan di teks

---

## Kategori Penyakit (Disease Category)

Setelah diagnosis diekstrak, sistem akan auto-kategorisasi berdasarkan keyword dalam diagnosis:

### Penyakit Infeksi
**Keywords:** infeksi, demam, flu, covid, tifoid, typhoid, hepatitis, diare, tbc, tuberculosis, batuk, pilek, bronkitis, pneumonia, malaria, istirahat, ispa, saluran napas, tenggorokan, radang, virus, bakteri

**Contoh:**
- "Demam Tifoid" → Penyakit Infeksi
- "Infeksi Saluran Napas" → Penyakit Infeksi
- "Batuk Pilek" → Penyakit Infeksi

### Penyakit Kronis
**Keywords:** hipertensi, diabetes, asma, kanker, jantung, ginjal, gagal ginjal, kolesterol, tekanan darah, darah tinggi, stroke, penyakit jantung, kronis, menahun

**Contoh:**
- "Hipertensi" → Penyakit Kronis
- "Diabetes Mellitus" → Penyakit Kronis

### Kecelakaan
**Keywords:** luka, patah, trauma, cedera, kecelakaan, fraktur, benturan, jatuh, terkilir, memar, lecet, robek, goresan

**Contoh:**
- "Luka Robek" → Kecelakaan
- "Fraktur Tulang" → Kecelakaan

### Pencernaan
**Keywords:** gastritis, maag, lambung, usus, pencernaan, diare, sembelit, konstipasi, mual, muntah, perut

**Contoh:**
- "Gastritis Akut" → Pencernaan
- "Maag Kronis" → Pencernaan

### Lainnya
Jika tidak ada keyword yang cocok → Lainnya

---

## Cara Kerja Sistem

### Flow Extraction:
```
1. Upload Image → Base64
2. Call OCR Service (PaddleOCR)
3. Get Raw Text
4. KEYWORD SEARCH:
   - Cari keyword di raw text
   - Ambil data di sekitar keyword
   - Parse & clean data
5. Save to Database
6. Display to User
```

### Contoh Log:
```
[INFO] Parsing kwitansi text (text_length: 450)
[INFO] Hospital name extracted (keyword: RUMAH SAKIT): SILOAM KEBON JERUK
[INFO] Invoice number extracted (keyword: NO.): KW/2025/04/3143
[INFO] Invoice date extracted (keyword: TANGGAL): 2025-04-14
[INFO] Total cost extracted (keyword: TOTAL BIAYA): 1036745
[INFO] Patient name extracted (keyword: NAMA PASIEN): Dimas Dickson
[INFO] Kwitansi parsing complete

[INFO] Parsing surat text (text_length: 380)
[INFO] Doctor name extracted (keyword: DOKTER): Wirawan Susanto
[INFO] Diagnosis extracted (keyword: DIAGNOSIS): Demam Tifoid
[INFO] Date range extracted (keyword: PERIODE SAKIT): 2025-04-14 to 2025-04-17
[INFO] Disease categorized as: Penyakit Infeksi
[INFO] Surat parsing complete
```

---

## Tips untuk Dokumen yang Baik

### ✅ DO (Lakukan):
1. **Gunakan keyword yang jelas**:
   - "NAMA PASIEN: John Doe" ✅
   - "DIAGNOSIS: Demam Tifoid" ✅
   - "TOTAL BIAYA: Rp 1.000.000" ✅

2. **Format konsisten**:
   - Keyword diikuti `:` atau `.`
   - Data di baris yang sama atau baris berikutnya

3. **Teks jelas dan terbaca**:
   - Font size cukup besar
   - Kontras baik (hitam di putih)
   - Tidak blur atau miring

### ❌ DON'T (Hindari):
1. **Tanpa keyword**:
   - "John Doe" (tanpa label) ❌
   - "1.000.000" (tanpa "Rp" atau "Total") ❌

2. **Format tidak standar**:
   - Data tersebar di berbagai tempat
   - Keyword tidak konsisten

3. **Kualitas gambar buruk**:
   - Resolusi rendah
   - Blur atau miring
   - Kontras rendah

---

## Troubleshooting

### Field kosong setelah OCR?

**Cek log Laravel:**
```bash
tail -f storage/logs/laravel.log
```

**Cari baris seperti:**
```
[INFO] Hospital name extracted (keyword: RUMAH SAKIT): ...
```

**Jika tidak ada log "extracted":**
- Keyword tidak ditemukan di teks OCR
- Cek raw text OCR di log
- Pastikan dokumen punya keyword yang sesuai

**Solusi:**
1. Pastikan dokumen punya keyword (RUMAH SAKIT, DOKTER, DIAGNOSIS, dll)
2. Cek kualitas gambar (min 300 DPI)
3. Edit manual di Step 2 jika perlu

---

## Summary

✅ **Keyword-based extraction** lebih akurat dari regex biasa
✅ **Sistem mencari keyword** lalu ambil data di sekitarnya
✅ **Fallback mechanism** jika keyword tidak ditemukan
✅ **Comprehensive logging** untuk debugging
✅ **User bisa edit** hasil OCR di Step 2

**Status**: ✅ READY TO USE dengan keyword-based extraction!

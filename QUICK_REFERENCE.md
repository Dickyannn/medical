# 🚀 Quick Reference - Keyword OCR

## Keyword yang Harus Ada di Dokumen

### 📄 KWITANSI (Receipt)

| Data | Keyword yang Dicari | Contoh |
|------|---------------------|--------|
| Nama RS | `RUMAH SAKIT`, `RS`, `KLINIK` | **RUMAH SAKIT** Siloam |
| No Kwitansi | `NO`, `NOMOR`, `INVOICE` | **NO**: KW/2025/001 |
| Tanggal | `TANGGAL`, `TGL`, `DATE` | **Tanggal**: 14 Apr 2025 |
| Total Biaya | `TOTAL`, `JUMLAH`, `BAYAR` | **Total**: Rp 1.000.000 |
| Nama Pasien | `PASIEN`, `NAMA PASIEN` | **Pasien**: John Doe |

### 🏥 SURAT RS (Medical Letter)

| Data | Keyword yang Dicari | Contoh |
|------|---------------------|--------|
| Nama Dokter | `DOKTER`, `DR.`, `DOCTOR` | **Dokter**: dr. Ahmad |
| Diagnosis | `DIAGNOSIS`, `DIAGNOSA` | **Diagnosis**: Demam Tifoid |
| Tanggal Mulai | `MULAI`, `PERIODE SAKIT` | **Mulai**: 14 Apr 2025 |
| Tanggal Selesai | `SELESAI`, `SAMPAI` | **Selesai**: 17 Apr 2025 |

---

## ✅ Contoh Dokumen BAIK

### Kwitansi:
```
RUMAH SAKIT SILOAM KEBON JERUK
Jl. Perjuangan No. 8

KWITANSI
NO: KW/2025/04/3143
TANGGAL: 14 April 2025

NAMA PASIEN: Dimas Dickson
TOTAL BIAYA: Rp 1.036.745
```
✅ Semua keyword ada → Ekstraksi 100% berhasil

### Surat RS:
```
SURAT KETERANGAN SAKIT

DOKTER: dr. Wirawan Susanto, Sp.PD
DIAGNOSIS: Demam Tifoid

PERIODE SAKIT: 14 April 2025 - 17 April 2025
```
✅ Semua keyword ada → Ekstraksi 100% berhasil

---

## ❌ Contoh Dokumen BURUK

### Kwitansi (Tanpa Keyword):
```
Siloam Hospital
Invoice ABC-123
14 April 2025
John Doe
1.000.000
```
❌ Tidak ada keyword → Ekstraksi mungkin gagal

**Fix**: Tambahkan keyword
```
RUMAH SAKIT Siloam
NO: ABC-123
TANGGAL: 14 April 2025
PASIEN: John Doe
TOTAL: Rp 1.000.000
```

---

## 🔍 Cara Cek Hasil OCR

### 1. Cek Log Laravel
```bash
tail -f storage/logs/laravel.log
```

**Cari baris ini:**
```
[INFO] Hospital name extracted (keyword: RUMAH SAKIT): Siloam
[INFO] Invoice number extracted (keyword: NO): KW/2025/001
[INFO] Total cost extracted (keyword: TOTAL): 1000000
```

✅ **Jika ada log "extracted"** → Berhasil!
❌ **Jika tidak ada** → Keyword tidak ditemukan

### 2. Cek Step 2 (Review OCR)
- Semua field harus terisi
- Data harus sesuai dokumen
- Edit jika ada yang salah

---

## 🛠️ Troubleshooting Cepat

### Field kosong?
1. **Cek keyword di dokumen** - Pastikan ada keyword yang sesuai
2. **Cek kualitas gambar** - Min 300 DPI, teks jelas
3. **Cek log Laravel** - Lihat keyword mana yang tidak match
4. **Edit manual** - Isi field di Step 2

### Data salah?
1. **Cek raw text OCR** di log - Apakah OCR baca dengan benar?
2. **Edit di Step 2** - User bisa edit semua field
3. **Report format baru** - Jika format dokumen berbeda

---

## 📋 Checklist Dokumen

Sebelum upload, pastikan dokumen punya:

**Kwitansi:**
- [ ] Keyword "RUMAH SAKIT" atau "RS" atau "KLINIK"
- [ ] Keyword "NO" atau "NOMOR" untuk nomor kwitansi
- [ ] Keyword "TANGGAL" atau "TGL" untuk tanggal
- [ ] Keyword "TOTAL" atau "JUMLAH" untuk biaya
- [ ] Keyword "PASIEN" untuk nama pasien
- [ ] Teks jelas dan terbaca (min 300 DPI)

**Surat RS:**
- [ ] Keyword "DOKTER" atau "DR." untuk nama dokter
- [ ] Keyword "DIAGNOSIS" atau "DIAGNOSA" untuk penyakit
- [ ] Keyword "PERIODE" atau "MULAI/SELESAI" untuk tanggal
- [ ] Teks jelas dan terbaca (min 300 DPI)

---

## 🎯 Tips Cepat

1. **Gunakan keyword yang jelas** - "RUMAH SAKIT" lebih baik dari "Hospital"
2. **Format konsisten** - Keyword diikuti `:` atau `.`
3. **Kualitas gambar baik** - Min 300 DPI, tidak blur
4. **Review di Step 2** - Selalu cek hasil OCR sebelum submit
5. **Edit jika perlu** - Semua field bisa diedit manual

---

## 📞 Need Help?

**Cek dokumentasi lengkap:**
- `KEYWORD_EXTRACTION_GUIDE.md` - Daftar lengkap keyword
- `KEYWORD_FIX_COMPLETE.md` - Penjelasan teknis
- `storage/logs/laravel.log` - Log ekstraksi

**Status**: ✅ Keyword-based OCR ready!

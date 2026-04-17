# 🐛 Debugging GA Dashboard

## Langkah-langkah untuk Cek Error:

### 1. Buka Dashboard
- Buka: `http://127.0.0.1:8000/dashboard-ga.html`
- Tekan F12 untuk buka DevTools (Chrome/Firefox)
- Klik tab `Console`

### 2. Cari Error Messages
Di console, cari pesan seperti:
```
=== Initializing GA Dashboard ===
Role set to: ga
initializeApp exists: true
renderGAUpload exists: true
...
```

### 3. Report Error
Jika ada error merah, screenshot atau copy-paste error messages ke sini.

## Checklist Debugging:

- [ ] Apakah header topbar tampil?
- [ ] Apakah ada tombol "Upload Dokumen", "Riwayat", "Stempel & Kirim"?
- [ ] Apakah ada konten di bawah header?
- [ ] Apa error message di console F12?

## Quick Fix Jika Kosong:

Coba buka browser console dan paste:
```javascript
console.log('currentRole:', currentRole);
console.log('window.selectedFiles:', window.selectedFiles);
console.log('renderGAUpload:', typeof renderGAUpload);
```

Report hasilnya.

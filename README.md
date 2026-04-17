# 📋 MedClaim — Medical Management System

**Status**: 🟢 Ready for Development  
**Version**: 1.0.0  
**Last Updated**: April 2025

---

## 🎯 Quick Overview

MedClaim adalah sistem otomasi ekstraksi, verifikasi, dan management klaim medis karyawan. Sistem ini menggunakan OCR untuk ekstraksi data dari kwitansi & surat rumah sakit, deteksi duplikasi pintar, dan workflow approval GA → Reviewer → F&A.

### Key Features
✅ **OCR Otomatis** (PaddleOCR - High Accuracy)  
✅ **Deteksi Duplikasi** (nama + tanggal + RS)  
✅ **Role-Based Access** (4 user types)  
✅ **Document Management** (kwitansi + surat)  
✅ **Workflow Approval** Multi-Step  
✅ **Analytics & Reporting**  
✅ **Stempel Digital/Manual** Flow  
✅ **Base64 Image Storage** (no filesystem)  

---

## 📂 Documentation Files

### 1. **[QUICK_START_OCR.md](./QUICK_START_OCR.md)** ⭐ NEW!
**Start here untuk setup OCR!**
- 5-minute setup guide
- Troubleshooting common issues
- Performance tips
- Daily usage checklist

### 2. **[OCR_INTEGRATION_GUIDE.md](./OCR_INTEGRATION_GUIDE.md)** ⭐ NEW!
**Complete OCR technical documentation:**
- Architecture & data flow
- API endpoints (Python + Laravel)
- Regex patterns for Indonesian medical docs
- Performance optimization
- Production deployment
- Security considerations

### 3. **[SYSTEM_DESIGN.md](./SYSTEM_DESIGN.md)** 
Baca DULU! Dokumen lengkap sistem meliputi:
- System overview & business value
- 4 user types & akses mereka
- Upload requirements & workflow
- 9-step data extraction process
- 12 extracted fields
- Dashboard features per role
- Database schema lengkap
- Duplication detection algorithm
- AI development prompts

👉 **Start here untuk understand keseluruhan sistem!**

---

### 4. **[API_INTEGRATION.md](./API_INTEGRATION.md)** 
Spesifikasi API lengkap untuk backend developer:
- Authentication (JWT token)
- Submission endpoints (GA upload)
- Review endpoints (Reviewer approve/reject)
- Reporting endpoints (F&A export)
- Analytics endpoints (HR Manager)
- Request/response examples
- Error handling
- Rate limiting & pagination

👉 **Gunakan untuk implement backend Laravel API!**

---

### 5. **[DATABASE_SETUP.md](./DATABASE_SETUP.md)**
Setup database dengan instruksi lengkap:
- Database schema (6 tables)
- Laravel migration files (copy-paste ready)
- Seeder dengan sample data
- Setup checklist
- Optimization tips

👉 **Gunakan untuk setup MySQL/PostgreSQL!**

---

### 6. **[public/medical.html](./public/medical.html)** 
Mockup UI lengkap dengan:
- Login page (demo roles: GA, Reviewer, F&A)
- GA Dashboard (upload, history, stempel)
- Reviewer Dashboard (queue, detail, approve/reject)
- F&A Dashboard (report, kwitansi preview)
- Fully styled dengan dark green theme

👉 **Preview di browser! Use sebagai reference untuk React/Next.js UI!**

---

## 🚀 Quick Start

### 1. Setup OCR Service (Required!)

**OCR service must be running for document processing**

```bash
# Terminal 1: Start OCR Service
cd ocr_service
start_ocr_service.bat  # Windows
# OR
./start_ocr_service.sh  # Linux/Mac

# Wait for: "✓ PaddleOCR initialized successfully"
```

**First-time setup**: 5-10 minutes (downloads PaddleOCR models)

📖 **Detailed guide**: See [QUICK_START_OCR.md](./QUICK_START_OCR.md)

### 2. Setup Laravel Backend

```bash
# Terminal 2: Start Laravel
composer install
cp .env.example .env
php artisan key:generate
php artisan migrate:fresh --seed
php artisan serve
```

### 3. Test the System

1. Open browser: `http://127.0.0.1:8000/dashboard-ga.html`
2. Login as GA (no password needed in demo)
3. Upload Kwitansi + Surat RS images
4. Watch OCR extract data automatically! ✨

### Frontend Developer (React/Next.js)
1. Preview mockup di `public/medical.html`
2. Study `SYSTEM_DESIGN.md` section 6 (Dashboard Features)
3. Create React components berdasarkan mockup
4. Connect ke API (lihat `API_INTEGRATION.md`)

### Backend Developer (Laravel)
1. Study workflow di `SYSTEM_DESIGN.md` section 8
2. Setup database: `php artisan migrate:fresh --seed`
3. Implement API endpoints dari `API_INTEGRATION.md`
4. **OCR Integration**: See `OCR_INTEGRATION_GUIDE.md`

---

## 🔄 Workflow Overview

```
GA: Upload dokumen + stempel
   ↓
REVIEWER: Approve (check duplikasi) atau Reject
   ↓
GA: Beri stempel fisik + upload ulang
   ↓
F&A: Lihat tabel & kwitansi distempel (surat RS hidden)
   ↓
Finance: Process pembayaran
```

---

## 👥 User Types

| Role | Main Tasks | Can See |
|------|-----------|---------|
| **GA** | Upload dokumen | Kwitansi + Surat RS |
| **Reviewer** | Approve/Reject | Kwitansi + Surat RS |
| **F&A Manager** | Export report | Kwitansi ONLY (surat RS hidden) |
| **HR Manager** | View analytics | Summary data only |

---

## 🎨 Color Theme
- Primary: Dark Green (#1A4D3E)
- Secondary: Amber (#7A4F00)
- Danger: Dark Red (#8B1A1A)
- Info: Dark Blue (#1A3A6B)

---

## 📞 Need Help?
- **OCR setup issues** → See `QUICK_START_OCR.md`
- **OCR integration** → See `OCR_INTEGRATION_GUIDE.md`
- **System design questions** → See `SYSTEM_DESIGN.md`
- **API implementation** → See `API_INTEGRATION.md`
- **Database setup** → See `DATABASE_SETUP.md`
- **UI reference** → Open `public/medical.html` in browser

## 🔧 Tech Stack

- **Backend**: Laravel 11 (PHP 8.2+)
- **Frontend**: Vanilla JS (can migrate to React/Next.js)
- **Database**: SQLite (dev) / MySQL (production)
- **OCR Engine**: PaddleOCR (Python 3.8+)
- **Image Storage**: Base64 in database
- **API**: RESTful JSON

## 📊 Project Status

- ✅ Database schema & migrations
- ✅ OCR service (PaddleOCR integration)
- ✅ File upload (Base64 storage)
- ✅ OCR extraction & parsing
- ✅ GA Dashboard (upload & history)
- ⏳ Reviewer Dashboard (in progress)
- ⏳ F&A Dashboard (in progress)
- ⏳ Duplicate detection (in progress)
- ⏳ Stempel workflow (in progress)

In order to ensure that the Laravel community is welcoming to all, please review and abide by the [Code of Conduct](https://laravel.com/docs/contributions#code-of-conduct).

## Security Vulnerabilities

If you discover a security vulnerability within Laravel, please send an e-mail to Taylor Otwell via [taylor@laravel.com](mailto:taylor@laravel.com). All security vulnerabilities will be promptly addressed.

## License

The Laravel framework is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).

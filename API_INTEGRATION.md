# 🔌 API INTEGRATION GUIDE — MedClaim System

**Version**: 1.0  
**Last Updated**: April 2025

---

## 📋 Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Authentication](#authentication)
3. [API Endpoints (Detailed)](#api-endpoints-detailed)
4. [Request/Response Examples](#requestresponse-examples)
5. [Error Handling](#error-handling)
6. [Rate Limiting & Pagination](#rate-limiting--pagination)

---

## 🏗️ Architecture Overview

```
┌─────────────────┐
│   FRONTEND      │
│   (React/Next)  │
└────────┬────────┘
         │ HTTP/REST
         ↓
┌─────────────────────────────────────────┐
│   API GATEWAY / LOAD BALANCER           │
│   (nginx / Cloud Load Balancer)         │
└────────┬────────────────────────────────┘
         │
         ↓
┌──────────────────────────────────────────────────────┐
│   BACKEND APPLICATION                               │
│   (Laravel 11 / Node.js + Express)                 │
│                                                     │
│   ├─ Auth Service                                  │
│   ├─ Submission Service (CRUD + OCR)              │
│   ├─ Review Service                               │
│   ├─ Deduplication Service                        │
│   ├─ Notification Service                         │
│   └─ Reporting Service                            │
└────────┬───────────────────────────────┬───────────┘
         │                               │
         ↓                               ↓
┌─────────────────┐          ┌──────────────────────┐
│   MY SQL / PG   │          │ OCR SERVICE          │
│   (Database)    │          │ (Google Vision API)  │
└─────────────────┘          └──────────────────────┘
         
         ↓
┌─────────────────┐
│   FILE STORAGE  │
│   (S3/Local)    │
└─────────────────┘
```

---

## 🔐 Authentication

### Token-Based (JWT)

**Header Format:**
```
Authorization: Bearer <JWT_TOKEN>
```

**JWT Payload:**
```json
{
  "sub": "user_id_12345",
  "name": "Ahmad Syafii",
  "email": "ahmad@company.id",
  "role": "ga",
  "department": "Engineering",
  "iat": 1644312000,
  "exp": 1644398400
}
```

**Token Expiry:**
- Access Token: 1 hour
- Refresh Token: 7 days

---

## 📡 API ENDPOINTS (Detailed)

### Authentication Endpoints

#### 1. Login
```
POST /api/v1/auth/login
Content-Type: application/json

Request:
{
  "email": "ahmad@company.id",
  "password": "password123"
}

Response (200 OK):
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "12345",
      "name": "Ahmad Syafii",
      "email": "ahmad@company.id",
      "role": "ga",
      "department": "Engineering"
    }
  },
  "message": "Login berhasil"
}

Response (401 Unauthorized):
{
  "status": "error",
  "message": "Email atau password salah",
  "code": "AUTH_INVALID_CREDENTIALS"
}
```

#### 2. Logout
```
POST /api/v1/auth/logout
Authorization: Bearer <token>

Response (200 OK):
{
  "status": "success",
  "message": "Logout berhasil"
}
```

#### 3. Refresh Token
```
POST /api/v1/auth/refresh
Authorization: Bearer <refresh_token>

Response (200 OK):
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

---

### Submission Endpoints (GA Upload)

#### 1. Upload Dokumen Baru
```
POST /api/v1/submissions/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

Request:
{
  "kwitansi_file": <FILE>,          // Kwitansi (PDF/JPG/PNG, max 50MB)
  "surat_file": <FILE>,             // Surat RS (PDF/JPG/PNG, max 50MB)
  "employee_name": "Budi Santoso",
  "nik_employee": "10234",
  "department": "Engineering",
  "relation_type": "self"            // self | spouse | child
}

Response (201 Created):
{
  "status": "success",
  "data": {
    "submission_id": "S001",
    "status": "ocr_processing",
    "extracted_data": {
      "patient_name": "Budi Santoso",
      "hospital_name": "RS Siloam Kebon Jeruk",
      "invoice_date": "2025-04-10",
      "total_cost": 1250000,
      "doctor_name": "dr. Wirawan Sp.PD",
      "diagnosis": "Demam Tifoid",
      "disease_category": "Penyakit Infeksi",
      "sick_date_from": "2025-04-08",
      "sick_date_to": "2025-04-12",
      "ocr_confidence_score": 92
    },
    "duplicate_check": {
      "is_duplicate": true,
      "similar_submission_id": "S001",
      "similarity_score": 95,
      "message": "Kesamaan terdeteksi dengan dokumen sebelumnya"
    },
    "created_at": "2025-04-14T10:30:00Z"
  }
}

Response (400 Bad Request):
{
  "status": "error",
  "message": "File tidak valid",
  "errors": {
    "kwitansi_file": "File size melebihi 50MB"
  }
}

Response (409 Conflict):
{
  "status": "error",
  "code": "DUPLICATE_DETECTED",
  "message": "Duplikasi terdeteksi",
  "data": {
    "similar_submission_id": "S001",
    "similarity_score": 95
  }
}
```

#### 2. Get My Submissions (History)
```
GET /api/v1/submissions/my-submissions
Authorization: Bearer <token>
Query Parameters:
  - status=pending_review,approved      (optional, comma-separated)
  - date_from=2025-04-01               (optional)
  - date_to=2025-04-30                 (optional)
  - page=1                             (optional, default:1)
  - per_page=20                        (optional, default:20)

Response (200 OK):
{
  "status": "success",
  "data": {
    "submissions": [
      {
        "id": "S001",
        "patient_name": "Budi Santoso",
        "hospital_name": "RS Siloam",
        "diagnosis": "Demam Tifoid",
        "total_cost": 1250000,
        "status": "duplicate_flagged",
        "invoice_date": "2025-04-10",
        "created_at": "2025-04-14T10:30:00Z",
        "is_duplicate": true,
        "duplicate_message": "Kesamaan dengan S001 (95% match)"
      },
      ...
    ],
    "pagination": {
      "current_page": 1,
      "per_page": 20,
      "total": 45,
      "last_page": 3
    }
  }
}
```

#### 3. Get Submission Detail
```
GET /api/v1/submissions/:submission_id
Authorization: Bearer <token>

Response (200 OK):
{
  "status": "success",
  "data": {
    "submission_id": "S001",
    "employee": {
      "id": "E001",
      "name": "Budi Santoso",
      "email": "budi@company.id",
      "nik": "10234",
      "department": "Engineering"
    },
    "patient_name": "Budi Santoso",
    "hospital_name": "RS Siloam Kebon Jeruk",
    "invoice_number": "KW/2025/04/8821",
    "invoice_date": "2025-04-10",
    "total_cost": 1250000,
    "doctor_name": "dr. Wirawan Sp.PD",
    "diagnosis": "Demam Tifoid",
    "disease_category": "Penyakit Infeksi",
    "sick_date_from": "2025-04-08",
    "sick_date_to": "2025-04-12",
    "ocr_confidence_score": 92,
    "documents": {
      "kwitansi_url": "/storage/submissions/S001/kwitansi.jpg",
      "surat_url": "/storage/submissions/S001/surat.pdf"
    },
    "status": "pending_review",
    "is_duplicate": false,
    "created_at": "2025-04-14T10:30:00Z",
    "created_by": "E001"
  }
}

Response (404 Not Found):
{
  "status": "error",
  "message": "Submission tidak ditemukan"
}
```

#### 4. Update OCR Fields (GA Edit)
```
PUT /api/v1/submissions/:submission_id/update-fields
Authorization: Bearer <token>
Content-Type: application/json

Request:
{
  "patient_name": "Budi Santoso",
  "hospital_name": "RS Siloam Kebon Jeruk",
  "diagnosis": "Demam Tifoid (diperbaharui)",
  "total_cost": 1250000
}

Response (200 OK):
{
  "status": "success",
  "data": {
    "submission_id": "S001",
    "updated_fields": [
      "diagnosis"
    ],
    "updated_at": "2025-04-14T10:45:00Z"
  }
}
```

#### 5. Submit to Reviewer
```
POST /api/v1/submissions/:submission_id/submit
Authorization: Bearer <token>

Response (200 OK):
{
  "status": "success",
  "data": {
    "submission_id": "S001",
    "status": "pending_review",
    "message": "Dokumen berhasil dikirim ke Reviewer",
    "submitted_at": "2025-04-14T10:45:00Z"
  }
}
```

#### 6. Upload Stamped Kwitansi
```
POST /api/v1/submissions/:submission_id/stamp
Authorization: Bearer <token>
Content-Type: multipart/form-data

Request:
{
  "stamped_file": <FILE>  // File kwitansi yang sudah distempel
}

Response (200 OK):
{
  "status": "success",
  "data": {
    "submission_id": "S001",
    "status": "stamped",
    "has_stamp": true,
    "stamped_file_url": "/storage/submissions/S001/kwitansi_stamped.jpg",
    "stamped_at": "2025-04-20T14:30:00Z"
  }
}
```

---

### Review Endpoints (HR Officer)

#### 1. Get Review Queue
```
GET /api/v1/reviews/queue
Authorization: Bearer <token>
Query Parameters:
  - status=pending_review,duplicate_flagged   (optional)
  - sort_by=created_at                        (optional)
  - order=desc                                (optional: asc/desc)
  - page=1                                    (optional)
  - per_page=50                               (optional)

Response (200 OK):
{
  "status": "success",
  "data": {
    "queue": [
      {
        "submission_id": "S001",
        "employee_name": "Budi Santoso",
        "hospital_name": "RS Siloam",
        "diagnosis": "Demam Tifoid",
        "total_cost": 1250000,
        "status": "duplicate_flagged",
        "invoice_date": "2025-04-10",
        "is_duplicate": true,
        "similar_submission_id": "S001",
        "similarity_score": 95,
        "created_at": "2025-04-14T10:30:00Z"
      },
      ...
    ],
    "stats": {
      "total_pending": 12,
      "total_duplicate_flagged": 3
    }
  }
}
```

#### 2. Get Submission for Review
```
GET /api/v1/reviews/:submission_id
Authorization: Bearer <token>

Response (200 OK):
{
  "status": "success",
  "data": {
    "submission_id": "S001",
    "employee": {
      "name": "Budi Santoso",
      "nik": "10234",
      "department": "Engineering"
    },
    "extracted_data": {
      "patient_name": "Budi Santoso",
      "hospital_name": "RS Siloam Kebon Jeruk",
      "invoice_number": "KW/2025/04/8821",
      "invoice_date": "2025-04-10",
      "total_cost": 1250000,
      "doctor_name": "dr. Wirawan Sp.PD",
      "diagnosis": "Demam Tifoid",
      "disease_category": "Penyakit Infeksi",
      "sick_date_from": "2025-04-08",
      "sick_date_to": "2025-04-12",
      "ocr_confidence_score": 92
    },
    "documents": {
      "kwitansi_url": "/storage/submissions/S001/kwitansi.jpg",
      "surat_url": "/storage/submissions/S001/surat.pdf"
    },
    "duplicate_alert": {
      "is_duplicate": true,
      "message": "Kesamaan terdeteksi",
      "similar_submission": {
        "id": "S002",
        "employee": "Budi Santoso",
        "date": "2025-04-10",
        "hospital": "RS Siloam",
        "similarity_score": 95
      }
    },
    "created_at": "2025-04-14T10:30:00Z"
  }
}
```

#### 3. Approve Submission
```
POST /api/v1/reviews/:submission_id/approve
Authorization: Bearer <token>
Content-Type: application/json

Request:
{
  "notes": "Dokumen valid, semua data sesuai"  // Optional
}

Response (200 OK):
{
  "status": "success",
  "data": {
    "submission_id": "S001",
    "status": "approved",
    "reviewed_by": "Ratna Dewi",
    "reviewed_at": "2025-04-14T11:00:00Z",
    "message": "Dokumen disetujui. GA akan menerima notifikasi."
  }
}
```

#### 4. Reject Submission
```
POST /api/v1/reviews/:submission_id/reject
Authorization: Bearer <token>
Content-Type: application/json

Request:
{
  "reason": "Kwitansi tidak terbaca jelas, harap upload ulang dengan resolusi lebih tinggi",
  "notes": "Format huruf terlalu kecil"  // Optional
}

Response (200 OK):
{
  "status": "success",
  "data": {
    "submission_id": "S001",
    "status": "rejected",
    "rejection_reason": "Kwitansi tidak terbaca jelas...",
    "reviewed_by": "Ratna Dewi",
    "reviewed_at": "2025-04-14T11:00:00Z"
  }
}
```

#### 5. Get Review History
```
GET /api/v1/reviews/history
Authorization: Bearer <token>
Query Parameters:
  - status=approved,rejected              (optional)
  - date_from=2025-04-01                  (optional)
  - date_to=2025-04-30                    (optional)
  - page=1                                (optional)
  - per_page=50                           (optional)

Response (200 OK):
{
  "status": "success",
  "data": {
    "history": [
      {
        "submission_id": "S001",
        "employee_name": "Budi Santoso",
        "status": "approved",
        "reviewed_at": "2025-04-14T11:00:00Z",
        "reviewed_by": "Ratna Dewi"
      },
      ...
    ],
    "stats": {
      "total_reviewed": 45,
      "approved_count": 40,
      "rejected_count": 5,
      "approval_rate": 88.89
    }
  }
}
```

---

### Reporting Endpoints (F&A)

#### 1. Get Claims Report
```
GET /api/v1/reports/claims
Authorization: Bearer <token>
Query Parameters:
  - month=2025-04                         (optional: YYYY-MM)
  - department=Engineering                (optional)
  - status=stamped,completed              (optional)
  - page=1                                (optional)
  - per_page=50                           (optional)

Response (200 OK):
{
  "status": "success",
  "data": {
    "claims": [
      {
        "submission_id": "S001",
        "employee_name": "Budi Santoso",
        "diagnosis": "Demam Tifoid",
        "hospital_name": "RS Siloam Kebon Jeruk",
        "invoice_date": "2025-04-10",
        "total_cost": 1250000,
        "kwitansi_url": "/storage/submissions/S001/kwitansi_stamped.jpg",
        "pay_status": "unpaid",
        "stamped_at": "2025-04-20T14:30:00Z"
      },
      ...
    ],
    "summary": {
      "total_claims": 12,
      "total_cost": "Rp 15.250.000",
      "average_cost": "Rp 1.270.833",
      "pending_payment": 12
    }
  }
}
```

#### 2. Get Kwitansi Preview
```
GET /api/v1/reports/submissions/:submission_id/kwitansi
Authorization: Bearer <token>

Response: Binary file (PDF/JPEG/PNG) atau:

{
  "status": "success",
  "data": {
    "url": "/storage/submissions/S001/kwitansi_stamped.jpg",
    "content_type": "image/jpeg"
  }
}
```

#### 3. Export Report to Excel
```
GET /api/v1/reports/export-excel
Authorization: Bearer <token>
Query Parameters:
  - month=2025-04                         (optional)
  - department=Engineering                (optional)

Response: Binary file (Excel .xlsx)
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
```

---

### Analytics Endpoints (HR Manager)

#### 1. Get Summary Metrics
```
GET /api/v1/analytics/summary
Authorization: Bearer <token>

Response (200 OK):
{
  "status": "success",
  "data": {
    "total_submissions": 150,
    "total_cost": 187500000,
    "average_cost": 1250000,
    "approval_rate": 88.67,
    "this_month": 12,
    "pending": 3,
    "completed": 42
  }
}
```

#### 2. Get Claims by Department
```
GET /api/v1/analytics/by-department
Authorization: Bearer <token>

Response (200 OK):
{
  "status": "success",
  "data": [
    {
      "department": "Engineering",
      "count": 45,
      "total_cost": 56250000,
      "average_cost": 1250000
    },
    {
      "department": "Marketing",
      "count": 35,
      "total_cost": 43750000,
      "average_cost": 1250000
    },
    ...
  ]
}
```

#### 3. Get Trend (Last 3 Months)
```
GET /api/v1/analytics/trend
Authorization: Bearer <token>
Query Parameters:
  - months=3                              (optional, default:3)

Response (200 OK):
{
  "status": "success",
  "data": {
    "trend": [
      {
        "month": "2025-02",
        "submissions": 45,
        "total_cost": 56250000,
        "approved": 40,
        "rejected": 5
      },
      {
        "month": "2025-03",
        "submissions": 38,
        "total_cost": 47500000,
        "approved": 34,
        "rejected": 4
      },
      {
        "month": "2025-04",
        "submissions": 12,
        "total_cost": 15000000,
        "approved": 10,
        "rejected": 2
      }
    ]
  }
}
```

---

## 📤 Request/Response Examples

### Example 1: Complete GA Upload Flow

**Request 1: Upload dokumen**
```bash
curl -X POST http://localhost:8000/api/v1/submissions/upload \
  -H "Authorization: Bearer eyJhbGciOi..." \
  -F "kwitansi_file=@/path/to/kwitansi.jpg" \
  -F "surat_file=@/path/to/surat.pdf" \
  -F "employee_name=Budi Santoso" \
  -F "nik_employee=10234" \
  -F "department=Engineering" \
  -F "relation_type=self"
```

**Response 1:**
```json
{
  "status": "success",
  "data": {
    "submission_id": "S001",
    "status": "ocr_processing",
    "extracted_data": {...}
  }
}
```

**Request 2: Get detail** (setelah OCR selesai)
```bash
curl -X GET http://localhost:8000/api/v1/submissions/S001 \
  -H "Authorization: Bearer eyJhbGciOi..."
```

**Request 3: Submit to Reviewer**
```bash
curl -X POST http://localhost:8000/api/v1/submissions/S001/submit \
  -H "Authorization: Bearer eyJhbGciOi..."
```

---

## ❌ Error Handling

### Standard Error Response Format

```json
{
  "status": "error",
  "code": "ERROR_CODE",
  "message": "Error message",
  "errors": {
    "field_name": "Specific error for this field"
  }
}
```

### Common Error Codes

| Code | HTTP | Deskripsi |
|------|------|-----------|
| `INVALID_CREDENTIALS` | 401 | Email/password salah |
| `UNAUTHORIZED` | 401 | Token invalid/expired |
| `FORBIDDEN` | 403 | Role tidak punya akses |
| `NOT_FOUND` | 404 | Resource tidak ditemukan |
| `VALIDATION_ERROR` | 422 | Input validation failed |
| `FILE_NOT_VALID` | 400 | File format/size invalid |
| `DUPLICATE_DETECTED` | 409 | Duplikasi terdeteksi |
| `RATE_LIMIT_EXCEEDED` | 429 | Rate limit tercepat |
| `INTERNAL_SERVER_ERROR` | 500 | Server error |

---

## ⏱️ Rate Limiting & Pagination

### Rate Limits
```
- GA (upload): 5 submissions/hour
- Reviewer (approve): 100 approvals/hour
- General API: 1000 requests/hour per user
```

### Rate Limit Headers
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1644398400
```

### Pagination
```
Default page size: 20
Max page size: 100

Query:
- page=1 (default)
- per_page=20 (default, max 100)

Response:
{
  "pagination": {
    "current_page": 1,
    "per_page": 20,
    "total": 150,
    "last_page": 8
  }
}
```

---

**Done! Share dengan backend team untuk start implementation.**

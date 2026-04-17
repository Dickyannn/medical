# 🗄️ DATABASE SETUP GUIDE — MedClaim System

**Version**: 1.0  
**Database**: MySQL 8.0+ / PostgreSQL 13+  
**Last Updated**: April 2025

---

## 📋 Quick Start

```bash
# Laravel 11 Migration Setup
php artisan migrate

# Seed sample data (optional)
php artisan db:seed --class=SampleDataSeeder

# Check migrations status
php artisan migrate:status
```

---

## 📊 Database Schema (Complete SQL)

### 1. Users Table
```sql
CREATE TABLE `users` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL UNIQUE,
  `email_verified_at` TIMESTAMP NULL,
  `password` VARCHAR(255) NOT NULL,
  `role` ENUM('ga', 'reviewer', 'manager', 'admin') NOT NULL DEFAULT 'ga',
  `department` VARCHAR(100) NULL,
  `nik` VARCHAR(20) NULL,
  `is_active` BOOLEAN DEFAULT TRUE,
  `last_login_at` TIMESTAMP NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  INDEX idx_email (email),
  INDEX idx_role (role),
  INDEX idx_department (department),
  INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 2. Submissions Table (Core)
```sql
CREATE TABLE `submissions` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  
  -- IDENTIFIKASI UNIK
  `submission_id` VARCHAR(20) NOT NULL UNIQUE,
  `employee_id` BIGINT UNSIGNED NOT NULL,
  `employee_name` VARCHAR(255) NOT NULL,
  `nik_employee` VARCHAR(20) NOT NULL,
  `department` VARCHAR(100) NOT NULL,
  `relation_type` ENUM('self', 'spouse', 'child') NOT NULL,
  
  -- DATA DARI KWITANSI
  `patient_name` VARCHAR(255) NOT NULL,
  `hospital_name` VARCHAR(255) NOT NULL,
  `invoice_number` VARCHAR(100) NULL,
  `invoice_date` DATE NOT NULL,
  `total_cost` DECIMAL(15, 2) NOT NULL,
  
  -- DATA DARI SURAT RS
  `doctor_name` VARCHAR(255) NULL,
  `diagnosis` VARCHAR(500) NOT NULL,
  `disease_category` VARCHAR(100) NULL,
  `sick_date_from` DATE NOT NULL,
  `sick_date_to` DATE NOT NULL,
  
  -- FILE PATHS
  `kwitansi_file_path` VARCHAR(500) NOT NULL,
  `surat_file_path` VARCHAR(500) NOT NULL,
  `stamped_file_path` VARCHAR(500) NULL,
  
  -- FILE HASHES (untuk duplikasi detection)
  `kwitansi_hash` VARCHAR(64) NULL,
  `surat_hash` VARCHAR(64) NULL,
  
  -- OCR METADATA
  `ocr_confidence_score` INT NULL DEFAULT 90,
  `ocr_result_json` LONGTEXT NULL,
  
  -- DUPLIKASI DETECTION
  `is_duplicate` BOOLEAN DEFAULT FALSE,
  `similar_submission_id` VARCHAR(20) NULL,
  `similarity_score` INT NULL,
  
  -- STATUS WORKFLOW
  `status` ENUM(
    'uploaded',
    'ocr_processing',
    'pending_review',
    'duplicate_flagged',
    'approved',
    'rejected',
    'pending_stamp',
    'stamped',
    'completed',
    'paid'
  ) NOT NULL DEFAULT 'uploaded',
  
  -- REJECTION INFO
  `rejection_reason` TEXT NULL,
  `rejected_at` TIMESTAMP NULL,
  `rejected_by` BIGINT UNSIGNED NULL,
  
  -- STAMP STATUS
  `has_stamp` BOOLEAN DEFAULT FALSE,
  `stamped_at` TIMESTAMP NULL,
  
  -- APPROVAL INFO
  `approved_at` TIMESTAMP NULL,
  `approved_by` BIGINT UNSIGNED NULL,
  
  -- AUDIT
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `created_by` BIGINT UNSIGNED NOT NULL,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` BIGINT UNSIGNED NULL,
  
  FOREIGN KEY (employee_id) REFERENCES users(id) ON DELETE RESTRICT,
  FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT,
  FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL,
  FOREIGN KEY (rejected_by) REFERENCES users(id) ON DELETE SET NULL,
  
  INDEX idx_submission_id (submission_id),
  INDEX idx_status (status),
  INDEX idx_employee (employee_id),
  INDEX idx_invoice_date (invoice_date),
  INDEX idx_hospital (hospital_name),
  INDEX idx_is_duplicate (is_duplicate),
  INDEX idx_patient_name (patient_name),
  INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 3. Deduplication Rules Table
```sql
CREATE TABLE `deduplication_rules` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `rule_name` VARCHAR(100) NOT NULL,
  
  `match_patient_name` BOOLEAN DEFAULT TRUE,
  `match_invoice_date` BOOLEAN DEFAULT TRUE,
  `match_hospital_name` BOOLEAN DEFAULT TRUE,
  `match_diagnosis` BOOLEAN DEFAULT FALSE,
  
  `similarity_threshold` INT DEFAULT 90,
  `time_window_days` INT DEFAULT 30,
  
  `is_active` BOOLEAN DEFAULT TRUE,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 4. Audit Logs Table
```sql
CREATE TABLE `audit_logs` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `submission_id` VARCHAR(20) NOT NULL,
  `action_type` ENUM(
    'created',
    'updated',
    'approved',
    'rejected',
    'stamped',
    'reviewed',
    'exported'
  ) NOT NULL,
  
  `field_name` VARCHAR(100) NULL,
  `old_value` LONGTEXT NULL,
  `new_value` LONGTEXT NULL,
  
  `actor_id` BIGINT UNSIGNED NOT NULL,
  `actor_role` VARCHAR(50),
  `ip_address` VARCHAR(45) NULL,
  `user_agent` TEXT NULL,
  
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (actor_id) REFERENCES users(id) ON DELETE RESTRICT,
  
  INDEX idx_submission_id (submission_id),
  INDEX idx_action_type (action_type),
  INDEX idx_actor_id (actor_id),
  INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 5. Notifications Table
```sql
CREATE TABLE `notifications` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `user_id` BIGINT UNSIGNED NOT NULL,
  `submission_id` VARCHAR(20) NULL,
  
  `notification_type` ENUM(
    'approved',
    'rejected',
    'pending_stamp',
    'new_pending_review',
    'duplicate_alert',
    'system_alert'
  ) NOT NULL,
  
  `title` VARCHAR(255) NOT NULL,
  `message` LONGTEXT NOT NULL,
  `icon` VARCHAR(100) NULL,
  `link` VARCHAR(500) NULL,
  
  `is_read` BOOLEAN DEFAULT FALSE,
  `read_at` TIMESTAMP NULL,
  
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  
  INDEX idx_user_id (user_id),
  INDEX idx_is_read (is_read),
  INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 6. Payment Status Table (Future)
```sql
CREATE TABLE `payment_status` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `submission_id` VARCHAR(20) NOT NULL UNIQUE,
  
  `payment_status` ENUM('unpaid', 'pending', 'paid', 'rejected') NOT NULL DEFAULT 'unpaid',
  `amount_paid` DECIMAL(15, 2) NULL,
  `paid_at` TIMESTAMP NULL,
  `payment_method` VARCHAR(100) NULL,
  `transaction_id` VARCHAR(100) NULL UNIQUE,
  
  `notes` TEXT NULL,
  
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  INDEX idx_payment_status (payment_status),
  INDEX idx_transaction_id (transaction_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 🔄 Laravel Migration Files

### Migration 1: Create Users Table

**File**: `database/migrations/2024_01_01_create_users_table.php`

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('users', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('email')->unique();
            $table->timestamp('email_verified_at')->nullable();
            $table->string('password');
            $table->enum('role', ['ga', 'reviewer', 'manager', 'admin'])->default('ga');
            $table->string('department')->nullable();
            $table->string('nik', 20)->nullable();
            $table->boolean('is_active')->default(true);
            $table->timestamp('last_login_at')->nullable();
            $table->timestamps();
            
            $table->index('email');
            $table->index('role');
            $table->index('department');
            $table->index('is_active');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('users');
    }
};
```

### Migration 2: Create Submissions Table

**File**: `database/migrations/2024_01_02_create_submissions_table.php`

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('submissions', function (Blueprint $table) {
            $table->id();
            
            // Identification
            $table->string('submission_id', 20)->unique();
            $table->foreignId('employee_id')->constrained('users')->restrictOnDelete();
            $table->string('employee_name');
            $table->string('nik_employee', 20);
            $table->string('department');
            $table->enum('relation_type', ['self', 'spouse', 'child']);
            
            // From Receipt (Kwitansi)
            $table->string('patient_name');
            $table->string('hospital_name');
            $table->string('invoice_number', 100)->nullable();
            $table->date('invoice_date');
            $table->decimal('total_cost', 15, 2);
            
            // From Letter (Surat RS)
            $table->string('doctor_name', 255)->nullable();
            $table->string('diagnosis');
            $table->string('disease_category', 100)->nullable();
            $table->date('sick_date_from');
            $table->date('sick_date_to');
            
            // Files
            $table->string('kwitansi_file_path');
            $table->string('surat_file_path');
            $table->string('stamped_file_path')->nullable();
            
            // File Hashes
            $table->string('kwitansi_hash', 64)->nullable();
            $table->string('surat_hash', 64)->nullable();
            
            // OCR
            $table->integer('ocr_confidence_score')->default(90)->nullable();
            $table->longText('ocr_result_json')->nullable();
            
            // Duplication Detection
            $table->boolean('is_duplicate')->default(false);
            $table->string('similar_submission_id', 20)->nullable();
            $table->integer('similarity_score')->nullable();
            
            // Status
            $table->enum('status', [
                'uploaded',
                'ocr_processing',
                'pending_review',
                'duplicate_flagged',
                'approved',
                'rejected',
                'pending_stamp',
                'stamped',
                'completed',
                'paid'
            ])->default('uploaded');
            
            // Rejection
            $table->text('rejection_reason')->nullable();
            $table->timestamp('rejected_at')->nullable();
            $table->foreignId('rejected_by')->nullable()->constrained('users')->nullOnDelete();
            
            // Stamp
            $table->boolean('has_stamp')->default(false);
            $table->timestamp('stamped_at')->nullable();
            
            // Approval
            $table->timestamp('approved_at')->nullable();
            $table->foreignId('approved_by')->nullable()->constrained('users')->nullOnDelete();
            
            // Audit
            $table->foreignId('created_by')->constrained('users')->restrictOnDelete();
            $table->foreignId('updated_by')->nullable()->constrained('users')->nullOnDelete();
            $table->timestamps();
            
            // Indices
            $table->index('submission_id');
            $table->index('status');
            $table->index('employee_id');
            $table->index('invoice_date');
            $table->index('hospital_name');
            $table->index('is_duplicate');
            $table->index('patient_name');
            $table->index('created_at');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('submissions');
    }
};
```

### Migration 3: Create Other Tables

**File**: `database/migrations/2024_01_03_create_support_tables.php`

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        // Deduplication Rules
        Schema::create('deduplication_rules', function (Blueprint $table) {
            $table->id();
            $table->string('rule_name');
            $table->boolean('match_patient_name')->default(true);
            $table->boolean('match_invoice_date')->default(true);
            $table->boolean('match_hospital_name')->default(true);
            $table->boolean('match_diagnosis')->default(false);
            $table->integer('similarity_threshold')->default(90);
            $table->integer('time_window_days')->default(30);
            $table->boolean('is_active')->default(true);
            $table->timestamps();
            $table->index('is_active');
        });

        // Audit Logs
        Schema::create('audit_logs', function (Blueprint $table) {
            $table->id();
            $table->string('submission_id', 20);
            $table->enum('action_type', [
                'created', 'updated', 'approved', 'rejected', 'stamped', 'reviewed', 'exported'
            ]);
            $table->string('field_name', 100)->nullable();
            $table->longText('old_value')->nullable();
            $table->longText('new_value')->nullable();
            $table->foreignId('actor_id')->constrained('users')->restrictOnDelete();
            $table->string('actor_role', 50)->nullable();
            $table->ipAddress('ip_address')->nullable();
            $table->text('user_agent')->nullable();
            $table->timestamp('created_at')->useCurrent();
            
            $table->index('submission_id');
            $table->index('action_type');
            $table->index('actor_id');
            $table->index('created_at');
        });

        // Notifications
        Schema::create('notifications', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained('users')->cascadeOnDelete();
            $table->string('submission_id', 20)->nullable();
            $table->enum('notification_type', [
                'approved', 'rejected', 'pending_stamp', 'new_pending_review', 'duplicate_alert', 'system_alert'
            ]);
            $table->string('title');
            $table->longText('message');
            $table->string('icon', 100)->nullable();
            $table->string('link', 500)->nullable();
            $table->boolean('is_read')->default(false);
            $table->timestamp('read_at')->nullable();
            $table->timestamps();
            
            $table->index('user_id');
            $table->index('is_read');
            $table->index('created_at');
        });

        // Payment Status
        Schema::create('payment_status', function (Blueprint $table) {
            $table->id();
            $table->string('submission_id', 20)->unique();
            $table->enum('payment_status', ['unpaid', 'pending', 'paid', 'rejected'])->default('unpaid');
            $table->decimal('amount_paid', 15, 2)->nullable();
            $table->timestamp('paid_at')->nullable();
            $table->string('payment_method', 100)->nullable();
            $table->string('transaction_id', 100)->unique()->nullable();
            $table->text('notes')->nullable();
            $table->timestamps();
            
            $table->index('payment_status');
            $table->index('transaction_id');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('payment_status');
        Schema::dropIfExists('notifications');
        Schema::dropIfExists('audit_logs');
        Schema::dropIfExists('deduplication_rules');
    }
};
```

---

## 📝 Seeder (Sample Data)

**File**: `database/seeders/SampleDataSeeder.php`

```php
<?php

namespace Database\Seeders;

use App\Models\User;
use App\Models\Submission;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class SampleDataSeeder extends Seeder
{
    public function run(): void
    {
        // Create Users
        $users = [
            [
                'name' => 'Ahmad Syafii',
                'email' => 'ahmad@company.id',
                'password' => Hash::make('password'),
                'role' => 'ga',
                'department' => 'Engineering',
                'nik' => '10234',
                'is_active' => true,
            ],
            [
                'name' => 'Budi Santoso',
                'email' => 'budi@company.id',
                'password' => Hash::make('password'),
                'role' => 'ga',
                'department' => 'Engineering',
                'nik' => '10235',
                'is_active' => true,
            ],
            [
                'name' => 'Ratna Dewi',
                'email' => 'ratna@company.id',
                'password' => Hash::make('password'),
                'role' => 'reviewer',
                'department' => 'HR',
                'is_active' => true,
            ],
            [
                'name' => 'Bima Prakoso',
                'email' => 'bima@company.id',
                'password' => Hash::make('password'),
                'role' => 'fa',
                'department' => 'Finance',
                'is_active' => true,
            ],
            [
                'name' => 'Admin System',
                'email' => 'admin@company.id',
                'password' => Hash::make('password'),
                'role' => 'admin',
                'department' => 'IT',
                'is_active' => true,
            ],
        ];

        foreach ($users as $user) {
            User::firstOrCreate(['email' => $user['email']], $user);
        }

        // Create Sample Submissions
        $ga_users = User::where('role', 'ga')->get();
        $submissions = [
            [
                'submission_id' => 'S001',
                'employee_id' => $ga_users[0]->id,
                'employee_name' => 'Budi Santoso',
                'nik_employee' => '10234',
                'department' => 'Engineering',
                'relation_type' => 'self',
                'patient_name' => 'Budi Santoso',
                'hospital_name' => 'RS Siloam Kebon Jeruk',
                'invoice_number' => 'KW/2025/04/8821',
                'invoice_date' => '2025-04-10',
                'total_cost' => 1250000,
                'doctor_name' => 'dr. Wirawan Sp.PD',
                'diagnosis' => 'Demam Tifoid',
                'disease_category' => 'Penyakit Infeksi',
                'sick_date_from' => '2025-04-08',
                'sick_date_to' => '2025-04-12',
                'kwitansi_file_path' => 'submissions/S001/kwitansi.jpg',
                'surat_file_path' => 'submissions/S001/surat.pdf',
                'ocr_confidence_score' => 92,
                'status' => 'duplicate_flagged',
                'is_duplicate' => true,
                'created_by' => $ga_users[0]->id,
            ],
            [
                'submission_id' => 'S002',
                'employee_id' => $ga_users[1]->id,
                'employee_name' => 'Siti Rahayu',
                'nik_employee' => '10236',
                'department' => 'Marketing',
                'relation_type' => 'self',
                'patient_name' => 'Siti Rahayu',
                'hospital_name' => 'RSUD Tarakan',
                'invoice_number' => 'KW/2025/04/9912',
                'invoice_date' => '2025-04-08',
                'total_cost' => 480000,
                'doctor_name' => 'dr. Hendra Wijaya',
                'diagnosis' => 'Infeksi Saluran Napas',
                'disease_category' => 'Penyakit Infeksi',
                'sick_date_from' => '2025-04-05',
                'sick_date_to' => '2025-04-10',
                'kwitansi_file_path' => 'submissions/S002/kwitansi.jpg',
                'surat_file_path' => 'submissions/S002/surat.pdf',
                'ocr_confidence_score' => 87,
                'status' => 'approved',
                'has_stamp' => true,
                'stamped_file_path' => 'submissions/S002/kwitansi_stamped.jpg',
                'stamped_at' => now(),
                'approved_by' => User::where('role', 'reviewer')->first()->id,
                'created_by' => $ga_users[1]->id,
            ],
        ];

        foreach ($submissions as $submission) {
            Submission::firstOrCreate(['submission_id' => $submission['submission_id']], $submission);
        }
    }
}
```

---

## ✅ Database Setup Checklist

- [ ] Create `.env` file with database credentials
- [ ] Run `php artisan migrate:fresh --seed` (fresh setup)
- [ ] Verify all tables created: `php artisan migrate:status`
- [ ] Check sample data: `SELECT * FROM submissions;`
- [ ] Create indexes: Done in migration
- [ ] Set up file storage: `php artisan storage:link`
- [ ] Configure OCR service credentials (Google Vision API key)
- [ ] Set up email configuration for notifications
- [ ] Test database connection: `php artisan tinker`

---

## 🔄 Useful Database Commands

```bash
# Show all migrations
php artisan migrate:status

# Rollback last migration
php artisan migrate:rollback

# Rollback all migrations
php artisan migrate:reset

# Fresh migrate + seed
php artisan migrate:fresh --seed

# Create new migration
php artisan make:migration create_table_name

# Create seeder
php artisan make:seeder TableNameSeeder

# Run specific seeder
php artisan db:seed --class=SampleDataSeeder

# Check database
php artisan tinker
>>> User::count()
>>> Submission::where('status', 'pending_review')->get()
```

---

## 📊 Database Optimization

### Add Indices (Already included in migrations)
```sql
-- For frequently searched columns
CREATE INDEX idx_status ON submissions(status);
CREATE INDEX idx_employee_id ON submissions(employee_id);
CREATE INDEX idx_invoice_date ON submissions(invoice_date);
CREATE INDEX idx_hospital_name ON submissions(hospital_name);
CREATE INDEX idx_is_duplicate ON submissions(is_duplicate);
```

### Analyze Query Performance
```sql
-- Show query execution plan
EXPLAIN SELECT * FROM submissions WHERE status = 'pending_review' AND invoice_date > DATE_SUB(NOW(), INTERVAL 30 DAY);
```

---

**Ready for database setup! Contact your DBA for production optimization.**

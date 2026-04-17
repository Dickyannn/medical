<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

class MedicalDataSeeder extends Seeder
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
                'name' => 'Siti Rahayu',
                'email' => 'siti@company.id',
                'password' => Hash::make('password'),
                'role' => 'ga',
                'department' => 'Marketing',
                'nik' => '10236',
                'is_active' => true,
            ],
            [
                'name' => 'Dewi Kurniasih',
                'email' => 'dewi@company.id',
                'password' => Hash::make('password'),
                'role' => 'ga',
                'department' => 'HR',
                'nik' => '10237',
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
                'name' => 'Rini Susanto',
                'email' => 'rini@company.id',
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
                'name' => 'Hendra Wijaya',
                'email' => 'hendra@company.id',
                'password' => Hash::make('password'),
                'role' => 'manager',
                'department' => 'HR',
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

        // Create Deduplication Rules
        DB::table('deduplication_rules')->insert([
            [
                'rule_name' => 'Default Duplication Rule',
                'match_patient_name' => true,
                'match_invoice_date' => true,
                'match_hospital_name' => true,
                'match_diagnosis' => false,
                'similarity_threshold' => 90,
                'time_window_days' => 30,
                'is_active' => true,
                'created_at' => now(),
                'updated_at' => now(),
            ]
        ]);

        // Create Sample Submissions
        $ga_users = User::where('role', 'ga')->get();
        $reviewer = User::where('role', 'reviewer')->first();
        $created_by = $ga_users[0]->id;

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
                'similar_submission_id' => 'S001',
                'similarity_score' => 95,
                'created_by' => $created_by,
                'created_at' => now()->subDays(4),
                'updated_at' => now()->subDays(4),
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
                'stamped_at' => now()->subDays(1),
                'approved_by' => $reviewer->id,
                'approved_at' => now()->subDays(2),
                'created_by' => $created_by,
                'created_at' => now()->subDays(5),
                'updated_at' => now()->subDays(1),
            ],
            [
                'submission_id' => 'S003',
                'employee_id' => $ga_users[2]->id,
                'employee_name' => 'Dewi Kurniasih',
                'nik_employee' => '10237',
                'department' => 'HR',
                'relation_type' => 'self',
                'patient_name' => 'Dewi Kurniasih',
                'hospital_name' => 'RS Pondok Indah',
                'invoice_number' => 'KW/2025/04/7712',
                'invoice_date' => '2025-04-07',
                'total_cost' => 730000,
                'doctor_name' => 'dr. Bambang Sutrisno Sp.A',
                'diagnosis' => 'Gastritis Akut',
                'disease_category' => 'Penyakit Pencernaan',
                'sick_date_from' => '2025-04-06',
                'sick_date_to' => '2025-04-09',
                'kwitansi_file_path' => 'submissions/S003/kwitansi.jpg',
                'surat_file_path' => 'submissions/S003/surat.pdf',
                'ocr_confidence_score' => 95,
                'status' => 'pending_review',
                'created_by' => $created_by,
                'created_at' => now()->subDays(6),
                'updated_at' => now()->subDays(6),
            ],
            [
                'submission_id' => 'S004',
                'employee_id' => $ga_users[3]->id,
                'employee_name' => 'Hendra Wijaya',
                'nik_employee' => '10238',
                'department' => 'Operations',
                'relation_type' => 'self',
                'patient_name' => 'Hendra Wijaya',
                'hospital_name' => 'Klinik Pratama Sehat',
                'invoice_number' => 'KW/2025/04/5534',
                'invoice_date' => '2025-04-05',
                'total_cost' => 215000,
                'doctor_name' => 'dr. Siti Nurhaliza',
                'diagnosis' => 'Hipertensi',
                'disease_category' => 'Penyakit Kronis',
                'sick_date_from' => '2025-04-04',
                'sick_date_to' => '2025-04-06',
                'kwitansi_file_path' => 'submissions/S004/kwitansi.jpg',
                'surat_file_path' => 'submissions/S004/surat.pdf',
                'ocr_confidence_score' => 78,
                'status' => 'rejected',
                'rejection_reason' => 'Kwitansi tidak terbaca jelas, harap upload ulang dengan resolusi lebih tinggi',
                'rejected_by' => $reviewer->id,
                'rejected_at' => now()->subDays(3),
                'created_by' => $created_by,
                'created_at' => now()->subDays(7),
                'updated_at' => now()->subDays(3),
            ],
            [
                'submission_id' => 'S005',
                'employee_id' => $ga_users[0]->id,
                'employee_name' => 'Rina Marlina',
                'nik_employee' => '10239',
                'department' => 'Finance',
                'relation_type' => 'self',
                'patient_name' => 'Rina Marlina',
                'hospital_name' => 'RS Medistra',
                'invoice_number' => 'KW/2025/04/4451',
                'invoice_date' => '2025-04-03',
                'total_cost' => 620000,
                'doctor_name' => 'dr. Eka Putri Sukma',
                'diagnosis' => 'Migrain Kronis',
                'disease_category' => 'Penyakit Saraf',
                'sick_date_from' => '2025-04-01',
                'sick_date_to' => '2025-04-05',
                'kwitansi_file_path' => 'submissions/S005/kwitansi.jpg',
                'surat_file_path' => 'submissions/S005/surat.pdf',
                'ocr_confidence_score' => 96,
                'status' => 'completed',
                'has_stamp' => true,
                'stamped_file_path' => 'submissions/S005/kwitansi_stamped.jpg',
                'stamped_at' => now()->subDays(8),
                'approved_by' => $reviewer->id,
                'approved_at' => now()->subDays(9),
                'created_by' => $created_by,
                'created_at' => now()->subDays(10),
                'updated_at' => now()->subDays(8),
            ],
            [
                'submission_id' => 'S006',
                'employee_id' => $ga_users[1]->id,
                'employee_name' => 'Doni Firmansyah',
                'nik_employee' => '10240',
                'department' => 'Engineering',
                'relation_type' => 'self',
                'patient_name' => 'Doni Firmansyah',
                'hospital_name' => 'RSCM',
                'invoice_number' => 'KW/2025/04/3362',
                'invoice_date' => '2025-04-01',
                'total_cost' => 890000,
                'doctor_name' => 'dr. Rizky Rahman Sp.OT',
                'diagnosis' => 'Vertigo',
                'disease_category' => 'Penyakit Saraf',
                'sick_date_from' => '2025-03-31',
                'sick_date_to' => '2025-04-03',
                'kwitansi_file_path' => 'submissions/S006/kwitansi.jpg',
                'surat_file_path' => 'submissions/S006/surat.pdf',
                'ocr_confidence_score' => 81,
                'status' => 'pending_review',
                'created_by' => $created_by,
                'created_at' => now()->subDays(12),
                'updated_at' => now()->subDays(12),
            ],
        ];

        foreach ($submissions as $submission) {
            DB::table('submissions')->insert($submission);
        }

        // Create Payment Status records
        $payment_statuses = [
            [
                'submission_id' => 'S002',
                'payment_status' => 'unpaid',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'submission_id' => 'S005',
                'payment_status' => 'unpaid',
                'created_at' => now(),
                'updated_at' => now(),
            ],
        ];

        foreach ($payment_statuses as $payment) {
            DB::table('payment_status')->insert($payment);
        }

        // Create Sample Notifications
        $notifications = [
            [
                'user_id' => $ga_users[1]->id,
                'submission_id' => 'S002',
                'notification_type' => 'approved',
                'title' => 'Dokumen Disetujui',
                'message' => 'Dokumen klaim medis Anda telah disetujui oleh Reviewer. Silakan cetak, beri stempel, dan upload kembali.',
                'icon' => '✓',
                'link' => '/ga/stamp/S002',
                'is_read' => true,
                'read_at' => now()->subDays(2),
                'created_at' => now()->subDays(2),
                'updated_at' => now()->subDays(2),
            ],
            [
                'user_id' => $ga_users[3]->id,
                'submission_id' => 'S004',
                'notification_type' => 'rejected',
                'title' => 'Dokumen Ditolak',
                'message' => 'Dokumen klaim medis Anda telah ditolak. Alasan: Kwitansi tidak terbaca jelas, harap upload ulang.',
                'icon' => '✗',
                'link' => '/ga/history',
                'is_read' => true,
                'read_at' => now()->subDays(3),
                'created_at' => now()->subDays(3),
                'updated_at' => now()->subDays(3),
            ],
        ];

        foreach ($notifications as $notification) {
            DB::table('notifications')->insert($notification);
        }
    }
}

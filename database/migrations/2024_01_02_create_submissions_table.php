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

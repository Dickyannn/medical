<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Submission extends Model
{
    use HasFactory;

    protected $fillable = [
        'submission_id',
        'employee_id',
        'employee_name',
        'nik_employee',
        'department',
        'relation_type',
        'patient_name',
        'hospital_name',
        'invoice_number',
        'invoice_date',
        'total_cost',
        'doctor_name',
        'diagnosis',
        'disease_category',
        'sick_date_from',
        'sick_date_to',
        'kwitansi_file_path',
        'surat_file_path',
        'stamped_file_path',
        'kwitansi_hash',
        'surat_hash',
        'kwitansi_image_base64',
        'surat_image_base64',
        'kwitansi_original_filename',
        'surat_original_filename',
        'ocr_confidence_score',
        'ocr_result_json',
        'ocr_kwitansi_data',
        'ocr_surat_data',
        'is_duplicate',
        'similar_submission_id',
        'similarity_score',
        'status',
        'rejection_reason',
        'rejected_at',
        'rejected_by',
        'has_stamp',
        'stamped_at',
        'approved_at',
        'approved_by',
        'created_by',
        'updated_by',
    ];

    protected $casts = [
        'invoice_date' => 'date',
        'sick_date_from' => 'date',
        'sick_date_to' => 'date',
        'total_cost' => 'decimal:2',
        'is_duplicate' => 'boolean',
        'has_stamp' => 'boolean',
        'rejected_at' => 'datetime',
        'stamped_at' => 'datetime',
        'approved_at' => 'datetime',
    ];

    public function employee(): BelongsTo
    {
        return $this->belongsTo(User::class, 'employee_id');
    }

    public function reviewedBy(): BelongsTo
    {
        return $this->belongsTo(User::class, 'approved_by');
    }

    public function rejectedBy(): BelongsTo
    {
        return $this->belongsTo(User::class, 'rejected_by');
    }

    public function createdByUser(): BelongsTo
    {
        return $this->belongsTo(User::class, 'created_by');
    }
}

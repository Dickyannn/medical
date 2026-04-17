<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('submissions', function (Blueprint $table) {
            // Add Base64 image columns for Kwitansi and Surat RS
            $table->longText('kwitansi_image_base64')->nullable()->after('kwitansi_file_path');
            $table->longText('surat_image_base64')->nullable()->after('surat_file_path');
            
            // Add filename storage
            $table->string('kwitansi_original_filename')->nullable()->after('kwitansi_image_base64');
            $table->string('surat_original_filename')->nullable()->after('surat_image_base64');
            
            // Add OCR extracted data (JSON)
            $table->longText('ocr_kwitansi_data')->nullable()->after('ocr_result_json');
            $table->longText('ocr_surat_data')->nullable()->after('ocr_kwitansi_data');
        });
    }

    public function down(): void
    {
        Schema::table('submissions', function (Blueprint $table) {
            $table->dropColumn([
                'kwitansi_image_base64',
                'surat_image_base64',
                'kwitansi_original_filename',
                'surat_original_filename',
                'ocr_kwitansi_data',
                'ocr_surat_data',
            ]);
        });
    }
};

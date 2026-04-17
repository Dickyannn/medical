<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('submissions', function (Blueprint $table) {
            // Make file paths nullable since we're using Base64 storage
            $table->string('kwitansi_file_path')->nullable()->change();
            $table->string('surat_file_path')->nullable()->change();
        });
    }

    public function down(): void
    {
        Schema::table('submissions', function (Blueprint $table) {
            $table->string('kwitansi_file_path')->nullable(false)->change();
            $table->string('surat_file_path')->nullable(false)->change();
        });
    }
};

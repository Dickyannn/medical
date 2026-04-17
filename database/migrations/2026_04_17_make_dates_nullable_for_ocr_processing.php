<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('submissions', function (Blueprint $table) {
            // Make date fields nullable - they will be populated by OCR extraction
            $table->date('invoice_date')->nullable()->change();
            $table->date('sick_date_from')->nullable()->change();
            $table->date('sick_date_to')->nullable()->change();
        });
    }

    public function down(): void
    {
        Schema::table('submissions', function (Blueprint $table) {
            // Revert changes
            $table->date('invoice_date')->nullable(false)->change();
            $table->date('sick_date_from')->nullable(false)->change();
            $table->date('sick_date_to')->nullable(false)->change();
        });
    }
};

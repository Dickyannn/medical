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

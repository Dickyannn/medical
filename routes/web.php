<?php

use App\Http\Controllers\SubmissionController;
use Illuminate\Support\Facades\Route;

// Redirect / to login
Route::get('/', function () {
    return redirect('/login.html');
});

// Serve login page
Route::get('/login.html', function () {
    return response(file_get_contents(public_path('login.html')), 200, [
        'Content-Type' => 'text/html; charset=UTF-8',
    ]);
});

// Dashboard fallback (redirects to appropriate dashboard based on role)
Route::get('/dashboard.html', function () {
    return response(file_get_contents(public_path('dashboard.html')), 200, [
        'Content-Type' => 'text/html; charset=UTF-8',
    ]);
});

// Serve dashboard pages per role
Route::get('/dashboard-ga.html', function () {
    return response(file_get_contents(public_path('dashboard-ga.html')), 200, [
        'Content-Type' => 'text/html; charset=UTF-8',
    ]);
});

Route::get('/dashboard-reviewer.html', function () {
    return response(file_get_contents(public_path('dashboard-reviewer.html')), 200, [
        'Content-Type' => 'text/html; charset=UTF-8',
    ]);
});

Route::get('/dashboard-fa.html', function () {
    return response(file_get_contents(public_path('dashboard-fa.html')), 200, [
        'Content-Type' => 'text/html; charset=UTF-8',
    ]);
});

// ════════════════════════════════════════════════
// API Routes for Medical Claims Submission
// ════════════════════════════════════════════════

Route::prefix('api')->middleware(['web'])->group(function () {
    // Test endpoint
    Route::get('/test', function () {
        return response()->json(['status' => 'ok', 'message' => 'API is working']);
    });
    
    // OCR processing without DB save (Step 1 → Step 2)
    Route::post('/ocr-process', [SubmissionController::class, 'processOCROnly']);
    
    // Submission endpoints - These can be public or protected based on your auth setup
    Route::post('/submissions', [SubmissionController::class, 'store']);
    Route::get('/submissions/{submissionId}', [SubmissionController::class, 'show']);
    Route::put('/submissions/{submissionId}', [SubmissionController::class, 'update']);
    Route::get('/my-submissions', [SubmissionController::class, 'listMySubmissions']);
    Route::get('/pending-reviews', [SubmissionController::class, 'listPendingReviews']);
});


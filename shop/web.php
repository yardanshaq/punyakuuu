<?php
use App\Http\Controllers\HomeController;
use App\Http\Controllers\ReportController;

Route::get('/', [HomeController::class, 'index']);
Route::get('/sales-report', [ReportController::class, 'salesReport'])->name('sales.report');
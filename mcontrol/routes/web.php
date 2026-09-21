<?php

use App\Http\Controllers\DashboardController;
use App\Http\Controllers\EventController;
use App\Http\Controllers\CalendarController;
use App\Http\Controllers\AnalysisController;
use App\Http\Controllers\EducationController;
use App\Http\Controllers\PrivacyController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes - M-Control Laravel
|--------------------------------------------------------------------------
*/

// Panel Principal (Dashboard)
Route::get('/', [DashboardController::class, 'index'])->name('dashboard');

// Registro y Gestión de Eventos
Route::get('/events/create', [EventController::class, 'create'])->name('events.create');
Route::post('/events', [EventController::class, 'store'])->name('events.store');
Route::delete('/events/{event}', [EventController::class, 'destroy'])->name('events.destroy');
Route::post('/events/evaluate-live', [EventController::class, 'evaluateLive'])->name('events.evaluateLive');

// Calendario Semáforo
Route::get('/calendar', [CalendarController::class, 'index'])->name('calendar');

// Métricas y Análisis Estadístico
Route::get('/analysis', [AnalysisController::class, 'index'])->name('analysis');

// Biblioteca Científica y Preguntas Frecuentes
Route::get('/education', [EducationController::class, 'index'])->name('education');

// Privacidad, Configuración y Gestión Soberana de Datos
Route::get('/privacy', [PrivacyController::class, 'index'])->name('privacy');
Route::post('/privacy/settings', [PrivacyController::class, 'saveSettings'])->name('privacy.settings');
Route::get('/privacy/export', [PrivacyController::class, 'exportJson'])->name('privacy.export');
Route::post('/privacy/reset', [PrivacyController::class, 'resetDemo'])->name('privacy.reset');
Route::post('/privacy/clear', [PrivacyController::class, 'clearAll'])->name('privacy.clear');

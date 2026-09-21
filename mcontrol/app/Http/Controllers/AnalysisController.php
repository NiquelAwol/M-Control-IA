<?php

namespace App\Http\Controllers;

use App\Models\Event;
use Carbon\Carbon;
use Illuminate\Http\Request;

class AnalysisController extends Controller
{
    public function index()
    {
        $events = Event::orderBy('event_date', 'desc')->get();
        $total = $events->count();
        $now = Carbon::now();

        // 1. Métricas temporales (7, 14, 30, 90 días)
        $count7 = Event::where('event_date', '>=', $now->copy()->subDays(7))->count();
        $count14 = Event::where('event_date', '>=', $now->copy()->subDays(14))->count();
        $count30 = Event::where('event_date', '>=', $now->copy()->subDays(30))->count();
        $count90 = Event::where('event_date', '>=', $now->copy()->subDays(90))->count();

        // 2. Distribución del semáforo
        $greenCount = $events->where('color', 'green')->count();
        $yellowCount = $events->where('color', 'yellow')->count();
        $redCount = $events->where('color', 'red')->count();

        $pGreen = $total > 0 ? round(($greenCount / $total) * 100) : 0;
        $pYellow = $total > 0 ? round(($yellowCount / $total) * 100) : 0;
        $pRed = $total > 0 ? round(($redCount / $total) * 100) : 0;

        // 3. Análisis de intervalos
        $intervalAvgText = 'N/A';
        $intervalLastText = 'Sin registros';
        $feedbackText = 'Registra eventos para que el sistema genere diagnósticos basados en tu historial.';

        if ($total > 0) {
            $latest = $events->first();
            $diffHours = abs($now->diffInHours($latest->event_date));
            if ($diffHours < 24) {
                $intervalLastText = "{$diffHours} horas";
            } else {
                $diffDays = round($diffHours / 24, 1);
                $intervalLastText = "{$diffDays} días";
            }

            if ($total > 1) {
                $diffs = [];
                for ($i = 0; $i < $total - 1; $i++) {
                    $diffs[] = abs($events[$i]->event_date->diffInHours($events[$i + 1]->event_date)) / 24;
                }
                $avgDays = round(array_sum($diffs) / count($diffs), 1);
                $intervalAvgText = "{$avgDays} días";
            } else {
                $intervalAvgText = '1 evento';
            }

            // Diagnóstico algorítmico
            if ($redCount > 0) {
                $feedbackText = "Has tenido <strong>{$redCount} registros en zona Roja</strong>. El principal motivo detectado ha sido interferencia en el descanso o presencia de fatiga/irritación. Te sugerimos priorizar el autocuidado y permitir descansos más prolongados para recuperar el balance.";
            } elseif ($yellowCount > 0) {
                $feedbackText = "Tu patrón presenta <strong>{$yellowCount} alertas Amarillas</strong>, principalmente vinculadas a intervalos estrechos o momentos de alto estrés. El sistema observa que la autorregulación es buena, pero conviene prestar atención al uso de la conducta como escape de ansiedad.";
            } else {
                $percText = $greenCount === $total ? '100%' : 'mayor porcentaje';
                $feedbackText = "¡Excelente equilibrio! El <strong>{$percText}</strong> de tus registros se encuentra en zona Verde, demostrando buen control personal, sin impacto negativo en tus actividades y con bienestar físico preservado.";
            }
        }

        return view('analysis', compact(
            'total',
            'count7',
            'count14',
            'count30',
            'count90',
            'greenCount',
            'yellowCount',
            'redCount',
            'pGreen',
            'pYellow',
            'pRed',
            'intervalAvgText',
            'intervalLastText',
            'feedbackText'
        ));
    }
}

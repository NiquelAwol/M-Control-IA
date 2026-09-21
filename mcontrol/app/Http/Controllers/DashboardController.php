<?php

namespace App\Http\Controllers;

use App\Models\Event;
use Carbon\Carbon;
use Illuminate\Http\Request;

class DashboardController extends Controller
{
    public function index()
    {
        $events = Event::orderBy('event_date', 'desc')->get();
        $latest = $events->first();

        // Estadísticas rápidas
        $now = Carbon::now();
        $count7Days = Event::where('event_date', '>=', $now->copy()->subDays(7))->count();
        $count30Days = Event::where('event_date', '>=', $now->copy()->subDays(30))->count();
        $avgScore = $events->count() > 0 ? round($events->avg('score')) : 100;

        // Intervalo promedio
        $avgIntervalText = 'Sin datos';
        if ($events->count() >= 2) {
            $diffs = [];
            for ($i = 0; $i < $events->count() - 1; $i++) {
                $diffs[] = abs($events[$i]->event_date->diffInHours($events[$i + 1]->event_date));
            }
            $avgHours = round(array_sum($diffs) / count($diffs));
            if ($avgHours >= 24) {
                $days = round($avgHours / 24, 1);
                $avgIntervalText = "{$days} días";
            } else {
                $avgIntervalText = "{$avgHours} horas";
            }
        }

        // Historial reciente
        $recentEvents = $events->take(5);

        return view('dashboard', compact(
            'latest',
            'count7Days',
            'count30Days',
            'avgScore',
            'avgIntervalText',
            'recentEvents',
            'events'
        ));
    }
}

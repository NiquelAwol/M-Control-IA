<?php

namespace App\Http\Controllers;

use App\Models\Event;
use Carbon\Carbon;
use Illuminate\Http\Request;

class CalendarController extends Controller
{
    public function index(Request $request)
    {
        $year = (int) $request->input('year', Carbon::now()->year);
        $month = (int) $request->input('month', Carbon::now()->month);

        // Validar rangos
        if ($month < 1) {
            $month = 12;
            $year--;
        } elseif ($month > 12) {
            $month = 1;
            $year++;
        }

        $currentDate = Carbon::createFromDate($year, $month, 1);
        $monthName = $currentDate->locale('es')->isoFormat('MMMM YYYY');
        $monthTitle = ucfirst($monthName);

        // Días del mes y día de inicio (Lunes = 0)
        $daysInMonth = $currentDate->daysInMonth;
        $firstDayOfWeek = $currentDate->dayOfWeek; // 0 = Domingo, 1 = Lunes, etc.
        $startDayOffset = ($firstDayOfWeek === 0) ? 6 : $firstDayOfWeek - 1;

        // Consultar eventos del mes solicitado
        $startOfMonth = $currentDate->copy()->startOfMonth();
        $endOfMonth = $currentDate->copy()->endOfMonth();

        $monthEvents = Event::whereBetween('event_date', [$startOfMonth, $endOfMonth])
            ->orderBy('event_date', 'asc')
            ->get();

        // Agrupar eventos por número de día
        $eventsByDay = [];
        for ($d = 1; $d <= $daysInMonth; $d++) {
            $eventsByDay[$d] = [];
        }

        foreach ($monthEvents as $event) {
            $dayNum = (int) $event->event_date->day;
            if (isset($eventsByDay[$dayNum])) {
                $eventsByDay[$dayNum][] = [
                    'id' => $event->id,
                    'date' => $event->event_date->format('Y-m-d H:i'),
                    'time' => $event->event_date->format('H:i'),
                    'control' => $event->control,
                    'interferencia' => $event->interferencia,
                    'sintomas' => $event->sintomas,
                    'estres' => $event->estres,
                    'porno' => $event->porno,
                    'notas' => $event->notas,
                    'score' => $event->score,
                    'color' => $event->color,
                    'explicacion' => $event->explicacion,
                ];
            }
        }

        // Determinar color predominante por día
        $dayColors = [];
        foreach ($eventsByDay as $d => $evList) {
            if (empty($evList)) {
                $dayColors[$d] = null;
            } else {
                $minScoreEvent = $evList[0];
                foreach ($evList as $ev) {
                    if ($ev['score'] < $minScoreEvent['score']) {
                        $minScoreEvent = $ev;
                    }
                }
                $dayColors[$d] = $minScoreEvent['color'];
            }
        }

        // Navegación
        $prevDate = $currentDate->copy()->subMonth();
        $nextDate = $currentDate->copy()->addMonth();

        // Todos los eventos para la tabla del mes / historial
        $tableEvents = Event::orderBy('event_date', 'desc')->get();

        return view('calendar', compact(
            'year',
            'month',
            'monthTitle',
            'daysInMonth',
            'startDayOffset',
            'eventsByDay',
            'dayColors',
            'prevDate',
            'nextDate',
            'tableEvents'
        ));
    }
}

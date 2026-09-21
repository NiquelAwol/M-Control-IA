<?php

namespace App\Services;

use App\Models\Event;
use Carbon\Carbon;

class WellnessScoreService
{
    /**
     * Calcula la puntuación (0-100), el color del semáforo y la explicación
     */
    public function evaluate(array $data, ?int $userId = null): array
    {
        $score = 100;
        $reasons = [];

        $control = $data['control'] ?? 'medio';
        $interferencia = $data['interferencia'] ?? 'ninguna';
        $sintomas = $data['sintomas'] ?? 'ninguno';
        $estres = $data['estres'] ?? 'medio';
        $eventDate = isset($data['event_date']) ? Carbon::parse($data['event_date']) : Carbon::now();

        // 1. Interferencia Funcional (Hasta 35 pts)
        if ($interferencia === 'severa') {
            $score -= 35;
            $reasons[] = 'interferencia significativa con tu rutina, trabajo o descanso';
        } elseif ($interferencia === 'leve') {
            $score -= 15;
            $reasons[] = 'ligera postergación de actividades';
        }

        // 2. Nivel de Control Subjetivo (Hasta 30 pts)
        if ($control === 'bajo') {
            $score -= 30;
            $reasons[] = 'sensación de pérdida de control o dificultad para posponer el impulso';
        } elseif ($control === 'medio') {
            $score -= 10;
            $reasons[] = 'control moderado del impulso';
        }

        // 3. Síntomas Físicos / Molestias (Hasta 25 pts)
        if ($sintomas === 'moderado_severo') {
            $score -= 25;
            $reasons[] = 'molestias físicas notorias o dolor';
        } elseif ($sintomas === 'leve') {
            $score -= 15;
            $reasons[] = 'leve irritación física';
        }

        // 4. Estrés y escape emocional (Hasta 12 pts)
        if ($estres === 'alto') {
            $score -= 12;
            $reasons[] = 'alto nivel de estrés';
        }

        // 5. Intervalo respecto al último evento (Hasta 15 pts)
        $lastEventQuery = Event::query();
        if ($userId) {
            $lastEventQuery->where('user_id', $userId);
        }
        $lastEvent = $lastEventQuery->where('event_date', '<', $eventDate)
            ->orderBy('event_date', 'desc')
            ->first();

        if ($lastEvent) {
            $hoursDiff = $lastEvent->event_date->diffInHours($eventDate);
            if ($hoursDiff >= 0 && $hoursDiff < 12) {
                $score -= 15;
                $reasons[] = 'intervalo muy breve desde el evento anterior (<12h)';
            } elseif ($hoursDiff >= 12 && $hoursDiff < 24) {
                $score -= 8;
                $reasons[] = 'frecuencia cercana (<24h)';
            }
        }

        $score = max(0, min(100, $score));

        // Determinación de color y explicación
        $color = 'green';
        $explicacion = '';

        if ($score >= 70 && $sintomas !== 'moderado_severo' && $control !== 'bajo') {
            $color = 'green';
            $explicacion = empty($reasons)
                ? 'Patrón en óptimo equilibrio: sin interferencia funcional, buen control y sin molestias físicas.'
                : 'Patrón compatible con tu bienestar. Señales mínimas de tensión pero con buen manejo general.';
        } elseif ($score >= 40 && $interferencia !== 'severa') {
            $color = 'yellow';
            $explicacion = 'Conviene observar el patrón. Se detectó: ' . implode(', ', $reasons) . '. Te sugerimos revisar tu contexto y niveles de estrés.';
        } else {
            $color = 'red';
            $reasonsText = !empty($reasons) ? implode(', ', $reasons) : 'sobrecarga física o funcional';
            $explicacion = 'Se recomienda pausa y autocuidado. Hay señales de atención: ' . $reasonsText . '. Si estas sensaciones persisten o generan malestar, recuerda que la orientación profesional puede ayudarte.';
        }

        return [
            'score' => $score,
            'color' => $color,
            'explicacion' => $explicacion,
        ];
    }
}

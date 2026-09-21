<?php

namespace Database\Seeders;

use App\Models\Event;
use Illuminate\Database\Seeder;

class EventSeeder extends Seeder
{
    public function run(): void
    {
        Event::truncate();

        Event::create([
            'event_date' => '2026-09-01 21:30:00',
            'control' => 'alto',
            'interferencia' => 'ninguna',
            'sintomas' => 'ninguno',
            'estres' => 'bajo',
            'porno' => false,
            'notas' => 'Día tranquilo tras ejercicio.',
            'score' => 95,
            'color' => 'green',
            'explicacion' => 'Intervalo adecuado de descanso, sin interferencia en tus actividades ni molestias físicas.',
        ]);

        Event::create([
            'event_date' => '2026-09-03 23:45:00',
            'control' => 'alto',
            'interferencia' => 'ninguna',
            'sintomas' => 'ninguno',
            'estres' => 'medio',
            'porno' => true,
            'notas' => 'Relajación antes de dormir.',
            'score' => 85,
            'color' => 'green',
            'explicacion' => 'Patrón armónico sin impacto negativo en responsabilidades ni dolor físico.',
        ]);

        Event::create([
            'event_date' => '2026-09-04 15:20:00',
            'control' => 'medio',
            'interferencia' => 'leve',
            'sintomas' => 'ninguno',
            'estres' => 'alto',
            'porno' => true,
            'notas' => 'Sensación de estrés por entregas laborales.',
            'score' => 55,
            'color' => 'yellow',
            'explicacion' => 'Intervalo menor a 24h y elevado estrés. Conviene observar si se utiliza como único recurso de escape ante la tensión.',
        ]);

        Event::create([
            'event_date' => '2026-09-06 02:10:00',
            'control' => 'bajo',
            'interferencia' => 'severa',
            'sintomas' => 'leve',
            'estres' => 'alto',
            'porno' => true,
            'notas' => 'Dificultad para posponer el impulso en la madrugada.',
            'score' => 30,
            'color' => 'red',
            'explicacion' => 'Interferencia en el descanso nocturno, sensación de bajo control y ligera molestia física. Se sugiere pausa y autocuidado.',
        ]);
    }
}

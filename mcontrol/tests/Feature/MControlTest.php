<?php

namespace Tests\Feature;

use App\Models\Event;
use App\Models\UserSetting;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class MControlTest extends TestCase
{
    use RefreshDatabase;

    public function test_dashboard_renders_successfully(): void
    {
        $response = $this->get('/');
        $response->assertStatus(200);
        $response->assertSee('Panel de Autorregulación');
    }

    public function test_event_create_page_renders(): void
    {
        $response = $this->get('/events/create');
        $response->assertStatus(200);
        $response->assertSee('Registro de Evento');
    }

    public function test_event_store_calculates_wellness_score_and_saves(): void
    {
        $data = [
            'event_date' => '2026-09-20 10:00:00',
            'control' => 'alto',
            'interferencia' => 'ninguna',
            'sintomas' => 'ninguno',
            'estres' => 'bajo',
            'porno' => '0',
            'notas' => 'Prueba unitaria automatizada',
            'redirect_to' => 'calendar',
        ];

        $response = $this->withoutMiddleware()->post('/events', $data);

        $response->assertRedirect(route('calendar'));
        $this->assertDatabaseHas('events', [
            'control' => 'alto',
            'interferencia' => 'ninguna',
            'score' => 100,
            'color' => 'green',
        ]);
    }

    public function test_calendar_page_renders(): void
    {
        $response = $this->get('/calendar');
        $response->assertStatus(200);
        $response->assertSee('Calendario de Autorregulación');
    }

    public function test_analysis_page_renders(): void
    {
        $response = $this->get('/analysis');
        $response->assertStatus(200);
        $response->assertSee('Análisis de Patrones y Bienestar');
    }

    public function test_education_page_renders(): void
    {
        $response = $this->get('/education');
        $response->assertStatus(200);
        $response->assertSee('Evidencia Científica y Autocuidado');
    }

    public function test_privacy_page_renders_and_export_json_works(): void
    {
        $response = $this->get('/privacy');
        $response->assertStatus(200);
        $response->assertSee('Privacidad y Control de Datos');

        $exportResponse = $this->get('/privacy/export');
        $exportResponse->assertStatus(200);
        $exportResponse->assertHeader('Content-Type', 'application/json');
    }
}

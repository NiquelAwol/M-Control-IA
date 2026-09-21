@extends('layouts.mcontrol')

@section('title', 'M-Control | Análisis y Tendencias')

@push('styles')
<style>
    .progress-bar-container {
        background-color: #0f172a;
        border-radius: 9999px;
        height: 14px;
        overflow: hidden;
        margin: 0.75rem 0 1.25rem 0;
        display: flex;
    }
    .progress-bar-fill {
        height: 100%;
        transition: width 0.5s ease;
    }
</style>
@endpush

@section('content')
    <div class="page-header">
        <div>
            <h1 class="page-title">📊 Análisis de Patrones y Bienestar</h1>
            <p class="page-subtitle">Indicadores estadísticos del modelo multidimensional de M-Control.</p>
        </div>
        <div style="display: flex; gap: 0.5rem;">
            <a href="{{ route('events.create') }}" class="btn btn-success">➕ Registrar Evento</a>
            <a href="{{ route('calendar') }}" class="btn btn-secondary">📅 Ver en Calendario</a>
        </div>
    </div>

    <!-- Métricas Temporales -->
    <div class="grid-4" style="margin-bottom: 2rem;">
        <div class="metric-box">
            <div class="metric-value sensitive-metric">{{ $count7 }}</div>
            <div class="metric-label">Últimos 7 Días</div>
        </div>
        <div class="metric-box">
            <div class="metric-value sensitive-metric">{{ $count14 }}</div>
            <div class="metric-label">Últimos 14 Días</div>
        </div>
        <div class="metric-box">
            <div class="metric-value sensitive-metric">{{ $count30 }}</div>
            <div class="metric-label">Últimos 30 Días</div>
        </div>
        <div class="metric-box">
            <div class="metric-value sensitive-metric">{{ $count90 }}</div>
            <div class="metric-label">Últimos 90 Días</div>
        </div>
    </div>

    <div class="grid-2">
        <!-- Distribución del Semáforo -->
        <div class="card">
            <div class="card-title">🚥 Distribución del Semáforo de Bienestar</div>
            <p style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1.25rem;">
                Proporción de tus registros clasificados según señales de salud y funcionamiento:
            </p>

            <!-- Barra compuesta -->
            <div class="progress-bar-container">
                <div class="progress-bar-fill" style="background-color: var(--color-green); width: {{ $total > 0 ? $pGreen : 100 }}%;"></div>
                <div class="progress-bar-fill" style="background-color: var(--color-yellow); width: {{ $total > 0 ? $pYellow : 0 }}%;"></div>
                <div class="progress-bar-fill" style="background-color: var(--color-red); width: {{ $total > 0 ? $pRed : 0 }}%;"></div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 0.75rem; margin-top: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="display: flex; align-items: center; gap: 0.5rem;">
                        <span class="status-indicator-dot green"></span>
                        <strong>Verde (Balance):</strong>
                    </span>
                    <span style="font-weight: 600; color: var(--color-green);">{{ $greenCount }} ({{ $pGreen }}%)</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="display: flex; align-items: center; gap: 0.5rem;">
                        <span class="status-indicator-dot yellow"></span>
                        <strong>Amarillo (Observar):</strong>
                    </span>
                    <span style="font-weight: 600; color: var(--color-yellow);">{{ $yellowCount }} ({{ $pYellow }}%)</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="display: flex; align-items: center; gap: 0.5rem;">
                        <span class="status-indicator-dot red"></span>
                        <strong>Rojo (Pausa sugerida):</strong>
                    </span>
                    <span style="font-weight: 600; color: var(--color-red);">{{ $redCount }} ({{ $pRed }}%)</span>
                </div>
            </div>

            <div class="callout callout-info" style="margin-top: 1.25rem; margin-bottom: 0;">
                Recuerda: Los colores reflejan tu bienestar y contexto (estrés, molestias, sueño), no un conteo punitivo de abstinencia.
            </div>
        </div>

        <!-- Análisis de Intervalos -->
        <div class="card">
            <div class="card-title">⏱️ Intervalos de Autorregulación</div>
            <p style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1.25rem;">
                Tiempo transcurrido entre eventos para observar tu cadencia personal:
            </p>

            <div class="grid-2" style="margin-bottom: 1rem;">
                <div class="metric-box">
                    <div class="metric-value">{{ $intervalAvgText }}</div>
                    <div class="metric-label">Intervalo Promedio</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">{{ $intervalLastText }}</div>
                    <div class="metric-label">Tiempo desde Último Evento</div>
                </div>
            </div>

            <div style="border-top: 1px solid var(--border-color); padding-top: 1rem;">
                <h4 style="font-size: 0.95rem; margin-bottom: 0.5rem;">Diagnóstico Algorítmico del Patrón:</h4>
                <p style="color: var(--text-secondary); font-size: 0.9rem; line-height: 1.6;">
                    {!! $feedbackText !!}
                </p>
            </div>
        </div>
    </div>

    <!-- Ponderación de Factores del Algoritmo -->
    <div class="card" style="margin-top: 1.5rem;">
        <div class="card-title">⚖️ Modelo de Puntuación de Bienestar (0–100)</div>
        <p style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;">
            M-Control no utiliza una regla rígida como "X días es bueno y Y días es malo". Utiliza la siguiente matriz de pesos científicos:
        </p>
        <div class="table-responsive">
            <table class="table-custom">
                <thead>
                    <tr>
                        <th>Factor Evaluado</th>
                        <th>Peso Científico</th>
                        <th>Criterio de Evaluación</th>
                        <th>Impacto en el Semáforo</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Interferencia Funcional</strong></td>
                        <td><span style="color: var(--color-red); font-weight: 700;">Muy Alto (35%)</span></td>
                        <td>Afectación a responsabilidades de trabajo, estudio, relaciones o sueño.</td>
                        <td>Interferencia severa detona alerta Roja automáticamente.</td>
                    </tr>
                    <tr>
                        <td><strong>Pérdida de Control</strong></td>
                        <td><span style="color: var(--color-red); font-weight: 700;">Muy Alto (30%)</span></td>
                        <td>Incapacidad persistente de posponer el impulso o repetición compulsiva.</td>
                        <td>Bajo control reduce drásticamente el puntaje hacia Amarillo/Rojo.</td>
                    </tr>
                    <tr>
                        <td><strong>Síntomas Físicos</strong></td>
                        <td><span style="color: var(--color-yellow); font-weight: 700;">Alto (25%)</span></td>
                        <td>Rozaduras, inflamación, hipersensibilidad o dolor por fricción excesiva.</td>
                        <td>Molestias moderadas activan recomendación de pausa física.</td>
                    </tr>
                    <tr>
                        <td><strong>Estrés / Escape Emocional</strong></td>
                        <td><span style="color: var(--accent); font-weight: 600;">Medio (15%)</span></td>
                        <td>Uso recurrente como única vía de afrontamiento ante ansiedad intensa.</td>
                        <td>Sugiere diversificar mecanismos de autorregulación emocional.</td>
                    </tr>
                    <tr>
                        <td><strong>Intervalo Histórico Propio</strong></td>
                        <td><span style="color: var(--accent); font-weight: 600;">Medio (15%)</span></td>
                        <td>Comparación con el promedio propio del usuario (no con tablas ajenas).</td>
                        <td>Cambios bruscos hacia alta frecuencia generan alerta Amarilla.</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- Navegación a Educación -->
    <div class="callout callout-info" style="justify-content: space-between; align-items: center; flex-wrap: wrap; margin-top: 1.5rem;">
        <div>
            <strong>¿Quieres profundizar en la base médica de estos factores?</strong>
            <p style="font-size: 0.85rem; color: #bae6fd; margin-top: 0.2rem;">Consulta los criterios de la OMS (ICD-11 CSBD) y organizaciones de medicina sexual.</p>
        </div>
        <a href="{{ route('education') }}" class="btn btn-primary btn-sm">Ir a Biblioteca Científica ➔</a>
    </div>
@endsection

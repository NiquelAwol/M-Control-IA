@extends('layouts.mcontrol')

@section('title', 'M-Control | Panel de Autorregulación')

@section('content')
    <!-- Encabezado de Bienvenida -->
    <div class="page-header">
        <div>
            <h1 class="page-title">Panel de Autorregulación</h1>
            <p class="page-subtitle">Seguimiento inteligente basado en evidencia científica, no en prohibiciones ni culpas.</p>
        </div>
        <div>
            <a href="{{ route('events.create') }}" class="btn btn-success">➕ Nuevo Registro Rápido</a>
        </div>
    </div>

    <!-- Aviso de Seguridad / Principio Científico -->
    <div class="callout callout-info">
        <span style="font-size: 1.5rem;">💡</span>
        <div>
            <strong>Nota de diseño científico:</strong> M-Control no promueve la abstinencia total ni juzga la frecuencia aislada. La ciencia médica (OMS, ISSM) demuestra que la masturbación es una práctica saludable; el foco está en evitar la interferencia funcional, la pérdida de control o el malestar físico.
        </div>
    </div>

    <!-- Estado Actual: Semáforo de Bienestar -->
    @if($latest)
        <div class="card semaforo-card {{ $latest->color }}" id="card-semaforo">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <span class="status-badge {{ $latest->color }}">
                        <span class="status-indicator-dot {{ $latest->color }}"></span>
                        @if($latest->color === 'green')
                            <span>Verde — Patrón Compatible y Equilibrado</span>
                        @elseif($latest->color === 'yellow')
                            <span>Amarillo — Conviene Observar el Contexto</span>
                        @else
                            <span>Rojo — Recomendación de Pausa y Autocuidado</span>
                        @endif
                    </span>
                    <h2 style="font-size: 1.5rem; margin-bottom: 0.5rem;">
                        @if($latest->color === 'green')
                            Tu patrón se encuentra en balance
                        @elseif($latest->color === 'yellow')
                            Atención sugerida a señales de estrés o frecuencia
                        @else
                            Señales de sobrecarga física o interferencia funcional
                        @endif
                    </h2>
                    <p style="color: var(--text-secondary); max-width: 750px;">
                        {{ $latest->explicacion }}
                    </p>
                </div>
                <div style="text-align: right; min-width: 140px;">
                    <div style="font-size: 0.85rem; color: var(--text-muted);">Puntuación de Bienestar</div>
                    <div style="font-size: 2.8rem; font-weight: 800; color: var(--accent);">{{ $latest->score }}</div>
                    <div style="font-size: 0.75rem; color: var(--text-secondary);">Escala de 0 a 100</div>
                </div>
            </div>

            <hr style="border: 0; border-top: 1px solid var(--border-color); margin: 1.25rem 0;">

            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                <div style="font-size: 0.9rem; color: var(--text-muted);">
                    Último evento registrado: <strong>{{ $latest->event_date->format('d/m/Y H:i') }}</strong>
                    @if($latest->notas) <em>("{{ $latest->notas }}")</em> @endif
                </div>
                <div style="display: flex; gap: 0.5rem;">
                    <a href="{{ route('analysis') }}" class="btn btn-secondary btn-sm">Ver Análisis Completo ➔</a>
                    <a href="{{ route('calendar') }}" class="btn btn-secondary btn-sm">Ver Calendario ➔</a>
                </div>
            </div>
        </div>
    @else
        <div class="card semaforo-card green">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <span class="status-badge green">
                        <span class="status-indicator-dot green"></span>
                        <span>Verde — Sin registros aún</span>
                    </span>
                    <h2 style="font-size: 1.5rem; margin-bottom: 0.5rem;">Bienvenido a M-Control</h2>
                    <p style="color: var(--text-secondary); max-width: 750px;">
                        Comienza registrando tu primer evento para que el sistema evalúe tu patrón individual y active el semáforo inteligente.
                    </p>
                </div>
                <div style="text-align: right; min-width: 140px;">
                    <div style="font-size: 0.85rem; color: var(--text-muted);">Puntuación Inicial</div>
                    <div style="font-size: 2.8rem; font-weight: 800; color: var(--color-green);">100</div>
                    <div style="font-size: 0.75rem; color: var(--text-secondary);">Escala de 0 a 100</div>
                </div>
            </div>
            <hr style="border: 0; border-top: 1px solid var(--border-color); margin: 1.25rem 0;">
            <div>
                <a href="{{ route('events.create') }}" class="btn btn-primary btn-sm">Registrar Primer Evento ➔</a>
            </div>
        </div>
    @endif

    <!-- Métricas Resumen -->
    <div class="grid-4" style="margin-bottom: 2rem;">
        <div class="metric-box">
            <div class="metric-value">{{ $count7Days }}</div>
            <div class="metric-label">Eventos (Últimos 7 días)</div>
        </div>
        <div class="metric-box">
            <div class="metric-value">{{ $count30Days }}</div>
            <div class="metric-label">Eventos (Últimos 30 días)</div>
        </div>
        <div class="metric-box">
            <div class="metric-value">{{ $avgIntervalText }}</div>
            <div class="metric-label">Intervalo Promedio</div>
        </div>
        <div class="metric-box">
            <div class="metric-value" style="color: {{ $latest && $latest->control === 'bajo' ? 'var(--color-red)' : ($latest && $latest->control === 'medio' ? 'var(--color-yellow)' : 'var(--color-green)') }};">
                @if($latest)
                    {{ ucfirst($latest->control) }}
                @else
                    Excelente
                @endif
            </div>
            <div class="metric-label">Control Autopercibido</div>
        </div>
    </div>

    <!-- Acceso Rápido a Secciones -->
    <h2 style="font-size: 1.3rem; margin-bottom: 1rem;">Módulos del Sistema</h2>
    <div class="grid-3">
        <!-- Tarjeta Registro -->
        <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div class="card-title">📝 Registro Inteligente</div>
                <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1rem;">
                    Registra tus eventos en segundos valorando aspectos clave: control autopercibido, estrés, molestias físicas e interferencia cotidiana.
                </p>
            </div>
            <a href="{{ route('events.create') }}" class="btn btn-primary btn-block">Ir a Registro ➔</a>
        </div>

        <!-- Tarjeta Calendario -->
        <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div class="card-title">📅 Calendario Semáforo</div>
                <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1rem;">
                    Visualiza tus días en Verde (balance), Amarillo (observación) y Rojo (pausa/autocuidado). Sin clasificaciones morales.
                </p>
            </div>
            <a href="{{ route('calendar') }}" class="btn btn-primary btn-block">Abrir Calendario ➔</a>
        </div>

        <!-- Tarjeta Evidencia Científica -->
        <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div class="card-title">📚 Evidencia y Mitos</div>
                <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1rem;">
                    Aprende con fuentes médicas avaladas (OMS ICD-11, Cleveland Clinic, ISSM). Desmitifica falsas creencias populares sobre la sexualidad.
                </p>
            </div>
            <a href="{{ route('education') }}" class="btn btn-primary btn-block">Consultar Evidencia ➔</a>
        </div>
    </div>

    <!-- Historial Reciente de Registros -->
    @if($recentEvents->count() > 0)
        <div class="card" style="margin-top: 2rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div class="card-title" style="margin: 0;">📋 Historial Reciente</div>
                <a href="{{ route('analysis') }}" class="btn btn-secondary btn-sm">Ver Historial Completo</a>
            </div>
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem;">
                    <thead>
                        <tr style="border-bottom: 2px solid var(--border-color); color: var(--text-muted);">
                            <th style="padding: 0.75rem 0.5rem;">Fecha y Hora</th>
                            <th style="padding: 0.75rem 0.5rem;">Semáforo</th>
                            <th style="padding: 0.75rem 0.5rem;">Puntaje</th>
                            <th style="padding: 0.75rem 0.5rem;">Control</th>
                            <th style="padding: 0.75rem 0.5rem;">Interferencia</th>
                            <th style="padding: 0.75rem 0.5rem;">Estrés</th>
                            <th style="padding: 0.75rem 0.5rem;">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach($recentEvents as $event)
                            <tr style="border-bottom: 1px solid var(--border-color);">
                                <td style="padding: 0.75rem 0.5rem;">{{ $event->event_date->format('d/m/Y H:i') }}</td>
                                <td style="padding: 0.75rem 0.5rem;">
                                    <span class="status-badge {{ $event->color }}" style="font-size: 0.75rem; padding: 0.2rem 0.6rem;">
                                        <span class="status-indicator-dot {{ $event->color }}"></span>
                                        {{ ucfirst($event->color) }}
                                    </span>
                                </td>
                                <td style="padding: 0.75rem 0.5rem; font-weight: 700;">{{ $event->score }}</td>
                                <td style="padding: 0.75rem 0.5rem;">{{ ucfirst($event->control) }}</td>
                                <td style="padding: 0.75rem 0.5rem;">{{ ucfirst($event->interferencia) }}</td>
                                <td style="padding: 0.75rem 0.5rem;">{{ ucfirst($event->estres) }}</td>
                                <td style="padding: 0.75rem 0.5rem;">
                                    <form action="{{ route('events.destroy', $event->id) }}" method="POST" onsubmit="return confirm('¿Eliminar este registro?');" style="display: inline;">
                                        @csrf
                                        @method('DELETE')
                                        <button type="submit" style="background: none; border: none; color: var(--color-red); cursor: pointer; font-size: 0.85rem;">🗑️ Borrar</button>
                                    </form>
                                </td>
                            </tr>
                        @endforeach
                    </tbody>
                </table>
            </div>
        </div>
    @endif
@endsection

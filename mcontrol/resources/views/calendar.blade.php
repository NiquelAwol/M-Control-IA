@extends('layouts.mcontrol')

@section('title', 'M-Control | Calendario Semáforo')

@section('content')
    <div class="page-header">
        <div>
            <h1 class="page-title">📅 Calendario de Autorregulación</h1>
            <p class="page-subtitle">Visualización mensual con sistema de colores orientativo y explicativo.</p>
        </div>
        <div style="display: flex; gap: 0.5rem;">
            <a href="{{ route('events.create') }}" class="btn btn-success">➕ Registrar Hoy</a>
            <a href="{{ route('analysis') }}" class="btn btn-secondary">📊 Ver Métricas</a>
        </div>
    </div>

    <!-- Leyenda del Semáforo -->
    <div class="card" style="padding: 1rem 1.5rem; margin-bottom: 1.5rem;">
        <div style="display: flex; gap: 1.5rem; align-items: center; flex-wrap: wrap; font-size: 0.9rem;">
            <span style="font-weight: 600; color: var(--text-primary);">Leyenda de Orientación:</span>
            <div style="display: flex; align-items: center; gap: 0.4rem;">
                <span class="status-indicator-dot green"></span>
                <span><strong>Verde:</strong> Patrón en balance, sin interferencia ni molestias</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.4rem;">
                <span class="status-indicator-dot yellow"></span>
                <span><strong>Amarillo:</strong> Intervalo corto o estrés; conviene observar</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.4rem;">
                <span class="status-indicator-dot red"></span>
                <span><strong>Rojo:</strong> Pausa sugerida por molestia física o interferencia</span>
            </div>
        </div>
    </div>

    <!-- Contenedor del Calendario -->
    <div class="card">
        <div class="calendar-controls">
            <a href="{{ route('calendar', ['year' => $prevDate->year, 'month' => $prevDate->month]) }}" class="btn btn-secondary btn-sm">
                ◀ Mes Anterior
            </a>
            <h2 id="calendar-month-title" style="font-size: 1.3rem; text-align: center; text-transform: capitalize;">
                {{ $monthTitle }}
            </h2>
            <a href="{{ route('calendar', ['year' => $nextDate->year, 'month' => $nextDate->month]) }}" class="btn btn-secondary btn-sm">
                Mes Siguiente ▶
            </a>
        </div>

        <div class="calendar-grid" id="calendar-grid">
            <!-- Encabezados de días de la semana -->
            @foreach(['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'] as $dayName)
                <div class="calendar-day-header">{{ $dayName }}</div>
            @endforeach

            <!-- Celdas vacías previas al día 1 -->
            @for ($i = 0; $i < $startDayOffset; $i++)
                <div class="calendar-day-cell empty"></div>
            @endfor

            <!-- Celdas de cada día del mes -->
            @for ($day = 1; $day <= $daysInMonth; $day++)
                @php
                    $color = $dayColors[$day] ?? null;
                    $dayEventList = $eventsByDay[$day] ?? [];
                    $hasEvents = !empty($dayEventList);
                @endphp
                <div class="calendar-day-cell {{ $color ? $color : '' }}" onclick="openDayModal({{ $day }})">
                    <div class="day-num">{{ $day }}</div>
                    @if($hasEvents)
                        <div class="day-badge">
                            @if($color === 'green')
                                🟢 Balance
                            @elseif($color === 'yellow')
                                🟡 Observar
                            @else
                                🔴 Pausa
                            @endif
                        </div>
                    @endif
                </div>
            @endfor
        </div>
    </div>

    <!-- Lista de Eventos Recientes -->
    <div class="card" style="margin-top: 1.5rem;">
        <div class="card-title">📋 Registro Detallado de Eventos</div>
        <p style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;">
            Historial cronológico de eventos registrados en la plataforma:
        </p>
        <div class="table-responsive">
            <table class="table-custom">
                <thead>
                    <tr>
                        <th>Fecha y Hora</th>
                        <th>Estado Semáforo</th>
                        <th>Control</th>
                        <th>Interferencia</th>
                        <th>Molestias</th>
                        <th>Puntaje</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    @forelse($tableEvents as $event)
                        <tr>
                            <td><strong>{{ $event->event_date->format('d/m/Y H:i') }}</strong></td>
                            <td>
                                <span class="status-badge {{ $event->color }}" style="margin: 0; padding: 0.2rem 0.6rem; font-size: 0.8rem;">
                                    @if($event->color === 'green')
                                        🟢 Verde
                                    @elseif($event->color === 'yellow')
                                        🟡 Amarillo
                                    @else
                                        🔴 Rojo
                                    @endif
                                </span>
                            </td>
                            <td>
                                @if($event->control === 'alto') Alto @elseif($event->control === 'medio') Medio @else Bajo @endif
                            </td>
                            <td>
                                @if($event->interferencia === 'ninguna') Ninguna @elseif($event->interferencia === 'leve') Leve @else Severa @endif
                            </td>
                            <td>
                                @if($event->sintomas === 'ninguno') Sin molestias @elseif($event->sintomas === 'leve') Leve @else Moderado/Severo @endif
                            </td>
                            <td>
                                <strong style="color: var(--accent);">{{ $event->score }} / 100</strong>
                            </td>
                            <td>
                                <form action="{{ route('events.destroy', $event->id) }}" method="POST" onsubmit="return confirm('¿Deseas eliminar este registro permanentemente?');" style="display:inline;">
                                    @csrf
                                    @method('DELETE')
                                    <button type="submit" class="btn btn-danger btn-sm">Eliminar</button>
                                </form>
                            </td>
                        </tr>
                    @empty
                        <tr>
                            <td colspan="7" style="text-align: center; color: var(--text-muted); padding: 2rem;">
                                No hay eventos registrados aún. Comienza añadiendo uno con el botón superior.
                            </td>
                        </tr>
                    @endforelse
                </tbody>
            </table>
        </div>
    </div>

    <!-- Modal Detalle del Día -->
    <div class="modal-overlay" id="day-modal" style="display: none;">
        <div class="modal-content">
            <div class="modal-header">
                <h3 id="modal-date-title">Detalle del Día</h3>
                <button class="modal-close" onclick="closeModal()">&times;</button>
            </div>
            <div id="modal-body">
                <!-- Contenido dinámico -->
            </div>
            <div style="margin-top: 1.5rem; display: flex; justify-content: flex-end; gap: 0.5rem;">
                <button class="btn btn-secondary btn-sm" onclick="closeModal()">Cerrar</button>
                <a href="{{ route('events.create') }}" class="btn btn-success btn-sm">➕ Agregar Evento Este Día</a>
            </div>
        </div>
    </div>
@endsection

@push('scripts')
<script>
    const eventsByDay = @json($eventsByDay);
    const monthTitle = @json($monthTitle);

    function openDayModal(day) {
        const modal = document.getElementById('day-modal');
        const title = document.getElementById('modal-date-title');
        const body = document.getElementById('modal-body');

        title.innerText = `Día ${day} — ${monthTitle}`;
        const dayEvents = eventsByDay[day] || [];

        if (dayEvents.length === 0) {
            body.innerHTML = `
                <p style="color: var(--text-secondary); margin-bottom: 1rem;">
                    No hay ningún registro anotado para este día.
                </p>
                <div class="callout callout-info">
                    El semáforo neutral o sin eventos indica un día libre de actividad registrada. Recuerda que no existe una cantidad obligatoria fija por semana ni por mes.
                </div>
            `;
        } else {
            let html = `<p style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 1rem;">Total de eventos en esta fecha: <strong>${dayEvents.length}</strong></p>`;
            dayEvents.forEach((ev) => {
                html += `
                    <div class="card semaforo-card ${ev.color}" style="margin-bottom: 1rem; padding: 1rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <strong>Hora: ${ev.time}</strong>
                            <span class="status-badge ${ev.color}" style="margin: 0; padding: 0.2rem 0.6rem; font-size: 0.75rem;">Puntaje: ${ev.score}/100</span>
                        </div>
                        <p style="font-size: 0.85rem; color: var(--text-primary); margin-bottom: 0.5rem;">
                            <strong>Evaluación:</strong> ${ev.explicacion}
                        </p>
                        <div style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.5;">
                            • Control: ${ev.control}<br>
                            • Interferencia: ${ev.interferencia}<br>
                            • Síntomas físicos: ${ev.sintomas}<br>
                            • Estrés previo: ${ev.estres}<br>
                            ${ev.notas ? `• Notas: "${ev.notas}"` : ''}
                        </div>
                    </div>
                `;
            });
            body.innerHTML = html;
        }

        modal.style.display = 'flex';
    }

    function closeModal() {
        document.getElementById('day-modal').style.display = 'none';
    }

    // Cerrar al hacer clic fuera del modal
    document.getElementById('day-modal').addEventListener('click', function(e) {
        if (e.target === this) {
            closeModal();
        }
    });
</script>
@endpush

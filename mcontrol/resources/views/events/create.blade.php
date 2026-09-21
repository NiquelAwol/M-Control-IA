@extends('layouts.mcontrol')

@section('title', 'M-Control | Registrar Evento')

@section('content')
    <div class="page-header">
        <div>
            <h1 class="page-title">📝 Registro de Evento</h1>
            <p class="page-subtitle">Monitorea los factores de contexto y bienestar sin juicios morales ni culpabilidad.</p>
        </div>
        <div>
            <a href="{{ route('dashboard') }}" class="btn btn-secondary">← Volver al Inicio</a>
        </div>
    </div>

    @if ($errors->any())
        <div class="callout callout-info" style="border-left-color: var(--color-red); margin-bottom: 1.5rem;">
            <span style="font-size: 1.5rem;">⚠️</span>
            <div>
                <strong>Por favor corrige los siguientes errores:</strong>
                <ul style="margin-top: 0.5rem; padding-left: 1.25rem;">
                    @foreach ($errors->all() as $error)
                        <li>{{ $error }}</li>
                    @endforeach
                </ul>
            </div>
        </div>
    @endif

    <div class="grid-2">
        <!-- Formulario de Registro -->
        <div class="card">
            <form id="form-registro" action="{{ route('events.store') }}" method="POST">
                @csrf
                <input type="hidden" name="redirect_to" id="redirect_to" value="calendar">

                <!-- Fecha y Hora -->
                <div class="form-group">
                    <label for="event_date" class="form-label">📅 Fecha y Hora del Evento</label>
                    <input type="datetime-local" id="event_date" name="event_date" class="form-control" 
                           value="{{ old('event_date', \Carbon\Carbon::now()->format('Y-m-d\TH:i')) }}" required>
                    <div class="form-hint">Se ajusta automáticamente al momento actual.</div>
                </div>

                <!-- Nivel de Control Subjetivo -->
                <div class="form-group">
                    <label class="form-label">🎯 Nivel de Control Autopercibido</label>
                    <div class="radio-group">
                        <label class="custom-option">
                            <input type="radio" name="control" value="alto" {{ old('control', 'alto') === 'alto' ? 'checked' : '' }}>
                            <div>
                                <strong>Alto control:</strong> Decisión consciente, sin sensación de urgencia impulsiva ni pérdida de control.
                            </div>
                        </label>
                        <label class="custom-option">
                            <input type="radio" name="control" value="medio" {{ old('control') === 'medio' ? 'checked' : '' }}>
                            <div>
                                <strong>Control moderado:</strong> Impulso presente, hubo vacilación pero se decidió continuar.
                            </div>
                        </label>
                        <label class="custom-option">
                            <input type="radio" name="control" value="bajo" {{ old('control') === 'bajo' ? 'checked' : '' }}>
                            <div>
                                <strong>Bajo control:</strong> Dificultad para posponer el impulso o sensación de compulsión repetitiva.
                            </div>
                        </label>
                    </div>
                </div>

                <!-- Interferencia Funcional -->
                <div class="form-group">
                    <label class="form-label">⏰ Interferencia con tu Vida Cotidiana</label>
                    <div class="radio-group">
                        <label class="custom-option">
                            <input type="radio" name="interferencia" value="ninguna" {{ old('interferencia', 'ninguna') === 'ninguna' ? 'checked' : '' }}>
                            <div>
                                <strong>Ninguna interferencia:</strong> Se realizó en tiempo libre sin desatender trabajo, estudio ni sueño.
                            </div>
                        </label>
                        <label class="custom-option">
                            <input type="radio" name="interferencia" value="leve" {{ old('interferencia') === 'leve' ? 'checked' : '' }}>
                            <div>
                                <strong>Interferencia leve:</strong> Pequeño retraso en alguna tarea o leve posposición de responsabilidades.
                            </div>
                        </label>
                        <label class="custom-option">
                            <input type="radio" name="interferencia" value="severa" {{ old('interferencia') === 'severa' ? 'checked' : '' }}>
                            <div>
                                <strong>Interferencia significativa:</strong> Se afectaron horas vitales de sueño, reuniones, trabajo o relaciones.
                            </div>
                        </label>
                    </div>
                </div>

                <!-- Síntomas Físicos -->
                <div class="form-group">
                    <label class="form-label">🩹 Síntomas o Molestias Físicas</label>
                    <div class="radio-group">
                        <label class="custom-option">
                            <input type="radio" name="sintomas" value="ninguno" {{ old('sintomas', 'ninguno') === 'ninguno' ? 'checked' : '' }}>
                            <div>
                                <strong>Sin molestias:</strong> Sensación física normal y cómoda.
                            </div>
                        </label>
                        <label class="custom-option">
                            <input type="radio" name="sintomas" value="leve" {{ old('sintomas') === 'leve' ? 'checked' : '' }}>
                            <div>
                                <strong>Molestia leve:</strong> Ligera rozadura o sensibilidad física transitoria.
                            </div>
                        </label>
                        <label class="custom-option">
                            <input type="radio" name="sintomas" value="moderado_severo" {{ old('sintomas') === 'moderado_severo' ? 'checked' : '' }}>
                            <div>
                                <strong>Dolor o irritación notoria:</strong> Inflamación o dolor que aconseja reposo inmediato.
                            </div>
                        </label>
                    </div>
                </div>

                <!-- Nivel de Estrés / Emoción Previa -->
                <div class="form-group">
                    <label class="form-label">🧠 Nivel de Estrés o Ansiedad Previa</label>
                    <div class="radio-group">
                        <label class="custom-option">
                            <input type="radio" name="estres" value="bajo" {{ old('estres', 'bajo') === 'bajo' ? 'checked' : '' }}>
                            <div>
                                <strong>Bajo / Calma:</strong> Estado anímico equilibrado.
                            </div>
                        </label>
                        <label class="custom-option">
                            <input type="radio" name="estres" value="medio" {{ old('estres') === 'medio' ? 'checked' : '' }}>
                            <div>
                                <strong>Medio:</strong> Nivel habitual de fatiga o carga diaria.
                            </div>
                        </label>
                        <label class="custom-option">
                            <input type="radio" name="estres" value="alto" {{ old('estres') === 'alto' ? 'checked' : '' }}>
                            <div>
                                <strong>Alto:</strong> Tensión o ansiedad intensa, utilizado como única vía de escape emocional.
                            </div>
                        </label>
                    </div>
                </div>

                <!-- Pornografía (Opcional) -->
                <div class="form-group">
                    <label class="form-label">👁️ Registro Opcional de Contenido</label>
                    <label class="custom-option">
                        <input type="checkbox" id="porno" name="porno" value="1" {{ old('porno') ? 'checked' : '' }}>
                        <div>
                            <strong>Acompañado de consumo de pornografía</strong>
                            <div class="form-hint">Variable independiente para analizar si influye en tu nivel de control.</div>
                        </div>
                    </label>
                </div>

                <!-- Notas adicionales -->
                <div class="form-group">
                    <label for="notas" class="form-label">📝 Notas Personales (Opcional)</label>
                    <textarea id="notas" name="notas" class="form-control" rows="2" 
                              placeholder="Ej: Me sentí cansado después de entrenar, o descansé mejor.">{{ old('notas') }}</textarea>
                </div>

                <!-- Acciones de Envío / Redirección -->
                <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1.5rem;">
                    <button type="submit" onclick="document.getElementById('redirect_to').value='calendar'" class="btn btn-success" style="flex: 1;">
                        💾 Guardar y Ver en Calendario
                    </button>
                    <button type="submit" onclick="document.getElementById('redirect_to').value='analysis'" class="btn btn-primary" style="flex: 1;">
                        📊 Guardar y Ver Métricas
                    </button>
                </div>
            </form>
        </div>

        <!-- Panel Lateral: Simulación y Evaluación en Tiempo Real -->
        <div>
            <div class="card semaforo-card green" id="preview-card">
                <div class="card-title">🔍 Evaluación Predictiva en Vivo</div>
                <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1rem;">
                    A medida que seleccionas las opciones, el motor algorítmico de <strong>M-Control</strong> calcula la puntuación y el color orientativo:
                </p>

                <div style="margin-bottom: 1rem;">
                    <span class="status-badge green" id="preview-badge">
                        <span class="status-indicator-dot green" id="preview-dot"></span>
                        <span id="preview-color-txt">🟢 Verde (Balance Óptimo)</span>
                    </span>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1rem;">
                    <span style="font-weight: 600;">Puntaje de Bienestar Estimado:</span>
                    <span style="font-size: 2rem; font-weight: 800; color: var(--accent);" id="preview-score">100 / 100</span>
                </div>

                <div class="callout callout-info" id="preview-explanation" style="font-size: 0.9rem;">
                    Patrón en óptimo equilibrio: sin interferencia funcional, buen control y sin molestias físicas.
                </div>

                <h4 style="font-size: 0.95rem; margin-top: 1.5rem; margin-bottom: 0.5rem;">¿Cómo funciona el semáforo?</h4>
                <ul style="color: var(--text-secondary); font-size: 0.85rem; padding-left: 1.25rem; line-height: 1.6;">
                    <li><strong>🟢 Verde:</strong> Buen balance personal y funcional.</li>
                    <li><strong>🟡 Amarillo:</strong> Observar si se usa como escape de estrés o si el intervalo es acelerado.</li>
                    <li><strong>🔴 Rojo:</strong> No es un juicio moral ni prohibición. Indica necesidad de pausa por dolor físico, interferencia severa o compulsión.</li>
                </ul>
            </div>

            <div class="card" style="margin-top: 1.5rem;">
                <div class="card-title">📌 Accesos Rápidos</div>
                <p style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;">
                    Navega a otras secciones del sistema:
                </p>
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                    <a href="{{ route('calendar') }}" class="btn btn-secondary btn-sm">📅 Ir al Calendario Mensual</a>
                    <a href="{{ route('analysis') }}" class="btn btn-secondary btn-sm">📊 Ir a Panel de Estadísticas</a>
                    <a href="{{ route('education') }}" class="btn btn-secondary btn-sm">📚 Consultar Evidencia Médica</a>
                </div>
            </div>
        </div>
    </div>
@endsection

@push('scripts')
<script>
    document.addEventListener('DOMContentLoaded', () => {
        const form = document.getElementById('form-registro');
        form.addEventListener('change', updateLivePreview);
        updateLivePreview();
    });

    function getFormData() {
        return {
            control: document.querySelector('input[name="control"]:checked')?.value || 'alto',
            interferencia: document.querySelector('input[name="interferencia"]:checked')?.value || 'ninguna',
            sintomas: document.querySelector('input[name="sintomas"]:checked')?.value || 'ninguno',
            estres: document.querySelector('input[name="estres"]:checked')?.value || 'bajo',
        };
    }

    function updateLivePreview() {
        const data = getFormData();
        let score = 100;
        let reasons = [];

        // 1. Interferencia
        if (data.interferencia === 'severa') {
            score -= 35;
            reasons.push('interferencia significativa con tu rutina o descanso');
        } else if (data.interferencia === 'leve') {
            score -= 15;
            reasons.push('ligera postergación de actividades');
        }

        // 2. Control
        if (data.control === 'bajo') {
            score -= 30;
            reasons.push('sensación de pérdida de control o dificultad para posponer el impulso');
        } else if (data.control === 'medio') {
            score -= 10;
            reasons.push('control moderado del impulso');
        }

        // 3. Síntomas
        if (data.sintomas === 'moderado_severo') {
            score -= 25;
            reasons.push('molestias físicas notorias o dolor');
        } else if (data.sintomas === 'leve') {
            score -= 15;
            reasons.push('leve irritación física');
        }

        // 4. Estrés
        if (data.estres === 'alto') {
            score -= 12;
            reasons.push('alto nivel de estrés');
        }

        score = Math.max(0, Math.min(100, score));

        let color = 'green';
        let explicacion = '';

        if (score >= 70 && data.sintomas !== 'moderado_severo' && data.control !== 'bajo') {
            color = 'green';
            explicacion = reasons.length === 0
                ? 'Patrón en óptimo equilibrio: sin interferencia funcional, buen control y sin molestias físicas.'
                : 'Patrón compatible con tu bienestar. Señales mínimas de tensión pero con buen manejo general.';
        } else if (score >= 40 && data.interferencia !== 'severa') {
            color = 'yellow';
            explicacion = 'Conviene observar el patrón. Se detectó: ' + reasons.join(', ') + '. Te sugerimos revisar tu contexto y niveles de estrés.';
        } else {
            color = 'red';
            explicacion = 'Se recomienda pausa y autocuidado. Hay señales de atención: ' + (reasons.join(', ') || 'sobrecarga física o funcional') + '. Recuerda que la orientación profesional puede ayudarte si esto persiste.';
        }

        const card = document.getElementById('preview-card');
        const badge = document.getElementById('preview-badge');
        const dot = document.getElementById('preview-dot');
        const colorTxt = document.getElementById('preview-color-txt');
        const scoreTxt = document.getElementById('preview-score');
        const expl = document.getElementById('preview-explanation');

        card.className = `card semaforo-card ${color}`;
        badge.className = `status-badge ${color}`;
        dot.className = `status-indicator-dot ${color}`;
        scoreTxt.innerText = `${score} / 100`;
        expl.innerText = explicacion;

        if (color === 'green') {
            colorTxt.innerText = '🟢 Verde (Balance Óptimo)';
        } else if (color === 'yellow') {
            colorTxt.innerText = '🟡 Amarillo (Observación)';
        } else {
            colorTxt.innerText = '🔴 Rojo (Pausa Recomendada)';
        }
    }
</script>
@endpush

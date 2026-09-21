@extends('layouts.mcontrol')

@section('title', 'M-Control | Privacidad y Configuración')

@section('content')
    <div class="page-header">
        <div>
            <h1 class="page-title">🔒 Privacidad y Control de Datos</h1>
            <p class="page-subtitle">Principios de seguridad ética y gestión total de tus registros personales.</p>
        </div>
        <div>
            <a href="{{ route('dashboard') }}" class="btn btn-secondary">← Volver al Inicio</a>
        </div>
    </div>

    <!-- Pilares de Privacidad de M-Control -->
    <div class="grid-3" style="margin-bottom: 2rem;">
        <div class="card">
            <div class="card-title">💻 Almacenamiento Seguro Propio</div>
            <p style="color: var(--text-secondary); font-size: 0.85rem; line-height: 1.6;">
                Tus eventos, notas y estados se guardan exclusivamente en tu base de datos SQLite autónoma. No existen servidores externos recolectando tus hábitos íntimos.
            </p>
        </div>
        <div class="card">
            <div class="card-title">🚫 Cero Publicidad y Venta</div>
            <p style="color: var(--text-secondary); font-size: 0.85rem; line-height: 1.6;">
                M-Control rechaza tajantemente la monetización de datos de salud sexual. No hay rastreadores publicitarios, telemetría oculta ni venta a terceros.
            </p>
        </div>
        <div class="card">
            <div class="card-title">👤 Modo Anónimo y Soberanía</div>
            <p style="color: var(--text-secondary); font-size: 0.85rem; line-height: 1.6;">
                No se requiere correo electrónico ni nombre real obligatorio. Puedes enmascarar cifras ante miradas curiosas, exportar o destruir tu historial cuando lo decidas.
            </p>
        </div>
    </div>

    <div class="grid-2">
        <!-- Preferencias y Modo Anónimo -->
        <div class="card">
            <div class="card-title">⚙️ Ajustes del Sistema</div>
            
            <form action="{{ route('privacy.settings') }}" method="POST">
                @csrf
                <div class="form-group">
                    <label class="form-label" for="objetivo">🎯 Objetivo Personal de Seguimiento</label>
                    <select id="objetivo" name="objetivo" class="form-control">
                        <option value="autorregulacion" {{ old('objetivo', $settings->objetivo) === 'autorregulacion' ? 'selected' : '' }}>
                            Equilibrio y Autorregulación (Recomendado)
                        </option>
                        <option value="reduccion" {{ old('objetivo', $settings->objetivo) === 'reduccion' ? 'selected' : '' }}>
                            Reducción consciente de frecuencia
                        </option>
                        <option value="observacion" {{ old('objetivo', $settings->objetivo) === 'observacion' ? 'selected' : '' }}>
                            Observación y autoconocimiento sin metas
                        </option>
                    </select>
                    <div class="form-hint">Adapta los mensajes explicativos de la plataforma a tu meta personal.</div>
                </div>

                <div class="form-group" style="margin-top: 1.5rem;">
                    <label class="form-label">🛡️ Modo Discreto / Camuflaje Visual</label>
                    <label class="custom-option">
                        <input type="checkbox" id="modo_anonimo" name="modo_anonimo" value="1" {{ old('modo_anonimo', $settings->modo_anonimo) ? 'checked' : '' }}>
                        <div>
                            <strong>Ocultar cifras sensibles en pantalla</strong>
                            <div class="form-hint">Muestra puntos (••••) en lugar de números de eventos para evitar que personas cercanas lean tu pantalla.</div>
                        </div>
                    </label>
                </div>

                <div style="margin-top: 1.5rem;">
                    <button type="submit" class="btn btn-primary btn-block">Guardar Ajustes</button>
                </div>
            </form>
        </div>

        <!-- Gestión y Exportación de Datos -->
        <div class="card">
            <div class="card-title">📦 Exportar y Limpiar Información</div>
            <p style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1.25rem;">
                Tú eres el único dueño de tu historial. Utiliza las siguientes herramientas para respaldar o destruir tus datos:
            </p>

            <div style="display: flex; flex-direction: column; gap: 1rem;">
                <div>
                    <a href="{{ route('privacy.export') }}" class="btn btn-secondary btn-block" style="text-align: left; justify-content: flex-start; text-decoration: none;">
                        📥 Exportar Historial Completo (JSON)
                    </a>
                    <div class="form-hint">Descarga un archivo local con todos tus registros, puntuaciones y fechas.</div>
                </div>

                <div>
                    <form action="{{ route('privacy.reset') }}" method="POST" onsubmit="return confirm('¿Deseas restaurar los registros de prueba de ejemplo? Esto reemplazará los registros actuales.');">
                        @csrf
                        <button type="submit" class="btn btn-secondary btn-block" style="text-align: left; justify-content: flex-start;">
                            🔄 Restaurar Datos de Ejemplo Iniciales
                        </button>
                    </form>
                    <div class="form-hint">Restablece los 4 eventos modelo de muestra para continuar explorando las métricas.</div>
                </div>

                <div style="border-top: 1px solid var(--border-color); padding-top: 1rem;">
                    <form action="{{ route('privacy.clear') }}" method="POST" onsubmit="return confirm('¡ADVERTENCIA! Esta acción borrará PERMANENTEMENTE todos tus registros de la base de datos. ¿Estás seguro?');">
                        @csrf
                        <button type="submit" class="btn btn-danger btn-block" style="text-align: left; justify-content: flex-start;">
                            🗑️ Borrar Todos los Registros Permanentemente
                        </button>
                    </form>
                    <div class="form-hint" style="color: #fca5a5;">Elimina instantáneamente todo rastro en la base de datos. Acción irreversible.</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Enlaces y Redirecciones Rápidas -->
    <div class="card" style="margin-top: 1.5rem;">
        <div class="card-title">🚀 Redirecciones Rápidas del Sistema</div>
        <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
            <a href="{{ route('dashboard') }}" class="btn btn-secondary btn-sm">🏠 Dashboard Principal</a>
            <a href="{{ route('calendar') }}" class="btn btn-secondary btn-sm">📅 Calendario Semáforo</a>
            <a href="{{ route('analysis') }}" class="btn btn-secondary btn-sm">📊 Métricas y Tendencias</a>
            <a href="{{ route('education') }}" class="btn btn-secondary btn-sm">📚 Biblioteca Científica</a>
            <a href="{{ route('events.create') }}" class="btn btn-success btn-sm">➕ Registrar Evento</a>
        </div>
    </div>
@endsection

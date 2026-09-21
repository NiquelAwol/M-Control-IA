<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@yield('title', 'M-Control | Autorregulación y Bienestar Masculino')</title>
    <link rel="stylesheet" href="{{ asset('css/styles.css') }}">
    @stack('styles')
</head>
<body>

    <!-- Navegación Superior -->
    <header class="navbar">
        <div class="nav-container">
            <a href="{{ route('dashboard') }}" class="brand">
                <div class="brand-icon">M</div>
                <span>M-Control</span>
                <span class="tag">Laravel Edition</span>
            </a>
            <nav>
                <ul class="nav-links">
                    <li><a href="{{ route('dashboard') }}" class="nav-link {{ request()->routeIs('dashboard') ? 'active' : '' }}">🏠 Inicio</a></li>
                    <li><a href="{{ route('calendar') }}" class="nav-link {{ request()->routeIs('calendar') ? 'active' : '' }}">📅 Calendario</a></li>
                    <li><a href="{{ route('analysis') }}" class="nav-link {{ request()->routeIs('analysis') ? 'active' : '' }}">📊 Métricas</a></li>
                    <li><a href="{{ route('education') }}" class="nav-link {{ request()->routeIs('education') ? 'active' : '' }}">📚 Evidencia y Salud</a></li>
                    <li><a href="{{ route('privacy') }}" class="nav-link {{ request()->routeIs('privacy') ? 'active' : '' }}">🔒 Privacidad</a></li>
                    <li><a href="{{ route('events.create') }}" class="nav-link nav-btn-action">➕ Registrar Evento</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Contenido Principal -->
    <main class="main-content">
        @if(session('success'))
            <div class="callout callout-info" style="border-left-color: var(--color-green); margin-bottom: 1.5rem;">
                <span style="font-size: 1.5rem;">✅</span>
                <div><strong>Éxito:</strong> {{ session('success') }}</div>
            </div>
        @endif

        @if(session('error'))
            <div class="callout callout-info" style="border-left-color: var(--color-red); margin-bottom: 1.5rem;">
                <span style="font-size: 1.5rem;">⚠️</span>
                <div><strong>Atención:</strong> {{ session('error') }}</div>
            </div>
        @endif

        @yield('content')
    </main>

    <footer class="footer" style="text-align: center; padding: 2rem; color: var(--color-text-muted); font-size: 0.85rem; border-top: 1px solid var(--color-border); margin-top: 3rem;">
        <p>M-Control &copy; {{ date('Y') }} &mdash; Plataforma de autorregulación y bienestar masculino basada en evidencia científica (OMS ICD-11, ISSM).</p>
        <p>Desarrollado en Laravel &bull; Privacidad y almacenamiento seguro.</p>
    </footer>

    @stack('scripts')
</body>
</html>

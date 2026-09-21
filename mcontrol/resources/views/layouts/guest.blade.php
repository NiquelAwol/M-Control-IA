<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">

    <title>{{ config('app.name', 'ERP Distribuidora Tecnológica') }}</title>

    <!-- Fuentes Google -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

    <!-- Font Awesome 6 (iconos) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <!-- CDN de Tailwind CSS: Aplica todos los estilos modernos en tiempo real -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Scripts y estilos locales -->
    @vite(['resources/css/app.css', 'resources/js/app.js'])

    <style>
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #172554 100%) !important;
            min-height: 100vh;
        }
    </style>


</head>

<body class="bg-gradient-to-br from-slate-900 via-indigo-950 to-blue-950 min-h-screen flex items-center justify-center p-4 selection:bg-blue-500 selection:text-white">

    <!-- Decoración de fondo (con pointer-events: none forzado para que JAMÁS bloquee clics) -->
    <div class="fixed inset-0 overflow-hidden -z-10" style="pointer-events: none;">
        <div class="absolute -top-40 -right-40 w-96 h-96 rounded-full bg-blue-500/20 blur-3xl"></div>
        <div class="absolute -bottom-40 -left-40 w-96 h-96 rounded-full bg-indigo-500/20 blur-3xl"></div>
    </div>

    <!-- Contenedor central -->
    <div class="w-full max-w-md my-8 relative z-10">
        <!-- Logo y Nombre de la Empresa -->
        <div class="flex justify-center mb-6">
            <a href="/" class="flex flex-col items-center group text-center">
                <img src="{{ asset('img/logo.svg') }}" class="w-16 h-16 transition-transform duration-300 group-hover:scale-105 drop-shadow-md" alt="Logo ERP">
                <span class="mt-3 text-2xl font-bold tracking-tight text-white drop-shadow-sm">
                    ERP Barberos <span class="text-blue-400">Tecnológica</span>
                </span>
                <span class="text-xs text-blue-200/80 uppercase tracking-widest font-semibold mt-1">
                    Plataforma de Gestión Empresarial
                </span>
            </a>
        </div>

        <!-- Tarjeta del Formulario -->
        <div class="bg-white/95 backdrop-blur-md px-8 py-8 shadow-2xl rounded-2xl border border-white/20">
            {{ $slot }}
        </div>

        <!-- Footer -->
        <div class="text-center mt-6 text-xs text-slate-400">
            &copy; 2026 ERP Distribuidora Tecnológica. Todos los derechos reservados.
        </div>
    </div>
</body>

</html>
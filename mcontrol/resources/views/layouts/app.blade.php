<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">

    <title>@yield('titulo', config('app.name', 'Laravel'))</title>

    <!-- Bootstrap 5 CSS CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- FontAwesome para los iconos -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <!-- Scripts / Vite -->
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>

<body class="bg-light">
    <div id="app">
        <!-- Barra de navegación superior o include -->
        @include('layouts.navigation')

        <!-- Cabecera de página opcional -->
        @hasSection('titulo_pagina')
        <div class="bg-white shadow-sm mb-4 py-3">
            <div class="container">
                <h1 class="h3 mb-0 text-gray-800">@yield('titulo_pagina')</h1>
            </div>
        </div>
        @endif

        <!-- Contenido Principal -->
        <main class="container py-4">
            @yield('contenido')
        </main>
    </div>

    <!-- Bootstrap JS Bundle CDN -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    @stack('scripts')
</body>

</html>
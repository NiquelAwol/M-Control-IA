<x-guest-layout>
    <!-- Encabezado del Formulario con Eslogan -->
    <div class="mb-6 text-center">
        <h2 class="text-2xl font-extrabold text-slate-800 tracking-tight">
            Iniciar Sesión
        </h2>
        <p class="text-sm text-slate-500 mt-1">
            Ingresa tus credenciales para acceder al sistema ERP
        </p>
    </div>

    <!-- Estado de Sesión -->
    <x-auth-session-status class="mb-4" :status="session('status')" />

    <form method="POST" action="{{ route('login') }}" class="space-y-5">
        @csrf

        <!-- Campo Correo Electrónico con Icono Font Awesome -->
        <div>
            <label for="email" class="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
                Correo Corporativo
            </label>
            <div class="relative rounded-xl shadow-sm">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                    <i class="fa-solid fa-envelope"></i>
                </div>
                <input id="email"
                    type="email"
                    name="email"
                    value="{{ old('email') }}"
                    required
                    autofocus
                    autocomplete="username"
                    placeholder="usuario@distribuidora.com"
                    class="block w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-800 focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all outline-none" />
            </div>
            <x-input-error :messages="$errors->get('email')" class="mt-1.5" />
        </div>

        <!-- Campo Contraseña con Icono Font Awesome -->
        <div>
            <div class="flex items-center justify-between mb-1">
                <label for="password" class="block text-xs font-bold uppercase tracking-wider text-slate-700">
                    Contraseña
                </label>
                @if (Route::has('password.request'))
                <a class="text-xs font-medium text-blue-600 hover:text-blue-700 hover:underline transition-colors" href="{{ route('password.request') }}">
                    ¿Olvidaste tu contraseña?
                </a>
                @endif
            </div>
            <div class="relative rounded-xl shadow-sm">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                    <i class="fa-solid fa-lock"></i>
                </div>
                <input id="password"
                    type="password"
                    name="password"
                    required
                    autocomplete="current-password"
                    placeholder="••••••••"
                    class="block w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-800 focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all outline-none" />
            </div>
            <x-input-error :messages="$errors->get('password')" class="mt-1.5" />
        </div>

        <!-- Recordarme -->
        <div class="flex items-center">
            <label for="remember_me" class="inline-flex items-center cursor-pointer">
                <input id="remember_me"
                    type="checkbox"
                    name="remember"
                    class="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500 transition">
                <span class="ms-2 text-xs font-medium text-slate-600">Mantener sesión iniciada</span>
            </label>
        </div>

        <!-- Botón de Inicio de Sesión (Forzado con alta visibilidad) -->
        <div>
            <button type="submit" class="w-full flex justify-center items-center gap-2 py-3 px-4 rounded-xl text-white font-semibold text-sm bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 active:scale-[0.99] shadow-lg shadow-blue-500/30 transition-all duration-200 !opacity-100 !bg-blue-600">
                <i class="fa-solid fa-arrow-right-to-bracket text-white"></i>
                <span class="text-white">Ingresar al Sistema</span>
            </button>
        </div>

        <!-- Enlace a Registro -->
        @if (Route::has('register'))
        <div class="text-center pt-2 border-t border-slate-100">
            <p class="text-xs text-slate-500">
                ¿No tienes acceso al ERP?
                <a href="{{ route('register') }}" class="font-bold text-blue-600 hover:text-blue-700 hover:underline ms-1">
                    Solicitar cuenta
                </a>
            </p>
        </div>
        @endif
    </form>
</x-guest-layout>
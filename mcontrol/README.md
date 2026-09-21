<p align="center"><a href="https://laravel.com" target="_blank"><img src="https://raw.githubusercontent.com/laravel/art/master/logo-lockup/5%20SVG/2%20CMYK/1%20Full%20Color/laravel-logolockup-cmyk-red.svg" width="400" alt="Laravel Logo"></a></p>

<p align="center">
<a href="https://github.com/laravel/framework/actions"><img src="https://github.com/laravel/framework/workflows/tests/badge.svg" alt="Build Status"></a>
<a href="https://packagist.org/packages/laravel/framework"><img src="https://img.shields.io/packagist/dt/laravel/framework" alt="Total Downloads"></a>
<a href="https://packagist.org/packages/laravel/framework"><img src="https://img.shields.io/packagist/v/laravel/framework" alt="Latest Stable Version"></a>
<a href="https://packagist.org/packages/laravel/framework"><img src="https://img.shields.io/packagist/l/laravel/framework" alt="License"></a>
</p>

## About Laravel

Laravel is a web application framework with expressive, elegant syntax. We believe development must be an enjoyable and creative experience to be truly fulfilling. Laravel takes the pain out of development by easing common tasks used in many web projects, such as:

- [Simple, fast routing engine](https://laravel.com/docs/routing).
- [Powerful dependency injection container](https://laravel.com/docs/container).
- Multiple back-ends for [session](https://laravel.com/docs/session) and [cache](https://laravel.com/docs/cache) storage.
- Expressive, intuitive [database ORM](https://laravel.com/docs/eloquent).
- Database agnostic [schema migrations](https://laravel.com/docs/migrations).
- [Robust background job processing](https://laravel.com/docs/queues).
- [Real-time event broadcasting](https://laravel.com/docs/broadcasting).

Laravel is accessible, powerful, and provides tools required for large, robust applications.

## Learning Laravel

Laravel has the most extensive and thorough [documentation](https://laravel.com/docs) and video tutorial library of all modern web application frameworks, making it a breeze to get started with the framework.

In addition, [Laracasts](https://laracasts.com) contains thousands of video tutorials on a range of topics including Laravel, modern PHP, unit testing, and JavaScript. Boost your skills by digging into our comprehensive video library.

You can also watch bite-sized lessons with real-world projects on [Laravel Learn](https://laravel.com/learn), where you will be guided through building a Laravel application from scratch while learning PHP fundamentals.

## Agentic Development

Laravel's predictable structure and conventions make it ideal for AI coding agents like Claude Code, Cursor, and GitHub Copilot. Install [Laravel Boost](https://laravel.com/docs/ai) to supercharge your AI workflow:

```bash
composer require laravel/boost --dev

php artisan boost:install
```

Boost provides your agent 15+ tools and skills that help agents build Laravel applications while following best practices.

## Contributing

Thank you for considering contributing to the Laravel framework! The contribution guide can be found in the [Laravel documentation](https://laravel.com/docs/contributions).

## Code of Conduct

In order to ensure that the Laravel community is welcoming to all, please review and abide by the [Code of Conduct](https://laravel.com/docs/contributions#code-of-conduct).

## Security Vulnerabilities

If you discover a security vulnerability within Laravel, please send an e-mail to Taylor Otwell via [taylor@laravel.com](mailto:taylor@laravel.com). All security vulnerabilities will be promptly addressed.

## License

The Laravel framework is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).

---

## Clase 2: Instalación y Configuración de Laravel

### 1. Entorno de Desarrollo y Dependencias
- **Sistema Operativo:** Ubuntu (WSL2) / Docker Desktop
- **Lenguaje:** PHP 8.3 con extensiones requeridas (`ext-xml`, `ext-sqlite3`)
- **Gestor de Dependencias:** Composer 2.x
- **Framework:** Laravel

### 2. Pasos Realizados
1. Verificación de versiones de PHP y Composer en el entorno WSL.
2. Instalación de extensiones necesarias de PHP.
3. Creación del proyecto Laravel con Composer.
4. Organización del proyecto en la raíz del repositorio respetando el archivo `.gitignore`.
5. Ejecución del servidor local con `php artisan serve`.
6. Confirmación de acceso en el navegador (`http://127.0.0.1:8000`).

### 3. Evidencias
Ubicadas en la carpeta `/Clase2`:
- `Captura 1`: Comprobación de versiones (`php -v` y `composer --version`).
- `Captura 2`: Estructura de archivos (`ls -la`).
- `Captura 3`: Pantalla de bienvenida de Laravel en el navegador.

---

## Clase 2: Instalación y Configuración de Laravel

### 1. Entorno de Desarrollo y Dependencias
- **Sistema Operativo:** Ubuntu (WSL2) / Docker Desktop
- **Lenguaje:** PHP 8.3 con extensiones requeridas (`ext-xml`, `ext-sqlite3`)
- **Gestor de Dependencias:** Composer 2.x
- **Framework:** Laravel

### 2. Pasos Realizados
1. Verificación de versiones de PHP y Composer en el entorno WSL.
2. Instalación de extensiones necesarias de PHP.
3. Creación del proyecto Laravel con Composer.
4. Organización del proyecto en la raíz del repositorio respetando el archivo `.gitignore`.
5. Ejecución del servidor local con `php artisan serve`.
6. Confirmación de acceso en el navegador (`http://127.0.0.1:8000`).

### 3. Evidencias
Ubicadas en los archivos rar del repositorio

# Entregable Semana 2: Instalación Laravel + Sail - Estructura y MVC

## Capítulo 2: Instalación de Laravel

### 1. Explicación de la estructura de carpetas
- **app/**: Contiene la lógica central del negocio y la arquitectura de la aplicación (Controladores, Modelos, Middleware, etc.).
- **config/**: Contiene todos los archivos de configuración del proyecto (base de datos, correo, servicios, etc.).
- **database/**: Contiene las migraciones de tablas, fábricas (*factories*) y pobladores (*seeders*) para la base de datos.
- **public/**: Punto de entrada HTTP para la aplicación (`index.php`) y lugar para activos públicos como imágenes, CSS y JS compilados.
- **resources/**: Contiene las vistas Blade (`views`), además de los archivos de idioma y recursos JS/CSS fuente.
- **routes/**: Define todas las rutas de la aplicación (`web.php` para la web, `console.php` para comandos Artisan).
- **storage/**: Almacena logs del sistema, archivos cargados, caché de plantillas y sesiones.
- **vendor/**: Contiene las dependencias de PHP administradas por Composer.

### 2. Diagrama del flujo de una petición (MVC)
```text
[Usuario / Navegador]
        │
        ▼
  [routes/web.php] ──► (Mapea la URL /dashboard)
        │
        ▼
[DashboardController] ──► (Consulta métricas) ──► [Modelo User / DB (MySQL)]
        │                                                     │
        ◄────────── (Retorna datos al controller) ────────────┘
        │
        ▼
[resources/views/dashboard/index.blade.php] ──► (Renderiza la vista HTML con Chart.js)
        │
        ▼
  [Navegador]
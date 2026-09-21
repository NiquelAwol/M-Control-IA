@extends('layouts.app')

@section('titulo', 'Dashboard')
@section('titulo_pagina', 'Panel de Control')

@section('contenido')
<!-- Tarjetas de estadísticas -->
<div class="row">
    <div class="col-xl-4 col-md-6 mb-4">
        <div class="card card-stats shadow h-100">
            <div class="card-body">
                <div class="row align-items-center">
                    <div class="col">
                        <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                            Total Usuarios</div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">{{ $totalUsuarios }}</div>
                    </div>
                    <div class="col-auto">
                        <div class="icon-circle bg-primary text-white">
                            <i class="fas fa-users fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="col-xl-4 col-md-6 mb-4">
        <div class="card card-stats shadow h-100" style="border-left-color: #1cc88a;">
            <div class="card-body">
                <div class="row align-items-center">
                    <div class="col">
                        <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                            Nuevos Hoy</div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">{{ $usuariosHoy }}</div>
                    </div>
                    <div class="col-auto">
                        <div class="icon-circle bg-success text-white">
                            <i class="fas fa-user-plus fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="col-xl-4 col-md-6 mb-4">
        <div class="card card-stats shadow h-100" style="border-left-color: #f6c23e;">
            <div class="card-body">
                <div class="row align-items-center">
                    <div class="col">
                        <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                            Registros Totales</div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">{{ $totalUsuarios * 3 }}</div>
                    </div>
                    <div class="col-auto">
                        <div class="icon-circle bg-warning text-white">
                            <i class="fas fa-file-alt fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Gráfico y Tabla -->
<div class="row">
    <!-- Gráfico -->
    <div class="col-xl-8 col-lg-7">
        <div class="card shadow mb-4">
            <div class="card-header py-3">
                <h6 class="m-0 font-weight-bold text-primary">Usuarios registrados por día (última semana)</h6>
            </div>
            <div class="card-body">
                <canvas id="userChart" width="100%" height="50"></canvas>
            </div>
        </div>
    </div>

    <!-- Tabla de usuarios recientes -->
    <div class="col-xl-4 col-lg-5">
        <div class="card shadow mb-4">
            <div class="card-header py-3">
                <h6 class="m-0 font-weight-bold text-primary">Últimos usuarios</h6>
            </div>
            <div class="card-body">
                <div class="list-group">
                    @forelse ($usuariosRecientes as $user)
                    <div class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                            <i class="fas fa-user-circle me-2 text-primary"></i>
                            {{ $user->name }}
                        </div>
                        <span class="badge bg-secondary rounded-pill">{{ $user->created_at->diffForHumans() }}</span>
                    </div>
                    @empty
                    <p class="text-muted">No hay usuarios registrados.</p>
                    @endforelse
                </div>
            </div>
        </div>
    </div>
</div>
@endsection

@push('scripts')
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const ctx = document.getElementById('userChart').getContext('2d');
        const userChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: @json($fechas),
                datasets: [{
                    label: 'Usuarios registrados',
                    data: @json($cantidades),
                    backgroundColor: 'rgba(78, 115, 223, 0.8)',
                    borderColor: 'rgba(78, 115, 223, 1)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    });
</script>
@endpush
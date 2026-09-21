<?php

namespace App\Http\Controllers;

use App\Models\Event;
use App\Models\UserSetting;
use Database\Seeders\EventSeeder;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\StreamedResponse;

class PrivacyController extends Controller
{
    public function index()
    {
        $settings = UserSetting::first() ?? new UserSetting([
            'objetivo' => 'autorregulacion',
            'modo_anonimo' => false,
            'alerta_sintomas' => true,
        ]);

        return view('privacy', compact('settings'));
    }

    public function saveSettings(Request $request)
    {
        $validated = $request->validate([
            'objetivo' => 'required|in:autorregulacion,reduccion,observacion',
            'modo_anonimo' => 'nullable|boolean',
        ]);

        $settings = UserSetting::first();
        if (!$settings) {
            $settings = new UserSetting();
        }

        $settings->objetivo = $validated['objetivo'];
        $settings->modo_anonimo = $request->boolean('modo_anonimo');
        $settings->save();

        return back()->with('success', 'Ajustes de privacidad guardados correctamente.');
    }

    public function exportJson()
    {
        $events = Event::orderBy('event_date', 'asc')->get();
        $settings = UserSetting::first();

        $data = [
            'export_date' => now()->toIso8601String(),
            'platform' => 'M-Control Laravel Edition',
            'settings' => $settings,
            'total_events' => $events->count(),
            'events' => $events,
        ];

        $json = json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
        $fileName = 'mcontrol_export_' . now()->format('Y_m_d_His') . '.json';

        return response($json, 200, [
            'Content-Type' => 'application/json',
            'Content-Disposition' => "attachment; filename=\"{$fileName}\"",
        ]);
    }

    public function resetDemo()
    {
        Event::truncate();
        $seeder = new EventSeeder();
        $seeder->run();

        return back()->with('success', 'Se han restaurado los datos de ejemplo predeterminados.');
    }

    public function clearAll()
    {
        Event::truncate();

        return back()->with('success', 'Todos los registros han sido eliminados de la base de datos de manera definitiva.');
    }
}

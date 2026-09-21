<?php

namespace App\Http\Controllers;

use App\Models\Event;
use App\Services\WellnessScoreService;
use Illuminate\Http\Request;

class EventController extends Controller
{
    protected WellnessScoreService $wellnessService;

    public function __construct(WellnessScoreService $wellnessService)
    {
        $this->wellnessService = $wellnessService;
    }

    /**
     * Muestra el formulario para registrar un nuevo evento.
     */
    public function create()
    {
        $latestEvents = Event::orderBy('event_date', 'desc')->take(5)->get();
        return view('events.create', compact('latestEvents'));
    }

    /**
     * Almacena un nuevo registro en la base de datos con evaluación algorítmica.
     */
    public function store(Request $request)
    {
        $validated = $request->validate([
            'event_date' => 'required|date',
            'control' => 'required|in:alto,medio,bajo',
            'interferencia' => 'required|in:ninguna,leve,severa',
            'sintomas' => 'required|in:ninguno,leve,moderado_severo',
            'estres' => 'required|in:bajo,medio,alto',
            'porno' => 'nullable|boolean',
            'notas' => 'nullable|string|max:1000',
            'redirect_to' => 'nullable|string|in:calendar,analysis,dashboard',
        ]);

        // Evaluar con el servicio algorítmico de bienestar
        $eval = $this->wellnessService->evaluate($validated);

        // Guardar el evento
        Event::create([
            'event_date' => $validated['event_date'],
            'control' => $validated['control'],
            'interferencia' => $validated['interferencia'],
            'sintomas' => $validated['sintomas'],
            'estres' => $validated['estres'],
            'porno' => $request->boolean('porno'),
            'notas' => $validated['notas'] ?? null,
            'score' => $eval['score'],
            'color' => $eval['color'],
            'explicacion' => $eval['explicacion'],
        ]);

        $redirectTo = $request->input('redirect_to', 'calendar');
        $targetRoute = match ($redirectTo) {
            'analysis' => 'analysis',
            'dashboard' => 'dashboard',
            default => 'calendar',
        };

        return redirect()->route($targetRoute)->with('success', '¡Registro guardado exitosamente con evaluación algorítmica!');
    }

    /**
     * Elimina un registro de la base de datos.
     */
    public function destroy(Event $event)
    {
        $event->delete();
        return back()->with('success', 'Registro eliminado del historial correctamente.');
    }

    /**
     * Endpoint API para evaluación en tiempo real (Live Preview).
     */
    public function evaluateLive(Request $request)
    {
        $data = $request->only(['event_date', 'control', 'interferencia', 'sintomas', 'estres']);
        $eval = $this->wellnessService->evaluate($data);
        return response()->json($eval);
    }
}

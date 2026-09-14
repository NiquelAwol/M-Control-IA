/**
 * M-Control: Módulo de Almacenamiento Local y Algoritmo de Bienestar
 * Basado en la investigación científica y conceptual de M-Control (2026)
 */

const STORAGE_KEY_EVENTS = 'mcontrol_events_data';
const STORAGE_KEY_SETTINGS = 'mcontrol_user_settings';

// Datos de ejemplo iniciales para que el usuario experimente el prototipo de inmediato
const DEFAULT_EVENTS = [
    {
        id: 'evt-1',
        date: '2026-09-01T21:30',
        control: 'alto', // alto, medio, bajo
        interferencia: 'ninguna', // ninguna, leve, severa
        sintomas: 'ninguno', // ninguno, leve, moderado_severo
        estres: 'bajo', // bajo, medio, alto
        porno: false,
        notas: 'Día tranquilo tras ejercicio.',
        score: 95,
        color: 'green',
        explicacion: 'Intervalo adecuado de descanso, sin interferencia en tus actividades ni molestias físicas.'
    },
    {
        id: 'evt-2',
        date: '2026-09-03T23:45',
        control: 'alto',
        interferencia: 'ninguna',
        sintomas: 'ninguno',
        estres: 'medio',
        porno: true,
        notas: 'Relajación antes de dormir.',
        score: 85,
        color: 'green',
        explicacion: 'Patrón armónico sin impacto negativo en responsabilidades ni dolor físico.'
    },
    {
        id: 'evt-3',
        date: '2026-09-04T15:20',
        control: 'medio',
        interferencia: 'leve', // leve retraso en deberes
        sintomas: 'ninguno',
        estres: 'alto',
        porno: true,
        notas: 'Sensación de estrés por entregas laborales.',
        score: 55,
        color: 'yellow',
        explicacion: 'Intervalo menor a 24h y elevado estrés. Conviene observar si se utiliza como único recurso de escape ante la tensión.'
    },
    {
        id: 'evt-4',
        date: '2026-09-06T02:10',
        control: 'bajo',
        interferencia: 'severa', // afectó horas de sueño
        sintomas: 'leve', // ligera irritación
        estres: 'alto',
        porno: true,
        notas: 'Dificultad para posponer el impulso en la madrugada.',
        score: 30,
        color: 'red',
        explicacion: 'Interferencia en el descanso nocturno, sensación de bajo control y ligera molestia física. Se sugiere pausa y autocuidado.'
    }
];

const DEFAULT_SETTINGS = {
    objetivo: 'autorregulacion', // autorregulacion, reduccion, observacion
    modoAnonimo: false,
    alertaSintomas: true
};

const StorageService = {
    // Inicializar almacenamiento si está vacío
    init() {
        if (!localStorage.getItem(STORAGE_KEY_EVENTS)) {
            localStorage.setItem(STORAGE_KEY_EVENTS, JSON.stringify(DEFAULT_EVENTS));
        }
        if (!localStorage.getItem(STORAGE_KEY_SETTINGS)) {
            localStorage.setItem(STORAGE_KEY_SETTINGS, JSON.stringify(DEFAULT_SETTINGS));
        }
    },

    // Obtener todos los eventos ordenados por fecha descendente
    getEvents() {
        this.init();
        try {
            const data = JSON.parse(localStorage.getItem(STORAGE_KEY_EVENTS));
            return data.sort((a, b) => new Date(b.date) - new Date(a.date));
        } catch (e) {
            console.error('Error al leer eventos:', e);
            return DEFAULT_EVENTS;
        }
    },

    // Guardar nuevo evento
    saveEvent(eventData) {
        const events = this.getEvents();
        
        // Calcular algoritmo de bienestar
        const evaluation = this.calculateWellness(eventData, events);
        
        const newEvent = {
            id: 'evt-' + Date.now(),
            date: eventData.date || new Date().toISOString().slice(0, 16),
            control: eventData.control || 'medio',
            interferencia: eventData.interferencia || 'ninguna',
            sintomas: eventData.sintomas || 'ninguno',
            estres: eventData.estres || 'medio',
            porno: !!eventData.porno,
            notas: eventData.notas || '',
            score: evaluation.score,
            color: evaluation.color,
            explicacion: evaluation.explicacion
        };

        events.unshift(newEvent);
        localStorage.setItem(STORAGE_KEY_EVENTS, JSON.stringify(events));
        return newEvent;
    },

    // Eliminar evento por id
    deleteEvent(id) {
        let events = this.getEvents();
        events = events.filter(e => e.id !== id);
        localStorage.setItem(STORAGE_KEY_EVENTS, JSON.stringify(events));
    },

    // Reiniciar datos a los ejemplos
    resetData() {
        localStorage.setItem(STORAGE_KEY_EVENTS, JSON.stringify(DEFAULT_EVENTS));
        localStorage.setItem(STORAGE_KEY_SETTINGS, JSON.stringify(DEFAULT_SETTINGS));
    },

    // Borrar todo completamente
    clearAll() {
        localStorage.setItem(STORAGE_KEY_EVENTS, JSON.stringify([]));
    },

    // Obtener configuración
    getSettings() {
        this.init();
        try {
            return JSON.parse(localStorage.getItem(STORAGE_KEY_SETTINGS));
        } catch (e) {
            return DEFAULT_SETTINGS;
        }
    },

    // Guardar configuración
    saveSettings(settings) {
        localStorage.setItem(STORAGE_KEY_SETTINGS, JSON.stringify(settings));
    },

    // Algoritmo de Puntuación de Bienestar (0 - 100) e interpretación de colores
    calculateWellness(current, existingEvents) {
        let score = 100;
        let reasons = [];

        // 1. Interferencia Funcional (Peso: Muy Alto - hasta 35 pts)
        if (current.interferencia === 'severa') {
            score -= 35;
            reasons.push('interferencia significativa con tu rutina, trabajo o descanso');
        } else if (current.interferencia === 'leve') {
            score -= 15;
            reasons.push('ligera postergación de actividades');
        }

        // 2. Nivel de Control Subjetivo (Peso: Muy Alto - hasta 30 pts)
        if (current.control === 'bajo') {
            score -= 30;
            reasons.push('sensación de pérdida de control o dificultad para posponer el impulso');
        } else if (current.control === 'medio') {
            score -= 10;
            reasons.push('control moderado del impulso');
        }

        // 3. Síntomas Físicos / Molestias (Peso: Alto - hasta 25 pts)
        if (current.sintomas === 'moderado_severo') {
            score -= 25;
            reasons.push('molestias físicas notorias o dolor');
        } else if (current.sintomas === 'leve') {
            score -= 15;
            reasons.push('leve irritación física');
        }

        // 4. Estrés y escape emocional (Peso: Medio - hasta 15 pts)
        if (current.estres === 'alto') {
            score -= 12;
            reasons.push('alto nivel de estrés');
        }

        // 5. Intervalo respecto al último evento (Peso: Medio - hasta 15 pts)
        if (existingEvents && existingEvents.length > 0) {
            const lastDate = new Date(existingEvents[0].date);
            const currentDate = new Date(current.date);
            const hoursDiff = (currentDate - lastDate) / (1000 * 60 * 60);

            if (hoursDiff > 0 && hoursDiff < 12) {
                score -= 15;
                reasons.push('intervalo muy breve desde el evento anterior (<12h)');
            } else if (hoursDiff >= 12 && hoursDiff < 24) {
                score -= 8;
                reasons.push('frecuencia cercana (<24h)');
            }
        }

        // Asegurar rango 0 a 100
        score = Math.max(0, Math.min(100, score));

        // Determinación de color según reglas de M-Control
        let color = 'green';
        let explicacion = '';

        if (score >= 70 && current.sintomas !== 'moderado_severo' && current.control !== 'bajo') {
            color = 'green';
            explicacion = reasons.length === 0
                ? 'Patrón en óptimo equilibrio: sin interferencia funcional, buen control y sin molestias físicas.'
                : 'Patrón compatible con tu bienestar. Señales mínimas de tensión pero con buen manejo general.';
        } else if (score >= 40 && current.interferencia !== 'severa') {
            color = 'yellow';
            explicacion = 'Conviene observar el patrón. Se detectó: ' + reasons.join(', ') + '. Te sugerimos revisar tu contexto y niveles de estrés.';
        } else {
            color = 'red';
            explicacion = 'Se recomienda pausa y autocuidado. Hay señales de atención: ' + (reasons.join(', ') || 'sobrecarga física o funcional') + '. Si estas sensaciones persisten o generan malestar, recuerda que la orientación profesional puede ayudarte.';
        }

        return { score, color, explicacion };
    }
};

// Exponer en entorno global del navegador
window.StorageService = StorageService;

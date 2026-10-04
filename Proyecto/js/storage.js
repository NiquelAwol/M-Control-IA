/**
 * M-Control: Módulo de Almacenamiento Local y Algoritmo de Bienestar
 * Basado en la investigación científica y conceptual de M-Control (2026)
 * Incluye soporte para el Calendario Predictivo Inteligente de 4 Estados (CIE-11 CSBD, NSSHB)
 */

const STORAGE_KEY_EVENTS = 'mcontrol_events_data';
const STORAGE_KEY_SETTINGS = 'mcontrol_user_settings';

// Datos longitudinales representativos (Julio - Octubre 2026) sincronizados con la base de datos
const DEFAULT_EVENTS = [
    {
        id: 'evt-1',
        date: '2026-07-01T22:30',
        control: 'alto',
        interferencia: 'ninguna',
        sintomas: 'ninguno',
        estres: 'bajo',
        porno: false,
        notas: 'Día tranquilo de descanso',
        score: 95,
        color: 'green',
        explicacion: 'Intervalo adecuado de descanso, sin interferencia ni molestias físicas.'
    },
    {
        id: 'evt-2',
        date: '2026-07-04T10:15',
        control: 'alto',
        interferencia: 'ninguna',
        sintomas: 'ninguno',
        estres: 'bajo',
        porno: false,
        notas: 'Fin de semana',
        score: 92,
        color: 'green',
        explicacion: 'Patrón armónico sin impacto negativo en responsabilidades.'
    },
    {
        id: 'evt-5',
        date: '2026-07-09T21:00',
        control: 'medio',
        interferencia: 'leve',
        sintomas: 'ninguno',
        estres: 'alto',
        porno: true,
        notas: 'Preocupación laboral',
        score: 64,
        color: 'yellow',
        explicacion: 'Intervalo menor a 24h y elevado estrés. Conviene observar contexto.'
    },
    {
        id: 'evt-7',
        date: '2026-07-10T23:10',
        control: 'bajo',
        interferencia: 'severa',
        sintomas: 'moderado_severo',
        estres: 'alto',
        porno: true,
        notas: 'Sensación de culpa y molestia',
        score: 22,
        color: 'red',
        explicacion: 'Interferencia en el descanso nocturno, sensación de bajo control y molestia física.'
    },
    {
        id: 'evt-18',
        date: '2026-08-01T11:30',
        control: 'bajo',
        interferencia: 'severa',
        sintomas: 'leve',
        estres: 'alto',
        porno: true,
        notas: 'Doble evento en menos de 14h',
        score: 28,
        color: 'red',
        explicacion: 'Frecuencia acelerada con pérdida de control autopercibido.'
    },
    {
        id: 'evt-25',
        date: '2026-08-15T09:00',
        control: 'bajo',
        interferencia: 'severa',
        sintomas: 'moderado_severo',
        estres: 'alto',
        porno: true,
        notas: 'Fuerte dolor e irritación tras desvelo',
        score: 18,
        color: 'red',
        explicacion: 'Alta interferencia y dolor físico. Se requiere pausa biológica.'
    },
    {
        id: 'evt-26',
        date: '2026-08-18T16:45',
        control: 'alto',
        interferencia: 'ninguna',
        sintomas: 'ninguno',
        estres: 'bajo',
        porno: false,
        notas: 'Pausa biológica de 79 horas',
        score: 96,
        color: 'green',
        explicacion: 'Excelente recuperación y autocontrol restaurado.'
    },
    {
        id: 'evt-38',
        date: '2026-09-10T08:30',
        control: 'bajo',
        interferencia: 'severa',
        sintomas: 'moderado_severo',
        estres: 'alto',
        porno: true,
        notas: 'Repetición matutina impulsiva',
        score: 20,
        color: 'red',
        explicacion: 'Afectación de responsabilidades académicas matutinas.'
    },
    {
        id: 'evt-44',
        date: '2026-09-21T14:00',
        control: 'bajo',
        interferencia: 'severa',
        sintomas: 'leve',
        estres: 'alto',
        porno: true,
        notas: 'Interferencia leve en jornada',
        score: 35,
        color: 'red',
        explicacion: 'Dificultad para posponer el impulso en período de exámenes.'
    },
    {
        id: 'evt-46',
        date: '2026-10-01T22:00',
        control: 'alto',
        interferencia: 'ninguna',
        sintomas: 'ninguno',
        estres: 'bajo',
        porno: false,
        notas: 'Pausa previa de 9 días',
        score: 96,
        color: 'green',
        explicacion: 'Inicio de mes con autorregulación óptima y pleno bienestar.'
    },
    {
        id: 'evt-47',
        date: '2026-10-02T23:15',
        control: 'alto',
        interferencia: 'ninguna',
        sintomas: 'ninguno',
        estres: 'bajo',
        porno: false,
        notas: 'Día de trabajo normal',
        score: 88,
        color: 'green',
        explicacion: 'Descanso adecuado de 25 horas sin interferencia cotidiana.'
    },
    {
        id: 'evt-48',
        date: '2026-10-03T19:00',
        control: 'medio',
        interferencia: 'leve',
        sintomas: 'ninguno',
        estres: 'medio',
        porno: true,
        notas: 'Fin de semana acelerado',
        score: 65,
        color: 'yellow',
        explicacion: 'Menor tiempo de descanso (19h); mantener vigilancia de contexto.'
    }
];

const DEFAULT_SETTINGS = {
    objetivo: 'autorregulacion',
    edad: 24,
    modoAnonimo: false,
    alertaSintomas: true
};

const StorageService = {
    init() {
        if (!localStorage.getItem(STORAGE_KEY_EVENTS)) {
            localStorage.setItem(STORAGE_KEY_EVENTS, JSON.stringify(DEFAULT_EVENTS));
        }
        if (!localStorage.getItem(STORAGE_KEY_SETTINGS)) {
            localStorage.setItem(STORAGE_KEY_SETTINGS, JSON.stringify(DEFAULT_SETTINGS));
        }
    },

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

    saveEvent(eventData) {
        const events = this.getEvents();
        const evaluation = this.calculateWellness(eventData, events);
        
        const newEvent = {
            id: 'evt-' + Date.now(),
            date: eventData.date,
            control: eventData.control,
            interferencia: eventData.interferencia,
            sintomas: eventData.sintomas,
            estres: eventData.estres,
            porno: eventData.porno || false,
            notas: eventData.notas || '',
            score: evaluation.score,
            color: evaluation.color,
            explicacion: evaluation.explicacion
        };

        events.unshift(newEvent);
        localStorage.setItem(STORAGE_KEY_EVENTS, JSON.stringify(events));

        // Notificar opcionalmente al backend de IA si está accesible
        try {
            fetch('/api/records', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    fecha: eventData.date.split('T')[0],
                    hora: eventData.date.split('T')[1] || '12:00',
                    nivel_control: eventData.control === 'alto' ? 5 : (eventData.control === 'medio' ? 3 : 1),
                    interferencia_sueno: eventData.interferencia === 'severa' ? 2 : (eventData.interferencia === 'leve' ? 1 : 0),
                    dolor: eventData.sintomas === 'moderado_severo' ? 2 : (eventData.sintomas === 'leve' ? 1 : 0),
                    estado_emocional: eventData.estres === 'alto' ? 'Estrés alto' : 'Calma',
                    observaciones: eventData.notas || ''
                })
            }).catch(() => {});
        } catch (err) {}

        return newEvent;
    },

    deleteEvent(id) {
        let events = this.getEvents();
        events = events.filter(e => e.id !== id);
        localStorage.setItem(STORAGE_KEY_EVENTS, JSON.stringify(events));
    },

    calculateWellness(current, pastEvents) {
        let score = 100;
        let reasons = [];

        // 1. Interferencia Funcional (35%)
        if (current.interferencia === 'severa') {
            score -= 35;
            reasons.push('Interferencia significativa en trabajo, estudio o descanso.');
        } else if (current.interferencia === 'leve') {
            score -= 15;
            reasons.push('Ligera postergación de actividades.');
        }

        // 2. Control Autopercibido (30%)
        if (current.control === 'bajo') {
            score -= 30;
            reasons.push('Dificultad o falta de control para posponer el impulso.');
        } else if (current.control === 'medio') {
            score -= 10;
        }

        // 3. Síntomas Físicos (25%)
        if (current.sintomas === 'moderado_severo') {
            score -= 25;
            reasons.push('Presencia de dolor o irritación física notoria.');
        } else if (current.sintomas === 'leve') {
            score -= 15;
            reasons.push('Leve molestia o sensibilidad incrementada.');
        }

        // 4. Estrés Previo (15%)
        if (current.estres === 'alto') {
            score -= 12;
            reasons.push('Estrés elevado como detonante de la conducta.');
        }

        // 5. Intervalo desde el último evento
        if (pastEvents && pastEvents.length > 0) {
            const lastDate = new Date(pastEvents[0].date);
            const curDate = new Date(current.date);
            const diffHours = (curDate - lastDate) / (1000 * 60 * 60);

            if (diffHours >= 0 && diffHours < 12) {
                score -= 15;
                reasons.push('Intervalo muy corto (<12h) desde el registro anterior.');
            } else if (diffHours >= 0 && diffHours < 24) {
                score -= 8;
            }
        }

        score = Math.max(0, Math.min(100, Math.round(score)));

        let color = 'green';
        if (score < 40 || current.interferencia === 'severa' || current.sintomas === 'moderado_severo') {
            color = 'red';
        } else if (score < 70 || current.interferencia === 'leve' || current.control === 'medio') {
            color = 'yellow';
        }

        let explicacion = reasons.length > 0 
            ? reasons.join(' ')
            : 'Patrón saludable con preservación plena del bienestar.';

        return { score, color, explicacion };
    },

    generatePredictiveCalendar(year, month) {
        // month es 1-indexed (1 = Enero, 10 = Octubre)
        const daysInMonth = new Date(year, month, 0).getDate();
        const firstDay = new Date(year, month - 1, 1);
        let startDayIndex = firstDay.getDay() - 1;
        if (startDayIndex === -1) startDayIndex = 6;

        const allEvents = this.getEvents();
        // Ordenar cronológicamente (más antiguo al más reciente)
        const sortedEvents = [...allEvents].sort((a, b) => new Date(a.date) - new Date(b.date));

        // Mapear eventos por fecha YYYY-MM-DD
        const mapEventsByDate = {};
        allEvents.forEach(e => {
            const dateStr = e.date.split('T')[0];
            if (!mapEventsByDate[dateStr]) mapEventsByDate[dateStr] = [];
            mapEventsByDate[dateStr].push(e);
        });

        // Buscar el último evento registrado en todo el historial
        const latestEvent = sortedEvents.length > 0 ? sortedEvents[sortedEvents.length - 1] : null;
        const latestEventDt = latestEvent ? new Date(latestEvent.date) : null;

        const dias = [];
        const resumen = { Verde: 0, Amarillo: 0, Naranja: 0, Rojo: 0 };

        for (let day = 1; day <= daysInMonth; day++) {
            const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            const dayEvents = mapEventsByDate[dateStr] || [];
            const tiene_registro = dayEvents.length > 0;
            const targetDate = new Date(`${dateStr}T12:00:00`);

            const es_futuro = latestEventDt ? (targetDate > latestEventDt && !tiene_registro) : (!tiene_registro);

            let nivel = 'Verde';
            let prob = 0.12;
            let conf = 0.85;
            let motivos = [];
            let recomendacion = 'Día favorable para mantener tu autorregulación y bienestar general.';

            if (tiene_registro) {
                // ==========================================
                // 1. DÍA CON EVENTO(S) REAL(ES) REGISTRADO(S)
                // ==========================================
                const totalEv = dayEvents.length;
                const tieneDolor = dayEvents.some(e => e.sintomas === 'moderado_severo' || e.sintomas === 'dolor');
                const tieneSintomaLeve = dayEvents.some(e => e.sintomas === 'leve');
                const tieneInterfSevera = dayEvents.some(e => e.interferencia === 'severa');
                const tieneInterfLeve = dayEvents.some(e => e.interferencia === 'leve');
                const bajoControl = dayEvents.some(e => e.control === 'bajo');
                const controlMedio = dayEvents.some(e => e.control === 'medio');

                if (tieneDolor || totalEv >= 3 || (bajoControl && tieneInterfSevera)) {
                    nivel = 'Rojo';
                    prob = 0.88;
                    conf = 0.95;
                    motivos = [
                        `Día con ${totalEv} evento(s) registrado(s).`,
                        totalEv >= 3 ? 'Alta cadencia concentrada (3+ eventos en el mismo día).' : 'Presencia de dolor o irritación física.',
                        'Interferencia relevante con descanso u obligaciones cotidianas.'
                    ];
                    recomendacion = 'Día no recomendable para repetir la conducta. Se requiere pausa biológica obligatoria.';
                } else if (totalEv === 2 || bajoControl || tieneInterfSevera) {
                    nivel = 'Naranja';
                    prob = 0.64;
                    conf = 0.92;
                    motivos = [
                        `Día con ${totalEv} evento(s) registrado(s).`,
                        totalEv === 2 ? '2 eventos en la misma jornada; descanso acortado.' : 'Percepción de dificultad para posponer el impulso.',
                        'Interferencia funcional moderada.'
                    ];
                    recomendacion = 'Atención sugerida. Considera pausas activas o posponer el impulso si detectas escape ansioso.';
                } else if (tieneInterfLeve || controlMedio || tieneSintomaLeve || dayEvents.some(e => e.estres === 'alto')) {
                    nivel = 'Amarillo';
                    prob = 0.38;
                    conf = 0.90;
                    motivos = [
                        `Día con ${totalEv} evento(s) registrado(s).`,
                        'Estrés previo o menor descanso entre eventos.'
                    ];
                    recomendacion = 'Observa tu patrón de conducta antes de actuar y verifica tu nivel de cansancio.';
                } else {
                    nivel = 'Verde';
                    prob = 0.12;
                    conf = 0.92;
                    motivos = [
                        `Día con ${totalEv} evento(s) registrado(s) con buen autocontrol y sin interferencia.`
                    ];
                    recomendacion = 'Registro armónico: autorregulación óptima y sin impacto adverso.';
                }
            } else {
                // ==========================================
                // 2. DÍA SIN REGISTRO: PREDICCIÓN REACTIVA IA
                // ==========================================
                if (!latestEventDt) {
                    nivel = 'Verde';
                    prob = 0.12;
                    conf = 0.75;
                    motivos = ['Sin eventos previos registrados. Patrón basal en equilibrio.'];
                    recomendacion = 'Comienza registrando tus hábitos para personalizar el modelo de IA.';
                } else {
                    const diffHours = (targetDate - latestEventDt) / (1000 * 60 * 60);

                    if (diffHours < 0) {
                        // Día del pasado sin eventos: fue un día de descanso exitoso
                        nivel = 'Verde';
                        prob = 0.08;
                        conf = 0.90;
                        motivos = ['Día sin eventos registrados en tu historial. Pausa biológica exitosa.'];
                        recomendacion = 'Excelente jornada de descanso y autorregulación conservada.';
                    } else {
                        // DÍA FUTURO REACTIVO: reacciona dinámicamente al último evento
                        const lastDateStr = latestEvent.date.split('T')[0];
                        const eventsLastDay = mapEventsByDate[lastDateStr] || [latestEvent];
                        const countLastDay = eventsLastDay.length;
                        const hadPainLastDay = eventsLastDay.some(e => e.sintomas === 'moderado_severo');
                        const hadLowControlLastDay = eventsLastDay.some(e => e.control === 'bajo');

                        const sevenDaysBeforeTarget = new Date(targetDate.getTime() - (7 * 24 * 60 * 60 * 1000));
                        const eventsIn7d = sortedEvents.filter(e => {
                            const d = new Date(e.date);
                            return d <= targetDate && d >= sevenDaysBeforeTarget;
                        }).length;

                        // CASO A: Sobrecarga aguda previa (3+ eventos o dolor/irritación)
                        if (countLastDay >= 3 || hadPainLastDay) {
                            if (diffHours < 36) {
                                nivel = 'Rojo';
                                prob = 0.85;
                                conf = 0.88;
                                motivos = [
                                    `${countLastDay} eventos registrados en la jornada previa reciente.`,
                                    'Alta fatiga física y neuronal; riesgo elevado de desregulación.',
                                    `Apenas ${Math.max(1, Math.round(diffHours))}h de recuperación transcurridas.`
                                ];
                                recomendacion = 'Día NO recomendable para realizar el hábito. Necesidad prioritaria de descanso biológico.';
                            } else if (diffHours < 60) {
                                nivel = 'Naranja';
                                prob = 0.62;
                                conf = 0.85;
                                motivos = [
                                    `Fase intermedia de recuperación (${Math.round(diffHours)}h de descanso acumuladas tras sobrecarga).`,
                                    'Historial reciente que aún requiere consolidación de descanso.'
                                ];
                                recomendacion = 'Mantén la pausa activa para permitir la restauración del control biológico.';
                            } else if (diffHours < 84) {
                                nivel = 'Amarillo';
                                prob = 0.38;
                                conf = 0.82;
                                motivos = [
                                    `Transición favorable hacia el restablecimiento del balance (${Math.round(diffHours)}h de descanso).`
                                ];
                                recomendacion = 'Observa tus impulsos y confirma que no haya tensión residual antes de actuar.';
                            } else {
                                nivel = 'Verde';
                                prob = 0.12;
                                conf = 0.85;
                                motivos = [
                                    `Intervalo de descanso biológico restaurado plenamente (> 72h).`,
                                    'Bajo riesgo de desregulación proyectado.'
                                ];
                                recomendacion = 'Día favorable para la autorregulación consciente y bienestar general.';
                            }
                        }
                        // CASO B: Cadencia previa de 2 eventos en un día o pérdida de control
                        else if (countLastDay === 2 || hadLowControlLastDay) {
                            if (diffHours < 28) {
                                nivel = 'Naranja';
                                prob = 0.60;
                                conf = 0.84;
                                motivos = [
                                    countLastDay === 2 ? '2 eventos registrados en la jornada previa reciente.' : 'Bajo autocontrol registrado en el último evento.',
                                    `Descanso insuficiente (${Math.max(1, Math.round(diffHours))}h desde el último evento).`
                                ];
                                recomendacion = 'Conviene posponer la conducta y consolidar el descanso biológico.';
                            } else if (diffHours < 52) {
                                nivel = 'Amarillo';
                                prob = 0.38;
                                conf = 0.82;
                                motivos = [
                                    `Fase de estabilización de cadencia (${Math.round(diffHours)}h de descanso transcurridas).`
                                ];
                                recomendacion = 'Observa el contexto ambiental y evita el aburrimiento como detonante.';
                            } else {
                                nivel = 'Verde';
                                prob = 0.12;
                                conf = 0.85;
                                motivos = [
                                    `Descanso biológico suficiente (> 48 horas acumuladas).`,
                                    'Patrón compatible con bienestar personal.'
                                ];
                                recomendacion = 'Día favorable para mantener tu autorregulación y bienestar general.';
                            }
                        }
                        // CASO C: 1 evento previo con buen control
                        else {
                            if (diffHours < 24) {
                                nivel = 'Amarillo';
                                prob = 0.35;
                                conf = 0.80;
                                motivos = [
                                    `Menor tiempo de descanso transcurrido (${Math.max(1, Math.round(diffHours))}h desde el último registro).`,
                                    'Mantener vigilancia en contextos de ocio o fatiga nocturna.'
                                ];
                                recomendacion = 'Observa tu nivel de cansancio o estrés antes de actuar.';
                            } else {
                                nivel = 'Verde';
                                prob = 0.12;
                                conf = 0.86;
                                motivos = [
                                    `Descanso biológico adecuado (> 24h transcurridas).`,
                                    eventsIn7d > 4 ? 'Vigilar acumulación semanal.' : 'Patrón de bajo riesgo según tu historial.'
                                ];
                                recomendacion = 'Día altamente favorable para tu bienestar y autorregulación.';
                            }
                        }
                    }
                }
            }

            resumen[nivel]++;
            dias.push({
                dia: day,
                fecha: dateStr,
                nivel: nivel,
                probabilidad: prob,
                probabilidad_pct: `${Math.round(prob * 100)}%`,
                confianza_pct: `${Math.round(conf * 100)}%`,
                tiene_registro: tiene_registro,
                total_eventos_dia: dayEvents.length,
                eventos_detalle: dayEvents,
                es_futuro: es_futuro,
                explicacion_principal: nivel === 'Rojo' 
                    ? 'El modelo estima una mayor probabilidad de desregulación o fatiga respecto a tu patrón habitual.'
                    : (nivel === 'Naranja' ? 'Varios indicadores de tu historial apuntan a posible pérdida de control o sobrecarga.' : (nivel === 'Amarillo' ? 'Se observa una posible tendencia o menor descanso que conviene vigilar.' : 'Tu historial muestra señales de balance y óptima autorregulación.')),
                factores_detectados: motivos.length > 0 ? motivos : ['Patrón de bajo riesgo según tu historial personal y datos NSSHB.'],
                recomendacion: recomendacion,
                disclaimer: 'Esta predicción se basa en tu historial personal y en la información científica disponible. No constituye un diagnóstico médico.'
            });
        }

        return {
            año: year,
            mes: month,
            primer_dia_semana: startDayIndex,
            total_dias: daysInMonth,
            resumen_estados: resumen,
            dias: dias
        };
    }
};

window.StorageService = StorageService;
StorageService.init();

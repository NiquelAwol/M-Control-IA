/**
 * M-Control: Módulo de Almacenamiento Local y Algoritmo de Bienestar
 * Basado en la investigación científica y conceptual de M-Control (2026)
 * Incluye soporte para el Calendario Predictivo Inteligente de 4 Estados (CIE-11 CSBD, NSSHB)
 */

const STORAGE_KEY_EVENTS = 'mcontrol_events_data';
const STORAGE_KEY_SETTINGS = 'mcontrol_user_settings';
const STORAGE_KEY_ACTIVE_USER = 'mcontrol_active_user_id';
const STORAGE_KEY_USERS_LIST = 'mcontrol_users_list';
const STORAGE_KEY_USER_EVENTS_PREFIX = 'mcontrol_events_user_';
const STORAGE_KEY_USER_SETTINGS_PREFIX = 'mcontrol_settings_user_';
const STORAGE_KEY_AUTH_SESSION = 'mcontrol_session_auth';

const DEFAULT_USERS = [
    { id: 5, alias: 'admin', edad: 24, objetivo: 'Administración del Sistema', pin: 'admin2026', rol: 'admin', fecha: '2026-07-01' },
    { id: 1, alias: 'Participante 1', edad: 24, objetivo: 'Autorregulación y Bienestar', pin: '1234', rol: 'participante', fecha: '2026-07-01' },
    { id: 2, alias: 'Participante 2', edad: 21, objetivo: 'Reducir Frecuencia y Mejorar Sueño', pin: '1234', rol: 'participante', fecha: '2026-07-01' },
    { id: 3, alias: 'Participante 3', edad: 28, objetivo: 'Observar Patrones de Estrés', pin: '1234', rol: 'participante', fecha: '2026-07-01' },
    { id: 4, alias: 'Tester_05', edad: 26, objetivo: 'autorregulacion', pin: '1234', rol: 'participante', fecha: '2026-07-01' },
    { id: 6, alias: 'Raul', edad: 27, objetivo: 'Autorregulación Deportiva y Rendimiento Físico', pin: '1234', rol: 'participante', fecha: '2026-07-01' },
    { id: 7, alias: 'Roberto', edad: 22, objetivo: 'Manejo de Ansiedad Académica y Calidad de Sueño', pin: '1234', rol: 'participante', fecha: '2026-07-01' },
    { id: 8, alias: 'Juan', edad: 31, objetivo: 'Reducción de Fatiga Sedentaria y Salud Ocupacional', pin: '1234', rol: 'participante', fecha: '2026-07-01' }
];

// Catálogo longitudinal completo por participante sincronizado con SQLite mcontrol_ai.db (126 registros)
const DEFAULT_EVENTS_BY_USER = {
    "1": [
        {
            "id": "evt-1-48",
            "date": "2026-10-03T19:00",
            "control": "medio",
            "interferencia": "leve",
            "sintomas": "ninguno",
            "estres": "alto",
            "porno": true,
            "notas": "Fin de semana acelerado",
            "score": 55,
            "color": "yellow",
            "explicacion": "Ligera postergación de actividades. Estrés elevado como detonante de la conducta.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-47",
            "date": "2026-10-02T23:15",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Día de trabajo normal",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-46",
            "date": "2026-10-01T22:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Pausa previa de 9 días",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-45",
            "date": "2026-09-21T21:30",
            "control": "bajo",
            "interferencia": "severa",
            "sintomas": "moderado_severo",
            "estres": "bajo",
            "porno": true,
            "notas": "Reiteración en mismo día",
            "score": 0,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Dificultad o falta de control para posponer el impulso. Presencia de dolor o irritación física notoria. Intervalo muy corto (<12h) desde el registro anterior.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-44",
            "date": "2026-09-21T14:00",
            "control": "bajo",
            "interferencia": "severa",
            "sintomas": "moderado_severo",
            "estres": "bajo",
            "porno": true,
            "notas": "Interferencia leve en jornada",
            "score": 2,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Dificultad o falta de control para posponer el impulso. Presencia de dolor o irritación física notoria.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-43",
            "date": "2026-09-20T23:20",
            "control": "medio",
            "interferencia": "leve",
            "sintomas": "ninguno",
            "estres": "alto",
            "porno": true,
            "notas": "Tensión laboral",
            "score": 63,
            "color": "yellow",
            "explicacion": "Ligera postergación de actividades. Estrés elevado como detonante de la conducta.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-42",
            "date": "2026-09-19T16:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Normal",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-41",
            "date": "2026-09-17T22:50",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Normal",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-40",
            "date": "2026-09-15T19:40",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Control excelente",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-39",
            "date": "2026-09-12T21:15",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Pausa de recuperación de 60h",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-38",
            "date": "2026-09-10T08:30",
            "control": "bajo",
            "interferencia": "severa",
            "sintomas": "moderado_severo",
            "estres": "bajo",
            "porno": true,
            "notas": "Repetición matutina impulsiva",
            "score": 0,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Dificultad o falta de control para posponer el impulso. Presencia de dolor o irritación física notoria. Intervalo muy corto (<12h) desde el registro anterior.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-37",
            "date": "2026-09-09T23:55",
            "control": "bajo",
            "interferencia": "severa",
            "sintomas": "moderado_severo",
            "estres": "alto",
            "porno": true,
            "notas": "Dificultad para conciliar sueño",
            "score": 0,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Dificultad o falta de control para posponer el impulso. Presencia de dolor o irritación física notoria. Estrés elevado como detonante de la conducta.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-36",
            "date": "2026-09-08T14:30",
            "control": "medio",
            "interferencia": "leve",
            "sintomas": "ninguno",
            "estres": "alto",
            "porno": true,
            "notas": "Día pesado en la universidad",
            "score": 63,
            "color": "yellow",
            "explicacion": "Ligera postergación de actividades. Estrés elevado como detonante de la conducta.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-35",
            "date": "2026-09-06T20:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Normal",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-34",
            "date": "2026-09-04T23:10",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Buen descanso",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-33",
            "date": "2026-09-02T18:20",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Normal",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-32",
            "date": "2026-08-31T22:40",
            "control": "medio",
            "interferencia": "leve",
            "sintomas": "ninguno",
            "estres": "alto",
            "porno": true,
            "notas": "Preocupación académica",
            "score": 63,
            "color": "yellow",
            "explicacion": "Ligera postergación de actividades. Estrés elevado como detonante de la conducta.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-31",
            "date": "2026-08-30T11:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Fin de semana regulado",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-30",
            "date": "2026-08-28T17:15",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Normal",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-29",
            "date": "2026-08-26T23:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "medio",
            "porno": true,
            "notas": "Normal",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-28",
            "date": "2026-08-24T19:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Equilibrio",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-27",
            "date": "2026-08-21T21:10",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Equilibrio",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-26",
            "date": "2026-08-18T16:45",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Pausa biológica de 79 horas",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-25",
            "date": "2026-08-15T09:00",
            "control": "bajo",
            "interferencia": "severa",
            "sintomas": "moderado_severo",
            "estres": "bajo",
            "porno": true,
            "notas": "Fuerte dolor e irritación",
            "score": 0,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Dificultad o falta de control para posponer el impulso. Presencia de dolor o irritación física notoria. Intervalo muy corto (<12h) desde el registro anterior.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-24",
            "date": "2026-08-15T01:20",
            "control": "bajo",
            "interferencia": "severa",
            "sintomas": "moderado_severo",
            "estres": "alto",
            "porno": true,
            "notas": "Madrugada en pantalla",
            "score": 0,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Dificultad o falta de control para posponer el impulso. Presencia de dolor o irritación física notoria. Estrés elevado como detonante de la conducta.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-23",
            "date": "2026-08-13T14:00",
            "control": "medio",
            "interferencia": "leve",
            "sintomas": "ninguno",
            "estres": "medio",
            "porno": true,
            "notas": "Afectó avance de estudio",
            "score": 75,
            "color": "yellow",
            "explicacion": "Ligera postergación de actividades.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-22",
            "date": "2026-08-11T23:15",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "alto",
            "porno": true,
            "notas": "Normal",
            "score": 88,
            "color": "green",
            "explicacion": "Estrés elevado como detonante de la conducta.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-21",
            "date": "2026-08-09T18:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Buen ritmo",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-20",
            "date": "2026-08-06T22:45",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Descanso de 72h óptimo",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-19",
            "date": "2026-08-03T20:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Recuperación de autocontrol",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-18",
            "date": "2026-08-01T11:30",
            "control": "bajo",
            "interferencia": "severa",
            "sintomas": "moderado_severo",
            "estres": "bajo",
            "porno": true,
            "notas": "Doble evento en menos de 14h",
            "score": 2,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Dificultad o falta de control para posponer el impulso. Presencia de dolor o irritación física notoria.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-17",
            "date": "2026-07-31T23:00",
            "control": "medio",
            "interferencia": "leve",
            "sintomas": "ninguno",
            "estres": "alto",
            "porno": true,
            "notas": "Cierre de mes laboral",
            "score": 63,
            "color": "yellow",
            "explicacion": "Ligera postergación de actividades. Estrés elevado como detonante de la conducta.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-16",
            "date": "2026-07-30T08:20",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Normal",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-15",
            "date": "2026-07-28T21:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Excelente control",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-14",
            "date": "2026-07-26T12:10",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Normal",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-13",
            "date": "2026-07-24T23:50",
            "control": "medio",
            "interferencia": "leve",
            "sintomas": "ninguno",
            "estres": "alto",
            "porno": true,
            "notas": "Desvelo",
            "score": 63,
            "color": "yellow",
            "explicacion": "Ligera postergación de actividades. Estrés elevado como detonante de la conducta.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-12",
            "date": "2026-07-22T17:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Control adecuado",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-11",
            "date": "2026-07-20T20:40",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "alto",
            "porno": true,
            "notas": "Presión de entrega",
            "score": 88,
            "color": "green",
            "explicacion": "Estrés elevado como detonante de la conducta.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-10",
            "date": "2026-07-18T22:15",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "medio",
            "porno": true,
            "notas": "Ayudó a conciliar sueño",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-9",
            "date": "2026-07-16T09:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Buen inicio de día",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-8",
            "date": "2026-07-13T18:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Recuperación tras descanso de 3 días",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-7",
            "date": "2026-07-10T23:10",
            "control": "bajo",
            "interferencia": "severa",
            "sintomas": "moderado_severo",
            "estres": "bajo",
            "porno": true,
            "notas": "Sensación de culpa y molestia",
            "score": 0,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Dificultad o falta de control para posponer el impulso. Presencia de dolor o irritación física notoria. Intervalo muy corto (<12h) desde el registro anterior.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-6",
            "date": "2026-07-10T14:30",
            "control": "bajo",
            "interferencia": "severa",
            "sintomas": "leve",
            "estres": "alto",
            "porno": true,
            "notas": "Postergación de estudio",
            "score": 0,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Dificultad o falta de control para posponer el impulso. Leve molestia o sensibilidad incrementada. Estrés elevado como detonante de la conducta.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-5",
            "date": "2026-07-09T21:00",
            "control": "medio",
            "interferencia": "leve",
            "sintomas": "ninguno",
            "estres": "alto",
            "porno": true,
            "notas": "Preocupación laboral",
            "score": 63,
            "color": "yellow",
            "explicacion": "Ligera postergación de actividades. Estrés elevado como detonante de la conducta.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-4",
            "date": "2026-07-08T19:20",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Normal",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-3",
            "date": "2026-07-06T23:45",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "alto",
            "porno": true,
            "notas": "Cansancio tras jornada",
            "score": 88,
            "color": "green",
            "explicacion": "Estrés elevado como detonante de la conducta.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-2",
            "date": "2026-07-04T10:15",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Fin de semana",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        },
        {
            "id": "evt-1-1",
            "date": "2026-07-01T22:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Día tranquilo de descanso",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 1
        }
    ],
    "2": [
        {
            "id": "evt-2-50",
            "date": "2026-10-04T10:00",
            "control": "bajo",
            "interferencia": "severa",
            "sintomas": "moderado_severo",
            "estres": "alto",
            "porno": true,
            "notas": "Sobrecarga de trabajo",
            "score": 0,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Dificultad o falta de control para posponer el impulso. Presencia de dolor o irritación física notoria. Estrés elevado como detonante de la conducta.",
            "usuario_id": 2
        }
    ],
    "3": [],
    "4": [],
    "5": [],
    "6": [
        {
            "id": "evt-6-74",
            "date": "2026-10-16T21:45",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Hábito plenamente autorregulado",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-73",
            "date": "2026-10-11T20:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Cero molestias físicas",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-72",
            "date": "2026-10-06T21:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Intervalo saludable de 96h",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-71",
            "date": "2026-10-02T22:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Inicio de mes con metas claras",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-70",
            "date": "2026-09-28T20:45",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Equilibrio total",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-69",
            "date": "2026-09-23T21:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Recuperación de 5 días",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-68",
            "date": "2026-09-18T19:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "alto",
            "porno": true,
            "notas": "Cansancio acumulado de trabajo y pesas",
            "score": 88,
            "color": "green",
            "explicacion": "Estrés elevado como detonante de la conducta.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-67",
            "date": "2026-09-14T22:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Normal",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-66",
            "date": "2026-09-09T20:15",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Sin interferencia en rendimiento",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-65",
            "date": "2026-09-04T21:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Ritmo constante de 96 horas",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-64",
            "date": "2026-08-30T22:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Control sostenido",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-63",
            "date": "2026-08-25T20:45",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Recuperación post-competencia",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-62",
            "date": "2026-08-20T21:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "alto",
            "porno": true,
            "notas": "Semana previa a torneo de atletismo",
            "score": 88,
            "color": "green",
            "explicacion": "Estrés elevado como detonante de la conducta.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-61",
            "date": "2026-08-15T22:15",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Bienestar preservado",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-60",
            "date": "2026-08-10T20:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Pausa de 5 días completa",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-59",
            "date": "2026-08-05T21:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Excelente disciplina biológica",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-58",
            "date": "2026-07-31T22:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Cierre de mes en perfecto balance",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-57",
            "date": "2026-07-26T21:45",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Intervalo amplio de 96 horas",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-56",
            "date": "2026-07-22T22:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "medio",
            "porno": true,
            "notas": "Fatiga muscular normal post-gimnasio",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-55",
            "date": "2026-07-18T20:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Control absoluto y bienestar físico",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-54",
            "date": "2026-07-14T21:15",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Normal tras jornada deportiva",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-53",
            "date": "2026-07-10T22:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Intervalo de 96 horas, óptimo control",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-52",
            "date": "2026-07-06T20:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Fin de semana tranquilo, excelente recuperación",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        },
        {
            "id": "evt-6-51",
            "date": "2026-07-02T21:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Descanso de 72h tras entrenamiento de fuerza",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 6
        }
    ],
    "7": [
        {
            "id": "evt-7-100",
            "date": "2026-10-07T21:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Semana sin evaluaciones, equilibrio",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-99",
            "date": "2026-10-01T22:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Inicio de mes tranquilo",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-98",
            "date": "2026-09-26T23:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Normal",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-97",
            "date": "2026-09-21T21:15",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Control retomado",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-96",
            "date": "2026-09-16T22:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Recuperación de 79h",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-95",
            "date": "2026-09-13T15:00",
            "control": "bajo",
            "interferencia": "severa",
            "sintomas": "moderado_severo",
            "estres": "bajo",
            "porno": true,
            "notas": "Sobrecarga de trabajo",
            "score": 10,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Dificultad o falta de control para posponer el impulso. Presencia de dolor o irritación física notoria.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-94",
            "date": "2026-09-12T01:30",
            "control": "bajo",
            "interferencia": "severa",
            "sintomas": "leve",
            "estres": "alto",
            "porno": true,
            "notas": "Entrega de proyecto final de programación",
            "score": 8,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Dificultad o falta de control para posponer el impulso. Leve molestia o sensibilidad incrementada. Estrés elevado como detonante de la conducta.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-93",
            "date": "2026-09-08T22:45",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Descanso adecuado",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-92",
            "date": "2026-09-03T21:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Normal",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-91",
            "date": "2026-08-29T23:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Buen descanso",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-90",
            "date": "2026-08-24T21:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Normal",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-89",
            "date": "2026-08-20T22:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Retoma control",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-88",
            "date": "2026-08-16T21:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Pausa biológica de 4 días completa",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-87",
            "date": "2026-08-12T11:30",
            "control": "bajo",
            "interferencia": "severa",
            "sintomas": "moderado_severo",
            "estres": "bajo",
            "porno": true,
            "notas": "Repetición matutina en menos de 10 horas",
            "score": 0,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Dificultad o falta de control para posponer el impulso. Presencia de dolor o irritación física notoria. Intervalo muy corto (<12h) desde el registro anterior.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-86",
            "date": "2026-08-12T02:10",
            "control": "bajo",
            "interferencia": "severa",
            "sintomas": "moderado_severo",
            "estres": "alto",
            "porno": true,
            "notas": "Semana de segundo parcial, insomnio y estrés",
            "score": 0,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Dificultad o falta de control para posponer el impulso. Presencia de dolor o irritación física notoria. Estrés elevado como detonante de la conducta.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-85",
            "date": "2026-08-08T23:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Descanso de 96 horas",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-84",
            "date": "2026-08-04T22:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Normal",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-83",
            "date": "2026-07-31T20:45",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Fin de mes académico",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-82",
            "date": "2026-07-27T23:15",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Ritmo regulado",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-81",
            "date": "2026-07-23T21:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Normal",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-80",
            "date": "2026-07-19T22:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Pausa de recuperación de 4 días",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-79",
            "date": "2026-07-15T14:20",
            "control": "bajo",
            "interferencia": "severa",
            "sintomas": "moderado_severo",
            "estres": "bajo",
            "porno": true,
            "notas": "Ráfaga impulsiva post-examen, culpa",
            "score": 2,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Dificultad o falta de control para posponer el impulso. Presencia de dolor o irritación física notoria.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-78",
            "date": "2026-07-15T01:45",
            "control": "medio",
            "interferencia": "severa",
            "sintomas": "leve",
            "estres": "alto",
            "porno": true,
            "notas": "Desvelo preparando parcial de cálculo",
            "score": 28,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Leve molestia o sensibilidad incrementada. Estrés elevado como detonante de la conducta.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-77",
            "date": "2026-07-11T20:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Fin de semana tranquilo",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-76",
            "date": "2026-07-07T22:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Estudio al día",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        },
        {
            "id": "evt-7-75",
            "date": "2026-07-03T23:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Semana normal de clases",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 7
        }
    ],
    "8": [
        {
            "id": "evt-8-127",
            "date": "2026-10-15T21:15",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Salud física y mental óptima",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-126",
            "date": "2026-10-10T22:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Intervalo de 120h",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-125",
            "date": "2026-10-05T21:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Estilo de vida saludable consolidado",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-124",
            "date": "2026-09-30T22:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Mes de septiembre completamente verde",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-123",
            "date": "2026-09-25T21:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Buen descanso",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-122",
            "date": "2026-09-20T22:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Normal",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-121",
            "date": "2026-09-15T21:15",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Control total",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-120",
            "date": "2026-09-10T22:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": false,
            "notas": "Cero dolor y cero irritación",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-119",
            "date": "2026-09-05T21:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Intervalo de 120 horas",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-118",
            "date": "2026-08-31T22:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Cierre de agosto con mejoría notable",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-117",
            "date": "2026-08-26T21:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Excelente nivel de energía",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-116",
            "date": "2026-08-21T22:15",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Autocontrol afianzado",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-115",
            "date": "2026-08-16T21:45",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Pausa de 5 días completa",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-114",
            "date": "2026-08-11T23:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "alto",
            "porno": true,
            "notas": "Sin interferencia en trabajo",
            "score": 88,
            "color": "green",
            "explicacion": "Estrés elevado como detonante de la conducta.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-113",
            "date": "2026-08-06T21:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Descanso de 96h sostenido",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-112",
            "date": "2026-08-02T22:00",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Implementa pausas activas cada 2 horas",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-111",
            "date": "2026-07-28T21:15",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Intervalo de 96h",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-110",
            "date": "2026-07-24T23:00",
            "control": "medio",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "alto",
            "porno": true,
            "notas": "Normal",
            "score": 78,
            "color": "yellow",
            "explicacion": "Estrés elevado como detonante de la conducta.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-109",
            "date": "2026-07-20T21:30",
            "control": "alto",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Pausa de 96 horas, gran mejoría física",
            "score": 100,
            "color": "green",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-108",
            "date": "2026-07-16T22:00",
            "control": "medio",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "bajo",
            "porno": true,
            "notas": "Comienza a leer guías médicas de M-Control",
            "score": 90,
            "color": "yellow",
            "explicacion": "Patrón saludable con preservación plena del bienestar.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-107",
            "date": "2026-07-13T23:45",
            "control": "medio",
            "interferencia": "severa",
            "sintomas": "leve",
            "estres": "bajo",
            "porno": true,
            "notas": "Fatiga laboral",
            "score": 40,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Leve molestia o sensibilidad incrementada.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-106",
            "date": "2026-07-10T21:00",
            "control": "medio",
            "interferencia": "ninguna",
            "sintomas": "ninguno",
            "estres": "alto",
            "porno": true,
            "notas": "Pausa de 3 días que alivió irritación",
            "score": 78,
            "color": "yellow",
            "explicacion": "Estrés elevado como detonante de la conducta.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-105",
            "date": "2026-07-07T11:30",
            "control": "bajo",
            "interferencia": "severa",
            "sintomas": "moderado_severo",
            "estres": "bajo",
            "porno": true,
            "notas": "Sensación de bajo control e irritación física",
            "score": 0,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Dificultad o falta de control para posponer el impulso. Presencia de dolor o irritación física notoria. Intervalo muy corto (<12h) desde el registro anterior.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-104",
            "date": "2026-07-07T01:00",
            "control": "bajo",
            "interferencia": "severa",
            "sintomas": "moderado_severo",
            "estres": "bajo",
            "porno": true,
            "notas": "Desvelo nocturno por caída de servidor",
            "score": 10,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Dificultad o falta de control para posponer el impulso. Presencia de dolor o irritación física notoria.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-103",
            "date": "2026-07-05T22:15",
            "control": "medio",
            "interferencia": "leve",
            "sintomas": "leve",
            "estres": "medio",
            "porno": true,
            "notas": "Dolor de espalda y vista cansada",
            "score": 60,
            "color": "yellow",
            "explicacion": "Ligera postergación de actividades. Leve molestia o sensibilidad incrementada.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-102",
            "date": "2026-07-03T15:00",
            "control": "bajo",
            "interferencia": "leve",
            "sintomas": "moderado_severo",
            "estres": "bajo",
            "porno": true,
            "notas": "Intervalo menor a 16 horas, escape ante sprint",
            "score": 22,
            "color": "red",
            "explicacion": "Ligera postergación de actividades. Dificultad o falta de control para posponer el impulso. Presencia de dolor o irritación física notoria.",
            "usuario_id": 8
        },
        {
            "id": "evt-8-101",
            "date": "2026-07-02T23:30",
            "control": "bajo",
            "interferencia": "severa",
            "sintomas": "leve",
            "estres": "alto",
            "porno": true,
            "notas": "Día pesado de programación frente a pantalla",
            "score": 8,
            "color": "red",
            "explicacion": "Interferencia significativa en trabajo, estudio o descanso. Dificultad o falta de control para posponer el impulso. Leve molestia o sensibilidad incrementada. Estrés elevado como detonante de la conducta.",
            "usuario_id": 8
        }
    ]
};

// Para compatibilidad previa
const DEFAULT_EVENTS = DEFAULT_EVENTS_BY_USER['1'] || [];

const DEFAULT_SETTINGS = {
    objetivo: 'autorregulacion',
    edad: 24,
    modoAnonimo: false,
    alertaSintomas: true
};

const StorageService = {
    init() {
        // 1. Inicializar lista de usuarios / participantes y garantizar sincronía con SQLite
        let storedUsers = [];
        try {
            storedUsers = JSON.parse(localStorage.getItem(STORAGE_KEY_USERS_LIST)) || [];
        } catch (e) {
            storedUsers = [];
        }
        const adminUser = storedUsers.find(u => (u.alias || '').toLowerCase() === 'admin');
        if (!storedUsers.length || (adminUser && adminUser.id === 1)) {
            storedUsers = [...DEFAULT_USERS];
            localStorage.setItem(STORAGE_KEY_USERS_LIST, JSON.stringify(storedUsers));
        } else {
            const hasAdmin = storedUsers.some(u => (u.alias || '').toLowerCase() === 'admin');
            if (!hasAdmin) {
                storedUsers.unshift({ id: 5, alias: 'admin', edad: 24, objetivo: 'Administración del Sistema', pin: 'admin2026', rol: 'admin', fecha: '2026-07-01' });
            }
            let updated = false;
            storedUsers.forEach(u => {
                if (u.id === 6 || (u.alias || '').toLowerCase() === 'participante4') { u.alias = 'Raul'; updated = true; }
                if (u.id === 7 || (u.alias || '').toLowerCase() === 'participante5') { u.alias = 'Roberto'; updated = true; }
                if (u.id === 8 || (u.alias || '').toLowerCase() === 'participante6') { u.alias = 'Juan'; updated = true; }
            });
            if (updated || !hasAdmin) {
                localStorage.setItem(STORAGE_KEY_USERS_LIST, JSON.stringify(storedUsers));
            }
        }

        // 2. Participante activo por defecto: 1 (Participante 1 con 48 eventos)
        if (!localStorage.getItem(STORAGE_KEY_ACTIVE_USER)) {
            localStorage.setItem(STORAGE_KEY_ACTIVE_USER, '1');
        }

        // 3. Inicializar historial de eventos por usuario con los 126 registros longitudinales de la BD
        if (typeof DEFAULT_EVENTS_BY_USER !== 'undefined') {
            Object.keys(DEFAULT_EVENTS_BY_USER).forEach(uid => {
                const userKey = STORAGE_KEY_USER_EVENTS_PREFIX + uid;
                const existing = localStorage.getItem(userKey);
                const defaultCount = (DEFAULT_EVENTS_BY_USER[uid] || []).length;
                if (!existing || JSON.parse(existing || '[]').length < defaultCount) {
                    localStorage.setItem(userKey, JSON.stringify(DEFAULT_EVENTS_BY_USER[uid]));
                    if (uid === '1') {
                        localStorage.setItem(STORAGE_KEY_EVENTS, JSON.stringify(DEFAULT_EVENTS_BY_USER[uid]));
                    }
                }
            });
        }

        // 4. Configuración inicial
        if (!localStorage.getItem(STORAGE_KEY_SETTINGS)) {
            localStorage.setItem(STORAGE_KEY_SETTINGS, JSON.stringify(DEFAULT_SETTINGS));
        }

        // 5. Sincronizar dinámicamente con servidor si hay conexión
        if (!this._syncedServerUsers) {
            this._syncedServerUsers = true;
            this.apiFetch('/api/users').then(r => r.ok ? r.json() : null).then(srvList => {
                if (Array.isArray(srvList) && srvList.length > 0) {
                    const formatted = srvList.map(u => ({
                        id: u.id,
                        alias: u.alias,
                        edad: u.edad || 24,
                        objetivo: u.objetivo_personal || 'autorregulacion',
                        pin: u.pin || '1234',
                        rol: u.rol || ((u.alias || '').toLowerCase() === 'admin' ? 'admin' : 'participante'),
                        fecha: (u.fecha_registro || '').split(' ')[0] || '2026-10-01'
                    }));
                    localStorage.setItem(STORAGE_KEY_USERS_LIST, JSON.stringify(formatted));
                }
            }).catch(() => {});

            // Sincronizar eventos del usuario activo
            const activeUid = this.getActiveUserId();
            this.syncEventsFromServer(activeUid).catch(() => {});
        }
    },

    // ==========================================
    // PUENTE DINÁMICO GITHUB PAGES -> TÚNEL ACTIVO
    // ==========================================
    async resolveApiBaseUrl() {
        if (this._cachedApiBase !== undefined) return this._cachedApiBase;
        const host = (window.location.hostname || '').toLowerCase();
        // Si estamos en localhost o directamente en el dominio del túnel, usar ruta relativa ''
        if (host === 'localhost' || host === '127.0.0.1' || host.endsWith('.trycloudflare.com')) {
            this._cachedApiBase = '';
            return '';
        }
        // Si el usuario entró por el Link Maestro Fijo (GitHub Pages), consultar el túnel activo en GitHub
        try {
            const rawUrl = 'https://raw.githubusercontent.com/NiquelAwol/M-Control-IA/main/tunnel_config.json?t=' + Date.now();
            const r = await fetch(rawUrl, { cache: 'no-store' });
            if (r.ok) {
                const cfg = await r.json();
                if (cfg && cfg.tunnel_url) {
                    this._cachedApiBase = cfg.tunnel_url.replace(/\/+$/, '');
                    return this._cachedApiBase;
                }
            }
        } catch (e) {}
        this._cachedApiBase = '';
        return '';
    },

    async apiFetch(endpoint, options = {}) {
        const base = await this.resolveApiBaseUrl();
        return fetch(base + endpoint, options);
    },

    // ==========================================
    // CONTROL DE ACCESO Y AUTENTICACIÓN ESTRICTA
    // ==========================================
    getAuthSession() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY_AUTH_SESSION);
            return raw ? JSON.parse(raw) : null;
        } catch (e) {
            return null;
        }
    },

    isAuthenticated() {
        const sess = this.getAuthSession();
        return !!(sess && sess.userId && sess.alias);
    },

    isAdmin() {
        const sess = this.getAuthSession();
        return !!(sess && (sess.rol === 'admin' || (sess.alias || '').toLowerCase() === 'admin'));
    },

    async authenticateWithCredentials(aliasInput, passwordInput) {
        this.init();
        const cleanAlias = (aliasInput || '').trim();
        const cleanPin = String(passwordInput || '').trim();
        if (!cleanAlias || !cleanPin) {
            return { ok: false, error: 'Debes ingresar tu usuario y contraseña.' };
        }

        // 1. Intentar autenticar contra el servidor central Python (para usuarios remotos por link)
        try {
            const resp = await this.apiFetch('/api/users/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ alias: cleanAlias, pin: cleanPin })
            });
            if (resp.ok) {
                const data = await resp.json();
                if (data && data.user) {
                    const srvUser = data.user;
                    const users = this.getUsers();
                    let localUser = users.find(u => (u.alias || '').toLowerCase() === srvUser.alias.toLowerCase());
                    if (!localUser) {
                        localUser = {
                            id: srvUser.id,
                            alias: srvUser.alias,
                            edad: srvUser.edad || 24,
                            objetivo: srvUser.objetivo_personal || 'autorregulacion',
                            pin: cleanPin,
                            rol: srvUser.rol || (srvUser.alias.toLowerCase() === 'admin' ? 'admin' : 'participante'),
                            fecha: (srvUser.fecha_registro || '').split(' ')[0] || '2026-10-01'
                        };
                        users.push(localUser);
                        localStorage.setItem(STORAGE_KEY_USERS_LIST, JSON.stringify(users));
                    } else {
                        localUser.pin = cleanPin;
                        localUser.rol = srvUser.rol || (localUser.alias.toLowerCase() === 'admin' ? 'admin' : 'participante');
                        localStorage.setItem(STORAGE_KEY_USERS_LIST, JSON.stringify(users));
                    }
                    this._establishSession(localUser);
                    return { ok: true, user: localUser };
                }
            } else if (resp.status === 401) {
                // Revisar también en usuarios locales por si el admin lo creó en localStorage
                const localMatch = this._findLocalUser(cleanAlias, cleanPin);
                if (localMatch) {
                    this._establishSession(localMatch);
                    return { ok: true, user: localMatch };
                }
                return { ok: false, error: 'Usuario o contraseña incorrectos. Solo el Administrador puede otorgar credenciales.' };
            }
        } catch (err) {
            // Fallback local si no hay conexión con la API
        }

        // 2. Verificación en lista local
        const localMatch = this._findLocalUser(cleanAlias, cleanPin);
        if (localMatch) {
            this._establishSession(localMatch);
            return { ok: true, user: localMatch };
        }
        return { ok: false, error: 'Usuario o contraseña incorrectos. Solicita tu cuenta al Administrador.' };
    },

    _findLocalUser(cleanAlias, cleanPin) {
        const users = this.getUsers();
        const norm = s => (s || '').toString().toLowerCase().replace(/\s+/g, '');
        return users.find(u => {
            const aliasMatches = norm(u.alias) === norm(cleanAlias) || (u.alias || '').trim().toLowerCase() === cleanAlias.toLowerCase();
            const pinMatches = String(u.pin || '').trim() === cleanPin;
            return aliasMatches && pinMatches;
        }) || null;
    },

    _establishSession(user) {
        const rol = user.rol || ((user.alias || '').toLowerCase() === 'admin' ? 'admin' : 'participante');
        const sessionObj = {
            userId: user.id,
            alias: user.alias,
            rol: rol,
            loginAt: new Date().toISOString()
        };
        localStorage.setItem(STORAGE_KEY_AUTH_SESSION, JSON.stringify(sessionObj));
        this.setCurrentUser(user.id);
    },

    logout() {
        localStorage.removeItem(STORAGE_KEY_AUTH_SESSION);
    },

    // ==========================================
    // GESTIÓN DE PARTICIPANTES (SOLO ADMIN)
    // ==========================================
    getUsers() {
        this.init();
        try {
            return JSON.parse(localStorage.getItem(STORAGE_KEY_USERS_LIST)) || DEFAULT_USERS;
        } catch (e) {
            return DEFAULT_USERS;
        }
    },

    getActiveUserId() {
        this.init();
        const sess = this.getAuthSession();
        if (sess && sess.userId) return parseInt(sess.userId, 10);
        const raw = localStorage.getItem(STORAGE_KEY_ACTIVE_USER);
        return raw ? parseInt(raw, 10) : 1;
    },

    getCurrentUser() {
        const users = this.getUsers();
        const activeId = this.getActiveUserId();
        return users.find(u => u.id === activeId) || users[0] || { id: 1, alias: 'admin', edad: 24, objetivo: 'autorregulacion', rol: 'admin' };
    },

    setCurrentUser(userId) {
        this.init();
        const idNum = parseInt(userId, 10);
        localStorage.setItem(STORAGE_KEY_ACTIVE_USER, String(idNum));
        const user = this.getCurrentUser();
        window.dispatchEvent(new CustomEvent('mcontrol:userChanged', { detail: { userId: idNum, user } }));
        return user;
    },

    async adminCreateUser(alias, edad = 24, objetivo = 'autorregulacion', pin = '1234') {
        this.init();
        if (!this.isAdmin()) {
            throw new Error('Acceso denegado: Solo el Administrador puede crear usuarios.');
        }
        const cleanAlias = (alias || '').trim();
        const cleanPin = String(pin || '').trim();
        if (!cleanAlias || !cleanPin) {
            throw new Error('Debes especificar un nombre de usuario y una contraseña.');
        }

        const users = this.getUsers();
        if (users.some(u => (u.alias || '').toLowerCase() === cleanAlias.toLowerCase())) {
            throw new Error(`El usuario "${cleanAlias}" ya existe.`);
        }

        let createdId = users.reduce((max, u) => Math.max(max, u.id || 0), 0) + 1;

        // Registrar también en el servidor SQLite central para que funcione por el link externo
        try {
            const resp = await this.apiFetch('/api/users/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    admin_alias: 'admin',
                    alias: cleanAlias,
                    edad: parseInt(edad, 10) || 24,
                    objetivo: objetivo,
                    pin: cleanPin
                })
            });
            if (resp.ok) {
                const data = await resp.json();
                if (data && data.user && data.user.id) {
                    createdId = data.user.id;
                }
            }
        } catch (e) {}

        const newUser = {
            id: createdId,
            alias: cleanAlias,
            edad: parseInt(edad, 10) || 24,
            objetivo: objetivo.trim() || 'autorregulacion',
            pin: cleanPin,
            rol: cleanAlias.toLowerCase() === 'admin' ? 'admin' : 'participante',
            fecha: new Date().toISOString().split('T')[0]
        };

        users.push(newUser);
        localStorage.setItem(STORAGE_KEY_USERS_LIST, JSON.stringify(users));
        localStorage.setItem(STORAGE_KEY_USER_EVENTS_PREFIX + newUser.id, JSON.stringify([]));
        return newUser;
    },

    async adminDeleteUser(userId) {
        if (!this.isAdmin()) return false;
        const users = this.getUsers();
        const target = users.find(u => u.id === userId);
        if (!target || (target.alias || '').toLowerCase() === 'admin') return false;

        const filtered = users.filter(u => u.id !== userId);
        localStorage.setItem(STORAGE_KEY_USERS_LIST, JSON.stringify(filtered));
        localStorage.removeItem(STORAGE_KEY_USER_EVENTS_PREFIX + userId);

        try {
            await this.apiFetch('/api/users/delete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ admin_alias: 'admin', user_id: userId })
            });
        } catch (e) {}
        return true;
    },

    // ==========================================
    // HISTORIAL DE EVENTOS AISLADO POR USUARIO
    // ==========================================
    getEvents(userId = null) {
        this.init();
        const uid = userId !== null ? parseInt(userId, 10) : this.getActiveUserId();
        const key = STORAGE_KEY_USER_EVENTS_PREFIX + uid;
        try {
            let raw = localStorage.getItem(key);
            if (!raw && uid === 1) {
                raw = localStorage.getItem(STORAGE_KEY_EVENTS);
            }
            if (raw) {
                const data = JSON.parse(raw);
                if (Array.isArray(data) && data.length > 0) {
                    return data.sort((a, b) => new Date(b.date) - new Date(a.date));
                }
            }
            // Fallback directo a los eventos por defecto de la base de datos
            const fallback = (typeof DEFAULT_EVENTS_BY_USER !== 'undefined' && DEFAULT_EVENTS_BY_USER[String(uid)]) ? DEFAULT_EVENTS_BY_USER[String(uid)] : [];
            if (fallback.length > 0) {
                localStorage.setItem(key, JSON.stringify(fallback));
                if (uid === 1) localStorage.setItem(STORAGE_KEY_EVENTS, JSON.stringify(fallback));
                return [...fallback].sort((a, b) => new Date(b.date) - new Date(a.date));
            }
            return [];
        } catch (e) {
            console.error('Error al leer eventos:', e);
            return (typeof DEFAULT_EVENTS_BY_USER !== 'undefined' && DEFAULT_EVENTS_BY_USER[String(uid)]) ? DEFAULT_EVENTS_BY_USER[String(uid)] : [];
        }
    },

    _convertServerRecordsToEvents(records, uid) {
        if (!Array.isArray(records) || records.length === 0) return [];
        const sorted = [...records].sort((a, b) => {
            const dtA = new Date(`${a.fecha}T${a.hora || '12:00'}`);
            const dtB = new Date(`${b.fecha}T${b.hora || '12:00'}`);
            return dtA - dtB;
        });

        const events = [];
        for (const r of sorted) {
            const ctrlVal = r.nivel_control || 3;
            const ctrlStr = ctrlVal >= 4 ? 'alto' : (ctrlVal >= 3 ? 'medio' : 'bajo');

            const interfVal = (r.interferencia_sueno || 0) + (r.interferencia_estudio || 0) + (r.interferencia_trabajo || 0) + (r.interferencia_social || 0);
            const interfStr = interfVal >= 2 ? 'severa' : (interfVal === 1 ? 'leve' : 'ninguna');

            const sintVal = (r.dolor || 0) + (r.irritacion || 0) + (r.malestar || 0);
            const sintStr = sintVal >= 2 ? 'moderado_severo' : (sintVal === 1 ? 'leve' : 'ninguno');

            const emoc = (r.estado_emocional || '').toLowerCase();
            const estresStr = (emoc.includes('estrés') || emoc.includes('ansiedad') || emoc.includes('estres')) ? 'alto' : ((emoc.includes('aburrimiento') || emoc.includes('cansancio')) ? 'medio' : 'bajo');

            const curDt = `${r.fecha}T${r.hora || '12:00'}`;
            const evalResult = this.calculateWellness({
                date: curDt,
                control: ctrlStr,
                interferencia: interfStr,
                sintomas: sintStr,
                estres: estresStr
            }, events.length > 0 ? [events[events.length - 1]] : []);

            events.push({
                id: `evt-${uid}-${r.id}`,
                date: curDt,
                control: ctrlStr,
                interferencia: interfStr,
                sintomas: sintStr,
                estres: estresStr,
                porno: Boolean(r.realizo_habito === 1 && (ctrlVal <= 3 || (r.nivel_deseo || 0) >= 4)),
                notas: r.observaciones || '',
                score: evalResult.score,
                color: evalResult.color,
                explicacion: evalResult.explicacion,
                usuario_id: uid
            });
        }
        return events.reverse();
    },

    async syncEventsFromServer(userId = null) {
        const uid = userId !== null ? parseInt(userId, 10) : this.getActiveUserId();
        try {
            const resp = await this.apiFetch(`/api/records?user_id=${uid}`);
            if (resp.ok) {
                const records = await resp.json();
                if (Array.isArray(records) && records.length > 0) {
                    const formatted = this._convertServerRecordsToEvents(records, uid);
                    const key = STORAGE_KEY_USER_EVENTS_PREFIX + uid;
                    localStorage.setItem(key, JSON.stringify(formatted));
                    if (uid === 1) {
                        localStorage.setItem(STORAGE_KEY_EVENTS, JSON.stringify(formatted));
                    }
                    return formatted;
                }
            }
        } catch (e) {
            // Modo offline / GitHub Pages
        }
        return this.getEvents(uid);
    },

    saveEvent(eventData, userId = null) {
        const uid = userId !== null ? parseInt(userId, 10) : this.getActiveUserId();
        const key = STORAGE_KEY_USER_EVENTS_PREFIX + uid;
        const events = this.getEvents(uid);
        const evaluation = this.calculateWellness(eventData, events);
        
        const newEvent = {
            id: 'evt-' + Date.now() + '-' + Math.floor(Math.random() * 1000),
            date: eventData.date,
            control: eventData.control,
            interferencia: eventData.interferencia,
            sintomas: eventData.sintomas,
            estres: eventData.estres,
            porno: eventData.porno || false,
            notas: eventData.notas || '',
            score: evaluation.score,
            color: evaluation.color,
            explicacion: evaluation.explicacion,
            usuario_id: uid
        };

        events.unshift(newEvent);
        localStorage.setItem(key, JSON.stringify(events));

        // Sincronizar en key global para compatibilidad si es usuario 1
        if (uid === 1) {
            localStorage.setItem(STORAGE_KEY_EVENTS, JSON.stringify(events));
        }

        // Notificar al backend de IA asociando el usuario_id correspondiente
        try {
            this.apiFetch('/api/records', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    usuario_id: uid,
                    fecha: eventData.date.split('T')[0],
                    hora: eventData.date.includes('T') ? eventData.date.split('T')[1] : '12:00',
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

    deleteEvent(id, userId = null) {
        const uid = userId !== null ? parseInt(userId, 10) : this.getActiveUserId();
        const key = STORAGE_KEY_USER_EVENTS_PREFIX + uid;
        let events = this.getEvents(uid);
        events = events.filter(e => e.id !== id);
        localStorage.setItem(key, JSON.stringify(events));
        if (uid === 1) {
            localStorage.setItem(STORAGE_KEY_EVENTS, JSON.stringify(events));
        }
    },

    getSettings(userId = null) {
        this.init();
        const uid = userId !== null ? parseInt(userId, 10) : this.getActiveUserId();
        const key = STORAGE_KEY_USER_SETTINGS_PREFIX + uid;
        const curUser = this.getCurrentUser();
        try {
            const data = JSON.parse(localStorage.getItem(key));
            if (data) return data;
        } catch (e) {}
        return {
            ...DEFAULT_SETTINGS,
            edad: curUser ? curUser.edad : 24,
            objetivo: curUser ? curUser.objetivo : 'autorregulacion'
        };
    },

    saveSettings(settings, userId = null) {
        const uid = userId !== null ? parseInt(userId, 10) : this.getActiveUserId();
        const key = STORAGE_KEY_USER_SETTINGS_PREFIX + uid;
        localStorage.setItem(key, JSON.stringify(settings));
        if (uid === 1) {
            localStorage.setItem(STORAGE_KEY_SETTINGS, JSON.stringify(settings));
        }
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

    generatePredictiveCalendar(year, month, userId = null) {
        // month es 1-indexed (1 = Enero, 10 = Octubre)
        const daysInMonth = new Date(year, month, 0).getDate();
        const firstDay = new Date(year, month - 1, 1);
        let startDayIndex = firstDay.getDay() - 1;
        if (startDayIndex === -1) startDayIndex = 6;

        const allEvents = this.getEvents(userId);
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

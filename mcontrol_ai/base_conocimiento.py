"""
base_conocimiento.py
M-Control AI | Base de Conocimiento Científico Estructurada

Almacena fuentes médicas, epidemiológicas y psicométricas revisadas por pares:
- Organización Mundial de la Salud (OMS / CIE-11 CSBD)
- National Survey of Sexual Health and Behavior (NSSHB / Herbenick et al.)
- International Society for Sexual Medicine (ISSM)
- Compulsive Sexual Behavior Disorder Scale (CSBD-19 / Bőthe et al.)
- Neurobiología del sueño y hormonas (Lastella et al., 2019)
- Mayo Clinic & Cleveland Clinic
"""

from typing import Dict, List, Any, Optional

# --- FUENTES CIENTÍFICAS REVISADAS Y FORMALIZADAS ---
FUENTES_CIENTIFICAS = [
    {
        "id": 1,
        "nombre": "CIE-11: Trastorno de Comportamiento Sexual Compulsivo (6C72)",
        "institucion": "Organización Mundial de la Salud (OMS)",
        "url": "https://icd.who.int/browse/2024-01/mms/es#1630268048",
        "año": 2019,
        "tipo": "Clasificación Diagnóstica Internacional Oficial",
        "poblacion": "Población global clínica y general",
        "muestra": 0,  # Consenso internacional de expertos
        "tema": "Trastornos del control de los impulsos",
        "contenido": (
            "Define el CSBD como un patrón persistente de incapacidad para controlar impulsos "
            "sexuales intensos y repetitivos que provoca malestar o deterioro marcado en áreas personal, "
            "familiar, social, educativa u ocupacional. Excluye explícitamente el malestar derivado "
            "únicamente de juicios morales o religiosos y el mero deseo sexual elevado sin deterioro."
        ),
        "nivel_evidencia": "Consenso Clínico Internacional Oficial (Nivel 1A)"
    },
    {
        "id": 2,
        "nombre": "National Survey of Sexual Health and Behavior (NSSHB)",
        "institucion": "The Kinsey Institute / Indiana University (Herbenick et al.)",
        "url": "https://pubmed.ncbi.nlm.nih.gov/21029386/",
        "año": 2010,
        "tipo": "Estudio Epidemiológico Nacional Probabilístico",
        "poblacion": "Hombres y mujeres en Estados Unidos (14 a 94 años)",
        "muestra": 5865,
        "tema": "Frecuencia poblacional y conductas sexuales",
        "contenido": (
            "Demuestra que no existe una frecuencia universalmente normal. La frecuencia de "
            "masturbación varía ampliamente en todas las edades. Entre hombres adultos de 18 a 59 años: "
            "~25% mensual a semanal, ~20% 2-3 veces/semana, <20% 4+ veces/semana. La frecuencia disminuye "
            "gradualmente con la edad pero persiste en proporciones significativas en adultos mayores."
        ),
        "nivel_evidencia": "Estudio Observacional Probabilístico a Gran Escala (Nivel 2A)"
    },
    {
        "id": 3,
        "nombre": "What is the 'Normal' Frequency of Masturbation?",
        "institucion": "International Society for Sexual Medicine (ISSM)",
        "url": "https://www.issm.info/sexual-health-qa/what-is-the-normal-frequency-of-masturbation/",
        "año": 2021,
        "tipo": "Guía de Divulgación y Posicionamiento Clínico",
        "poblacion": "Hombres y mujeres adultos",
        "muestra": 0,
        "tema": "Normalidad estadística vs. salud clínica",
        "contenido": (
            "Confirma que no existe un límite superior o inferior universalmente saludable. "
            "La masturbación solo se vuelve médicamente preocupante cuando genera daño físico, dolor, "
            "irritación o interfiere con las actividades de la vida diaria, el trabajo o las relaciones."
        ),
        "nivel_evidencia": "Posicionamiento de Sociedad Médica Internacional (Nivel 1B)"
    },
    {
        "id": 4,
        "nombre": "The Compulsive Sexual Behavior Disorder Scale (CSBD-19)",
        "institucion": "Journal of Behavioral Addictions (Bőthe, Potenza, Griffiths, Kraus et al.)",
        "url": "https://pubmed.ncbi.nlm.nih.gov/32609629/",
        "año": 2020,
        "tipo": "Validación Psicométrica Transcultural",
        "poblacion": "Adultos diversos en múltiples países e idiomas",
        "muestra": 9325,
        "tema": "Evaluación multidimensional de desregulación sexual",
        "contenido": (
            "Estructura el comportamiento desregulado en 5 factores: 1) Pérdida de control, "
            "2) Salience (relevancia excesiva postergando otras áreas), 3) Relapse (recaídas compulsivas), "
            "4) Dissatisfaction (pérdida de satisfacción o placer), y 5) Consecuencias negativas. "
            "Establece un umbral óptimo de riesgo de 50/76 puntos."
        ),
        "nivel_evidencia": "Validación Psicométrica Rigurosa Revisada por Pares (Nivel 1B)"
    },
    {
        "id": 5,
        "nombre": "Sex and Sleep: Perceptions of Sex as a Sleep Promoting Behavior",
        "institucion": "Frontiers in Public Health (Lastella et al.)",
        "url": "https://pubmed.ncbi.nlm.nih.gov/30881958/",
        "año": 2019,
        "tipo": "Estudio Observacional / Medicina del Sueño",
        "poblacion": "Adultos de población general",
        "muestra": 778,
        "tema": "Relación entre orgasmo, hormonas y conciliación del sueño",
        "contenido": (
            "La mayoría de participantes percibe la actividad sexual y la masturbación como promotoras "
            "del sueño y reductoras de la latencia para dormir. Se explica por el incremento de prolactina "
            "y oxitocina posorgasmo, acompañado de una atenuación de los niveles de cortisol (estrés). "
            "M-Control reconoce este beneficio pero alerta si la conducta nocturna prolongada en pantallas "
            "posterga la hora de descanso."
        ),
        "nivel_evidencia": "Estudio Observacional Revisado por Pares (Nivel 2B)"
    },
    {
        "id": 6,
        "nombre": "Masturbation: Facts & Health Benefits",
        "institucion": "Cleveland Clinic",
        "url": "https://my.clevelandclinic.org/health/articles/24332-masturbation",
        "año": 2023,
        "tipo": "Artículo de Revisión y Salud Clínica",
        "poblacion": "Población general masculina",
        "muestra": 0,
        "tema": "Beneficios fisiológicos y desmitificación médica",
        "contenido": (
            "Confirma que la masturbación no causa ceguera, disfunción eréctil permanente, pérdida de visión "
            "ni disminución del conteo espermático. Los efectos físicos adversos por alta frecuencia "
            "(irritación, rozaduras o inflamación) son transitorios y ceden con descanso."
        ),
        "nivel_evidencia": "Revisión Clínica Institucional (Nivel 2C)"
    },
    {
        "id": 7,
        "nombre": "Compulsive Sexual Behavior: Symptoms, Causes & Treatment",
        "institucion": "Mayo Clinic",
        "url": "https://www.mayoclinic.org/es/diseases-conditions/compulsive-sexual-behavior/symptoms-causes/syc-20360434",
        "año": 2023,
        "tipo": "Guía Clínica Especializada",
        "poblacion": "Pacientes con pérdida de control conductual",
        "muestra": 0,
        "tema": "Indicadores conductuales de desregulación",
        "contenido": (
            "Describe las señales clave: uso reiterado de la conducta sexual como única vía de escape ante "
            "ansiedad, culpa, soledad o estrés; gasto desproporcionado de tiempo; e intentos continuados y fallidos "
            "de reducir o frenar el hábito."
        ),
        "nivel_evidencia": "Guía de Práctica Clínica Especializada (Nivel 2A)"
    },
    {
        "id": 8,
        "nombre": "Ejaculation Frequency and Risk of Prostate Cancer",
        "institucion": "European Urology (Rider et al. / Harvard T.H. Chan School of Public Health)",
        "url": "https://pubmed.ncbi.nlm.nih.gov/27033442/",
        "año": 2016,
        "tipo": "Estudio de Cohorte Prospectivo Longitudinal (18 años de seguimiento)",
        "poblacion": "Hombres adultos profesionales de la salud",
        "muestra": 31925,
        "tema": "Frecuencia eyaculatoria y salud prostática a largo plazo",
        "contenido": (
            "Encontró que hombres con 21 o más eyaculaciones al mes presentaron una reducción relativa "
            "de ~20% en el diagnóstico de cáncer de próstata frente a quienes reportaron 4-7 al mes. "
            "M-Control documenta esta evidencia aclarando que es una asociación estadística observacional y no una "
            "prescripción que justifique forzar una cuota fija obligatoria."
        ),
        "nivel_evidencia": "Estudio de Cohorte Prospectivo a Gran Escala (Nivel 1B)"
    }
]

# --- DATOS POBLACIONALES DEL NSSHB ESTRATIFICADOS POR EDAD ---
DATOS_POBLACIONALES_NSSHB = [
    # 18 a 24 años
    {"edad_min": 18, "edad_max": 24, "frecuencia": "Ninguna en el último año", "porcentaje": 9.3, "frecuencia_semanal_est": 0.0},
    {"edad_min": 18, "edad_max": 24, "frecuencia": "Pocas veces al año", "porcentaje": 12.1, "frecuencia_semanal_est": 0.1},
    {"edad_min": 18, "edad_max": 24, "frecuencia": "1 a 4 veces al mes (semanal)", "porcentaje": 27.4, "frecuencia_semanal_est": 0.75},
    {"edad_min": 18, "edad_max": 24, "frecuencia": "2 a 3 veces por semana", "porcentaje": 28.5, "frecuencia_semanal_est": 2.5},
    {"edad_min": 18, "edad_max": 24, "frecuencia": "4 o más veces por semana", "porcentaje": 22.7, "frecuencia_semanal_est": 4.5},

    # 25 a 29 años
    {"edad_min": 25, "edad_max": 29, "frecuencia": "Ninguna en el último año", "porcentaje": 11.2, "frecuencia_semanal_est": 0.0},
    {"edad_min": 25, "edad_max": 29, "frecuencia": "Pocas veces al año", "porcentaje": 14.5, "frecuencia_semanal_est": 0.1},
    {"edad_min": 25, "edad_max": 29, "frecuencia": "1 a 4 veces al mes (semanal)", "porcentaje": 28.0, "frecuencia_semanal_est": 0.75},
    {"edad_min": 25, "edad_max": 29, "frecuencia": "2 a 3 veces por semana", "porcentaje": 26.1, "frecuencia_semanal_est": 2.5},
    {"edad_min": 25, "edad_max": 29, "frecuencia": "4 o más veces por semana", "porcentaje": 20.2, "frecuencia_semanal_est": 4.5},

    # 30 a 39 años
    {"edad_min": 30, "edad_max": 39, "frecuencia": "Ninguna en el último año", "porcentaje": 14.6, "frecuencia_semanal_est": 0.0},
    {"edad_min": 30, "edad_max": 39, "frecuencia": "Pocas veces al año", "porcentaje": 18.2, "frecuencia_semanal_est": 0.1},
    {"edad_min": 30, "edad_max": 39, "frecuencia": "1 a 4 veces al mes (semanal)", "porcentaje": 29.3, "frecuencia_semanal_est": 0.75},
    {"edad_min": 30, "edad_max": 39, "frecuencia": "2 a 3 veces por semana", "porcentaje": 22.4, "frecuencia_semanal_est": 2.5},
    {"edad_min": 30, "edad_max": 39, "frecuencia": "4 o más veces por semana", "porcentaje": 15.5, "frecuencia_semanal_est": 4.5},

    # 40 a 49 años
    {"edad_min": 40, "edad_max": 49, "frecuencia": "Ninguna en el último año", "porcentaje": 19.8, "frecuencia_semanal_est": 0.0},
    {"edad_min": 40, "edad_max": 49, "frecuencia": "Pocas veces al año", "porcentaje": 21.0, "frecuencia_semanal_est": 0.1},
    {"edad_min": 40, "edad_max": 49, "frecuencia": "1 a 4 veces al mes (semanal)", "porcentaje": 26.5, "frecuencia_semanal_est": 0.75},
    {"edad_min": 40, "edad_max": 49, "frecuencia": "2 a 3 veces por semana", "porcentaje": 19.2, "frecuencia_semanal_est": 2.5},
    {"edad_min": 40, "edad_max": 49, "frecuencia": "4 o más veces por semana", "porcentaje": 13.5, "frecuencia_semanal_est": 4.5},

    # 50 a 59 años
    {"edad_min": 50, "edad_max": 59, "frecuencia": "Ninguna en el último año", "porcentaje": 26.5, "frecuencia_semanal_est": 0.0},
    {"edad_min": 50, "edad_max": 59, "frecuencia": "Pocas veces al año", "porcentaje": 23.1, "frecuencia_semanal_est": 0.1},
    {"edad_min": 50, "edad_max": 59, "frecuencia": "1 a 4 veces al mes (semanal)", "porcentaje": 24.2, "frecuencia_semanal_est": 0.75},
    {"edad_min": 50, "edad_max": 59, "frecuencia": "2 a 3 veces por semana", "porcentaje": 16.0, "frecuencia_semanal_est": 2.5},
    {"edad_min": 50, "edad_max": 59, "frecuencia": "4 o más veces por semana", "porcentaje": 10.2, "frecuencia_semanal_est": 4.5},

    # 60+ años
    {"edad_min": 60, "edad_max": 99, "frecuencia": "Ninguna en el último año", "porcentaje": 41.0, "frecuencia_semanal_est": 0.0},
    {"edad_min": 60, "edad_max": 99, "frecuencia": "Pocas veces al año", "porcentaje": 22.5, "frecuencia_semanal_est": 0.1},
    {"edad_min": 60, "edad_max": 99, "frecuencia": "1 a 4 veces al mes (semanal)", "porcentaje": 19.3, "frecuencia_semanal_est": 0.75},
    {"edad_min": 60, "edad_max": 99, "frecuencia": "2 a 3 veces por semana", "porcentaje": 11.4, "frecuencia_semanal_est": 2.5},
    {"edad_min": 60, "edad_max": 99, "frecuencia": "4 o más veces por semana", "porcentaje": 5.8, "frecuencia_semanal_est": 4.5}
]

# --- INDICADORES Y PESOS CLÍNICOS DEL MODELO ---
DIMENSIONES_CLINICAS = {
    "interferencia_funcional": {
        "peso": 0.35,
        "descripcion": "Impacto acumulativo en sueño, jornada de estudio, responsabilidades de trabajo y vínculos sociales.",
        "origen": "CIE-11 CSBD criterio B (deterioro funcional en áreas clave)."
    },
    "perdida_control": {
        "peso": 0.30,
        "descripcion": "Incapacidad para posponer la conducta, impulsividad y antecedentes de intentos fallidos de reducción.",
        "origen": "CIE-11 CSBD criterio A / Escala CSBD-19 Factor Control."
    },
    "sintomas_fisicos": {
        "peso": 0.20,
        "descripcion": "Presencia de irritación cutánea, inflamación, hipersensibilidad o dolor por fricción reiterada.",
        "origen": "Cleveland Clinic & ISSM (criterio biológico de descanso fisiológico necesario)."
    },
    "escape_emocional": {
        "peso": 0.15,
        "descripcion": "Uso repetido del hábito como único mecanismo para afrontar ansiedad, estrés o aislamiento.",
        "origen": "Mayo Clinic & HBI-19 (Coping subscale)."
    }
}


def obtener_prior_poblacional(edad: int) -> Dict[str, Any]:
    """
    Retorna la distribución estadística del grupo etario correspondiente
    según la encuesta probabilística NSSHB.
    """
    edad = max(18, min(edad, 95))
    cohortes = [d for d in DATOS_POBLACIONALES_NSSHB if d["edad_min"] <= edad <= d["edad_max"]]
    
    # Calcular frecuencia semanal esperada ponderada
    frecuencia_esperada = sum((c["porcentaje"] / 100.0) * c["frecuencia_semanal_est"] for c in cohortes)
    
    return {
        "edad": edad,
        "cohorte": f"{cohortes[0]['edad_min']}-{cohortes[0]['edad_max']} años",
        "distribucion": cohortes,
        "frecuencia_semanal_media_cohorte": round(frecuencia_esperada, 2),
        "fuente": "NSSHB / Herbenick et al. 2010 (PubMed PMID: 21029386)"
    }


def obtener_fuentes() -> List[Dict[str, Any]]:
    """Retorna todas las fuentes científicas catalogadas."""
    return FUENTES_CIENTIFICAS


def obtener_fuente_por_id(fuente_id: int) -> Optional[Dict[str, Any]]:
    """Busca una fuente específica por su identificador."""
    for f in FUENTES_CIENTIFICAS:
        if f["id"] == fuente_id:
            return f
    return None

"""
xai_explainer.py
M-Control AI | Motor de Explicabilidad Clínica y Generación de Fichas Preventivas

Convierte las predicciones cuantitativas de Machine Learning en explicaciones
comprensibles, empáticas, fundamentadas en evidencia y libres de juicios morales,
en estricto apego a las directrices de la OMS/CIE-11 y la ISSM.
"""

from typing import Any, Dict, List


ESTADOS_CONFIG = {
    "Verde": {
        "etiqueta": "🟢 DÍA RECOMENDABLE / BAJO RIESGO",
        "badge": "badge-green",
        "descripcion": "El modelo estima un patrón favorable y de bajo riesgo de desregulación según tu historial.",
        "tono": "positivo"
    },
    "Amarillo": {
        "etiqueta": "🟡 DÍA DE PRECAUCIÓN / VIGILANCIA",
        "badge": "badge-yellow",
        "descripcion": "Se observa una posible tendencia de aceleración de frecuencia o estrés acumulado que conviene vigilar.",
        "tono": "observacion"
    },
    "Naranja": {
        "etiqueta": "🟠 ALERTA MODERADA",
        "badge": "badge-orange",
        "descripcion": "Tu historial reciente muestra varios indicadores asociados a pérdida de control o ligera interferencia.",
        "tono": "alerta"
    },
    "Rojo": {
        "etiqueta": "🔴 DÍA NO RECOMENDABLE / ALTA ALERTA",
        "badge": "badge-red",
        "descripcion": "El modelo identifica una probabilidad elevada de que este evento se relacione con un patrón de desregulación o malestar según tus registros anteriores.",
        "tono": "pausa"
    }
}

DISCLAIMER_MEDICO = (
    "Nota importante: Esta predicción se basa en tu historial personal, análisis de tendencias y "
    "en la literatura científica disponible (CIE-11 CSBD, NSSHB e ISSM). No constituye una prohibición "
    "ni un diagnóstico médico. M-Control es una herramienta de autorregulación y autoconocimiento."
)


def formatear_ficha_dia(prediccion: Dict[str, Any]) -> Dict[str, Any]:
    """
    Toma el resultado crudo del modelo predictivo y genera una ficha estructurada
    lista para ser consumida por la interfaz de usuario del calendario inteligente.
    """
    nivel = prediccion.get("nivel", "Verde")
    cfg = ESTADOS_CONFIG.get(nivel, ESTADOS_CONFIG["Verde"])
    prob = prediccion.get("probabilidad", 0.1)
    conf = prediccion.get("confianza", 0.7)
    motivos = prediccion.get("motivos", [])
    recomendacion = prediccion.get("recomendacion", "")
    fecha = prediccion.get("fecha", "")

    return {
        "fecha": fecha,
        "nivel": nivel,
        "etiqueta_estado": cfg["etiqueta"],
        "badge_class": cfg["badge"],
        "probabilidad_pct": f"{int(prob * 100)}%",
        "confianza_pct": f"{int(conf * 100)}%",
        "probabilidad_num": round(prob, 3),
        "confianza_num": round(conf, 3),
        "probabilidad": round(prob, 3),
        "confianza": round(conf, 3),
        "explicacion_principal": cfg["descripcion"],
        "factores_detectados": motivos,
        "motivos": motivos,
        "recomendacion": recomendacion,
        "disclaimer": DISCLAIMER_MEDICO,
        "modelo_version": prediccion.get("modelo_version", "v2.0-hybrid")
    }


def generar_resumen_texto(ficha: Dict[str, Any]) -> str:
    """Genera la representación en texto plano tal como se especifica en la pauta."""
    lineas = [
        f"Fecha: {ficha['fecha']}",
        f"Estado: {ficha['etiqueta_estado']}",
        f"Predicción: {ficha['explicacion_principal']}",
        f"Confianza: {ficha['confianza_pct']}",
        "",
        "Factores detectados:"
    ]
    for m in ficha["factores_detectados"]:
        lineas.append(f"• {m}")
    lineas.append("")
    lineas.append(f"Recomendación: {ficha['recomendacion']}")
    lineas.append("")
    lineas.append(ficha["disclaimer"])
    return "\n".join(lineas)

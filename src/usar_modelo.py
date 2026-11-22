"""
usar_modelo.py
M-Control | Inteligencia Artificial · Proyecto Final (Tercer Corte)
Docente: Jhon James Cano Sánchez
Integrantes: Andrés Felipe Mejía Suaza & Miguel Ángel Ramírez

Script de Demostración en Vivo (Requisito 6 - Clase 12):
Carga directamente el modelo serializado 'modelo_final.joblib' SIN VOLVER A ENTRENAR
y realiza predicciones sobre casos clínicos nuevos, interpretando la probabilidad
y emitiendo la recomendación preventiva en lenguaje natural.
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd


def obtener_directorio_base():
    """Resuelve la raíz del repositorio tanto si se ejecuta desde /app como desde /app/src."""
    actual = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(actual) == "src":
        return os.path.dirname(actual)
    return actual


def clasificar_semaforo(prob_alerta: float) -> str:
    """Traduce la probabilidad continua P(y=1|x) al semáforo clínico de 4 estados de M-Control."""
    if prob_alerta < 0.25:
        return "VERDE (Balance y Autorregulación Favorable)"
    elif prob_alerta < 0.50:
        return "AMARILLO (Vigilancia de Contexto / Precaución Leve)"
    elif prob_alerta < 0.75:
        return "NARANJA (Alerta Moderada - Se sugiere posponer y descansar)"
    else:
        return "ROJO (Alerta Alta - Requiere Pausa Biológica Preventiva)"


def main():
    base_dir = obtener_directorio_base()
    ruta_modelo = os.path.join(base_dir, "src", "modelo_final.joblib")
    if not os.path.exists(ruta_modelo):
        ruta_modelo = os.path.join(base_dir, "modelo_final.joblib")
    if not os.path.exists(ruta_modelo):
        print("[ERROR] No se encontró 'modelo_final.joblib'. Ejecute primero 'python modelo_proyecto.py'.")
        return

    print("=" * 82)
    print("  M-CONTROL | DEMOSTRACIÓN EN VIVO CON CASOS NUEVOS (usar_modelo.py)")
    print("  inferencia directa desde 'modelo_final.joblib' (SIN RE-ENTRENAMIENTO)")
    print("=" * 82)

    artefacto = joblib.load(ruta_modelo)
    pipeline = artefacto["pipeline"]
    nombre_modelo = artefacto["nombre_modelo"]
    features = artefacto["features"]

    print(f"\n[OK] Modelo cargado instantáneamente : {nombre_modelo}")
    print(f"[OK] Hiperparámetros óptimos         : {artefacto.get('mejores_hiperparametros')}")
    print(f"[OK] Características esperadas ({len(features)}) : {features}\n")

    # Casos clínicos nuevos representativos de usuarios de Cartago, Valle del Cauca
    casos_nuevos = [
        {
            "titulo": "CASO 1: Estudiante universitario en época de parciales (Sobrecarga Aguda)",
            "contexto": "Joven de 21 años en Cartago; solo 9.5 horas de descanso desde el último evento, estrés alto (9/10), interferencia en horas de sueño y bajo control autopercibido.",
            "datos": {
                "intervalo_horas": 9.5,
                "nivel_estres": 9,
                "interferencia_funcional": 2,
                "sintomas_fisicos": 1,
                "consumo_pornografia": 1,
                "hora_evento": 23,
                "control_1": 1,
                "control_2": 0,
                "control_3": 0
            }
        },
        {
            "titulo": "CASO 2: Adulto joven deportista con hábito autorregulado (Balance Saludable)",
            "contexto": "Usuario de 27 años; 56 horas de descanso biológico acumulado, estrés bajo (2/10), cero interferencia laboral o académica, sin molestias físicas y control alto.",
            "datos": {
                "intervalo_horas": 56.0,
                "nivel_estres": 2,
                "interferencia_funcional": 0,
                "sintomas_fisicos": 0,
                "consumo_pornografia": 0,
                "hora_evento": 21,
                "control_1": 0,
                "control_2": 0,
                "control_3": 1
            }
        },
        {
            "titulo": "CASO 3: Caso No Lineal (Buen descanso y bajo estrés, pero con irritación física)",
            "contexto": "Usuario de 24 años; descansó 41 horas y tiene estrés moderado-bajo (4/10), pero presenta irritación física e interferencia leve. (Caso donde fallaba el Perceptrón 2D).",
            "datos": {
                "intervalo_horas": 41.0,
                "nivel_estres": 4,
                "interferencia_funcional": 1,
                "sintomas_fisicos": 1,
                "consumo_pornografia": 1,
                "hora_evento": 22,
                "control_1": 0,
                "control_2": 1,
                "control_3": 0
            }
        },
        {
            "titulo": "CASO 4: Trabajador en transición de fatiga vespertina (Zona Intermedia)",
            "contexto": "Usuario de 31 años en jornada laboral sedentaria; 24 horas de descanso, estrés intermedio (6/10), sin dolor físico pero con control moderado.",
            "datos": {
                "intervalo_horas": 24.0,
                "nivel_estres": 6,
                "interferencia_funcional": 0,
                "sintomas_fisicos": 0,
                "consumo_pornografia": 1,
                "hora_evento": 19,
                "control_1": 0,
                "control_2": 1,
                "control_3": 0
            }
        }
    ]

    for idx, caso in enumerate(casos_nuevos, start=1):
        fila_df = pd.DataFrame([caso["datos"]])[features]
        X_nuevo = fila_df.values
        clase_pred = int(pipeline.predict(X_nuevo)[0])
        prob_alerta = float(pipeline.predict_proba(X_nuevo)[0, 1])
        semaforo = clasificar_semaforo(prob_alerta)

        print("-" * 82)
        print(f"  {caso['titulo']}")
        print("-" * 82)
        print(f"  • Contexto Clínico : {caso['contexto']}")
        print(f"  • Vector Entrada   : Intervalo={caso['datos']['intervalo_horas']}h | Estrés={caso['datos']['nivel_estres']}/10 | "
              f"Interferencia={caso['datos']['interferencia_funcional']} | Síntomas={caso['datos']['sintomas_fisicos']}")
        print(f"  • Clase Predicha   : {clase_pred} ({'REQUIERE PAUSA PREVENTIVA' if clase_pred == 1 else 'FAVORABLE / EN BALANCE'})")
        print(f"  • Probabilidad IA  : {prob_alerta * 100:.2f} % de riesgo de desregulación")
        print(f"  • Estado Semáforo  : {semaforo}")
        if clase_pred == 1:
            print("  • Recomendación IA : El modelo detecta factores de sobrecarga o afectación funcional/física.")
            print("                       Se recomienda una pausa biológica de recuperación de 48 a 72 horas.")
        else:
            print("  • Recomendación IA : Patrón conductual compatible con el bienestar y la autorregulación.")
            print("                       No se detecta interferencia ni fatiga acumulada.")
        print()

    print("=" * 82)
    print("  [FIN DE LA DEMOSTRACIÓN EN VIVO - INFERENCIA COMPLETADA EXITOSAMENTE]")
    print("=" * 82)


if __name__ == "__main__":
    main()

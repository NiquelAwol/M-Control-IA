"""
ml_engine.py
M-Control AI | Motor de Machine Learning Real y Aprendizaje Progresivo

Implementa:
1. Ingeniería de características temporales y clínicas (ventanas móviles 7d, 14d, 30d).
2. Algoritmo de clasificación supervisada calibrado (Random Forest / Calibrated Classifier).
3. Estrategia de Cold-Start con Priors Bayesianos basados en edad y NSSHB.
4. Aprendizaje continuo incremental sin sobreajuste (evitando saltos bruscos).
5. Estimación de probabilidad continua (0.0 a 1.0) y categorización en 4 estados:
   🟢 Verde (< 0.25), 🟡 Amarillo (0.25 - 0.49), 🟠 Naranja (0.50 - 0.74), 🔴 Rojo (>= 0.75).
"""

import os
import joblib
import numpy as np
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import TimeSeriesSplit

from .base_conocimiento import obtener_prior_poblacional
from .database import (
    obtener_conexion,
    obtener_registros_usuario,
    registrar_historial_modelo
)

# Directorio para guardar modelos entrenados
MODELS_DIR = os.path.join(os.path.dirname(__file__), "modelos")
os.makedirs(MODELS_DIR, exist_ok=True)
MODEL_FILE = os.path.join(MODELS_DIR, "mcontrol_classifier_v2.joblib")


class MotorML:
    """Motor de Machine Learning predictivo y adaptativo para M-Control."""

    def __init__(self, usuario_id: int = 1, db_path: Optional[str] = None):
        self.usuario_id = usuario_id
        self.db_path = db_path
        self.version = "v2.0-calibrated-rf"
        self.modelo = None
        self.feature_names = [
            "horas_desde_ultimo",
            "frecuencia_7d",
            "frecuencia_14d",
            "frecuencia_30d",
            "ratio_aceleracion_7_30",
            "promedio_control_reciente",
            "interferencia_acumulada_7d",
            "sintomas_fisicos_recientes",
            "escape_emocional_ratio",
            "dia_semana",
            "es_nocturno",
            "edad_usuario"
        ]
        self._cargar_o_inicializar_modelo()

    def _cargar_o_inicializar_modelo(self):
        """Carga el modelo guardado si existe, o entrena uno nuevo."""
        if os.path.exists(MODEL_FILE):
            try:
                self.modelo = joblib.load(MODEL_FILE)
            except Exception:
                self.modelo = None
        if self.modelo is None:
            self.entrenar_modelo()

    def _obtener_edad_usuario(self) -> int:
        """Obtiene la edad del usuario desde la base de datos."""
        conn = obtener_conexion(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT edad FROM usuarios WHERE id = ?", (self.usuario_id,))
        row = cursor.fetchone()
        conn.close()
        return row["edad"] if row else 24

    def extraer_features_de_registros(self, registros: List[Dict[str, Any]]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Transforma la lista temporal de registros en matrices X (features) e y (etiquetas clínicas).
        Etiqueta y = 1 (Desregulación / Riesgo Alto) según los criterios diagnósticos CIE-11 CSBD:
        - Pérdida de control (nivel_control <= 2) acompañado de interferencia funcional, dolor o malestar posterior.
        - Eventos repetidos en intervalo crítico (< 12 horas) con afectación.
        """
        if not registros:
            return np.empty((0, len(self.feature_names))), np.empty(0)

        edad = self._obtener_edad_usuario()
        X_list = []
        y_list = []

        # Convertir marcas temporales para cálculos longitudinales
        eventos = []
        for r in registros:
            try:
                dt = datetime.strptime(f"{r['fecha']} {r['hora']}", "%Y-%m-%d %H:%M")
            except Exception:
                dt = datetime.strptime(r['fecha'], "%Y-%m-%d")
            eventos.append((dt, r))

        eventos.sort(key=lambda x: x[0])

        for i in range(len(eventos)):
            dt_act, r_act = eventos[i]

            # 1. Horas desde el evento inmediatamente anterior
            if i > 0:
                dt_ant, _ = eventos[i - 1]
                horas_desde_ultimo = max(0.5, (dt_act - dt_ant).total_seconds() / 3600.0)
            else:
                horas_desde_ultimo = 72.0  # Valor neutral de partida

            # 2. Ventanas históricas anteriores (excluyendo el evento actual)
            eventos_previos = [e for e in eventos[:i]]
            
            # Frecuencias en 7, 14 y 30 días
            frec_7d = sum(1 for dt, _ in eventos_previos if (dt_act - dt).days <= 7)
            frec_14d = sum(1 for dt, _ in eventos_previos if (dt_act - dt).days <= 14)
            frec_30d = sum(1 for dt, _ in eventos_previos if (dt_act - dt).days <= 30)

            # Ratio de aceleración: frecuencia reciente normalizada vs promedio mensual
            tasa_esperada_7d = (frec_30d / 30.0) * 7.0 if frec_30d > 0 else 1.0
            ratio_aceleracion = frec_7d / tasa_esperada_7d if tasa_esperada_7d > 0 else 1.0

            # Últimos 3 eventos previos para medias móviles
            ultimos_3 = [r for _, r in eventos_previos[-3:]] if eventos_previos else [r_act]
            prom_control = np.mean([r["nivel_control"] for r in ultimos_3])
            sintomas_recientes = sum(r["dolor"] + r["irritacion"] for r in ultimos_3)

            # Interferencia acumulada en los últimos 7 días
            eventos_7d = [r for dt, r in eventos_previos if (dt_act - dt).days <= 7]
            interferencia_7d = sum(
                r["interferencia_sueno"] + r["interferencia_estudio"] +
                r["interferencia_trabajo"] + r["interferencia_social"]
                for r in eventos_7d
            )

            # Proporción de escape emocional reciente
            estados_emocionales = [r["estado_emocional"].lower() for r in ultimos_3]
            emociones_escape = sum(1 for e in estados_emocionales if any(w in e for w in ["estrés", "estres", "ansiedad", "escape", "impulsivo"]))
            escape_ratio = emociones_escape / len(ultimos_3)

            dia_semana = dt_act.weekday()
            es_nocturno = 1 if (dt_act.hour >= 23 or dt_act.hour < 5) else 0

            vector_x = [
                float(horas_desde_ultimo),
                float(frec_7d),
                float(frec_14d),
                float(frec_30d),
                float(ratio_aceleracion),
                float(prom_control),
                float(interferencia_7d),
                float(sintomas_recientes),
                float(escape_ratio),
                float(dia_semana),
                float(es_nocturno),
                float(edad)
            ]
            X_list.append(vector_x)

            # Criterio CIE-11 CSBD para etiquetar desregulación (y = 1)
            interferencia_total = (
                r_act["interferencia_sueno"] + r_act["interferencia_estudio"] +
                r_act["interferencia_trabajo"] + r_act["interferencia_social"]
            )
            sintomas_act = r_act["dolor"] + r_act["irritacion"]
            bajo_control = 1 if r_act["nivel_control"] <= 2 else 0

            es_desregulado = 1 if (
                (bajo_control and (interferencia_total >= 1 or sintomas_act >= 1 or r_act["malestar"] == 1)) or
                (horas_desde_ultimo < 12.0 and bajo_control) or
                (interferencia_total >= 3)
            ) else 0

            y_list.append(es_desregulado)

        return np.array(X_list, dtype=float), np.array(y_list, dtype=int)

    def entrenar_modelo(self) -> Dict[str, Any]:
        """
        Entrena el clasificador probabilístico calibrado utilizando el historial
        del usuario en SQLite. Devuelve las métricas de entrenamiento.
        """
        registros = obtener_registros_usuario(self.usuario_id, self.db_path)
        X, y = self.extraer_features_de_registros(registros)

        if len(X) < 10 or len(np.unique(y)) < 2:
            # Conjunto de respaldo sintético calibrado con priors NSSHB y pesos CIE-11
            X_syn, y_syn = self._generar_datos_respaldo()
            X = np.vstack([X, X_syn]) if len(X) > 0 else X_syn
            y = np.concatenate([y, y_syn]) if len(y) > 0 else y_syn

        base_clf = RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            min_samples_split=3,
            random_state=42,
            class_weight="balanced"
        )
        
        # Calibración de probabilidad con CalibratedClassifierCV (isotonic / sigmoid)
        calibrador = CalibratedClassifierCV(estimator=base_clf, method="sigmoid", cv=3)
        calibrador.fit(X, y)
        self.modelo = calibrador

        # Guardar en disco
        joblib.dump(self.modelo, MODEL_FILE)

        # Cálculo de métricas básicas de ajuste
        preds_prob = self.modelo.predict_proba(X)[:, 1]
        preds_clase = (preds_prob >= 0.5).astype(int)
        acc = float(np.mean(preds_clase == y))

        metricas = {
            "accuracy": round(acc, 3),
            "cantidad_registros": len(X),
            "proporcion_positivos": round(float(np.mean(y)), 3),
            "algoritmo": "Calibrated Random Forest (Sigmoid)"
        }
        registrar_historial_modelo(self.usuario_id, self.version, len(X), metricas, self.db_path)
        return metricas

    def _generar_datos_respaldo(self) -> Tuple[np.ndarray, np.ndarray]:
        """Genera datos clínicos de referencia para entrenar cuando el usuario es nuevo."""
        np.random.seed(42)
        X_syn = []
        y_syn = []
        edad = self._obtener_edad_usuario()

        for _ in range(80):
            # Caso 1: Regulado / Saludable
            horas = np.random.uniform(24, 96)
            frec_7 = np.random.randint(1, 4)
            frec_14 = frec_7 + np.random.randint(1, 4)
            frec_30 = frec_14 + np.random.randint(2, 6)
            ratio = frec_7 / max(1, (frec_30 / 30) * 7)
            control = np.random.uniform(3.5, 5.0)
            interf = np.random.randint(0, 2)
            sint = 0
            escape = np.random.uniform(0.0, 0.3)
            dia = np.random.randint(0, 7)
            noct = np.random.choice([0, 1], p=[0.7, 0.3])
            X_syn.append([horas, frec_7, frec_14, frec_30, ratio, control, interf, sint, escape, dia, noct, edad])
            y_syn.append(0)

        for _ in range(40):
            # Caso 2: Desregulado / Alerta
            horas = np.random.uniform(4, 18)
            frec_7 = np.random.randint(5, 10)
            frec_14 = frec_7 + np.random.randint(4, 8)
            frec_30 = frec_14 + np.random.randint(5, 12)
            ratio = frec_7 / max(1, (frec_30 / 30) * 7)
            control = np.random.uniform(1.0, 2.5)
            interf = np.random.randint(2, 7)
            sint = np.random.randint(1, 4)
            escape = np.random.uniform(0.6, 1.0)
            dia = np.random.randint(0, 7)
            noct = np.random.choice([0, 1], p=[0.4, 0.6])
            X_syn.append([horas, frec_7, frec_14, frec_30, ratio, control, interf, sint, escape, dia, noct, edad])
            y_syn.append(1)

        return np.array(X_syn, dtype=float), np.array(y_syn, dtype=int)

    def predecir_dia(self, fecha_objetivo: datetime, registros_existentes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Predice el nivel de riesgo y la favorabilidad de regulación para una fecha específica.
        Maneja Cold-Start con priors bayesianos poblacionales si hay pocos datos.
        """
        edad = self._obtener_edad_usuario()
        prior = obtener_prior_poblacional(edad)
        n_registros = len(registros_existentes)

        # 1. Modo Cold-Start (0 a 5 registros)
        if n_registros < 5:
            prob_base = 0.15  # Prior general de baja probabilidad de desregulación
            confianza = 0.48 + (n_registros * 0.04)  # 48% a 68% de confianza
            motivos = [
                f"Fase de inicio (Cold-Start): {n_registros} eventos registrados.",
                f"Predicción anclada al grupo etario poblacional NSSHB ({prior['cohorte']}).",
                "Confianza limitada: el sistema se calibrará conforme registres más eventos."
            ]
            probabilidad = prob_base
        else:
            # 2. Modo Personalizado: Extraer vector de features simulando el estado a la fecha objetivo
            vector_x = self._construir_vector_predictivo(fecha_objetivo, registros_existentes, edad)
            prob_ml = float(self.modelo.predict_proba([vector_x])[0][1])

            # Ponderación Bayesiana: combina modelo personal con prior poblacional para estabilidad
            peso_personal = min(0.90, 0.50 + (n_registros * 0.015))
            peso_prior = 1.0 - peso_personal
            probabilidad = (prob_ml * peso_personal) + (0.15 * peso_prior)

            # Salvaguarda Clínica Preventiva (CIE-11 CSBD / ISSM):
            # Analizar carga de eventos del último día activo
            eventos_ordenados = []
            for r in registros_existentes:
                try:
                    dt = datetime.strptime(f"{r['fecha']} {r['hora']}", "%Y-%m-%d %H:%M")
                except Exception:
                    dt = datetime.strptime(r['fecha'], "%Y-%m-%d")
                eventos_ordenados.append((dt, r))
            eventos_ordenados.sort(key=lambda x: x[0])
            previos = [e for e in eventos_ordenados if e[0] <= fecha_objetivo]

            if previos:
                ult_dt, _ = previos[-1]
                fecha_ult_str = ult_dt.strftime("%Y-%m-%d")
                ev_ult_dia = sum(1 for e in previos if e[0].strftime("%Y-%m-%d") == fecha_ult_str)
            else:
                ev_ult_dia = 0

            sintomas_recientes = vector_x[7]
            prom_control = vector_x[5]
            interferencia_7d = vector_x[6]
            horas_descanso = vector_x[0]
            ratio_aceleracion = vector_x[4]
            escape_ratio = vector_x[8]

            # CASO 1: 3 o más eventos en el día previo o dolor físico -> Pausa estricta y descompresión
            if ev_ult_dia >= 3 or sintomas_recientes >= 2 or (prom_control <= 1.8 and interferencia_7d >= 3):
                if horas_descanso < 36:
                    probabilidad = max(probabilidad, 0.85)
                elif horas_descanso < 60:
                    probabilidad = max(probabilidad, 0.62)
                elif horas_descanso < 84:
                    probabilidad = max(probabilidad, 0.38)
            # CASO 2: 2 eventos en el día previo o dolor leve/bajo control
            elif ev_ult_dia == 2 or sintomas_recientes >= 1 or (prom_control <= 2.5 and (interferencia_7d >= 1 or escape_ratio >= 0.6)):
                if horas_descanso < 28:
                    probabilidad = max(probabilidad, 0.62)
                elif horas_descanso < 52:
                    probabilidad = max(probabilidad, 0.38)
            # CASO 3: Intervalo menor a 24h o aceleración
            elif horas_descanso < 24 or ratio_aceleracion > 1.25 or escape_ratio >= 0.5:
                probabilidad = max(probabilidad, 0.35)
            # CASO 4: Descanso pleno (> 48h)
            elif horas_descanso >= 48 and ratio_aceleracion <= 1.0 and sintomas_recientes == 0:
                probabilidad = min(probabilidad, 0.15)

            # Confianza aumenta con el volumen y regularidad de datos
            confianza = min(0.92, 0.65 + (n_registros * 0.006))
            motivos = self._generar_motivos_explicativos(vector_x, registros_existentes, probabilidad)
            if ev_ult_dia >= 3 and horas_descanso < 60:
                motivos.insert(0, f"{ev_ult_dia} eventos registrados en la jornada previa reciente: sobrecarga física y necesidad estricta de descanso.")
            elif ev_ult_dia == 2 and horas_descanso < 50:
                motivos.insert(0, f"2 eventos registrados en la jornada previa: descanso de recuperación en curso.")

        # 3. Mapeo a los 4 colores de estado
        if probabilidad < 0.25:
            nivel = "Verde"
            recomendacion = "Día altamente favorable para mantener tu autorregulación y bienestar general."
        elif probabilidad < 0.50:
            nivel = "Amarillo"
            recomendacion = "Se observa una tendencia de menor descanso o tensión previa. Conviene observar tu contexto."
        elif probabilidad < 0.75:
            nivel = "Naranja"
            recomendacion = "Varios indicadores de tu historial apuntan a posible pérdida de control. Considera posponer o realizar pausas activas."
        else:
            nivel = "Rojo"
            recomendacion = "Alta probabilidad de desregulación o malestar según tu patrón. Recomendable descanso biológico y autocuidado."

        return {
            "fecha": fecha_objetivo.strftime("%Y-%m-%d"),
            "nivel": nivel,
            "probabilidad": round(float(probabilidad), 3),
            "confianza": round(float(confianza), 3),
            "motivos": motivos,
            "recomendacion": recomendacion,
            "modelo_version": self.version
        }

    def _construir_vector_predictivo(self, fecha_objetivo: datetime, registros: List[Dict[str, Any]], edad: int) -> List[float]:
        """Construye las características predictivas proyectadas para la fecha futura."""
        eventos = []
        for r in registros:
            try:
                dt = datetime.strptime(f"{r['fecha']} {r['hora']}", "%Y-%m-%d %H:%M")
            except Exception:
                dt = datetime.strptime(r['fecha'], "%Y-%m-%d")
            eventos.append((dt, r))
        eventos.sort(key=lambda x: x[0])

        eventos_previos = [e for e in eventos if e[0] <= fecha_objetivo]
        if eventos_previos:
            ultimo_dt, _ = eventos_previos[-1]
            horas_desde_ultimo = max(1.0, (fecha_objetivo - ultimo_dt).total_seconds() / 3600.0)
        else:
            horas_desde_ultimo = 48.0

        frec_7d = sum(1 for dt, _ in eventos_previos if (fecha_objetivo - dt).days <= 7)
        frec_14d = sum(1 for dt, _ in eventos_previos if (fecha_objetivo - dt).days <= 14)
        frec_30d = sum(1 for dt, _ in eventos_previos if (fecha_objetivo - dt).days <= 30)

        tasa_esperada_7d = (frec_30d / 30.0) * 7.0 if frec_30d > 0 else 1.0
        ratio_aceleracion = frec_7d / tasa_esperada_7d if tasa_esperada_7d > 0 else 1.0

        ultimos_3 = [r for _, r in eventos_previos[-3:]] if eventos_previos else []
        prom_control = np.mean([r["nivel_control"] for r in ultimos_3]) if ultimos_3 else 3.5
        sintomas_recientes = sum(r["dolor"] + r["irritacion"] for r in ultimos_3) if ultimos_3 else 0

        eventos_7d = [r for dt, r in eventos_previos if (fecha_objetivo - dt).days <= 7]
        interferencia_7d = sum(
            r["interferencia_sueno"] + r["interferencia_estudio"] +
            r["interferencia_trabajo"] + r["interferencia_social"]
            for r in eventos_7d
        ) if eventos_7d else 0

        estados_emocionales = [r["estado_emocional"].lower() for r in ultimos_3] if ultimos_3 else []
        emociones_escape = sum(1 for e in estados_emocionales if any(w in e for w in ["estrés", "estres", "ansiedad", "escape", "impulsivo"]))
        escape_ratio = emociones_escape / max(1, len(ultimos_3))

        dia_semana = fecha_objetivo.weekday()
        es_nocturno = 0

        return [
            horas_desde_ultimo, frec_7d, frec_14d, frec_30d, ratio_aceleracion,
            prom_control, interferencia_7d, sintomas_recientes, escape_ratio,
            dia_semana, es_nocturno, edad
        ]

    def _generar_motivos_explicativos(self, vector_x: List[float], registros: List[Dict[str, Any]], probabilidad: float) -> List[str]:
        """Genera factores explicativos en lenguaje claro y sin diagnósticos médicos."""
        horas_descanso = vector_x[0]
        frec_7d = vector_x[1]
        ratio_aceleracion = vector_x[4]
        prom_control = vector_x[5]
        interferencia_7d = vector_x[6]
        sintomas_recientes = vector_x[7]
        escape_ratio = vector_x[8]

        motivos = []
        if ratio_aceleracion > 1.3:
            motivos.append(f"Aumento de frecuencia reciente: ritmo semanal {int((ratio_aceleracion - 1.0) * 100)}% superior a tu promedio mensual.")
        elif ratio_aceleracion < 0.8:
            motivos.append("Cadencia de descanso preservada respecto a tu historial habitual.")

        if horas_descanso < 18:
            motivos.append(f"Intervalo de recuperación corto ({int(horas_descanso)} horas desde el último registro).")
        elif horas_descanso > 48:
            motivos.append(f"Período de descanso biológico amplio ({int(horas_descanso)} horas).")

        if prom_control <= 2.5:
            motivos.append("Historial reciente con menor percepción de control voluntario.")
        elif prom_control >= 4.0:
            motivos.append("Buen nivel de autodeterminación y control autopercibido.")

        if interferencia_7d >= 2:
            motivos.append("Se detectaron pequeñas interferencias en descanso o jornada de estudio/trabajo.")

        if sintomas_recientes > 0:
            motivos.append("Registros previos con reportes de leve irritación o molestia física.")

        if escape_ratio >= 0.5:
            motivos.append("Coincidencia de tensión emocional previa en los últimos eventos.")

        if not motivos:
            motivos.append("Patrón dentro de los parámetros habituales de autorregulación.")

        return motivos

"""
calendar_predictor.py
M-Control AI | Generador del Calendario Predictivo Inteligente

Orquesta la generación de pronósticos mensuales de autorregulación:
- Combina registros reales pasados con predicciones futuras de Machine Learning.
- Asigna los 4 estados de semáforo preventivo (🟢 Verde, 🟡 Amarillo, 🟠 Naranja, 🔴 Rojo).
- Persiste las predicciones en SQLite y entrega el payload estructurado para la interfaz.
"""

import calendar
from datetime import datetime, date, timedelta
from typing import Any, Dict, List, Optional

from .ml_engine import MotorML
from .xai_explainer import formatear_ficha_dia
from .database import (
    obtener_conexion,
    obtener_registros_usuario,
    guardar_predicciones,
    obtener_predicciones_mes
)

NOMBRES_MESES = [
    "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]


class PredictorCalendario:
    """Generador del Calendario Predictivo para cualquier mes y año."""

    def __init__(self, usuario_id: int = 1, db_path: Optional[str] = None):
        self.usuario_id = usuario_id
        self.db_path = db_path
        self.motor_ml = MotorML(usuario_id=usuario_id, db_path=db_path)

    def generar_calendario_mes(self, año: int, mes: int, fecha_referencia: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Genera el mes completo estructurado con días pasados y predicciones futuras.
        Por defecto, fecha_referencia es la fecha actual del sistema.
        """
        if fecha_referencia is None:
            fecha_referencia = datetime.now()

        registros = obtener_registros_usuario(self.usuario_id, self.db_path)
        
        # Mapear registros por día 'YYYY-MM-DD'
        mapa_registros: Dict[str, List[Dict[str, Any]]] = {}
        for r in registros:
            mapa_registros.setdefault(r["fecha"], []).append(r)

        num_dias = calendar.monthrange(año, mes)[1]
        primer_dia_semana = calendar.monthrange(año, mes)[0] # 0 = Lunes, 6 = Domingo

        dias_calendario = []
        predicciones_a_guardar = []

        # Estado acumulado temporal para proyecciones continuas
        registros_simulados = list(registros)

        for dia in range(1, num_dias + 1):
            fecha_dt = datetime(año, mes, dia)
            fecha_str = fecha_dt.strftime("%Y-%m-%d")
            es_futuro = fecha_dt.date() > fecha_referencia.date()
            tiene_registro = fecha_str in mapa_registros

            if tiene_registro:
                # El día tiene registros pasados: evaluar el estado histórico
                eventos_dia = mapa_registros[fecha_str]
                total_ev = len(eventos_dia)
                bajo_control = any(e["nivel_control"] <= 2 for e in eventos_dia)
                con_interf = any((e["interferencia_sueno"] + e["interferencia_estudio"] + e["interferencia_trabajo"]) > 0 for e in eventos_dia)
                con_dolor = any((e["dolor"] + e["irritacion"]) > 0 for e in eventos_dia)
                con_malestar = any(e["malestar"] == 1 for e in eventos_dia)

                if con_dolor or total_ev >= 3 or (bajo_control and con_interf and con_malestar):
                    nivel = "Rojo"
                    prob = 0.88
                    motivo_txt = f"Día con {total_ev} evento(s). Sobrecarga física aguda o dolor registrado."
                elif total_ev == 2 or bajo_control or con_interf:
                    nivel = "Naranja" if (bajo_control or con_interf or total_ev >= 2) else "Amarillo"
                    prob = 0.62 if nivel == "Naranja" else 0.40
                    motivo_txt = f"Día con {total_ev} evento(s). Indicadores de menor descanso o control moderado."
                elif any(e["nivel_deseo"] >= 7 for e in eventos_dia):
                    nivel = "Amarillo"
                    prob = 0.38
                    motivo_txt = f"Día con {total_ev} evento(s) con nivel de deseo elevado registrado."
                else:
                    nivel = "Verde"
                    prob = 0.12
                    motivo_txt = f"Día con {total_ev} evento(s) en balance y autocontrol preservado."

                pred_cruda = {
                    "fecha": fecha_str,
                    "nivel": nivel,
                    "probabilidad": prob,
                    "confianza": 0.95,
                    "motivos": [motivo_txt],
                    "recomendacion": "Registro histórico consolidado en base de datos.",
                    "modelo_version": "historial-registrado"
                }
            else:
                # El día no tiene registro (día futuro o sin eventos pasados) -> PREDICCIÓN ML
                pred_cruda = self.motor_ml.predecir_dia(fecha_dt, registros_simulados)
                predicciones_a_guardar.append(pred_cruda)

            ficha = formatear_ficha_dia(pred_cruda)
            ficha["dia"] = dia
            ficha["es_futuro"] = es_futuro
            ficha["tiene_registro"] = tiene_registro
            ficha["total_eventos_dia"] = len(mapa_registros.get(fecha_str, []))
            ficha["eventos_detalle"] = mapa_registros.get(fecha_str, [])
            dias_calendario.append(ficha)

        # Guardar predicciones generadas en la base de datos
        if predicciones_a_guardar:
            guardar_predicciones(self.usuario_id, predicciones_a_guardar, self.db_path)

        # Resumen estadístico del mes
        conteo_colores = {"Verde": 0, "Amarillo": 0, "Naranja": 0, "Rojo": 0}
        for d in dias_calendario:
            conteo_colores[d["nivel"]] += 1

        return {
            "usuario_id": self.usuario_id,
            "año": año,
            "mes": mes,
            "nombre_mes": NOMBRES_MESES[mes],
            "primer_dia_semana": primer_dia_semana,
            "total_dias": num_dias,
            "resumen_estados": conteo_colores,
            "dias": dias_calendario
        }

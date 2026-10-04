"""
api_service.py
M-Control AI | Servidor Local API REST y Puente Web

Servidor HTTP nativo en Python (sin dependencias externas pesadas) que expone
los endpoints del sistema de IA para interactuar con la interfaz de M-Control:
- GET /api/calendar?year=2026&month=10 : Retorna el calendario mensual predictivo.
- GET /api/prediction?date=YYYY-MM-DD  : Retorna la ficha explicativa de un día.
- POST /api/records                     : Registra nuevo evento y actualiza el modelo.
- GET /api/knowledge-base              : Retorna las fuentes científicas y NSSHB.
- GET /api/metrics                     : Retorna reporte de validación del modelo.
- Servidor de archivos estáticos para la carpeta Proyecto/
"""

import json
import os
import urllib.parse
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Any, Dict

from .base_conocimiento import obtener_fuentes, DATOS_POBLACIONALES_NSSHB
from .calendar_predictor import PredictorCalendario
from .database import insertar_registro, obtener_conexion, sembrar_datos_iniciales, inicializar_base_datos
from .evaluador_metricas import ejecutar_suite_validacion
from .ml_engine import MotorML
from .privacy import exportar_datos_usuario_json, purgar_datos_usuario

PROYECTO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Proyecto")


class MControlAPIHandler(SimpleHTTPRequestHandler):
    """Manejador HTTP que combina la API de IA con el frontend estático."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PROYECTO_DIR, **kwargs)

    def _responder_json(self, data: Any, status: int = 200):
        """Envía respuesta en formato JSON con cabeceras CORS."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))

    def do_OPTIONS(self):
        """Manejo de pre-flight CORS."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        """Maneja solicitudes GET a la API o sirve archivos estáticos."""
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        # 1. Calendario predictivo
        if parsed.path == "/api/calendar":
            año = int(params.get("year", [datetime.now().year])[0])
            mes = int(params.get("month", [datetime.now().month])[0])
            predictor = PredictorCalendario(usuario_id=1)
            calendario_data = predictor.generar_calendario_mes(año, mes)
            return self._responder_json(calendario_data)

        # 2. Predicción de un día específico
        elif parsed.path == "/api/prediction":
            fecha_str = params.get("date", [datetime.now().strftime("%Y-%m-%d")])[0]
            try:
                dt = datetime.strptime(fecha_str, "%Y-%m-%d")
            except Exception:
                dt = datetime.now()
            predictor = PredictorCalendario(usuario_id=1)
            cal = predictor.generar_calendario_mes(dt.year, dt.month)
            for d in cal["dias"]:
                if d["fecha"] == fecha_str:
                    return self._responder_json(d)
            return self._responder_json({"error": "Día no encontrado"}, 404)

        # 3. Base de conocimiento científico
        elif parsed.path == "/api/knowledge-base":
            return self._responder_json({
                "fuentes": obtener_fuentes(),
                "nsshb_cohortes": DATOS_POBLACIONALES_NSSHB
            })

        # 4. Métricas de validación del modelo de IA
        elif parsed.path == "/api/metrics":
            metricas = ejecutar_suite_validacion(usuario_id=1)
            return self._responder_json(metricas)

        # 5. Exportar datos JSON del usuario
        elif parsed.path == "/api/export":
            export_str = exportar_datos_usuario_json(usuario_id=1)
            return self._responder_json(json.loads(export_str))

        # En caso contrario, servir archivo estático desde Proyecto/
        return super().do_GET()

    def do_POST(self):
        """Maneja solicitudes POST (registro de eventos o entrenamiento)."""
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/api/records":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            try:
                datos = json.loads(body)
            except Exception:
                return self._responder_json({"error": "JSON malformado"}, 400)

            reg_id = insertar_registro(1, datos)

            # Re-entrenamiento incremental del modelo de Machine Learning
            motor = MotorML(usuario_id=1)
            metricas_entrenamiento = motor.entrenar_modelo()

            # Re-generar predicciones del mes actual
            predictor = PredictorCalendario(usuario_id=1)
            ahora = datetime.now()
            predictor.generar_calendario_mes(ahora.year, ahora.month)

            return self._responder_json({
                "status": "ok",
                "registro_id": reg_id,
                "mensaje": "Evento guardado y modelo re-calibrado con éxito",
                "metricas_modelo": metricas_entrenamiento
            }, 201)

        elif parsed.path == "/api/reset":
            purgar_datos_usuario(1)
            sembrar_datos_iniciales(1)
            motor = MotorML(usuario_id=1)
            motor.entrenar_modelo()
            return self._responder_json({"status": "ok", "mensaje": "Datos restablecidos con éxito"})

        return self._responder_json({"error": "Endpoint no encontrado"}, 404)


def iniciar_servidor(puerto: int = 8088):
    """Inicia el servidor local de M-Control AI."""
    inicializar_base_datos()
    sembrar_datos_iniciales(1)
    server_address = ("", puerto)
    httpd = HTTPServer(server_address, MControlAPIHandler)
    print("=" * 60)
    print(f"  M-CONTROL AI | SERVIDOR PREDICTIVO ACTIVO")
    print(f"  URL Local:  http://localhost:{puerto}")
    print(f"  Directorio: {PROYECTO_DIR}")
    print("=" * 60)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
        httpd.server_close()


if __name__ == "__main__":
    iniciar_servidor(8088)

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
from .database import (
    insertar_registro, obtener_conexion, sembrar_datos_iniciales, inicializar_base_datos,
    listar_usuarios, obtener_usuario, autenticar_usuario, crear_usuario, obtener_registros_usuario
)
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

        # 1. Calendario predictivo por usuario
        if parsed.path == "/api/calendar":
            año = int(params.get("year", [datetime.now().year])[0])
            mes = int(params.get("month", [datetime.now().month])[0])
            usuario_id = int(params.get("user_id", params.get("usuario_id", [1]))[0])
            predictor = PredictorCalendario(usuario_id=usuario_id)
            calendario_data = predictor.generar_calendario_mes(año, mes)
            return self._responder_json(calendario_data)

        # 2. Listado de usuarios / perfiles registrados
        elif parsed.path == "/api/users":
            usuarios = listar_usuarios()
            return self._responder_json(usuarios)

        # 3. Predicción de un día específico
        elif parsed.path == "/api/prediction":
            fecha_str = params.get("date", [datetime.now().strftime("%Y-%m-%d")])[0]
            usuario_id = int(params.get("user_id", params.get("usuario_id", [1]))[0])
            try:
                dt = datetime.strptime(fecha_str, "%Y-%m-%d")
            except Exception:
                dt = datetime.now()
            predictor = PredictorCalendario(usuario_id=usuario_id)
            cal = predictor.generar_calendario_mes(dt.year, dt.month)
            for d in cal["dias"]:
                if d["fecha"] == fecha_str:
                    return self._responder_json(d)
            return self._responder_json({"error": "Día no encontrado"}, 404)

        # 4. Registros históricos del usuario
        elif parsed.path == "/api/records":
            usuario_id = int(params.get("user_id", params.get("usuario_id", [1]))[0])
            registros = obtener_registros_usuario(usuario_id)
            return self._responder_json(registros)

        # 5. Base de conocimiento científico
        elif parsed.path == "/api/knowledge-base":
            return self._responder_json({
                "fuentes": obtener_fuentes(),
                "nsshb_cohortes": DATOS_POBLACIONALES_NSSHB
            })

        # 6. Métricas de validación del modelo de IA por usuario
        elif parsed.path == "/api/metrics":
            usuario_id = int(params.get("user_id", params.get("usuario_id", [1]))[0])
            metricas = ejecutar_suite_validacion(usuario_id=usuario_id)
            return self._responder_json(metricas)

        # 7. Exportar datos JSON del usuario
        elif parsed.path == "/api/export":
            usuario_id = int(params.get("user_id", params.get("usuario_id", [1]))[0])
            export_str = exportar_datos_usuario_json(usuario_id=usuario_id)
            return self._responder_json(json.loads(export_str))

        # En caso contrario, servir archivo estático desde Proyecto/
        return super().do_GET()

    def do_POST(self):
        """Maneja solicitudes POST (registro de eventos o entrenamiento)."""
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/api/users/login":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            try:
                datos = json.loads(body)
            except Exception:
                return self._responder_json({"error": "JSON malformado"}, 400)

            alias = datos.get("alias", "").strip()
            pin = str(datos.get("pin", "1234")).strip()
            usuario = autenticar_usuario(alias, pin)
            if usuario:
                return self._responder_json({"status": "ok", "user": usuario})
            else:
                # Si no existe, crearlo automáticamente para facilitar onboarding de participantes
                nuevo_user = crear_usuario(alias, edad=int(datos.get("edad", 24)), objetivo_personal=datos.get("objetivo", "Autorregulación"), pin=pin)
                return self._responder_json({"status": "ok", "user": nuevo_user, "nuevo": True}, 201)

        elif parsed.path == "/api/users/register":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            try:
                datos = json.loads(body)
            except Exception:
                return self._responder_json({"error": "JSON malformado"}, 400)

            alias = datos.get("alias", f"Participante {len(listar_usuarios()) + 1}").strip()
            edad = int(datos.get("edad", 24))
            objetivo = datos.get("objetivo", "Autorregulación y Bienestar").strip()
            pin = str(datos.get("pin", "1234")).strip()
            nuevo_user = crear_usuario(alias, edad, objetivo, pin)
            return self._responder_json({"status": "ok", "user": nuevo_user}, 201)

        elif parsed.path == "/api/records":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            try:
                datos = json.loads(body)
            except Exception:
                return self._responder_json({"error": "JSON malformado"}, 400)

            usuario_id = int(datos.get("usuario_id", datos.get("user_id", 1)))
            reg_id = insertar_registro(usuario_id, datos)

            # Re-entrenamiento incremental del modelo de Machine Learning para este usuario
            motor = MotorML(usuario_id=usuario_id)
            metricas_entrenamiento = motor.entrenar_modelo()

            # Re-generar predicciones del mes actual
            predictor = PredictorCalendario(usuario_id=usuario_id)
            ahora = datetime.now()
            predictor.generar_calendario_mes(ahora.year, ahora.month)

            return self._responder_json({
                "status": "ok",
                "registro_id": reg_id,
                "usuario_id": usuario_id,
                "mensaje": "Evento guardado y modelo re-calibrado con éxito",
                "metricas_modelo": metricas_entrenamiento
            }, 201)

        elif parsed.path == "/api/reset":
            usuario_id = 1
            purgar_datos_usuario(usuario_id)
            sembrar_datos_iniciales(usuario_id)
            motor = MotorML(usuario_id=usuario_id)
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

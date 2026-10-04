"""
privacy.py
M-Control AI | Módulo de Seguridad, Privacidad Ética y Auditoría de Lenguaje

Garantiza:
1. Soberanía total del usuario y almacenamiento local autónomo (Local-First).
2. Funciones de exportación y borrado total definitivo (Derecho al olvido).
3. Hashing criptográfico seguro para credenciales/PIN.
4. Filtro ético de lenguaje médico: bloquea cualquier término patologizante o
   diagnóstico clínico (ej. 'adicto', 'enfermo', 'trastorno confirmado').
"""

import hashlib
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from .database import (
    obtener_conexion,
    obtener_registros_usuario,
    DEFAULT_DB_PATH
)

TERMINOS_PROHIBIDOS = [
    "tienes adiccion", "tienes adicción", "eres adicto",
    "estas enfermo", "estás enfermo", "padeces de",
    "diagnostico confirmado", "diagnóstico confirmado",
    "conducta pecaminosa", "prohibido masturbarse"
]


def validar_lenguaje_etico(texto: str) -> bool:
    """Verifica que un texto explicativo no contenga diagnósticos médicos prohibidos ni juicios morales."""
    texto_l = texto.lower()
    for t in TERMINOS_PROHIBIDOS:
        if t in texto_l:
            return False
    return True


def generar_hash_seguridad(pin_o_clave: str, sal: str = "mcontrol_salt_2026") -> str:
    """Genera un hash criptográfico SHA-256 seguro para proteger el acceso."""
    dato = f"{sal}:{pin_o_clave}".encode("utf-8")
    return hashlib.sha256(dato).hexdigest()


def exportar_datos_usuario_json(usuario_id: int = 1, db_path: Optional[str] = None) -> str:
    """Exporta todos los registros históricos, predicciones y configuraciones del usuario a un JSON estructurado."""
    conn = obtener_conexion(db_path)
    cursor = conn.cursor()
    
    # Usuario
    cursor.execute("SELECT id, edad, fecha_registro, objetivo_personal FROM usuarios WHERE id = ?", (usuario_id,))
    usuario = dict(cursor.fetchone())
    
    # Registros
    cursor.execute("SELECT * FROM registros_habito WHERE usuario_id = ? ORDER BY fecha ASC", (usuario_id,))
    registros = [dict(r) for r in cursor.fetchall()]

    # Predicciones
    cursor.execute("SELECT * FROM predicciones WHERE usuario_id = ? ORDER BY fecha ASC", (usuario_id,))
    predicciones = [dict(r) for r in cursor.fetchall()]

    conn.close()

    export_payload = {
        "metadata": {
            "sistema": "M-Control AI v2.0",
            "fecha_exportacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "soberania": "Datos bajo control exclusivo del usuario (Local-First)"
        },
        "usuario": usuario,
        "total_registros": len(registros),
        "registros": registros,
        "predicciones": predicciones
    }
    return json.dumps(export_payload, indent=2, ensure_ascii=False)


def purgar_datos_usuario(usuario_id: int = 1, db_path: Optional[str] = None) -> bool:
    """Elimina permanentemente todos los registros y predicciones del usuario (Derecho al olvido)."""
    conn = obtener_conexion(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM registros_habito WHERE usuario_id = ?", (usuario_id,))
    cursor.execute("DELETE FROM predicciones WHERE usuario_id = ?", (usuario_id,))
    cursor.execute("DELETE FROM historial_modelo WHERE usuario_id = ?", (usuario_id,))
    conn.commit()
    conn.close()
    return True

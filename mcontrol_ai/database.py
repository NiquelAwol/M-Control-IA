"""
database.py
M-Control AI | Capa de Persistencia y Base de Datos Relacional SQLite

Implementa el esquema relacional de 6 tablas requeridas por la arquitectura:
1. usuarios
2. fuentes_cientificas
3. datos_cientificos
4. registros_habito
5. predicciones
6. historial_modelo
"""

import json
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from .base_conocimiento import DATOS_POBLACIONALES_NSSHB, FUENTES_CIENTIFICAS

# Ruta predeterminada de la base de datos dentro del proyecto
DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mcontrol_ai.db")


def obtener_conexion(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Retorna una conexión a SQLite con soporte de claves foráneas y filas como diccionarios."""
    path = db_path or DEFAULT_DB_PATH
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def inicializar_base_datos(db_path: Optional[str] = None) -> str:
    """
    Crea las 6 tablas relacionales y puebla las fuentes científicas
    y datos poblacionales del NSSHB si la base está vacía.
    """
    path = db_path or DEFAULT_DB_PATH
    conn = obtener_conexion(path)
    cursor = conn.cursor()

    # 1. Tabla de Usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alias TEXT NOT NULL DEFAULT 'Participante 1',
        pin TEXT DEFAULT '1234',
        edad INTEGER NOT NULL DEFAULT 24,
        fecha_registro TEXT NOT NULL,
        objetivo_personal TEXT NOT NULL DEFAULT 'Autorregulación',
        hash_seguridad TEXT
    );
    """)
    # Asegurar columnas alias y pin en bases de datos ya existentes
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN alias TEXT DEFAULT 'Participante 1';")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN pin TEXT DEFAULT '1234';")
    except Exception:
        pass

    # 2. Tabla de Fuentes Científicas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fuentes_cientificas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        institucion TEXT NOT NULL,
        url TEXT NOT NULL,
        año INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        poblacion TEXT,
        muestra INTEGER,
        tema TEXT,
        contenido TEXT,
        nivel_evidencia TEXT
    );
    """)

    # 3. Tabla de Datos Científicos Poblacionales
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datos_cientificos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fuente_id INTEGER NOT NULL,
        edad_min INTEGER NOT NULL,
        edad_max INTEGER NOT NULL,
        frecuencia TEXT NOT NULL,
        porcentaje REAL NOT NULL,
        contexto TEXT,
        FOREIGN KEY (fuente_id) REFERENCES fuentes_cientificas (id) ON DELETE CASCADE
    );
    """)

    # 4. Tabla de Registros del Hábito
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registros_habito (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        hora TEXT NOT NULL,
        duracion INTEGER DEFAULT 15,
        realizo_habito INTEGER NOT NULL DEFAULT 1,
        nivel_deseo INTEGER DEFAULT 5,
        nivel_control INTEGER NOT NULL DEFAULT 3,
        estado_emocional TEXT DEFAULT 'Calma',
        interferencia_sueno INTEGER DEFAULT 0,
        interferencia_estudio INTEGER DEFAULT 0,
        interferencia_trabajo INTEGER DEFAULT 0,
        interferencia_social INTEGER DEFAULT 0,
        dolor INTEGER DEFAULT 0,
        irritacion INTEGER DEFAULT 0,
        malestar INTEGER DEFAULT 0,
        observaciones TEXT,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
    );
    """)

    # 5. Tabla de Predicciones del Modelo
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predicciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        nivel TEXT NOT NULL,
        probabilidad REAL NOT NULL,
        confianza REAL NOT NULL,
        motivos TEXT NOT NULL,
        recomendacion TEXT NOT NULL,
        modelo_version TEXT NOT NULL,
        fecha_generacion TEXT NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE,
        UNIQUE(usuario_id, fecha)
    );
    """)

    # 6. Tabla de Historial y Versionado del Modelo
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial_modelo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        modelo_version TEXT NOT NULL,
        fecha_entrenamiento TEXT NOT NULL,
        cantidad_datos INTEGER NOT NULL,
        metricas TEXT NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
    );
    """)

    conn.commit()

    # --- POBLAR FUENTES CIENTÍFICAS SI ESTÁ VACÍA ---
    cursor.execute("SELECT COUNT(*) AS total FROM fuentes_cientificas;")
    if cursor.fetchone()["total"] == 0:
        for f in FUENTES_CIENTIFICAS:
            cursor.execute("""
            INSERT INTO fuentes_cientificas (id, nombre, institucion, url, año, tipo, poblacion, muestra, tema, contenido, nivel_evidencia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f["id"], f["nombre"], f["institucion"], f["url"], f["año"],
                f["tipo"], f["poblacion"], f["muestra"], f["tema"],
                f["contenido"], f["nivel_evidencia"]
            ))

        # Población NSSHB vinculada a fuente_id = 2 (NSSHB)
        for dp in DATOS_POBLACIONALES_NSSHB:
            cursor.execute("""
            INSERT INTO datos_cientificos (fuente_id, edad_min, edad_max, frecuencia, porcentaje, contexto)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                2, dp["edad_min"], dp["edad_max"], dp["frecuencia"],
                dp["porcentaje"], f"Encuesta probabilística estadounidense NSSHB para cohorte {dp['edad_min']}-{dp['edad_max']} años"
            ))
        conn.commit()

    # --- CREAR USUARIOS POR DEFECTO SI NO EXISTEN ---
    cursor.execute("SELECT COUNT(*) AS total FROM usuarios;")
    if cursor.fetchone()["total"] == 0:
        ahora_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
        INSERT INTO usuarios (id, alias, pin, edad, fecha_registro, objetivo_personal, hash_seguridad)
        VALUES (1, 'Participante 1', '1234', 24, ?, 'Autorregulación y Bienestar', 'anon_hash_user1')
        """, (ahora_str,))
        cursor.execute("""
        INSERT INTO usuarios (id, alias, pin, edad, fecha_registro, objetivo_personal, hash_seguridad)
        VALUES (2, 'Participante 2', '1234', 21, ?, 'Reducir Frecuencia y Mejorar Sueño', 'anon_hash_user2')
        """, (ahora_str,))
        cursor.execute("""
        INSERT INTO usuarios (id, alias, pin, edad, fecha_registro, objetivo_personal, hash_seguridad)
        VALUES (3, 'Participante 3', '1234', 28, ?, 'Observar Patrones de Estrés', 'anon_hash_user3')
        """, (ahora_str,))
        conn.commit()
    else:
        # Asegurar alias si algún usuario tenía valor nulo
        cursor.execute("UPDATE usuarios SET alias = 'Participante ' || id WHERE alias IS NULL OR alias = '';")
        cursor.execute("UPDATE usuarios SET pin = '1234' WHERE pin IS NULL OR pin = '';")
        conn.commit()

    conn.close()
    return path


def listar_usuarios(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retorna todos los usuarios registrados con su conteo de eventos."""
    conn = obtener_conexion(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT u.id, u.alias, u.edad, u.objetivo_personal, u.fecha_registro,
           COUNT(r.id) AS total_eventos
    FROM usuarios u
    LEFT JOIN registros_habito r ON u.id = r.usuario_id
    GROUP BY u.id
    ORDER BY u.id ASC
    """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def obtener_usuario(usuario_id: int, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Retorna el perfil de un usuario por su ID."""
    conn = obtener_conexion(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, alias, edad, objetivo_personal, fecha_registro FROM usuarios WHERE id = ?", (usuario_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def autenticar_usuario(alias: str, pin: str = "1234", db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Autentica a un usuario por alias y PIN."""
    conn = obtener_conexion(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, alias, edad, objetivo_personal, fecha_registro 
    FROM usuarios 
    WHERE LOWER(alias) = LOWER(?) AND (pin = ? OR pin IS NULL)
    """, (alias.strip(), pin.strip()))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def crear_usuario(alias: str, edad: int = 24, objetivo_personal: str = "Autorregulación", pin: str = "1234", db_path: Optional[str] = None) -> Dict[str, Any]:
    """Crea un nuevo usuario en la base de datos."""
    conn = obtener_conexion(db_path)
    cursor = conn.cursor()
    ahora_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO usuarios (alias, pin, edad, fecha_registro, objetivo_personal, hash_seguridad)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (alias.strip(), pin.strip(), edad, ahora_str, objetivo_personal.strip(), f"hash_{alias.strip().lower()}"))
    nuevo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {
        "id": nuevo_id,
        "alias": alias.strip(),
        "edad": edad,
        "objetivo_personal": objetivo_personal.strip(),
        "fecha_registro": ahora_str
    }


def sembrar_datos_iniciales(usuario_id: int = 1, db_path: Optional[str] = None) -> int:
    """
    Siembra registros longitudinales representativos para el usuario,
    permitiendo entrenar el modelo de Machine Learning y generar predicciones.
    """
    conn = obtener_conexion(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS total FROM registros_habito WHERE usuario_id = ?", (usuario_id,))
    total = cursor.fetchone()["total"]
    if total > 0:
        conn.close()
        return total

    # Registros clínicos sintetizados basados en la investigación de M-Control
    # Se cubren meses previos (Julio, Agosto, Septiembre 2026)
    registros = [
        # Julio 2026: Balance general (Verde)
        ("2026-07-01", "22:30", 15, 1, 4, 5, "Calma", 0, 0, 0, 0, 0, 0, 0, "Día tranquilo de descanso"),
        ("2026-07-04", "10:15", 10, 1, 5, 5, "Relajación", 0, 0, 0, 0, 0, 0, 0, "Fin de semana"),
        ("2026-07-06", "23:45", 20, 1, 6, 4, "Estrés leve", 0, 0, 0, 0, 0, 0, 0, "Cansancio tras jornada"),
        ("2026-07-08", "19:20", 15, 1, 5, 4, "Calma", 0, 0, 0, 0, 0, 0, 0, "Normal"),
        ("2026-07-09", "21:00", 25, 1, 7, 3, "Ansiedad", 1, 0, 0, 0, 0, 0, 0, "Preocupación laboral"),
        ("2026-07-10", "14:30", 20, 1, 8, 2, "Estrés alto", 1, 1, 0, 0, 0, 1, 0, "Postergación de estudio"),
        ("2026-07-10", "23:10", 30, 1, 9, 1, "Escape emocional", 2, 2, 1, 1, 1, 1, 1, "Sensación de culpa y molestia"),
        ("2026-07-13", "18:00", 15, 1, 4, 5, "Calma", 0, 0, 0, 0, 0, 0, 0, "Recuperación tras descanso de 3 días"),
        ("2026-07-16", "09:30", 12, 1, 3, 5, "Energía", 0, 0, 0, 0, 0, 0, 0, "Buen inicio de día"),
        ("2026-07-18", "22:15", 15, 1, 5, 4, "Cansancio", 0, 0, 0, 0, 0, 0, 0, "Ayudó a conciliar sueño"),
        ("2026-07-20", "20:40", 18, 1, 6, 4, "Estrés", 0, 0, 0, 0, 0, 0, 0, "Presión de entrega"),
        ("2026-07-22", "17:00", 15, 1, 4, 5, "Calma", 0, 0, 0, 0, 0, 0, 0, "Control adecuado"),
        ("2026-07-24", "23:50", 25, 1, 8, 3, "Ansiedad", 1, 0, 0, 0, 0, 0, 0, "Desvelo"),
        ("2026-07-26", "12:10", 15, 1, 5, 4, "Calma", 0, 0, 0, 0, 0, 0, 0, "Normal"),
        ("2026-07-28", "21:30", 12, 1, 3, 5, "Relajación", 0, 0, 0, 0, 0, 0, 0, "Excelente control"),
        ("2026-07-30", "08:20", 15, 1, 5, 4, "Calma", 0, 0, 0, 0, 0, 0, 0, "Normal"),
        ("2026-07-31", "23:00", 25, 1, 7, 3, "Estrés", 1, 0, 0, 0, 0, 0, 0, "Cierre de mes laboral"),

        # Agosto 2026: Variabilidad y detección de patrones de alerta
        ("2026-08-01", "11:30", 30, 1, 9, 2, "Impulsivo", 1, 1, 0, 0, 1, 1, 1, "Doble evento en menos de 14h"),
        ("2026-08-03", "20:00", 15, 1, 5, 4, "Calma", 0, 0, 0, 0, 0, 0, 0, "Recuperación de autocontrol"),
        ("2026-08-06", "22:45", 15, 1, 3, 5, "Relajación", 0, 0, 0, 0, 0, 0, 0, "Descanso de 72h óptimo"),
        ("2026-08-09", "18:30", 15, 1, 4, 5, "Calma", 0, 0, 0, 0, 0, 0, 0, "Buen ritmo"),
        ("2026-08-11", "23:15", 20, 1, 6, 4, "Estrés leve", 0, 0, 0, 0, 0, 0, 0, "Normal"),
        ("2026-08-13", "14:00", 20, 1, 7, 3, "Aburrimiento", 0, 1, 0, 0, 0, 0, 0, "Afectó avance de estudio"),
        ("2026-08-15", "01:20", 30, 1, 8, 2, "Ansiedad", 2, 0, 0, 0, 1, 1, 1, "Madrugada en pantalla"),
        ("2026-08-15", "09:00", 20, 1, 10, 1, "Pérdida de control", 2, 2, 1, 1, 1, 1, 1, "Fuerte dolor e irritación"),
        ("2026-08-18", "16:45", 15, 1, 3, 5, "Calma", 0, 0, 0, 0, 0, 0, 0, "Pausa biológica de 79 horas"),
        ("2026-08-21", "21:10", 15, 1, 4, 5, "Calma", 0, 0, 0, 0, 0, 0, 0, "Equilibrio"),
        ("2026-08-24", "19:30", 15, 1, 4, 5, "Relajación", 0, 0, 0, 0, 0, 0, 0, "Equilibrio"),
        ("2026-08-26", "23:00", 18, 1, 5, 4, "Cansancio", 0, 0, 0, 0, 0, 0, 0, "Normal"),
        ("2026-08-28", "17:15", 15, 1, 5, 4, "Calma", 0, 0, 0, 0, 0, 0, 0, "Normal"),
        ("2026-08-30", "11:00", 15, 1, 4, 5, "Calma", 0, 0, 0, 0, 0, 0, 0, "Fin de semana regulado"),
        ("2026-08-31", "22:40", 25, 1, 7, 3, "Estrés", 1, 0, 0, 0, 0, 0, 0, "Preocupación académica"),

        # Septiembre 2026: Mes previo al actual
        ("2026-09-02", "18:20", 15, 1, 5, 4, "Calma", 0, 0, 0, 0, 0, 0, 0, "Normal"),
        ("2026-09-04", "23:10", 15, 1, 3, 5, "Relajación", 0, 0, 0, 0, 0, 0, 0, "Buen descanso"),
        ("2026-09-06", "20:00", 18, 1, 5, 4, "Calma", 0, 0, 0, 0, 0, 0, 0, "Normal"),
        ("2026-09-08", "14:30", 25, 1, 7, 3, "Estrés", 0, 1, 0, 0, 0, 0, 0, "Día pesado en la universidad"),
        ("2026-09-09", "23:55", 30, 1, 8, 2, "Ansiedad", 2, 0, 0, 0, 1, 0, 1, "Dificultad para conciliar sueño"),
        ("2026-09-10", "08:30", 20, 1, 9, 1, "Escape emocional", 2, 2, 1, 1, 1, 1, 1, "Repetición matutina impulsiva"),
        ("2026-09-12", "21:15", 15, 1, 4, 5, "Calma", 0, 0, 0, 0, 0, 0, 0, "Pausa de recuperación de 60h"),
        ("2026-09-15", "19:40", 12, 1, 3, 5, "Relajación", 0, 0, 0, 0, 0, 0, 0, "Control excelente"),
        ("2026-09-17", "22:50", 15, 1, 5, 4, "Calma", 0, 0, 0, 0, 0, 0, 0, "Normal"),
        ("2026-09-19", "16:30", 15, 1, 5, 4, "Calma", 0, 0, 0, 0, 0, 0, 0, "Normal"),
        ("2026-09-20", "23:20", 22, 1, 7, 3, "Estrés", 1, 0, 0, 0, 0, 0, 0, "Tensión laboral"),
        ("2026-09-21", "14:00", 25, 1, 8, 2, "Impulsivo", 1, 1, 0, 0, 1, 0, 1, "Interferencia leve en jornada"),
        ("2026-09-21", "21:30", 20, 1, 9, 1, "Escape", 2, 1, 1, 0, 1, 1, 1, "Reiteración en mismo día"),
        
        # Inicios de Octubre 2026 (mes actual en curso)
        ("2026-10-01", "22:00", 15, 1, 4, 5, "Calma", 0, 0, 0, 0, 0, 0, 0, "Pausa previa de 9 días"),
        ("2026-10-02", "23:15", 15, 1, 5, 4, "Relajación", 0, 0, 0, 0, 0, 0, 0, "Día de trabajo normal"),
        ("2026-10-03", "19:00", 20, 1, 6, 3, "Estrés", 1, 0, 0, 0, 0, 0, 0, "Fin de semana acelerado")
    ]

    for r in registros:
        cursor.execute("""
        INSERT INTO registros_habito (
            usuario_id, fecha, hora, duracion, realizo_habito, nivel_deseo,
            nivel_control, estado_emocional, interferencia_sueno, interferencia_estudio,
            interferencia_trabajo, interferencia_social, dolor, irritacion, malestar, observaciones
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (usuario_id, *r))

    conn.commit()
    cursor.execute("SELECT COUNT(*) AS total FROM registros_habito WHERE usuario_id = ?", (usuario_id,))
    total_creado = cursor.fetchone()["total"]
    conn.close()
    return total_creado


def obtener_registros_usuario(usuario_id: int = 1, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retorna todos los registros históricos de un usuario ordenados por fecha y hora."""
    conn = obtener_conexion(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM registros_habito 
    WHERE usuario_id = ? 
    ORDER BY fecha ASC, hora ASC
    """, (usuario_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def insertar_registro(usuario_id: int, datos: Dict[str, Any], db_path: Optional[str] = None) -> int:
    """Inserta un nuevo registro de hábito en la base de datos."""
    conn = obtener_conexion(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO registros_habito (
        usuario_id, fecha, hora, duracion, realizo_habito, nivel_deseo,
        nivel_control, estado_emocional, interferencia_sueno, interferencia_estudio,
        interferencia_trabajo, interferencia_social, dolor, irritacion, malestar, observaciones
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        usuario_id,
        datos.get("fecha", datetime.now().strftime("%Y-%m-%d")),
        datos.get("hora", datetime.now().strftime("%H:%M")),
        datos.get("duracion", 15),
        datos.get("realizo_habito", 1),
        datos.get("nivel_deseo", 5),
        datos.get("nivel_control", 3),
        datos.get("estado_emocional", "Calma"),
        datos.get("interferencia_sueno", 0),
        datos.get("interferencia_estudio", 0),
        datos.get("interferencia_trabajo", 0),
        datos.get("interferencia_social", 0),
        datos.get("dolor", 0),
        datos.get("irritacion", 0),
        datos.get("malestar", 0),
        datos.get("observaciones", "")
    ))
    registro_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return registro_id


def guardar_predicciones(usuario_id: int, predicciones: List[Dict[str, Any]], db_path: Optional[str] = None):
    """Guarda o actualiza las predicciones del calendario inteligente."""
    conn = obtener_conexion(db_path)
    cursor = conn.cursor()
    for p in predicciones:
        motivos_str = json.dumps(p.get("motivos", []), ensure_ascii=False)
        cursor.execute("""
        INSERT INTO predicciones (
            usuario_id, fecha, nivel, probabilidad, confianza,
            motivos, recomendacion, modelo_version, fecha_generacion
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(usuario_id, fecha) DO UPDATE SET
            nivel = excluded.nivel,
            probabilidad = excluded.probabilidad,
            confianza = excluded.confianza,
            motivos = excluded.motivos,
            recomendacion = excluded.recomendacion,
            modelo_version = excluded.modelo_version,
            fecha_generacion = excluded.fecha_generacion
        """, (
            usuario_id,
            p["fecha"],
            p["nivel"],
            p["probabilidad"],
            p["confianza"],
            motivos_str,
            p["recomendacion"],
            p.get("modelo_version", "v2.0-hybrid"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
    conn.commit()
    conn.close()


def obtener_predicciones_mes(usuario_id: int, año: int, mes: int, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Obtiene las predicciones almacenadas para un mes específico (YYYY-MM)."""
    conn = obtener_conexion(db_path)
    cursor = conn.cursor()
    filtro_mes = f"{año:04d}-{mes:02d}%"
    cursor.execute("""
    SELECT * FROM predicciones 
    WHERE usuario_id = ? AND fecha LIKE ?
    ORDER BY fecha ASC
    """, (usuario_id, filtro_mes))
    rows = []
    for r in cursor.fetchall():
        d = dict(r)
        try:
            d["motivos"] = json.loads(d["motivos"])
        except Exception:
            d["motivos"] = []
        rows.append(d)
    conn.close()
    return rows


def registrar_historial_modelo(usuario_id: int, modelo_version: str, cantidad_datos: int, metricas: Dict[str, Any], db_path: Optional[str] = None):
    """Registra una sesión de entrenamiento y validación del modelo."""
    conn = obtener_conexion(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO historial_modelo (usuario_id, modelo_version, fecha_entrenamiento, cantidad_datos, metricas)
    VALUES (?, ?, ?, ?, ?)
    """, (
        usuario_id,
        modelo_version,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        cantidad_datos,
        json.dumps(metricas, ensure_ascii=False)
    ))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    db_file = inicializar_base_datos()
    total = sembrar_datos_iniciales(1)
    print(f"[OK] Base de datos inicializada en: {db_file}")
    print(f"[OK] Total de registros sembrados para usuario 1: {total}")

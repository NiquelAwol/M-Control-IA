"""
preparacion_datos.py
M-Control | Inteligencia Artificial · Segundo Corte
Docente: Jhon James Cano Sánchez
Estudiantes: Andrés Felipe Mejía Suaza & Miguel Ángel Ramírez

Script de preparación y limpieza de datos con Pandas (Clase 7).
Inspecciona el dataset crudo recolectado, realiza el tratamiento justificado de:
- Valores nulos
- Filas duplicadas
- Tipos de datos incorrectos
- Valores atípicos o físicamente imposibles
- Categorías inconsistentes
Codifica variables categóricas con pd.get_dummies, genera la tabla comparativa
'Antes / Después' y exporta el dataset limpio a data/mcontrol_limpio.csv.
"""

import os
import pandas as pd
import numpy as np


def obtener_directorio_base():
    """Permite ejecutar el script tanto desde la raíz (/app) como desde /app/src."""
    actual = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(actual) == "src":
        return os.path.dirname(actual)
    return actual


def main():
    base_dir = obtener_directorio_base()
    print("=" * 75)
    print("  M-CONTROL | PREPARACIÓN Y LIMPIEZA DE DATOS CON PANDAS (CLASE 7)")
    print("=" * 75)

    archivo_origen = os.path.join(base_dir, "data", "datos_mcontrol_crudo.csv")
    if not os.path.exists(archivo_origen):
        archivo_origen = os.path.join(base_dir, "datos_mcontrol.csv")

    # 1. CARGA E INSPECCIÓN INICIAL CON PANDAS
    print("\n--- 1. CARGA E INSPECCIÓN INICIAL DEL DATASET CRUDO ---")
    df_raw = pd.read_csv(archivo_origen)
    filas_inicial, cols_inicial = df_raw.shape
    print(f"Archivo cargado : {os.path.relpath(archivo_origen, base_dir)}")
    print(f"Dimensiones iniciales (df.shape): {filas_inicial} filas x {cols_inicial} columnas\n")

    print("Estructura y tipos de datos iniciales (df.info()):")
    df_raw.info()

    nulos_por_col = df_raw.isnull().sum()
    total_nulos_inicial = int(nulos_por_col.sum())
    print("\nConteo de valores nulos por columna (df.isnull().sum()):")
    print(nulos_por_col[nulos_por_col > 0] if total_nulos_inicial > 0 else nulos_por_col)
    print(f"Total de celdas nulas encontradas: {total_nulos_inicial}")

    duplicados_inicial = int(df_raw.duplicated().sum())
    print(f"Filas duplicadas exactas (df.duplicated().sum()): {duplicados_inicial}")

    categorias_raw = df_raw['estado_semaforo'].unique().tolist()
    print(f"Categorías en 'estado_semaforo' antes de limpiar: {categorias_raw}")

    # 2. TRATAMIENTO JUSTIFICADO DE PROBLEMAS EN LOS DATOS
    print("\n--- 2. TRATAMIENTO JUSTIFICADO DE DATOS ---")
    df_clean = df_raw.copy()

    # A. Eliminación de duplicados
    df_clean = df_clean.drop_duplicates()
    print(f"[1. Duplicados] Se eliminaron {duplicados_inicial} filas duplicadas producto de doble envío en formulario.")
    print(f"    Filas restantes: {len(df_clean)}")

    # B. Tratamiento de valores nulos
    filas_con_nulos = df_clean.isnull().any(axis=1).sum()
    df_clean = df_clean.dropna(subset=['intervalo_horas', 'nivel_estres']).copy()
    print(f"[2. Valores Nulos] Se eliminaron {filas_con_nulos} registros con valores faltantes en 'intervalo_horas' o 'nivel_estres'.")
    print("    Justificación: No se imputan con la media para no distorsionar la relación fisiológica real entre descanso y estrés.")
    print(f"    Filas restantes: {len(df_clean)}")

    # C. Corrección de tipos de datos
    df_clean['fecha_hora'] = pd.to_datetime(df_clean['fecha_hora'], errors='coerce')
    df_clean['intervalo_horas'] = df_clean['intervalo_horas'].astype(float)
    df_clean['nivel_estres'] = df_clean['nivel_estres'].astype(int)
    df_clean['hora_evento'] = df_clean['fecha_hora'].dt.hour
    print("[3. Tipos de Datos] 'fecha_hora' convertida de object/str a datetime64; 'nivel_estres' tipado a int64.")

    # D. Filtrado de valores atípicos o imposibles
    condicion_imposible = (df_clean['intervalo_horas'] <= 0) | (df_clean['intervalo_horas'] > 720) | (df_clean['nivel_estres'] < 1) | (df_clean['nivel_estres'] > 10)
    filas_atipicas = int(condicion_imposible.sum())
    df_clean = df_clean[~condicion_imposible].copy()
    print(f"[4. Atípicos / Imposibles] Se descartaron {filas_atipicas} registros con valores imposibles (intervalo -6.5h < 0 y estrés 15 fuera de escala 1-10).")
    print(f"    Filas restantes: {len(df_clean)}")

    # E. Unificación de categorías inconsistentes
    df_clean['estado_semaforo'] = df_clean['estado_semaforo'].astype(str).str.strip().str.title()
    categorias_limpias = df_clean['estado_semaforo'].unique().tolist()
    print(f"[5. Categorías Inconsistentes] Unificadas con .str.strip().str.title(): {categorias_limpias}")

    # F. Definición de la Variable Objetivo 0/1 para el Perceptrón
    # Umbral: puntuación_bienestar < 70.0 (o estado Amarilla/Roja) -> requiere_pausa = 1
    df_clean['requiere_pausa'] = np.where(df_clean['puntuacion_bienestar'] < 70.0, 1, 0)
    print("\n[6. Variable Objetivo 0/1] Creada columna 'requiere_pausa':")
    print("    • 1 (Alerta / Requiere Pausa Biológica): puntuacion_bienestar < 70")
    print("    • 0 (Balance / Autorregulación Óptima) : puntuacion_bienestar >= 70")
    print("    • Nota clave: 'puntuacion_bienestar' NO se usa como entrada (X) en el modelo para evitar fuga de datos.")

    # G. Codificación de variables categóricas con pd.get_dummies
    df_encoded = pd.get_dummies(df_clean, columns=['control_autopercibido'], prefix='control', dtype=int)
    print("\n[7. Codificación Categórica] Aplicado pd.get_dummies sobre 'control_autopercibido' -> ['control_1', 'control_2', 'control_3'].")

    # 3. EXPORTACIÓN DEL DATASET LIMPIO A data/mcontrol_limpio.csv
    os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)
    ruta_salida = os.path.join(base_dir, "data", "mcontrol_limpio.csv")
    df_encoded.to_csv(ruta_salida, index=False, encoding='utf-8')
    print(f"\n[OK] Dataset limpio exportado en: {os.path.relpath(ruta_salida, base_dir)}")

    # 4. TABLA COMPARATIVA ANTES / DESPUÉS
    filas_final, cols_final = df_encoded.shape
    nulos_final = int(df_encoded.isnull().sum().sum())
    duplicados_final = int(df_encoded.duplicated().sum())

    print("\n" + "=" * 75)
    print("  TABLA COMPARATIVA 'ANTES / DESPUÉS' (REQUISITO OFICIAL CLASE 7)")
    print("=" * 75)
    tabla_comparativa = pd.DataFrame({
        "Indicador del Dataset": [
            "Número de Filas (Registros)",
            "Número de Columnas",
            "Valores Nulos (Celdas vacías)",
            "Filas Duplicadas",
            "Valores Atípicos / Imposibles",
            "Categorías en 'estado_semaforo'"
        ],
        "Antes (Crudo)": [
            str(filas_inicial),
            str(cols_inicial),
            str(total_nulos_inicial),
            str(duplicados_inicial),
            str(filas_atipicas),
            "6 variantes ('verde', 'VERDE ', 'Rojo '...)"
        ],
        "Después (Limpio)": [
            str(filas_final),
            str(cols_final),
            str(nulos_final),
            str(duplicados_final),
            "0",
            "3 unificadas ('Verde', 'Amarillo', 'Rojo')"
        ]
    })
    print(tabla_comparativa.to_string(index=False))
    print("=" * 75)


if __name__ == "__main__":
    main()

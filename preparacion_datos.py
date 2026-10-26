"""
preparacion_datos.py
M-Control | Inteligencia Artificial · Segundo Corte
Docente: Jhon James Cano Sánchez
Estudiantes: Andrés Felipe Mejía Suaza & Miguel Ángel Linares

Script de preparación y limpieza de datos con Pandas (Clase 7).
Inspecciona el dataset original, realiza tratamiento justificado de datos,
codifica variables categóricas, genera tabla comparativa 'antes/después'
y exporta el dataset limpio a data/mcontrol_limpio.csv.
"""

import os
import pandas as pd
import numpy as np


def main():
    print("=" * 70)
    print("  M-CONTROL | PREPARACIÓN Y LIMPIEZA DE DATOS (CLASE 7)")
    print("=" * 70)

    archivo_origen = "datos_mcontrol.csv"
    if not os.path.exists(archivo_origen):
        print(f"[ERROR] No se encontró '{archivo_origen}'.")
        return

    # 1. CARGA E INSPECCIÓN INICIAL CON PANDAS
    print("\n--- 1. INSPECCIÓN INICIAL DEL DATASET ---")
    df_raw = pd.read_csv(archivo_origen)
    filas_inicial, cols_inicial = df_raw.shape
    print(f"Dimensiones iniciales (shape): {filas_inicial} filas x {cols_inicial} columnas")

    print("\nResumen general (info):")
    df_raw.info()

    nulos_inicial = df_raw.isnull().sum()
    print("\nValores nulos por columna (inicial):")
    print(nulos_inicial)

    duplicados_inicial = df_raw.duplicated().sum()
    print(f"\nFilas duplicadas identificadas: {duplicados_inicial}")

    # 2. TRATAMIENTO JUSTIFICADO DE DATOS
    print("\n--- 2. TRATAMIENTO JUSTIFICADO DE DATOS ---")
    df_clean = df_raw.copy()

    # A. Tratamiento de duplicados
    if duplicados_inicial > 0:
        df_clean = df_clean.drop_duplicates()
        print(f"[ACCION] Se eliminaron {duplicados_inicial} registros duplicados.")
    else:
        print("[JUSTIFICACION] No se encontraron filas duplicadas idénticas en el dataset.")

    # B. Normalización y tipado de fechas
    df_clean['fecha_hora'] = pd.to_datetime(df_clean['fecha_hora'], errors='coerce')
    df_clean['hora_evento'] = df_clean['fecha_hora'].dt.hour
    df_clean['dia_semana'] = df_clean['fecha_hora'].dt.day_name()
    print("[ACCION] 'fecha_hora' convertida a datetime y extraídas features 'hora_evento' y 'dia_semana'.")

    # C. Tratamiento de nulos o valores atípicos imposibles
    # Un intervalo de horas biológicamente debe ser > 0 y < 720 (un mes)
    filas_invalidas_intervalo = df_clean[(df_clean['intervalo_horas'] <= 0) | (df_clean['intervalo_horas'] > 720)]
    if len(filas_invalidas_intervalo) > 0:
        df_clean = df_clean[~df_clean.index.isin(filas_invalidas_intervalo.index)]
        print(f"[ACCION] Se eliminaron {len(filas_invalidas_intervalo)} registros con intervalos fisiológicamente inválidos.")
    else:
        print("[JUSTIFICACION] Todos los intervalos de descanso (7.5h a 79.7h) se encuentran en el rango fisiológico válido.")

    # D. Normalización de categorías textuales (espacios, tildes, mayúsculas)
    df_clean['estado_semaforo'] = df_clean['estado_semaforo'].astype(str).str.strip().str.title()
    print("[ACCION] 'estado_semaforo' normalizado a formato Título (Verde, Amarillo, Rojo).")

    # E. Definición de la Variable Objetivo 0/1 para Machine Learning
    # y = 1 si requiere alerta o pausa biológica (Semáforo Amarillo o Rojo, o bienestar < 70, o interferencia >= 1)
    # y = 0 si patrón en balance autorregulado (Semáforo Verde, bienestar >= 70, sin interferencia)
    df_clean['requiere_pausa'] = np.where(
        (df_clean['estado_semaforo'].isin(['Amarillo', 'Rojo'])) | 
        (df_clean['puntuacion_bienestar'] < 70.0) | 
        (df_clean['interferencia_funcional'] >= 1),
        1, 0
    )
    print("\n[DEFINICION VARIABLE OBJETIVO]")
    print("Variable binaria creada: 'requiere_pausa' (0 = Favorable/Equilibrado, 1 = Alerta/Requiere Pausa).")
    print(df_clean['requiere_pausa'].value_counts().rename(index={0: "0 (Verde - Balance)", 1: "1 (Alerta / Pausa)"}))

    # F. Codificación de variables categóricas con pd.get_dummies
    # Codificamos 'control_autopercibido' (1: Bajo, 2: Medio, 3: Alto) a dummies explicativas
    df_encoded = pd.get_dummies(df_clean, columns=['control_autopercibido'], prefix='control', dtype=int)
    print("\n[ACCION] Codificación con pd.get_dummies aplicada sobre 'control_autopercibido' -> ['control_1', 'control_2', 'control_3'].")

    # 3. EXPORTACIÓN A data/mcontrol_limpio.csv
    os.makedirs("data", exist_ok=True)
    ruta_salida = os.path.join("data", "mcontrol_limpio.csv")
    df_encoded.to_csv(ruta_salida, index=False, encoding='utf-8')
    print(f"\n[OK] Dataset limpio y preparado exportado exitosamente en: {ruta_salida}")

    # 4. TABLA COMPARATIVA ANTES / DESPUÉS
    filas_final, cols_final = df_encoded.shape
    nulos_final = df_encoded.isnull().sum().sum()

    print("\n" + "=" * 70)
    print("  TABLA COMPARATIVA 'ANTES / DESPUÉS' (REQUISITO OFICIAL CLASE 7)")
    print("=" * 70)
    tabla_comparativa = pd.DataFrame({
        "Métrica": ["Número de Filas", "Número de Columnas", "Total Valores Nulos", "Filas Duplicadas", "Nuevas Features Creadas"],
        "Antes (Dataset Raw)": [filas_inicial, cols_inicial, nulos_inicial.sum(), duplicados_inicial, 0],
        "Después (Dataset Limpio)": [filas_final, cols_final, nulos_final, 0, 4]
    })
    print(tabla_comparativa.to_string(index=False))
    print("=" * 70)

    return df_encoded


if __name__ == "__main__":
    main()

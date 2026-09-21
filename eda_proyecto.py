"""
eda_proyecto.py
M-Control | Inteligencia Artificial (COTECNOVA)

Script para realizar el Análisis Exploratorio de Datos (EDA) sobre el dataset
de autorregulación de M-Control utilizando NumPy y Matplotlib (Clase 4).
"""

import csv
import os
import matplotlib.pyplot as plt
import numpy as np


def cargar_datos(archivo_csv):
    """
    Carga el archivo CSV del proyecto y retorna:
    - datos_numericos: Array NumPy 2D con las columnas numéricas.
    - datos_completos: Lista de registros con todas las columnas.
    - nombres_columnas: Lista con los encabezados.
    """
    datos = []
    nombres_columnas = []
    try:
        with open(archivo_csv, mode="r", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            nombres_columnas = next(lector)
            for fila in lector:
                # Columnas:
                # 0: id_registro, 1: fecha_hora, 2: intervalo_horas,
                # 3: control_autopercibido, 4: interferencia_funcional,
                # 5: sintomas_fisicos, 6: nivel_estres, 7: consumo_pornografia,
                # 8: puntuacion_bienestar, 9: estado_semaforo
                intervalo = float(fila[2])
                control = float(fila[3])
                interferencia = float(fila[4])
                sintomas = float(fila[5])
                estres = float(fila[6])
                porno = float(fila[7])
                bienestar = float(fila[8])
                semaforo = fila[9].strip()

                datos.append([
                    int(fila[0]), fila[1], intervalo, control,
                    interferencia, sintomas, estres, porno,
                    bienestar, semaforo
                ])
        print(f"[OK] Datos cargados correctamente: {len(datos)} registros.")
    except FileNotFoundError:
        print(f"[ERROR] Archivo '{archivo_csv}' no encontrado.")
        return None, None, None
    except Exception as e:
        print(f"[ERROR] Error al leer archivo: {e}")
        return None, None, None

    # Array de NumPy con las columnas numéricas principales:
    # Col 0: intervalo_horas, Col 1: puntuacion_bienestar, Col 2: nivel_estres, Col 3: control
    datos_numericos = np.array(
        [[fila[2], fila[8], fila[6], fila[3]] for fila in datos],
        dtype=float
    )

    return datos_numericos, datos, nombres_columnas


def analizar_datos(datos_numericos):
    """
    Calcula estadísticas descriptivas vectorizadas utilizando NumPy
    para las variables clave del proyecto.
    """
    if datos_numericos is None or len(datos_numericos) == 0:
        return None

    intervalos = datos_numericos[:, 0]
    bienestar = datos_numericos[:, 1]
    estres = datos_numericos[:, 2]

    estadisticas = {
        "intervalo_horas": {
            "media": float(np.mean(intervalos)),
            "mediana": float(np.median(intervalos)),
            "desviacion": float(np.std(intervalos)),
            "minimo": float(np.min(intervalos)),
            "maximo": float(np.max(intervalos))
        },
        "puntuacion_bienestar": {
            "media": float(np.mean(bienestar)),
            "mediana": float(np.median(bienestar)),
            "desviacion": float(np.std(bienestar)),
            "minimo": float(np.min(bienestar)),
            "maximo": float(np.max(bienestar))
        },
        "nivel_estres": {
            "media": float(np.mean(estres)),
            "mediana": float(np.median(estres)),
            "desviacion": float(np.std(estres)),
            "minimo": float(np.min(estres)),
            "maximo": float(np.max(estres))
        }
    }
    return estadisticas


def generar_visualizaciones(datos_numericos, datos_completos, directorio_salida="."):
    """
    Genera visualizaciones para EDA utilizando Matplotlib y las guarda como archivos PNG:
    1. Histograma de distribución de la Puntuación de Bienestar.
    2. Gráfico de dispersión: Intervalo de horas de descanso vs Puntuación de Bienestar.
    3. Gráfico de dispersión: Nivel de estrés vs Puntuación de Bienestar.
    """
    if datos_numericos is None or len(datos_numericos) == 0:
        return

    intervalos = datos_numericos[:, 0]
    bienestar = datos_numericos[:, 1]
    estres = datos_numericos[:, 2]

    # Asignación de colores por semáforo para los gráficos de dispersión
    color_map = {"Verde": "#22c55e", "Amarillo": "#eab308", "Rojo": "#ef4444"}
    colores_puntos = [color_map.get(fila[9], "#3b82f6") for fila in datos_completos]

    # --- 1. HISTOGRAMA: Distribución de la Puntuación de Bienestar ---
    plt.figure(figsize=(9, 5))
    n, bins, patches = plt.hist(bienestar, bins=8, color="#38bdf8", edgecolor="#0f172a", alpha=0.85)
    plt.axvline(np.mean(bienestar), color="#dc2626", linestyle="dashed", linewidth=2, label=f"Media: {np.mean(bienestar):.1f}")
    plt.axvline(np.median(bienestar), color="#16a34a", linestyle="dotted", linewidth=2, label=f"Mediana: {np.median(bienestar):.1f}")
    plt.title("M-Control | Distribución de la Puntuación de Bienestar (0 - 100)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Puntuación de Bienestar", fontsize=11)
    plt.ylabel("Frecuencia (Cantidad de Eventos)", fontsize=11)
    plt.grid(True, axis="y", linestyle="--", alpha=0.6)
    plt.legend(frameon=True)
    plt.tight_layout()
    ruta_hist = os.path.join(directorio_salida, "histograma_bienestar.png")
    plt.savefig(ruta_hist, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[OK] Gráfica guardada: {ruta_hist}")

    # --- 2. GRÁFICO DE DISPERSIÓN: Intervalo de Horas vs Bienestar ---
    plt.figure(figsize=(9, 5.5))
    plt.scatter(intervalos, bienestar, c=colores_puntos, s=75, edgecolors="#1e293b", alpha=0.9, zorder=3)
    plt.axhline(70, color="#22c55e", linestyle="--", alpha=0.6, label="Umbral Verde (>= 70)")
    plt.axhline(40, color="#ef4444", linestyle="--", alpha=0.6, label="Umbral Rojo (< 40)")
    plt.title("M-Control | Relación: Intervalo de Descanso (Horas) vs Bienestar", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Intervalo de Recuperación / Descanso (Horas)", fontsize=11)
    plt.ylabel("Puntuación de Bienestar (0 - 100)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.5, zorder=0)
    plt.legend(frameon=True, loc="lower right")
    plt.tight_layout()
    ruta_disp1 = os.path.join(directorio_salida, "dispersion_intervalo_bienestar.png")
    plt.savefig(ruta_disp1, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[OK] Gráfica guardada: {ruta_disp1}")

    # --- 3. GRÁFICO DE DISPERSIÓN: Nivel de Estrés vs Bienestar ---
    plt.figure(figsize=(9, 5.5))
    plt.scatter(estres, bienestar, c=colores_puntos, s=75, edgecolors="#1e293b", alpha=0.9, zorder=3)
    plt.title("M-Control | Relación: Nivel de Estrés Previo vs Puntuación de Bienestar", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Nivel de Estrés Previo (Escala 1 al 10)", fontsize=11)
    plt.ylabel("Puntuación de Bienestar (0 - 100)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.5, zorder=0)
    plt.tight_layout()
    ruta_disp2 = os.path.join(directorio_salida, "dispersion_estres_bienestar.png")
    plt.savefig(ruta_disp2, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[OK] Gráfica guardada: {ruta_disp2}")


def main():
    """Función principal que orquesta el flujo completo de EDA."""
    print("=" * 60)
    print("   ANÁLISIS EXPLORATORIO DE DATOS (EDA) - M-CONTROL (CLASE 4)")
    print("=" * 60)

    base_dir = os.path.dirname(__file__)
    ruta_csv = os.path.join(base_dir, "datos_mcontrol.csv")

    datos_num, datos_comp, columnas = cargar_datos(ruta_csv)
    if datos_num is None:
        return

    estadisticas = analizar_datos(datos_num)
    if estadisticas:
        print("\n=== ESTADÍSTICAS DESCRIPTIVAS CALCULADAS CON NUMPY ===")
        print("-" * 55)
        for variable, metricas in estadisticas.items():
            print(f"\nVARIABLE: {variable.upper()}")
            for k, v in metricas.items():
                print(f"  • {k.capitalize()}: {v:.2f}")

    print("\n=== GENERANDO VISUALIZACIONES CON MATPLOTLIB ===")
    generar_visualizaciones(datos_num, datos_comp, base_dir)
    print("\n[ÉXITO] Análisis Exploratorio de Datos completado con éxito.")


if __name__ == "__main__":
    main()

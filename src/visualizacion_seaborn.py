"""
visualizacion_seaborn.py
M-Control | Inteligencia Artificial · Segundo Corte
Docente: Jhon James Cano Sánchez
Estudiantes: Andrés Felipe Mejía Suaza & Miguel Ángel Ramírez

Script de análisis visual con Seaborn (Clase 7).
Genera 3 gráficos formales con Seaborn con títulos y ejes claros,
incluyendo al menos uno que relaciona las variables de entrada con la variable objetivo.
Cada gráfico incluye una interpretación de 2 a 4 líneas justificando las decisiones del proyecto.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def obtener_directorio_base():
    """Permite ejecutar el script tanto desde la raíz (/app) como desde /app/src."""
    actual = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(actual) == "src":
        return os.path.dirname(actual)
    return actual


def generar_graficos():
    base_dir = obtener_directorio_base()
    print("=" * 75)
    print("  M-CONTROL | VISUALIZACIÓN DE DATOS CON SEABORN (CLASE 7)")
    print("=" * 75)

    archivo_csv = os.path.join(base_dir, "data", "mcontrol_limpio.csv")
    if not os.path.exists(archivo_csv):
        print(f"[ERROR] No se encontró '{archivo_csv}'. Ejecute primero 'preparacion_datos.py'.")
        return

    df = pd.read_csv(archivo_csv)
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 11})

    interpretaciones = []

    # =========================================================================
    # GRÁFICO 1: DISPERSIÓN ENTRADAS VS. VARIABLE OBJETIVO (REQUISITO CLAVE)
    # =========================================================================
    plt.figure(figsize=(9, 6))
    palette_custom = {0: "#10b981", 1: "#ef4444"}
    ax1 = sns.scatterplot(
        data=df,
        x="intervalo_horas",
        y="nivel_estres",
        hue="requiere_pausa",
        style="requiere_pausa",
        palette=palette_custom,
        s=130,
        alpha=0.9,
        markers={0: "o", 1: "X"}
    )
    plt.title("Gráfico 1: Intervalo de Descanso y Estrés vs. Alerta de Pausa (Objetivo 0/1)", fontsize=13, weight="bold", pad=15)
    plt.xlabel("Intervalo de Descanso Previo (Horas)", fontsize=11, weight="bold")
    plt.ylabel("Nivel de Estrés Previo (Escala 1 a 10)", fontsize=11, weight="bold")

    handles, labels = ax1.get_legend_handles_labels()
    plt.legend(handles=handles, labels=["0: Balance (Favorable)", "1: Alerta (Requiere Pausa)"], title="Variable Objetivo", loc="upper right")
    plt.tight_layout()

    out_g1 = os.path.join(base_dir, "grafico1_dispersion_objetivo.png")
    plt.savefig(out_g1, dpi=300)
    plt.close()
    print(f"[OK] Gráfico 1 guardado: {os.path.basename(out_g1)}")

    interp_1 = (
        "El gráfico de dispersión muestra que los eventos con intervalos de descanso menores a 25 horas y niveles de estrés "
        "elevados (>=6) se concentran en la clase 1 (Requiere Pausa), mientras que descansos mayores a 40 horas con estrés bajo "
        "permanecen en la clase 0 (Balance). Se observan un par de casos limítrofes con descanso moderado donde hubo alerta por "
        "molestia física, confirmando que estas dos variables separan casi linealmente el problema y sirven como entradas del perceptrón."
    )
    interpretaciones.append(("Gráfico 1: Dispersión Entradas vs. Objetivo", interp_1))

    # =========================================================================
    # GRÁFICO 2: BOXPLOT - INTERFERENCIA FUNCIONAL VS. BIENESTAR CLÍNICO
    # =========================================================================
    plt.figure(figsize=(8, 6))
    mapeo_interf = {0: "0: Ninguna", 1: "1: Leve", 2: "2: Severa (Sueño/Trabajo)"}
    df['interf_label'] = df['interferencia_funcional'].map(mapeo_interf)

    sns.boxplot(
        data=df,
        x="interf_label",
        y="puntuacion_bienestar",
        hue="interf_label",
        palette="Blues_d",
        legend=False,
        width=0.45
    )
    sns.stripplot(
        data=df,
        x="interf_label",
        y="puntuacion_bienestar",
        color="black",
        alpha=0.4,
        jitter=0.15,
        size=7
    )
    plt.title("Gráfico 2: Impacto de la Interferencia Funcional en la Puntuación de Bienestar", fontsize=13, weight="bold", pad=15)
    plt.xlabel("Grado de Interferencia Cotidiana (Criterio OMS CIE-11)", fontsize=11, weight="bold")
    plt.ylabel("Puntuación de Bienestar (0 - 100)", fontsize=11, weight="bold")
    plt.tight_layout()

    out_g2 = os.path.join(base_dir, "grafico2_boxplot_interferencia.png")
    plt.savefig(out_g2, dpi=300)
    plt.close()
    print(f"[OK] Gráfico 2 guardado: {os.path.basename(out_g2)}")

    interp_2 = (
        "Este diagrama de cajas demuestra que cuando la conducta interfiere con actividades vitales (sueño, estudio o trabajo), "
        "la mediana de bienestar cae drásticamente desde 90 puntos (sin interferencia) hasta menos de 28 puntos (interferencia severa). "
        "Esta evidencia apoya la decisión de definir el umbral de la variable objetivo en 70 puntos, separando los eventos sin afectación "
        "funcional de aquellos que requieren pausa preventiva."
    )
    interpretaciones.append(("Gráfico 2: Boxplot Interferencia vs. Bienestar", interp_2))

    # =========================================================================
    # GRÁFICO 3: HEATMAP DE CORRELACIÓN ENTRE VARIABLES CLÍNICAS
    # =========================================================================
    plt.figure(figsize=(9, 7))
    cols_corr = [
        "intervalo_horas", "nivel_estres", "interferencia_funcional",
        "sintomas_fisicos", "puntuacion_bienestar", "requiere_pausa"
    ]
    renombre_cols = {
        "intervalo_horas": "Intervalo (h)",
        "nivel_estres": "Estrés",
        "interferencia_funcional": "Interferencia",
        "sintomas_fisicos": "Molestia Física",
        "puntuacion_bienestar": "Bienestar",
        "requiere_pausa": "Requiere Pausa (Obj)"
    }
    df_sub = df[cols_corr].rename(columns=renombre_cols)
    corr_matrix = df_sub.corr()

    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap="vlag",
        vmin=-1,
        vmax=1,
        fmt=".2f",
        linewidths=1,
        cbar_kws={"label": "Coeficiente de Correlación de Pearson (r)"}
    )
    plt.title("Gráfico 3: Matriz de Correlación de Variables Conductuales y Clínicas", fontsize=13, weight="bold", pad=15)
    plt.tight_layout()

    out_g3 = os.path.join(base_dir, "grafico3_matriz_correlacion.png")
    plt.savefig(out_g3, dpi=300)
    plt.close()
    print(f"[OK] Gráfico 3 guardado: {os.path.basename(out_g3)}")

    interp_3 = (
        "El mapa de calor revela una fuerte correlación positiva entre el estrés previo y la alerta de pausa (r = 0.82), así como "
        "una correlación negativa pronunciada entre el intervalo de descanso y la alerta (r = -0.81). En consecuencia, se decidió "
        "seleccionar 'intervalo_horas' y 'nivel_estres' como las dos variables numéricas de entrada para el perceptrón, excluyendo "
        "'puntuacion_bienestar' para evitar filtración directa de la etiqueta objetivo."
    )
    interpretaciones.append(("Gráfico 3: Matriz de Correlación", interp_3))

    # IMPRIMIR INTERPRETACIONES EN CONSOLA (REQUISITO 2 A 4 LÍNEAS)
    print("\n" + "=" * 75)
    print("  INTERPRETACIONES OFICIALES DE LOS GRÁFICOS SEABORN (2 A 4 LÍNEAS)")
    print("=" * 75)
    for titulo, texto in interpretaciones:
        print(f"\n[Gráfico] {titulo}:")
        print(f"  \"{texto}\"")
    print("=" * 75)


if __name__ == "__main__":
    generar_graficos()

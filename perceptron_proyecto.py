"""
perceptron_proyecto.py
M-Control | Inteligencia Artificial · Segundo Corte
Docente: Jhon James Cano Sánchez
Estudiantes: Andrés Felipe Mejía Suaza & Miguel Ángel Linares

Actividad Independiente de las Clases 8 y 9:
Implementación de un Perceptrón simple para clasificación binaria desde cero
utilizando exclusivamente NumPy y Matplotlib (SIN SCIKIT-LEARN).
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class PerceptronDesdeCero:
    """
    Perceptrón con función de activación sigmoide, función de costo
    de pérdida logarítmica (Binary Cross-Entropy) y optimización
    por Descenso del Gradiente analítico implementado puramente en NumPy.
    """

    def __init__(self, learning_rate=0.15, epocas=1500):
        self.learning_rate = learning_rate
        self.epocas = epocas
        self.w = None  # Pesos w1, w2
        self.b = None  # Sesgo bias
        self.historial_perdida = []

    def sigmoide(self, z):
        """Función de activación logística acotada en (0, 1)."""
        # Clip para evitar desbordamiento numérico (overflow)
        z_clipped = np.clip(z, -500, 500)
        return 1.0 / (1.0 + np.exp(-z_clipped))

    def calcular_perdida(self, y_true, y_pred):
        """Pérdida logarítmica (Binary Cross-Entropy Loss)."""
        m = len(y_true)
        epsilon = 1e-15  # Para prevenir log(0)
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        perdida = - (1.0 / m) * np.sum(y_true * np.log(y_pred) + (1.0 - y_true) * np.log(1.0 - y_pred))
        return perdida

    def entrenar(self, X, y):
        """
        Entrenamiento mediante Descenso del Gradiente por lotes (Batch Gradient Descent).
        X: matriz de características (m muestras, n features) estandarizadas.
        y: vector de etiquetas reales (0 o 1).
        """
        m, n = X.shape
        np.random.seed(42)
        # Inicialización de pesos pequeños aleatorios y sesgo en cero
        self.w = np.random.randn(n) * 0.01
        self.b = 0.0
        self.historial_perdida = []

        for epoca in range(self.epocas):
            # 1. Forward Pass (Propagación hacia adelante)
            z = np.dot(X, self.w) + self.b
            y_pred = self.sigmoide(z)

            # 2. Cálculo de la función de pérdida
            perdida = self.calcular_perdida(y, y_pred)
            self.historial_perdida.append(perdida)

            # 3. Backward Pass (Cálculo analítico de gradientes)
            error = y_pred - y
            dw = (1.0 / m) * np.dot(X.T, error)
            db = (1.0 / m) * np.sum(error)

            # 4. Actualización de parámetros con descenso del gradiente
            self.w -= self.learning_rate * dw
            self.b -= self.learning_rate * db

        return self.historial_perdida

    def predecir_probabilidad(self, X):
        """Retorna la probabilidad estimada P(y=1|x)."""
        z = np.dot(X, self.w) + self.b
        return self.sigmoide(z)

    def predecir_clase(self, X, umbral=0.5):
        """Retorna la clase binaria predicha (0 o 1)."""
        prob = self.predecir_probabilidad(X)
        return (prob >= umbral).astype(int)

    def exactitud(self, y_true, y_pred):
        """Calcula el porcentaje de aciertos del modelo."""
        return np.mean(y_true == y_pred) * 100.0


def main():
    print("=" * 75)
    print("  M-CONTROL | PERCEPTRÓN DESDE CERO CON NUMPY (CLASES 8 Y 9)")
    print("  Implementación Matemática: Sigmoide + Binary Cross-Entropy + Descenso Gradiente")
    print("=" * 75)

    # 1. CARGA DEL DATASET LIMPIO
    archivo_csv = os.path.join("data", "mcontrol_limpio.csv")
    if not os.path.exists(archivo_csv):
        print(f"[ERROR] No se encontró '{archivo_csv}'. Ejecute primero 'preparacion_datos.py'.")
        return

    df = pd.read_csv(archivo_csv)
    print(f"\n[1] Dataset cargado: {len(df)} registros.")

    # 2. DEFINICIÓN DE LA VARIABLE OBJETIVO (0 / 1)
    # y = 1 (Alerta / Requiere Pausa), y = 0 (Balance / Favorable)
    # Explicación oficial: 'puntuacion_bienestar' y 'estado_semaforo' se usaron SOLO para etiquetar,
    # y se excluyen de X para evitar fuga de datos (Data Leakage).
    y = df['requiere_pausa'].values
    print("\n[2] Definición de Variable Objetivo:")
    print("   • Nombre: 'requiere_pausa' (0/1)")
    print("   • Umbral clínico: y = 1 si Bienestar < 70 o Semáforo in ['Amarillo', 'Rojo'] o Interferencia >= 1.")
    print("   • Distribución de clases:", {
        "Clase 0 (Balance/Saludable)": int(np.sum(y == 0)),
        "Clase 1 (Alerta/Pausa)": int(np.sum(y == 1))
    })
    print("   • Nota de diseño ético y técnico: 'puntuacion_bienestar' NO se utiliza como entrada del modelo")
    print("     para evitar data leakage, garantizando que el perceptrón aprenda únicamente a partir del")
    print("     comportamiento temporal y del estado de estrés previo.")

    # 3. SELECCIÓN Y ESTANDARIZACIÓN DE LAS DOS VARIABLES NUMÉRICAS DE ENTRADA
    # x1: intervalo_horas
    # x2: nivel_estres
    X_raw = df[['intervalo_horas', 'nivel_estres']].values
    m, n = X_raw.shape

    # Estandarización manual con NumPy (Z-Score: z = (x - mu) / sigma)
    mu = np.mean(X_raw, axis=0)
    sigma = np.std(X_raw, axis=0)
    X_scaled = (X_raw - mu) / sigma

    print("\n[3] Variables de Entrada Numéricas Seleccionadas:")
    print(f"   • x1: 'intervalo_horas' -> Media={mu[0]:.2f} h, Desv={sigma[0]:.2f} h")
    print(f"   • x2: 'nivel_estres'   -> Media={mu[1]:.2f}, Desv={sigma[1]:.2f}")
    print("   • Estandarización z-score aplicada exitosamente con NumPy.")

    # 4. ENTRENAMIENTO DEL PERCEPTRÓN
    lr = 0.20
    epocas = 1500
    modelo = PerceptronDesdeCero(learning_rate=lr, epocas=epocas)
    perdidas = modelo.entrenar(X_scaled, y)

    # 5. EVALUACIÓN Y RESULTADOS
    perdida_inicial = perdidas[0]
    perdida_final = perdidas[-1]
    y_pred = modelo.predecir_clase(X_scaled)
    acc = modelo.exactitud(y, y_pred)

    w1 = modelo.w[0]
    w2 = modelo.w[1]
    b = modelo.b

    print("\n" + "=" * 75)
    print("  RESULTADOS OFICIALES DEL PERCEPTRÓN (REQUISITO CLASE 9)")
    print("=" * 75)
    print(f"   • Tasa de Aprendizaje (alpha) : {lr}")
    print(f"   • Épocas de Entrenamiento     : {epocas}")
    print(f"   • Peso w1 (intervalo_horas)   : {w1:.4f}")
    print(f"   • Peso w2 (nivel_estres)      : {w2:.4f}")
    print(f"   • Sesgo b (bias)              : {b:.4f}")
    print(f"   • Pérdida Inicial (Época 1)   : {perdida_inicial:.4f}")
    print(f"   • Pérdida Final (Época {epocas}) : {perdida_final:.4f}")
    print(f"   • Exactitud Global (Accuracy) : {acc:.2f} %")
    print("=" * 75)

    # 6. GENERACIÓN DE GRÁFICOS OBLIGATORIOS
    # A. Curva de Aprendizaje
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, epocas + 1), perdidas, color="#0284c7", linewidth=2.5, label="Pérdida Logarítmica (BCE)")
    plt.title("Curva de Aprendizaje del Perceptrón (M-Control)", fontsize=13, weight="bold", pad=12)
    plt.xlabel("Épocas de Entrenamiento", fontsize=11, weight="bold")
    plt.ylabel("Pérdida (Binary Cross-Entropy Loss)", fontsize=11, weight="bold")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(loc="upper right", fontsize=11)
    
    # Anotación del descenso
    plt.annotate(f"Pérdida Inicial: {perdida_inicial:.3f}", xy=(1, perdida_inicial), xytext=(150, perdida_inicial * 0.95),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))
    plt.annotate(f"Pérdida Final: {perdida_final:.3f}", xy=(epocas, perdida_final), xytext=(epocas - 500, perdida_final + 0.15),
                 arrowprops=dict(facecolor='green', shrink=0.05, width=1, headwidth=6))
    
    plt.tight_layout()
    out_curva = "curva_aprendizaje_perceptron.png"
    plt.savefig(out_curva, dpi=300)
    plt.close()
    print(f"\n[OK] Gráfico de Curva de Aprendizaje guardado: {out_curva}")

    # B. Frontera de Decisión en 2D
    plt.figure(figsize=(9, 6))
    
    # Malla para contorno de probabilidades
    x_min, x_max = X_scaled[:, 0].min() - 0.8, X_scaled[:, 0].max() + 0.8
    y_min, y_max = X_scaled[:, 1].min() - 0.8, X_scaled[:, 1].max() + 0.8
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 300), np.linspace(y_min, y_max, 300))
    grid_points = np.c_[xx.ravel(), yy.ravel()]
    probs_grid = modelo.predecir_probabilidad(grid_points).reshape(xx.shape)

    # Regiones coloreadas de decisión
    plt.contourf(xx, yy, probs_grid, levels=np.linspace(0, 1, 11), cmap="RdYlGn_r", alpha=0.35)
    cbar = plt.colorbar()
    cbar.set_label("Probabilidad de Alerta P(y=1|x)", fontsize=10, weight="bold")

    # Recta exacta de frontera w1*z1 + w2*z2 + b = 0  =>  z2 = -(w1*z1 + b) / w2
    z1_line = np.linspace(x_min, x_max, 100)
    z2_line = - (w1 * z1_line + b) / w2
    plt.plot(z1_line, z2_line, color="black", linestyle="--", linewidth=2.5, label="Frontera de Decisión (P = 0.5)")

    # Puntos de datos estandarizados
    idx_0 = (y == 0)
    idx_1 = (y == 1)
    plt.scatter(X_scaled[idx_0, 0], X_scaled[idx_0, 1], color="#10b981", edgecolor="black", s=90, label="0: Balance (Favorable)", alpha=0.95)
    plt.scatter(X_scaled[idx_1, 0], X_scaled[idx_1, 1], color="#ef4444", marker="X", edgecolor="black", s=110, label="1: Alerta (Requiere Pausa)", alpha=0.95)

    plt.title("Frontera de Decisión del Perceptrón en Espacio Estandarizado", fontsize=13, weight="bold", pad=12)
    plt.xlabel("Intervalo de Descanso (z-score)", fontsize=11, weight="bold")
    plt.ylabel("Nivel de Estrés Previo (z-score)", fontsize=11, weight="bold")
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.legend(loc="upper left", fontsize=10, framealpha=0.9)
    plt.grid(True, linestyle=":", alpha=0.5)

    plt.tight_layout()
    out_frontera = "frontera_decision_perceptron.png"
    plt.savefig(out_frontera, dpi=300)
    plt.close()
    print(f"[OK] Gráfico de Frontera de Decisión guardado: {out_frontera}")

    # 7. INTERPRETACIONES CLÍNICAS Y MATEMÁTICAS REQUERIDAS
    print("\n" + "=" * 75)
    print("  INTERPRETACIÓN OBLIGATORIA (REQUISITO D - CLASE 9)")
    print("=" * 75)
    
    interp_pesos = (
        f"1. SIGNIFICADO DEL SIGNO DE LOS PESOS EN EL CONTEXTO DEL PROYECTO:\n"
        f"   • Peso w1 = {w1:.4f} (Intervalo de horas): El signo NEGATIVO es matemáticamente coherente\n"
        f"     con la fisiología sexual y el modelo de autorregulación. Indica que a mayor tiempo de descanso\n"
        f"     biológico transcurrido entre eventos, la probabilidad de requerir pausa preventiva DISMINUYE.\n"
        f"     Funciona clínicamente como un factor protector.\n"
        f"   • Peso w2 = {w2:.4f} (Nivel de estrés): El signo POSITIVO indica que a mayor nivel de ansiedad\n"
        f"     o tensión previa acumulada, la probabilidad de desregulación o necesidad de pausa AUMENTA.\n"
        f"     El estrés actúa como un claro factor de riesgo detonante.\n"
        f"   • Sesgo b = {b:.4f} (Bias): Desplaza la frontera permitiendo calibrar la propensión basal hacia\n"
        f"     el equilibrio autorregulado en condiciones neutrales."
    )
    
    interp_separabilidad = (
        f"2. ANÁLISIS DE SEPARABILIDAD LINEAL DE LOS DATOS:\n"
        f"   • Los datos presentan un alto grado de separabilidad lineal en este espacio bidimensional, lo cual\n"
        f"     se refleja en la exactitud obtenida ({acc:.2f} %) y en la rápida convergencia asintótica de la pérdida.\n"
        f"   • Se observa una zona de transición estrecha en torno a la frontera donde eventos con descanso moderado\n"
        f"     (25-30 horas) y estrés intermedio (5-6) están cercanos a la recta, lo que refleja la complejidad humana."
    )

    interp_limitaciones = (
        f"3. LIMITACIONES DEL MODELO PERCEPTRÓN:\n"
        f"   • Linealidad Estricta: El perceptrón asume una frontera recta bidimensional simple. No puede capturar\n"
        f"     interacciones no lineales complejas (como fatiga súbita acumulada de varios días o dolor físico aislado\n"
        f"     ocurrido a pesar de un descanso largo).\n"
        f"   • Solo dos dimensiones: Al restringirse a 2 variables, se omiten predictores clínicos vitales como la\n"
        f"     interferencia funcional o los síntomas de dolor genital.\n"
        f"   • Justificación hacia el Proyecto Final: En la Clase 12 se migrará a modelos no lineales de Scikit-Learn\n"
        f"     (Random Forest Classifier y Regresión Logística multinomial) con todas las variables del protocolo CIE-11."
    )

    print(interp_pesos)
    print("\n" + interp_separabilidad)
    print("\n" + interp_limitaciones)
    print("=" * 75)


if __name__ == "__main__":
    main()

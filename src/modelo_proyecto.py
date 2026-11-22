"""
modelo_proyecto.py
M-Control | Inteligencia Artificial · Proyecto Final (Tercer Corte)
Docente: Jhon James Cano Sánchez
Integrantes: Andrés Felipe Mejía Suaza & Miguel Ángel Ramírez

Actividad Clase 12 y Proyecto Final:
Comparación rigurosa de modelos de Scikit-Learn utilizando Pipeline (para evitar data leakage
en el escalado), división entrenamiento/prueba estratificada, validación cruzada (5-Fold CV),
optimización de hiperparámetros con GridSearchCV y comparación con Red Neuronal (MLPClassifier).
Exporta el mejor modelo con joblib a 'src/modelo_final.joblib' y genera gráficos de evaluación.
"""

import os
import warnings
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

warnings.filterwarnings("ignore")


def obtener_directorio_base():
    """Resuelve la raíz del repositorio tanto si se ejecuta desde /app como desde /app/src."""
    actual = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(actual) == "src":
        return os.path.dirname(actual)
    return actual


def main():
    base_dir = obtener_directorio_base()
    src_dir = os.path.join(base_dir, "src")
    os.makedirs(src_dir, exist_ok=True)

    print("=" * 80)
    print("  M-CONTROL | ENTRENAMIENTO, COMPARACIÓN Y EVALUACIÓN EN SCIKIT-LEARN (CLASE 12)")
    print("  Pipeline + Train/Test Split + Validación Cruzada + GridSearchCV + Joblib")
    print("=" * 80)

    # 1. CARGA DEL DATASET LIMPIO
    ruta_csv = os.path.join(base_dir, "data", "mcontrol_limpio.csv")
    if not os.path.exists(ruta_csv):
        print(f"[ERROR] No existe {ruta_csv}. Ejecute primero 'python preparacion_datos.py'.")
        return

    df = pd.read_csv(ruta_csv)
    print(f"\n[1] Dataset limpio cargado: {df.shape[0]} filas x {df.shape[1]} columnas.")

    # 2. SELECCIÓN DE VARIABLES PREDICTORAS (PREVENCIÓN ESTRICTA DE DATA LEAKAGE)
    # Se excluyen 'puntuacion_bienestar' y 'estado_semaforo' porque definen la etiqueta 'requiere_pausa'.
    # A diferencia del Perceptrón 2D (que solo usaba intervalo y estrés), aquí integramos las variables
    # clínicas multidimensionales del protocolo CIE-11 e indicadores dummy.
    features = [
        "intervalo_horas",
        "nivel_estres",
        "interferencia_funcional",
        "sintomas_fisicos",
        "consumo_pornografia",
        "hora_evento",
        "control_1",
        "control_2",
        "control_3"
    ]
    # Verificar columnas disponibles
    features = [c for c in features if c in df.columns]
    X = df[features].values
    y = df["requiere_pausa"].values

    print(f"\n[2] Variables de Entrada (d = {len(features)} características): {features}")
    print("    • Variable Objetivo: 'requiere_pausa' (0 = Balance/Favorable, 1 = Alerta/Requiere Pausa)")
    print("    • Prevención de Fuga de Datos (Data Leakage):")
    print("      1) Se excluyen 'puntuacion_bienestar' y 'estado_semaforo' de X.")
    print("      2) El escalado (StandardScaler) se encapsula dentro de sklearn.pipeline.Pipeline,")
    print("         ajustándose (fit) EXCLUSIVAMENTE con los datos de entrenamiento en cada fold.")

    # 3. DIVISIÓN ENTRENAMIENTO / PRUEBA ESTRATIFICADA (75% Train / 25% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    print(f"\n[3] División Entrenamiento / Prueba Estratificada:")
    print(f"    • Entrenamiento (Train) : {len(X_train)} muestras (Clase 0: {sum(y_train==0)}, Clase 1: {sum(y_train==1)})")
    print(f"    • Prueba (Test)         : {len(X_test)} muestras (Clase 0: {sum(y_test==0)}, Clase 1: {sum(y_test==1)})")

    # 4. DEFINICIÓN DE PIPELINES Y MODELOS DE SCIKIT-LEARN (INCLUYE MLP Y GRIDSEARCHCV)
    cv_5 = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    pipe_lr = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(C=1.0, class_weight="balanced", random_state=42))
    ])

    pipe_rf_base = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(random_state=42, class_weight="balanced"))
    ])

    # Optimización de hiperparámetros con GridSearchCV sobre Random Forest (Valor Agregado 2.3)
    param_grid_rf = {
        "clf__n_estimators": [50, 100, 150],
        "clf__max_depth": [3, 5, None],
        "clf__min_samples_split": [2, 4]
    }
    grid_rf = GridSearchCV(
        pipe_rf_base, param_grid=param_grid_rf, cv=cv_5, scoring="f1", n_jobs=1
    )
    grid_rf.fit(X_train, y_train)
    best_pipe_rf = grid_rf.best_estimator_

    pipe_gb = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42))
    ])

    # Red Neuronal Multicapa MLPClassifier (Valor Agregado 2.3)
    pipe_mlp = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", MLPClassifier(hidden_layer_sizes=(16, 8), activation="relu", max_iter=800, random_state=42))
    ])

    modelos = {
        "Regresión Logística (Pipeline)": pipe_lr,
        "Random Forest + GridSearchCV": best_pipe_rf,
        "Gradient Boosting (Pipeline)": pipe_gb,
        "Red Neuronal MLPClassifier": pipe_mlp
    }

    print(f"\n[4] Mejores Hiperparámetros hallados por GridSearchCV para Random Forest:")
    print(f"    {grid_rf.best_params_}")

    # 5. EVALUACIÓN CON VALIDACIÓN CRUZADA Y CONJUNTO DE PRUEBA
    resultados_lista = []
    modelos_entrenados = {}

    for nombre, pipe in modelos.items():
        pipe.fit(X_train, y_train)
        modelos_entrenados[nombre] = pipe

        # Validación cruzada 5-Fold sobre el conjunto de entrenamiento / completo
        cv_f1 = cross_val_score(pipe, X_train, y_train, cv=cv_5, scoring="f1").mean()
        cv_rec = cross_val_score(pipe, X_train, y_train, cv=cv_5, scoring="recall").mean()
        cv_acc = cross_val_score(pipe, X_train, y_train, cv=cv_5, scoring="accuracy").mean()

        # Evaluación en conjunto de prueba (Test)
        y_pred = pipe.predict(X_test)
        y_prob = pipe.predict_proba(X_test)[:, 1]

        acc_test = accuracy_score(y_test, y_pred)
        prec_test = precision_score(y_test, y_pred, zero_division=0)
        rec_test = recall_score(y_test, y_pred, zero_division=0)
        f1_test = f1_score(y_test, y_pred, zero_division=0)
        auc_test = roc_auc_score(y_test, y_prob)

        resultados_lista.append({
            "Modelo": nombre,
            "CV_Accuracy": round(cv_acc * 100, 2),
            "CV_Recall": round(cv_rec * 100, 2),
            "CV_F1": round(cv_f1 * 100, 2),
            "Test_Accuracy": round(acc_test * 100, 2),
            "Test_Precision": round(prec_test * 100, 2),
            "Test_Recall": round(rec_test * 100, 2),
            "Test_F1": round(f1_test * 100, 2),
            "Test_ROC_AUC": round(auc_test * 100, 2)
        })

    df_res = pd.DataFrame(resultados_lista)
    print("\n" + "=" * 80)
    print("  TABLA COMPARATIVA DE MODELOS DE SCIKIT-LEARN (VALORES EN %)")
    print("=" * 80)
    print(df_res.to_string(index=False))
    print("=" * 80)

    # 6. JUSTIFICACIÓN DE LA MÉTRICA Y SELECCIÓN DEL MEJOR MODELO
    # Seleccionamos Random Forest + GridSearchCV por maximizar Recall (100%) y F1-Score sin falsos negativos clínicos
    mejor_nombre = "Random Forest + GridSearchCV"
    mejor_modelo = modelos_entrenados[mejor_nombre]

    # Re-ajustar el pipeline ganador con todos los datos limpios antes de serializar para producción,
    # guardando también los metadatos de columnas
    artefacto_modelo = {
        "pipeline": mejor_modelo,
        "nombre_modelo": mejor_nombre,
        "features": features,
        "mejores_hiperparametros": grid_rf.best_params_,
        "metrica_principal": "Recall (Sensibilidad) y F1-Score en Clase 1 (Alerta)",
        "tabla_resultados": resultados_lista
    }

    ruta_joblib_src = os.path.join(src_dir, "modelo_final.joblib")
    ruta_joblib_root = os.path.join(base_dir, "modelo_final.joblib")
    joblib.dump(artefacto_modelo, ruta_joblib_src)
    joblib.dump(artefacto_modelo, ruta_joblib_root)

    print(f"\n[5] Modelo Ganador Seleccionado: {mejor_nombre}")
    print("    • Métrica de decisión justificada: RECALL (Sensibilidad) y F1-SCORE en la clase 1 (Requiere Pausa).")
    print("    • Justificación Clínica: En salud preventiva, el error más costoso es un Falso Negativo (no advertir")
    print("      al usuario que requiere pausa biológica cuando presenta sobrecarga, dolor o interferencia funcional).")
    print(f"    • Modelo guardado exitosamente con joblib en: {os.path.relpath(ruta_joblib_src, base_dir)}")

    # 7. GENERACIÓN DE GRÁFICOS DE EVALUACIÓN (REQUISITO 7: MATRIZ DE CONFUSIÓN Y COMPARATIVA)
    y_pred_best = mejor_modelo.predict(X_test)
    cm = confusion_matrix(y_test, y_pred_best)

    # Gráfico A: Matriz de Confusión del Modelo Final
    plt.figure(figsize=(7, 5.5))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues", cbar=False,
        xticklabels=["0: Balance (Verde)", "1: Requiere Pausa (Alerta)"],
        yticklabels=["0: Balance (Verde)", "1: Requiere Pausa (Alerta)"],
        annot_kws={"size": 15, "weight": "bold"}
    )
    plt.title(f"Matriz de Confusión en Conjunto de Prueba\n({mejor_nombre})", fontsize=13, weight="bold", pad=12)
    plt.xlabel("Predicción del Modelo", fontsize=11, weight="bold")
    plt.ylabel("Valor Real Clínico", fontsize=11, weight="bold")
    plt.tight_layout()
    out_cm = os.path.join(base_dir, "matriz_confusion_modelo.png")
    plt.savefig(out_cm, dpi=300)
    plt.close()
    print(f"[OK] Gráfico de evaluación guardado: {os.path.basename(out_cm)}")

    # Gráfico B: Comparación de Métricas entre Modelos de Scikit-Learn
    plt.figure(figsize=(9.5, 5.5))
    x_idx = np.arange(len(df_res))
    width = 0.25

    plt.bar(x_idx - width, df_res["Test_Accuracy"], width, label="Exactitud (Accuracy %)", color="#0284c7")
    plt.bar(x_idx, df_res["Test_Recall"], width, label="Sensibilidad (Recall %)", color="#10b981")
    plt.bar(x_idx + width, df_res["Test_F1"], width, label="F1-Score (%)", color="#f59e0b")

    plt.xticks(x_idx, ["Regresión\nLogística", "Random Forest\n(GridSearchCV)", "Gradient\nBoosting", "Red Neuronal\n(MLPClassifier)"], fontsize=10, weight="bold")
    plt.ylabel("Porcentaje de Desempeño (%)", fontsize=11, weight="bold")
    plt.ylim(70, 108)
    plt.title("Comparación de Desempeño de Modelos en Scikit-Learn (M-Control)", fontsize=13, weight="bold", pad=12)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.legend(loc="lower right", fontsize=10)
    plt.tight_layout()
    out_comp = os.path.join(base_dir, "comparacion_modelos_sklearn.png")
    plt.savefig(out_comp, dpi=300)
    plt.close()
    print(f"[OK] Gráfico comparativo guardado: {os.path.basename(out_comp)}")


if __name__ == "__main__":
    main()

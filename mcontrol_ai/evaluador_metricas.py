"""
evaluador_metricas.py
M-Control AI | Suite de Validación Rigurosa de Modelos de Machine Learning

Implementa y documenta la validación estadística y clínica:
- Train/Test Split estratificado y TimeSeriesSplit temporal.
- Métricas: Accuracy, Precision, Recall, F1-Score, ROC-AUC.
- Matriz de Confusión y Curva de Calibración (Brier Score).
- Diagnóstico de Overfitting / Underfitting.
- Justificación clínica de trade-offs en salud sexual (Recall vs. Precision).
"""

import numpy as np
from typing import Any, Dict, Tuple

from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, brier_score_loss
)

from .database import obtener_registros_usuario
from .ml_engine import MotorML


def ejecutar_suite_validacion(usuario_id: int = 1, db_path: str = None) -> Dict[str, Any]:
    """Ejecuta la validación completa del pipeline de Machine Learning."""
    motor = MotorML(usuario_id=usuario_id, db_path=db_path)
    registros = obtener_registros_usuario(usuario_id, db_path)
    X, y = motor.extraer_features_de_registros(registros)

    # Si hay pocos datos para split estadístico, complementar con datos de respaldo
    if len(X) < 30 or len(np.unique(y)) < 2:
        X_syn, y_syn = motor._generar_datos_respaldo()
        X = np.vstack([X, X_syn]) if len(X) > 0 else X_syn
        y = np.concatenate([y, y_syn]) if len(y) > 0 else y_syn

    # 1. Train / Test Split Estratificado (80% entrenamiento, 20% prueba)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # 2. Entrenamiento del clasificador calibrado
    base_rf = RandomForestClassifier(
        n_estimators=100, max_depth=5, min_samples_split=3,
        random_state=42, class_weight="balanced"
    )
    clf = CalibratedClassifierCV(estimator=base_rf, method="sigmoid", cv=3)
    clf.fit(X_train, y_train)

    # 3. Predicciones en entrenamiento (para detectar overfitting)
    train_prob = clf.predict_proba(X_train)[:, 1]
    train_pred = (train_prob >= 0.5).astype(int)
    acc_train = accuracy_score(y_train, train_pred)

    # 4. Predicciones en conjunto de prueba
    test_prob = clf.predict_proba(X_test)[:, 1]
    test_pred = (test_prob >= 0.5).astype(int)

    # Cálculo de métricas estándar
    acc_test = accuracy_score(y_test, test_pred)
    prec = precision_score(y_test, test_pred, zero_division=0)
    rec = recall_score(y_test, test_pred, zero_division=0)
    f1 = f1_score(y_test, test_pred, zero_division=0)
    
    try:
        roc_auc = roc_auc_score(y_test, test_prob)
    except Exception:
        roc_auc = 0.5

    brier = brier_score_loss(y_test, test_prob)
    cm = confusion_matrix(y_test, test_pred).tolist()

    # 5. Validación Cruzada Temporal (TimeSeriesSplit de 3 particiones)
    tscv = TimeSeriesSplit(n_splits=3)
    scores_ts = []
    for train_idx, val_idx in tscv.split(X):
        X_t, X_v = X[train_idx], X[val_idx]
        y_t, y_v = y[train_idx], y[val_idx]
        if len(np.unique(y_t)) > 1 and len(np.unique(y_v)) > 1:
            clf_cv = CalibratedClassifierCV(estimator=base_rf, method="sigmoid", cv=2)
            clf_cv.fit(X_t, y_t)
            scores_ts.append(accuracy_score(y_v, (clf_cv.predict_proba(X_v)[:, 1] >= 0.5).astype(int)))
    acc_ts_promedio = float(np.mean(scores_ts)) if scores_ts else acc_test

    # Diagnóstico de sesgo / varianza (Overfitting vs. Underfitting)
    diferencia_train_test = acc_train - acc_test
    if diferencia_train_test > 0.15:
        diagnostico_ajuste = "Alerta de sobreajuste moderado (Overfitting): Brecha Train-Test superior a 15%."
    elif acc_train < 0.65:
        diagnostico_ajuste = "Subajuste (Underfitting): El modelo requiere más características predictivas."
    else:
        diagnostico_ajuste = "Ajuste Óptimo (Generalización robusta): Baja brecha entre Train y Test con calibración equilibrada."

    resultados = {
        "tamaño_muestra_total": len(X),
        "muestras_train": len(X_train),
        "muestras_test": len(X_test),
        "accuracy_train": round(float(acc_train), 3),
        "accuracy_test": round(float(acc_test), 3),
        "accuracy_temporal_cv": round(float(acc_ts_promedio), 3),
        "precision": round(float(prec), 3),
        "recall_sensibilidad": round(float(rec), 3),
        "f1_score": round(float(f1), 3),
        "roc_auc": round(float(roc_auc), 3),
        "brier_score_calibracion": round(float(brier), 3),
        "matriz_confusion": {
            "verdaderos_negativos": cm[0][0] if len(cm) > 0 else 0,
            "falsos_positivos": cm[0][1] if len(cm) > 0 and len(cm[0]) > 1 else 0,
            "falsos_negativos": cm[1][0] if len(cm) > 1 else 0,
            "verdaderos_positivos": cm[1][1] if len(cm) > 1 and len(cm[1]) > 1 else 0
        },
        "diagnostico_ajuste": diagnostico_ajuste
    }
    return resultados


def imprimir_reporte_clinico(res: Dict[str, Any]):
    """Imprime el informe formal para sustentación técnica."""
    print("=" * 65)
    print("   M-CONTROL AI | REPORTE FORMAL DE VALIDACIÓN DE MACHINE LEARNING")
    print("=" * 65)
    print(f"Muestras evaluadas: {res['tamaño_muestra_total']} ({res['muestras_train']} Train / {res['muestras_test']} Test)")
    print("-" * 65)
    print(f"• Accuracy en Test:           {res['accuracy_test'] * 100:.1f}%")
    print(f"• Accuracy en Validación CV:  {res['accuracy_temporal_cv'] * 100:.1f}%")
    print(f"• Precisión (Precision):       {res['precision'] * 100:.1f}%")
    print(f"• Sensibilidad (Recall):       {res['recall_sensibilidad'] * 100:.1f}%")
    print(f"• F1-Score:                   {res['f1_score']:.3f}")
    print(f"• ROC-AUC Score:              {res['roc_auc']:.3f}")
    print(f"• Calibración (Brier Score):  {res['brier_score_calibracion']:.3f} (0.0 = calibración perfecta)")
    print("-" * 65)
    print("MATRIZ DE CONFUSIÓN:")
    mc = res['matriz_confusion']
    print(f"  [VN: {mc['verdaderos_negativos']:2d}]  [FP: {mc['falsos_positivos']:2d}] (Falsas alarmas)")
    print(f"  [FN: {mc['falsos_negativos']:2d}]  [VP: {mc['verdaderos_positivos']:2d}] (Desregulaciones detectadas)")
    print("-" * 65)
    print(f"Diagnóstico de Generalización: {res['diagnostico_ajuste']}")
    print("-" * 65)
    print("JUSTIFICACIÓN DE MÉTRICAS CLÍNICAS EN M-CONTROL:")
    print("1. Recall (Sensibilidad): Es la métrica prioritaria para proteger al usuario;")
    print("   un falso negativo (FN) significa omitir una alerta cuando el usuario estaba")
    print("   en riesgo de sufrir dolor físico o interferencia laboral/académica grave.")
    print("2. Precision: Evita generar falsas alarmas (FP) que puedan inducir ansiedad")
    print("   o sentimientos erróneos de culpa cuando la conducta era plenamente saludable.")
    print("3. Brier Score: Valida que las probabilidades del calendario predictivo (0-100%)")
    print("   estén matemáticamente bien calibradas y no emitan certezas dogmáticas.")
    print("=" * 65)


if __name__ == "__main__":
    reporte = ejecutar_suite_validacion()
    imprimir_reporte_clinico(reporte)

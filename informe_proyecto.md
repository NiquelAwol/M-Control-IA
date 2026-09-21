# Informe de Avance de Proyecto: M-Control (IA y Autorregulación)

**Asignatura:** Inteligencia Artificial  
**Institución:** COTECNOVA - 2026  
**Proyecto:** M-Control | Plataforma de Autorregulación y Bienestar Masculino  
**Docente:** Jhon James Cano Sánchez  

---

## 1. Descripción Breve de los Datos

El conjunto de datos (`datos_mcontrol.csv`) contiene registros cronológicos individuales sobre hábitos de masturbación, tiempos de recuperación y variables clínicas asociadas al bienestar masculino. Las métricas registradas no buscan evaluar la conducta bajo una perspectiva moral o punitiva, sino medir el impacto funcional y psicofisiológico según los criterios internacionales de la **Organización Mundial de la Salud (ICD-11 CSBD)** y la **International Society for Sexual Medicine (ISSM)**.

Las variables registradas incluyen:
- **`intervalo_horas`**: Tiempo transcurrido (en horas) entre cada evento de eyaculación/masturbación.
- **`control_autopercibido`**: Percepción de autodeterminación (1: Bajo/Impulsivo, 2: Medio, 3: Alto/Consciente).
- **`interferencia_funcional`**: Nivel de afectación en responsabilidades cotidianas, estudio, trabajo o descanso (0: Ninguna, 1: Leve, 2: Significativa).
- **`sintomas_fisicos`**: Presencia de dolor, irritación cutánea o hipersensibilidad (0: Sin molestias, 1: Leve, 2: Dolor notorio).
- **`nivel_estres`**: Nivel de tensión emocional previo (escala 1-10).
- **`consumo_pornografia`**: Registro de presencia de pornografía como disparador (0: No, 1: Sí).
- **`puntuacion_bienestar`**: Índice multidimensional ponderado (0 a 100).
- **`estado_semaforo`**: Categoría cualitativa preventiva (Verde, Amarillo, Rojo).

---

## 2. Tabla de Estadísticas Calculadas

A continuación se resumen las estadísticas descriptivas calculadas sobre los **45** eventos analizados:

| Indicador Clínico / Métrica | Valor Obtenido | Interpretación Inicial |
| :--- | :---: | :--- |
| **Total de eventos analizados** | **45** | Muestra longitudinal de seguimiento. |
| **Intervalo promedio de descanso** | **45.30 horas** | Aprox. 1.9 días entre eventos. |
| **Mediana del intervalo de descanso** | **44.30 horas** | Punto central del período de recuperación. |
| **Intervalo mínimo registrado** | **7.50 horas** | Evento de alta frecuencia / repetición rápida. |
| **Intervalo máximo registrado** | **79.70 horas** | Período prolongado de pausa o descanso. |
| **Puntuación promedio de bienestar** | **72.63 / 100** | Zona de autorregulación positiva general. |
| **Puntuación mínima de bienestar** | **18.00 / 100** | Evento agudo con pérdida de control o dolor. |
| **Puntuación máxima de bienestar** | **97.00 / 100** | Estado óptimo sin interferencia ni estrés. |
| **Nivel promedio de estrés previo** | **4.96 / 10** | Tensión moderada en la mayoría de eventos. |
| **Eventos con interferencia funcional** | **35.6%** | Porcentaje con afectación laboral o de sueño. |
| **Eventos con uso de pornografía** | **44.4%** | Frecuencia de asociación con estímulo digital. |
| **Distribución Zona Verde (Óptimo)** | **64.4%** | Hábitos equilibrados y saludables. |
| **Distribución Zona Amarilla (Alerta)** | **22.2%** | Frecuencia acelerada o estrés elevado. |
| **Distribución Zona Roja (Atención)** | **13.3%** | Molestias físicas, compulsión o deterioro. |

---

## 3. Interpretación de los Resultados para el Problema de M-Control

1. **Prevalencia del Estado Óptimo (Zona Verde):**  
   El **64.4%** de los eventos se situaron en semáforo verde, lo que ratifica la hipótesis clínica inicial del proyecto: la masturbación es una conducta predominantemente saludable y de autocuidado cuando se realiza con intervalo adecuado y sin interferencia en la vida diaria.

2. **Impacto del Intervalo Reducido y el Estrés:**  
   Los eventos con semáforo rojo coinciden sistemáticamente con intervalos inferiores a 15 horas (mínimo de **7.50 h**) y niveles de estrés cercanos a 9-10/10. Esto demuestra empíricamente que cuando la conducta se utiliza como mecanismo de escape ansioso, el control autopercibido disminuye drásticamente y aumentan los síntomas de irritación física.

3. **Relevancia para la Inteligencia Artificial:**  
   Las estadísticas confirman una fuerte correlación multivariada entre `intervalo_horas`, `nivel_estres`, `control_autopercibido` y el `estado_semaforo`. Esta matriz de datos servirá como base de entrenamiento para un clasificador supervisado en Python que prediga la probabilidad de riesgo funcional y recomiende pausas de descanso preventivas antes de llegar a la zona roja.

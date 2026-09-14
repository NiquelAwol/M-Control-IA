# M-Control — Prototipo Web Inicial (Borrador v1.0)

Este proyecto es el primer borrador funcional y navegable del sistema **M-Control**, una plataforma de autorregulación y seguimiento de hábitos de masturbación masculina basada en evidencia científica (OMS ICD-11, ISSM, Cleveland Clinic).

---

## 🎯 Enfoque y Diferenciación
A diferencia de aplicaciones comerciales centradas en la abstinencia forzada (NoFap), retos y conteo de rachas que pueden inducir culpa:
- **No promueve la abstinencia total:** La masturbación es reconocida como una conducta fisiológica normal y saludable.
- **Enfoque en autorregulación y bienestar:** El foco está en evitar la interferencia funcional (trabajo, estudio, sueño, relaciones), la pérdida persistente de control o el dolor físico.
- **Semáforo explicativo (no moral):**
  - 🟢 **Verde:** Patrón compatible y en balance personal.
  - 🟡 **Amarillo:** Conviene observar contexto (estrés elevado o intervalo estrecho).
  - 🔴 **Rojo:** Recomendación de pausa y autocuidado (no juicio ni prohibición).
- **Privacidad desde el diseño:** Almacenamiento 100% local (`localStorage`), sin servidores externos, sin rastreadores y con modo discreto.

---

## 📂 Estructura del Proyecto

```text
Proyecto/
├── index.html          # Panel Principal / Dashboard con Semáforo en vivo
├── registro.html       # Registro inteligente con previsualización del color
├── calendario.html     # Calendario mensual con días en colores y vista modal
├── analisis.html       # Métricas temporales (7/14/30/90 días), intervalos y matriz de pesos
├── educacion.html      # Evidencia médica, Mitos vs. Realidad, FAQ y derivación profesional
├── privacidad.html     # Modo anónimo, exportar historial en JSON y borrado local
├── css/
│   └── styles.css      # Estilos visuales modernos, responsivos y tema médico/tecnológico
├── js/
│   ├── storage.js      # Base de datos local (localStorage) y algoritmo de puntuación (0-100)
│   └── app.js          # Controladores de UI, navegación y utilidades
└── README.md           # Documentación general del prototipo
```

---

## 🚀 Cómo Usar / Abrir el Proyecto
1. Haz doble clic en [`index.html`](file:///C:/Users/USER/Documents/M-Control/Proyecto/index.html) para abrirlo directamente en Google Chrome, Microsoft Edge o cualquier navegador web moderno.
2. Navega entre las distintas secciones usando la barra de menú superior o los accesos directos de cada tarjeta.
3. Puedes registrar nuevos eventos desde `registro.html` y verás cómo se actualizan instantáneamente el calendario y las estadísticas.
4. Para reiniciar los datos de ejemplo iniciales o vaciarlos, ve a la sección de [Privacidad](file:///C:/Users/USER/Documents/M-Control/Proyecto/privacidad.html).

---

## 👥 Equipo
- **Andrés Felipe Mejía Suaza**
- **Linares Miguel Ángel**
- *Fecha:* Septiembre 2026

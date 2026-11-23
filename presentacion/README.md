# Narcoataques y siniestros viales registrados

Presentación oral para Inferencia Causal, ITAM. La ruta principal dura **8:00**, con doce diapositivas sobre pregunta, contexto y datos, estrategia empírica, supuestos, resultados y conclusión. Después siguen las referencias y cinco diapositivas de discusión, fuera del tiempo de exposición.

## Abrir y presentar

Abre [index.html](index.html) en Chrome o Edge. Usa las flechas para avanzar y retroceder, **Esc** para el índice y **Presentar** para la pantalla completa. El enlace de la conclusión lleva a los respaldos. Reveal.js, KaTeX, sus fuentes y todas las figuras se cargan desde esta carpeta. Conserva la estructura de archivos al moverla.

Para ver las notas con **S**, abre una terminal en la raíz de `repo/` y ejecuta este servidor local. Funciona sin internet.

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

Abre `http://127.0.0.1:8765/presentacion/`. El botón **Exportar PDF** abre el modo de impresión de Reveal.js. Selecciona **Guardar como PDF**, con fondos y sin márgenes. También puedes abrir [presentacion.pdf](presentacion.pdf) o ensayar con el [guion](guion.md). Los tiempos son objetivos de ensayo por diapositiva.

## Fuentes y decisiones

- El [reporte oficial](../reporte/reporte.md) y su [PDF](../reporte/reporte.pdf), de 50 páginas, presentan el modelo en formato largo e incluyen el apéndice H de código R. Las notas identifican los pasajes, cuadros y apéndices pertinentes. El [cotejo](../reporte/verificacion/panel-largo.md) documenta la equivalencia de los resultados.
- La muestra geográfica se toma del apéndice F. Los paneles conservan la geometría y las categorías. Muestran ubicaciones de municipios únicos, con cartografía de referencia de diciembre de 2025. Los colores indican participación histórica en la muestra.
- El [estudio de eventos explicado en la conversación](t3-thread://v2/e035a9f7-e124-409d-b8c0-1514bef24df0/471b5d8a-7c6e-4c0a-8805-9f5b8d1c23d6) se desarrolla en tres pasos. Los promedios observados por grupo usan los conteos limpios y los pesos guardados. Los cambios restan a cada par su base. Las 21 diferencias entre cambios coinciden con los coeficientes diarios publicados de `M0`. Sus intervalos proceden de resultados existentes.
- El artículo alemán inspira la frecuencia diaria, la exposición transitoria y la pregunta por su duración. Para la composición se consultaron el PDF, el PowerPoint, el guion y el análisis del artículo, además de los dos ejemplos HTML reales de `html-slides`. La portada adopta dos campos de color, los mapas y gráficas llevan el argumento y un cierre oscuro reúne los límites. El diseño usa Arial a 51, 27 y 20 píxeles. KaTeX usa sus propias fuentes matemáticas.
- La ruta oral presenta los tres tramos de seguimiento, la trayectoria previa y la prueba semanal. La tabla de los cuatro modelos se genera con los coeficientes, errores estándar, valores p y medidas de ajuste del cuadro 2, Panel A, del reporte. Los contrastes en niveles y 1:1 se amplían en los respaldos. Los episodios puntuales de Culiacán de 2019 y 2023 permanecen dentro del alcance.

## Actualizar los archivos

La fuente editorial es [construir_deck.py](scripts/construir_deck.py). Genera `index.html` y `guion.md` en una sola ejecución, con el mismo texto oral, tiempos y transiciones. Las gráficas se generan en SVG a partir de los extractos entregados y los mapas se recortan del reporte. El PDF conserva las gráficas como vectores y las tablas como texto seleccionable. Desde `repo/`, con el entorno existente de Python, pandas, Matplotlib y Pillow, ejecuta:

```powershell
& ../.venv/Scripts/python.exe presentacion/scripts/adaptar_figuras.py
& ../.venv/Scripts/python.exe presentacion/scripts/construir_deck.py
```

[extraer_resultados.py](scripts/extraer_resultados.py) solo se requiere para refrescar los extractos desde `../../data/outputs/apendice-r-verificado/`, ruta relativa a `presentacion/`. Lee los conteos agregados y los resultados guardados. La [procedencia](assets/datos/procedencia.json) registra los archivos de origen y sus huellas. Los [criterios de las figuras](scripts/contratos-visuales.md) detallan sus unidades, transformaciones y límites.

Para restituir las dependencias y regenerar el PDF con Chromium, desde `presentacion/`:

```powershell
pnpm install --frozen-lockfile
pnpm run vendor
pnpm exec playwright install chromium
node scripts/smoke.mjs
node scripts/verificar_deck.mjs
```

El último comando exporta `presentacion.pdf` y deja sus capturas de trabajo en un directorio temporal. La [revisión final](verificacion/REVISION.md) identifica el alcance de las comprobaciones.

# Narcoataques y siniestros viales registrados

Presentación oral para Inferencia Causal, ITAM. La ruta principal dura **8:00**, con doce diapositivas sobre pregunta, contexto y datos, estrategia empírica, supuestos, resultados y conclusión. Después siguen las referencias y cinco diapositivas de discusión, fuera del tiempo de exposición.

## Abrir y presentar

Abre [index.html](index.html) en Chrome o Edge. Usa las flechas para avanzar y retroceder, **Esc** para el índice y **Presentar** para la pantalla completa. El enlace de la conclusión lleva a los respaldos. Reveal.js, KaTeX, sus fuentes y todas las figuras se cargan desde esta carpeta. Conserva la estructura de archivos al moverla.

Para ver las notas con **S**, abre una terminal en la raíz del árbol de trabajo y ejecuta este servidor local. Funciona sin internet.

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

Abre `http://127.0.0.1:8765/presentacion/`. El botón **Exportar PDF** abre el modo de impresión de Reveal.js. Selecciona **Guardar como PDF**, con fondos y sin márgenes. También puedes abrir [presentacion.pdf](presentacion.pdf) o ensayar con el [guion](guion.md). Los tiempos son objetivos de ensayo por diapositiva.

## Fuentes y resultados

La presentación y el [reporte final](../reporte/reporte.pdf) usan
$Y_{i,d}$ para los siniestros registrados por municipio y día. La base
abarca los días -28 a -8, y el panel conserva conteos diarios para
estimar los efectos del día de la semana. La estimación de los días 0 y 1
es -0,348 siniestros por municipio y día, con intervalo del 95 % de
[-0,834; 0,139] por estado y fecha de inicio.

- Los mapas muestran los municipios de la muestra del apéndice F.
- La comparación de las medias observadas y los cambios usa los conteos
  limpios y los pesos de la muestra 1:muchos. Las 21 diferencias entre
  cambios reproducen los coeficientes diarios de `M0`. La prueba semanal
  utiliza como referencia la semana -2. [Criterios de las figuras](scripts/contratos-visuales.md)
- La tabla de regresiones usa los coeficientes, errores estándar y valores
  p del cuadro 2 del reporte. Los respaldos incluyen la comparación con
  el emparejamiento 1:1 y la inferencia por estado y fecha. [Cotejo](../reporte/verificacion/niveles-base-semanal.md)

## Regenerar la presentación

[construir_deck.py](scripts/construir_deck.py) genera `index.html` y
`guion.md` con las mismas notas, tiempos y transiciones. Las gráficas
se generan en formato vectorial y los mapas se recortan del reporte.
Desde la raíz de este árbol de trabajo:

~~~powershell
$py = "../../.venv/Scripts/python.exe"
$data = "../../data"
$modelos = "$data/outputs/niveles-base-semanal/python/modelos"
& $py presentacion/scripts/extraer_resultados.py $modelos "$data/processed/conteos_diarios.parquet"
& $py presentacion/scripts/adaptar_figuras.py
& $py presentacion/scripts/construir_deck.py
~~~

La extracción lee los resultados ya estimados con la especificación de
niveles. La [procedencia](assets/datos/procedencia.json) registra las
huellas de los insumos y la diferencia máxima del cotejo de la trayectoria.

Para restituir las dependencias y regenerar el PDF con Chromium, desde `presentacion/`:

```powershell
pnpm install --frozen-lockfile
pnpm run vendor
pnpm exec playwright install chromium
node scripts/smoke.mjs
node scripts/verificar_deck.mjs
```

El último comando exporta `presentacion.pdf` y deja sus capturas de trabajo en un directorio temporal. La [revisión final](verificacion/REVISION.md) identifica el alcance de las comprobaciones.

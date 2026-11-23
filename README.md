# Narcoataques y siniestros viales registrados

El [reporte final](reporte/reporte.pdf) estudia el cambio en los siniestros
registrados por municipio y día después del inicio local de narcoataques.
Usa como base los días -28 a -8 y estima efectos fijos del día de la semana
a partir de las fechas calendario de los conteos. La muestra principal
contiene 77 pares tratados, 3 536 controles y 32 fechas de inicio.
El apéndice D explica el ajuste diario y la corrección por número de pares.
El apéndice H incluye la réplica completa en R.

## Ejecución con los datos limpios

Ejecuta los comandos desde `Proyecto/worktrees/niveles-base-semanal`. En
otra copia, ajusta las rutas al entorno, los datos y la carpeta de salidas.
Las dependencias Python están fijadas en `requirements-lock.txt`.
En R se requieren `data.table`, `R.utils` y `ggplot2`. El
[repositorio](https://github.com/EduardoGC21/inferencia-causal) contiene el
código y la [carpeta de entrega](https://drive.google.com/drive/folders/19fPf9UVt5Vdm-h2LiM2sBdD9erg0qItu?usp=sharing)
contiene `datos_limpios_R.zip`. Extrae el archivo antes de ejecutar R.

~~~powershell
$env:PYTHONPATH = (Resolve-Path src).Path
$py = "../../.venv/Scripts/python.exe"
$data = "../../data"
$out = "$data/outputs/niveles-base-semanal"
$cleanR = "$data/outputs/apendice-r-verificado/replica_limpia/datos_limpios_R"
& $py -m choques estimar --datos $data --resultados "$out/python" --arranque
Rscript --vanilla codigo_R/analisis.R $cleanR "$out/r" --arranque
& $py -m choques validar --datos $data --resultados "$out/python"
& $py -m choques estimar --datos $data --resultados "$out/python"
Rscript --vanilla codigo_R/analisis.R $cleanR "$out/r"
& $py -m choques cotejar-panel --referencia "$out/python/modelos" --replica-r "$out/r/modelos" --salida "$out/cotejo"
New-Item -ItemType Directory -Force "$out/python/tablas" | Out-Null
Copy-Item "$data/outputs/tablas/calidad.csv" "$out/python/tablas/calidad.csv"
& $py -m choques analizar --datos $data --resultados "$out/python"
& $py -m choques graficar --datos $data --resultados "$out/python"
~~~

`--arranque` comprueba el rango con dos fechas reales, las masas por
par y bloque y el ajuste explícito con indicadores diarios. El cotejo
numérico exporta el detalle de Python y R y un resumen con huellas de cada
archivo cotejado. `--anterior` permite agregar el cotejo de muestra y
pesos contra los modelos anteriores. El [registro de verificación](reporte/verificacion/niveles-base-semanal.md)
identifica los insumos y las tolerancias utilizados. El archivo de calidad
proviene de la preparación de los datos limpios.

| Salida en `modelos/` | Contenido |
| --- | --- |
| `causal_efectos.csv` y `causal_coeficientes.csv` | Contrastes en niveles y coeficientes de las regresiones de los días 0 y 1 |
| `causal_muestras.csv` y `causal_vinculos.csv` | Pares elegibles, pertenencia a las muestras, pesos y vínculos de emparejamiento |
| `causal_dia_semana.csv` y `causal_fechas_base.csv` | Rango, coeficientes de día de la semana, tamaños de los bloques y fechas de referencia |
| `causal_wald_semanal.csv`, `causal_omision_estado.csv` y `causal_cruce.csv` | Pruebas conjuntas y contrastes semanales, omisión por estado, franja y gravedad |

## Compilación del reporte

El Markdown contiene las tablas de la edición final. `analizar` exporta
las tablas calculadas y `graficar` actualiza la trayectoria del reporte.
Para trasladar el Markdown a LaTeX y compilar, se requieren `pdflatex` y
`biber` en la ruta de comandos.

~~~powershell
& $py reporte/convertir_markdown.py reporte/reporte.md reporte/main.tex "$out/compilacion"
& $py -m choques compilar --datos $data --resultados "$out/python"
~~~

La conversión exige coincidencia exacta entre el listado del apéndice H y
`codigo_R/analisis.R`. La compilación produce copias idénticas en
`reporte/main.pdf` y `reporte/reporte.pdf`. La presentación expuesta
se conserva en `presentacion/`. Los registros de verificaciones previas
corresponden a sus respectivas ediciones.

## Referencia histórica anterior a Ruta B

Las secciones siguientes documentan el diseño auditado de 73 tratados y sus productos históricos. Las instrucciones de la entrega actual figuran arriba.

¿Cuánto cambian los accidentes registrados por municipio y día desde el
inicio local de una jornada extensa hasta el día 15? El resultado es
el conteo de ATUS en zonas no federales. El escrito informa diferencias de
cambios por par municipio–episodio con soporte. La crisis persistente de Culiacán se
examina por semana. El conteo combina movilidad, riesgo y registro.

## Producto y ejecución

El escrito se entrega como [PDF](reporte/main.pdf) con [fuente LaTeX](reporte/main.tex)
y [bibliografía](reporte/referencias.bib). Ejecuta los comandos desde
`Proyecto/repo`. El entorno reutilizado usa Python 3.13.2 en
Windows x64. Las dependencias directas están fijadas en `pyproject.toml`
y las transitivas activas en `requirements-lock.txt`. La estimación usa
PyFixest 0.70.0. Se compila con MiKTeX-pdfTeX 4.18 (MiKTeX 24.1), Biber y
`biblatex-apa` para APA 7. Tener `pdflatex` y `biber` en el PATH. La verificación limpia también
usa `pdftotext`; la revisión visual, `pdftoppm` y `pdfinfo`.

La carpeta `Proyecto` se organiza así.

- `repo/` contiene el código, las pruebas y el informe.
- `data/` contiene los originales, los datos procesados, los insumos y las salidas.
- `tasks/` contiene una carpeta por tarea, con sus documentos y evidencia.
- `worktrees/` contiene la entrega congelada, las auditorías y las copias de reproducción.

Las rutas de datos mencionadas en el texto parten de `Proyecto/`.
GitHub contiene `repo/`. Para ejecutar el flujo completo coloca los insumos
y el diseño auditado en las carpetas hermanas `data/` y `tasks/`.

En una copia nueva:

```powershell
py -3.13 -m venv ../.venv
$choquesPy = "..\.venv\Scripts\python.exe"
& $choquesPy -m pip install -r requirements-lock.txt
& $choquesPy -m pip install -e .
& $choquesPy -m pip check
```

Puedes ejecutar las pruebas sintéticas después de instalar el entorno con
`& $choquesPy -m choques validar`. Con los insumos locales se puede ejecutar
el flujo completo. La configuración por defecto es `config/proyecto.toml`.

```powershell
$choquesPy = "..\.venv\Scripts\python.exe"
& $choquesPy -m choques todo
& $choquesPy -m choques compilar
& $choquesPy reproducir.py
```

`todo` ejecuta descarga, preparación, validación, estimación, análisis y
gráficas. Cada nombre funciona como subcomando independiente. `soporte`
reconstruye las comparaciones auditadas y municipales, los pesos y los
descartes sin estimar. El catálogo CSV entregado es el insumo de `todo`. Se puede reconstruir desde las hojas
de evidencia mediante `python -m choques consolidar`.

## Comparaciones municipales

El subcomando `todo` descarga y verifica las fuentes, prepara las
covariables y los conteos, ejecuta las pruebas sintéticas y estima tanto
la referencia auditada como las comparaciones con controles municipales.
La [nota de resultados](reporte/comparaciones-municipales.md) reúne las
estimaciones, el balance, las falsificaciones y los límites de la rama
diaria. La reproducción del escrito sigue usando los insumos auditados.

`estimar` compara el matching uno a muchos (`emparejada`) con el vecino más
cercano por tratado (`emparejada_1a1`). Ambos usan los mismos tratados y
fechas dentro de cada diseño, principal o placebo. Filtra `reparto_controles.csv`
por `diseno` y `muestra` para consultar los pares y los pesos de cada método.
La columna `distancia_log2` registra la distancia del vecino elegido en 1:1.

La [revisión de controles](reporte/cotejo-controles.md) documenta la búsqueda
de exposiciones omitidas en las fechas de mayor peso. `estimar` reconstruye
ambos matchings con cobertura predicha, ventanas hasta el día 0 y las señales
del cotejo. `analizar` genera las tablas que `compilar` incorpora al PDF.

`preparar` construye el cruce de franja y gravedad desde los microdatos.
`estimar` publica las nueve celdas y el contraste noche menos día por
clase. Si el parquet de conteos es anterior al cruce, regénéralo con `preparar`.

Para trabajar en un worktree, usa una carpeta que contenga `repo/`,
`tasks/` y `data/` como hermanas. Copia de la entrega auditada las
entradas de `data/inputs/`, `tasks/` y los originales de `data/raw/`
con su manifiesto. Cada ejecución resuelve sus rutas desde la configuración
del checkout y escribe en su propio `data/`. Ejecuta `configuracion`
para consultar las rutas resueltas antes de correr el flujo.

`descargar --fuente municipios` verifica o recupera los 100 originales
municipales de [config/fuentes_municipales.json](config/fuentes_municipales.json).
El manifiesto registra las URL, la consulta exacta de cada entidad al SAIC,
los periodos, las fechas de consulta y publicación de las ediciones y los
SHA-256. Si una edición cambia en origen, la descarga requiere los
originales fijados. La reproducción limpia toma esos archivos de
`data/raw/municipios/` y reconstruye los productos en otra copia.

| Producto | Ruta desde `data/` |
| --- | --- |
| Población, economía, vehículos, denominadores y cambios territoriales | `processed/municipios/`, `outputs/modelos/tasas_saic.csv` y `tasas_vmrc.csv` |
| Cortes, faltantes, cobertura y soporte por tratado | `outputs/modelos/covariables_por_fecha.csv`, `cobertura_covariables.csv`, `descartes_municipales.csv` y `soporte_municipal.csv` |
| Muestras, pesos, balance y denominador censal alterno | `outputs/modelos/muestras_municipales.csv`, `reparto_controles.csv`, `pesos_por_fecha.csv`, `balance.csv` y `soporte_denominador_censal.csv` |
| Trayectoria, modelos ajustados, Wald, bases y tramos | `outputs/modelos/comparaciones_municipales.csv`, `modelos_m0_m3.csv`, `wald_previos.csv`, `wald_modelos.csv` y `tramos_y_base.csv` |
| Sensibilidades de selección y cotejo de controles | `outputs/modelos/sensibilidades_seleccion.csv`, `composicion_sensibilidades.csv` y `muestras_sensibilidades.csv` |
| Conciliación horaria, gravedad, historial y trayectoria visual | `processed/conteos_diarios.parquet`, `outputs/modelos/franjas_y_gravedad.csv`, `frecuencias_franjas_y_gravedad.csv`, `historial.csv` y `outputs/figuras/dinamica_municipal.{pdf,png}` |
| Nueve combinaciones de franja y gravedad y contraste noche menos día por clase | `outputs/modelos/franjas_x_gravedad.csv`, `frecuencias_franjas_x_gravedad.csv` y `outputs/tablas/contraste_nocturno_por_gravedad.tex` |

`reproducir.py` compara los productos por SHA-256 y el texto paginado del
PDF. La ejecución local confirma 73 pares tratados, 7 351 controles,
30 fechas y +0,237468 choques registrados en el día 0, con tolerancia
absoluta de 10⁻⁶. El archivo `data/outputs/qa/reproduccion.md` registra
los tiempos por etapa y el cotejo de productos. El commit auditado
`68c3457` permite reproducir la entrega original con los mismos insumos
auditados.

## Datos, cobertura y trazabilidad

El [ZIP oficial de ATUS](https://www.inegi.org.mx/contenidos/programas/accidentes/datosabiertos/conjunto_de_datos_atus_anual_csv.zip)
contiene los CSV 1997–2025, diccionario, claves y metadatos. La edición
incluye cifras definitivas de 2025 y el metadato modificado el 12 de noviembre
de 2026. Se conserva el archivo completo en `data/raw/`, junto con el
JSON oficial del catálogo municipal de Sinaloa. El manifiesto `data/raw/manifiesto.csv`
registra nombres, URL, fecha, tamaños y SHA-256. Conserve el manifiesto si
parte de una copia sin originales, para que la descarga compruebe la edición.
También puede bajar los archivos a mano con los nombres exactos del manifiesto
y validar sus huellas en PowerShell con `Get-FileHash -Algorithm SHA256`.
Si la liga ofrece una edición nueva, use la copia oficial entregada con este
proyecto. La descarga valida los ZIP y los hashes y reutiliza archivos íntegros.

`preparar` conserva año y renglón como identidad técnica de cada fila.
Los códigos reservados de municipio no entran en el marco diario. El
microdato no trae un identificador de accidente, por lo que los atributos
idénticos se conservan y su número se registra. Las cinco filas con fecha
inservible quedan en `data/interim/fecha_invalida.parquet`. El panel diario
distingue la existencia de registros, ceros bajo continuidad mensual y días
sin reporte verificable. La continuidad requiere registros válidos en el mes
en cuestión y en los tres previos. Los meses finales de 2018 se usan solo
para esa historia. La edición de INEGI retiró certificados cero de 2018–2024.
Los ceros inferidos representan el conteo publicado bajo esa regla de
cobertura. Una interrupción completa del reporte puede cambiar la elegibilidad.

La clase, las fechas y el ámbito de cada episodio se conservan en
`data/processed/exposiciones.parquet` y en `data/inputs/episodios.csv`.
La bitácora `tasks/busqueda-eventos/busqueda-eventos.md` enlaza consultas, fuentes, revisiones
cruzadas, decisiones e incertidumbres. Los casos de prensa no forman un censo.
La comparación semanal usa el perímetro histórico de Culiacán. Tras la entrada
en funciones de Eldorado el 1 de noviembre de 2024 se requiere cobertura para
sumar ambas claves. Los huecos posteriores tienen sentido territorial y
de reporte. Se evita en la comparación diaria el uso de las claves que
cambiaron de territorio en Sinaloa si la ventana alcanza esa fecha.

## Diseño y verificaciones

El diseño previo y las huellas congeladas están en `tasks/diseno-t05/`.
La bitácora en `tasks/revision-auditoria/` registra los cambios posteriores.
`estimar` comprueba la huella de revisión, incluidos panel, exposiciones y muestra.
`preparar` verifica el ZIP antes de usarlo y `consolidar` valida ambos catálogos antes de publicarlos.
La muestra común asigna un peso de uno a cada par tratado y peso total igual
a ambos grupos dentro de cada fecha. PyFixest estima los 16 horizontes
posteriores y 12 diagnósticos previos, con base en el día -2. La validación
sintética comprueba fechas, cobertura, uniones, exposiciones repetidas,
contaminación, casos nulos, reponderación y los errores agrupados.
Las ventanas originales se fijaron antes de observar efectos. Las bases `explora_base_media` y `explora_base_semana` son sensibilidades posteriores y conservan la muestra revisada.

`data/outputs/tablas/calidad.csv` concilia los totales antes y después de agregar.
`data/outputs/tablas/efectos.csv` registra estimaciones, errores, intervalos, tamaños
de muestra y MDE. El registro `data/outputs/qa/reproduccion.md` documenta el cotejo
desde una copia con datos y salidas separados, usando los originales validados por hash.
El plan en `tasks/plan-proyecto/` contiene decisiones y tiempos. El syllabus fija
el miércoles 2 de diciembre de 2026 y no especifica canal ni hora exacta.
La presentación corresponde a otra sesión.

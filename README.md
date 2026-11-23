# Narcoataques y siniestros viales registrados

## Reporte aprobado y compilación editorial

Se incorporaron las 21 propuestas aprobadas en Markdown. El cuerpo ocupa siete
páginas a 11 puntos; las referencias están en la página 8 y los apéndices en
las páginas 9–49. La selección de tratados y controles se identifica como
matching 1:muchos o 1:1. Las cifras de los modelos se conservan.

Para trasladar una nueva versión aprobada del Markdown a LaTeX, desde este
checkout:

```powershell
python reporte/convertir_markdown.py reporte/reporte.md reporte/main.tex ../tasks/revision-editorial/compilacion
python -m choques compilar
```

Estos comandos solo actualizan el escrito; no ejecutan estimaciones ni el
flujo completo. La compilación utiliza Biber y conserva idénticos `main.pdf`
y `reporte.pdf`. Las figuras locales están en `reporte/figuras/`.
`codigo_R/analisis.R`, ya incorporado a main, se conserva sin cambios.

El apéndice H (pp. 23–49) incorpora las 1 465 líneas de ese archivo R, con
números de línea. Una ejecución nueva desde el ZIP de datos limpios reprodujo
los 22 productos cotejados con tolerancia absoluta de 1e-6 y las 18 tablas a
la precisión impresa. El [registro del cotejo](reporte/verificacion/reproduccion-r.json)
incluye huellas del código, insumos y resultados Python de referencia.

El código está en este [repositorio](https://github.com/EduardoGC21/inferencia-causal).
La [carpeta de entrega de datos](https://drive.google.com/drive/folders/19fPf9UVt5Vdm-h2LiM2sBdD9erg0qItu?usp=sharing)
es el destino indicado para `datos_limpios_R.zip` y los demás datos del proyecto.
Tras descargar y descomprimir ese ZIP, instalar `data.table`, `R.utils` y
`ggplot2` y ejecutar desde la raíz del repositorio:

```powershell
Rscript --vanilla codigo_R/analisis.R RUTA/datos_limpios_R RUTA/resultados_R
```

R reconstruye el análisis desde datos limpios; la obtención y limpieza siguen
en Python. Las salidas históricas adicionales del archivo R, incluida la
comparación semanal de Culiacán, permanecen fuera de los resultados del reporte.

La [verificación editorial](reporte/verificacion/revision-editorial.json)
identifica el PDF final. Los manifiestos de reproducción analítica anteriores
conservan su alcance histórico; no certifican una nueva ejecución del flujo
completo para esta edición.

## Diseño final: Ruta B

La entrega final es [reporte/reporte.pdf](reporte/reporte.pdf), con [Markdown](reporte/reporte.md) y [LaTeX](reporte/main.tex). `reporte/main.pdf` conserva una copia idéntica del PDF. El diseño se aprobó
el 21 de noviembre de 2026 después de observar T05 y la auditoría. La rama
`diseno-causal-final` parte de `e283e2d76190b496644133c7e1e5c0b004a4e99f`,
que contiene `0335513`. T08 queda fuera del alcance.

El escrito identifica a Eduardo Garcia Cortez, clave única 207480, y al profesor
Mauricio Romero. La [verificación del syllabus](reporte/cumplimiento-syllabus.md)
localiza las cinco secciones obligatorias y sus evidencias: siete páginas de
cuerpo, una de referencias APA y 41 de apéndices (49 en total), con fuente de 11 puntos
en el cuerpo y de 9 puntos en el listado de código.
Los párrafos se alinean a la izquierda, sin justificación ni sangría inicial.
El apéndice incluye el mapa de municipios tratados y controles.
El reporte se concentra en jornadas extensas con inicio local definido.
La comparación semanal de la crisis prolongada de Culiacán se retiró del cuerpo
y del apéndice por su exposición distinta y problemas de cobertura. Su código
y sus fuentes se conservan. Esta edición no excluye municipios ni cambia las
estimaciones del análisis principal.
La sección Datos y el apéndice E identifican la búsqueda web asistida por tres
subagentes de IA que originó el catálogo de ataques, sus cotejos entre agentes
y sus límites. Esta procedencia corresponde al tratamiento; los accidentes
y las covariables provienen de fuentes oficiales. Las bitácoras no se presentan
como constancia de una validación humana exhaustiva.

La [matriz de auditoría y verificación](reporte/auditoria-final.md) vincula cada
requisito con su código, salidas y evidencia de cierre.

El contraste principal es el promedio diario **d0..1**, M0, matching 1:muchos,
en `log(1+Y)`. `Y` cuenta registros ATUS publicados con fecha válida: no mide
riesgo por viaje y puede cambiar por movilidad, riesgo o captación. Se reportan
también d0, d1, d2..6, wk0 y wk+1, niveles, matching 1:1 y M0–M3. La conclusión
se basa en los resultados regenerados, incluidos los diagnósticos desfavorables.

### Decisiones y diferencias respecto de T05

| Componente | T05 / referencia auditada | Diseño final |
| --- | --- | --- |
| Base | Día puntual -2 | Tres semanas del mismo día en [-28,-8] |
| Notación | b(t)=t-2 | q=h mod 7; r=t+q; fechas r-28, r-21, r-14 |
| Diagnóstico inmediato previo | -14..-3 | Semana -1 y días -7..-1, incluidos -2 y -5 |
| Calibre | Nivel medio de tratados de la fecha | Nivel propio de cada tratado, con offset 0.5 y razón [0.5,2] |
| Matching | Desde el pool ya restringido por la fecha | Desde el universo elegible, calibre individual y luego población, empleo/mil y autos/mil |
| Soporte | Diez controles de cinco estados por fecha | Diez candidatos de cinco estados por tratado; después se elige el vecino 1:1 |
| Elegibilidad principal | Continuidad hasta +15 y aislamiento hasta +16 | Tres meses completos anteriores al mes del inicio, exposición [-49,-1] y territorio hasta t-1 |
| Resultado principal | Niveles, día 0 | Promedio de dos días naturales en log(1+Y); niveles complementarios |
| Persistencia | Misma muestra seleccionada a futuro | Rama explícita con cobertura [-28,+13] y aislamiento hasta +14, comparada con la muestra previa |
| Inferencia | CRV1 estatal y doble; Wald de 12 previos | Ambas CRV1, CRV3 estatal, omisiones y Wald semanal de tres restricciones |
| Culiacán | Doce donantes, incluido 24028 | Donantes sin segregación M en la ventana; rama descriptiva |

Para h=1, la base es {-27,-20,-13}; para h=7 vuelve a {-28,-21,-14}.
La fórmula literal r=t+h sería incompatible con la ventana limpia para ciertos
horizontes. Se transforma cada observación antes de promediar. `100*expm1(beta)`
describe la escala geométrica de 1+Y, no directamente el cambio porcentual del
promedio aritmético de accidentes. Dos fechas naturales no equivalen a 48 horas
posteriores exactas si la jornada comienza por la tarde.

El indicador de continuidad mensual original se conserva. La rama final
construye por separado el conteo de filas publicadas; no usa `nan_to_num` sobre
faltantes del panel. Un cero se interpreta como cero registros de fecha válida
publicados dentro del universo previamente predicho. No demuestra ausencia de
accidentes ni continuidad de captación. Las cinco fechas inválidas y la
incertidumbre de su localización se documentan. Las covariables se miden antes
de t-28, usando ediciones retrospectivas; no se afirma disponer de todos sus
vintages en tiempo real.

M0 incluye tratamiento y fecha; M1 añade log población; M2, empleo/mil; M3,
autos/mil. La progresión conserva muestra y pesos. En M0 cada tratado pesa uno
y reparte su masa entre donantes; el ajuste por covariables puede modificar la
ponderación implícita del ATT. Ambos matchings comparten tratados y se permite
reutilizar controles. El CRV3 omite estados con pesos fijos y vuelve a absorber
las fechas; no rematchea ni renormaliza masas. La prueba semanal omite wk-2 y
contrasta wk-4, wk-3 y wk-1, verificando rango e indefinición.

### Calendario y sensibilidades

`config/calendario_escolar.csv` registra intervalos, tipos y fuentes oficiales.
Se distingue LFT federal de recesos de alumnos de educación básica; los fines
de semana contiguos al receso se extienden hasta el regreso. CTE y talleres se
identifican como tales. Las cinco fechas de auditoría (2019-12-31, 2023-01-05,
2023-04-09, 2024-01-07, 2025-04-23) no agotan los recesos y ninguna es por sí
misma un feriado laboral general LFT. En d0..1, el 31 de diciembre sí incluye
el feriado del 1 de enero. Se conserva la sensibilidad de cinco fechas y se
añaden LFT y unión LFT–SEP, filtrando cohortes por d0 o d1. El receso
extraordinario de 2020 no representa toda la educación remota como vacaciones.
No se cubren todos los ajustes estatales ni calendarios universitarios.

Las exclusiones de corroboración son Chilchota 16025 (2021-07-14) y Contepec
16017 (2025-04-23). Las señales son Centro 27004 (2025-04-01..02) y Coatzacoalcos
30039 (2022-08-20); su sensibilidad ex post usa [-49,+14] y reconstruye pesos.
Todas se muestran independientemente de significancia. También se conserva
b=-2 en la muestra final para aislar el cambio de base, y la referencia auditada
para identificar cambios de composición. El placebo desplaza el índice -28
días y reconstruye criterios y las tres fechas base para los seis horizontes.

San Fernando 28035 (2023-04-30), otro caso pendiente de la auditoría, entra al
ampliar la muestra. Se añade la exclusión de los cuatro casos señalados,
incluyendo Huaniqueo 16037 (2025-04-23), que sigue fuera por elegibilidad previa.

### Consecuencias empíricas reproducidas

La referencia auditada mantiene 73 tratados y +0.237468 en d0 con b=-2.
El diseño final usa 77 tratados, 3536 controles y 32 fechas: log d0..1=-0.107136,
IC doble [-0.195466,-0.018805]; niveles=-0.396551, IC doble [-0.864827,+0.071724].
La equivalencia geométrica de 1+Y es aproximadamente -10.2%; no es directamente
ese porcentaje de la media de Y. Morelia pasa de diez donantes antiguos a doce
donantes bajo el nuevo diseño y conserva doce al excluir las señales.

La narrativa de la auditoría sólo resiste parcialmente. El Wald semanal log
rechaza por estado (p=0.000220), aunque no en dos vías (p=0.109213); persiste la
caída en h=-2. La exclusión amplia LFT–SEP reduce a 25 tratados y su IC log
inmediato incluye cero. Hay indicios de semana +1 según inferencia y escenarios.
Por ello el informe no afirma una reducción causal incondicional ni disipación
completa desde el día 2. El placebo no reproduce la caída inmediata.
En sus tramos posteriores, CRV1 estatal sí rechaza d2..6 en ambas escalas y
wk0 en niveles; dos vías no rechaza. La tabla informa ambas inferencias: no se
describe el placebo como un cero uniforme en todos los horizontes.

### Ejecución y productos finales

Desde este worktree, con `data/` y `tasks/` como hermanas locales de `repo/`:

```powershell
$choquesPy = (Resolve-Path ../../../.venv/Scripts/python.exe).Path
& $choquesPy -m pip install -r requirements-lock.txt
& $choquesPy -m pip install -e .
& $choquesPy -m pip check
& $choquesPy -m unittest discover -s tests -p 'test_*.py'
& $choquesPy -m choques configuracion
& $choquesPy -m choques validar
& $choquesPy -m choques todo
& $choquesPy -m choques compilar
& $choquesPy reproducir.py
```

Se reutiliza `Proyecto/.venv`. Los originales y las hojas de evidencia fueron
copiados desde las carpetas canónicas y se verifican por SHA-256; las salidas
de este worktree son independientes. La copia limpia reconstruye inputs desde
las hojas y todas las ocho etapas con su propio código. El PDF debe ser binario
idéntico: una coincidencia de texto ya no permite omitir una diferencia SHA-256.
La validación es determinista; tiempos y rutas variables quedan en logs QA.

| Salidas bajo data/outputs/modelos/ | Contenido |
| --- | --- |
| `causal_efectos.csv` | Escenario, método, modelo, escala, base, horizonte, agrupación, IC, MDE, N y soporte |
| `causal_muestras.csv`, `causal_vinculos.csv` | Pertenencia, valores previos, pesos y contribuciones individuales |
| `causal_elegibilidad.csv`, `causal_descartes.csv` | Predicción de cobertura, exposición, territorio y filtros sucesivos |
| `causal_uniones.csv`, `causal_balance.csv` | Numeradores, denominadores, utilizabilidad y DME |
| `causal_fechas_base.csv` | Fechas exactas reales/placebo y las tres bases |
| `causal_wald_semanal.csv`, `causal_omision_estado.csv` | Rango, condicionamiento, restricciones y réplicas CRV3 |
| `causal_calendario.csv`, `causal_exclusiones_calendario.csv` | Días oficiales, fuentes y cohortes afectadas |
| `causal_morelia_donantes.csv`, `causal_cruce.csv` | Donantes antes/después y nueve celdas horarias con contraste pareado |
| `culiacan_descartes_territoriales.csv` | Exclusiones territoriales, incluido 24028 → 24059 el 2024-08-30 |

Las tablas `causal_*.tex`, cifras y `causal_dinamica.{pdf,png}` se generan con
`analizar` y `graficar`. Los productos sin prefijo `causal_` preservan la
referencia auditada diaria b=-2; Culiacán sí incorpora la corrección territorial.
`legacy_comparison` conserva deliberadamente el calibre anterior sólo para esa
referencia. Los hashes históricos de código no se reescriben: el manifiesto
histórico protege datos y T05, mientras la evidencia final identifica el código
nuevo. La muestra auditada sigue cotejándose contra su huella original.

T05 registraba 77 tratados/31 fechas; la revisión de inventario, 73/30. Que el
rediseño también dé 77 tratados no significa identidad de muestra. La comparación
reconstruye la referencia revisada identificada; sus dos archivos congelados
se conservan sin cambios. El profesor autorizó Python para este proyecto,
según confirmación del estudiante el 21 de noviembre de 2026.

## Documentación de la referencia auditada anterior

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

# Violencia criminal y accidentes registrados

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
PyFixest 0.70.0. Se compiló con MiKTeX-pdfTeX 4.18 (MiKTeX 24.1) y BibTeX.
Tener `pdflatex` y `bibtex` en el PATH. La verificación limpia también
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
| Conciliación horaria, gravedad, historial y trayectoria visual | `processed/conteos_diarios.parquet`, `outputs/modelos/franjas_y_gravedad.csv`, `frecuencias_franjas_y_gravedad.csv`, `historial.csv` y `outputs/figuras/dinamica_municipal.{pdf,png}` |

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

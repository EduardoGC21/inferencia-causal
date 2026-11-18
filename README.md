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
reconstruye la lista de comparaciones y descartes sin estimar. El catálogo
CSV entregado es el insumo de `todo`. Se puede reconstruir desde las hojas
de evidencia mediante `python -m choques consolidar`.

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

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
[programa de esta edición](codigo_R/analisis.R) también se puede extraer de los
adjuntos del PDF. La [carpeta de entrega](https://drive.google.com/drive/folders/19fPf9UVt5Vdm-h2LiM2sBdD9erg0qItu?usp=sharing)
contiene `datos_limpios_R.zip`. Extrae el archivo antes de ejecutar R.

~~~powershell
$env:PYTHONPATH = (Resolve-Path src).Path
$py = "../../.venv/Scripts/python.exe"
$data = "../../data"
$out = "$data/outputs/niveles-base-semanal/solo-base"
$cleanR = "$data/outputs/apendice-r-verificado/replica_limpia/datos_limpios_R"
& $py -m choques estimar --datos $data --resultados "$out/python" --arranque
Rscript --vanilla codigo_R/analisis.R $cleanR "$out/r" --arranque
& $py -m choques validar --datos $data --resultados "$out/python"
& $py -m choques estimar --datos $data --resultados "$out/python"
Rscript --vanilla codigo_R/analisis.R $cleanR "$out/r"
& $py -m choques cotejar-panel --referencia "$out/python/modelos" --replica-r "$out/r/modelos" --salida "$out/cotejo"
& $py -m choques analizar --datos $data --resultados "$out/python"
& $py -m choques graficar --datos $data --resultados "$out/python"
~~~

`--arranque` comprueba el rango con dos fechas reales, las masas por
par y bloque y el ajuste explícito con indicadores diarios. El cotejo
numérico exporta el detalle de Python y R y un resumen con huellas de cada
archivo cotejado. `--anterior` permite agregar el cotejo de muestra y
pesos contra los modelos anteriores. El [registro de verificación](reporte/verificacion/niveles-base-semanal.md)
identifica los insumos y las tolerancias utilizados.

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
`codigo_R/analisis.R`. El PDF adjunta ese mismo archivo para ejecutar la réplica.
La compilación produce copias idénticas en
`reporte/main.pdf` y `reporte/reporte.pdf`. La [presentación final](presentacion/index.html) y el
[guion](presentacion/guion.md) usan la misma especificación y notación.
Las [instrucciones de la presentación](presentacion/README.md) explican
cómo regenerar las figuras y su PDF. Los registros de verificaciones
previas corresponden a sus respectivas ediciones.

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
Se evita en la comparación diaria el uso de las claves que
cambiaron de territorio en Sinaloa si la ventana alcanza esa fecha.

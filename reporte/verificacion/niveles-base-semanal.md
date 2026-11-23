# Verificación del panel diario en niveles

Árbol de trabajo `worktrees/niveles-base-semanal`, rama
`codex/niveles-base-semanal`, base
`593f46ac3b25884de4e3c676491c04a70a791049`.

## Identificación y pesos

En el arranque, Python y R reconstruyeron una muestra de ocho pares en dos
fechas reales. La base contiene exactamente los días -28 a -8, con tres
observaciones de cada día de la semana. La fecha calendario se codifica
desde lunes, con valor cero. Cada bloque conserva el peso original del
par. El error máximo de masa en Python fue $4,44\times10^{-16}$.

El rango adicional de las columnas de día de la semana fue cero al
agregar en dos filas y seis al conservar los días. Los dos programas
cotejaron los siete coeficientes en el arranque, el de
Tratado × Después y los seis de día de la semana, contra mínimos
cuadrados ponderados con indicadores explícitos. La diferencia máxima
fue $3,95\times10^{-14}$ en Python y $1,07\times10^{-14}$ en R.

Para los días 0 y 1 del modelo principal, el panel tiene 83 099 filas.
La corrección de muestra finita usa 3 613 pares y el rango del contraste
entre bloques, que es 33 en $M_0$. Los efectos del día de la semana
provienen de la variación dentro de los bloques. Las puntuaciones de los
coeficientes del contraste se agregan por estado, fecha de inicio y su
intersección, con 31 grados de libertad en la inferencia principal. La
prueba semanal de Wald usa la misma base de 21 días. Contrasta las semanas
-4, -3 y -1 con el promedio de la base. La semana -2 queda implícita porque
las diferencias de las tres semanas de la base suman cero. Las 30
pruebas conjuntas conservan el estadístico $F$ y el valor $p$ de la
ejecución anterior, ya que las tres restricciones generan el mismo
espacio lineal.

## Concordancia de la réplica

El cotejo comprobó 180 908 filas de muestra por escenario y método,
184 743 vínculos, 319 662 filas de elegibilidad, 2 660 estimaciones, 41 coeficientes del cuadro de
progresión y sus muestras complementarias, 30 pruebas conjuntas de Wald,
90 contrastes semanales individuales y 48 contrastes de franja y gravedad.
También comprobó 14 784 réplicas por omisión de estados, 786 diagnósticos
del día de la semana y 1 470 fechas de referencia. Se usó una tolerancia
absoluta de $10^{-9}$. La mayor diferencia en las filas de efectos,
incluido el efecto mínimo detectable, fue $1,32\times10^{-12}$.
Las claves, la elegibilidad de los pares y los pesos de Python coincidieron
exactamente con los de la ejecución anterior.

El modelo principal estimó -0,347548 siniestros registrados por municipio
y día en los días 0 y 1. El error estándar agrupado por estado y fecha
de inicio fue 0,238603, el intervalo del 95 % fue [-0,834181; 0,139085] y
el valor $p$ bilateral fue 0,155282.

## Reproducción

Los comandos del [README](../../README.md) utilizan los datos limpios del
proyecto y generan salidas separadas para Python y R. Para comprobar
además la continuidad de la muestra y los pesos respecto de la ejecución anterior en niveles, añade este argumento al comando `cotejar-panel` desde el
árbol de trabajo:

~~~powershell
--anterior ../../data/outputs/niveles-base-semanal/python/modelos
~~~

Los cuatro archivos centrales de Python, `panel_diario.parquet`,
`conteos_diarios.parquet`, `exposiciones.parquet` y
`fecha_invalida.parquet`, coinciden por SHA-256 con la ejecución
anterior. R reconstruye los pares y sus pesos desde la extracción de
`datos_limpios_R.zip`. Los CSV detallados del cotejo quedan en
`../../data/outputs/niveles-base-semanal/solo-base/cotejo/`. El
[registro numérico](niveles-base-semanal.json) conserva los resultados
del cotejo y las huellas de los artefactos.

Los casos sintéticos de integración se ejecutaron mediante
`python -m choques validar`. La prueba de arranque del panel diario y
el cotejo entre lenguajes verifican la especificación vigente por sus
rutas de ejecución. Las salidas vigentes contienen una sola base y una sola escala del resultado.


## Reporte compilado

Se regeneraron las tablas y la trayectoria con la ejecución final. Sus
huellas coinciden con las de las salidas que alimentan el reporte.
Se renderizaron las 45 páginas del PDF a 100 puntos por pulgada y se
revisaron la trayectoria, los cuadros, la paginación y el listado. El
cuerpo ocupa siete páginas y las referencias empiezan en la octava.
La conversión comprobó la identidad del listado del apéndice H con las
1 354 líneas de `codigo_R/analisis.R`. `main.pdf` y `reporte.pdf`
son idénticos. La revisión de notación usa $Y_{i,d}$ para el conteo diario y
$\bar Y_{ith}$ para el promedio del tramo. La revisión visual confirmó
la notación en las páginas 3 y 4. Las salidas de la estimación
conservan sus huellas y la presentación final usa las mismas cifras.
[Verificación de la presentación](../../presentacion/verificacion/REVISION.md)

La figura 1a del reporte reutiliza las series de cambios diarios de la
diapositiva 7. La brecha entre tratados y controles coincide con los 21
coeficientes diarios de $M_0$ en la salida de Python para el emparejamiento
1:muchos. La diferencia absoluta máxima es de $8,20\times10^{-13}$.
La figura 1b presenta los coeficientes y sus intervalos puntuales. El
[generador de la figura 1a](../figuras/README.md#trayectoria-de-siniestros-registrados)
coteja las series y guarda el panel vectorial que compila el reporte.
Se revisaron las páginas 5 a 8 del PDF recompilado. Las dos figuras
quedaron en la página 6 y la compilación conservó el listado íntegro de R.

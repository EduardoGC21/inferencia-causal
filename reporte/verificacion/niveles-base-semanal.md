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
`datos_limpios_R.zip`. Los CSV del nuevo cotejo con la réplica completa en R quedan en
`../../data/outputs/niveles-base-semanal/solo-base/revision-escrito/cotejo/`. El
[registro numérico](niveles-base-semanal.json) conserva los resultados
del cotejo y las huellas de los artefactos.

Los casos sintéticos de integración se ejecutaron mediante
`python -m choques validar`. La prueba de arranque del panel diario y
el cotejo entre lenguajes verifican la especificación vigente por sus
rutas de ejecución. Las salidas vigentes contienen una sola base y una sola escala del resultado.

## Reporte compilado

El cuerpo ocupa las páginas 1 a 8. La página 9 contiene las referencias y las páginas 10 a 45 contienen los apéndices. Las 45 páginas se revisaron a partir de imágenes a 110 puntos por pulgada. Las secciones de método, resultados, trayectoria y conclusión conservan su continuidad. Los 17 cuadros se cotejaron con las salidas numéricas de la edición. Las dos copias del PDF son idénticas.

En las páginas 1, 5 y 8 coinciden la muestra, el horizonte, el signo, la unidad, el intervalo y el valor $p$ del contraste principal. Los conteos limpios y los pesos del emparejamiento reproducen las medias diarias. Entre la base y los días 0 y 1, la media pasó de 2,050093 a 1,655844 entre los tratados y de 2,094472 a 2,047772 entre los controles. La diferencia de esos cambios es -0,347548 siniestros registrados por municipio y día.

Las figuras 1a y 1b de la página 6 distinguen los 42 promedios diarios observados por grupo de los 21 cambios diarios respecto a la base. Se cotejaron los conteos con los 3 613 pares de la muestra principal. La discrepancia máxima para los promedios fue de $4,93\times10^{-13}$. La brecha entre los cambios de tratados y controles reproduce los 21 coeficientes diarios de $M_0$ con una discrepancia máxima de $8,20\times10^{-13}$. La figura 1c de la página 7 muestra las diferencias de cambios y sus intervalos puntuales por estado y fecha. [Fuentes de las figuras](../figuras/README.md)

| Apéndice y páginas | Comprobación |
| --- | --- |
| A, 10–12 | Los archivos de elegibilidad, vínculos y balance respaldan la selección de 108 a 84 y a 77 tratados. Los 77 pares de control del esquema 1:1 pertenecen a los 3 536 del 1:muchos. Se confirmó la presencia de diez controles de Jalisco el 10 de agosto de 2022. |
| B, 13 | Los seis errores estándar del cuadro B1 corresponden a la misma agrupación doble que sus intervalos. El placebo reconstruye 81 pares tratados en 38 fechas. |
| C, 14–15 | Se cotejaron las nueve muestras por escenario, los dos conjuntos de exclusiones de casos pendientes y las 32 fechas del calendario. |
| D, 16–17 | El ajuste usa 83 099 filas diarias. La corrección del contraste principal usa 3 613 pares y 31 grados de libertad. La prueba semanal da $p=0{,}035$ por estado y $p=0{,}081$ por estado y fecha. |
| E, 18 | Los archivos de documentación del paquete contienen las fuentes de los episodios y las noticias vinculadas a los tratados. La construcción del catálogo distingue los casos pendientes de corroboración. |
| F, 19 | El mapa y el archivo de municipios identifican 54 tratados, 765 controles y 47 municipios en ambos grupos en fechas distintas. |
| G, 20 | Se cotejaron los seis contrastes de noche menos día por gravedad. Todos los intervalos del 95 % incluyen cero. |
| H, 21–45 | Las 1 353 líneas numeradas corresponden a la fuente de R. El PDF adjunta una copia exacta de ese programa. La instrucción de ejecución se puede copiar del PDF y el enlace dirige a la carpeta de datos. |

El ZIP de Drive y la copia local tienen la misma huella SHA-256. Sus 17 archivos coinciden con la extracción utilizada en la réplica. El registro numérico conserva la huella del ZIP, la del programa adjunto y las de los resultados cotejados. [Registro numérico](niveles-base-semanal.json)

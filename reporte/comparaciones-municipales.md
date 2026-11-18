# Comparaciones municipales y diagnósticos de la rama diaria

El contraste del día 0 es **+0,237** choques registrados por municipio en la
muestra auditada, **+0,289** en el matching uno a muchos, **+0,390** en el 1:1
y **+0,064** al ajustar por las tres covariables en una muestra común. Los
IC del 95 % incluyen cero. Persisten diferencias previas y el signo del
día 0 cambia con la base previa promedio. Los resultados describen cambios
en el registro de choques en jornadas documentadas con soporte.

## Matching y soporte

Los candidatos provienen de los filtros auditados de cobertura, lavado,
exposición, geografía y nivel de choques previos. Por tratado se exige que
cada covariable esté entre la mitad y el doble de su valor, con extremos
incluidos. Un cero explícito se compara con cero. El tratado debe conservar
al menos 10 controles de cinco estados. Cada tratado reparte peso uno entre
sus controles y los pesos de un control compartido se suman por fecha.

La sensibilidad 1:1 usa el mismo conjunto de candidatos de cada tratado con
soporte y elige el de menor distancia euclidiana en los logaritmos base 2 de
las razones control/tratado para población, empleo y autos. Las tres
variables pesan igual y dos ceros confirmados aportan distancia cero. En
empates se elige la menor clave municipal. Cada vínculo 1:1 aporta peso uno
y el mismo municipio puede ser el vecino más cercano de varios tratados.
Sus aportes se suman en una fila por municipio y fecha. El mínimo de
soporte se aplica antes de elegir al vecino. En el diseño principal y en
el placebo se conservan los mismos tratados y fechas que en uno a muchos.

| Comparación | Tratados | Controles | Fechas | Día 0 | IC 95 % por entidad | IC 95 % por entidad y fecha |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| Auditada completa | 73 | 7 351 | 30 | +0,237 | [−0,211, +0,686] | [−0,406, +0,881] |
| Mismos tratados, controles auditados | 59 | 7 281 | 28 | +0,261 | [−0,179, +0,701] | [−0,518, +1,041] |
| Mismos tratados, controles completos | 59 | 7 153 | 28 | +0,259 | [−0,180, +0,699] | [−0,522, +1,041] |
| Matching uno a muchos | 59 | 2 203 | 28 | +0,289 | [−0,155, +0,733] | [−0,481, +1,059] |
| Matching 1:1 | 59 | 57 | 28 | +0,390 | [−0,195, +0,975] | [−0,457, +1,237] |

El emparejamiento retiene 27 de 29 episodios y 11 de 14 estados tratados.
En 1:1 los 59 vínculos usan 57 observaciones municipio–fecha de 49
municipios de control. Dos observaciones se comparten entre tratados. El
número de entidades en la estimación pasa de 32 con uno a muchos a 25 con
1:1. La máxima repetición de un municipio de control en distintas fechas
es 21 en la auditada, 15 en uno a
muchos y tres en 1:1. El primer filtro que deja a un tratado sin el mínimo de
controles o entidades es población en ocho casos, autos en tres y empleo
en dos. En el caso restante faltan covariables del tratado. Al fijar los mismos 59 tratados, el contraste cambia en +0,028
respecto de sus controles auditados. La amplitud del IC por entidad pasa de
0,880 a 0,888 y la del IC doble de 1,559 a 1,541. El IC doble de la muestra
auditada completa mide 1,288. Frente a uno a muchos, el 1:1 mueve el contraste
del día 0 en +0,101 y amplía el IC por entidad a 1,169 y el doble a 1,694.

La diferencia de medias estandarizada usa una escala fija, la raíz del
promedio de las varianzas ponderadas de ambos grupos en la referencia
auditada. Los valores positivos indican una media mayor en tratados.

| Covariable | Auditada completa | Mismos tratados y controles completos | Uno a muchos | 1:1 |
| --- | ---: | ---: | ---: | ---: |
| Población | +0,238 | +0,152 | +0,028 | +0,030 |
| Ocupados por mil | −0,047 | +0,027 | +0,059 | +0,045 |
| Autos particulares por mil | −0,395 | −0,387 | −0,177 | −0,008 |
| Nivel de choques previos | +0,057 | +0,097 | +0,032 | +0,015 |
| Viviendas con automóvil | +0,288 | +0,216 | +0,324 | +0,376 |
| Valor agregado por habitante | −0,178 | −0,128 | −0,102 | +0,009 |

La población, la motorización y los choques previos quedan más balanceados
con uno a muchos frente a sus controles completos, y aumenta la diferencia
en empleo. El 1:1 reduce más las diferencias en motorización, empleo,
choques previos y valor agregado frente a uno a muchos. La población queda
prácticamente igual de balanceada y aumenta la diferencia en viviendas con
automóvil. Usar el último censo anterior al cierre del numerador
retiene 59 tratados y 2 189 controles emparejados. En placebo se pasa de
70 tratados y 2 625 controles con CONAPO a 69 tratados y 2 590 controles con el
denominador censal. El desfase del censo se registra en días por numerador.

## Regresión sobre una muestra común

M0–M3 usan 72 tratados, 7 223 controles, 30 fechas y los mismos pesos.
La variable dependiente es el cambio desde −2. Las regresiones incluyen
efectos fijos de fecha índice y añaden en orden logaritmo de la población,
personal ocupado por mil habitantes y autos particulares por mil.

| Modelo | Día 0 e IC por entidad | Día 7 e IC por entidad | Día 15 e IC por entidad |
| --- | --- | --- | --- |
| M0 | +0,141 [−0,308, +0,590] | +0,498 [+0,220, +0,776] | +0,661 [+0,283, +1,039] |
| M1 | +0,058 [−0,309, +0,426] | +0,421 [+0,177, +0,666] | +0,510 [+0,131, +0,889] |
| M2 | +0,070 [−0,292, +0,432] | +0,425 [+0,174, +0,676] | +0,500 [+0,129, +0,870] |
| M3 | +0,064 [−0,334, +0,463] | +0,409 [+0,152, +0,665] | +0,525 [+0,151, +0,899] |

En M3 el IC doble del día 0 va de −0,543 a +0,672. La prueba conjunta de las
tres covariables en el día 0 da F(3, 31) = 1,772 y p = 0,173 por entidad.
Por entidad y fecha da F(3, 29) = 1,411 y p = 0,259. Los p por entidad para
el bloque añadido a M1, M2 y M3 son 0,272, 0,412 y 0,886. Se usa CRV1 con
la corrección `(N−1)/(N−K) × G/(G−1)`, donde K suma las fechas y los
coeficientes identificados y G es el número de entidades o el mínimo entre
entidades y fechas en la sensibilidad de dos vías. Los grados de libertad
del denominador son G−1. Para los doce diagnósticos previos se usa su
covarianza compartida. La prueba conjunta de previos da p < 0,001 con ambas
agrupaciones en la auditada, uno a muchos y M3. En 1:1, la agrupación por
entidad da F(12, 24) = 5,873 y p = 0,000118. La matriz de covarianza de dos
vías es indefinida para esta prueba conjunta en el diseño principal y el
placebo.

El placebo se reconstruye 28 días antes del inicio real con la ventana
completa libre de exposición. Se vuelven a resolver cortes, soporte y pesos.
Los 70 tratados y 36 fechas se conservan en ambos matchings. Uno a muchos
usa 2 625 observaciones de control y 1:1 usa 68. En el día 7 placebo, uno a
muchos da +0,454 con IC por entidad [+0,189, +0,719] e IC doble [+0,049,
+0,859]. El 1:1 da +0,414 con IC por entidad [−0,702, +1,530] e IC doble
[−0,589, +1,417]. M3 en su muestra común placebo da +0,212 con IC por
entidad [−0,081, +0,505]. Estos contrastes y los previos limitan una lectura
causal.

## Tramos, horarios, gravedad e historial

| Muestra y base | Días 1–7 e IC por entidad | Días 8–15 e IC por entidad |
| --- | --- | --- |
| Auditada, −2 | +0,375 [+0,128, +0,622] | +0,495 [+0,205, +0,786] |
| Uno a muchos, −2 | +0,551 [+0,317, +0,785] | +0,608 [+0,342, +0,875] |
| 1:1, −2 | +0,298 [−0,308, +0,904] | +0,290 [−0,190, +0,771] |
| Auditada, promedio de −14 a −2 | −0,068 [−0,273, +0,138] | +0,053 [−0,114, +0,220] |
| Uno a muchos, promedio de −14 a −2 | +0,037 [−0,191, +0,265] | +0,094 [−0,073, +0,261] |
| 1:1, promedio de −14 a −2 | −0,105 [−0,469, +0,259] | −0,113 [−0,463, +0,237] |

El día 0 con la base promedio es −0,205 [−0,626, +0,215] en la auditada y
−0,225 [−0,702, +0,252] con uno a muchos. En 1:1 es −0,013 [−0,694, +0,668].
Los tramos ponderan por igual sus días dentro de cada par. La figura
`dinamica_municipal` compara la trayectoria de los mismos 59 tratados con
los controles auditados y ambos matchings, con IC puntuales por día. El día
−1 se reserva por anticipación.

El contraste pareado noche menos día de la primera semana con base −2 es
+0,013 [−0,161, +0,187] en la auditada, +0,101 [−0,048, +0,250] con uno a
muchos y −0,225 [−0,650, +0,200] con 1:1. La comparación horaria empieza
en el día 1 porque el catálogo carece de una hora de inicio sistemática.
Día abarca de 06:00 a 17:59 y noche
las horas restantes de la fecha civil. En base −2 y ambos tramos los dos
grupos suman cero choques de hora desconocida. Los 1 208 choques observados
en tratados auditados durante la primera semana incluyen 17 fatales, 289
con heridos y 902 de sólo daños. Los conteos de clase conservan los ceros
con cobertura. Los intervalos por gravedad son exploratorios y las
frecuencias de fatales son bajas.

Con una ventana de 365 días, 10 pares tienen antecedente confirmado en el
catálogo, 61 carecen de antecedente documentado y dos tienen ventana
incompleta. Los dos grupos con historial evaluable sólo comparten tres
fechas. Las brechas se presentan de forma descriptiva. El catálogo comienza
en 2019 y su cobertura es desigual.

## Cobertura y límites de las fuentes

| Fuente utilizada | Corte de referencia | Publicación o edición fijada |
| --- | --- | --- |
| Encuesta Intercensal 2015 | 15 de marzo de 2015 | 8 de diciembre de 2015, tabulados actualizados el 24 de octubre de 2016 |
| ITER 2020 | 15 de marzo de 2020 | 25 de enero de 2021, archivo corregido en 2021 |
| Censos Económicos, SAIC histórico | Años de actividad 2018 y 2023 | Definitivos del 16 de julio de 2020 y del 24 de julio de 2025 |
| VMRC definitivo | Cierre anual 2018–2024 | Paquete histórico modificado el 27 de agosto de 2026 |
| CONAPO, población municipal | 1 de julio de cada año | Edición 2024 con mapa de 2022. Reconstrucción hasta 2020, proyección a partir de 2021 |

Se aplica el último corte cuyo periodo de referencia terminó estrictamente
antes de la fecha índice menos 28 días. Esto permite usar una medición
anterior al episodio publicada más tarde. La Intercensal 2025 y cualquier
interpolación con un extremo posterior quedan fuera de las estimaciones.
El total municipal de H001A usa la cobertura del SAIC histórico en ambos
cortes. La captación de algunas actividades rurales es muestral y la
cobertura de Chiapas es parcial en algunos municipios. El numerador mide
ocupación en el lugar del establecimiento. El VACB por habitante se
expresa en pesos de 2023 con el inflactor SAIC de 1,26412683998505 para
2018. Vivienda es un diagnóstico de acceso al automóvil o camioneta según
la pregunta de cada censo. El padrón VMRC refleja el lugar de registro.

En la muestra principal, se unen 7 321 de 7 351 filas de control con
población censal, 7 297 con SAIC y 7 277 con VMRC. Se usan 7 321, 7 279 y
7 259, respectivamente, tras considerar los denominadores y la fecha
efectiva. En tratados se usan 72 de 73 para cada fuente. La equivalencia municipal
distingue altas por segregación y cambios de nombre. Se excluyen cruces de
perímetros incompatibles y celdas sin población comparable, incluso si
la clave coincide. El corte de VMRC de Colima rotulado 2023 se midió en
abril de 2024. Su denominador corresponde a 2024 y la tasa se excluye
si la medición o la mitad de ese año rebasan el umbral temporal. Cuando
el tabulado contiene al municipio de origen de una segregación pero
falta el municipio nuevo, el perímetro queda sin confirmar. Esta regla
afecta 26 filas de control y una tratada de VMRC en la muestra principal.

El VMRC contiene las 16 alcaldías de Ciudad de México en los siete años.
Entre 2021 y 2022 los autos particulares registrados suben 21,3 % en
Tamaulipas y 14,9 % en Baja California. El INEGI registra la regularización
de autos importados desde 2022, cambios de cobertura municipal y un ajuste
de servicio en Morelos en 2024. Las series de población y padrón afectan el
soporte sin medir movilidad. Los cambios en los conteos ATUS pueden
reflejar cantidad de viajes, riesgo por viaje, desvíos o captación. La
comparación también depende de la cobertura y el aislamiento posteriores
al episodio. La inferencia permanece sensible a la base y a los
conglomerados disponibles.

## Sensibilidad a la selección y al cotejo de controles

Se reconstruyen elegibilidad y pesos con los cortes municipales vigentes.
La cobertura predicha requiere al menos una fila fechable de ATUS en cada
uno de los tres meses completos anteriores al mes en que comienza la
ventana de medición. Una anomalía de fecha en el periodo de medición conserva
la exclusión. Para las observaciones así admitidas, cero significa que no
se publicó una fila ese día. El corte al inicio acorta tanto la ventana de
cobertura como la de aislamiento al día 0. Se conserva la base −2 y se
estima únicamente ese horizonte porque puede haber exposiciones posteriores.

| Escenario | Tratados | Fechas | Uno a muchos, día 0 e IC por entidad | 1:1, día 0 e IC por entidad |
| --- | ---: | ---: | --- | --- |
| Referencia | 59 | 28 | +0,289 [−0,155, +0,733] | +0,390 [−0,195, +0,975] |
| Cobertura predicha | 61 | 29 | +0,251 [−0,213, +0,715] | +0,410 [−0,154, +0,974] |
| Ventana hasta día 0 | 66 | 31 | +0,397 [−0,077, +0,871] | +0,561 [−0,262, +1,383] |
| Ventana hasta día 0 y cobertura predicha | 67 | 32 | +0,390 [−0,077, +0,858] | +0,552 [−0,262, +1,366] |
| Excluir señales del cotejo | 58 | 28 | +0,003 [−0,264, +0,271] | +0,052 [−0,575, +0,678] |

Los cambios de cobertura y ventana incorporan tratados. Al excluir
dos señales del cotejo baja el contraste en ambos matchings y sale
Morelia por pérdida de soporte. El escenario cambia tanto la composición
de tratados como los comparadores. Todos los intervalos del cuadro abarcan
cero. La revisión de 27 pares de control y el alcance de ACLED se detallan
en el [cotejo](cotejo-controles.md). Los resultados con base promedio y
agrupación doble se guardan en `sensibilidades_seleccion.csv`.

## Reproducción verificada

Python 3.13.2 en Windows x64. La descarga limpia recuperó 100 originales
municipales (258,3 MB) y verificó sus SHA-256 en 128,52 s. Con las nuevas
sensibilidades, `python -m choques estimar` tardó 140,73 s en el worktree.
`python reproducir.py` cotejó 73 productos por SHA-256 y el PDF binario
en una copia limpia. El escrito contiene siete páginas de texto y
referencias más seis de apéndice. El commit auditado por separado cotejó
36 productos y el PDF. El contraste auditado regenerado es +0,237468052.
Se comprobaron por separado los 129 vecinos elegidos en principal y placebo,
la igualdad de tratados y de las sumas de pesos por fecha y la coincidencia
de las filas preexistentes en las tablas ampliadas.

| Etapa de la copia limpia | Segundos |
| --- | ---: |
| Descargar (verificar originales locales) | 3,23 |
| Consolidar | 2,59 |
| Preparar | 10 506,72 |
| Validar | 11,26 |
| Estimar | 126,56 |
| Analizar | 3,96 |
| Graficar | 6,07 |
| Compilar | 6,39 |

El tiempo de pared de preparación coincide con un salto en el reloj de
la sesión. Se conserva en el registro de reproducción y queda fuera de
la comparación de rendimiento. La reproducción anterior midió 100,54 s
en esa etapa, con los mismos insumos y código de preparación.

Fuentes oficiales. [EIC 2015](https://www.inegi.org.mx/programas/intercensal/2015/default.html)
· [ITER 2020](https://www.inegi.org.mx/app/descarga/ficha.html?ag=0&f=csv&tit=326108)
· [Metodología del SAIC](https://www.inegi.org.mx/contenidos/app/saic/saic_historico_metodologico_ce2024.pdf)
· [INEGI VMRC](https://www.inegi.org.mx/programas/vehiculosmotor/)
· [CONAPO](https://www.gob.mx/conapo/documentos/reconstruccion-y-proyecciones-de-la-poblacion-de-los-municipios-de-mexico-1990-2040)
· [Equivalencias municipales](https://www.inegi.org.mx/app/ageeml/)

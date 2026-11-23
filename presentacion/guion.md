# Guion de exposición

**Narcoataques y siniestros viales registrados**

Eduardo Garcia Cortez · CU: 207480 · Inferencia Causal · ITAM

Ruta principal de **480 segundos (8:00)**. Los tiempos incluyen las transiciones. Para ensayar, lee la explicación oral y la transición. Las referencias y los respaldos quedan fuera del tiempo.

## ¿Cómo cambian los siniestros viales registrados tras el inicio de narcoataques?

**Identificador** `pregunta` · **Tiempo** 0:00–0:20 (20 s)

**Explicación oral**

¿Cómo cambian los siniestros viales registrados tras el inicio de narcoataques? El artículo de Bauernschuster y Rekers inspira el seguimiento diario después de un evento. Aquí observo las dos semanas desde el inicio.

**Transición**

Primero, ¿por qué esperaríamos un cambio?

**Referencia para consulta.** Reporte, §1 y §5. Bauernschuster y Rekers (2022).

## Por qué podrían cambiar los siniestros viales registrados

**Identificador** `contexto` · **Tiempo** 0:20–0:50 (30 s)

**Explicación oral**

Los bloqueos, los desvíos y los cambios al conducir pueden afectar los siniestros. En este estudio, un narcoataque reúne acciones coordinadas en al menos tres lugares en 24 horas, con afectación del espacio público, los comercios o el transporte. Tres agentes de inteligencia artificial recopilaron prensa y comunicados. Se buscaron fuentes independientes para corroborar fecha y municipio. La cobertura es desigual y no hubo validación humana exhaustiva.

**Transición**

El mapa ubica los municipios que entraron a la muestra.

**Referencia para consulta.** Reporte, §2 para la definición y apéndice E para la búsqueda web, la corroboración entre fuentes y los casos pendientes.

## La muestra reúne 77 pares tratados

**Identificador** `datos` · **Tiempo** 0:50–1:40 (50 s)

**Explicación oral**

Los mapas cuentan municipios únicos. En el análisis, la unidad es el par municipio–episodio. Un municipio reaparece si participa en otra fecha. Hay 31 episodios y 32 fechas porque un mismo episodio puede empezar en fechas distintas según el municipio. El tratamiento marca el inicio local, aunque la violencia continúe después. Los siniestros y las covariables provienen de fuentes oficiales. ATUS es la Estadística de Accidentes de Tránsito Terrestre en Zonas Urbanas y Suburbanas del Instituto Nacional de Estadística y Geografía, INEGI. Un cero indica cero registros publicados con fecha válida. El conteo tampoco mide el riesgo por viaje.

**Transición**

Con esta unidad, podemos buscar municipios comparables para cada inicio.

**Referencia para consulta.** Reporte, §2 y apéndices A, E y F. Los 3 613 pares son 77 tratados y 3 536 controles.

## Cómo elegimos los controles para comparar cambios

**Identificador** `matching` · **Tiempo** 1:40–2:30 (50 s)

**Explicación oral**

El contrafactual es cómo habría cambiado el resultado del tratado sin el ataque. Para aproximarlo, busco controles en estados ajenos al episodio. Exijo cobertura en tres meses completos previos, estabilidad territorial y ausencia de exposición documentada desde el Día menos 49. Aplico márgenes de la mitad al doble en accidentes previos, población, empleo y autos. El mínimo es de diez candidatos de al menos cinco estados. Uno a muchos usa todos los elegibles y reparte el peso. Uno a uno elige al más cercano por población, empleo y autos. Después, diferencias en diferencias compara los cambios en las mismas fechas. Queremos estimar el efecto promedio de los pares tratados incluidos, con igual peso por par.

**Transición**

Todos los tramos usan la misma base previa.

**Referencia para consulta.** Reporte, §3 y apéndice A. Covariables disponibles con medición anterior a t−28.

## La base reúne 21 días, del −28 al −8

**Identificador** `base` · **Tiempo** 2:30–3:20 (50 s)

**Explicación oral**

La base de cada par es el promedio de los 21 conteos de las semanas menos cuatro, menos tres y menos dos. Incluye tres lunes, tres martes y lo mismo para cada día de la semana. Para el inicio del jueves 17 de octubre de 2019 en Culiacán, abarca del 19 de septiembre al 9 de octubre. La semana menos uno sirve para detectar diferencias previas. Para cada tramo posterior, el resultado es el promedio de sus días. El día cero puede incluir horas anteriores al inicio local.

**Transición**

El ajuste conserva una observación por día en cada bloque.

**Referencia para consulta.** Reporte, §3. La base de comparación y el promedio de cada tramo están en siniestros registrados por municipio y día.

## Las filas diarias permiten ajustar por día de la semana

**Identificador** `regresion` · **Tiempo** 3:20–4:10 (50 s)

**Explicación oral**

Después indica el bloque que analizo, incluso si es un diagnóstico previo. El ajuste compara los cambios de tratados y controles con el mismo inicio. Cada bloque recibe el mismo peso por par, aunque tenga distinta duración. Uso el día de la semana de cada fecha del conteo, con lunes como referencia. Con dos filas agregadas, los efectos de inicio por bloque absorben esa información. Las filas diarias identifican los seis efectos. En el modelo principal los 77 tratados pesan igual. Los demás modelos ajustan por población, empleo y autos.

**Transición**

Veamos los conteos que dan origen a esa comparación.

**Referencia para consulta.** Reporte, §3 y apéndice D. El ajuste absorbe efectos de par y de inicio por bloque. Los seis efectos de día de la semana se identifican por la variación dentro de cada bloque.

## Cada grupo se compara con su propia base

**Identificador** `eventos` · **Tiempo** 4:10–5:10 (60 s)

**Explicación oral**

A la izquierda están los conteos medios en niveles. Alineo cada serie en el inicio local. Los tratados pesan lo mismo y los controles conservan los pesos del emparejamiento. El fondo sombreado marca los 21 días de la base. A la derecha, resto el promedio de esos días a cada par y después promedio los cambios dentro de cada grupo. El cero indica igualdad con la base propia. En el día menos dos los grupos ya muestran cambios distintos. Su distancia vertical reproduce el coeficiente diario del modelo principal: el ajuste de día de la semana es común dentro de cada fecha de inicio y se cancela al comparar los grupos.

**Transición**

Ahora veamos esa distancia y sus intervalos de confianza.

**Referencia para consulta.** Muestra principal 1:muchos. El cotejo verifica los 21 contrastes diarios de M₀ contra la diferencia entre cambios ponderados.

## Los grupos ya difieren antes del inicio

**Identificador** `trayectoria` · **Tiempo** 5:10–5:55 (45 s)

**Explicación oral**

Cada punto compara el cambio de tratados y controles. En los días menos tres y menos dos, los intervalos puntuales quedan por debajo de cero. La prueba conjunta compara las semanas menos cuatro, menos tres y menos uno con la base común. Las tres semanas de la base suman cero frente a su promedio, así que la semana menos dos queda implícita. Se rechaza al cinco por ciento con agrupación estatal. Con la agrupación por estado y fecha, el valor p es 0,081. Las diferencias previas limitan cuánto podemos atribuir al inicio del ataque.

**Transición**

Con esa cautela, veamos el resultado inicial y cuánto cambia con el ajuste.

**Referencia para consulta.** Reporte, §3–4, figura 1 y apéndice D. La gráfica usa el modelo M₀, emparejamiento 1:muchos y base de 21 días. La prueba semanal compara tres semanas con la base de 21 días.

## Añadir covariables cambia poco la estimación inicial

**Identificador** `resultados` · **Tiempo** 5:55–6:30 (35 s)

**Explicación oral**

El modelo inicial estima 0,348 siniestros registrados menos por municipio y día en los días cero y uno. El intervalo agrupado por estado y fecha incluye cero. Al añadir logaritmo de población, empleo y autos por mil habitantes, la estimación cambia poco. Los cuatro modelos usan los mismos pares, pesos y efectos fijos.

**Transición**

Veamos qué se estima en los tramos posteriores.

**Referencia para consulta.** Reporte, cuadro 2 y apéndices A y B. Los cuatro modelos usan 3 613 pares: 77 tratados y 3 536 de control.

## La caída estimada es mayor en los días 0 y 1

**Identificador** `duracion` · **Tiempo** 6:30–7:10 (40 s)

**Explicación oral**

Cada punto resume un tramo. Se estiman menos 0,348 en los dos primeros días, menos 0,145 en los días dos a seis y menos 0,079 en la segunda semana, en siniestros registrados por municipio y día. Los tres intervalos incluyen cero. Los posteriores admiten caídas de magnitud relevante. La muestra que exige continuidad del reporte y aislamiento posterior cambia los pares disponibles. Con estos datos la duración sigue abierta.

**Transición**

Veamos la sensibilidad al calendario y al inicio ficticio.

**Referencia para consulta.** Modelo M₀, 1:muchos. Reporte, §4, cuadros B1–B2 y apéndice D. Se permite que el episodio inicial continúe.

## Sensibilidad del resultado

**Identificador** `sensibilidades` · **Tiempo** 7:10–7:40 (30 s)

**Explicación oral**

Excluir feriados y recesos deja 25 tratados. El placebo ubica el inicio 28 días antes, reconstruye los pares y estima una caída menor. Los tres intervalos incluyen cero. Cada comparación usa la misma regla de base, los días menos veintiocho a menos ocho respecto a su inicio.

**Transición**

¿Qué se puede sostener con ese conjunto de resultados?

**Referencia para consulta.** Reporte, cuadros B2–B3 y C1–C3. Siniestros registrados por municipio y día. Intervalos agrupados por estado y fecha. La sensibilidad amplia usa feriados laborales y recesos de educación básica.

## La mayor caída estimada aparece al inicio

**Identificador** `conclusion` · **Tiempo** 7:40–8:00 (20 s)

**Explicación oral**

La mayor caída estimada aparece en los días cero y uno. El intervalo incluye cero. La duración sigue abierta y las diferencias previas limitan cuánto podemos atribuir al ataque.

**Transición**

Aquí termina la exposición. Las referencias y los respaldos quedan para consulta.

**Referencia para consulta.** Reporte, cuadro 2, §5 y apéndices E–G. El coeficiente mide la diferencia de cambios en siniestros registrados por municipio y día.

## Referencias

**Identificador** `referencias` · **Tiempo** Fuera de la ruta cronometrada

**Explicación oral**

Las referencias quedan disponibles para consulta.

**Transición**

Pasar al índice de respaldos si hay preguntas.

**Referencia para consulta.** Reporte, referencias y apéndices E y F.

# Respaldos

## Respaldos para la discusión

**Identificador** `respaldos` · **Tiempo** Fuera de la ruta cronometrada

**Explicación oral**

Abre la pregunta correspondiente. Cada respaldo termina con un enlace al índice.

**Transición**

Volver a la conclusión cuando termine la discusión.

**Referencia para consulta.** Reporte, apéndices A–H.

## Soporte, balance y pesos

**Identificador** `soporte` · **Tiempo** Fuera de la ruta cronometrada

**Explicación oral**

El filtro de comparabilidad usa la media de los días menos 28 a menos 15. Su razón usa un desplazamiento de 0,5 en numerador y denominador. Las tres covariables cumplen por separado el margen. En uno a muchos, si un control se reutiliza en una fecha, se suman sus aportes; un tratado con cuarenta controles reparte una unidad en cuarenta partes. En uno a uno se elige el vecino por población, empleo y autos. La cobertura previa predice el universo, y los cambios posteriores de captación pueden afectar el resultado. El comparador observado requiere además ausencia de contagio y cambios paralelos.

**Transición**

Volver al índice de respaldos.

**Referencia para consulta.** Reporte, cuadro 1, §3 y apéndices A y D.

## La agrupación permite errores dependientes

**Identificador** `inferencia` · **Tiempo** Fuera de la ruta cronometrada

**Explicación oral**

Se suma la covarianza por estado y por fecha y se resta la de su intersección. En los días cero y uno el panel tiene 83 099 filas. La corrección de muestra finita cuenta 3 613 pares y el rango del contraste entre bloques. Las desviaciones diarias dentro de cada bloque se cancelan al sumar las contribuciones a la varianza del contraste. La inferencia principal tiene 31 grados de libertad. El intervalo alternativo omite un estado por turno. Con la agrupación por estado y fecha, el efecto mínimo detectable del contraste inmediato es 0,690 siniestros registrados por municipio y día.

**Transición**

Volver al índice de respaldos.

**Referencia para consulta.** Reporte, §3.1, §4 y apéndice D. El efecto mínimo detectable usa una prueba bilateral al 5 % y potencia del 80 %.

## La estimación inmediata es negativa con ambos métodos

**Identificador** `contrastes` · **Tiempo** Fuera de la ruta cronometrada

**Explicación oral**

El emparejamiento uno a uno conserva los 77 tratados. Se estiman 0,311 siniestros registrados menos por municipio y día. Los intervalos de ambos métodos incluyen cero. Cambian los controles y sus pesos.

**Transición**

Volver al índice de respaldos.

**Referencia para consulta.** Reporte, §4, cuadro A5 y cuadros B1–B2. Estimaciones en siniestros registrados por municipio y día.

## Trayectorias diarias de ambos emparejamientos

**Identificador** `alternativas` · **Tiempo** Fuera de la ruta cronometrada

**Explicación oral**

Los dos métodos usan la base de 21 días y el ajuste por día de la semana. Uno a uno conserva los mismos 77 pares tratados. El cuadro de resultados y la trayectoria permiten ver cómo cambian la magnitud y la precisión al seleccionar otro conjunto de controles.

**Transición**

Volver al índice de respaldos.

**Referencia para consulta.** Reporte, figura 1 y apéndices A–C.

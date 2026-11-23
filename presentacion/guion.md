# Guion de exposición

**Narcoataques y siniestros viales registrados**

Eduardo Garcia Cortez · CU: 207480 · Inferencia Causal · ITAM

Ruta principal de **480 segundos (8:00)**. Los tiempos incluyen las transiciones. Para ensayar, lee la explicación oral y la transición. Los respaldos quedan fuera del tiempo.

## ¿Cómo cambian los accidentes registrados tras el inicio local de narcoataques?

**Identificador** `pregunta` · **Tiempo** 0:00–0:30 (30 s)

**Explicación oral**

¿Cómo cambian los accidentes registrados tras el inicio local de narcoataques? Los bloqueos pueden reducir la circulación y los desvíos podrían compensar esa caída. El artículo de Bauernschuster y Rekers inspira el seguimiento diario de una exposición transitoria. Aquí observo las dos semanas desde el inicio y adapto el emparejamiento al contexto mexicano.

**Transición**

El mapa ubica los municipios que aportan esas comparaciones.

**Referencia para consulta.** Reporte, §1 y §5. Bauernschuster y Rekers (2022).

## La muestra reúne 77 pares tratados

**Identificador** `datos` · **Tiempo** 0:30–1:20 (50 s)

**Explicación oral**

El mapa cuenta municipios únicos. La unidad es el par municipio–episodio: un municipio reaparece si participa en otra fecha. El catálogo propio exige acciones coordinadas en tres o más lugares en 24 horas. La violencia puede continuar después del inicio local. Tres agentes de inteligencia artificial asistieron la búsqueda web, con cobertura desigual y sin validación humana exhaustiva. Los accidentes y las covariables provienen de fuentes oficiales. ATUS es la Estadística de Accidentes de Tránsito Terrestre en Zonas Urbanas y Suburbanas del Instituto Nacional de Estadística y Geografía, INEGI. Un cero indica cero registros publicados con fecha válida. El conteo tampoco mide el riesgo por viaje.

**Transición**

Con esta unidad, podemos buscar municipios comparables para cada inicio.

**Referencia para consulta.** Reporte, §2 y apéndices A, E y F. Los 3 613 pares son 77 tratados y 3 536 controles.

## Cada tratado tiene su comparación

**Identificador** `matching` · **Tiempo** 1:20–2:10 (50 s)

**Explicación oral**

Cada tratado se compara con municipios de estados ajenos al episodio, en las mismas fechas. Exijo cobertura en tres meses completos previos, estabilidad territorial y ausencia de exposición documentada desde el Día menos 49. Aplico márgenes de la mitad al doble en accidentes previos, población, empleo y autos. Diez candidatos de cinco estados es el mínimo para que el tratado tenga soporte. Uno a muchos usa a todos los elegibles. Uno a uno toma al más cercano por población, empleo y autos, dentro de ese mismo conjunto. Un control puede participar más de una vez. El efecto que queremos medir es el cambio promedio atribuible al inicio entre los pares tratados incluidos, con igual peso por par.

**Transición**

La comparación requiere una base previa para cada día analizado.

**Referencia para consulta.** Reporte, §3 y apéndice A. Covariables disponibles con medición anterior a t−28.

## Cada día tiene tres referencias previas

**Identificador** `base` · **Tiempo** 2:10–3:05 (55 s)

**Explicación oral**

Cada casilla es un día respecto al inicio. Analizo tres tramos posteriores: días cero a uno, dos a seis y siete a trece. Si el inicio es jueves, uso los jueves menos 28, menos 21 y menos 14. El jueves siguiente reutiliza esos jueves. La semana menos uno sirve para el diagnóstico previo. En la fórmula, i indica municipio, t el inicio local, h el día relativo y Y el conteo. Primero transformo cada conteo con logaritmo de uno más Y. Después promedio las tres referencias y resto esa base del valor observado. Cada tramo promedia cambios de días naturales. El Día 0 puede incluir horas anteriores al inicio.

**Transición**

Una vez que cada municipio tiene un cambio, podemos contrastarlo con el de sus controles.

**Referencia para consulta.** Reporte, §3. Ejemplo fechado: 17 de octubre de 2019 en Culiacán.

## La fecha común permite comparar cambios

**Identificador** `regresion` · **Tiempo** 3:05–4:00 (55 s)

**Explicación oral**

La variable dependiente es el cambio que acabamos de construir. D vale uno para el tratado y cero para un control. Lambda es el efecto fijo de fecha: descuenta cambios comunes en esas fechas, por ejemplo, una caída general de la circulación durante la pandemia. Beta es la diferencia entre cambios. X reúne covariables previas, gamma sus coeficientes y u el residuo. La regresión usa mínimos cuadrados ponderados. En M cero, cada tratado pesa uno y distribuye una unidad de peso entre sus controles. Equivale a promediar 77 contrastes, uno por par tratado. M uno añade logaritmo de población, M dos empleo por mil habitantes y M tres autos por mil. La muestra y los pesos explícitos se conservan.

**Transición**

Veamos las trayectorias que dan origen a ese contraste.

**Referencia para consulta.** Reporte, §3 y §3.1. Los modelos ajustados pueden cambiar la ponderación implícita.

## De las trayectorias a la diferencia de cambios

**Identificador** `eventos` · **Tiempo** 4:00–5:00 (60 s)

**Explicación oral**

A la izquierda, cada línea promedia los valores observados de logaritmo de uno más Y. Alineo cada serie en su inicio local. Los tratados pesan lo mismo y los controles conservan los pesos del emparejamiento. El fondo claro marca la ventana de referencia. Cada comparación usa tres días de esa ventana. A la derecha, resto a cada par su propia base del mismo día semanal y después promedio por grupo. El cero de este panel indica igualdad con la base propia. Justo antes del inicio, por ejemplo en el Día menos dos, las dos líneas registran cambios distintos. La distancia vertical entre ellas da el coeficiente diario del modelo M cero. Así llegamos a un contraste de cambios con unidades y pesos definidos.

**Transición**

Ahora podemos ver esa distancia como una sola trayectoria, con su incertidumbre.

**Referencia para consulta.** Conteos diarios limpios y pares y pesos guardados. Las 21 diferencias de cambios reproducen los coeficientes de M₀.

## Las diferencias previas limitan la atribución

**Identificador** `trayectoria` · **Tiempo** 5:00–5:45 (45 s)

**Explicación oral**

Cada punto compara los cambios. Su intervalo puntual del 95 por ciento admite dependencia por estado y fecha. Para atribuirlo al ataque, los cambios sin ataque tendrían que ser paralelos en esta escala. También requerimos una base libre de anticipación y de efectos de ataques previos, y controles sin contagio. El emparejamiento mejora el balance observado. Aun así, los Días menos cinco y menos dos presentan diferencias negativas. La prueba semanal rechaza diferencias previas nulas por estado. Al agrupar también por fecha, el valor p es 0,109. La evidencia deja abierta una fuente de sesgo.

**Transición**

Con esa cautela, veamos el resultado inicial y cuánto cambia con el ajuste.

**Referencia para consulta.** Reporte, §3–4, figura 1 y apéndice D. La prueba semanal compara Sem. −4, −3 y −1 con Sem. −2.

## El ajuste cambia poco la estimación inicial

**Identificador** `resultados` · **Tiempo** 5:45–6:25 (40 s)

**Explicación oral**

En M cero, menos 0,107 es el coeficiente estimado del tratamiento. Resta al cambio medio de los tratados el de sus controles, respecto a la base y en la escala de logaritmo de uno más Y. Su valor p es 0,019. Cada columna añade al modelo anterior logaritmo de población, empleo o autos por mil habitantes. El coeficiente cambia poco. En conteos y con el emparejamiento uno a uno, los intervalos del tratamiento incluyen cero.

**Transición**

Veamos si la caída persiste después del primer tramo.

**Referencia para consulta.** Reporte, cuadro 2, Panel A, y apéndices A y B. Los asteriscos siguen los umbrales de R: 0,001 (***), 0,01 (**) y 0,05 (*). Los coeficientes de las covariables son ajustes estadísticos.

## La duración queda abierta

**Identificador** `duracion` · **Tiempo** 6:25–7:05 (40 s)

**Explicación oral**

Cada punto resume un tramo y tiene su propio intervalo. La mayor caída se estima en los días cero a uno: menos 0,107 en la escala logarítmica. Después, las estimaciones son menores y sus intervalos admiten una caída y un cambio nulo. La señal de los días siete a trece depende de la agrupación y las exclusiones. Si exijo continuidad del registro y ausencia de otro ataque posterior, cambia la muestra. El seguimiento hasta el Día trece deja abierta la duración.

**Transición**

La base y el calendario también afectan la lectura del resultado inicial.

**Referencia para consulta.** Reporte, §4, cuadros B1–B2 y apéndice D. Se permite que el episodio inicial continúe.

## La referencia previa y el calendario importan

**Identificador** `sensibilidades` · **Tiempo** 7:05–7:40 (35 s)

**Explicación oral**

Con los mismos pares y pesos, si uso la semana previa, la caída es menor. Si uso el Día menos dos, el signo cambia. Ambos intervalos incluyen cero. Al excluir feriados y recesos escolares, el coeficiente es algo más negativo, pero quedan solo 25 pares tratados y aumenta la incertidumbre. También cambia la composición. El placebo reconstruye la comparación 28 días antes. Su estimación inmediata es de menor magnitud y su intervalo incluye cero. Ninguna de estas comprobaciones, por sí sola, establece causalidad.

**Transición**

¿Qué se puede sostener con ese conjunto de resultados?

**Referencia para consulta.** Reporte, cuadros B2–B3 y C1–C4. La sensibilidad amplia usa feriados laborales y recesos de educación básica.

## La mayor caída relativa aparece al inicio

**Identificador** `conclusion` · **Tiempo** 7:40–8:00 (20 s)

**Explicación oral**

La mayor caída relativa de registros aparece al inicio. Después, las estimaciones son menores y queda abierta la duración. La limitación central para atribuir la caída al ataque es que tratados y controles ya mostraban diferencias antes del inicio.

**Transición**

Aquí termina la exposición. Los respaldos sirven para la discusión.

**Referencia para consulta.** Reporte, §5 y apéndices E–G.

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

El nivel de accidentes se calcula en Días menos 28 a menos 15. Su razón usa un desplazamiento de 0,5 en numerador y denominador. Las tres covariables cumplen por separado el margen. En uno a muchos, si un control se reutiliza en una fecha, se suman sus aportes; un tratado con cuarenta controles reparte una unidad en cuarenta partes. En uno a uno se elige el vecino por población, empleo y autos. La cobertura previa predice el universo, y los cambios posteriores de captación pueden afectar el resultado. El comparador observado requiere además ausencia de contagio y cambios paralelos.

**Transición**

Volver al índice de respaldos.

**Referencia para consulta.** Reporte, cuadro 1, §3 y apéndices A y D.

## La agrupación permite errores dependientes

**Identificador** `inferencia` · **Tiempo** Fuera de la ruta cronometrada

**Explicación oral**

La agrupación en dos dimensiones admite dependencia por estado y por fecha, descuenta su intersección y conserva el coeficiente. Se distingue de un ajuste de Bonferroni: los intervalos de la trayectoria tienen cobertura nominal por punto. Catorce estados aportan tratados y el peso está concentrado. El intervalo alternativo omite un estado a la vez, conserva los pesos de las filas restantes y vuelve a absorber las fechas. En la prueba previa, la semana menos dos es el punto de referencia para una comparación conjunta distinta de la base diaria y del placebo. El efecto mínimo detectable en niveles para Días 0–1 es de 0,664 registros por municipio y día, bajo prueba bilateral del 5 por ciento y potencia del 80 por ciento.

**Transición**

Volver al índice de respaldos.

**Referencia para consulta.** Reporte, §3.1, §4 y apéndice D.

## El signo se mantiene con 1:1 y en niveles

**Identificador** `contrastes` · **Tiempo** Fuera de la ruta cronometrada

**Explicación oral**

En uno a uno la magnitud es similar y el intervalo se amplía. En niveles se estiman 0,397 registros menos por municipio y día. El intervalo admite otras magnitudes y un cambio nulo. La transformación exponencial del coeficiente principal da una caída del 10,2 por ciento en la escala geométrica de uno más Y. La media aritmética de los accidentes corresponde a otra cantidad.

**Transición**

Volver al índice de respaldos.

**Referencia para consulta.** Reporte, §4 y cuadros B1–B2.

## En niveles cambia la precisión

**Identificador** `alternativas` · **Tiempo** Fuera de la ruta cronometrada

**Explicación oral**

En niveles, el punto se interpreta como registros por municipio y día. En uno a uno usamos los mismos 77 pares tratados y cambiamos comparadores y pesos. Un intervalo que incluye cero admite un cambio nulo y también otros efectos. Que un método excluya cero y otro lo incluya no establece una diferencia estadística entre métodos. Las tendencias paralelas se requieren en la escala empleada. La comparación semanal de la crisis prolongada de Culiacán desde septiembre de 2024 queda fuera del reporte y de esta exposición.

**Transición**

Volver al índice de respaldos.

**Referencia para consulta.** Reporte, figura 1, apéndices A–C y README del repositorio.

## Los registros y el catálogo tienen coberturas distintas

**Identificador** `alcance` · **Tiempo** Fuera de la ruta cronometrada

**Explicación oral**

El catálogo recoge prensa y comunicados sobre acciones coordinadas. Los cotejos entre agentes ayudan a corroborar casos y dejan incertidumbre en la cobertura. Las exclusiones de casos pendientes o señales en controles corresponden a sensibilidades del reporte. ATUS se concentra en vías no federales. El registro puede cambiar si se altera la atención de emergencias o el proceso de publicación. Las covariables se enlazan con medición previa a la base, aunque las ediciones consultadas son retrospectivas. El apéndice H contiene el código R reproducible.

**Transición**

Volver al índice de respaldos.

**Referencia para consulta.** Reporte, §2 y apéndices A, C, E, F y H.

## El antecedente alemán orienta la pregunta temporal

**Identificador** `fuentes` · **Tiempo** Fuera de la ruta cronometrada

**Explicación oral**

El artículo aprovecha fechas de operativos y participación por estado en Alemania. Le tomo la pregunta por la duración de un cambio tras una exposición transitoria y la frecuencia diaria. El diseño mexicano usa inicios locales que pueden repetirse y compara municipios seleccionados para las mismas fechas. La base y las reglas de emparejamiento responden a ese problema.

**Transición**

Volver al índice de respaldos.

**Referencia para consulta.** Bauernschuster y Rekers (2022), figuras 1 y 4. Reporte, §1 y §3.

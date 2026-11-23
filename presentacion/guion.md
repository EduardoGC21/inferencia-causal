# Guion de exposición

**Narcoataques y siniestros viales registrados**

Eduardo Garcia Cortez · CU: 207480 · Inferencia Causal · ITAM

Ruta principal de **480 segundos (8:00)**. Los tiempos incluyen las transiciones. Para ensayar, lee la explicación oral y la transición. Los respaldos quedan fuera del tiempo.

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

La comparación requiere una base previa para cada día analizado.

**Referencia para consulta.** Reporte, §3 y apéndice A. Covariables disponibles con medición anterior a t−28.

## Cada día tiene tres referencias previas

**Identificador** `base` · **Tiempo** 2:30–3:20 (50 s)

**Explicación oral**

Analizo tres tramos posteriores: días cero a uno, dos a seis y siete a trece. Si el inicio es jueves, uso los jueves menos 28, menos 21 y menos 14. El jueves siguiente reutiliza esas referencias. Dejo fuera la semana menos uno para ver si los grupos ya divergían. En la fórmula, i indica municipio, t el inicio local, h el día relativo y r conserva el día de la semana. Aplico logaritmo de uno más Y a cada conteo antes de promediar las tres referencias. Resto esa base del valor observado. Cada tramo promedia cambios diarios. El Día 0 puede incluir horas anteriores al inicio.

**Transición**

Una vez que cada municipio tiene un cambio, podemos contrastarlo con el de sus controles.

**Referencia para consulta.** Reporte, §3. La regla r(t,h) = t + (h mod 7) mantiene la base entre los días −28 y −8. El ejemplo usa el jueves 17 de octubre de 2019 en Culiacán.

## Estimación por mínimos cuadrados ponderados

**Identificador** `regresion` · **Tiempo** 3:20–4:10 (50 s)

**Explicación oral**

La variable dependiente es el cambio que acabamos de construir. D vale uno para el tratado y cero para un control. Lambda es el efecto fijo de fecha y descuenta cambios comunes a cada inicio. Beta es la diferencia entre cambios. Buscamos estimar el efecto promedio del tratamiento sobre los tratados, el ATT. X reúne covariables previas, gamma sus coeficientes y u el residuo. La regresión usa mínimos cuadrados ponderados. En M cero, cada tratado pesa uno y distribuye una unidad de peso entre sus controles. Equivale a promediar 77 contrastes, uno por par tratado. M uno añade logaritmo de población, M dos empleo por mil habitantes y M tres autos por mil. La muestra y los pesos explícitos se conservan.

**Transición**

Veamos las trayectorias que dan origen a ese contraste.

**Referencia para consulta.** Reporte, §3 y §3.1. Los modelos ajustados pueden cambiar la ponderación implícita.

## Promedios y cambios de tratados y controles

**Identificador** `eventos` · **Tiempo** 4:10–5:10 (60 s)

**Explicación oral**

A la izquierda, cada línea promedia los valores observados de logaritmo de uno más Y. Alineo cada serie en su inicio local. Los tratados pesan lo mismo y los controles conservan los pesos del emparejamiento. A la derecha, resto a cada par su propia base del mismo día semanal y después promedio por grupo. El cero de este panel indica igualdad con la base propia. Justo antes del inicio, por ejemplo en el Día menos dos, las dos líneas registran cambios distintos. La distancia vertical entre ellas da el coeficiente diario del modelo M cero. Así llegamos a un contraste de cambios con unidades y pesos definidos.

**Transición**

Ahora podemos ver esa distancia como una sola trayectoria, con su incertidumbre.

**Referencia para consulta.** Conteos diarios limpios y pares y pesos guardados. Las 21 diferencias de cambios reproducen los coeficientes de M₀.

## Diagnóstico de tendencias paralelas

**Identificador** `trayectoria` · **Tiempo** 5:10–5:55 (45 s)

**Explicación oral**

Cada punto es la diferencia entre los cambios de tratados y controles. Es el coeficiente estimado, beta gorro. Las barras muestran la incertidumbre de esa diferencia. Antes del Día 0 esperamos que los puntos fluctúen alrededor de cero. Aquí aparecen diferencias puntuales, como en el Día −2. La prueba por semanas detecta diferencias al agrupar por estado y es inconclusa al agrupar por estado y fecha. Por eso interpreto con cautela la caída que aparece al inicio.

**Transición**

Con esa cautela, veamos el resultado inicial y cuánto cambia con el ajuste.

**Referencia para consulta.** Reporte, §3–4, figura 1 y apéndice D. La prueba semanal compara Sem. −4, −3 y −1 con Sem. −2.

## Añadir covariables cambia poco la estimación inicial

**Identificador** `resultados` · **Tiempo** 5:55–6:30 (35 s)

**Explicación oral**

En M cero, menos 0,107 es el coeficiente estimado del tratamiento. Resta al cambio medio de los tratados el de sus controles, respecto a la base y en la escala de logaritmo de uno más Y. Su valor p es 0,019. Cada columna añade al modelo anterior logaritmo de población, empleo o autos por mil habitantes. El coeficiente cambia poco. En conteos y con el emparejamiento uno a uno, los intervalos del tratamiento incluyen cero.

**Transición**

Veamos si la caída persiste después del primer tramo.

**Referencia para consulta.** Reporte, cuadro 2, Panel A, y apéndices A y B. Los asteriscos siguen los umbrales de R: 0,001 (***), 0,01 (**) y 0,05 (*). Los coeficientes de las covariables son ajustes estadísticos.

## La caída estimada es mayor en los días 0 y 1

**Identificador** `duracion` · **Tiempo** 6:30–7:10 (40 s)

**Explicación oral**

Cada punto resume un tramo y tiene su propio intervalo. La mayor caída se estima en los días cero a uno: menos 0,107 en la escala logarítmica. Después, los coeficientes están más cerca de cero y sus intervalos admiten una caída y un cambio nulo. La señal de los días siete a trece depende de la agrupación y las exclusiones. Si exijo continuidad del registro y ausencia de otro ataque posterior, cambia la muestra. El seguimiento hasta el Día trece deja abierta la duración.

**Transición**

La base y el calendario también afectan la lectura del resultado inicial.

**Referencia para consulta.** Reporte, §4, cuadros B1–B2 y apéndice D. Se permite que el episodio inicial continúe.

## Sensibilidad del resultado

**Identificador** `sensibilidades` · **Tiempo** 7:10–7:40 (30 s)

**Explicación oral**

Con los mismos pares y pesos, usar la semana previa como base atenúa la caída y el intervalo incluye cero. Si el día cero o uno cae en feriado o receso, excluyo ese inicio. Quedan 25 pares y el intervalo se amplía. El placebo simula un inicio 28 días antes. La caída estimada es menor y su intervalo incluye cero.

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

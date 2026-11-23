---
fecha_creacion: 2026-11-22
tags:
 - nota
---

# Narcoataques y siniestros viales registrados

*Cambios en siniestros viales tras el inicio local de narcoataques en municipios mexicanos, 2019–2025*

**Eduardo Garcia Cortez · Clave única: 207480**

**Profesor: Mauricio Romero**

Inferencia Causal · ITAM · Noviembre de 2026

> Versión Markdown sincronizada con el [reporte en PDF](reporte.pdf). El PDF corresponde al contenido aprobado de esta nota.

## Resumen

Se estudian los accidentes registrados tras el inicio local de narcoataques en municipios mexicanos, 2019–2025. Se comparan cambios de municipios tratados con controles emparejados, respecto a tres semanas previas del mismo día de la semana. La muestra contiene 77 pares municipio–episodio y 32 fechas de inicio. En los Días 0–1, la estimación principal es -0,107 en $\log(1+Y)$, donde $Y$ cuenta accidentes registrados, con intervalo de confianza del 95 % de [-0,195; -0,019], agrupado por estado y fecha. La caída posterior es menor e incierta. Las diferencias previas entre grupos limitan la atribución causal.

## 1. Contexto y motivación

¿Cómo cambian los accidentes registrados tras el inicio local de narcoataques? La hipótesis es que los bloqueos y la suspensión del transporte reducen la circulación; los desvíos y los cambios al conducir pueden contrarrestar esa caída. La violencia contra transportistas de Chilpancingo en febrero de 2024 ilustra la interrupción del transporte público (Amapola Periodismo, 2024). Se utiliza la Estadística de Accidentes de Tránsito Terrestre en Zonas Urbanas y Suburbanas (ATUS), del Instituto Nacional de Estadística y Geografía (INEGI), que cubre vías no federales (2026a). Su conteo refleja accidentes y captación; no mide riesgo por viaje.

El objetivo es el efecto promedio del tratamiento entre los tratados (ATT): la diferencia entre los registros con y sin el inicio del ataque para los pares municipio–episodio incluidos, con igual peso para cada par. Se distinguen Días 0–1, Días 2–6 y Sem. +1 (Días 7–13). El Día 0 es la fecha del inicio local y puede incluir horas anteriores al ataque; Días 0–1 son dos días naturales, no necesariamente las primeras 48 horas.

Bauernschuster y Rekers (2022) encuentran una reducción de accidentes durante operativos alemanes de velocidad de un día, sin persistencia posterior detectable. Este antecedente motiva separar el cambio inmediato de su duración y revisar el calendario, aunque los mecanismos difieren de los narcoataques. Dell (2015) documenta desplazamientos de rutas del narcotráfico y de la violencia, lo que motiva examinar posibles efectos sobre los controles; no demuestra que hayan ocurrido en esta muestra.

## 2. Datos

### Accidentes y exposición.

Se utilizan los microdatos definitivos de ATUS de 2019–2025 y los últimos meses de 2018 para revisar la cobertura previa (Instituto Nacional de Estadística y Geografía, 2025a, 2026a). En 2019–2025 hay 2 518 436 registros con fecha válida. Se conservan filas con atributos repetidos porque ATUS no proporciona un identificador único de accidente.

La muestra principal contiene 3 613 pares municipio–fecha: 77 tratados y 3 536 controles. Reúne 54 municipios tratados y 765 de control, con posibles repeticiones entre grupos y fechas. Los 31 episodios tienen inicio local en 32 fechas, pues un episodio puede comenzar en fechas distintas según el municipio. Cada regresión utiliza una observación por par para el día o intervalo analizado.

Se identifica un episodio a partir de acciones coordinadas en al menos tres lugares dentro de 24 horas, con afectación del espacio público, comercios o transporte. Los lugares pueden pertenecer a municipios distintos. Para cada municipio se identifica el inicio local, aunque la violencia continúe después.

El catálogo es propio: tres subagentes de inteligencia artificial (IA) recopilaron prensa y comunicados oficiales que corroboran algunos casos. No es una base oficial consolidada ni una validación humana exhaustiva. La cobertura es desigual y persisten casos pendientes de corroboración. Los incidentes menores o inciertos sirven como antecedentes de exposición; los apéndices C y E detallan las exclusiones y la construcción del catálogo.

### Cobertura y ceros.

Se exige al menos un registro con fecha válida en cada uno de los tres meses completos anteriores al mes del inicio. La muestra principal se selecciona con información previa y no exige continuidad del registro después del ataque.

El resultado cuenta accidentes publicados con fecha válida. Un cero indica ausencia de registros para ese municipio y día; no distingue entre ausencia de accidentes, hechos sin registro o interrupciones de la captación. Los faltantes del panel de continuidad se conservan como faltantes.

### Covariables y territorio.

La población procede de la Encuesta Intercensal 2015 (EIC) y de los Principales resultados por localidad (ITER) del Censo 2020. El Sistema Automatizado de Información Censal (SAIC) aporta empleo de 2018 y 2023; Vehículos de Motor Registrados en Circulación (VMRC), automóviles de 2018–2024. Las tasas por mil habitantes usan población anual del Consejo Nacional de Población (CONAPO). El Catálogo Único de Claves de Áreas Geoestadísticas Estatales, Municipales y Localidades (AGEEML) permite revisar cambios territoriales (Consejo Nacional de Población, 2024; Instituto Nacional de Estadística y Geografía, 2015, 2021, 2025b, 2026c, 2026b).

Para cada inicio $t$, se selecciona por variable la medición más reciente anterior a $t-28$. Las ediciones consultadas son retrospectivas: la regla evita mediciones posteriores al ataque, pero no reproduce la información publicada en aquel momento.

Antes de exigir datos completos, el empleo y los automóviles se enlazan en 82 de los 84 pares tratados elegibles (97,6 % en cada fuente). Una fila enlazada puede contener valores inutilizables; el emparejamiento exige valores utilizables. El apéndice A presenta las tasas de todas las fuentes y los filtros que dejan 77 pares tratados.

**Cuadro 1.** Comparabilidad previa de la muestra final

| Variable | Tratados: media (DE) | Controles 1:muchos | DME 1:muchos | DME 1:1 |
|:---|---:|---:|---:|---:|
| Población | 229 998,60 (243 845,81) | 225 349,52 (281 538,21) | 0,013 | 0,005 |
| Empleo / mil | 206,96 (95,98) | 197,32 (90,33) | 0,070 | 0,027 |
| Autos / mil | 208,63 (87,90) | 219,93 (97,55) | -0,082 | -0,023 |
| Accidentes previos | 2,05 (3,41) | 2,09 (3,45) | -0,011 | 0,012 |

Desviación estándar (DE) ponderada entre pares. Las diferencias de medias estandarizadas (DME) utilizan como escala común la raíz del promedio de varianzas de ambos grupos de la referencia con calibre individual. El nivel previo es la media de $[-28,-15]$; su DE entre pares difiere de la DE de niveles diarios que estandariza los efectos.

## 3. Estrategia empírica

### Estimando y base.

Sea $t$ el inicio local, $D_{it}$ la asignación focal y $A_{it}$ la elegibilidad previa. Para $g(y)=\log(1+y)$, principal, o $g(y)=y$, complementaria, el objetivo es

$$
\tau_h^g=E[g(Y_{i,t+h}(1))-g(Y_{i,t+h}(0))\mid D_{it}=1,A_{it}=1,\text{soporte}].
$$

La muestra principal no se condiciona a la ausencia de violencia posterior. Se definen $q(h)=h\bmod7\in\{0,\ldots,6\}$, $r(t,h)=t+q(h)$ y

$$
B_{ith}^g=\tfrac13\sum_{k\in\{28,21,14\}}g(Y_{i,r(t,h)-k}),\qquad
\Delta_{ith}^g=g(Y_{i,t+h})-B_{ith}^g.
$$

Para cada día analizado, la base promedia tres fechas anteriores al inicio con el mismo día de la semana, entre los Días -28 y -8. La semana inmediatamente anterior queda fuera. Cada intervalo promedia los cambios diarios respecto a esa base.

En Culiacán, Sinaloa, el jueves 17 de octubre de 2019 se compara con los jueves 19 y 26 de septiembre y 3 de octubre. El jueves siguiente reutiliza esas referencias; la base siempre permanece antes del inicio.

Se aplica $\log(1+Y)$ a cada conteo antes de promediar: el uno incluye ceros y el logaritmo reduce la influencia de conteos altos. En niveles se utiliza el conteo directo. Cada escala requiere tendencias paralelas propias; la validez en una no demuestra validez en la otra.

### Comparadores y pesos.

Se excluyen municipios con exposición documentada entre los Días -49 y -1: la regla cubre la base y añade 21 días anteriores a su primera medición. Se supone que los ataques más antiguos ya no afectan la comparación.

Los controles proceden de estados ajenos al episodio. También se excluyen municipios con antecedentes documentados y estados con señales previas sin municipio identificable. Se exige estabilidad territorial desde el inicio de la base hasta la víspera del ataque. La selección principal no utiliza ataques posteriores.

El nivel previo es la media de los Días -28 a -15. Se exige $(\bar Y_c+0.5)/(\bar Y_i+0.5)\in[0.5,2]$, donde $\bar Y_i$ y $\bar Y_c$ son las medias del tratado y del candidato. La población, el empleo y los automóviles por mil habitantes también deben estar, por separado, entre la mitad y el doble del valor tratado. Se requieren al menos diez candidatos de cinco estados por tratado.

El matching 1:muchos utiliza todos los candidatos: cada tratado pesa uno y reparte otro peso total de uno entre sus controles. El matching 1:1 elige el candidato más cercano según población, empleo y automóviles, después de comprobar el mismo mínimo de candidatos y estados. Se permite reutilizar controles; sus pesos acumulan las contribuciones de cada tratado.

La regresión de diferencias en diferencias compara el cambio de cada municipio tratado respecto a su base previa con el cambio de sus controles en las mismas fechas. Se estima por mínimos cuadrados ponderados:

$$
\Delta_{ith}^{g}=\lambda_{th}+\beta_h^{g}D_{it}+X_{it}'\gamma_h+u_{ith}.
$$

Aquí, $i$ es el municipio; $t$, el inicio local; y $h$, el día o intervalo. $\Delta_{ith}^g$ es el cambio respecto a la base en la escala $g$. $D_{it}$ distingue tratados y controles; $\lambda_{th}$ recoge el cambio común de la fecha. $\beta_h^g$ compara los cambios de ambos grupos. $X_{it}$ contiene covariables previas, $\gamma_h$ sus coeficientes y $u_{ith}$ el residuo.

El modelo principal $M_0$ omite $X_{it}$ y promedia por igual las diferencias en diferencias de los tratados. $M_1$ añade logaritmo de población; $M_2$, empleo por mil habitantes; y $M_3$, automóviles por mil habitantes. Todos conservan muestra y pesos explícitos. Los modelos ajustados evalúan sensibilidad al ajuste lineal, cuya ponderación implícita puede diferir de la de $M_0$.

### Identificación y sesgo.

Supuestos no comprobables directamente: sin el ataque, tratados y controles habrían tenido cambios paralelos en la escala analizada; no habría anticipación en la base, efectos persistentes de ataques anteriores ni efectos de la violencia sobre los controles. El emparejamiento mejora la comparabilidad observada, pero no garantiza esos supuestos. Si fallan, el coeficiente puede incorporar diferencias ajenas al ataque. Los cambios de captación también limitan interpretar los registros como cambios de accidentes reales.

Comprobaciones con la información disponible: fechas, criterios de inclusión y pesos. Los resultados previos y el placebo permiten detectar problemas de comparación; no demostrar tendencias paralelas (Roth, 2022). Como los episodios pueden repetirse, no corresponde suponer automáticamente una adopción permanente del tratamiento (Dube et al., 2025).

### 3.1. Inferencia y separación de estimandos

Se utilizan errores estándar agrupados por estado para admitir dependencia entre municipios del mismo estado a lo largo del tiempo. Los intervalos principales añaden agrupación por fecha de inicio, que admite dependencia entre municipios con la misma fecha. La agrupación cambia la precisión, no el coeficiente ni la muestra.

De los 32 estados, 14 aportan tratados. Se revisa la concentración de peso mediante la omisión de cada estado por turno y un intervalo alternativo. El apéndice D detalla el cálculo y las correcciones por número de grupos (MacKinnon et al., 2023a, 2023b). Estas medidas no corrigen sesgo.

La duración se examina en la muestra principal. Como contraste, se exige continuidad del reporte entre los Días -28 y +13 y ausencia de otra exposición hasta +14; el episodio inicial puede continuar. Esta muestra depende de sucesos posteriores al ataque y puede incorporar selección, por lo que no se interpreta automáticamente como el mismo efecto causal.

## 4. Resultados

### Efecto inmediato y escala.

En los Días 0–1, $M_0$ con emparejamiento 1:muchos estima -0,107 en $\log(1+Y)$, con intervalo de confianza del 95 % de [-0,195; -0,019], agrupado por estado y fecha. Equivale a -0,130 desviaciones estándar diarias previas y a una caída aproximada del 10,2 % en la escala geométrica de $1+Y$, no directamente en el promedio de $Y$. El intervalo alternativo por omisión de estados también excluye cero.

En niveles, se estiman 0,397 registros menos por municipio y día, equivalentes a -0,108 desviaciones estándar; el intervalo [-0,865; 0,072] incluye cero. El efecto mínimo detectable (MDE) es de 0,664 registros, con prueba bilateral al 5 % y potencia del 80 %. El cambio nulo no queda demostrado. Estos resultados no distinguen circulación, conducta y captación.

Los contrastes y la estandarización se detallan en el cuadro B1 del apéndice B; el cálculo de potencia, en el apéndice D.

### Especificaciones progresivas.

El cuadro 2 muestra que el ajuste por población, empleo y automóviles cambia poco la estimación inmediata: los coeficientes se sitúan entre -0,105 y -0,108 en $\log(1+Y)$ y entre -0,381 y -0,401 registros por municipio y día.

Esta estabilidad no descarta factores omitidos ni garantiza tendencias paralelas. El Panel A presenta los resultados logarítmicos; el Panel B, en niveles, está en el apéndice A.

**Cuadro 2.** Días 0–1: regresiones con ajuste progresivo en la muestra principal

**Panel A. Resultado: cambio en $\log(1+Y)$**

| Variable / estadístico | $M_0$ | $M_1$ | $M_2$ | $M_3$ |
|:---|---:|---:|---:|---:|
| Tratamiento | -0,107<br>(0,043)<br>[-0,195; -0,019]<br>$p=0{,}019$ | -0,105<br>(0,043)<br>[-0,194; -0,017]<br>$p=0{,}021$ | -0,107<br>(0,043)<br>[-0,195; -0,018]<br>$p=0{,}020$ | -0,108<br>(0,045)<br>[-0,200; -0,017]<br>$p=0{,}022$ |
| Logaritmo de la población | — | -0,022<br>(0,019)<br>[-0,061; 0,017]<br>$p=0{,}261$ | -0,030<br>(0,029)<br>[-0,088; 0,028]<br>$p=0{,}303$ | -0,029<br>(0,028)<br>[-0,085; 0,028]<br>$p=0{,}309$ |
| Empleo por cada mil habitantes | — | — | 0,000184<br>(0,000399)<br>[-0,000631; 0,000998]<br>$p=0{,}649$ | 0,000214<br>(0,000434)<br>[-0,000671; 0,001100]<br>$p=0{,}625$ |
| Automóviles por cada mil habitantes | — | — | — | -0,000111<br>(0,000245)<br>[-0,000612; 0,000389]<br>$p=0{,}653$ |
| $R^2$ ponderado | 0,162 | 0,164 | 0,165 | 0,166 |
| $R^2$ tras descontar las fechas | 0,022 | 0,025 | 0,026 | 0,027 |

Cada celda presenta estimación, error estándar (EE), intervalo de confianza (IC) del 95 % y valor $p$ bilateral, con agrupación por estado y fecha y 31 grados de libertad. El guion indica una variable excluida. Las dos medidas de $R^2$ se explican en el apéndice A.

Emparejamiento 1:muchos: los cuatro modelos utilizan 3 613 observaciones municipio–fecha, 77 pares tratados, 32 fechas de inicio y efectos fijos de fecha. Conservan muestra, pesos y base de tres semanas. Los coeficientes de las covariables son ajustes estadísticos, no sus efectos causales.

### Trayectoria y falsificaciones.

La figura 1 muestra una caída alrededor del inicio, mayor en los Días 0–1. También aparecen diferencias previas: Sem. -1 tiene una estimación logarítmica de -0,034 [-0,079; 0,011], y los Días -2 y -5 presentan -0,116 y -0,085. Estas señales limitan la atribución al ataque. Los intervalos corresponden a cada punto, no a toda la trayectoria.

**Figura 1. Los accidentes registrados muestran una caída relativa alrededor del inicio local.** Modelo $M_0$, emparejamientos 1:muchos y 1:1. Día 0: inicio local. Base: tres fechas previas del mismo día de la semana. Arriba: cambio en $\log(1+Y)$; abajo: cambio en registros por municipio y día. Barras: intervalos puntuales del 95 %, agrupados por estado y fecha. La línea vertical marca el Día 0.

![Trayectoria de registros](figuras/trayectoria-siniestros.png)

El contraste conjunto de las semanas -4, -3 y -1, respecto a la -2, rechaza diferencias previas nulas con agrupación estatal ($p<0{,}001$), pero no con agrupación por estado y fecha ($p=0{,}109$). El primer resultado señala diferencias que el emparejamiento no eliminó; el segundo no demuestra tendencias paralelas. Esta referencia sirve al diagnóstico y no sustituye la base principal (apéndice D).

El placebo reconstruye la muestra, el emparejamiento y la base con un inicio ficticio 28 días antes. En Días 0–1 estima -0,023 en logaritmos, con intervalo de [-0,087; 0,040], agrupado por estado y fecha. No reproduce una caída inmediata comparable, pero no prueba causalidad ni una diferencia formal entre coeficientes.

En periodos posteriores del placebo, algunos intervalos estatales excluyen cero, aunque los agrupados por estado y fecha lo incluyen. El ejercicio no descarta todos los cambios previos; el apéndice B presenta los contrastes completos.

### Persistencia y sensibilidades.

Las estimaciones logarítmicas son -0,018 en Días 2–6 y -0,041 en Sem. +1. Sus intervalos, agrupados por estado y fecha, incluyen cero; los efectos mínimos detectables, con una prueba bilateral al 5 % y potencia del 80 %, son 0,072 y 0,061, respectivamente. La menor magnitud estimada no prueba que el cambio desaparezca desde el Día 2. La señal de Sem. +1 depende de la agrupación y las exclusiones.

Con la semana inmediatamente anterior como base, y los mismos pares y pesos, Días 0–1 arroja -0,064 [-0,167; 0,039]. La menor magnitud y el intervalo que incluye cero muestran sensibilidad a la referencia. Los apéndices B y C detallan duración y bases alternativas.

### Calendario y controles.

Se excluyen inicios cuyo Día 0 o Día 1 coincide con feriados de la Ley Federal del Trabajo (LFT) o recesos de la Secretaría de Educación Pública (SEP), pues ambos pueden alterar la circulación (Cámara de Diputados, 2025; Secretaría de Educación de Veracruz, 2026).

La muestra se reduce de 77 a 25 pares tratados y de 32 a 15 fechas. La estimación logarítmica inmediata es -0,123 [-0,258; 0,011], con agrupación por estado y fecha. El intervalo incluye cero y cambia la composición de la muestra; la diferencia no se atribuye solo al calendario ni solo al menor tamaño. El apéndice C presenta las fechas y las exclusiones adicionales.


## 5. Conclusión y validez externa

Se documenta una reducción relativa inmediata de accidentes registrados: -0,107 en $\log(1+Y)$ durante los Días 0–1, con intervalo del 95 % de [-0,195; -0,019], agrupado por estado y fecha. El ajuste por covariables cambia poco la estimación; el placebo no reproduce una caída comparable. Después, las estimaciones son menores e inciertas, sin una fecha precisa de desaparición. El patrón es compatible con menos circulación, cambios al conducir o alteraciones de la captación; no identifica cada mecanismo ni demuestra menor riesgo por viaje.

El resultado promedia 77 pares municipio–episodio documentados en 2019–2025, con igual peso por tratado y registros de vías no federales. No representa cada ataque ni se extrapola automáticamente a otros incidentes o territorios. Las diferencias previas, la sensibilidad de la inferencia y la cobertura desigual del catálogo limitan la atribución causal. Para las autoridades, una caída de registros requiere contrastar movilidad, atención de emergencias y captación antes de interpretarla como una mejora de seguridad.

## Referencias

Amapola Periodismo. (2024, 8 de febrero). *Chilpancingo: tres días de parálisis por la violencia*. <https://amapolaperiodismo.com/2024/02/08/chilpancingo-tres-dias-de-paralisis-por-la-violencia/>

Bauernschuster, S., & Rekers, R. (2022). Speed limit enforcement and road safety. *Journal of Public Economics*, *210*, Artículo 104663. <https://doi.org/10.1016/j.jpubeco.2022.104663>

Cámara de Diputados. (2025). *Ley Federal del Trabajo, artículo 74*. <https://www.ordenjuridico.gob.mx/Documentos/Federal/html/wo125151.html>

Consejo Nacional de Población. (2024). *Reconstrucción y proyecciones de la población de los municipios de México, 1990–2040*. <https://conapo.segob.gob.mx/work/models/CONAPO/pry23/DBMun/00_Republica_mexicana.zip>

Dell, M. (2015). Trafficking networks and the Mexican Drug War. *American Economic Review*, *105*(6), 1738–1779. <https://doi.org/10.1257/aer.20121637>

Dube, A., Girardi, D., Jordà, Ò., & Taylor, A. M. (2025). A local projections approach to difference-in-differences. *Journal of Applied Econometrics*, *40*(7), 741–758. <https://doi.org/10.1002/jae.70000>

Instituto Nacional de Estadística y Geografía. (2015). *Encuesta Intercensal 2015: tabulados de población y vivienda*. <https://www.inegi.org.mx/programas/intercensal/2015/>

Instituto Nacional de Estadística y Geografía. (2021). *Censo de Población y Vivienda 2020: principales resultados por localidad (ITER)*. <https://www.inegi.org.mx/programas/ccpv/2020/>

Instituto Nacional de Estadística y Geografía. (2025a). *Estadística de Accidentes de Tránsito Terrestre en Zonas Urbanas y Suburbanas, diccionario de datos*. <https://inegi.org.mx/rnm/index.php/catalog/1115/data-dictionary/F1>

Instituto Nacional de Estadística y Geografía. (2025b). *Sistema Automatizado de Información Censal (SAIC)*. <https://www.inegi.org.mx/app/saic/>

Instituto Nacional de Estadística y Geografía. (2026a). *Accidentes de Tránsito Terrestre en Zonas Urbanas y Suburbanas*. <https://www.inegi.org.mx/programas/accidentes/>

Instituto Nacional de Estadística y Geografía. (2026b). *Catálogo Único de Claves de Áreas Geoestadísticas Estatales, Municipales y Localidades*. <https://www.inegi.org.mx/app/ageeml/>

Instituto Nacional de Estadística y Geografía. (2026c). *Vehículos de Motor Registrados en Circulación (VMRC)*. <https://www.inegi.org.mx/programas/vehiculosmotor/>

MacKinnon, J. G., Nielsen, M. Ø., & Webb, M. D. (2023a). Cluster-robust inference: A guide to empirical practice. *Journal of Econometrics*, *232*(2), 272–299. <https://doi.org/10.1016/j.jeconom.2022.04.001>

MacKinnon, J. G., Nielsen, M. Ø., & Webb, M. D. (2023b). Fast and reliable jackknife and bootstrap methods for cluster-robust inference. *Journal of Applied Econometrics*, *38*(5), 671–694. <https://doi.org/10.1002/jae.2969>

Roth, J. (2022). Pretest with caution: Event-study estimates after testing for parallel trends. *American Economic Review: Insights*, *4*(3), 305–322. <https://doi.org/10.1257/aeri.20210236>

Secretaría de Educación de Veracruz. (2026). *Calendarios escolares históricos de educación básica*. <https://www.sev.gob.mx/educacion-basica/calendario-escolar/>

## Apéndice A. Fuentes y especificaciones progresivas

### Regresiones complementarias en niveles.

**Panel B del cuadro 2. Resultado: cambio en el número de accidentes registrados**

| Variable / estadístico | $M_0$ | $M_1$ | $M_2$ | $M_3$ |
|:---|---:|---:|---:|---:|
| Tratamiento | -0,397<br>(0,230)<br>[-0,865; 0,072]<br>$p=0{,}094$ | -0,381<br>(0,230)<br>[-0,849; 0,087]<br>$p=0{,}107$ | -0,383<br>(0,236)<br>[-0,864; 0,097]<br>$p=0{,}114$ | -0,401<br>(0,241)<br>[-0,893; 0,090]<br>$p=0{,}106$ |
| Logaritmo de la población | — | -0,193<br>(0,106)<br>[-0,410; 0,024]<br>$p=0{,}079$ | -0,207<br>(0,129)<br>[-0,470; 0,056]<br>$p=0{,}119$ | -0,194<br>(0,121)<br>[-0,441; 0,053]<br>$p=0{,}119$ |
| Empleo por cada mil habitantes | — | — | 0,000327<br>(0,001345)<br>[-0,002416; 0,003071]<br>$p=0{,}809$ | 0,000656<br>(0,001396)<br>[-0,002191; 0,003503]<br>$p=0{,}642$ |
| Automóviles por cada mil habitantes | — | — | — | -0,001195<br>(0,001017)<br>[-0,003268; 0,000878]<br>$p=0{,}249$ |
| $R^2$ ponderado | 0,180 | 0,191 | 0,191 | 0,194 |
| $R^2$ tras descontar las fechas | 0,017 | 0,030 | 0,030 | 0,033 |

Cada celda presenta la estimación, el error estándar entre paréntesis, el intervalo de confianza del 95 % entre corchetes y el valor $p$ bilateral. La agrupación por estado y fecha utiliza 31 grados de libertad. Los cuatro modelos utilizan 3 613 observaciones municipio–fecha, 77 pares tratados y 32 fechas de inicio, e incluyen efectos fijos de fecha. Los pesos y la base previa son los mismos del Panel A.

Las dos medidas de $R^2$ del cuadro 2 y su Panel B resumen el ajuste de la regresión. La primera incluye los efectos fijos de fecha; la segunda mide el ajuste adicional del tratamiento y las covariables después de descontar las medias ponderadas de cada fecha. Ambas se calculan como $R^2=1-\mathrm{SCE}/\mathrm{SCT}$. La suma de cuadrados del error (SCE) utiliza residuos y pesos. La suma de cuadrados total (SCT) utiliza desviaciones respecto a la media ponderada general en la primera medida y respecto a las medias ponderadas de fecha en la segunda. Un $R^2$ mayor no demuestra validez causal.

### Detalles de medición y emparejamiento.

Colima requiere una precaución adicional: los automóviles de la serie etiquetada como 2023 tienen fecha de medición del 30 de abril de 2024 y usan población de 2024 como denominador. El valor solo es utilizable cuando tanto esa medición como la fecha del denominador, el 1 de julio de 2024, preceden a $t-28$. Los ceros, los valores confidenciales, los faltantes y las incompatibilidades territoriales se distinguen antes de elegir los controles.

En Morelia, Michoacán, para el inicio del 23 de abril de 2025 se seleccionan doce municipios de control. La cantidad resulta de los filtros de comparabilidad y no se fija de antemano. El nivel previo de accidentes registrados de cada candidato se compara con el nivel del municipio tratado.

### Fuentes y selección de la muestra.

**Cuadro A1.** Uniones antes del emparejamiento

| Fuente    |       Rol | Unidas / elegibles |     % | Valor utilizable / elegibles |
|:----------|----------:|-------------------:|------:|-----------------------------:|
| EIC 2015  |  Tratados |                7/7 | 100,0 |                          7/7 |
| ITER 2020 |  Tratados |              75/77 |  97,4 |                        75/77 |
| EIC 2015  | Controles |        3 411/3 453 |  98,8 |                  3 411/3 453 |
| ITER 2020 | Controles |      20 814/20 981 |  99,2 |                20 814/20 981 |
| SAIC      |  Tratados |              82/84 |  97,6 |                        82/84 |
| SAIC      | Controles |      24 230/24 434 |  99,2 |                24 139/24 434 |
| VMRC      |  Tratados |              82/84 |  97,6 |                        82/84 |
| VMRC      | Controles |      24 092/24 434 |  98,6 |                24 002/24 434 |

El universo son pares elegibles antes de exigir valores completos. Unión no equivale a valor utilizable. CONAPO corresponde al año del numerador. AGEEML es un inventario de cambios: no tener fila no es fallo de unión; se evalúa estabilidad territorial entre fechas.

**Cuadro A2.** Uniones auxiliares y territorio

| Operación | Numerador / denominador | % | Universo |
|:---|---:|---:|---:|
| CONAPO en SAIC | 3 613/3 613 | 100,0 | Pares de la muestra final |
| CONAPO en VMRC | 3 613/3 613 | 100,0 | Pares de la muestra final |
| AGEEML: perímetro estable | 106 554/106 554 | 100,0 | Municipio-fechas candidatos |

**Cuadro A3.** Pérdidas de tratados hasta la muestra principal

| Paso, orden jerárquico              | Trat. restantes | Trat. excluidos |
|:------------------------------------|----------------:|----------------:|
| Candidatos del catálogo             |             108 |               — |
| Sin historia de cobertura           |              94 |              14 |
| Exposición previa, tras cobertura   |              84 |              10 |
| Territorio, tras filtros anteriores |              84 |               0 |
| Covariables faltantes               |              82 |               2 |
| Controles completos insuficientes   |              82 |               0 |
| Calibre individual sin soporte      |              82 |               0 |
| Población sin soporte               |              78 |               4 |
| Empleo sin soporte                  |              77 |               1 |
| Autos sin soporte                   |              77 |               0 |

Cada fila cuenta pérdidas después de los filtros anteriores. Un fallo de soporte significa menos de diez candidatos o menos de cinco estados. La elegibilidad se construye hasta $t-1$; el soporte usa sólo covariables y niveles previos. Las exclusiones de persistencia se contabilizan aparte y no seleccionan el efecto inmediato principal. Los faltantes de covariables no se convierten en cero.

**Cuadro A4.** Días 0–1: $M_0$–$M_3$, muestra fija

| Controles | Modelo | Trat. | $N$ | $\log(1+Y)$, IC: estado y fecha | Niveles, IC: estado y fecha |
|:---|---:|---:|---:|---:|---:|
| Completos, calibre | Base ($M_0$) | 82 | 13 977 | -0,099 [-0,186; -0,012] | -0,426 [-0,893; 0,041] |
| Completos, calibre | $M_1$: + población | 82 | 13 977 | -0,097 [-0,182; -0,013] | -0,360 [-0,825; 0,104] |
| Completos, calibre | $M_2$: + empleo | 82 | 13 977 | -0,097 [-0,181; -0,012] | -0,362 [-0,816; 0,092] |
| Completos, calibre | $M_3$: + automóviles | 82 | 13 977 | -0,097 [-0,187; -0,007] | -0,379 [-0,851; 0,092] |
| Sin emparejar | Base ($M_0$) | 77 | 22 561 | -0,118 [-0,211; -0,025] | -0,458 [-0,921; 0,005] |
| Sin emparejar | $M_1$: + población | 77 | 22 561 | -0,095 [-0,173; -0,018] | -0,320 [-0,647; 0,006] |
| Sin emparejar | $M_2$: + empleo | 77 | 22 561 | -0,095 [-0,174; -0,017] | -0,320 [-0,648; 0,008] |
| Sin emparejar | $M_3$: + automóviles | 77 | 22 561 | -0,099 [-0,182; -0,015] | -0,343 [-0,697; 0,012] |
| 1:muchos | Base ($M_0$) | 77 | 3 613 | -0,107 [-0,195; -0,019] | -0,397 [-0,865; 0,072] |
| 1:muchos | $M_1$: + población | 77 | 3 613 | -0,105 [-0,194; -0,017] | -0,381 [-0,849; 0,087] |
| 1:muchos | $M_2$: + empleo | 77 | 3 613 | -0,107 [-0,195; -0,018] | -0,383 [-0,864; 0,097] |
| 1:muchos | $M_3$: + automóviles | 77 | 3 613 | -0,108 [-0,200; -0,017] | -0,401 [-0,893; 0,090] |
| 1:1 | Base ($M_0$) | 77 | 154 | -0,102 [-0,224; 0,019] | -0,353 [-0,905; 0,199] |
| 1:1 | $M_1$: + población | 77 | 154 | -0,102 [-0,227; 0,022] | -0,354 [-0,925; 0,217] |
| 1:1 | $M_2$: + empleo | 77 | 154 | -0,103 [-0,229; 0,023] | -0,362 [-0,942; 0,219] |
| 1:1 | $M_3$: + automóviles | 77 | 154 | -0,104 [-0,232; 0,025] | -0,375 [-0,971; 0,222] |

$M_0$: tratamiento y fecha; $M_1$: añade log población; $M_2$: empleo/mil; $M_3$: autos/mil. La muestra completa exige covariables utilizables y calibre individual, sin los tres intervalos adicionales del emparejamiento; conserva todos los tratados con ese soporte. Cada progresión usa exactamente sus mismos pares y pesos. La referencia sin emparejamiento mantiene los mismos tratados y controles completos, con pesos uniformes por fecha. Los dos esquemas comparten tratados, no controles. Las DME del cuadro 1 usan una escala común fijada antes del emparejamiento.

**Cuadro A5.** DME con los mismos tratados antes y después del emparejamiento

| Variable           | Antes de emparejar | 1:muchos |    1:1 |
|:-------------------|-------------------:|---------:|-------:|
| Población          |              0,274 |    0,013 |  0,005 |
| Empleo / mil       |              0,269 |    0,070 |  0,027 |
| Autos / mil        |             -0,021 |   -0,082 | -0,023 |
| Accidentes previos |              0,175 |   -0,011 |  0,012 |

La referencia previa incluye controles con datos completos y ponderación uniforme dentro de cada fecha. Las columnas posteriores cambian los vínculos y pesos, con los mismos tratados. La escala de estandarización es común, fijada en la referencia con calibre individual; una DME pequeña no demuestra balance de variables omitidas ni paralelismo. En niveles y log las covariables son las mismas, por lo que no se duplican estas estadísticas de balance.

## Apéndice B. Contrastes principales, persistencia y placebo

**Cuadro B1.** Contrastes principales, emparejamiento 1:muchos

| Escala | Tramo | $\hat\beta$ (EE) | IC 95 %: estado y fecha | $\beta/\sigma$ | MDE: estado y fecha |
|:---|---:|---:|---:|---:|---:|
| $\log(1+Y)$ | Día 0 | -0,116 (0,032) | [-0,251; 0,019] | -0,141 | 0,192 |
| $\log(1+Y)$ | Día 1 | -0,098 (0,026) | [-0,193; -0,003] | -0,119 | 0,135 |
| $\log(1+Y)$ | Días 0–1 | -0,107 (0,022) | [-0,195; -0,019] | -0,130 | 0,125 |
| $\log(1+Y)$ | Días 2–6 | -0,018 (0,015) | [-0,069; 0,032] | -0,022 | 0,072 |
| $\log(1+Y)$ | Sem. +1 | -0,041 (0,010) | [-0,084; 0,002] | -0,049 | 0,061 |
| Niveles | Día 0 | -0,306 (0,172) | [-1,006; 0,393] | -0,083 | 0,992 |
| Niveles | Día 1 | -0,487 (0,135) | [-0,911; -0,062] | -0,132 | 0,602 |
| Niveles | Días 0–1 | -0,397 (0,128) | [-0,865; 0,072] | -0,108 | 0,664 |
| Niveles | Días 2–6 | -0,126 (0,058) | [-0,336; 0,085] | -0,034 | 0,298 |
| Niveles | Sem. +1 | -0,079 (0,057) | [-0,317; 0,158] | -0,022 | 0,336 |

Los errores estándar (EE), entre paréntesis, se agrupan por estado. Los intervalos de confianza (IC) del 95 % se agrupan por estado y fecha; por eso no se calculan a partir de los EE entre paréntesis. El modelo $M_0$ utiliza 3 613 pares municipio–fecha. Los tramos son promedios diarios. La columna $\beta/\sigma$ divide el coeficiente por la desviación estándar diaria del resultado en $[-28,-8]$, calculada con divisor $n-1$; en niveles, esa desviación es de 3,68. El efecto mínimo detectable (MDE) se explica en el apéndice D.

**Cuadro B2.** Log: selección y horizontes, IC: estado y fecha

| Selección | Matching | Trat. | Días 0–1 | Días 2–6 | Sem. +1 |
|:---|---:|---:|---:|---:|---:|
| Principal | 1:muchos | 77 | -0,107 [-0,195; -0,019] | -0,018 [-0,069; 0,032] | -0,041 [-0,084; 0,002] |
| Principal | 1:1 | 77 | -0,102 [-0,224; 0,019] | -0,027 [-0,104; 0,050] | -0,084 [-0,168; 0,000] |
| Aislamiento posterior | 1:muchos | 69 | -0,124 [-0,220; -0,029] | -0,010 [-0,064; 0,044] | -0,045 [-0,092; 0,003] |
| Aislamiento posterior | 1:1 | 69 | -0,104 [-0,241; 0,033] | -0,024 [-0,107; 0,058] | -0,093 [-0,178; -0,008] |
| Placebo 28 días antes | 1:muchos | 81 | -0,023 [-0,087; 0,040] | -0,025 [-0,063; 0,012] | 0,010 [-0,025; 0,044] |
| Placebo 28 días antes | 1:1 | 81 | -0,059 [-0,153; 0,035] | -0,030 [-0,110; 0,051] | 0,008 [-0,055; 0,071] |

La muestra con aislamiento posterior exige cobertura $[-28,+13]$ y ausencia de otra exposición hasta +14. Sus diferencias incorporan selección posterior. El placebo reconstruye la muestra en $t-28$; sus tamaños no tienen que coincidir con los reales.

**Cuadro B3.** Placebo 28 días antes: efectos por periodo

| Escala | Horizonte | 1:muchos, IC: estado y fecha | $p_E$ | 1:1, IC: estado y fecha | $p_E$ |
|:---|---:|---:|---:|---:|---:|
| Log | Día 0 | -0,041 [-0,138; 0,056] | 0,248 | -0,078 [-0,225; 0,069] | 0,219 |
| Log | Día 1 | -0,006 [-0,110; 0,098] | 0,823 | -0,040 [-0,198; 0,118] | 0,473 |
| Log | Días 0–1 | -0,023 [-0,087; 0,040] | 0,333 | -0,059 [-0,153; 0,035] | 0,110 |
| Log | Días 2–6 | -0,025 [-0,063; 0,012] | 0,048 | -0,030 [-0,110; 0,051] | 0,365 |
| Log | Sem. 0 | -0,025 [-0,059; 0,010] | 0,068 | -0,038 [-0,098; 0,022] | 0,137 |
| Log | Sem. +1 | 0,010 [-0,025; 0,044] | 0,160 | 0,008 [-0,055; 0,071] | 0,752 |
| Niveles | Día 0 | -0,262 [-0,746; 0,222] | 0,097 | -0,395 [-1,132; 0,342] | 0,221 |
| Niveles | Día 1 | -0,023 [-0,423; 0,377] | 0,846 | -0,354 [-1,064; 0,357] | 0,238 |
| Niveles | Días 0–1 | -0,142 [-0,497; 0,212] | 0,226 | -0,374 [-0,944; 0,195] | 0,139 |
| Niveles | Días 2–6 | -0,156 [-0,364; 0,052] | 0,029 | -0,178 [-0,543; 0,187] | 0,233 |
| Niveles | Sem. 0 | -0,152 [-0,328; 0,023] | 0,022 | -0,234 [-0,509; 0,041] | 0,061 |
| Niveles | Sem. +1 | -0,032 [-0,148; 0,085] | 0,397 | -0,059 [-0,282; 0,164] | 0,584 |

$p_E$ corresponde a CRV1 estatal; los intervalos se agrupan por estado y fecha. Los rechazos estatales en tramos posteriores impiden describir todos los placebos como ceros limpios. Se exportan inicio real, índice ficticio, resultado y las tres fechas de base en `data/outputs/modelos/causal_fechas_base.csv`. También se publican días individuales -7 a -1 y 0 a 13 y la sensibilidad con base semana -1 en exactamente la misma muestra final. Los diagnósticos y las referencias alternativas se presentan sin seleccionar sus resultados según la significancia.

## Apéndice C. Sensibilidades y calendario

**Cuadro C1.** Días 0–1: exclusiones, IC: estado y fecha

| Exclusión / muestra | Matching | Trat. | Fechas | Log, IC: estado y fecha | Niveles, IC: estado y fecha |
|:---|---:|---:|---:|---:|---:|
| Principal | 1:muchos | 77 | 32 | -0,107 [-0,195; -0,019] | -0,397 [-0,865; 0,072] |
| Principal | 1:1 | 77 | 32 | -0,102 [-0,224; 0,019] | -0,353 [-0,905; 0,199] |
| Cinco fechas de auditoría | 1:muchos | 56 | 27 | -0,128 [-0,217; -0,039] | -0,504 [-0,875; -0,133] |
| Cinco fechas de auditoría | 1:1 | 56 | 27 | -0,136 [-0,283; 0,010] | -0,551 [-0,968; -0,134] |
| Sin feriados LFT | 1:muchos | 73 | 30 | -0,121 [-0,216; -0,026] | -0,486 [-0,988; 0,016] |
| Sin feriados LFT | 1:1 | 73 | 30 | -0,099 [-0,227; 0,029] | -0,340 [-0,921; 0,241] |
| Sin LFT ni recesos SEP | 1:muchos | 25 | 15 | -0,123 [-0,258; 0,011] | -0,585 [-1,160; -0,011] |
| Sin LFT ni recesos SEP | 1:1 | 25 | 15 | -0,123 [-0,404; 0,158] | -0,607 [-1,394; 0,181] |
| Sin dos tratados pendientes | 1:muchos | 75 | 32 | -0,109 [-0,199; -0,018] | -0,405 [-0,882; 0,071] |
| Sin dos tratados pendientes | 1:1 | 75 | 32 | -0,103 [-0,229; 0,022] | -0,360 [-0,925; 0,205] |
| Sin cuatro casos pendientes | 1:muchos | 74 | 32 | -0,108 [-0,200; -0,017] | -0,407 [-0,890; 0,075] |
| Sin cuatro casos pendientes | 1:1 | 74 | 32 | -0,099 [-0,225; 0,028] | -0,356 [-0,927; 0,216] |
| Sin dos señales en controles | 1:muchos | 77 | 32 | -0,107 [-0,196; -0,019] | -0,397 [-0,865; 0,071] |
| Sin dos señales en controles | 1:1 | 77 | 32 | -0,100 [-0,223; 0,023] | -0,344 [-0,901; 0,213] |

Las cinco fechas son 31/12/2019, 05/01/2023, 09/04/2023, 07/01/2024 y 23/04/2025. La regla amplia se aplica al día 0 o 1 sin eliminar automáticamente domingos. Se distinguen vacaciones, talleres, suspensiones y receso extraordinario de 2020; no se llama vacaciones a toda la educación a distancia.

Se excluyen por separado dos municipios de Michoacán: Chilchota (14/07/2021) y Contepec (23/04/2025). Se añade excluir los cuatro casos pendientes: también Huaniqueo, Michoacán (23/04/2025), y San Fernando, Tamaulipas (30/04/2023). San Fernando entra en la muestra principal; Huaniqueo sigue fuera por elegibilidad previa. Las señales son Centro, Tabasco (01–02/04/2025), y Coatzacoalcos, Veracruz (20/08/2022). Se elimina su contribución si intersecta $[t-49,t+14]$ y se reconstruyen emparejamiento y pesos. Coatzacoalcos ocurrió después del 09/08/2022: es una sensibilidad ex post explícita, no un filtro del principal. El cotejo anterior cubrió 27 pares de cuatro fechas. ACLED devolvió HTTP 403: no existe verificación exhaustiva y una búsqueda sin señal no demuestra ausencia.

**Cuadro C2.** Soporte de los escenarios

| Escenario                    |   Matching | Trat. | Cont. | Fechas | Episodios |
|:-----------------------------|---------:|------:|------:|-------:|----------:|
| Principal                    | 1:muchos |    77 | 3 536 |     32 |        31 |
| Principal                    |      1:1 |    77 |    77 |     32 |        31 |
| Aislamiento posterior        | 1:muchos |    69 | 3 038 |     30 |        29 |
| Aislamiento posterior        |      1:1 |    69 |    69 |     30 |        29 |
| Placebo 28 días antes        | 1:muchos |    81 | 3 838 |     38 |        37 |
| Placebo 28 días antes        |      1:1 |    81 |    81 |     38 |        37 |
| Cinco fechas de auditoría    | 1:muchos |    56 | 2 842 |     27 |        26 |
| Cinco fechas de auditoría    |      1:1 |    56 |    56 |     27 |        26 |
| Sin feriados LFT             | 1:muchos |    73 | 3 320 |     30 |        29 |
| Sin feriados LFT             |      1:1 |    73 |    73 |     30 |        29 |
| Sin LFT ni recesos SEP       | 1:muchos |    25 | 1 314 |     15 |        15 |
| Sin LFT ni recesos SEP       |      1:1 |    25 |    25 |     15 |        15 |
| Sin dos tratados pendientes  | 1:muchos |    75 | 3 457 |     32 |        31 |
| Sin dos tratados pendientes  |      1:1 |    75 |    75 |     32 |        31 |
| Sin cuatro casos pendientes  | 1:muchos |    74 | 3 283 |     32 |        31 |
| Sin cuatro casos pendientes  |      1:1 |    74 |    74 |     32 |        31 |
| Sin dos señales en controles | 1:muchos |    77 | 3 533 |     32 |        31 |
| Sin dos señales en controles |      1:1 |    77 |    77 |     32 |        31 |

**Cuadro C3.** Cohortes finales y calendario oficial

| Inicio     | Trat. | LFT en días 0–1 | SEP en días 0–1 | Cinco fechas |
|:-----------|------:|----------------:|----------------:|-------------:|
| 2019-10-17 |     1 |              No |              No |           No |
| 2019-11-30 |     1 |              No |              No |           No |
| 2019-12-31 |     1 |              Sí |              Sí |           Sí |
| 2020-03-10 |     3 |              No |              No |           No |
| 2020-06-19 |     1 |              No |              Sí |           No |
| 2020-06-20 |     5 |              No |              Sí |           No |
| 2020-12-04 |     1 |              No |              No |           No |
| 2021-05-28 |     2 |              No |              No |           No |
| 2021-07-14 |     2 |              No |              Sí |           No |
| 2022-03-13 |     1 |              No |              No |           No |
| 2022-08-09 |     5 |              No |              Sí |           No |
| 2022-08-10 |     1 |              No |              Sí |           No |
| 2022-08-12 |     2 |              No |              Sí |           No |
| 2022-08-18 |     1 |              No |              Sí |           No |
| 2022-08-27 |     2 |              No |              Sí |           No |
| 2022-11-28 |     1 |              No |              No |           No |
| 2022-12-04 |     2 |              No |              No |           No |
| 2023-01-05 |     3 |              No |              Sí |           Sí |
| 2023-02-19 |     1 |              No |              No |           No |
| 2023-04-09 |     2 |              No |              Sí |           Sí |
| 2023-04-30 |     3 |              Sí |              No |           No |
| 2023-08-27 |     3 |              No |              Sí |           No |
| 2023-09-22 |     1 |              No |              No |           No |
| 2023-09-27 |     2 |              No |              No |           No |
| 2023-12-22 |     1 |              No |              Sí |           No |
| 2024-01-07 |     5 |              No |              Sí |           Sí |
| 2024-05-05 |     1 |              No |              No |           No |
| 2024-10-04 |     3 |              No |              No |           No |
| 2025-04-23 |    10 |              No |              Sí |           Sí |
| 2025-07-26 |     5 |              No |              Sí |           No |
| 2025-09-28 |     1 |              No |              No |           No |
| 2025-10-03 |     4 |              No |              No |           No |

El calendario es nacional de educación básica, con fines de semana contiguos hasta la reanudación. No representa cada institución o adaptación estatal. La LFT sigue el artículo 74, incluido el cambio presidencial de 2024. Ninguna cohorte estimada coincide en días 0–1 con una jornada electoral ordinaria.

### Sensibilidad a la base de comparación

El cuadro C4 mantiene exactamente los mismos pares municipio–fecha y pesos, y cambia únicamente la referencia previa. Compara el Día -2, la base principal de tres semanas del mismo día de la semana y la semana inmediatamente anterior. Las diferencias entre columnas permiten observar cuánto depende el resultado de esa elección.

**Cuadro C4.** Días 0–1 con idénticos pares y pesos: base e IC agrupados por estado y fecha

| Matching | Escala | Día -2 | Tres semanas | Sem. -1 |
|:---|---:|---:|---:|---:|
| 1:muchos | Log | 0,013 [-0,074; 0,100] | -0,107 [-0,195; -0,019] | -0,064 [-0,167; 0,039] |
| 1:muchos | Niveles | 0,185 [-0,296; 0,666] | -0,397 [-0,865; 0,072] | -0,191 [-0,725; 0,343] |
| 1:1 | Log | -0,004 [-0,146; 0,138] | -0,102 [-0,224; 0,019] | -0,039 [-0,136; 0,058] |
| 1:1 | Niveles | 0,299 [-0,395; 0,992] | -0,353 [-0,905; 0,199] | 0,015 [-0,597; 0,626] |

## Apéndice D. Inferencia y potencia

Los errores agrupados por estado utilizan una estimación de varianza robusta por grupos, identificada como CRV1. Su corrección por tamaño de muestra es $\frac{G}{G-1}\frac{N-1}{N-K}$, donde $G$ es el número de estados, $N$ el número de pares municipio–fecha y $K$ el número de parámetros, incluidos los efectos de fecha. Los intervalos utilizan $G-1$ grados de libertad. En la agrupación por estado y fecha se suman los componentes de estado y fecha y se resta su intersección; la corrección y los grados de libertad utilizan el menor número de grupos. Este cálculo no permite cualquier dependencia entre estados en fechas distintas. Las varianzas indefinidas se señalan sin producir intervalos.

La alternativa CRV3 omite cada estado por turno, mantiene los pesos de los casos restantes y vuelve a estimar los efectos de fecha. Si $\hat\beta$ es el coeficiente con la muestra completa y $\hat\beta_{-g}$ el coeficiente sin el estado $g$, su varianza es

$$
\widehat V_{\mathrm{CRV3}}=\frac{G-1}{G}\sum_{g=1}^{G}(\hat\beta_{-g}-\hat\beta)^2.
$$

El cálculo se centra en el coeficiente completo y difiere de una variante centrada en la media de las estimaciones por omisión (MacKinnon et al., 2023a, 2023b).

### Efecto mínimo detectable.

El efecto mínimo detectable (MDE) es la magnitud que la prueba detectaría con una probabilidad del 80 %, bajo los supuestos del cálculo. Se utiliza una prueba bilateral al 5 %, errores estándar fijos y una distribución $t$ no central. En niveles, los umbrales de la especificación principal del cuadro D1 equivalen al 18,0 % de la media previa con agrupación estatal y al 32,4 % con agrupación por estado y fecha; esa media es de 2,05 registros por municipio y día. Los umbrales en $\log(1+Y)$ no son porcentajes directos del promedio de accidentes. Estas medidas de potencia condicional no corrigen sesgo ni demuestran equivalencia con cero.

**Cuadro D1.** Días 0–1: agrupamiento, CRV3 y MDE

| Matching   |  Escala |   Inferencia |          Días 0–1, IC 95% |  gl |   MDE |
|:---------|--------:|-------------:|--------------------------:|----:|------:|
| 1:muchos |     Log | CRV1 estatal | -0,107 [-0,152; -0,062] |  31 | 0,064 |
| 1:muchos |     Log |   CRV1: estado y fecha | -0,107 [-0,195; -0,019] |  31 | 0,125 |
| 1:muchos |     Log | CRV3 estatal | -0,107 [-0,199; -0,015] |  31 | 0,130 |
| 1:muchos | Niveles | CRV1 estatal | -0,397 [-0,657; -0,136] |  31 | 0,370 |
| 1:muchos | Niveles |   CRV1: estado y fecha |  -0,397 [-0,865; 0,072] |  31 | 0,664 |
| 1:muchos | Niveles | CRV3 estatal |  -0,397 [-0,925; 0,132] |  31 | 0,749 |
| 1:1      |     Log | CRV1 estatal | -0,102 [-0,182; -0,023] |  27 | 0,113 |
| 1:1      |     Log |   CRV1: estado y fecha |  -0,102 [-0,224; 0,019] |  27 | 0,172 |
| 1:1      |     Log | CRV3 estatal |  -0,102 [-0,221; 0,017] |  27 | 0,169 |
| 1:1      | Niveles | CRV1 estatal |  -0,353 [-0,770; 0,065] |  27 | 0,591 |
| 1:1      | Niveles |   CRV1: estado y fecha |  -0,353 [-0,905; 0,199] |  27 | 0,781 |
| 1:1      | Niveles | CRV3 estatal |  -0,353 [-0,934; 0,229] |  27 | 0,823 |

**Cuadro D2.** Wald semanal de tres restricciones

| Matching   |  Escala | Agrupación |     F |            p | Rango | Condición |   Cálculo |
|:---------|--------:|-----------:|------:|-------------:|------:|----------:|----------:|
| 1:muchos |     Log |    Estatal | 8,841 | $<0{,}001$ |     3 |      21,6 | calculada |
| 1:muchos |     Log |      Estado y fecha | 2,189 |        0,109 |     3 |       8,0 | calculada |
| 1:muchos | Niveles |    Estatal | 3,238 |        0,035 |     3 |      11,2 | calculada |
| 1:muchos | Niveles |      Estado y fecha | 2,459 |        0,081 |     3 |      12,4 | calculada |
| 1:1      |     Log |    Estatal | 1,385 |        0,269 |     3 |       5,4 | calculada |
| 1:1      |     Log |      Estado y fecha | 1,340 |        0,282 |     3 |       6,6 | calculada |
| 1:1      | Niveles |    Estatal | 1,369 |        0,273 |     3 |      14,3 | calculada |
| 1:1      | Niveles |      Estado y fecha | 1,043 |        0,389 |     3 |      15,0 | calculada |

Se omite semana -2 y se contrastan -4, -3 y -1. Se informa singularidad o indefinición sin usar una inversa generalizada para fabricar $p$. CRV3 tampoco repara anticipación, selección o interferencia.

**Cuadro D3.** Omisión de estados, $M_0$ y 1:muchos

| Estado omitido      | Log, días 0–1 | Niveles, días 0–1 |
|:--------------------|--------------:|------------------:|
| Aguascalientes      |        -0,121 |            -0,371 |
| Baja California     |        -0,100 |            -0,383 |
| Baja California Sur |        -0,106 |            -0,389 |
| Campeche            |        -0,109 |            -0,401 |
| Coahuila            |        -0,106 |            -0,395 |
| Colima              |        -0,109 |            -0,395 |
| Chiapas             |        -0,105 |            -0,392 |
| Chihuahua           |        -0,107 |            -0,403 |
| Ciudad de México    |        -0,109 |            -0,404 |
| Durango             |        -0,106 |            -0,395 |
| Guanajuato          |        -0,106 |            -0,412 |
| Guerrero            |        -0,105 |            -0,382 |
| Hidalgo             |        -0,107 |            -0,397 |
| Jalisco             |        -0,108 |            -0,399 |
| Estado de México    |        -0,103 |            -0,367 |
| Michoacán           |        -0,134 |            -0,560 |
| Morelos             |        -0,104 |            -0,390 |
| Nayarit             |        -0,115 |            -0,409 |
| Nuevo León          |        -0,118 |            -0,440 |
| Oaxaca              |        -0,108 |            -0,395 |
| Puebla              |        -0,108 |            -0,400 |
| Querétaro           |        -0,106 |            -0,391 |
| Quintana Roo        |        -0,109 |            -0,413 |
| San Luis Potosí     |        -0,109 |            -0,406 |
| Sinaloa             |        -0,079 |            -0,206 |
| Sonora              |        -0,109 |            -0,420 |
| Tabasco             |        -0,102 |            -0,375 |
| Tamaulipas          |        -0,100 |            -0,419 |
| Tlaxcala            |        -0,107 |            -0,397 |
| Veracruz            |        -0,107 |            -0,392 |
| Yucatán             |        -0,106 |            -0,391 |
| Zacatecas           |        -0,101 |            -0,399 |

Las réplicas mantienen pesos originales y vuelven a absorber las fechas. No se fuerza igualdad de masas después de omitir un estado: renormalizar o repetir el emparejamiento sería otro estimador, no el CRV3 anunciado. Se exportan 1:1 y $M_1$–$M_3$.

## Apéndice E. Construcción del catálogo y reproducción

### Catálogo de ataques.

Las búsquedas originales cubrieron tres regiones (norte, occidente y centro, sur y oriente) y tres periodos (2019–2021, 2022–2023 y 2024–2025). Tres subagentes de IA registraron consultas, enlaces, fechas de publicación y consulta, lugares y evidencia; los cotejos entre agentes examinaron casos de regiones distintas. Se buscaron dos orígenes informativos independientes para corroborar municipio y fecha: republicar un mismo boletín no constituye otra fuente. Una jornada que cruza medianoche puede tener fechas municipales distintas. Las discrepancias y corroboraciones pendientes se conservan en el catálogo.

Se utilizó el modelo «Sol 6.2», con la configuración «xhigh» y el modo «fast». Las bitácoras documentan las búsquedas y los cotejos, pero no registran la configuración del modelo.

Los cotejos documentados corresponden a agentes de IA; no se presentan como una validación humana exhaustiva. La prensa puede omitir episodios y una búsqueda sin hallazgos no acredita ausencia de ataques en los controles. Esta asistencia se usó para construir el catálogo de exposición, no para generar registros de accidentes ni covariables municipales, que provienen de las fuentes oficiales descritas en la sección 2.

### Reproducción del análisis.

El paquete `src/choques/`, configuración y pruebas acompañan al escrito. `README.md` documenta Python 3.13.2, dependencias y compilador. ATUS y los cien originales municipales deben corresponder a sus manifiestos: una edición nueva en la misma URL no los sustituye. Las entradas son `data/inputs/episodios.csv` y `data/inputs/fuentes_eventos.csv`, reconstruidas desde las hojas de evidencia. Las rutas parten de la carpeta que contiene `repo/`, `data/` y `tasks/`.

La interfaz de comandos ejecuta `validar`, `todo` y `compilar`. `python reproducir.py` crea otra copia, verifica originales, reconstruye ocho etapas y exige igualdad SHA-256 de todos los productos y del PDF. Las pruebas unitarias y sintéticas cubren calibre heterogéneo, base limpia, log con ceros, invariancia al futuro, territorio, pesos e inferencia con reestimación de fechas. Los tiempos de ejecución se registran aparte de los resultados. El registro de verificación distingue la reproducción del análisis de las revisiones editoriales del PDF.

Los datos públicos se enlazan en la bibliografía y los manifiestos fijan sus ediciones. El apéndice H incluye el código R completo y los enlaces al repositorio y a la carpeta de entrega de datos.

## Apéndice F. Contexto geográfico de la muestra

**Figura 2.** Municipios tratados y controles de la muestra principal. Naranja: 54 municipios tratados; azul: 765 municipios de control. Un municipio puede aparecer en ambos grupos en fechas distintas: ocurre en 47 casos. El gris indica que no pertenece al grupo de ese panel. El color muestra participación, no tamaño del efecto ni peso estadístico.

![Municipios tratados y controles](figuras/mapa-municipios.png)

El mapa reúne las 32 fechas de inicio entre octubre de 2019 y octubre de 2025; los conteos únicos difieren de los 77 pares tratados y 3 536 pares de control municipio–fecha. Entre los lugares tratados están Culiacán, Sinaloa; Morelia, Michoacán; y Reynosa, Tamaulipas. Tijuana, Baja California, aparece en el grupo de control. La cartografía de referencia procede del Marco Geoestadístico del INEGI, diciembre de 2025, y del servicio del catálogo municipal. Sirve para ubicar los municipios; no reconstruye sus límites históricos ni representa riesgo por superficie. Se usa una proyección equirectangular con paralelo de referencia en 23 grados norte, sin calcular áreas o distancias.

## Apéndice G. Análisis exploratorio por horario y gravedad

El cuadro G1 compara, por gravedad, el cambio de accidentes registrados de noche con el de día en los Días 0–1 de la muestra principal. Se define el día de 06:00 a 17:59 y la noche de 18:00 a 05:59. Cada cifra resta dos cambios estimados, no los conteos nocturnos y diurnos. Un valor negativo indica una reducción relativa mayor de noche, o un aumento menor; uno positivo indica lo contrario.

En el emparejamiento 1:muchos, los tres intervalos de confianza incluyen cero. Ambos esquemas de matching tampoco muestran un patrón uniforme por gravedad. El ejercicio no permite atribuir la reducción agregada a una franja horaria ni a una conducta específica. Los registros con hora desconocida permanecen en el total. No se ajusta la inferencia por las comparaciones múltiples, por lo que los resultados son exploratorios.

**Cuadro G1.** Días 0–1: noche menos día por gravedad

| Gravedad    | 1:muchos: noche menos día |     1:1: noche menos día |
|:------------|--------------------------:|-------------------------:|
| Fatal       |  -0,024 [-0,055; 0,007] | -0,039 [-0,078; 0,000] |
| Con heridos |   0,089 [-0,019; 0,197] |  0,041 [-0,135; 0,217] |
| Solo daños  |  -0,051 [-0,256; 0,154] |  0,000 [-0,292; 0,292] |

Registros por municipio y día; IC del 95 % agrupados por estado y fecha.

## Apéndice H. Código reproducible en R

Se incluye el archivo completo `codigo_R/analisis.R`, idéntico al ejecutado para la verificación. La obtención y limpieza de los datos se realizan en Python; este archivo reconstruye el análisis estadístico a partir del paquete de datos limpios, sin leer coeficientes, muestras emparejadas ni pesos precalculados.

La ejecución en R reprodujo 22 productos de referencia con tolerancia absoluta de $10^{-6}$, incluidos muestras, pesos, coeficientes e inferencia. Las 18 tablas cotejadas coinciden a la precisión impresa. La diferencia máxima en efectos e inferencia fue de $1{,}4\times10^{-12}$. El registro de verificación se conserva en `reporte/verificacion/reproduccion-r.json`.

El archivo conserva salidas históricas adicionales, incluida la comparación semanal de Culiacán. Esos resultados no forman parte del análisis presentado en este reporte.

### Código, datos y ejecución.

Repositorio de código e instrucciones: <https://github.com/EduardoGC21/inferencia-causal>.

Carpeta de entrega de datos: <https://drive.google.com/drive/folders/19fPf9UVt5Vdm-h2LiM2sBdD9erg0qItu?usp=sharing>.

Para reproducir el análisis, descargar y descomprimir `datos_limpios_R.zip`, instalar los paquetes `data.table`, `R.utils` y `ggplot2`, y ejecutar desde la raíz del repositorio: `Rscript codigo_R/analisis.R RUTA/datos_limpios_R RUTA/resultados_R`. Las rutas se sustituyen por las carpetas de entrada y salida elegidas; las instrucciones también aparecen al inicio del código. La ejecución verificada utilizó R 4.6.1.

### Listado completo de `codigo_R/analisis.R`.

```r
# Violencia criminal y accidentes registrados, 2019-2025
# Código reproducible del análisis final y de las dos gráficas del reporte.
# Ingesta, clasificación y limpieza: Python. Análisis estadístico: este archivo.
# No necesita Python ni lee coeficientes, muestras o pesos precalculados.
#
# 1. Descomprime datos_limpios_R.zip (el paquete para compartir por Drive).
# 2. Instala una vez: install.packages(c("data.table", "R.utils", "ggplot2"))
# 3. Desde la raíz del repositorio:
#    Rscript codigo_R/analisis.R RUTA/datos_limpios_R RUTA/resultados_R
# También puedes cambiar las dos rutas siguientes y ejecutar todo desde RStudio.
# Las salidas siempre van a la carpeta indicada; no modifica reporte/ ni Python.
# Verificado con R 4.6.1, data.table 1.18.4 y ggplot2 4.0.3.

# 1. Rutas, paquetes y parámetros -------------------------------------------

carpeta_datos <- "datos_limpios_R"
carpeta_salida <- "resultados_R"
argumentos <- commandArgs(trailingOnly = TRUE)
if (length(argumentos) >= 1) carpeta_datos <- argumentos[1]
if (length(argumentos) >= 2) carpeta_salida <- argumentos[2]

library(data.table)
library(ggplot2)
setDTthreads(1)
options(digits = 10, scipen = 999)
if (.Platform$OS.type == "windows") {
  Sys.setlocale("LC_CTYPE", "Spanish_Mexico.UTF-8")
}
stopifnot(dir.exists(carpeta_datos))
for (subcarpeta in c("modelos", "tablas", "figuras")) {
  dir.create(file.path(carpeta_salida, subcarpeta), recursive = TRUE,
             showWarnings = FALSE)
}

alpha <- 0.05
potencia <- 0.80
min_controles <- 10
min_estados <- 5
covariables <- c("poblacion", "empleo_mil", "autos_mil")
columnas_modelo <- c("tratado", "log_poblacion", "empleo_mil", "autos_mil")
cinco_fechas <- as.Date(c("2019-12-31", "2023-01-05", "2023-04-09",
                         "2024-01-07", "2025-04-23"))
tramos <- c(setNames(lapply(-7:13, identity), as.character(-7:13)),
            list(d0 = 0, d1 = 1, "d0..1" = 0:1, "d2..6" = 2:6,
                 wk0 = 0:6, "wk+1" = 7:13, "wk-1" = -7:-1))

guardar <- function(datos, nombre, tipo = "modelos") {
  fwrite(datos, file.path(carpeta_salida, tipo, paste0(nombre, ".csv")),
         na = "", logical01 = FALSE)
}
leer <- function(nombre) {
  archivo <- file.path(carpeta_datos, paste0(nombre, ".csv"))
  if (!file.exists(archivo)) archivo <- paste0(archivo, ".gz")
  conexion <- if (grepl("\\.gz$", archivo)) gzfile(archivo, "rt") else file(archivo, "rt")
  encabezado <- strsplit(readLines(conexion, n = 1), ",", fixed = TRUE)[[1]]
  close(conexion)
  datos <- fread(archivo, na.strings = c("NA", ""),
                 colClasses = list(character = intersect(encabezado,
                                                          c("clave", "cve_ent", "origen", "destino"))),
                 showProgress = FALSE, data.table = FALSE)
  for (campo in intersect(c("fecha", "inicio", "fin"), names(datos))) {
    datos[[campo]] <- as.Date(datos[[campo]])
  }
  datos
}
unir_filas <- function(lista) as.data.frame(rbindlist(lista, fill = TRUE))

# 2. Datos ya limpios ------------------------------------------------------
# La tabla de continuidad conserva NA. El conteo publicado, otro resultado,
# cuenta cero filas cuando no existe un registro en conteos_diarios.

cat("Lectura de los datos limpios\n")
panel <- leer("panel_diario")
claves <- sort(unique(panel$clave))
fechas <- sort(unique(panel$fecha))
estados <- substr(claves, 1, 2)
posicion <- cbind(match(panel$clave, claves), match(panel$fecha, fechas))
valores_panel <- matrix(NA_real_, length(claves), length(fechas))
continuidad <- matrix(FALSE, length(claves), length(fechas))
valores_panel[posicion] <- panel$accidentes
continuidad[posicion] <- panel$continuidad
rm(panel, posicion)

conteos <- as.data.table(leer("conteos_diarios"))
setkey(conteos, clave, fecha)
publicados <- matrix(0, length(claves), length(fechas))
posicion <- cbind(match(conteos$clave, claves), match(conteos$fecha, fechas))
publicados[posicion] <- conteos$dia + conteos$noche + conteos$hora_desconocida
rm(posicion)
stopifnot(sum(publicados) == sum(conteos$dia + conteos$noche + conteos$hora_desconocida))

eventos <- leer("exposiciones")
eventos$clave[is.na(eventos$clave)] <- ""
activos <- eventos[!is.na(eventos$inicio), ]
activos$hasta <- activos$fin
activos$hasta[is.na(activos$hasta)] <- activos$inicio[is.na(activos$hasta)]
abiertos <- activos$clase_final == "persistente" & is.na(activos$fin)
activos$hasta[abiertos] <- as.Date("2262-04-11")
focales <- activos[activos$estado == "confirmado" & activos$clase_final == "extensa", ]
reportados <- leer("cobertura_mensual")
invalidos <- leer("fecha_invalida")
cambios <- leer("cambios_territoriales")
calendario_sep <- leer("calendario_escolar")
senales <- leer("cotejo_controles")
calidad <- leer("calidad")
tablas_municipales <- lapply(c("censo", "conapo", "saic", "vmrc"), leer)
names(tablas_municipales) <- c("censo", "conapo", "saic", "vmrc")
meses <- sort(unique(reportados$mes))
presencia <- matrix(FALSE, length(claves), length(meses))
ubicacion <- cbind(match(reportados$clave, claves), match(reportados$mes, meses))
presencia[ubicacion[!is.na(ubicacion[, 1]), , drop = FALSE]] <- TRUE
rm(reportados, ubicacion)

extraer <- function(muestra, h, matriz = publicados) {
  fila <- match(muestra$clave, claves)
  columna <- match(muestra$indice + h, fechas)
  stopifnot(!anyNA(fila), !anyNA(columna))
  matriz[cbind(fila, columna)]
}

# 3. Territorio y covariables medidas antes de t-28 -------------------------
# El código M divide municipios. En ATUS, Eldorado/Juan José Ríos entran el
# 1 de noviembre de 2024; se conserva la fecha administrativa como etiqueta.

territorios <- function(llaves, fecha, atus = FALSE) {
  resultado <- rep("inicial", length(llaves))
  divisiones <- cambios[cambios$codigo == "M", ]
  efectiva <- divisiones$fecha
  if (atus) {
    efectiva[divisiones$destino %in% c("25019", "25020")] <- as.Date("2024-11-01")
  }
  divisiones <- divisiones[efectiva <= fecha, ]
  if (nrow(divisiones)) {
    for (i in order(divisiones$fecha)) {
      afectada <- llaves %in% c(divisiones$origen[i], divisiones$destino[i])
      resultado[afectada] <- as.character(divisiones$fecha[i])
    }
  }
  resultado
}
elegir_corte <- function(fecha, cortes) {
  disponibles <- as.integer(names(cortes))[as.Date(cortes) < fecha - 28]
  if (length(disponibles)) max(disponibles) else NA_integer_
}
cortes_censo <- c("2015" = "2015-03-15", "2020" = "2020-03-15")
cortes_saic <- c("2018" = "2018-12-31", "2023" = "2023-12-31")
cortes_vmrc <- setNames(paste0(2018:2024, "-12-31"), 2018:2024)

unir_corte <- function(destino, fuente, campos, etiqueta, solo_estado = character()) {
  stopifnot(!anyDuplicated(fuente$clave))
  ubicacion <- match(destino$clave, fuente$clave)
  encontrada <- !is.na(ubicacion)
  compatible <- encontrada & destino$territorio == fuente$territorio[ubicacion]
  compatible[is.na(compatible)] <- FALSE
  estado_union <- ifelse(compatible, "unida",
                        ifelse(encontrada, "territorio_incompatible",
                               ifelse(substr(destino$clave, 1, 2) %in% solo_estado,
                                      "solo_entidad", "sin_clave")))
  for (campo in campos) {
    destino[[campo]] <- fuente[[campo]][ubicacion]
    destino[[campo]][!compatible] <- NA
  }
  destino[[paste0(etiqueta, "_union")]] <- estado_union
  destino
}

# Tasas por mil con denominadores anuales CONAPO y alternativa censal.
vmrc <- tablas_municipales$vmrc
es_municipal <- vmrc$vmrc_cobertura == "Municipal" &
  !substr(vmrc$clave, 3, 5) %in% c("000", "996", "998", "999")
agregados_vmrc <- vmrc[!es_municipal, ]
tablas_municipales$vmrc <- vmrc[es_municipal, ]
for (fuente in c("saic", "vmrc")) {
  tabla <- tablas_municipales[[fuente]]
  tabla$medicion <- as.Date(paste0(tabla$anio, "-12-31"))
  if (fuente == "vmrc") {
    colima <- substr(tabla$clave, 1, 2) == "06" & tabla$anio == 2023
    tabla$medicion[colima] <- as.Date("2024-04-30")
  }
  partes <- list()
  cierres <- sort(unique(tabla$medicion))
  for (i in seq_along(cierres)) {
    cierre <- cierres[i]
    filas <- tabla[tabla$medicion == cierre, ]
    anual <- tablas_municipales$conapo
    anual <- anual[anual$anio == as.integer(format(cierre, "%Y")), ]
    filas <- unir_corte(filas, anual, c("conapo", "conapo_origen"), "conapo")
    filas$anio_denominador <- as.integer(format(cierre, "%Y"))
    anio_censo <- max(as.integer(names(cortes_censo))[as.Date(cortes_censo) < cierre])
    censo <- tablas_municipales$censo
    censo <- censo[censo$anio == anio_censo, ]
    censo$poblacion_alt <- censo$poblacion
    filas <- unir_corte(filas, censo, "poblacion_alt", "censo_alt")
    filas$anio_censo_alt <- anio_censo
    filas$desfase_censo_dias <- as.numeric(cierre - as.Date(cortes_censo[as.character(anio_censo)]))
    partes[[i]] <- filas
  }
  tabla <- unir_filas(partes)
  numerador <- if (fuente == "saic") "empleo" else "autos"
  tasa <- paste0(numerador, "_mil")
  tabla[[tasa]] <- 1000 * tabla[[numerador]] / tabla$conapo
  tabla[[paste0(tasa, "_alt")]] <- 1000 * tabla[[numerador]] / tabla$poblacion_alt
  tabla[!tabla$perimetro_confirmado, c(tasa, paste0(tasa, "_alt"))] <- NA
  if (fuente == "saic") {
    tabla$vacb_pc_2023 <- tabla$vacb_millones_2023 * 1000000 / tabla$conapo
    tabla$vacb_pc_2023[!tabla$perimetro_confirmado] <- NA
  } else {
    names(tabla)[names(tabla) == "medicion"] <- "medicion_vmrc"
  }
  tablas_municipales[[fuente]] <- tabla
}

adjuntar_covariables <- function(muestra, persistencia = FALSE, auditada = FALSE) {
  campos_fuente <- list(
    censo = c("poblacion", "poblacion_estado", "auto_vivienda", "auto_vivienda_estado"),
    saic = c("empleo", "empleo_estado", "empleo_mil", "empleo_mil_alt",
             "vacb_pc_2023", "vacb_millones_estado"),
    vmrc = c("autos", "autos_estado", "autos_mil", "autos_mil_alt", "medicion_vmrc")
  )
  cortes <- list(censo = cortes_censo, saic = cortes_saic, vmrc = cortes_vmrc)
  partes <- list()
  indices <- sort(unique(muestra$indice))
  for (i in seq_along(indices)) {
    indice <- indices[i]
    cohorte <- muestra[muestra$indice == indice, ]
    fin <- indice + if (auditada) 16 else if (persistencia) 14 else -1
    inicio <- indice - 28
    cohorte$territorio <- territorios(cohorte$clave,
                                     if (!auditada && !persistencia) fin else indice, TRUE)
    cohorte$territorio_ventana <- territorios(cohorte$clave, inicio, TRUE) ==
      territorios(cohorte$clave, fin, TRUE)
    for (fuente in names(campos_fuente)) {
      anio <- elegir_corte(indice, cortes[[fuente]])
      campos <- campos_fuente[[fuente]]
      extras <- "perimetro_confirmado"
      if (fuente != "censo") {
        extras <- c(extras, "conapo", "conapo_union", "conapo_origen",
                    "anio_denominador", "poblacion_alt", "censo_alt_union",
                    "anio_censo_alt", "desfase_censo_dias")
      }
      tabla <- tablas_municipales[[fuente]]
      tabla <- tabla[tabla$anio == anio, ]
      names(tabla)[match(extras, names(tabla))] <- paste0(fuente, "_", extras)
      solo_estado <- character()
      if (fuente == "vmrc") {
        solo_estado <- setdiff(substr(agregados_vmrc$clave[agregados_vmrc$anio == anio], 1, 2),
                               substr(tabla$clave, 1, 2))
      }
      cohorte <- unir_corte(cohorte, tabla, c(campos, paste0(fuente, "_", extras)),
                            fuente, solo_estado)
      cohorte[[paste0("corte_", fuente)]] <- anio
      union <- paste0(fuente, "_union")
      cruzada <- cohorte[[union]] == "unida" & !cohorte$territorio_ventana
      cohorte[[union]][cruzada] <- "quiebre_en_ventana"
      sin_perimetro <- cohorte[[union]] == "unida" &
        !is.na(cohorte[[paste0(fuente, "_perimetro_confirmado")]]) &
        !cohorte[[paste0(fuente, "_perimetro_confirmado")]]
      cohorte[[union]][sin_perimetro] <- "perimetro_no_confirmado"
      cohorte[cruzada | sin_perimetro, campos] <- NA
    }
    mitad_anio <- as.Date(ifelse(is.na(cohorte$vmrc_anio_denominador), NA,
                                paste0(cohorte$vmrc_anio_denominador, "-07-01")))
    tardia <- cohorte$vmrc_union == "unida" &
      (cohorte$medicion_vmrc >= inicio | mitad_anio >= inicio)
    tardia[is.na(tardia)] <- FALSE
    cohorte[tardia, c("autos_mil", "autos_mil_alt")] <- NA
    cohorte$vmrc_union[tardia] <- "medicion_posterior"
    partes[[i]] <- cohorte
  }
  unir_filas(partes)
}

# 4. Elegibilidad previa, persistencia y placebo ---------------------------

cobertura_previa <- function(indice) {
  primer_dia <- as.Date(format(indice, "%Y-%m-01"))
  anteriores <- format(seq(primer_dia, by = "-1 month", length.out = 4)[-1], "%Y-%m")
  columnas <- match(anteriores, meses)
  vista <- if (anyNA(columnas)) rep(FALSE, length(claves)) else
    rowSums(presencia[, columnas, drop = FALSE]) == 3
  mes_valido <- !is.na(invalidos$mes) & invalidos$mes %in% 1:12
  mes_invalido <- sprintf("%04d-%02d", invalidos$anio, invalidos$mes)
  bloqueada <- invalidos$clave[mes_valido & mes_invalido %in% anteriores]
  desconocida <- !mes_valido & invalidos$anio < as.integer(format(indice, "%Y")) &
    invalidos$anio %in% as.integer(substr(anteriores, 1, 4))
  bloqueada <- c(bloqueada, invalidos$clave[desconocida])
  vista & !claves %in% bloqueada
}

seleccionar <- function(placebo = FALSE, persistencia = FALSE) {
  focal <- focales
  focal$indice <- focal$inicio - if (placebo) 28 else 0
  partes <- auditoria <- list()
  indices <- sort(unique(focal$indice))
  for (i in seq_along(indices)) {
    indice <- indices[i]
    cohorte <- focal[focal$indice == indice, ]
    stopifnot(!anyDuplicated(cohorte$clave))
    derecha <- indice + if (persistencia) 14 else -1
    local <- claves %in% cohorte$clave
    conocidos <- activos[activos$inicio <= derecha & activos$hasta >= indice - 49, ]
    bloqueada <- claves %in% conocidos$clave[conocidos$clave != ""] |
      estados %in% conocidos$cve_ent[conocidos$clave == ""]
    if (persistencia) {
      for (j in seq_len(nrow(cohorte))) {
        conflictos <- conocidos[conocidos$id_episodio != cohorte$id_episodio[j] |
                                   conocidos$inicio <= indice - 1, ]
        hit <- conflictos$clave == cohorte$clave[j] |
          (conflictos$clave == "" & conflictos$cve_ent == cohorte$cve_ent[j])
        lugar <- match(cohorte$clave[j], claves)
        if (!is.na(lugar)) bloqueada[lugar] <- any(hit, na.rm = TRUE)
      }
    }
    geografia <- estados %in% cohorte$cve_ent
    predicha <- cobertura_previa(indice)
    territorial <- territorios(claves, indice - 28, TRUE) == territorios(claves, derecha, TRUE)
    completa <- rep(TRUE, length(claves))
    if (persistencia) {
      ventana <- fechas >= indice - 28 & fechas <= indice + 13
      completa <- if (sum(ventana) == 42) rowSums(continuidad[, ventana, drop = FALSE] &
        is.finite(valores_panel[, ventana, drop = FALSE])) == 42 else rep(FALSE, length(claves))
    }
    calendario <- indice - 49 >= min(fechas) && indice + 13 <= max(fechas)
    elegible <- predicha & !bloqueada & territorial & completa & (local | !geografia) & calendario
    nivel <- rowMeans(publicados[, fechas >= indice - 28 & fechas <= indice - 15, drop = FALSE])
    auditoria[[i]] <- data.frame(clave = claves, indice, tratado = as.integer(local),
                                cobertura_predicha = predicha, exposicion_en_ventana = bloqueada,
                                territorio_compatible = territorial, cobertura_completa = completa,
                                estado_focal = geografia, elegible)
    if (!any(elegible & local)) next
    elegidas <- claves[elegible]
    episodio <- cohorte$id_episodio[match(elegidas, cohorte$clave)]
    episodio[is.na(episodio)] <- ""
    partes[[i]] <- data.frame(clave = elegidas, estado = estados[elegible], indice,
                             tratado = as.integer(local[elegible]), id_episodio = episodio,
                             peso = 1, pre_nivel = nivel[elegible])
  }
  list(muestra = unir_filas(partes), auditoria = unir_filas(auditoria))
}

# 5. Emparejamientos, soporte y pesos --------------------------------------
# Cada tratado requiere diez candidatos de cinco estados tras cada filtro.
# El calibre de accidentes usa +0.5. Las tres covariables usan [valor/2,2*valor].

soporte <- function(controles) nrow(controles) >= min_controles &&
  length(unique(controles$estado)) >= min_estados

comprobar_pesos <- function(muestra) {
  if (!nrow(muestra)) return(invisible(NULL))
  stopifnot(!anyDuplicated(muestra[c("indice", "clave")]), all(muestra$peso > 0))
  masas <- aggregate(peso ~ indice + tratado, muestra, sum)
  stopifnot(max(abs(masas$peso[masas$tratado == 1] - masas$peso[masas$tratado == 0])) < 0.000000001)
}

emparejar <- function(muestra, variables = covariables, individual = TRUE) {
  seleccionadas <- perdidas <- vinculos <- list()
  indices <- sort(unique(muestra$indice))
  for (i in seq_along(indices)) {
    indice <- indices[i]
    cohorte <- muestra[muestra$indice == indice, ]
    tratados <- cohorte[cohorte$tratado == 1, ]
    controles <- cohorte[cohorte$tratado == 0, ]
    completos <- controles[if (length(variables)) complete.cases(controles[variables]) else
                             rep(TRUE, nrow(controles)), ]
    pesos <- setNames(rep(0, nrow(controles)), controles$clave)
    retenidos <- character()
    for (j in seq_len(nrow(tratados))) {
      tratado <- tratados[j, ]
      faltantes <- variables[is.na(tratado[1, variables, drop = TRUE])]
      candidatos <- if (length(faltantes)) completos[FALSE, ] else completos
      motivo <- if (length(faltantes)) "faltantes_tratado" else ""
      if (motivo == "" && !soporte(candidatos)) motivo <- "datos_completos"
      conteo <- list()
      if (individual) {
        razon <- (candidatos$pre_nivel + 0.5) / (tratado$pre_nivel + 0.5)
        candidatos <- candidatos[razon >= 0.5 & razon <= 2, ]
        conteo$despues_pre_nivel <- nrow(candidatos)
        conteo$estados_despues_pre_nivel <- length(unique(candidatos$estado))
        if (motivo == "" && !soporte(candidatos)) motivo <- "pre_nivel"
      }
      for (variable in variables) {
        dentro <- candidatos[[variable]] >= tratado[[variable]] / 2 &
          candidatos[[variable]] <= tratado[[variable]] * 2
        dentro[is.na(dentro)] <- FALSE
        candidatos <- candidatos[dentro, ]
        conteo[[paste0("despues_", variable)]] <- nrow(candidatos)
        conteo[[paste0("estados_despues_", variable)]] <- length(unique(candidatos$estado))
        if (motivo == "" && !soporte(candidatos)) motivo <- variable
      }
      perdidas[[length(perdidas) + 1]] <- data.frame(
        indice, clave = tratado$clave, estado = tratado$estado, id_episodio = tratado$id_episodio,
        faltantes_tratado = paste(faltantes, collapse = ";"), controles_auditados = nrow(controles),
        controles_completos = nrow(completos), estados_completos = length(unique(completos$estado)),
        as.data.frame(conteo), motivo, incluida = motivo == "")
      if (motivo != "") next
      retenidos <- c(retenidos, tratado$clave)
      aporte <- 1 / nrow(candidatos)
      pesos[candidatos$clave] <- pesos[candidatos$clave] + aporte
      vinculos[[length(vinculos) + 1]] <- data.frame(
        indice, tratado_clave = tratado$clave, control_clave = candidatos$clave,
        contribucion = aporte)
    }
    if (length(retenidos)) {
      t <- tratados[tratados$clave %in% retenidos, ]
      t$peso <- 1
      c <- controles[pesos[controles$clave] > 0, ]
      c$peso <- unname(pesos[c$clave])
      seleccionadas[[i]] <- rbind(t, c)
    }
  }
  resultado <- unir_filas(seleccionadas)
  comprobar_pesos(resultado)
  list(muestra = resultado, perdidas = unir_filas(perdidas), vinculos = unir_filas(vinculos))
}

uno_a_uno <- function(muestra, vinculos) {
  identificador <- paste(muestra$indice, muestra$clave)
  t <- match(paste(vinculos$indice, vinculos$tratado_clave), identificador)
  c <- match(paste(vinculos$indice, vinculos$control_clave), identificador)
  vt <- as.matrix(muestra[t, covariables])
  vc <- as.matrix(muestra[c, covariables])
  razon <- vc / vt
  razon[vt == 0] <- 1
  vinculos$distancia_log2 <- sqrt(rowSums(log2(razon)^2))
  vinculos <- vinculos[order(vinculos$distancia_log2, vinculos$control_clave), ]
  elegidos <- vinculos[!duplicated(vinculos[c("indice", "tratado_clave")]), ]
  elegidos$contribucion <- 1
  pesos <- aggregate(contribucion ~ indice + control_clave, elegidos, sum)
  c <- muestra[match(paste(pesos$indice, pesos$control_clave), identificador), ]
  c$peso <- pesos$contribucion
  resultado <- rbind(muestra[muestra$tratado == 1, ], c)
  rownames(resultado) <- NULL
  comprobar_pesos(resultado)
  list(muestra = resultado, vinculos = elegidos)
}

mismos_tratados <- function(universo, emparejada) {
  partes <- list()
  t <- emparejada[emparejada$tratado == 1, ]
  indices <- sort(unique(t$indice))
  for (i in seq_along(indices)) {
    tratados <- t[t$indice == indices[i], ]
    c <- universo[universo$indice == indices[i] & universo$tratado == 0 &
                    complete.cases(universo[covariables]), ]
    tratados$peso <- 1
    c$peso <- nrow(tratados) / nrow(c)
    partes[[i]] <- rbind(tratados, c)
  }
  resultado <- unir_filas(partes)
  comprobar_pesos(resultado)
  resultado
}

# 6. Regresión ponderada, efectos de fecha e inferencia ---------------------
# Se absorbe cada fecha con su media ponderada. Se estiman varios horizontes
# a la vez por mínimos cuadrados. Las fórmulas siguientes reproducen las
# correcciones de muestra finita de Python, sin reparar varianzas negativas.
# CRV1: covarianza robusta agrupada por estado o por estado y fecha.
# CRV3: covarianza de réplicas que omiten un estado con los pesos originales.

rango_matriz <- function(x) {
  d <- svd(x, nu = 0, nv = 0)$d
  if (!length(d)) return(0L)
  sum(d > max(dim(x)) * max(d) * .Machine$double.eps)
}

estimar <- function(muestra, columnas, y, inferencia = TRUE) {
  x <- as.matrix(muestra[columnas])
  y <- as.matrix(y)
  n <- nrow(x)
  k <- ncol(x)
  m <- ncol(y)
  stopifnot(nrow(y) == n, all(is.finite(x)), all(is.finite(y)))
  b <- matrix(NA_real_, m, k)
  covarianzas <- list(entidad = NULL, entidad_fecha = NULL)
  gl <- c(entidad = NA_real_, entidad_fecha = NA_real_)
  grupos <- match(muestra$indice, unique(muestra$indice))
  f <- length(unique(grupos))
  g <- length(unique(muestra$estado))
  z <- cbind(x, y)
  sumas <- rowsum(z * muestra$peso, grupos, reorder = TRUE)
  masas <- rowsum(muestra$peso, grupos, reorder = TRUE)[, 1]
  medias <- sumas / masas
  dentro <- (z - medias[grupos, , drop = FALSE]) * sqrt(muestra$peso)
  xw <- dentro[, seq_len(k), drop = FALSE]
  yw <- dentro[, k + seq_len(m), drop = FALSE]
  independientes <- integer()
  for (j in seq_len(k)) {
    bloque <- xw[, c(independientes, j), drop = FALSE]
    if (rango_matriz(bloque) > length(independientes)) independientes <- c(independientes, j)
  }
  if (!length(independientes)) return(list(b = b, v = covarianzas, gl = gl))
  xw <- xw[, independientes, drop = FALSE]
  descomposicion <- svd(xw)
  ajuste <- descomposicion$v %*%
    (crossprod(descomposicion$u, yw) / descomposicion$d)
  b[, independientes] <- t(ajuste)
  if (!inferencia || g < 2 || n <= f + length(independientes)) {
    return(list(b = b, v = covarianzas, gl = gl))
  }
  residuo <- yw - xw %*% ajuste
  influencia <- xw %*% solve(crossprod(xw))
  puntuaciones <- do.call(cbind, lapply(seq_len(m), function(j) influencia * residuo[, j]))
  posiciones <- unlist(lapply(seq_len(m), function(j) (j - 1) * k + independientes))
  correccion <- (n - 1) / (n - f - length(independientes))
  carne <- function(grupo) crossprod(rowsum(puntuaciones, grupo, reorder = FALSE))
  expandir <- function(v) {
    completa <- matrix(NA_real_, k * m, k * m)
    completa[posiciones, posiciones] <- v
    completa
  }
  v_estado <- carne(muestra$estado)
  covarianzas$entidad <- expandir(v_estado * correccion * g / (g - 1))
  gl["entidad"] <- g - 1
  if (f >= 6) {
    menor <- min(g, f)
    v_fecha <- carne(grupos)
    v_interseccion <- carne(paste(muestra$estado, muestra$indice))
    covarianzas$entidad_fecha <- expandir((v_estado + v_fecha - v_interseccion) *
                                         correccion * menor / (menor - 1))
    gl["entidad_fecha"] <- menor - 1
  }
  list(b = b, v = covarianzas, gl = gl)
}

intervalo <- function(coeficiente, varianza, gl) {
  ee <- sqrt(pmax(varianza, 0))
  ee[!is.na(varianza) & varianza < 0] <- NA_real_
  critico <- qt(1 - alpha / 2, gl)
  data.frame(efecto = coeficiente, ee, gl = unname(gl),
             ic_inf = coeficiente - critico * ee, ic_sup = coeficiente + critico * ee,
             p = ifelse(ee > 0, 2 * pt(-abs(coeficiente / ee), gl), NA_real_))
}

# Efecto mínimo detectable (MDE): t no central, prueba bilateral al 5%,
# potencia del 80%. Se calcula el multiplicador una vez por grado de libertad.
gl_posibles <- 1:31
factor_mde <- sapply(gl_posibles, function(gl) {
  critico <- qt(1 - alpha / 2, gl)
  rechazo <- function(ncp) {
    pt(critico, gl, ncp, lower.tail = FALSE) + pt(-critico, gl, ncp) - potencia
  }
  uniroot(rechazo, c(0, critico + 5), tol = 0.000000000001)$root
})
mde <- function(gl, ee) ifelse(is.finite(gl) & is.finite(ee) & ee > 0,
                              ee * factor_mde[gl], NA_real_)

wald <- function(b, v, gl) {
  resultado <- data.frame(f = NA_real_, gl_num = length(b), gl_den = unname(gl),
                          p = NA_real_, estado = "calculada")
  if (is.null(v) || !is.finite(gl)) {
    resultado$estado <- "conglomerados o grados de libertad insuficientes"
  } else if (!all(is.finite(b)) || !all(is.finite(v))) {
    resultado$estado <- "coeficientes sin identificar"
  } else {
    v <- (v + t(v)) / 2
    autovalores <- eigen(v, symmetric = TRUE, only.values = TRUE)$values
    tolerancia <- max(abs(autovalores)) * length(b) * .Machine$double.eps
    if (min(autovalores) < -tolerancia) {
      resultado$estado <- "covarianza indefinida"
    } else if (min(autovalores) <= tolerancia) {
      resultado$estado <- "covarianza sin rango"
    } else {
      resultado$f <- as.numeric(crossprod(b, solve(v, b))) / length(b)
      resultado$p <- pf(resultado$f, length(b), gl, lower.tail = FALSE)
    }
  }
  resultado
}

resumir <- function(muestra) {
  t <- muestra[muestra$tratado == 1, ]
  c <- muestra[muestra$tratado == 0, ]
  peso_episodio <- tapply(t$peso, t$id_episodio, sum) / nrow(t)
  peso_estado <- tapply(t$peso, t$estado, sum) / nrow(t)
  data.frame(n = nrow(muestra), municipios = length(unique(muestra$clave)),
             tratados = nrow(t), controles = nrow(c),
             municipios_tratados = length(unique(t$clave)),
             municipios_controles = length(unique(c$clave)),
             fechas = length(unique(muestra$indice)), episodios = length(unique(t$id_episodio)),
             estados = length(unique(muestra$estado)), estados_tratados = length(unique(t$estado)),
             estados_controles = length(unique(c$estado)), max_peso_episodio = max(peso_episodio),
             max_peso_estado = max(peso_estado), episodios_efectivos = 1 / sum(peso_episodio^2),
             estados_tratados_efectivos = 1 / sum(peso_estado^2),
             max_reuso_control = max(table(c$clave)))
}

# 7. Contrastes, bases y pruebas previas -----------------------------------
# %% es el módulo no negativo de R: también sirve para h = -7,...,-1.
# Primero se aplica log(1+Y) a cada observación; después se promedia.

offsets_base <- function(h) (h %% 7) - c(28, 21, 14)
transformar <- function(x, escala) {
  stopifnot(all(is.finite(x)), all(x >= 0))
  if (escala == "log1p") log1p(x) else x
}
# Sumas en doble precisión y en el orden de Python. rowMeans acumula con
# precisión extendida en R: difiere en los residuos de contrastes idénticos
# a su base. Sus valores p son artefactos numéricos, no pruebas informativas.
promedio_vectores <- function(lista) Reduce("+", lista) / length(lista)
contrastes <- function(muestra, escala, base = "tres_semanas", horizontes = tramos) {
  dias <- sort(unique(unlist(horizontes)))
  referencias <- lapply(dias, function(h) {
    if (base == "tres_semanas") offsets_base(h) else if (base == "wk-1") -7:-1 else -2
  })
  names(referencias) <- as.character(dias)
  necesarios <- sort(unique(c(dias, unlist(referencias))))
  valores <- lapply(necesarios, function(h) transformar(extraer(muestra, h), escala))
  names(valores) <- as.character(necesarios)
  delta <- lapply(dias, function(h) {
    valores[[as.character(h)]] - promedio_vectores(valores[as.character(referencias[[as.character(h)]])])
  })
  names(delta) <- as.character(dias)
  resultado <- sapply(horizontes, function(h) promedio_vectores(delta[as.character(h)]))
  matrix(resultado, nrow = nrow(muestra), dimnames = list(NULL, names(horizontes)))
}

resultados <- function(muestra, escala, base, modelos = 0, crv3 = FALSE) {
  y <- contrastes(muestra, escala, base)
  resumen <- resumir(muestra)
  t <- muestra[muestra$tratado == 1, ]
  previa <- unlist(lapply(-28:-8, function(h) extraer(t, h)))
  sigma <- sd(transformar(previa, escala))
  media <- mean(previa)
  filas <- omisiones <- list()
  muestra$log_poblacion <- log(muestra$poblacion)
  for (modelo in modelos) {
    columnas <- columnas_modelo[seq_len(modelo + 1)]
    ajuste <- estimar(muestra, columnas, y)
    if (crv3) {
      entidades <- sort(unique(muestra$estado))
      replicas <- matrix(NA_real_, length(entidades), length(ajuste$b))
      for (i in seq_along(entidades)) {
        conservar <- muestra$estado != entidades[i]
        replica <- estimar(muestra[conservar, ], columnas, y[conservar, , drop = FALSE], FALSE)$b
        replicas[i, ] <- as.vector(t(replica))
        omisiones[[length(omisiones) + 1]] <- data.frame(
          estado_omitido = entidades[i], modelo = paste0("M", modelo), tramo = names(tramos),
          efecto = replica[, 1], identificada = is.finite(replica[, 1]))
      }
      diferencia <- sweep(replicas, 2, as.vector(t(ajuste$b)), "-")
      ajuste$v$CRV3 <- crossprod(diferencia) * (length(entidades) - 1) / length(entidades)
      ajuste$gl["CRV3"] <- length(entidades) - 1
    }
    for (agrupacion in names(ajuste$v)) {
      v <- ajuste$v[[agrupacion]]
      varianza <- if (is.null(v)) rep(NA_real_, ncol(y)) else
        diag(v)[seq(1, nrow(v), by = length(columnas))]
      estadisticas <- intervalo(ajuste$b[, 1], varianza, ajuste$gl[agrupacion])
      estado <- ifelse(!is.finite(ajuste$b[, 1]), "sin_identificar",
                       if (is.null(v)) "sin_covarianza" else
                         ifelse(varianza < 0, "varianza_negativa",
                                ifelse(varianza == 0, "varianza_cero", "calculada")))
      filas[[length(filas) + 1]] <- cbind(
        data.frame(modelo = paste0("M", modelo), tramo = names(tramos), agrupacion,
                   base, escala), resumen[rep(1, ncol(y)), ], estadisticas,
        sigma_pre = sigma, media_pre = media, estado_inferencia = estado,
        efecto_sigma = estadisticas$efecto / sigma,
        mde = mde(ajuste$gl[agrupacion], estadisticas$ee))
    }
  }
  list(efectos = unir_filas(filas), omisiones = unir_filas(omisiones))
}

pruebas_semanales <- function(muestra, escala) {
  promedio <- function(h) rowMeans(sapply(h, function(d) transformar(extraer(muestra, d), escala)))
  referencia <- promedio(-14:-8)
  y <- cbind("wk-4" = promedio(-28:-22) - referencia,
             "wk-3" = promedio(-21:-15) - referencia,
             "wk-1" = promedio(-7:-1) - referencia)
  ajuste <- estimar(muestra, "tratado", y)
  filas <- list()
  for (agrupacion in names(ajuste$v)) {
    v <- ajuste$v[[agrupacion]]
    eigen_min <- if (is.null(v)) NA_real_ else min(eigen(v, symmetric = TRUE, only.values = TRUE)$values)
    condicion <- if (is.null(v)) NA_real_ else {
      d <- svd(v, nu = 0, nv = 0)$d
      max(d) / min(d)
    }
    filas[[length(filas) + 1]] <- cbind(data.frame(
      escala, agrupacion, referencia = "wk-2 [-14,-8]", restricciones = "wk-4;wk-3;wk-1",
      rango = if (is.null(v)) 0 else rango_matriz(v), condicion, autovalor_min = eigen_min),
      wald(ajuste$b[, 1], v, ajuste$gl[agrupacion]))
    individuales <- intervalo(ajuste$b[, 1], if (is.null(v)) rep(NA_real_, 3) else diag(v),
                              ajuste$gl[agrupacion])
    filas[[length(filas) + 1]] <- cbind(data.frame(
      escala, agrupacion, referencia = "wk-2 [-14,-8]", restricciones = colnames(y)), individuales)
  }
  unir_filas(filas)
}

# 8. Balance previo y cobertura de las uniones -----------------------------

momentos <- function(muestra, variable) {
  muestra <- muestra[!is.na(muestra[[variable]]), ]
  muestra <- muestra[order(muestra[[variable]]), ]
  x <- muestra[[variable]]
  w <- muestra$peso
  if (!length(x)) return(data.frame(n = 0, peso = 0, media = NA_real_, de = NA_real_,
                                    p10 = NA_real_, p50 = NA_real_, p90 = NA_real_))
  media <- weighted.mean(x, w)
  cuantiles <- sapply(c(0.1, 0.5, 0.9), function(p) x[which(cumsum(w) / sum(w) >= p)[1]])
  data.frame(n = length(x), peso = sum(w), media, de = sqrt(weighted.mean((x - media)^2, w)),
             p10 = cuantiles[1], p50 = cuantiles[2], p90 = cuantiles[3])
}

balance <- function(grupos) {
  filas <- list()
  for (variable in c(covariables, "pre_nivel")) {
    ref <- grupos$auditada
    escala <- sqrt(mean(sapply(0:1, function(rol) momentos(ref[ref$tratado == rol, ], variable)$de^2)))
    for (metodo in names(grupos)) {
      muestra <- grupos[[metodo]]
      control <- momentos(muestra[muestra$tratado == 0, ], variable)
      tratado <- momentos(muestra[muestra$tratado == 1, ], variable)
      diferencia <- tratado$media - control$media
      filas[[length(filas) + 1]] <- cbind(
        data.frame(muestra = metodo, covariable = variable, tratado = 0:1), rbind(control, tratado),
        diferencia, escala_auditada = escala, dme = if (escala > 0) diferencia / escala else NA_real_)
    }
  }
  unir_filas(filas)
}

cobertura_uniones <- function(muestra, escenario) {
  filas <- list()
  indices <- sort(unique(muestra$indice))
  for (i in seq_along(indices)) {
    for (rol in 0:1) {
      grupo <- muestra[muestra$indice == indices[i] & muestra$tratado == rol, ]
      if (!nrow(grupo)) next
      for (fuente in c("censo", "saic", "vmrc")) {
        columna <- c(censo = "poblacion", saic = "empleo", vmrc = "autos")[[fuente]]
        valor <- c(censo = "poblacion", saic = "empleo_mil", vmrc = "autos_mil")[[fuente]]
        union <- grupo[[paste0(fuente, "_union")]]
        estado <- grupo[[paste0(columna, "_estado")]]
        denominador <- grupo[[paste0(fuente, "_conapo_union")]]
        contar <- function(x, valor) sum(x == valor, na.rm = TRUE)
        fila <- data.frame(especificacion = escenario, indice = indices[i], tratado = rol,
                           fuente, corte = grupo[[paste0("corte_", fuente)]][1], pares = nrow(grupo),
                           unidas = contar(union, "unida"), tasa_union = mean(union == "unida"),
                           utilizables = sum(!is.na(grupo[[valor]])), ceros = contar(estado, "cero"),
                           confidenciales = contar(estado, "confidencial"),
                           faltantes_declarados = contar(estado, "faltante"),
                           conapo_sin_clave = if (is.null(denominador)) NA_integer_ else contar(denominador, "sin_clave"),
                           conapo_territorio_incompatible = if (is.null(denominador)) NA_integer_ else
                             contar(denominador, "territorio_incompatible"))
        for (codigo in c("sin_clave", "solo_entidad", "territorio_incompatible", "quiebre_en_ventana",
                         "perimetro_no_confirmado", "medicion_posterior")) fila[[codigo]] <- contar(union, codigo)
        filas[[length(filas) + 1]] <- fila
      }
    }
  }
  unir_filas(filas)
}

# 9. Muestras del diseño final y sensibilidades ----------------------------

calendario_oficial <- function(dias) {
  filas <- vector("list", length(dias))
  for (i in seq_along(dias)) {
    dia <- dias[i]
    anio <- as.integer(format(dia, "%Y"))
    lunes <- function(mes) {
      fechas_mes <- as.Date(sprintf("%04d-%02d-01", anio, mes)) + 0:30
      fechas_mes[as.POSIXlt(fechas_mes)$wday == 1 & as.integer(format(fechas_mes, "%m")) == mes]
    }
    feriados <- c(as.Date(paste0(anio, c("-01-01", "-05-01", "-09-16", "-12-25"))),
                  lunes(2)[1], lunes(3)[3], lunes(11)[3], as.Date("2024-10-01"))
    hit <- calendario_sep[calendario_sep$inicio <= dia & calendario_sep$fin >= dia, ]
    filas[[i]] <- data.frame(fecha = dia, laboral = dia %in% feriados, escolar = nrow(hit) > 0,
                             tipo_escolar = paste(sort(unique(hit$tipo)), collapse = ";"),
                             fuentes = paste(sort(unique(hit$fuente)), collapse = ";"))
  }
  unir_filas(filas)
}
dias_calendario <- as.Date(sort(unique(as.vector(outer(
  as.numeric(na.omit(eventos$inicio)), -56:14, "+")))), origin = "1970-01-01")
calendario <- calendario_oficial(dias_calendario)
guardar(calendario, "causal_calendario")
banderas <- function(indice) calendario[match(indice + 0:1, calendario$fecha), ]

muestras <- list()
vinculos_totales <- perdidas_totales <- auditorias <- uniones <- balances <- soportes <- list()
universo_principal <- NULL
for (escenario in c("principal", "persistencia", "placebo")) {
  cat("Selección y emparejamientos:", escenario, "\n")
  seleccion <- seleccionar(escenario == "placebo", escenario == "persistencia")
  auditorias[[escenario]] <- transform(seleccion$auditoria, escenario = escenario)
  universo <- adjuntar_covariables(seleccion$muestra, escenario == "persistencia")
  if (escenario == "principal") universo_principal <- universo
  uniones[[escenario]] <- cobertura_uniones(universo, escenario)
  muchos <- emparejar(universo)
  uno <- uno_a_uno(muchos$muestra, muchos$vinculos)
  nivel <- emparejar(universo, character())
  comun <- emparejar(universo[complete.cases(universo[covariables]), ], character())
  grupos <- list(sin_covariables = nivel$muestra,
                 mismos_tratados = mismos_tratados(universo, muchos$muestra),
                 comun_m0_m3 = comun$muestra, emparejada = muchos$muestra,
                 emparejada_1a1 = uno$muestra)
  muestras[[escenario]] <- grupos
  perdidas_totales[[escenario]] <- transform(muchos$perdidas, escenario = escenario)
  for (metodo in c("sin_covariables", "comun_m0_m3", "emparejada", "emparejada_1a1")) {
    enlaces <- switch(metodo, sin_covariables = nivel$vinculos, comun_m0_m3 = comun$vinculos,
                      emparejada = muchos$vinculos, emparejada_1a1 = uno$vinculos)
    vinculos_totales[[paste(escenario, metodo)]] <- transform(enlaces, escenario = escenario, muestra = metodo)
  }
  for (metodo in names(grupos)) {
    soportes[[paste(escenario, metodo)]] <- cbind(escenario, muestra = metodo, resumir(grupos[[metodo]]))
  }
  balances[[escenario]] <- transform(balance(c(list(auditada = nivel$muestra), grupos)), escenario = escenario)
}

tratados <- muestras$principal$emparejada
tratados <- tratados[tratados$tratado == 1, c("clave", "indice")]
exclusiones <- tratados
exclusiones$audit_cinco <- tratados$indice %in% cinco_fechas
exclusiones$laboral <- sapply(seq_len(nrow(tratados)), function(i) any(banderas(tratados$indice[i])$laboral))
exclusiones$escolar <- sapply(seq_len(nrow(tratados)), function(i) any(banderas(tratados$indice[i])$escolar))
guardar(exclusiones, "causal_exclusiones_calendario")

sensibilidades <- c("sin_cinco", "sin_laborales", "sin_laborales_escolares", "sin_pendientes",
                    "sin_todos_pendientes", "sin_senales")
for (escenario in sensibilidades) {
  cat("Sensibilidad:", escenario, "\n")
  universo <- universo_principal
  if (escenario %in% c("sin_cinco", "sin_laborales", "sin_laborales_escolares")) {
    indices <- sort(unique(universo$indice))
    quitar <- sapply(seq_along(indices), function(i) {
      if (escenario == "sin_cinco") return(indices[i] %in% cinco_fechas)
      banderas_fecha <- banderas(indices[i])
      any(banderas_fecha$laboral) || (escenario == "sin_laborales_escolares" && any(banderas_fecha$escolar))
    })
    universo <- universo[!universo$indice %in% indices[quitar], ]
  } else if (escenario %in% c("sin_pendientes", "sin_todos_pendientes")) {
    pendiente <- (universo$clave == "16025" & universo$indice == as.Date("2021-07-14")) |
      (universo$clave == "16017" & universo$indice == as.Date("2025-04-23"))
    if (escenario == "sin_todos_pendientes") {
      pendiente <- pendiente | (universo$clave == "16037" & universo$indice == as.Date("2025-04-23")) |
        (universo$clave == "28035" & universo$indice == as.Date("2023-04-30"))
    }
    universo <- universo[!(pendiente & universo$tratado == 1), ]
  } else {
    bloqueada <- rep(FALSE, nrow(universo))
    for (i in seq_len(nrow(senales))) {
      bloqueada <- bloqueada | (universo$clave == senales$clave[i] & universo$tratado == 0 &
                                 universo$indice - 49 <= senales$fin[i] & universo$indice + 14 >= senales$inicio[i])
    }
    universo <- universo[!bloqueada, ]
  }
  muchos <- emparejar(universo)
  uno <- uno_a_uno(muchos$muestra, muchos$vinculos)
  muestras[[escenario]] <- list(emparejada = muchos$muestra, emparejada_1a1 = uno$muestra)
  perdidas_totales[[escenario]] <- transform(muchos$perdidas, escenario = escenario)
  for (metodo in names(muestras[[escenario]])) {
    enlaces <- if (metodo == "emparejada") muchos$vinculos else uno$vinculos
    vinculos_totales[[paste(escenario, metodo)]] <- transform(enlaces, escenario = escenario, muestra = metodo)
    soportes[[paste(escenario, metodo)]] <- cbind(escenario, muestra = metodo, resumir(muestras[[escenario]][[metodo]]))
  }
}

# 10. Ejecución de los modelos y exportación de los resultados --------------

efectos <- omisiones <- pruebas <- registros_muestra <- list()
for (escenario in names(muestras)) {
  for (metodo in names(muestras[[escenario]])) {
    cat("Estimación:", escenario, metodo, "\n")
    muestra <- muestras[[escenario]][[metodo]]
    registros_muestra[[paste(escenario, metodo)]] <- transform(muestra, escenario = escenario, muestra = metodo)
    for (escala in c("log1p", "niveles")) {
      bases <- if (escenario == "principal") c("tres_semanas", "-2", "wk-1") else "tres_semanas"
      for (base in bases) {
        modelos <- if (metodo != "sin_covariables" && escenario == "principal" && base == "tres_semanas") 0:3 else 0
        ajuste <- resultados(muestra, escala, base, modelos,
                              crv3 = escenario == "principal" && base == "tres_semanas")
        llave <- paste(escenario, metodo, escala, base)
        efectos[[llave]] <- transform(ajuste$efectos, escenario = escenario, muestra = metodo)
        if (nrow(ajuste$omisiones)) {
          omisiones[[llave]] <- transform(ajuste$omisiones, escala = escala, muestra = metodo)
        }
      }
      if (escenario %in% c("principal", "persistencia", "placebo")) {
        pruebas[[paste(escenario, metodo, escala)]] <- transform(pruebas_semanales(muestra, escala),
                                                              escenario = escenario, muestra = metodo)
      }
    }
  }
}
efectos <- unir_filas(efectos)
omisiones <- unir_filas(omisiones)
pruebas <- unir_filas(pruebas)
balance_final <- unir_filas(balances)
soporte_final <- unir_filas(soportes)
perdidas_finales <- unir_filas(perdidas_totales)
auditoria_final <- unir_filas(auditorias)
uniones_finales <- unir_filas(uniones)
vinculos_finales <- unir_filas(vinculos_totales)
productos <- list(causal_efectos = efectos, causal_omision_estado = omisiones,
                   causal_wald_semanal = pruebas, causal_soporte = soporte_final,
                   causal_muestras = unir_filas(registros_muestra), causal_vinculos = vinculos_finales,
                   causal_descartes = perdidas_finales, causal_elegibilidad = auditoria_final,
                   causal_uniones = uniones_finales, causal_balance = balance_final)
for (nombre in names(productos)) guardar(productos[[nombre]], nombre)

# Nueve celdas horarias por gravedad y el contraste pareado noche menos día.
franjas <- c("dia", "noche", "hora_desconocida")
gravedades <- c("fatal", "heridos", "danos")
celdas <- unlist(lapply(franjas, function(f) paste(f, gravedades, sep = "_")))
cruces <- list()
for (metodo in c("emparejada", "emparejada_1a1")) {
  muestra <- muestras$principal[[metodo]]
  celdas_en <- function(h) {
    datos <- conteos[data.table(clave = muestra$clave, fecha = muestra$indice + h), ..celdas]
    valores <- as.matrix(datos)
    valores[is.na(valores)] <- 0
    valores
  }
  cambios_celdas <- lapply(0:1, function(h) celdas_en(h) -
                            Reduce("+", lapply(offsets_base(h), celdas_en)) / 3)
  cambio <- Reduce("+", cambios_celdas) / 2
  stopifnot(max(abs(rowSums(cambio) - contrastes(muestra, "niveles")[, "d0..1"])) < 0.000000001)
  y <- cbind(cambio, cambio[, 4:6] - cambio[, 1:3])
  actividad <- colSums(Reduce("+", lapply(sort(unique(c(0:1, offsets_base(0), offsets_base(1)))), celdas_en))) > 0
  presente <- c(actividad, actividad[1:3] | actividad[4:6])
  ajuste <- estimar(muestra, "tratado", y)
  for (agrupacion in names(ajuste$v)) {
    v <- ajuste$v[[agrupacion]]
    estadisticas <- intervalo(ajuste$b[, 1], if (is.null(v)) rep(NA_real_, 12) else diag(v),
                              ajuste$gl[agrupacion])
    estadisticas[!presente, c("ee", "ic_inf", "ic_sup", "p")] <- NA
    cruces[[paste(metodo, agrupacion)]] <- cbind(data.frame(
      muestra = metodo, franja = c(rep(franjas, each = 3), rep("noche_menos_dia", 3)),
      gravedad = rep(gravedades, 4), tramo = "d0..1",
      estado = ifelse(presente, "estimado", "sin_registros"), agrupacion), estadisticas)
  }
}
cruce_final <- unir_filas(cruces)
guardar(cruce_final, "causal_cruce")

fechas_base <- list()
for (escenario in c("principal", "placebo")) {
  indices <- sort(unique(muestras[[escenario]]$emparejada$indice))
  for (i in seq_along(indices)) {
    for (h in -7:13) {
      refs <- indices[i] + offsets_base(h)
      fechas_base[[length(fechas_base) + 1]] <- data.frame(
        escenario, indice = indices[i], inicio_real = indices[i] + if (escenario == "placebo") 28 else 0,
        h, resultado = indices[i] + h, b1 = refs[1], b2 = refs[2], b3 = refs[3])
    }
  }
}
guardar(unir_filas(fechas_base), "causal_fechas_base")
guardar(data.frame(registros_fecha_invalida = nrow(invalidos),
                    mes_desconocido = sum(!invalidos$mes %in% 1:12),
                    regla = "conteo de filas publicadas con fecha valida; elegibilidad predicha hasta t-1"),
         "causal_medicion")

# 11. Referencia auditada anterior para el cuadro de trazabilidad -----------
# Esta rama conserva el calibre alrededor de la media de la fecha y exige
# continuidad hasta +15 y aislamiento hasta +16. No selecciona el diseño final.

cat("Reconstrucción de la referencia auditada\n")
seleccionar_auditada <- function() {
  partes <- list()
  indices <- sort(unique(focales$inicio))
  territoriales <- c("25001", "25006", "25010", "25011", "25017", "25019", "25020")
  for (i in seq_along(indices)) {
    indice <- indices[i]
    cohorte <- focales[focales$inicio == indice, ]
    local <- claves %in% cohorte$clave
    derecha <- indice + 16
    izquierda <- indice - 49
    conocidos <- activos[activos$inicio <= derecha & activos$hasta >= izquierda, ]
    bloqueados_t <- character()
    for (j in seq_len(nrow(cohorte))) {
      fila <- cohorte[j, ]
      otro <- conocidos$id_episodio != fila$id_episodio
      conflicto <- (conocidos$clave == fila$clave & otro) |
        (conocidos$clave == "" & conocidos$cve_ent == fila$cve_ent & otro)
      if (any(conflicto, na.rm = TRUE)) bloqueados_t <- c(bloqueados_t, fila$clave)
    }
    geografia <- unique(activos$cve_ent[activos$id_episodio %in% cohorte$id_episodio])
    quiebre <- claves %in% territoriales & derecha >= as.Date("2024-11-01")
    ventana <- fechas >= indice - 28 & fechas <= indice + 15
    calendario <- sum(ventana) == 44 && izquierda >= min(fechas) && derecha <= max(fechas)
    completa <- rowSums(continuidad[, ventana, drop = FALSE] &
                         is.finite(valores_panel[, ventana, drop = FALSE])) == sum(ventana) & calendario
    nivel <- rowMeans(valores_panel[, fechas >= indice - 28 & fechas < indice - 14, drop = FALSE])
    t <- local & !claves %in% bloqueados_t & !quiebre & completa
    c <- !local & !estados %in% geografia &
      !claves %in% conocidos$clave[conocidos$clave != ""] &
      !estados %in% conocidos$cve_ent[conocidos$clave == ""] & !quiebre & completa
    if (!any(t)) next
    razon <- (nivel + 0.5) / (mean(nivel[t]) + 0.5)
    c <- c & !is.na(razon) & razon >= 0.5 & razon <= 2
    if (sum(c) < min_controles || length(unique(estados[c])) < min_estados) next
    elegidas <- t | c
    episodio <- cohorte$id_episodio[match(claves[elegidas], cohorte$clave)]
    episodio[is.na(episodio)] <- ""
    partes[[i]] <- data.frame(clave = claves[elegidas], estado = estados[elegidas], indice,
                             tratado = as.integer(t[elegidas]), id_episodio = episodio,
                             peso = ifelse(t[elegidas], 1, sum(t) / sum(c)), pre_nivel = nivel[elegidas])
  }
  unir_filas(partes)
}
auditada <- seleccionar_auditada()
comprobar_pesos(auditada)
y_auditada <- extraer(auditada, 0, valores_panel) - extraer(auditada, -2, valores_panel)
b_auditada <- estimar(auditada, "tratado", matrix(y_auditada, ncol = 1))
stopifnot(nrow(auditada[auditada$tratado == 1, ]) == 73,
          abs(b_auditada$b[1, 1] - 0.237468) < 0.000001)
guardar(cbind(resumir(auditada), intervalo(b_auditada$b[1, 1], b_auditada$v$entidad[1, 1],
                                         b_auditada$gl["entidad"])), "referencia_sin_emparejar")
auditada <- adjuntar_covariables(auditada, auditada = TRUE)
muchos_antes <- emparejar(auditada, individual = FALSE)
uno_antes <- uno_a_uno(muchos_antes$muestra, muchos_antes$vinculos)
grupos_antes <- list(emparejada = muchos_antes$muestra, emparejada_1a1 = uno_antes$muestra)
referencia <- list()
for (metodo in names(grupos_antes)) {
  muestra <- grupos_antes[[metodo]]
  horizontes <- c(-14:-3, 0:15)
  y <- sapply(horizontes, function(h) extraer(muestra, h, valores_panel) - extraer(muestra, -2, valores_panel))
  ajuste <- estimar(muestra, "tratado", y)
  estatal <- intervalo(ajuste$b[, 1], diag(ajuste$v$entidad), ajuste$gl["entidad"])
  doble <- intervalo(ajuste$b[, 1], diag(ajuste$v$entidad_fecha), ajuste$gl["entidad_fecha"])
  referencia[[metodo]] <- cbind(data.frame(muestra = metodo, h = horizontes),
                               resumir(muestra)[rep(1, length(horizontes)), ], estatal,
                               ee_doble = doble$ee, gl_doble = doble$gl,
                               ic_doble_inf = doble$ic_inf, ic_doble_sup = doble$ic_sup)
}
referencia <- unir_filas(referencia)
guardar(referencia, "referencia_auditada")

morelia <- list()
for (escenario in c("auditada", "principal", "sin_senales")) {
  enlaces <- if (escenario == "auditada") muchos_antes$vinculos else
    vinculos_finales[vinculos_finales$escenario == escenario & vinculos_finales$muestra == "emparejada", ]
  enlaces <- enlaces[enlaces$tratado_clave == "16053" & enlaces$indice == as.Date("2025-04-23"), ]
  morelia[[escenario]] <- data.frame(escenario, control_clave = enlaces$control_clave,
                                    contribucion = enlaces$contribucion)
}
morelia <- unir_filas(morelia)
guardar(morelia, "causal_morelia_donantes")

# 12. Culiacán: comparación semanal estrictamente descriptiva ---------------
# Se conserva NA por falta de continuidad; se suma Eldorado a Culiacán desde
# noviembre de 2024. Entrenamiento -25..-10, validación -9..-3 y base -2.

cat("Comparación semanal de Culiacán\n")
inicio_culiacan <- as.Date("2024-09-09")
semana_dia <- as.integer(floor(as.numeric(fechas - inicio_culiacan) / 7))
semanas <- sort(unique(semana_dia))
semanas <- semanas[semanas >= -25 & sapply(semanas, function(s) sum(semana_dia == s)) == 7]
valores <- valores_panel
valores[!continuidad] <- NA_real_
c <- match("25006", claves)
e <- match("25019", claves)
despues <- fechas >= as.Date("2024-11-01")
valores[c, despues] <- valores[c, despues] + valores[e, despues]
semanal <- sapply(semanas, function(s) rowSums(valores[, semana_dia == s, drop = FALSE]))
rm(valores)
entrenar <- semanas >= -25 & semanas <= -10
base_cul <- semanas == -2
validar <- semanas > -10 & semanas < -1 & !base_cul
post_observado <- semanas >= 0 & is.finite(semanal[c, ])
comun <- entrenar | validar | base_cul | post_observado
expuestos <- activos[activos$hasta >= inicio_culiacan - 25 * 7 - 21 & activos$inicio <= max(fechas), ]
elegibles <- which(estados != "25" &
                    !estados %in% expuestos$cve_ent[expuestos$clave == ""] &
                    !claves %in% expuestos$clave[expuestos$clave != ""] &
                    rowSums(is.finite(semanal[, comun, drop = FALSE])) == sum(comun))
primera_semana <- inicio_culiacan + 7 * min(semanas[comun])
ultima_semana <- inicio_culiacan + 7 * max(semanas[comun]) + 6
divisiones <- cambios[cambios$codigo == "M" & cambios$fecha >= primera_semana & cambios$fecha <= ultima_semana, ]
permitida <- !claves %in% c(divisiones$origen, divisiones$destino)
descartadas <- claves[elegibles[!permitida[elegibles]]]
guardar(data.frame(clave = descartadas, desde = primera_semana, hasta = ultima_semana,
                    motivo = "segregacion_M"), "culiacan_descartes_territoriales")
elegibles <- elegibles[permitida[elegibles]]

comparar_semanal <- function(fila, universo) {
  diferencia <- sweep(semanal[universo, entrenar, drop = FALSE], 2, semanal[fila, entrenar], "-")
  distancia <- sqrt(rowMeans(diferencia^2))
  elegidos <- universo[order(distancia, seq_along(universo))[1:12]]
  control <- colMeans(semanal[elegidos, , drop = FALSE])
  diferencia <- semanal[fila, ] - control
  list(elegidos = elegidos, control = control, brecha = diferencia - diferencia[base_cul])
}
stopifnot(all(-25:-2 %in% semanas), sum(base_cul) == 1,
          all(is.finite(semanal[c, entrenar | validar | base_cul])), length(elegibles) >= 12)
comparacion <- comparar_semanal(c, elegibles)
control <- comparacion$control
control[!is.finite(semanal[c, ])] <- NA_real_
brecha <- comparacion$brecha
brecha[semanas == -1] <- NA_real_
culiacan <- data.frame(semana = semanas, inicio = inicio_culiacan + 7 * semanas,
                       tratado = semanal[c, ], control, brecha)
placebos_cul <- list()
for (fila in c(c, if (length(elegibles) > 12) comparacion$elegidos else integer())) {
  placebo <- comparar_semanal(fila, elegibles[elegibles != fila])$brecha
  placebos_cul[[length(placebos_cul) + 1]] <- data.frame(
    clave = claves[fila], rol = if (fila == c) "tratado" else "placebo",
    rmse_pre_validacion = sqrt(mean(placebo[validar]^2)), brecha_media_post = mean(placebo[post_observado]))
}
soporte_cul <- data.frame(comparadores_elegibles = length(elegibles), comparadores_usados = 12,
                          semanas_post_observadas = sum(post_observado),
                          semanas_post_totales = sum(semanas >= 0), estado = "comparación descriptiva")
guardar(culiacan, "culiacan")
guardar(unir_filas(placebos_cul), "culiacan_placebos")
guardar(data.frame(clave = claves[comparacion$elegidos]), "culiacan_controles")
guardar(soporte_cul, "culiacan_soporte")

# 13. Tablas del reporte ---------------------------------------------------
# Se exportan CSV legibles y tablas LaTeX a resultados_R/tablas/.
# No compila ni modifica el escrito: estas tablas permiten consultar y cotejar
# las cifras del apéndice sin R Markdown.

formato <- function(x, decimales = 2) {
  x[is.finite(x) & abs(x) < 0.5 * 10^(-decimales)] <- 0
  ifelse(is.finite(x), formatC(x, format = "f", digits = decimales,
                              big.mark = " ", decimal.mark = ","), "—")
}
valor_p <- function(x) ifelse(is.finite(x) & x < 0.001, "\\(<0{,}001\\)", formato(x, 3))
resultado <- function(fila, intervalo = TRUE) {
  if (intervalo) paste0(formato(fila$efecto, 3), " [", formato(fila$ic_inf, 3), "; ",
                        formato(fila$ic_sup, 3), "]") else
    paste0(formato(fila$efecto, 3), " (", formato(fila$ee, 3), ")")
}
obtener <- function(escenario = "principal", metodo = "emparejada", escala = "log1p",
                    tramo = "d0..1", agrupacion = "entidad", modelo = "M0", base = "tres_semanas") {
  fila <- efectos[efectos$escenario == escenario & efectos$muestra == metodo & efectos$escala == escala &
                    efectos$tramo == tramo & efectos$agrupacion == agrupacion &
                    efectos$modelo == modelo & efectos$base == base, ]
  stopifnot(nrow(fila) == 1)
  fila
}
tabla <- function(nombre, encabezados, filas) {
  datos <- as.data.frame(do.call(rbind, filas), stringsAsFactors = FALSE)
  names(datos) <- encabezados
  guardar(datos, nombre, "tablas")
  texto <- c(paste0("\\begin{tabular}{l", paste(rep("r", ncol(datos) - 1), collapse = ""), "}"),
             "\\toprule", paste0(paste(encabezados, collapse = " & "), " \\\\"), "\\midrule",
             apply(datos, 1, function(f) paste0(paste(f, collapse = " & "), " \\\\")),
             "\\bottomrule", "\\end{tabular}")
  writeLines(enc2utf8(texto), file.path(carpeta_salida, "tablas", paste0(nombre, ".tex")), useBytes = TRUE)
}
nombres_metodo <- c(emparejada = "1:muchos", emparejada_1a1 = "1:1", mismos_tratados = "Sin matching",
                    sin_covariables = "Calibre individual", comun_m0_m3 = "Completos, calibre")
nombres_escenario <- c(principal = "Principal", persistencia = "Aislamiento posterior", placebo = "Placebo -28",
                       sin_cinco = "Cinco fechas de auditoría", sin_laborales = "Sin feriados LFT",
                       sin_laborales_escolares = "Sin LFT ni recesos SEP", sin_pendientes = "Sin dos tratados pendientes",
                       sin_todos_pendientes = "Sin cuatro casos pendientes", sin_senales = "Sin dos señales en controles")
nombres_covariable <- c(poblacion = "Población", empleo_mil = "Empleo / mil", autos_mil = "Autos / mil",
                        pre_nivel = "Accidentes previos")

filas <- list()
for (escala in c("log1p", "niveles")) {
  for (tramo in c("d0", "d1", "d0..1", "d2..6", "wk+1")) {
    a <- obtener(escala = escala, tramo = tramo)
    b <- obtener(escala = escala, tramo = tramo, agrupacion = "entidad_fecha")
    filas[[length(filas) + 1]] <- c(if (escala == "log1p") "$\\log(1+Y)$" else "Niveles", tramo,
                                   resultado(a, FALSE), paste0("[", formato(b$ic_inf, 3), "; ", formato(b$ic_sup, 3), "]"),
                                   formato(a$efecto_sigma, 3), formato(b$mde, 3))
  }
}
tabla("causal_principales", c("Escala", "Tramo", "$\\hat\\beta$ (EE)", "IC 95\\% doble", "$\\beta/\\sigma$", "MDE doble"), filas)

filas <- list()
for (metodo in c("comun_m0_m3", "mismos_tratados", "emparejada", "emparejada_1a1")) {
  for (modelo in paste0("M", 0:3)) {
    a <- obtener(metodo = metodo, modelo = modelo, agrupacion = "entidad_fecha")
    b <- obtener(metodo = metodo, modelo = modelo, escala = "niveles", agrupacion = "entidad_fecha")
    filas[[length(filas) + 1]] <- c(nombres_metodo[metodo], modelo, formato(a$tratados, 0), formato(a$n, 0),
                                   resultado(a), resultado(b))
  }
}
tabla("causal_modelos", c("Controles", "Modelo", "T", "$N$", "$\\log(1+Y)$, IC doble", "Niveles, IC doble"), filas)

bal <- balance_final[balance_final$escenario == "principal", ]
filas <- antes_despues <- list()
for (variable in names(nombres_covariable)) {
  a <- bal[bal$muestra == "emparejada" & bal$covariable == variable, ]
  b <- bal[bal$muestra == "emparejada_1a1" & bal$covariable == variable & bal$tratado == 0, ]
  filas[[variable]] <- c(nombres_covariable[variable],
                         paste0(formato(a$media[a$tratado == 1]), " (", formato(a$de[a$tratado == 1]), ")"),
                         paste0(formato(a$media[a$tratado == 0]), " (", formato(a$de[a$tratado == 0]), ")"),
                         formato(a$dme[a$tratado == 0], 3), formato(b$dme, 3))
  antes_despues[[variable]] <- c(nombres_covariable[variable], sapply(
    c("mismos_tratados", "emparejada", "emparejada_1a1"), function(m) {
      formato(bal$dme[bal$muestra == m & bal$covariable == variable & bal$tratado == 0], 3)
    }))
}
tabla("causal_balance", c("Variable", "Tratados: media (DE)", "Controles 1:muchos", "DME 1:muchos", "DME 1:1"), filas)
tabla("causal_balance_prepost", c("Variable", "Sin matching, mismos T", "1:muchos", "1:1"), antes_despues)

filas <- list()
for (fuente in c("censo", "saic", "vmrc")) {
  for (rol in c(1, 0)) {
    u <- uniones_finales[uniones_finales$especificacion == "principal" & uniones_finales$fuente == fuente &
                          uniones_finales$tratado == rol, ]
    cortes <- if (fuente == "censo") sort(unique(u$corte)) else NA_integer_
    for (corte in cortes) {
      grupo <- if (is.na(corte)) u else u[u$corte == corte, ]
      etiqueta <- if (fuente == "censo") paste(if (corte == 2015) "EIC" else "ITER", corte) else toupper(fuente)
      filas[[length(filas) + 1]] <- c(etiqueta, if (rol == 1) "T" else "C",
                                     paste0(formato(sum(grupo$unidas), 0), "/", formato(sum(grupo$pares), 0)),
                                     formato(100 * sum(grupo$unidas) / sum(grupo$pares), 1),
                                     paste0(formato(sum(grupo$utilizables), 0), "/", formato(sum(grupo$pares), 0)))
    }
  }
}
tabla("causal_uniones", c("Fuente", "Rol", "Unidas / elegibles", "\\%", "Valor utilizable / elegibles"), filas)

filas <- list()
soporte_tabla <- soporte_final[soporte_final$muestra %in% c("emparejada", "emparejada_1a1"), ]
for (i in seq_len(nrow(soporte_tabla))) {
  r <- soporte_tabla[i, ]
  filas[[i]] <- c(nombres_escenario[r$escenario], nombres_metodo[r$muestra],
                  formato(unlist(r[c("tratados", "controles", "fechas", "episodios")]), 0))
}
tabla("causal_soporte", c("Escenario", "Método", "T", "C", "Fechas", "Episodios"), filas)

filas <- list()
for (escenario in c("principal", sensibilidades)) {
  for (metodo in c("emparejada", "emparejada_1a1")) {
    a <- obtener(escenario, metodo, agrupacion = "entidad_fecha")
    b <- obtener(escenario, metodo, escala = "niveles", agrupacion = "entidad_fecha")
    filas[[length(filas) + 1]] <- c(nombres_escenario[escenario], nombres_metodo[metodo],
                                   formato(a$tratados, 0), formato(a$fechas, 0), resultado(a), resultado(b))
  }
}
tabla("causal_sensibilidades", c("Exclusión / muestra", "Método", "T", "Fechas", "Log, IC doble", "Niveles, IC doble"), filas)

filas <- list()
for (escenario in c("principal", "persistencia", "placebo")) {
  for (metodo in c("emparejada", "emparejada_1a1")) {
    a <- obtener(escenario, metodo)
    filas[[length(filas) + 1]] <- c(nombres_escenario[escenario], nombres_metodo[metodo], formato(a$tratados, 0),
                                   sapply(c("d0..1", "d2..6", "wk+1"), function(h) resultado(
                                     obtener(escenario, metodo, tramo = h, agrupacion = "entidad_fecha"))))
  }
}
tabla("causal_persistencia", c("Selección", "Método", "T", "d0..1", "d2..6", "wk+1"), filas)

filas <- list()
for (escala in c("log1p", "niveles")) {
  for (tramo in c("d0", "d1", "d0..1", "d2..6", "wk0", "wk+1")) {
    fila <- c(if (escala == "log1p") "Log" else "Niveles", tramo)
    for (metodo in c("emparejada", "emparejada_1a1")) {
      fila <- c(fila, resultado(obtener("placebo", metodo, escala, tramo, "entidad_fecha")),
                 valor_p(obtener("placebo", metodo, escala, tramo)$p))
    }
    filas[[length(filas) + 1]] <- fila
  }
}
tabla("causal_placebo", c("Escala", "Horizonte", "1:muchos, IC doble", "$p_E$", "1:1, IC doble", "$p_E$"), filas)

filas <- previos <- list()
for (metodo in c("emparejada", "emparejada_1a1")) {
  for (escala in c("log1p", "niveles")) {
    for (agrupacion in c("entidad", "entidad_fecha", "CRV3")) {
      a <- obtener(metodo = metodo, escala = escala, agrupacion = agrupacion)
      nombre <- c(entidad = "CRV1 estatal", entidad_fecha = "CRV1 doble", CRV3 = "CRV3 estatal")[[agrupacion]]
      filas[[length(filas) + 1]] <- c(nombres_metodo[metodo], if (escala == "log1p") "Log" else "Niveles",
                                     nombre, resultado(a), formato(a$gl, 0), formato(a$mde, 3))
    }
    pruebas_grupo <- pruebas[pruebas$escenario == "principal" & pruebas$muestra == metodo & pruebas$escala == escala &
                                pruebas$restricciones == "wk-4;wk-3;wk-1", ]
    for (i in seq_len(nrow(pruebas_grupo))) {
      p <- pruebas_grupo[i, ]
      previos[[length(previos) + 1]] <- c(nombres_metodo[metodo], if (escala == "log1p") "Log" else "Niveles",
                                         if (p$agrupacion == "entidad") "Estatal" else "Doble", formato(p$f, 3),
                                         valor_p(p$p), formato(p$rango, 0), formato(p$condicion, 1), p$estado)
    }
  }
}
tabla("causal_inferencia", c("Método", "Escala", "Inferencia", "d0..1, IC 95\\%", "gl", "MDE"), filas)
tabla("causal_previos", c("Método", "Escala", "Agrupación", "F", "p", "Rango", "$\\kappa$", "Estado"), previos)

filas <- bases <- list()
for (metodo in c("emparejada", "emparejada_1a1")) {
  anterior <- referencia[referencia$muestra == metodo & referencia$h == 0, ]
  a <- obtener(metodo = metodo, escala = "niveles", tramo = "d0", base = "-2")
  b <- obtener(metodo = metodo, escala = "niveles", tramo = "d0")
  filas[[metodo]] <- c(nombres_metodo[metodo], formato(anterior$tratados, 0), resultado(anterior),
                       formato(a$tratados, 0), resultado(a), resultado(b))
  for (escala in c("log1p", "niveles")) {
    bases[[paste(metodo, escala)]] <- c(nombres_metodo[metodo], if (escala == "log1p") "Log" else "Niveles",
                                       sapply(c("-2", "tres_semanas", "wk-1"), function(base) resultado(
                                         obtener(metodo = metodo, escala = escala, base = base, agrupacion = "entidad_fecha"))))
  }
}
tabla("causal_trazabilidad", c("Método", "T auditada", "Auditada: d0, b=-2", "T final", "Final: d0, b=-2", "Final: d0, base limpia"), filas)
tabla("causal_bases", c("Método", "Escala", "b=-2", "Tres semanas", "wk-1"), bases)

filas <- list()
for (gravedad in gravedades) {
  fila <- c(c(fatal = "Fatal", heridos = "Con heridos", danos = "Solo daños")[[gravedad]])
  for (metodo in c("emparejada", "emparejada_1a1")) {
    r <- cruce_final[cruce_final$muestra == metodo & cruce_final$franja == "noche_menos_dia" &
                       cruce_final$gravedad == gravedad & cruce_final$agrupacion == "entidad_fecha", ]
    fila <- c(fila, resultado(r))
  }
  filas[[gravedad]] <- fila
}
tabla("causal_cruce", c("Gravedad", "1:muchos: noche menos día", "1:1: noche menos día"), filas)

filas <- list()
indices <- sort(unique(exclusiones$indice))
for (i in seq_along(indices)) {
  r <- exclusiones[exclusiones$indice == indices[i], ]
  filas[[i]] <- c(as.character(indices[i]), formato(nrow(r), 0),
                  ifelse(c(any(r$laboral), any(r$escolar), any(r$audit_cinco)), "Sí", "No"))
}
tabla("causal_calendario", c("Inicio", "T", "LFT en d0..1", "SEP en d0..1", "Cinco auditadas"), filas)

filas <- list()
estados_omitidos <- sort(unique(omisiones$estado_omitido))
for (estado in estados_omitidos) {
  r <- omisiones[omisiones$muestra == "emparejada" & omisiones$modelo == "M0" &
                   omisiones$tramo == "d0..1" & omisiones$estado_omitido == estado, ]
  filas[[estado]] <- c(estado, formato(r$efecto[r$escala == "log1p"], 3), formato(r$efecto[r$escala == "niveles"], 3))
}
tabla("causal_omision", c("Estado omitido", "Log d0..1", "Niveles d0..1"), filas)

filas <- list()
muestra <- muestras$principal$emparejada
for (fuente in c("saic", "vmrc")) {
  num <- sum(muestra[[paste0(fuente, "_conapo_union")]] == "unida", na.rm = TRUE)
  filas[[fuente]] <- c(paste("CONAPO en", toupper(fuente)), paste0(formato(num, 0), "/", formato(nrow(muestra), 0)),
                       formato(100 * num / nrow(muestra), 1), "Pares de la muestra final")
}
a <- auditoria_final[auditoria_final$escenario == "principal", ]
num <- sum(a$territorio_compatible)
filas[["territorio"]] <- c("AGEEML: perímetro estable", paste0(formato(num, 0), "/", formato(nrow(a), 0)),
                            formato(100 * num / nrow(a), 1), "Municipio-fechas candidatos")
tabla("causal_uniones_aux", c("Operación", "Numerador / denominador", "\\%", "Universo"), filas)

t <- a[a$tratado == 1, ]
n <- nrow(t)
filas <- list(c("Candidatos del catálogo", formato(n, 0), "---"))
mascaras <- list("Sin historia de cobertura" = !t$cobertura_predicha,
                 "Exposición previa, tras cobertura" = t$cobertura_predicha & t$exposicion_en_ventana,
                 "Territorio, tras filtros anteriores" = t$cobertura_predicha & !t$exposicion_en_ventana & !t$territorio_compatible)
for (nombre in names(mascaras)) {
  excluidos <- sum(mascaras[[nombre]])
  n <- n - excluidos
  filas[[length(filas) + 1]] <- c(nombre, formato(n, 0), formato(excluidos, 0))
}
motivos <- c(faltantes_tratado = "Covariables faltantes", datos_completos = "Controles completos insuficientes",
             pre_nivel = "Calibre individual sin soporte", poblacion = "Población sin soporte",
             empleo_mil = "Empleo sin soporte", autos_mil = "Autos sin soporte")
for (motivo in names(motivos)) {
  excluidos <- sum(perdidas_finales$escenario == "principal" & perdidas_finales$motivo == motivo)
  n <- n - excluidos
  filas[[length(filas) + 1]] <- c(motivos[motivo], formato(n, 0), formato(excluidos, 0))
}
stopifnot(n == obtener()$tratados)
tabla("causal_perdidas", c("Paso, orden jerárquico", "T restantes", "T excluidos"), filas)

# Cifras que aparecen fuera de las tablas: soporte, dispersión, porcentajes,
# estados efectivos, Wald, donantes de Morelia y semanas observadas de Culiacán.
cifras <- list()
anotar <- function(nombre, valor, decimales = 3) {
  cifras[[nombre]] <<- data.frame(nombre, valor, decimales, impreso = formato(valor, decimales))
}
selecciones <- list(Main = obtener(), Doble = obtener(agrupacion = "entidad_fecha"),
                    Nivel = obtener(escala = "niveles"), NivelDoble = obtener(escala = "niveles", agrupacion = "entidad_fecha"),
                    Previa = obtener(tramo = "wk-1"), PreviaDoble = obtener(tramo = "wk-1", agrupacion = "entidad_fecha"),
                    MenosDos = obtener(tramo = "-2"), MenosCinco = obtener(tramo = "-5"),
                    CRVTres = obtener(agrupacion = "CRV3"), Placebo = obtener("placebo", agrupacion = "entidad_fecha"),
                    BaseSemana = obtener(base = "wk-1", agrupacion = "entidad_fecha"))
for (nombre in names(selecciones)) {
  for (campo in c("efecto", "ee", "ic_inf", "ic_sup", "p", "mde", "efecto_sigma")) {
    anotar(paste(nombre, campo, sep = "_"), selecciones[[nombre]][[campo]])
  }
}
principal <- obtener()
nivel <- obtener(escala = "niveles")
for (campo in c("tratados", "controles", "fechas", "episodios", "estados_tratados", "estados", "n")) anotar(campo, principal[[campo]], 0)
anotar("EstadosEf", principal$estados_tratados_efectivos, 1)
anotar("MediaPre", nivel$media_pre, 2)
anotar("SigmaPre", nivel$sigma_pre, 2)
anotar("PorcentajeUnoMas", 100 * expm1(principal$efecto), 1)
anotar("MdePctNivel", 100 * nivel$mde / nivel$media_pre, 1)
anotar("MdePctNivelDoble", 100 * obtener(escala = "niveles", agrupacion = "entidad_fecha")$mde / nivel$media_pre, 1)
for (agrupacion in c("entidad", "entidad_fecha")) {
  r <- pruebas[pruebas$escenario == "principal" & pruebas$muestra == "emparejada" & pruebas$escala == "log1p" &
                  pruebas$restricciones == "wk-4;wk-3;wk-1" & pruebas$agrupacion == agrupacion, ]
  anotar(paste0("Wald_", agrupacion, "_p"), r$p)
}
for (escenario in c("auditada", "principal", "sin_senales")) anotar(paste0("Morelia_", escenario), sum(morelia$escenario == escenario), 0)
r <- perdidas_finales[perdidas_finales$escenario == "principal" & perdidas_finales$clave == "16053" &
                         perdidas_finales$indice == as.Date("2025-04-23"), ]
anotar("MoreliaUniverso", r$controles_auditados, 0)
anotar("MoreliaCalibre", r$despues_pre_nivel, 0)
anotar("CulDonantes", soporte_cul$comparadores_usados, 0)
anotar("CulObs", soporte_cul$semanas_post_observadas, 0)
anotar("CulTotal", soporte_cul$semanas_post_totales, 0)
anotar("CulBrecha", mean(culiacan$brecha[culiacan$semana >= 0], na.rm = TRUE), 2)
guardar(unir_filas(cifras), "cifras_reporte", "tablas")
guardar(calidad, "calidad", "tablas")

# 14. Gráficas del reporte -------------------------------------------------
# Se guardan PDF y PNG con los datos que acaban de estimarse en R.
# Los intervalos son del 95% con agrupación por estado y fecha.

datos_dinamica <- efectos[efectos$escenario == "principal" & efectos$base == "tres_semanas" &
                            efectos$modelo == "M0" & efectos$agrupacion == "entidad_fecha" &
                            efectos$muestra %in% c("emparejada", "emparejada_1a1") &
                            efectos$tramo %in% as.character(-7:13), ]
datos_dinamica$h <- as.integer(datos_dinamica$tramo)
datos_dinamica$dia_grafica <- datos_dinamica$h + ifelse(datos_dinamica$muestra == "emparejada", -0.1, 0.1)
datos_dinamica$panel <- factor(datos_dinamica$escala, levels = c("log1p", "niveles"),
                              labels = c("Cambio en log(1 + registros)", "Registros por municipio y día"))
datos_dinamica$metodo <- factor(datos_dinamica$muestra, levels = c("emparejada", "emparejada_1a1"),
                               labels = c("1:muchos", "1:1"))
datos_dinamica <- datos_dinamica[order(datos_dinamica$panel, datos_dinamica$metodo, datos_dinamica$h), ]
guardar(datos_dinamica, "datos_causal_dinamica", "figuras")
g_dinamica <- ggplot(datos_dinamica, aes(dia_grafica, efecto, color = metodo, group = metodo)) +
  geom_hline(yintercept = 0, color = "#555555", linewidth = 0.3) +
  geom_vline(xintercept = -0.5, color = "#555555", linetype = "dashed", linewidth = 0.3) +
  geom_errorbar(aes(ymin = ic_inf, ymax = ic_sup), width = 0.12, linewidth = 0.3) +
  geom_line(linewidth = 0.35) + geom_point(size = 1.4) +
  facet_wrap(~panel, ncol = 1, scales = "free_y") +
  scale_color_manual(values = c("1:muchos" = "#135a76", "1:1" = "#974421")) +
  scale_x_continuous(breaks = c(-7, -5, -2, 0, 1, 3, 6, 9, 13)) +
  labs(title = "Base de tres semanas del mismo día; IC 95 % de dos vías",
       x = "Día respecto al inicio local", y = NULL, color = NULL) +
  theme_minimal(base_size = 10) +
  theme(legend.position = "top", panel.grid.minor = element_blank(),
        panel.grid.major.x = element_blank(), strip.text = element_text(face = "bold"),
        plot.title = element_text(size = 11))

datos_cul <- merge(data.frame(semana = seq(min(culiacan$semana), max(culiacan$semana))),
                    culiacan, by = "semana", all.x = TRUE, sort = TRUE)
datos_cul$brecha[datos_cul$semana == -1] <- NA_real_
# Un grupo nuevo tras cada hueco impide unir visualmente semanas sin cobertura.
datos_cul$segmento <- cumsum(is.na(datos_cul$brecha))
guardar(datos_cul, "datos_culiacan", "figuras")
g_culiacan <- ggplot(datos_cul, aes(semana, brecha)) +
  annotate("rect", xmin = 1.5, xmax = 6.5, ymin = -Inf, ymax = Inf, fill = "#f2e5d9") +
  geom_hline(yintercept = 0, color = "#686d70", linewidth = 0.3) +
  geom_vline(aes(xintercept = 0, linetype = "Inicio de la crisis"), color = "#686d70", linewidth = 0.4) +
  geom_vline(aes(xintercept = 7, linetype = "Cambio territorial"), color = "#974421", linewidth = 0.4) +
  geom_line(aes(group = segmento), color = "#135a76", linewidth = 0.5, na.rm = TRUE) +
  geom_point(color = "#135a76", size = 1.4, na.rm = TRUE) +
  scale_linetype_manual(values = c("Inicio de la crisis" = "dashed", "Cambio territorial" = "dotted")) +
  labs(title = "Brecha descriptiva semanal de Culiacán", x = "Semana respecto al inicio local",
       y = "Accidentes por semana", linetype = NULL,
       caption = "Sombreado: captación en revisión (25 de septiembre a 27 de octubre de 2024)") +
  theme_minimal(base_size = 10) +
  theme(legend.position = "bottom", panel.grid.minor = element_blank(),
        panel.grid.major.x = element_blank(), plot.title = element_text(size = 11, face = "bold"))

for (extension in c("pdf", "png")) {
  ggsave(file.path(carpeta_salida, "figuras", paste0("causal_dinamica.", extension)),
         g_dinamica, width = 7.35, height = 4.6, dpi = 150, bg = "white")
  ggsave(file.path(carpeta_salida, "figuras", paste0("culiacan.", extension)),
         g_culiacan, width = 7.35, height = 3.4, dpi = 150, bg = "white")
}
writeLines(capture.output(sessionInfo()), file.path(carpeta_salida, "sesion_R.txt"))
cat("\nAnálisis terminado:", nrow(efectos), "estimaciones finales.\n")
print(obtener(agrupacion = "entidad_fecha")[c("efecto", "ee", "ic_inf", "ic_sup", "tratados", "controles", "fechas")], row.names = FALSE)
cat("Resultados y gráficas en:", normalizePath(carpeta_salida), "\n")
```

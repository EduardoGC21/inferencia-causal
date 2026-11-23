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

Se estudian los siniestros viales registrados tras el inicio local de narcoataques en municipios mexicanos entre 2019 y 2025. Se comparan municipios tratados y controles emparejados en un panel de conteos diarios. El modelo usa como base los días -28 a -8 e incluye efectos fijos del día de la semana. En los 77 pares tratados y 32 fechas de inicio, el contraste de los días 0 y 1 estima 0,348 siniestros registrados menos por municipio y día, con un intervalo de confianza del 95 % de [-0,834; 0,139], agrupado por estado y fecha de inicio. El intervalo incluye cero y la presencia de diferencias previas limita la atribución al ataque.

## 1. Contexto y motivación

¿Cómo cambian los accidentes registrados tras el inicio local de narcoataques? La hipótesis es que los bloqueos y la suspensión del transporte reducen la circulación; los desvíos y los cambios al conducir pueden contrarrestar esa caída. La violencia contra transportistas de Chilpancingo en febrero de 2024 ilustra la interrupción del transporte público (Amapola Periodismo, 2024). Se utiliza la Estadística de Accidentes de Tránsito Terrestre en Zonas Urbanas y Suburbanas (ATUS), del Instituto Nacional de Estadística y Geografía (INEGI), que cubre vías no federales (2026a). Su conteo refleja accidentes y captación; no mide riesgo por viaje.

El objetivo es el efecto promedio del tratamiento entre los tratados (ATT): la diferencia entre los registros con y sin el inicio del ataque para los pares municipio–episodio incluidos, con igual peso para cada par. Se distinguen Días 0–1, Días 2–6 y Sem. +1 (Días 7–13). El Día 0 es la fecha del inicio local y puede incluir horas anteriores al ataque; Días 0–1 son dos días naturales, no necesariamente las primeras 48 horas.

Bauernschuster y Rekers (2022) encuentran una reducción de accidentes durante operativos alemanes de velocidad de un día, sin persistencia posterior detectable. Este antecedente motiva separar el cambio inmediato de su duración y revisar el calendario, aunque los mecanismos difieren de los narcoataques. Dell (2015) documenta desplazamientos de rutas del narcotráfico y de la violencia, lo que motiva examinar posibles efectos sobre los controles; no demuestra que hayan ocurrido en esta muestra.

## 2. Datos

### Accidentes y exposición.

Se utilizan los microdatos definitivos de ATUS de 2019–2025 y los últimos meses de 2018 para revisar la cobertura previa (Instituto Nacional de Estadística y Geografía, 2025a, 2026a). En 2019–2025 hay 2 518 436 registros con fecha válida. Se conservan filas con atributos repetidos porque ATUS no proporciona un identificador único de accidente.

La muestra principal contiene 3 613 pares municipio–fecha: 77 tratados y 3 536 controles. Reúne 54 municipios tratados y 765 de control, con posibles repeticiones entre grupos y fechas. Los 31 episodios tienen inicio local en 32 fechas, pues un episodio puede comenzar en fechas distintas según el municipio. Cada regresión reúne los 21 conteos de la base y los conteos de cada día del tramo analizado. Un mismo par aporta observaciones diarias a ambos bloques.

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

Desviación estándar (DE) ponderada entre pares. Las diferencias de medias estandarizadas (DME) utilizan como escala común la raíz del promedio de varianzas de ambos grupos de la referencia con calibre individual. El calibre usa la media de $[-28,-15]$; su DE entre pares difiere de la DE de niveles diarios que estandariza los efectos.

## 3. Estrategia empírica

### Estimando y base.

Sea $t$ la fecha de inicio local y sea $h$ el tramo de días relativos al inicio. $Y_{i,d}$ cuenta los siniestros publicados del municipio $i$ en la fecha calendario $d$. Para cada par, la base $B_{it}$ y el resultado medio $\bar Y_{ith}$ son

$$
B_{it}=\frac{1}{21}\sum_{k=-28}^{-8} Y_{i,t+k},
\qquad
\bar Y_{ith}=\frac{1}{|h|}\sum_{k\in h}Y_{i,t+k}.
$$

La base comprende las semanas -4, -3 y -2 e incluye tres observaciones de cada día de la semana. $|h|$ es el número de días del tramo. En Culiacán, para el inicio del jueves 17 de octubre de 2019, la base abarca del 19 de septiembre al 9 de octubre, inclusive. La semana -1 permite examinar diferencias inmediatamente anteriores al inicio.

Sea $\mathrm{Treat}_{it}$ el indicador de par tratado y $A_{it}$ el de elegibilidad previa. Si $\bar Y_{ith}(1)$ y $\bar Y_{ith}(0)$ son los promedios diarios potenciales con y sin ataque, el objetivo es

$$
\tau_{\mathrm{ATT},h}=E[\bar Y_{ith}(1)-\bar Y_{ith}(0)\mid
\mathrm{Treat}_{it}=1,A_{it}=1,\text{soporte}].
$$

### Comparadores y pesos.

Se excluyen municipios con exposición documentada entre los Días -49 y -1: la regla cubre la base y añade 21 días anteriores a su primera medición. Se supone que los ataques más antiguos ya no afectan la comparación.

Los controles proceden de estados ajenos al episodio. También se excluyen municipios con antecedentes documentados y estados con señales previas sin municipio identificable. Se exige estabilidad territorial desde el inicio de la base hasta la víspera del ataque. La selección principal no utiliza ataques posteriores.

El calibre usa la media de los días -28 a -15. Se exige $(\bar Y_c+0.5)/(\bar Y_i+0.5)\in[0.5,2]$, donde $\bar Y_i$ y $\bar Y_c$ son las medias del tratado y del candidato. La población, el empleo y los automóviles por mil habitantes también deben estar, por separado, entre la mitad y el doble del valor tratado. Se requieren al menos diez candidatos de cinco estados por tratado.

El emparejamiento 1:muchos utiliza todos los candidatos: cada tratado pesa uno y reparte otro peso total de uno entre sus controles. El emparejamiento 1:1 elige el candidato más cercano según población, empleo y automóviles, después de comprobar el mismo mínimo de candidatos y estados. Se permite reutilizar controles; sus pesos acumulan las contribuciones de cada tratado.

### Regresión en el panel diario.

Cada par $i,t$ aporta una fila por fecha calendario $d$ de cada bloque $s$. Se define $\mathrm{Post}_s=1$ para el tramo analizado y $0$ para la base, también en los diagnósticos previos. Si $w_{it}$ es el peso del emparejamiento, cada día recibe $w_{it}/21$ en la base y $w_{it}/|h|$ en el tramo. Así, cada bloque aporta el mismo peso total por par y representa un promedio diario.

$$
\begin{aligned}
Y_{i,d}={}&\alpha_{ith}+\lambda_{th}\mathrm{Post}_s
  +\delta_{h,\operatorname{ds}(d)}\\
 &+\tau_{\mathrm{DD},h}(\mathrm{Treat}_{it}\times\mathrm{Post}_s)
  +(X_{it}'\gamma_h)\mathrm{Post}_s+\varepsilon_{ithsd}.
\end{aligned}
$$

$\alpha_{ith}$ es el efecto fijo del par. $\lambda_{th}\mathrm{Post}_s$ es el efecto fijo de fecha de inicio por bloque, con la base como referencia. $\operatorname{ds}(d)$ identifica el día de la semana de la fecha del conteo y $\delta_{h,\operatorname{ds}(d)}$ es su efecto fijo, con lunes como referencia. La interacción de interés es $D_{its}=\mathrm{Treat}_{it}\mathrm{Post}_s$ (**Tratado × Después**).

Con dos filas agregadas, la composición por día de la semana es idéntica para todos los pares de una fecha de inicio en cada bloque. En esa representación, los efectos de fecha por bloque absorben los indicadores de día de la semana. Las filas diarias aportan variación dentro de la base y permiten estimar seis coeficientes de día de la semana. El apéndice D muestra cómo se ajusta el modelo y se calculan los errores estándar.

El modelo principal $M_0$ omite $X_{it}$ y da el mismo peso a cada par tratado. Bajo los supuestos de identificación, $\tau_{\mathrm{DD},h}=\tau_{\mathrm{ATT},h}$ en $M_0$. $M_1$ añade el logaritmo de la población, $M_2$ el empleo por mil habitantes y $M_3$ los automóviles por mil habitantes. Los cuatro modelos conservan la muestra y los pesos explícitos.

### Identificación y sesgo.

Supuestos no comprobables directamente: sin el ataque, tratados y controles habrían tenido cambios paralelos en el número de siniestros registrados; no habría anticipación en la base, efectos persistentes de ataques anteriores ni efectos de la violencia sobre los controles. El emparejamiento mejora la comparabilidad observada, pero no garantiza esos supuestos. Si fallan, el coeficiente puede incorporar diferencias ajenas al ataque. Los cambios de captación también limitan interpretar los registros como cambios de accidentes reales.

Comprobaciones con la información disponible: fechas, criterios de inclusión y pesos. Los resultados previos y el placebo permiten detectar problemas de comparación; no demostrar tendencias paralelas (Roth, 2022). Como los episodios pueden repetirse, no corresponde suponer automáticamente una adopción permanente del tratamiento (Dube et al., 2025).

### 3.1. Inferencia y separación de estimandos

Se utilizan errores estándar agrupados por estado para admitir dependencia entre municipios del mismo estado a lo largo del tiempo. Los intervalos principales añaden agrupación por fecha de inicio, que admite dependencia entre municipios con la misma fecha. La agrupación cambia la precisión, no el coeficiente ni la muestra.

De los 32 estados, 14 aportan tratados. Se revisa la concentración de peso mediante la omisión de cada estado por turno y un intervalo alternativo. El apéndice D detalla el cálculo y las correcciones por número de grupos (MacKinnon et al., 2023a, 2023b). Estas medidas no corrigen sesgo.

La duración se examina en la muestra principal. Como contraste, se exige continuidad del reporte entre los Días -28 y +13 y ausencia de otra exposición hasta +14; el episodio inicial puede continuar. Esta muestra depende de sucesos posteriores al ataque y puede incorporar selección, por lo que no se interpreta automáticamente como el mismo efecto causal.

## 4. Resultados

### Siniestros registrados en los días 0 y 1.

En los días 0 y 1, $M_0$ con emparejamiento 1:muchos estima 0,348 siniestros registrados menos por municipio y día. El intervalo de confianza del 95 % (IC) agrupado por estado y fecha de inicio es [-0,834; 0,139], con $p=0{,}155$. El intervalo incluye cero. Con agrupación solo por estado, el intervalo es [-0,635; -0,060]. La estimación equivale a -0,094 desviaciones estándar diarias de la base y el efecto mínimo detectable (MDE) es de 0,690 siniestros por municipio y día, con una prueba bilateral al 5 % y potencia del 80 %.

El cuadro 2 presenta la interacción Tratado × Después y los coeficientes de las covariables. El efecto estimado con los cuatro modelos se sitúa entre -0,348 y -0,341 siniestros registrados por municipio y día. El cuadro B1 desglosa los días 0 y 1 y los tramos posteriores.

**Cuadro 2.** Días 0 y 1. Regresiones con ajuste progresivo en la muestra principal

| Variable | $M_0$ | $M_1$ | $M_2$ | $M_3$ |
| :--- | ---: | ---: | ---: | ---: |
| Tratado × Después | -0,348<br>(0,239)<br>[-0,834; 0,139]<br>$p=0{,}155$ | -0,341<br>(0,239)<br>[-0,830; 0,147]<br>$p=0{,}164$ | -0,341<br>(0,244)<br>[-0,839; 0,156]<br>$p=0{,}172$ | -0,343<br>(0,246)<br>[-0,844; 0,158]<br>$p=0{,}173$ |
| Logaritmo de la población | — | -0,077<br>(0,080)<br>[-0,241; 0,086]<br>$p=0{,}342$ | -0,076<br>(0,078)<br>[-0,236; 0,083]<br>$p=0{,}336$ | -0,075<br>(0,076)<br>[-0,229; 0,079]<br>$p=0{,}328$ |
| Empleo por cada mil habitantes | — | — | -0,000026<br>(0,001025)<br>[-0,002116; 0,002063]<br>$p=0{,}980$ | 0,000006<br>(0,001053)<br>[-0,002141; 0,002153]<br>$p=0{,}996$ |
| Automóviles por cada mil habitantes | — | — | — | -0,000117<br>(0,000725)<br>[-0,001595; 0,001362]<br>$p=0{,}873$ |

Cada celda presenta estimación, error estándar entre paréntesis, intervalo de confianza del 95 % y valor $p$ bilateral, con agrupación por estado y fecha de inicio y 31 grados de libertad. Cada modelo utiliza 3 613 pares, 77 tratados y 32 fechas de inicio. Los coeficientes de las covariables corresponden al ajuste estadístico.

### Trayectoria y falsificaciones.

La figura 1 muestra los contrastes de los días -7 a +13. Los días -3 y -2 presentan diferencias de -0,451 y -0,533, con intervalos puntuales que quedan por debajo de cero en el emparejamiento 1:muchos. El contraste de la semana -1 frente a la base principal es -0,157 (IC [-0,316; 0,002]).

**Figura 1. La trayectoria muestra descensos en los días -2 y 1.** Modelo $M_0$, emparejamientos 1:muchos y 1:1. Base de los días -28 a -8. Los intervalos del 95 % son puntuales y se agrupan por estado y fecha de inicio.

![Trayectoria de registros](figuras/trayectoria-siniestros.png)

La prueba conjunta de Wald contrasta las semanas -4, -3 y -1 con la base de los días -28 a -8. En el emparejamiento 1:muchos, el valor $p$ es 0,035 por estado y 0,081 por estado y fecha de inicio. La primera agrupación rechaza la hipótesis conjunta al 5 %. Con la segunda, el resultado es compatible con diferencias previas nulas en el conjunto de semanas. El apéndice D explica por qué bastan tres restricciones.

El placebo asigna un inicio ficticio 28 días antes del observado y reconstruye los criterios de inclusión, el emparejamiento y la base. En los días 0 y 1 estima -0,191 siniestros por municipio y día (IC [-0,569; 0,188]). El intervalo inmediato incluye cero. Los días 2 a 6 y la semana 0 del placebo presentan intervalos por estado que quedan por debajo de cero en el emparejamiento 1:muchos. El cuadro B3 presenta los seis tramos y los valores $p$ de ambas agrupaciones.

### Persistencia y calendario.

Las estimaciones son -0,145 en los días 2 a 6 (IC [-0,353; 0,063]) y -0,079 en la semana +1 (IC [-0,317; 0,158]). Los intervalos incluyen cero y admiten reducciones de magnitud relevante. El cuadro B2 compara estos resultados con los de la muestra que exige continuidad e introduce aislamiento posterior.

El calendario puede alterar la circulación (Cámara de Diputados, 2025; Secretaría de Educación de Veracruz, 2026). Excluir las fechas con un feriado de la Ley Federal del Trabajo (LFT) o un receso de la Secretaría de Educación Pública (SEP) en el día 0 o 1 reduce la muestra a 25 tratados y 15 fechas. El contraste inmediato estima -0,595 siniestros por municipio y día (IC [-1,288; 0,098]). El apéndice C enumera las exclusiones y el soporte de cada escenario.

## 5. Conclusión y validez externa

En los días 0 y 1 se estiman 0,348 siniestros registrados menos por municipio y día (IC del 95 % [-0,834; 0,139], por estado y fecha de inicio). Las estimaciones posteriores son de menor magnitud y sus intervalos incluyen cero. En los días -3 y -2 ya se observaban diferencias entre los grupos. Los resultados son compatibles con cambios en la circulación, la conducción o la captación de los registros. Los datos disponibles miden siniestros publicados en vías no federales y carecen de un denominador de viajes.

El resultado corresponde a 77 pares municipio–inicio documentados entre 2019 y 2025, con igual peso por tratado. Las diferencias previas, la sensibilidad de la inferencia y la cobertura desigual del catálogo limitan la atribución causal y la extrapolación a otros incidentes. Para interpretar la caída de los registros como un cambio en seguridad vial, las autoridades necesitarían contrastar también la movilidad, la atención de emergencias y la captación.

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

**Cuadro A4.** DME con los mismos tratados antes y después del emparejamiento

| Variable           | Antes de emparejar | 1:muchos |    1:1 |
|:-------------------|-------------------:|---------:|-------:|
| Población          |              0,274 |    0,013 |  0,005 |
| Empleo / mil       |              0,269 |    0,070 |  0,027 |
| Autos / mil        |             -0,021 |   -0,082 | -0,023 |
| Accidentes previos |              0,175 |   -0,011 |  0,012 |

La referencia previa incluye controles con datos completos y ponderación uniforme dentro de cada fecha. Las columnas posteriores cambian los vínculos y pesos, con los mismos tratados. La escala de estandarización es común, fijada en la referencia con calibre individual; una DME pequeña no demuestra balance de variables omitidas ni paralelismo.

**Cuadro A5.** Días 0–1: $M_0$–$M_3$, muestra fija

| Controles | Modelo | Trat. | $N$ | Estimación e IC por estado y fecha |
| :--- | ---: | ---: | ---: | ---: |
| Completos, calibre | $M_0$ | 82 | 13 977 | -0,393 [-0,857; 0,071] |
| Completos, calibre | $M_1$ | 82 | 13 977 | -0,361 [-0,827; 0,104] |
| Completos, calibre | $M_2$ | 82 | 13 977 | -0,359 [-0,820; 0,102] |
| Completos, calibre | $M_3$ | 82 | 13 977 | -0,364 [-0,841; 0,113] |
| Sin emparejar | $M_0$ | 77 | 22 561 | -0,385 [-0,820; 0,050] |
| Sin emparejar | $M_1$ | 77 | 22 561 | -0,298 [-0,623; 0,027] |
| Sin emparejar | $M_2$ | 77 | 22 561 | -0,298 [-0,623; 0,027] |
| Sin emparejar | $M_3$ | 77 | 22 561 | -0,310 [-0,656; 0,035] |
| 1:muchos | $M_0$ | 77 | 3 613 | -0,348 [-0,834; 0,139] |
| 1:muchos | $M_1$ | 77 | 3 613 | -0,341 [-0,830; 0,147] |
| 1:muchos | $M_2$ | 77 | 3 613 | -0,341 [-0,839; 0,156] |
| 1:muchos | $M_3$ | 77 | 3 613 | -0,343 [-0,844; 0,158] |
| 1:1 | $M_0$ | 77 | 154 | -0,311 [-0,820; 0,198] |
| 1:1 | $M_1$ | 77 | 154 | -0,312 [-0,829; 0,206] |
| 1:1 | $M_2$ | 77 | 154 | -0,315 [-0,840; 0,210] |
| 1:1 | $M_3$ | 77 | 154 | -0,320 [-0,858; 0,217] |

$M_0$ incluye la interacción de tratamiento y los efectos fijos. $M_1$ añade el logaritmo de la población, $M_2$ el empleo por mil habitantes y $M_3$ los automóviles por mil habitantes. La muestra completa exige covariables utilizables y calibre individual, sin los tres intervalos adicionales del emparejamiento; conserva todos los tratados con ese soporte. Cada progresión usa exactamente sus mismos pares y pesos. La referencia sin emparejamiento mantiene los mismos tratados y controles completos, con pesos uniformes por fecha. Los dos esquemas comparten tratados, no controles. Las DME del cuadro 1 usan una escala común fijada antes del emparejamiento.

## Apéndice B. Contrastes principales, persistencia y placebo

**Cuadro B1.** Contrastes principales, emparejamiento 1:muchos

| Tramo | $\hat\tau$ (EE estatal) | IC del 95 % por estado y fecha | $\tau/\sigma$ | MDE por estado y fecha |
| :--- | ---: | ---: | ---: | ---: |
| Día 0 | -0,224 (0,174) | [-0,872; 0,424] | -0,061 | 0,919 |
| Día 1 | -0,471 (0,148) | [-0,934; -0,008] | -0,128 | 0,657 |
| Días 0–1 | -0,348 (0,141) | [-0,834; 0,139] | -0,094 | 0,690 |
| Días 2–6 | -0,145 (0,057) | [-0,353; 0,063] | -0,039 | 0,295 |
| Sem. 0 | -0,203 (0,070) | [-0,448; 0,042] | -0,055 | 0,347 |
| Sem. +1 | -0,079 (0,057) | [-0,317; 0,158] | -0,022 | 0,336 |

Los errores estándar (EE), entre paréntesis, se agrupan por estado. Los intervalos de confianza (IC) del 95 % se agrupan por estado y fecha; por eso no se calculan a partir de los EE entre paréntesis. El modelo $M_0$ utiliza 3 613 pares municipio–fecha. Los tramos son promedios diarios. La columna $\tau/\sigma$ divide el coeficiente por la desviación estándar diaria del resultado en $[-28,-8]$, calculada con divisor $n-1$; en niveles, esa desviación es de 3,68. El efecto mínimo detectable (MDE) se explica en el apéndice D.

**Cuadro B2.** Selección y horizontes. Intervalos por estado y fecha de inicio

| Selección | Método | Trat. | Días 0–1 | Días 2–6 | Sem. +1 |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Principal | 1:muchos | 77 | -0,348 [-0,834; 0,139] | -0,145 [-0,353; 0,063] | -0,079 [-0,317; 0,158] |
| Principal | 1:1 | 77 | -0,311 [-0,820; 0,198] | -0,108 [-0,425; 0,208] | -0,181 [-0,572; 0,210] |
| Aislamiento posterior | 1:muchos | 69 | -0,444 [-0,968; 0,080] | -0,083 [-0,266; 0,100] | -0,094 [-0,358; 0,169] |
| Aislamiento posterior | 1:1 | 69 | -0,330 [-0,879; 0,219] | -0,080 [-0,422; 0,263] | -0,222 [-0,649; 0,206] |
| Placebo 28 días antes | 1:muchos | 81 | -0,191 [-0,569; 0,188] | -0,136 [-0,306; 0,033] | -0,032 [-0,148; 0,085] |
| Placebo 28 días antes | 1:1 | 81 | -0,460 [-0,990; 0,070] | -0,144 [-0,458; 0,170] | -0,059 [-0,282; 0,164] |

La muestra con aislamiento posterior exige cobertura $[-28,+13]$ y ausencia de otra exposición hasta +14. Sus diferencias incorporan selección posterior. El placebo reconstruye la muestra en $t-28$; sus tamaños no tienen que coincidir con los reales.

**Cuadro B3.** Placebo 28 días antes: efectos por periodo

| Horizonte | 1:muchos, IC doble | $p$ doble | $p$ estatal | 1:1, IC doble | $p$ doble | $p$ estatal |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Día 0 | -0,244 [-0,653; 0,165] | 0,233 | 0,121 | -0,447 [-1,095; 0,200] | 0,168 | 0,150 |
| Día 1 | -0,138 [-0,616; 0,341] | 0,562 | 0,322 | -0,472 [-1,105; 0,161] | 0,138 | 0,090 |
| Días 0–1 | -0,191 [-0,569; 0,188] | 0,312 | 0,140 | -0,460 [-0,990; 0,070] | 0,086 | 0,065 |
| Días 2–6 | -0,136 [-0,306; 0,033] | 0,112 | 0,015 | -0,144 [-0,458; 0,170] | 0,357 | 0,266 |
| Sem. 0 | -0,152 [-0,328; 0,023] | 0,087 | 0,022 | -0,234 [-0,509; 0,041] | 0,092 | 0,061 |
| Sem. +1 | -0,032 [-0,148; 0,085] | 0,583 | 0,397 | -0,059 [-0,282; 0,164] | 0,590 | 0,584 |

Los valores $p$ estatales permiten revisar la sensibilidad a la agrupación. `causal_fechas_base.csv` registra cada fecha de base, su día de la semana y el inicio real o ficticio correspondiente. `causal_efectos.csv` incluye los días individuales del -7 al +13.

## Apéndice C. Sensibilidades y calendario

**Cuadro C1.** Días 0–1: exclusiones, IC: estado y fecha

| Exclusión / muestra | Método | Trat. | Fechas | Estimación e IC por estado y fecha |
| :--- | ---: | ---: | ---: | ---: |
| Principal | 1:muchos | 77 | 32 | -0,348 [-0,834; 0,139] |
| Principal | 1:1 | 77 | 32 | -0,311 [-0,820; 0,198] |
| Cinco fechas de auditoría | 1:muchos | 56 | 27 | -0,426 [-0,816; -0,036] |
| Cinco fechas de auditoría | 1:1 | 56 | 27 | -0,431 [-0,799; -0,062] |
| Sin feriados LFT | 1:muchos | 73 | 30 | -0,431 [-0,949; 0,087] |
| Sin feriados LFT | 1:1 | 73 | 30 | -0,308 [-0,842; 0,227] |
| Sin LFT ni recesos SEP | 1:muchos | 25 | 15 | -0,595 [-1,288; 0,098] |
| Sin LFT ni recesos SEP | 1:1 | 25 | 15 | -0,607 [-1,307; 0,094] |
| Sin dos tratados pendientes | 1:muchos | 75 | 32 | -0,354 [-0,851; 0,142] |
| Sin dos tratados pendientes | 1:1 | 75 | 32 | -0,322 [-0,837; 0,193] |
| Sin cuatro casos pendientes | 1:muchos | 74 | 32 | -0,354 [-0,857; 0,150] |
| Sin cuatro casos pendientes | 1:1 | 74 | 32 | -0,318 [-0,840; 0,204] |
| Sin dos señales en controles | 1:muchos | 77 | 32 | -0,348 [-0,834; 0,139] |
| Sin dos señales en controles | 1:1 | 77 | 32 | -0,289 [-0,812; 0,234] |

Las cinco fechas son 31/12/2019, 05/01/2023, 09/04/2023, 07/01/2024 y 23/04/2025. La regla amplia se aplica al día 0 o 1 sin eliminar automáticamente domingos. Se distinguen vacaciones, talleres, suspensiones y receso extraordinario de 2020; no se llama vacaciones a toda la educación a distancia.

Se excluyen por separado dos municipios de Michoacán: Chilchota (14/07/2021) y Contepec (23/04/2025). Se añade excluir los cuatro casos pendientes: también Huaniqueo, Michoacán (23/04/2025), y San Fernando, Tamaulipas (30/04/2023). San Fernando entra en la muestra principal; Huaniqueo sigue fuera por elegibilidad previa. Las señales son Centro, Tabasco (01–02/04/2025), y Coatzacoalcos, Veracruz (20/08/2022). Se elimina su contribución si intersecta $[t-49,t+14]$ y se reconstruyen emparejamiento y pesos. Coatzacoalcos ocurrió después del 09/08/2022: es una sensibilidad ex post explícita, no un filtro del principal. El cotejo anterior cubrió 27 pares de cuatro fechas. ACLED devolvió HTTP 403: no existe verificación exhaustiva y una búsqueda sin señal no demuestra ausencia.

**Cuadro C2.** Soporte de los escenarios

| Escenario                    |   Método | Trat. | Cont. | Fechas | Episodios |
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

## Apéndice D. Inferencia y potencia

La estimación de varianza robusta por conglomerados (CRV1) aplica el factor $\frac{G}{G-1}\frac{N-1}{N-F-K}$. $N$ cuenta pares municipio–fecha de inicio, $F$ cuenta fechas de inicio y $K$ es el rango de los regresores del contraste tras absorber esas fechas. Para la agrupación estatal, $G$ cuenta estados. Para agrupar por estado y fecha, se suman sus dos componentes de covarianza y se resta el de la intersección. Se toma $G$ como el menor de los dos recuentos y se usa una distribución $t$ con $G-1$ grados de libertad para los intervalos.

### Cálculo con conteos diarios.

Para estimar los efectos del día de la semana, se centran sus indicadores en cada fecha de inicio y bloque y se usan los conteos y los pesos diarios. Los indicadores centrados suman cero dentro de cada par y bloque. Con ello son ortogonales tanto a los efectos de par y fecha por bloque como a los regresores que varían solo entre bloques. Se estiman por separado los seis efectos de día de la semana y el contraste ponderado de las medias de bloque ajustadas por esos efectos.

La diferencia entre las medias de los efectos del día de la semana es común a los pares de una misma fecha de inicio. El efecto de fecha la absorbe en el contraste. Las contribuciones de las desviaciones de cada día respecto a su bloque suman cero dentro del par y, por tanto, también dentro de cada conglomerado. Los coeficientes del contraste y su covarianza agrupada surgen así del componente entre bloques. Para la corrección de muestra finita, se cuentan los $N$ pares y el rango $F+K$ de ese componente. Los efectos semanales se estiman en el componente diario ortogonal. En $M_0$ para los días 0 y 1, el panel tiene 83 099 filas y la corrección usa $N=3\,613$, $F=32$, $K=1$ y $G=32$.

La alternativa CRV3 omite cada estado por turno, mantiene los pesos de los casos restantes y vuelve a estimar el contraste dentro de cada fecha. La ortogonalidad descrita también vale en cada réplica. Si $\hat\tau$ es el coeficiente con la muestra completa y $\hat\tau_{-g}$ el coeficiente sin el estado $g$, su varianza es

$$
\widehat V_{\mathrm{CRV3}}=\frac{G-1}{G}\sum_{g=1}^{G}(\hat\tau_{-g}-\hat\tau)^2.
$$

El cálculo se centra en el coeficiente completo y difiere de una variante centrada en la media de las estimaciones por omisión (MacKinnon et al., 2023a, 2023b).

### Efecto mínimo detectable.

El efecto mínimo detectable (MDE) es la magnitud que la prueba detectaría con una probabilidad del 80 %, bajo los supuestos del cálculo. Se utiliza una prueba bilateral al 5 %, errores estándar fijos y una distribución $t$ no central. En el cuadro D1, los umbrales de la especificación principal equivalen al 19,9 % de la media previa con agrupación estatal y al 33,7 % con agrupación por estado y fecha de inicio. La media previa es de 2,05 siniestros por municipio y día.

**Cuadro D1.** Días 0–1: agrupamiento, CRV3 y MDE

| Método | Inferencia | Días 0–1, IC 95% | gl | MDE |
| :--- | ---: | ---: | ---: | ---: |
| 1:muchos | CRV1 estatal | -0,348 [-0,635; -0,060] | 31 | 0,408 |
| 1:muchos | CRV1: estado y fecha | -0,348 [-0,834; 0,139] | 31 | 0,690 |
| 1:muchos | CRV3 estatal | -0,348 [-0,950; 0,255] | 31 | 0,854 |
| 1:1 | CRV1 estatal | -0,311 [-0,706; 0,084] | 27 | 0,559 |
| 1:1 | CRV1: estado y fecha | -0,311 [-0,820; 0,198] | 27 | 0,721 |
| 1:1 | CRV3 estatal | -0,311 [-0,912; 0,290] | 27 | 0,851 |

**Cuadro D2.** Wald semanal de tres restricciones

| Método | Agrupación | F | p | Rango | Condición | Cálculo |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1:muchos | Estatal | 3,238 | 0,035 | 3 | 8,1 | calculada |
| 1:muchos | Estado y fecha | 2,459 | 0,081 | 3 | 5,1 | calculada |
| 1:1 | Estatal | 1,369 | 0,273 | 3 | 29,8 | calculada |
| 1:1 | Estado y fecha | 1,043 | 0,389 | 3 | 15,3 | calculada |

La prueba compara las semanas -4, -3 y -1 con la base común de los días -28 a -8. Cada contraste compara siete conteos diarios con el promedio de los 21 días de la base. Las diferencias de las semanas -4, -3 y -2 respecto a ese promedio suman cero. La semana -2 queda implícita. La prueba conjunta incorpora la covarianza entre los tres coeficientes.

**Cuadro D3.** Omisión de estados, $M_0$ y 1:muchos

| Estado omitido | Días 0–1 | Estado omitido | Días 0–1 |
| :--- | ---: | :--- | ---: |
| Aguascalientes | -0,379 | Morelos | -0,341 |
| Baja California | -0,337 | Nayarit | -0,363 |
| Baja California Sur | -0,340 | Nuevo León | -0,365 |
| Campeche | -0,351 | Oaxaca | -0,348 |
| Coahuila | -0,349 | Puebla | -0,349 |
| Colima | -0,344 | Querétaro | -0,350 |
| Chiapas | -0,343 | Quintana Roo | -0,358 |
| Chihuahua | -0,351 | San Luis Potosí | -0,357 |
| Ciudad de México | -0,354 | Sinaloa | -0,119 |
| Durango | -0,344 | Sonora | -0,359 |
| Guanajuato | -0,320 | Tabasco | -0,330 |
| Guerrero | -0,344 | Tamaulipas | -0,384 |
| Hidalgo | -0,350 | Tlaxcala | -0,349 |
| Jalisco | -0,346 | Veracruz | -0,361 |
| Estado de México | -0,321 | Yucatán | -0,343 |
| Michoacán | -0,528 | Zacatecas | -0,345 |

Las réplicas mantienen pesos originales y vuelven a absorber las fechas. No se fuerza igualdad de masas después de omitir un estado: renormalizar o repetir el emparejamiento sería otro estimador, no el CRV3 anunciado. Se exportan 1:1 y $M_1$–$M_3$.

## Apéndice E. Construcción del catálogo y reproducción

### Catálogo de ataques.

Las búsquedas originales cubrieron tres regiones (norte, occidente y centro, sur y oriente) y tres periodos (2019–2021, 2022–2023 y 2024–2025). Tres subagentes de IA registraron consultas, enlaces, fechas de publicación y consulta, lugares y evidencia; los cotejos entre agentes examinaron casos de regiones distintas. Se buscaron dos orígenes informativos independientes para corroborar municipio y fecha: republicar un mismo boletín no constituye otra fuente. Una jornada que cruza medianoche puede tener fechas municipales distintas. Las discrepancias y corroboraciones pendientes se conservan en el catálogo.

Se utilizó el modelo «Sol 6.2», con la configuración «xhigh» y el modo «fast». Las bitácoras documentan las búsquedas y los cotejos, pero no registran la configuración del modelo.

Los cotejos documentados corresponden a agentes de IA; no se presentan como una validación humana exhaustiva. La prensa puede omitir episodios y una búsqueda sin hallazgos no acredita ausencia de ataques en los controles. Esta asistencia se usó para construir el catálogo de exposición, no para generar registros de accidentes ni covariables municipales, que provienen de las fuentes oficiales descritas en la sección 2.

### Reproducción del análisis.

El paquete `src/choques/`, configuración y pruebas acompañan al escrito. `README.md` documenta Python 3.13.2, dependencias y compilador. ATUS y los cien originales municipales deben corresponder a sus manifiestos: una edición nueva en la misma URL no los sustituye. Las entradas son `data/inputs/episodios.csv` y `data/inputs/fuentes_eventos.csv`, reconstruidas desde las hojas de evidencia. Las rutas parten de la carpeta que contiene `repo/`, `data/` y `tasks/`.

El comando `estimar` reconstruye la muestra y ajusta el panel diario. La opción `--arranque` verifica las fechas, el rango y los pesos, y compara el ajuste con una regresión diaria explícita en dos fechas de inicio. `cotejar-panel` confronta las salidas de Python y R, incluidos los días individuales, los tramos, el placebo y la prueba conjunta de Wald. Las instrucciones y la evidencia reproducible están en `reporte/verificacion/niveles-base-semanal.md`.

Los datos públicos se enlazan en la bibliografía y los manifiestos fijan sus ediciones. El apéndice H incluye el código R completo y los enlaces al repositorio y a la carpeta de entrega de datos.

## Apéndice F. Contexto geográfico de la muestra

La figura 2 ubica los municipios de la muestra principal y muestra su distribución territorial.

**Figura 2.** Municipios tratados y controles de la muestra principal. Naranja: 54 municipios tratados; azul: 765 municipios de control. Un municipio puede aparecer en ambos grupos en fechas distintas: ocurre en 47 casos. El gris indica que no pertenece al grupo de ese panel. El color identifica la participación en la muestra.

![Municipios tratados y controles](figuras/mapa-municipios.png)

El mapa reúne las 32 fechas de inicio entre octubre de 2019 y octubre de 2025; los conteos únicos difieren de los 77 pares tratados y 3 536 pares de control municipio–fecha. Entre los lugares tratados están Culiacán, Sinaloa; Morelia, Michoacán; y Reynosa, Tamaulipas. Tijuana, Baja California, aparece en el grupo de control. La cartografía de referencia procede del Marco Geoestadístico del INEGI, diciembre de 2025, y del servicio del catálogo municipal. Sirve para ubicar los municipios; no reconstruye sus límites históricos ni representa riesgo por superficie. Se usa una proyección equirectangular con paralelo de referencia en 23 grados norte, sin calcular áreas o distancias.

## Apéndice G. Análisis exploratorio por horario y gravedad

El cuadro G1 compara, por gravedad, el cambio de accidentes registrados de noche con el de día en los Días 0–1 de la muestra principal. Se define el día de 06:00 a 17:59 y la noche de 18:00 a 05:59. Cada cifra resta dos cambios estimados, no los conteos nocturnos y diurnos. Un valor negativo indica una reducción relativa mayor de noche, o un aumento menor; uno positivo indica lo contrario.

En ambos emparejamientos, los tres intervalos de confianza incluyen cero. Los contrastes por gravedad permiten examinar si la diferencia entre la noche y el día se concentra en alguna clase de siniestro. Los registros con hora desconocida permanecen en el total. No se ajusta la inferencia por las comparaciones múltiples, por lo que los resultados son exploratorios.

**Cuadro G1.** Días 0–1: noche menos día por gravedad

| Gravedad | 1:muchos: noche menos día | 1:1: noche menos día |
| :--- | ---: | ---: |
| Fatal | -0,011 [-0,036; 0,013] | -0,026 [-0,061; 0,008] |
| Con heridos | 0,082 [-0,012; 0,177] | 0,051 [-0,097; 0,199] |
| Solo daños | -0,104 [-0,270; 0,061] | -0,036 [-0,334; 0,261] |

Registros por municipio y día; IC del 95 % agrupados por estado y fecha.

## Apéndice H. Código reproducible en R

Se incluye el archivo completo `codigo_R/analisis.R`. La obtención y limpieza de los datos se realizan en Python. Este archivo reconstruye las muestras, el emparejamiento, los pesos y las estimaciones a partir del paquete de datos limpios.

La ejecución ordinaria ajusta el panel diario con conteos en niveles, la base de 21 días y efectos fijos del día de la semana. El argumento `--arranque` verifica fechas, pesos y rango del modelo en dos fechas reales. El programa exporta los efectos, el diagnóstico semanal, las sensibilidades y el contraste por franja y gravedad.

El subcomando `python -m choques cotejar-panel` coteja muestras, pesos, estimaciones e inferencia de Python y R. El registro `reporte/verificacion/niveles-base-semanal.json` identifica las salidas y las diferencias máximas por estadístico.

### Código, datos y ejecución.

Repositorio de código e instrucciones: <https://github.com/EduardoGC21/inferencia-causal>.

Carpeta de entrega de datos: <https://drive.google.com/drive/folders/19fPf9UVt5Vdm-h2LiM2sBdD9erg0qItu?usp=sharing>.

Para reproducir el análisis, descargar y descomprimir `datos_limpios_R.zip`, instalar los paquetes `data.table`, `R.utils` y `ggplot2`, y ejecutar desde la raíz del repositorio: `Rscript codigo_R/analisis.R RUTA/datos_limpios_R RUTA/resultados_R`. Las rutas se sustituyen por las carpetas de entrada y salida elegidas; las instrucciones también aparecen al inicio del código. La ejecución verificada utilizó R 4.6.1.

### Listado completo de `codigo_R/analisis.R`.

```r
# Violencia criminal y accidentes registrados, 2019-2025
# Código reproducible del análisis final y de la trayectoria del reporte.
# Ingesta, clasificación y limpieza: Python. Análisis estadístico: este archivo.
# No necesita Python ni lee coeficientes, muestras o pesos precalculados.
#
# 1. Descomprime datos_limpios_R.zip (el paquete para compartir por Drive).
# 2. Instala una vez: install.packages(c("data.table", "R.utils", "ggplot2"))
# 3. Desde la raíz del repositorio:
#    Rscript codigo_R/analisis.R RUTA/datos_limpios_R RUTA/resultados_R
#    Añade --arranque para comprobar fechas, pesos y rango con dos cohortes.
# También puedes cambiar las dos rutas siguientes y ejecutar todo desde RStudio.
# Las salidas siempre van a la carpeta indicada; no modifica reporte/ ni Python.
# Verificado con R 4.6.1, data.table 1.18.4 y ggplot2 4.0.3.

# 1. Rutas, paquetes y parámetros -------------------------------------------

carpeta_datos <- "datos_limpios_R"
carpeta_salida <- "resultados_R"
argumentos <- commandArgs(trailingOnly = TRUE)
if (length(argumentos) >= 1) carpeta_datos <- argumentos[1]
if (length(argumentos) >= 2) carpeta_salida <- argumentos[2]
arranque <- identical(argumentos[3], "--arranque")

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

adjuntar_covariables <- function(muestra, persistencia = FALSE) {
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
    fin <- indice + if (persistencia) 14 else -1
    inicio <- indice - 28
    cohorte$territorio <- territorios(cohorte$clave,
                                     if (!persistencia) fin else indice, TRUE)
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
  entidades <- muestra$estado
  pesos <- muestra$peso
  z <- cbind(x, y)
  sumas <- rowsum(z * pesos, grupos, reorder = TRUE)
  masas <- rowsum(pesos, grupos, reorder = TRUE)[, 1]
  dentro <- z - (sumas / masas)[grupos, , drop = FALSE]
  dentro <- dentro * sqrt(pesos)
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
  # N pares y rango del contraste entre bloques. Los efectos semanales
  # se ajustan en el componente diario ortogonal al contraste.
  correccion <- (n - 1) / (n - f - length(independientes))
  carne <- function(grupo) crossprod(rowsum(puntuaciones, grupo, reorder = FALSE))
  expandir <- function(v) {
    completa <- matrix(NA_real_, k * m, k * m)
    completa[posiciones, posiciones] <- v
    completa
  }
  v_estado <- carne(entidades)
  covarianzas$entidad <- expandir(v_estado * correccion * g / (g - 1))
  gl["entidad"] <- g - 1
  if (f >= 6) {
    menor <- min(g, f)
    v_fecha <- carne(grupos)
    v_interseccion <- carne(paste(entidades, grupos))
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

# 7. Panel diario en niveles y pruebas previas -----------------------------

dias_base <- -28:-8
tramos_semanales <- list("wk-4" = -28:-22, "wk-3" = -21:-15, "wk-1" = -7:-1)
dia_semana <- function(fecha) (as.integer(fecha) + 3L) %% 7L  # Lunes = 0.
promedio_vectores <- function(lista) Reduce("+", lista) / length(lista)

cambios_panel <- function(muestra, diario, horizontes) {
  fechas_indice <- sort(unique(muestra$indice))
  grupo <- match(muestra$indice, fechas_indice)
  pesos <- muestra$peso
  masas <- as.vector(rowsum(pesos, grupo))
  indicadores <- diag(7)[, -1, drop = FALSE]
  # Cada bloque reparte el peso original por igual entre sus días.
  # Los indicadores centrados en fecha y bloque son ortogonales a los
  # efectos de par y a todos los regresores que solo cambian entre bloques.
  bloque <- function(dias) {
    y <- diario[as.character(dias)]
    stopifnot(all(vapply(y, function(z) all(is.finite(z)), logical(1))))
    dias_semana <- outer(dias, dia_semana(fechas_indice), "+") %% 7L
    d <- lapply(seq_along(dias), function(j) indicadores[dias_semana[j, ] + 1L, , drop = FALSE])
    perfil <- promedio_vectores(d)
    centrados <- lapply(d, function(z) z - perfil)
    gram <- promedio_vectores(lapply(centrados, function(z) crossprod(z, z * masas)))
    rhs <- promedio_vectores(Map(function(z, valores) {
      crossprod(z, rowsum(valores * pesos, grupo))
    }, centrados, y))
    list(media = promedio_vectores(y), perfil = perfil, gram = gram, rhs = rhs)
  }
  inicial <- bloque(dias_base)
  calculos <- lapply(seq_along(horizontes), function(j) {
    dias <- horizontes[[j]]
    final <- bloque(dias)
    gram <- inicial$gram + final$gram
    espectro <- eigen(gram, symmetric = TRUE)
    retenidos <- espectro$values > 6 * max(abs(espectro$values)) * .Machine$double.eps
    rango <- sum(retenidos)
    stopifnot(rango == 6)
    vectores <- espectro$vectors[, retenidos, drop = FALSE]
    gamma <- vectores %*% (crossprod(vectores, inicial$rhs + final$rhs) / espectro$values[retenidos])
    ajuste <- ((final$perfil - inicial$perfil) %*% gamma)[grupo, , drop = FALSE]
    diagnostico <- data.frame(tramo = names(horizontes)[j], dias_base = length(dias_base),
                              dias_tramo = length(dias), filas = nrow(muestra) * (length(dias_base) + length(dias)),
                              rango_dia_semana = rango, as.list(setNames(gamma[, 1], paste0("d", 1:6))))
    list(y = final$media - inicial$media - ajuste, diagnostico = diagnostico)
  })
  list(y = do.call(cbind, lapply(calculos, "[[", "y")),
       diagnosticos = unir_filas(lapply(calculos, "[[", "diagnostico")))
}

comprobar_arranque <- function(muestra) {
  indices <- sort(unique(muestra$indice))[1:2]
  elegidos <- muestra[muestra$indice %in% indices, ]
  filas <- unlist(lapply(split(seq_len(nrow(elegidos)), list(elegidos$indice, elegidos$tratado)), head, 3))
  elegidos <- elegidos[filas, ]
  n <- nrow(elegidos)
  stopifnot(identical(dias_base, -28:-8),
            identical(dia_semana(as.Date("2025-04-21") + 0:6), 0:6))
  bloques <- list(dias_base, 0:1)
  offsets <- unlist(bloques)
  diario <- setNames(lapply(offsets, function(h) matrix(extraer(elegidos, h), ncol = 1)), offsets)
  post <- rep(0:1, lengths(bloques))
  pesos <- sapply(seq_along(offsets), function(j) elegidos$peso / length(bloques[[post[j] + 1]]))
  stopifnot(all(abs(rowSums(pesos[, 1:21]) - elegidos$peso) < 1e-12),
            all(abs(rowSums(pesos[, 22:23]) - elegidos$peso) < 1e-12))
  dias <- sapply(offsets, function(h) dia_semana(elegidos$indice + h))
  stopifnot(all(apply(dias[, 1:21], 1, function(d) all(tabulate(d + 1L, 7) == 3))))
  celdas <- outer(elegidos$indice, indices, "==") * 1
  perfil <- function(columnas) {
    Reduce("+", lapply(columnas, function(j) diag(7)[dias[, j] + 1L, -1])) / length(columnas)
  }
  agregado <- rbind(perfil(1:21), perfil(22:23))
  ceros <- celdas * 0
  fechas_bloque <- rbind(cbind(celdas, ceros), cbind(ceros, celdas))
  absorbidos <- rango_matriz(cbind(fechas_bloque, agregado)) - rango_matriz(fechas_bloque)
  x <- do.call(rbind, lapply(seq_along(offsets), function(j) {
    cbind(diag(n), celdas * post[j], elegidos$tratado * post[j], diag(7)[dias[, j] + 1L, -1])
  }))
  rank <- rango_matriz(x) - rango_matriz(x[, seq_len(ncol(x) - 6)])
  stopifnot(absorbidos == 0, rank == 6)
  ajuste <- cambios_panel(elegidos, diario, list("d0..1" = 0:1))
  reducido <- c(estimar(elegidos, "tratado", ajuste$y, FALSE)$b[1, 1],
                unlist(ajuste$diagnosticos[paste0("d", 1:6)]))
  completo <- tail(lm.wfit(x, unlist(diario), as.vector(pesos))$coefficients, 7)
  error <- max(abs(completo - reducido))
  stopifnot(error < 1e-10)
  guardar(data.frame(pares = n, fechas = length(indices), dias_base = length(dias_base),
                     dia_semana = "lunes=0", rango_incremental_agregado = absorbidos,
                     rango_incremental_diario = rank, diferencia_maxima_ajuste_explicito = error), "arranque")
  cat("Arranque: 21 días, masa por bloque y seis efectos de día de la semana comprobados.\n")
}

resultados <- function(muestra, diario, modelos = 0, crv3 = FALSE) {
  horizonte <- tramos
  panel <- cambios_panel(muestra, diario, horizonte)
  y <- panel$y
  resumen <- resumir(muestra)
  previa <- unlist(lapply(diario[as.character(dias_base)], function(z) z[muestra$tratado == 1, 1]))
  sigma <- sd(previa)
  media <- mean(previa)
  filas <- omisiones <- terminos <- list()
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
          estado_omitido = entidades[i], modelo = paste0("M", modelo), tramo = names(horizonte),
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
        data.frame(modelo = paste0("M", modelo), tramo = names(horizonte), agrupacion,
                   base = "tres_semanas", escala = "niveles"), resumen[rep(1, ncol(y)), ], estadisticas,
        sigma_pre = sigma, media_pre = media, estado_inferencia = estado,
        efecto_sigma = estadisticas$efecto / sigma,
        mde = mde(ajuste$gl[agrupacion], estadisticas$ee))
      if (agrupacion == "entidad_fecha" && crv3) {
        j <- match("d0..1", names(horizonte))
        idx <- (j - 1) * length(columnas) + seq_along(columnas)
        terminos[[length(terminos) + 1]] <- cbind(
          data.frame(modelo = paste0("M", modelo), termino = columnas, tramo = "d0..1", agrupacion),
          intervalo(ajuste$b[j, ], if (is.null(v)) NA_real_ else diag(v)[idx], ajuste$gl[agrupacion]))
      }
    }
  }
  list(efectos = unir_filas(filas), omisiones = unir_filas(omisiones),
       diagnosticos = panel$diagnosticos, terminos = unir_filas(terminos))
}

pruebas_semanales <- function(muestra, diario) {
  # Las tres semanas de base suman cero frente a su propio promedio.
  # Al omitir la semana -2 conservamos tres restricciones independientes.
  panel <- cambios_panel(muestra, diario, tramos_semanales)
  ajuste <- estimar(muestra, "tratado", panel$y)
  filas <- list()
  for (agrupacion in names(ajuste$v)) {
    v <- ajuste$v[[agrupacion]]
    eigen_min <- if (is.null(v)) NA_real_ else min(eigen(v, symmetric = TRUE, only.values = TRUE)$values)
    condicion <- if (is.null(v)) NA_real_ else {
      d <- svd(v, nu = 0, nv = 0)$d
      max(d) / min(d)
    }
    filas[[length(filas) + 1]] <- cbind(data.frame(
      escala = "niveles", agrupacion, referencia = "tres_semanas [-28,-8]", restricciones = "wk-4;wk-3;wk-1",
      rango = if (is.null(v)) 0 else rango_matriz(v), condicion, autovalor_min = eigen_min),
      wald(ajuste$b[, 1], v, ajuste$gl[agrupacion]))
    individuales <- intervalo(ajuste$b[, 1], if (is.null(v)) rep(NA_real_, 3) else diag(v),
                              ajuste$gl[agrupacion])
    filas[[length(filas) + 1]] <- cbind(data.frame(
      escala = "niveles", agrupacion, referencia = "tres_semanas [-28,-8]", restricciones = names(tramos_semanales)),
      individuales)
  }
  list(pruebas = unir_filas(filas), diagnosticos = panel$diagnosticos)
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
  if (arranque) {
    comprobar_arranque(muchos$muestra)
    quit(save = "no")
  }
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

efectos <- omisiones <- pruebas <- registros_muestra <- rangos <- terminos <- list()
for (escenario in names(muestras)) {
  for (metodo in names(muestras[[escenario]])) {
    cat("Estimación:", escenario, metodo, "\n")
    muestra <- muestras[[escenario]][[metodo]]
    registros_muestra[[paste(escenario, metodo)]] <- transform(muestra, escenario = escenario, muestra = metodo)
    if (!nrow(muestra)) next
    offsets <- -28:13
    diario <- setNames(lapply(offsets, function(h) matrix(extraer(muestra, h), ncol = 1)), offsets)
    stopifnot(all(vapply(diario, function(z) all(z >= 0), logical(1))))
    principal <- escenario == "principal"
    modelos <- if (metodo != "sin_covariables" && principal) 0:3 else 0
    ajuste <- resultados(muestra, diario, modelos, crv3 = principal)
    llave <- paste(escenario, metodo)
    efectos[[llave]] <- transform(ajuste$efectos, escenario = escenario, muestra = metodo)
    rangos[[llave]] <- transform(ajuste$diagnosticos, escenario = escenario, muestra = metodo,
                                 base = "tres_semanas")
    if (nrow(ajuste$omisiones)) {
      omisiones[[llave]] <- transform(ajuste$omisiones, escala = "niveles", muestra = metodo)
      terminos[[llave]] <- transform(ajuste$terminos, escenario = escenario, muestra = metodo)
    }
    if (escenario %in% c("principal", "persistencia", "placebo")) {
      previo <- pruebas_semanales(muestra, diario)
      pruebas[[llave]] <- transform(previo$pruebas, escenario = escenario, muestra = metodo)
      nuevos <- previo$diagnosticos[!previo$diagnosticos$tramo %in% names(tramos), ]
      rangos[[paste(llave, "previo")]] <- transform(nuevos, escenario = escenario, muestra = metodo,
                                                  base = "tres_semanas")
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
                   causal_uniones = uniones_finales, causal_balance = balance_final,
                   causal_dia_semana = unir_filas(rangos), causal_coeficientes = unir_filas(terminos))
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
  offsets <- c(dias_base, 0:1)
  diario <- setNames(lapply(offsets, function(h) {
    z <- celdas_en(h)
    stopifnot(all(rowSums(z) == extraer(muestra, h)))
    cbind(z, z[, 4:6] - z[, 1:3])
  }), offsets)
  actividad <- colSums(Reduce("+", diario)[, 1:9]) > 0
  presente <- c(actividad, actividad[1:3] | actividad[4:6])
  panel <- cambios_panel(muestra, diario, tramos["d0..1"])
  ajuste <- estimar(muestra, "tratado", panel$y)
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
    for (h in dias_base) {
      fecha <- indices[i] + h
      fechas_base[[length(fechas_base) + 1]] <- data.frame(
        escenario, indice = indices[i], inicio_real = indices[i] + if (escenario == "placebo") 28 else 0,
        h, fecha, dia_semana = dia_semana(fecha))
    }
  }
}
guardar(unir_filas(fechas_base), "causal_fechas_base")
guardar(data.frame(registros_fecha_invalida = nrow(invalidos),
                    mes_desconocido = sum(!invalidos$mes %in% 1:12),
                    regla = "conteo de filas publicadas con fecha valida; elegibilidad predicha hasta t-1"),
         "causal_medicion")

morelia <- list()
for (escenario in c("principal", "sin_senales")) {
  enlaces <- vinculos_finales[vinculos_finales$escenario == escenario & vinculos_finales$muestra == "emparejada", ]
  enlaces <- enlaces[enlaces$tratado_clave == "16053" & enlaces$indice == as.Date("2025-04-23"), ]
  morelia[[escenario]] <- data.frame(escenario, control_clave = enlaces$control_clave,
                                    contribucion = enlaces$contribucion)
}
morelia <- unir_filas(morelia)
guardar(morelia, "causal_morelia_donantes")

# 11. Tablas del reporte ---------------------------------------------------
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
obtener <- function(escenario = "principal", metodo = "emparejada", escala = "niveles",
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
for (tramo in c("d0", "d1", "d0..1", "d2..6", "wk0", "wk+1")) {
  a <- obtener(tramo = tramo)
  b <- obtener(tramo = tramo, agrupacion = "entidad_fecha")
  filas[[tramo]] <- c(tramo, resultado(a, FALSE), resultado(b),
                      formato(a$efecto_sigma, 3), formato(b$mde, 3))
}
tabla("causal_principales", c("Tramo", "Estimación (EE estatal)", "Estimación e IC doble", "DE", "MDE doble"), filas)

filas <- list()
for (metodo in c("comun_m0_m3", "mismos_tratados", "emparejada", "emparejada_1a1")) {
  for (modelo in paste0("M", 0:3)) {
    a <- obtener(metodo = metodo, modelo = modelo, agrupacion = "entidad_fecha")
    filas[[length(filas) + 1]] <- c(nombres_metodo[metodo], modelo, formato(a$tratados, 0),
                                   formato(a$n, 0), resultado(a))
  }
}
tabla("causal_modelos", c("Controles", "Modelo", "T", "$N$", "Estimación e IC doble"), filas)

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
    filas[[length(filas) + 1]] <- c(nombres_escenario[escenario], nombres_metodo[metodo],
                                   formato(a$tratados, 0), formato(a$fechas, 0), resultado(a))
  }
}
tabla("causal_sensibilidades", c("Exclusión / muestra", "Método", "T", "Fechas", "Estimación e IC doble"), filas)

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
for (tramo in c("d0", "d1", "d0..1", "d2..6", "wk0", "wk+1")) {
  fila <- tramo
  for (metodo in c("emparejada", "emparejada_1a1")) {
    a <- obtener("placebo", metodo, tramo = tramo)
    b <- obtener("placebo", metodo, tramo = tramo, agrupacion = "entidad_fecha")
    fila <- c(fila, resultado(b), valor_p(b$p), valor_p(a$p))
  }
  filas[[tramo]] <- fila
}
tabla("causal_placebo", c("Horizonte", "1:muchos, IC doble", "$p$ doble", "$p$ estatal",
                         "1:1, IC doble", "$p$ doble", "$p$ estatal"), filas)

filas <- previos <- list()
for (metodo in c("emparejada", "emparejada_1a1")) {
  for (agrupacion in c("entidad", "entidad_fecha", "CRV3")) {
    a <- obtener(metodo = metodo, agrupacion = agrupacion)
    nombre <- c(entidad = "CRV1 estatal", entidad_fecha = "CRV1 doble", CRV3 = "CRV3 estatal")[[agrupacion]]
    filas[[length(filas) + 1]] <- c(nombres_metodo[metodo], nombre, resultado(a), formato(a$gl, 0), formato(a$mde, 3))
  }
  pruebas_grupo <- pruebas[pruebas$escenario == "principal" & pruebas$muestra == metodo &
                            pruebas$restricciones == "wk-4;wk-3;wk-1", ]
  for (i in seq_len(nrow(pruebas_grupo))) {
    p <- pruebas_grupo[i, ]
    previos[[length(previos) + 1]] <- c(nombres_metodo[metodo],
                                       if (p$agrupacion == "entidad") "Estatal" else "Doble", formato(p$f, 3),
                                       valor_p(p$p), formato(p$rango, 0), formato(p$condicion, 1), p$estado)
  }
}
tabla("causal_inferencia", c("Método", "Inferencia", "d0..1, IC 95\\%", "gl", "MDE"), filas)
tabla("causal_previos", c("Método", "Agrupación", "F", "p", "Rango", "$\\kappa$", "Estado"), previos)

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
  filas[[estado]] <- c(estado, formato(r$efecto, 3))
}
tabla("causal_omision", c("Estado omitido", "Días 0–1"), filas)

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
# estados efectivos, Wald, donantes de Morelia.
cifras <- list()
anotar <- function(nombre, valor, decimales = 3) {
  cifras[[nombre]] <<- data.frame(nombre, valor, decimales, impreso = formato(valor, decimales))
}
selecciones <- list(Main = obtener(), Doble = obtener(agrupacion = "entidad_fecha"),
                    Nivel = obtener(escala = "niveles"), NivelDoble = obtener(escala = "niveles", agrupacion = "entidad_fecha"),
                    Previa = obtener(tramo = "wk-1"), PreviaDoble = obtener(tramo = "wk-1", agrupacion = "entidad_fecha"),
                    MenosDos = obtener(tramo = "-2"), MenosCinco = obtener(tramo = "-5"),
                    CRVTres = obtener(agrupacion = "CRV3"), Placebo = obtener("placebo", agrupacion = "entidad_fecha"))
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
anotar("MdePctNivel", 100 * nivel$mde / nivel$media_pre, 1)
anotar("MdePctNivelDoble", 100 * obtener(escala = "niveles", agrupacion = "entidad_fecha")$mde / nivel$media_pre, 1)
for (agrupacion in c("entidad", "entidad_fecha")) {
  r <- pruebas[pruebas$escenario == "principal" & pruebas$muestra == "emparejada" &
                  pruebas$restricciones == "wk-4;wk-3;wk-1" & pruebas$agrupacion == agrupacion, ]
  anotar(paste0("Wald_", agrupacion, "_p"), r$p)
}
for (escenario in c("principal", "sin_senales")) anotar(paste0("Morelia_", escenario), sum(morelia$escenario == escenario), 0)
r <- perdidas_finales[perdidas_finales$escenario == "principal" & perdidas_finales$clave == "16053" &
                         perdidas_finales$indice == as.Date("2025-04-23"), ]
anotar("MoreliaUniverso", r$controles_auditados, 0)
anotar("MoreliaCalibre", r$despues_pre_nivel, 0)
guardar(unir_filas(cifras), "cifras_reporte", "tablas")
guardar(calidad, "calidad", "tablas")

# 12. Trayectoria del reporte -------------------------------------------------
# Se guardan PDF y PNG con los datos que acaban de estimarse en R.
# Los intervalos son del 95% con agrupación por estado y fecha.

datos_dinamica <- efectos[efectos$escenario == "principal" & efectos$base == "tres_semanas" &
                            efectos$modelo == "M0" & efectos$agrupacion == "entidad_fecha" &
                            efectos$muestra %in% c("emparejada", "emparejada_1a1") &
                            efectos$tramo %in% as.character(-7:13), ]
datos_dinamica$h <- as.integer(datos_dinamica$tramo)
datos_dinamica$dia_grafica <- datos_dinamica$h + ifelse(datos_dinamica$muestra == "emparejada", -0.1, 0.1)
datos_dinamica$metodo <- factor(datos_dinamica$muestra, levels = c("emparejada", "emparejada_1a1"),
                               labels = c("1:muchos", "1:1"))
datos_dinamica <- datos_dinamica[order(datos_dinamica$metodo, datos_dinamica$h), ]
guardar(datos_dinamica, "datos_causal_dinamica", "figuras")
g_dinamica <- ggplot(datos_dinamica, aes(dia_grafica, efecto, color = metodo, group = metodo)) +
  geom_hline(yintercept = 0, color = "#555555", linewidth = 0.3) +
  geom_vline(xintercept = 0, color = "#555555", linetype = "dashed", linewidth = 0.3) +
  geom_errorbar(aes(ymin = ic_inf, ymax = ic_sup), width = 0.12, linewidth = 0.3) +
  geom_line(aes(linetype = metodo), linewidth = 0.35) + geom_point(aes(shape = metodo), size = 1.4) +
  scale_color_manual(values = c("1:muchos" = "#135a76", "1:1" = "#974421")) +
  scale_x_continuous(breaks = c(-7, -5, -2, 0, 1, 3, 6, 9, 13)) +
  labs(title = "Estimaciones diarias alrededor del inicio local",
       subtitle = "Base: días -28 a -8 · Intervalos puntuales del 95 % por estado y fecha",
       x = "Día respecto al inicio local", y = "Siniestros registrados por municipio y día",
       color = NULL, linetype = NULL, shape = NULL) +
  theme_minimal(base_size = 10) +
  theme(legend.position = "top", panel.grid.minor = element_blank(),
        panel.grid.major.x = element_blank(), strip.text = element_text(face = "bold"),
        plot.title = element_text(size = 11))

for (extension in c("pdf", "png")) {
  ggsave(file.path(carpeta_salida, "figuras", paste0("causal_dinamica.", extension)),
         g_dinamica, width = 7.35, height = 3.5, dpi = 150, bg = "white")
}
writeLines(capture.output(sessionInfo()), file.path(carpeta_salida, "sesion_R.txt"))
cat("\nAnálisis terminado:", nrow(efectos), "estimaciones finales.\n")
print(obtener(agrupacion = "entidad_fecha")[c("efecto", "ee", "ic_inf", "ic_sup", "tratados", "controles", "fechas")], row.names = FALSE)
cat("Resultados y gráficas en:", normalizePath(carpeta_salida), "\n")
```

# Cotejo del formato largo con la regresión de cambios

Árbol de trabajo `worktrees/twfe-panel-apilado`, rama
`codex/twfe-panel-apilado`, base `79860e1`.

## Las dos formulaciones reproducen la inferencia por pares

Se cotejaron 6 440 filas de efectos, 60 pruebas conjuntas semanales de Wald,
180 contrastes semanales individuales y 48 cruces por franja y gravedad. Las
filas de efectos incluyen los modelos $M_0$ a $M_3$, niveles y logaritmos,
los emparejamientos 1:muchos y 1:1, los días previos, los tramos posteriores,
el placebo y las sensibilidades. La réplica en R reconstruyó 180 908 filas de
muestra por escenario y método y reprodujo sus pares, covariables y pesos.

Los coeficientes de tratamiento, errores estándar, intervalos, valores $p$ y
diagnósticos conjuntos coinciden con una tolerancia absoluta de $10^{-9}$.
Los grados de libertad por conglomerados coinciden exactamente. El cotejo en
Python incluye la varianza por omisión sucesiva de estados (CRV3) y verifica
los 60 valores impresos de estimación e inferencia de las covariables en
los paneles A y B del cuadro 2.

En 40 filas el horizonte es su propia referencia (Día −2 o Semana −1). El
cambio es cero por definición. El cotejo registra el cero analítico y omite la
prueba $t$. El orden de las operaciones produce residuos ínfimos y valores
$p$ arbitrarios en algunas filas. En el contraste logarítmico 1:muchos de la
Semana −1 con agrupación por estado y fecha, R produce una varianza negativa
de redondeo y deja el error estándar indefinido. El archivo de resultados de R
conserva ese diagnóstico.

## La corrección de muestra finita determina la diferencia

El modelo principal de los Días 0–1 usa 3 613 pares, 77 tratados y 3 536 de
control. La siguiente tabla compara las tres formas de calcular ese coeficiente
en $\log(1+Z)$, con agrupación por estado y fecha de inicio.

| Formulación y corrección | Coeficiente | Error estándar | Intervalo del 95 % | Valor $p$ | Grados de libertad |
| --- | ---: | ---: | ---: | ---: | ---: |
| Cambios, por pares | −0,107136 | 0,043310 | [−0,195466; −0,018805] | 0,019053 | 31 |
| Formato largo, por pares | −0,107136 | 0,043310 | [−0,195466; −0,018805] | 0,019053 | 31 |
| Formato largo, por filas | −0,107136 | 0,061253 | [−0,232063; 0,017791] | 0,090178 | 31 |

Contar las $2N$ filas y los $N$ efectos adicionales de par en la corrección
robusta por grupos (CRV1) conserva el denominador de grados de libertad
residuales. El numerador pasa de $N-1$ a $2N-1$. La varianza casi se duplica y
los errores estándar aumentan alrededor de 41 %. Con esa corrección
alternativa, el intervalo principal incluye cero y 14 de las 60 pruebas
conjuntas dejan de rechazar la hipótesis nula al 5 %. La inferencia del reporte
utiliza la corrección por pares.

## Reproducción y revisión

Desde la raíz del árbol de trabajo, estas rutas identifican los insumos locales
verificados. El [README](../../README.md) explica cómo sustituirlas en otra copia.

```powershell
$env:PYTHONPATH = (Resolve-Path src).Path
$choquesPy = "../../.venv/Scripts/python.exe"
$cotejo = "reporte/verificacion/twfe-local"
Rscript --vanilla codigo_R/analisis.R ../../data/outputs/apendice-r-verificado/replica_limpia/datos_limpios_R "$cotejo/r" --panel-largo
& $choquesPy -m choques cotejar-panel --referencia ../diseno-causal-final/data/outputs/modelos --procesados ../diseno-causal-final/data/processed --replica-r "$cotejo/r/modelos" --salida "$cotejo/cotejo"
```

El [registro numérico](panel-largo.json) contiene las huellas y diferencias
máximas por estadístico. La carpeta de salida conserva el detalle por
especificación, incluidos los resultados con la corrección por filas.

Se ejecutaron los casos de integración de preparación y comparación semanal
de `tests/caso_sintetico.py` y las comprobaciones de navegación y exportación de
la presentación. Los PDF se revisaron visualmente en las páginas 4, 17, 18,
23, 31, 34 y 35 del [reporte](../reporte.pdf) y 5, 6 y 9 de la
[presentación](../../presentacion/presentacion.pdf). La presentación tiene
18 páginas y el guion conserva 480 segundos.

Para la versión oficial se repitió el cotejo con el código final. R en
formato largo reprodujo los 13 archivos de resultados. La réplica completa
en cambios reprodujo 22 productos y las 18 tablas con la notación actual.
La compilación reprodujo el PDF del reporte byte por byte.

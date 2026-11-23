# Cumplimiento del programa del curso

Fuentes. Programa de Inferencia Causal, ITAM, 2026-2, sección 6, pp. 4–5, y
diapositivas de diferencias en diferencias, pp. 4–5, 44 y 47.
La entrega es [reporte.pdf](reporte.pdf), de Eduardo Garcia Cortez, clave
única 207480, para el profesor Mauricio Romero. La numeración corresponde
al PDF del árbol de trabajo.

| Requisito | Ubicación en la versión revisada |
| --- | --- |
| Texto de 6–8 páginas y fuente de 11–12 puntos | Siete páginas de cuerpo (1–7), `article` a 11 puntos, referencias en p. 8 y apéndices en pp. 9–50 |
| Notación canónica del curso | Sección 3, pp. 3–4. Resultados potenciales $Y^g_{ith1}(1)$ y $Y^g_{ith1}(0)$, efecto objetivo $\tau_{\mathrm{ATT},h}^g$ y coeficiente $\tau_{\mathrm{DD},h}^g$ de la interacción $D_{its}=\mathrm{Treat}_{it}\mathrm{Post}_s$. El índice adicional identifica el par, el horizonte y la fila de comparación del proyecto. |
| Contexto, pregunta, mecanismos y literatura | Sección 1, p. 1: dos antecedentes académicos y una fuente de contexto; ATT antes del estimador |
| Datos, fuentes, periodo, unidad y N | P. 2: ATUS 2019–2025 e historia de 2018; 3 613 pares municipio–fecha, 77 tratados, 3 536 controles, 31 episodios y 32 fechas |
| Tratamiento, medición, ceros y selección | P. 2: catálogo propio, inicio local, cobertura previa y límites de la captación |
| Covariables y tasas de enlace | P. 2: fuentes oficiales y corte previo; empleo y automóviles en 82/84 pares tratados elegibles (97,6 %); detalle de uniones en p. 10 |
| Descriptivos y balance | Cuadro 1, p. 3; ampliación en apéndice A |
| Estimando formal, ecuaciones y pesos | Sección 3, pp. 3–4: resultados potenciales, base, diferencias en diferencias y matching por tratado |
| Supuestos y sesgo | P. 4: supuestos no comprobables, comprobaciones disponibles y sesgo posible si fallan |
| Agrupación de errores y justificación | P. 4: estado y fecha; detalle en apéndice D, pp. 17–19 |
| Resultados, errores, N y progresión | Cuadro 2, Panel A, p. 5; características comunes en la nota. Panel B en p. 9 |
| Unidades naturales y tamaños estandarizados | P. 5: -0,107 en escala logarítmica, -0,397 registros y -0,130 y -0,108 desviaciones estándar |
| Efecto mínimo detectable para resultados nulos | Pp. 5 y 7; prueba bilateral al 5 % y potencia del 80 %. Detalle en apéndices B y D |
| Al menos una figura | Figura 1, p. 6: trayectoria en dos escalas y dos esquemas de matching; mapa en p. 21 |
| Robustez y falsificaciones | Pp. 6–7: diferencias previas, placebo, duración, base alternativa y calendario; apéndices B–D |
| Conclusión, validez externa, límites y relevancia de política | Sección 5, p. 7 |
| Apéndices, código y datos públicos | Apéndices A–H, pp. 9–50. Fuentes y reproducción en p. 20. Apéndice H, pp. 23–50, con el código R completo (1 509 líneas), instrucciones y enlaces. |
| Presentación de 8–10 minutos | [Presentación](../presentacion/presentacion.pdf) y [guion](../presentacion/guion.md) para ocho minutos de exposición. |

El estudiante confirmó la autorización del profesor para utilizar Python.
El código R completo se incluye en el PDF conforme al requisito de la sección 6,
p. 4 del syllabus. Su nueva ejecución se cotejó con los resultados vigentes. Para
esta entrega, el límite acordado se aplica al cuerpo; referencias y
apéndices van aparte. La presentación oral es una entrega separada.

## Verificación

Se cotejó la notación de resultados potenciales y de la ecuación con las
diapositivas del curso. La edición revisada usa $Z$ para el conteo diario,
$Y$ para el resultado construido y $\hat\tau$ como abreviatura del coeficiente
estimado en los cuadros. El [registro numérico](verificacion/panel-largo.json)
identifica los PDF, los insumos y el [cotejo](verificacion/panel-largo.md) entre
las dos formulaciones. La [verificación de la presentación](../presentacion/verificacion/REVISION.md)
registra la exportación y la duración del guion.

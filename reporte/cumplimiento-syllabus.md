# Cumplimiento del programa del curso

Fuentes. Programa de Inferencia Causal, ITAM, 2026-2, sección 6, pp. 4–5, y
diapositivas de diferencias en diferencias, pp. 4–5, 44 y 47.
La entrega es [reporte.pdf](reporte.pdf), de Eduardo Garcia Cortez, clave
única 207480, para el profesor Mauricio Romero. La numeración corresponde
al PDF del árbol de trabajo.

| Requisito | Ubicación en la versión revisada |
| --- | --- |
| Texto de 6–8 páginas y fuente de 11–12 puntos | Ocho páginas de cuerpo (1–8), `article` a 11 puntos, referencias en p. 9 y apéndices en pp. 10–46 |
| Notación canónica del curso | Sección 3, pp. 3–4. Resultados potenciales $\bar Y_{ith}(1)$ y $\bar Y_{ith}(0)$, efecto objetivo $\tau_{\mathrm{ATT},h}$ y coeficiente $\tau_{\mathrm{DD},h}$ de Tratado × Después. La regresión incluye conteos diarios $Y_{i,d}$ y efectos fijos del día de la semana. |
| Contexto, pregunta, mecanismos y literatura | Sección 1, p. 1: dos antecedentes académicos y una fuente de contexto; ATT antes del estimador |
| Datos, fuentes, periodo, unidad y N | P. 2: ATUS 2019–2025 e historia de 2018; 3 613 pares municipio–fecha, 77 tratados, 3 536 controles, 31 episodios y 32 fechas |
| Tratamiento, medición, ceros y selección | P. 2: catálogo propio, inicio local, cobertura previa y límites de la captación |
| Covariables y tasas de enlace | P. 2: fuentes oficiales y corte previo; empleo y automóviles en 82/84 pares tratados elegibles (97,6 %); detalle de uniones en p. 10 |
| Descriptivos y balance | Cuadro 1, p. 3; ampliación en apéndice A |
| Estimando formal, ecuaciones y pesos | Sección 3, pp. 3–4: resultados potenciales, base, diferencias en diferencias y matching por tratado |
| Supuestos y sesgo | P. 4: supuestos no comprobables, comprobaciones disponibles y sesgo posible si fallan |
| Agrupación de errores y justificación | P. 4: estado y fecha; detalle en apéndice D, pp. 17–18 |
| Resultados, errores, N y progresión | Cuadro 2, p. 5, en siniestros registrados por municipio y día. Las demás muestras figuran en el cuadro A5, p. 12 |
| Unidades naturales y tamaños estandarizados | P. 5. Se estiman -0,348 siniestros registrados por municipio y día, equivalentes a -0,094 desviaciones estándar de los conteos diarios de la base |
| Efecto mínimo detectable para resultados nulos | P. 5 y apéndices B y D. Prueba bilateral al 5 % y potencia del 80 % |
| Al menos una figura | Figuras 1a y 1b, p. 6. Conteos de los días -28 a +13 y cambios respecto a la base. Figura 1c, p. 7. Trayectoria de los coeficientes en niveles. Mapa en p. 20 |
| Robustez y falsificaciones | Pp. 6–8. Diferencias previas, placebo, duración y calendario. Apéndices B–D |
| Conclusión, validez externa, límites y relevancia de política | Sección 5, p. 8 |
| Apéndices, código y datos públicos | Apéndices A–H, pp. 10–46. Fuentes y reproducción en p. 19. Apéndice H, pp. 22–46, con el código R completo (1 354 líneas), instrucciones y enlaces. |
| Presentación de 8–10 minutos | [Presentación](../presentacion/presentacion.pdf) y [guion](../presentacion/guion.md) para ocho minutos de exposición. |

El estudiante confirmó la autorización del profesor para utilizar Python.
El código R completo se incluye en el PDF conforme al requisito de la sección 6,
p. 4 del syllabus. Su nueva ejecución se cotejó con los resultados vigentes. Para
esta entrega, el límite acordado se aplica al cuerpo; referencias y
apéndices van aparte. La presentación oral es una entrega separada.

## Verificación

Se cotejó la notación de resultados potenciales y de la ecuación con las
diapositivas del curso. La edición revisada usa $Y_{i,d}$ para el conteo diario, $\bar Y_{ith}$ para el
promedio del tramo y $\hat\tau$ para el coeficiente estimado. El [registro
numérico](verificacion/niveles-base-semanal.json) identifica los archivos
entregados. El [registro de verificación](verificacion/niveles-base-semanal.md)
documenta la concordancia entre Python y R. La [verificación de la presentación](../presentacion/verificacion/REVISION.md)
registra la exportación y la duración del guion.

# Cumplimiento del syllabus: reporte aprobado

Fuente: syllabus de Inferencia Causal, ITAM, 2026-2, sección 6, páginas 4–5.
La entrega es [reporte.pdf](reporte.pdf), de Eduardo Garcia Cortez, clave
única 207480, para el profesor Mauricio Romero. La numeración corresponde
al PDF final.

| Requisito | Ubicación en la versión aprobada |
| --- | --- |
| Texto de 6–8 páginas y fuente de 11–12 puntos | Siete páginas de cuerpo (1–7), `article` a 11pt; referencias en p. 8 y apéndices en pp. 9–49 |
| Contexto, pregunta, mecanismos y literatura | Sección 1, p. 1: dos antecedentes académicos y una fuente de contexto; ATT antes del estimador |
| Datos, fuentes, periodo, unidad y N | P. 2: ATUS 2019–2025 e historia de 2018; 3 613 pares municipio–fecha, 77 tratados, 3 536 controles, 31 episodios y 32 fechas |
| Tratamiento, medición, ceros y selección | P. 2: catálogo propio, inicio local, cobertura previa y límites de la captación |
| Covariables y tasas de enlace | P. 2: fuentes oficiales y corte previo; empleo y automóviles en 82/84 pares tratados elegibles (97,6 %); detalle de uniones en p. 10 |
| Descriptivos y balance | Cuadro 1, p. 3; ampliación en apéndice A |
| Estimando formal, ecuaciones y pesos | Sección 3, pp. 3–4: resultados potenciales, base, diferencias en diferencias y matching por tratado |
| Supuestos y sesgo | P. 4: supuestos no comprobables, comprobaciones disponibles y sesgo posible si fallan |
| Agrupación de errores y justificación | P. 4: estado y fecha; detalle en apéndice D, pp. 17–19 |
| Resultados, errores, N y progresión | Cuadro 2, Panel A, p. 5; características comunes en la nota. Panel B en p. 9 |
| Unidades naturales y tamaños estandarizados | P. 5: -0,107 en log(1+Y), -0,397 registros y -0,130 y -0,108 desviaciones estándar |
| Efecto mínimo detectable para resultados nulos | Pp. 5 y 7; prueba bilateral al 5 % y potencia del 80 %. Detalle en apéndices B y D |
| Al menos una figura | Figura 1, p. 6: trayectoria en dos escalas y dos esquemas de matching; mapa en p. 21 |
| Robustez y falsificaciones | Pp. 6–7: diferencias previas, placebo, duración, base alternativa y calendario; apéndices B–D |
| Conclusión, validez externa, límites y relevancia de política | Sección 5, p. 7 |
| Apéndices, código y datos públicos | Apéndices A–H, pp. 9–49; fuentes y reproducción en p. 20. Apéndice H, pp. 23–49: código R completo (1 465 líneas), instrucciones y enlaces al repositorio y a la carpeta de entrega de datos |

El estudiante confirmó la autorización del profesor para utilizar Python.
El código R completo se incluye en el PDF conforme al requisito de la sección 6,
p. 4 del syllabus. Su nueva ejecución se cotejó con los resultados vigentes. Para
esta entrega, el límite acordado se aplica al cuerpo; referencias y
apéndices van aparte. La presentación oral es una entrega separada.

## Verificación

Se revisaron las páginas modificadas y nuevas; las otras 21 páginas coinciden
por píxeles con la versión ya revisada. La compilación normal con Biber terminó
sin advertencias LaTeX ni cajas desbordadas. Las 1 465 líneas del código del PDF
coinciden con el archivo R, salvo los espacios que añade el formato del listado.
Los enlaces de GitHub y Drive están presentes como vínculos activos.

[revision-editorial.json](verificacion/revision-editorial.json) identifica
el PDF actual. El [cotejo de R](verificacion/reproduccion-r.json) acredita 22
productos dentro de la tolerancia absoluta de 1e-6 y 18 tablas idénticas a la
precisión impresa. Se verificaron los 15 insumos por sus huellas y se preservaron
los resultados Python. No se ejecutaron pruebas unitarias ni el flujo Python
completo; los manifiestos anteriores conservan su alcance histórico.

# Evidencia de Ruta B y de la entrega escrita

## Revisión editorial vigente

La entrega aprobada está en [reporte.pdf](reporte.pdf), [reporte.md](reporte.md)
y [main.tex](main.tex). Tiene siete páginas de cuerpo, una de referencias y
41 de apéndices; 49 en total. Mantiene fuente de 11 puntos en el cuerpo, párrafos a
la izquierda y citas y referencias APA. La figura geográfica está en el
apéndice F; el cruce exploratorio por horario y gravedad, en el G; y el código
R completo, con enlaces al repositorio y a la carpeta de datos, en el H (pp. 23–49).
[Cumplimiento del syllabus](cumplimiento-syllabus.md) localiza las secciones.

Se incorporaron las 21 propuestas aprobadas y la etiqueta «Matching» para
describir la selección de tratados y controles. Se revisaron las páginas
modificadas y nuevas y su coincidencia con el Markdown; las otras 21 páginas
conservan sus píxeles. La compilación normal con Biber produce `main.pdf` y
`reporte.pdf` idénticos. Se cotejaron las 1 465 líneas del listado contra el R.

[revision-editorial.json](verificacion/revision-editorial.json) identifica
esta entrega. La nueva ejecución del R reprodujo 22 productos dentro de la
tolerancia absoluta de 1e-6 y 18 tablas a la precisión impresa; consta en
[reproduccion-r.json](verificacion/reproduccion-r.json). No se ejecutaron
pruebas unitarias ni el flujo Python completo. Los manifiestos de 117 productos y 38 fuentes son registros
de la reproducción anterior, cuyo PDF tiene SHA-256
`fcfeab43aff0209365029ba62d5ebbdcdc9adc64eb4f616455d6bd4fc5d269d7`.

La comparación semanal de la crisis prolongada de Culiacán permanece fuera
del reporte. Las jornadas puntuales de 2019 y 2023 siguen en el análisis.

## Registro de ejecución analítica y verificación anterior

Rama `diseno-causal-final`, base `e283e2d76190b496644133c7e1e5c0b004a4e99f`.
Autorización: `run`, 21/11/2026, después del plan; posteriormente se autorizó
publicar los cambios mediante PR. La base contiene el commit
auditado `0335513294fbeaaf160d8bdbca3da8b6f6b56456`. Se conservó el historial.
Esa entrega se integró mediante el PR 2, con merge
`785c153dabd3567d76c21e1ff3ccae62f9162a90`. T08 está fuera del alcance.

La revisión de portada y syllabus usa la rama `portada-syllabus-final`, sobre
ese merge, en el mismo worktree con datos separados. Identifica a Eduardo Garcia
Cortez, clave única 207480, al profesor Mauricio Romero y el título solicitado.
La [matriz del syllabus](cumplimiento-syllabus.md) localiza cada requisito en
el PDF. Se añadió N en Datos y una tabla breve M0–M3 en Resultados; los 53 CSV
de resultados numéricos conservan sus huellas anteriores. No se modificaron
estimaciones, muestras ni criterios de selección.

El documento rector es `Proyecto/tasks/auditoria-final/auditoria-final.md`.
Las rutas de datos siguientes se refieren a las carpetas hermanas de este
worktree, no a las salidas mutables del repositorio principal.

## Decisiones y contradicciones resueltas

- **Tres semanas y ventana limpia.** `r=t+h` es incompatible con `[-28,-8]`
  en varios horizontes. Se fija `r=t+(h mod 7)`, con residuo en 0..6; las tres
  fechas `r-28,r-21,r-14` son del mismo día de semana y siempre están dentro
  de la ventana. Cada tramo promedia contrastes diarios. No se incorpora wk-1.
- **Dos días frente a 48 horas.** d0..1 son dos fechas naturales. Un inicio
  vespertino no permite interpretar ese tramo como 48 horas exactas de exposición.
- **Elegibilidad principal.** Tres meses completos anteriores al mes de t,
  antecedentes `[-49,-1]` y territorio hasta t-1. El resultado es el conteo
  de registros publicados de fecha válida. Un cero de registros no certifica
  continuidad de captación ni ausencia física de accidentes. Se conserva aparte
  el panel original con faltantes; no se aplica un rellenado general de NaN.
- **Persistencia.** Se añade cobertura observada `[-28,+13]` y aislamiento
  hasta +14 para 2..6 y 7..13. Esta selección posterior no define el principal.
  La excepción del episodio focal sólo vale para su propio tratado desde t.
- **Calibre y soporte.** Universo elegible, nivel individual y luego población,
  empleo/mil y autos/mil; diez candidatos de cinco estados por tratado, antes
  de escoger 1:1. No se fuerza un número final de donantes.
- **Previos.** La referencia omitida del Wald es wk-2. Contrastar wk-4, wk-3
  y wk-1 contra ella evita la dependencia exacta de semanas normalizadas por
  su propio promedio. Se comprueban rango, autovalores y condicionamiento.
- **Calendario.** Las cinco fechas candidatas se conservan como sensibilidad
  de la auditoría, pero no son cinco feriados generales de la LFT ni agotan el
  calendario escolar. Se añaden LFT y unión LFT-SEP para d0 o d1, con reglas
  y fuentes fijadas en `config/calendario_escolar.csv`. No se llama vacaciones
  a toda la enseñanza remota de 2020 ni se excluyen domingos ordinarios.
- **T05 y revisión auditada.** T05 original registra 77 tratados/31 fechas;
  la revisión auditada usa 73/30. Se conserva esta última como referencia b=-2
  reproducible y se distingue del catálogo original de T05.
  Las sensibilidades de base sobre la muestra final mantienen pares y pesos.
- **Conclusión.** La auditoría anticipaba una caída causal y totalmente transitoria.
  Los resultados nuevos no sostienen esa afirmación completa; el texto informa
  pretests adversos, dependencia de escala/calendario e indicios en semana +1.

## Matriz de requisitos, implementación y evidencia

| Requisito | Implementación | Resultado o evidencia verificable |
| --- | --- | --- |
| H1: seis fuentes, tasas de unión y datos | `municipios.py`, `informe_final.py`; Sección 2 y Apéndice A; seis entradas bibliográficas | `causal_uniones.csv`; tablas `causal_uniones.tex` y `causal_uniones_aux.tex`, con numeradores, denominadores y universos |
| H1: balance y progresión | M0 tratamiento/fecha; M1 log población; M2 empleo/mil; M3 autos/mil; muestras y pesos fijos | `causal_balance.csv`, `causal_modelos.tex`, `causal_progresion_principal.tex` y `causal_balance_prepost.tex`; progresión principal también en el cuerpo, p. 5 |
| H1: cruce horario, notación y rutas | Resultados, cruce exploratorio; potencial `Y_{i,t+h}(0)` formalizado; rutas desde carpeta contenedora | Cuadro de noche menos día; `causal_cruce.csv`; suma de nueve celdas comprobada en ejecución |
| H2: calibre individual | `modelos.caliber_mask`, `seleccion.match`, `causal.select_pre` | Prueba de tratados heterogéneos en una fecha; `causal_vinculos.csv`, `causal_descartes.csv` |
| H2: Morelia y precipicio antiguo | Referencia antigua preservada; filtros nuevos desde universo elegible | `causal_morelia_donantes.csv`; 10 antiguos, 14 tras calibre nuevo, 12 tras covariables, 12 al excluir señales |
| H3: base limpia de tres semanas | `baseline_offsets`, `contrasts`; transformación antes del promedio | Prueba de todos los residuos/horizontes y límites; `causal_fechas_base.csv`; sensibilidad b=-2 y wk-1 con muestra fija |
| H4: no seleccionar principal a futuro | `predicted_coverage`, `select_pre`; rama separada de persistencia | Prueba de invariancia a cambios posteriores en registros, anomalías y exposiciones; `causal_elegibilidad.csv`, `causal_perdidas.tex` |
| H4: distinguir persistencia | Comparación de muestra previa y rama de cobertura/aislamiento completo | `causal_persistencia.tex`, `causal_soporte.csv`; cautela explícita en texto |
| H5: Culiacán y cambios M | `persistente.territorial_donors`; orígenes y destinos dentro del intervalo usado | `culiacan_descartes_territoriales.csv`, excluye 24028 por 24059 el 30/08/2024; prueba M/W y límites; figura estrictamente descriptiva |
| H6: CRV1 estatal y dos vías | Estimador ponderado existente, correcciones y grados de libertad documentados | `causal_efectos.csv`; validación contra matriz explícita y PyFixest |
| H6: CRV3 y omisión estatal | Pesos originales, efectos de fecha reestimados, `(G-1)/G` centrado en estimación completa | Prueba ponderada contra regresión explícita; `causal_omision_estado.csv`, `causal_inferencia.tex`, `causal_omision.tex` |
| H6: pocas restricciones y potencia | Wald semanal de rango comprobado; MDE bilateral 5%, potencia 80%, t no central | `causal_wald_semanal.csv`, `causal_previos.tex`; MDE estatal/doble por escala y matching en `causal_inferencia.tex` |
| H7: corroboración pendiente | Exclusiones obligatorias Chilchota/Contepec y adicional de los cuatro pendientes | `causal_sensibilidades.tex`; San Fernando entra en el diseño nuevo, Huaniqueo sigue fuera |
| H7: cotejo de controles | Excluir Centro 27004 (01-02/04/2025), Coatzacoalcos 30039 (20/08/2022), reconstruir pesos | Escenario `sin_senales`; alcance de sólo 27 pares cotejados y HTTP 403 de ACLED declarado |
| H7: lenguaje exigido | Uso de Python autorizado por el profesor | Confirmación expresa del estudiante el 21/11/2026; punto resuelto |
| H8: entorno y rutas Windows | Lock en `.venv` compartida; `TemporaryDirectory()` del sistema; datos/tareas hermanas locales | Instalación y `pip check`; validación normal; reproducción aislada |
| H8: UTF-8 y leyenda | Acentos corregidos en JSON/lock; nota `tasks/figuras/figuras.md` actualizada | Diff versionado y parche externo `Proyecto/tasks/diseno-causal-final/evidence/figuras.patch` |
| H9: dispersión | DE diaria previa `[-28,-8]`, ddof=1; balance entre medias previas `[-28,-15]` | Notas de Cuadros 1 y 2; `sigma_pre` y `efecto_sigma` en CSV |
| Placebo seis horizontes | Índice ficticio t-28, elegibilidad y matching reconstruidos | `causal_placebo.tex`; d0,d1,d0..1,d2..6,wk0,wk+1 en ambas escalas y matchings, IC doble y p estatal; fechas exactas CSV |
| Cinco fechas y calendario oficial completo pertinente | Tres sensibilidades de calendario, independientes de estimaciones | `causal_calendario.csv`, `causal_exclusiones_calendario.csv`, `causal_calendario.tex`; muestra y pérdidas informadas |
| Doble escala y ceros | log1p principal, niveles complementarios; finitos no negativos | Prueba de cero y transformación antes de promediar; coeficientes, unidades naturales y DE en tablas |
| Pruebas unitarias y sintéticas | `tests/test_causal.py` y suites existentes integradas en `validar` | Ocho pruebas nuevas; recuperación de efecto conocido en pipeline sintético; `validacion.md` determinista |
| Syllabus §6: contexto y ATT antes de estimador | Sección 1 y estimando formal en Sección 3 | Pregunta, cifras, mecanismo, literatura y población objetivo en PDF |
| Syllabus §6: supuestos y sesgo | Sección 3, diferencia de brechas contrafactuales | Supuestos no comprobables separados de diagnósticos; selección, interferencia y medición explícitas |
| Syllabus §6: resultados y validez externa | Secciones 4-5 y apéndices | Figura, EE, N, progresión, σ, unidades, MDE, robustez; alcance a registros y jornadas con soporte |
| Syllabus §6: extensión y tipografía | Article 11pt; apéndice separado | Siete páginas de texto, una de referencias y diez de apéndice; 18/18 páginas inspeccionadas; `revision-visual.json` |
| Paquete reproducible y fuentes públicas | CLI real, lock, originales fijados, `reproducir.py` | Copia limpia definitiva: 117/117 productos SHA-256 idénticos, incluido PDF binario; 38 fuentes de código/configuración cotejadas sin cambios |
| Preservación de T05 y cambios ajenos | Archivos congelados sin modificaciones; referencia histórica separada | Ambas huellas originales y locales idénticas; main limpio, `diff --check` aprobado; `preservacion.json` |

## Verificación final

- `python -m choques todo`: salida 0, 332.132 s. Incluye `validar`: ocho
  pruebas unitarias y las suites sintéticas existentes aprobadas.
- `python -m choques compilar`: salida 0. Tras la revisión cruzada se repitieron
  `analizar` y `compilar` para explicitar el placebo estatal. Log final: cero overfull
  hboxes, cero referencias o citas indefinidas.
- Revisión de portada y syllabus: `configuracion`, `py_compile`, `analizar` y
  `compilar` terminaron con salida 0. La copia limpia volvió a ejecutar las ocho
  etapas con el código actual, incluidas las ocho pruebas unitarias y las suites
  sintéticas de `validar`. El registro anterior de `todo` corresponde al cierre
  de Ruta B; los cambios posteriores sólo afectan presentación y documentación.
- PDF actualizado: 18 páginas. Texto 1-7, referencias 8, apéndices 9-18; 11pt.
  El syllabus sólo excluye explícitamente el apéndice: aun con referencias son
  ocho páginas, dentro del intervalo 6-8. Se inspeccionaron directamente los
  18 PNG a 110 dpi: sin recortes, solapamientos ni glifos ausentes. La tabla de
  soporte tiene una página propia en el apéndice.
- SHA-256 del PDF inspeccionado:
  `fcfeab43aff0209365029ba62d5ebbdcdc9adc64eb4f616455d6bd4fc5d269d7`.
- Git: rama y base verificadas, commit auditado ancestro de HEAD; main limpio,
  en `785c153dabd3567d76c21e1ff3ccae62f9162a90`. T05 original y copia conservan
  sus dos huellas iniciales. La revisión editorial permanece local y revisable
  en `portada-syllabus-final`; no se publicaron estos cambios.
- `python reproducir.py`: versión definitiva aprobada, **117/117 productos
  con SHA-256 idéntico (100%)**, incluido PDF binario y validación sintética
  sin normalización. Los 38 archivos de código/configuración se conservaron
  idénticos a los copiados durante la ejecución. Copia:
  `worktrees/diseno-causal-final/worktrees/reproduccion-rjg8q7fb`, relativa a
  Proyecto. Se reconstruyeron descargar, consolidar, preparar, validar, estimar,
  analizar, graficar y compilar; las ocho etapas terminaron con salida 0.
- `pip check`: salida 0; openpyxl 3.1.5 y xlrd 2.0.2 en `Proyecto/.venv`.

Evidencia bajo [data/outputs/qa](../../data/outputs/qa/):
[comandos](../../data/outputs/qa/comandos-finales.json),
[log de todo](../../data/outputs/qa/todo-final.txt),
[validación](../../data/outputs/modelos/validacion.md),
[log LaTeX](../../data/outputs/qa/compilacion.txt),
[metadatos PDF](../../data/outputs/qa/pdf-metadata.json),
[revisión visual](../../data/outputs/qa/revision-visual.json),
[preservación](../../data/outputs/qa/preservacion.json),
[entorno](../../data/outputs/qa/entorno-final.json),
[reproducción limpia](../../data/outputs/qa/reproduccion.md),
[SHA-256 de productos](../../data/outputs/qa/sha256-verificados.json),
[SHA-256 de fuentes](../../data/outputs/qa/sha256-fuentes.json),
[log íntegro de reproducción](../../data/outputs/qa/reproduccion-ejecucion.txt).

Los comprobantes que acompañan al PR se versionan en
[reporte/verificacion/](verificacion/): registro de reproducción, huellas de
productos y fuentes, validación y revisión visual. El parche de la actualización
autorizada en la carpeta hermana `tasks/figuras/` se entrega allí por separado;
esa carpeta no pertenece al repositorio.
El parche utiliza contexto cero y se verificó con `git apply --check --unidiff-zero`
sobre una copia de la versión anterior.

### Morelia: identidad de los donantes

| Referencia | Claves de donantes del 23/04/2025 |
| --- | --- |
| Auditada, 10 | 05030, 07101, 09005, 09012, 15033, 15109, 25012, 27004, 30193, 31050 |
| Final, 12 | 08019, 08037, 10005, 12001, 15106, 19006, 21114, 22014, 23005, 26030, 28032, 30087 |
| Sin las dos señales, 12 | Las mismas doce claves finales |

Las listas no son anidadas: cambian la elegibilidad y el centro del calibre.
El universo final es 628; 617 tienen covariables completas, 14 pasan el calibre
individual y 12 pasan los tres intervalos municipales. Cada vínculo final pesa
1/12. Fuente: `causal_descartes.csv` y `causal_morelia_donantes.csv`.

## Límites que no se convierten en cumplimiento artificial

El permiso de Python está resuelto por la confirmación del estudiante. Las
auditorías pasadas no constituyen entregables pendientes de este PR.

1. No hay cotejo exhaustivo de exposición en controles ni garantía de captación
   ATUS estable. El calendario nacional básico no cubre todas las instituciones.
2. El rediseño posterior a observar T05 no es una preespecificación. La evidencia
   no autoriza afirmar una reducción causal incondicional y totalmente transitoria.
   El placebo inmediato d0..1 incluye cero; CRV1 estatal rechaza d2..6 en
   ambas escalas y wk0 en niveles, mientras dos vías no rechaza. Estos resultados
   se muestran conjuntamente, sin describir el placebo como uniformemente nulo.

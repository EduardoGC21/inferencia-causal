"""Genera la presentación y el guion desde una sola fuente editorial."""
import csv
from html import escape
from pathlib import Path

DECK = Path(__file__).resolve().parents[1]
def read_results(name):
    with (DECK / "assets/datos" / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


effects = read_results("efectos.csv")
coefficients = read_results("causal_coeficientes.csv")
weekly = read_results("causal_wald_semanal.csv")

slides = []
data = "INEGI (ATUS y covariables), Consejo Nacional de Población (CONAPO) y catálogo propio."
sources = "INEGI (ATUS y covariables), CONAPO y catálogo propio."


def add(id, chapter, title, seconds, body, speech, transition, locator, source=None, style="", *, table_note=""):
    slides.append(dict(id=id, chapter=chapter, title=title, seconds=seconds, body=body,
                       speech=speech, transition=transition, locator=locator, source=source,
                       style=style, table_note=table_note))


def math(tex, block=False):
    cls = ' class="equation"' if block else ""
    return f'<span{cls} data-tex="{escape(tex, quote=True)}"></span>'


def figure(file, alt):
    return f'<img src="assets/{file}" alt="{escape(alt, quote=True)}">'


def num(n, digits=3):
    return f"{float(n):.{digits}f}".replace(".", ",").replace("-", "−")


def result(tramo="d0..1", **options):
    key = dict(tramo=tramo, escenario="principal", muestra="emparejada", modelo="M0",
               escala="niveles", base="tres_semanas", agrupacion="entidad_fecha") | options
    row, = (row for row in effects if all(row[k] == v for k, v in key.items()))
    return row


def rows(items):
    return [(label, num(row["efecto"]), f'[{num(row["ic_inf"])}; {num(row["ic_sup"])}]')
            for label, row in items]


def table(head, body):
    columns = "".join(f'<th scope="col">{x}</th>' for x in head)
    body = "".join(f'<tr><th scope="row">{r[0]}</th>' + "".join(f"<td>{x}</td>" for x in r[1:]) + "</tr>"
                   for r in body)
    return f"<table><thead><tr>{columns}</tr></thead><tbody>{body}</tbody></table>"


def calendar():
    def period(label, start, end, group=""):
        cells = []
        for h in range(start, end + 1):
            cls = "reference" if h <= -8 else "prior" if h < 0 else "followup"
            cells.append(f'<span class="{cls}">{str(h).replace("-", "−")}</span>')
        return f'<div class="{group}"><strong>{label}</strong><div class="days" style="--day-count:{end - start + 1}">{"".join(cells)}</div></div>'

    before = "".join(period(f"Semana −{n}", -7 * n, -7 * n + 6) for n in (4, 3, 2, 1))
    immediate = period("Días 0–1", 0, 1)
    after = period("Días 2–6", 2, 6, "period-mid")
    week = period("Días 7–13", 7, 13, "period-late")
    return (f'<div class="calendar" aria-label="Días −28 a 13. Las semanas −4 a −2 forman la base común. El seguimiento abarca tres tramos.">'
            f'{before}<div class="split-period">{immediate}{after}</div>{week}</div>')


def models_table():
    labels = {
        "tratado": "Tratado × Después (" + math(r"\widehat{\tau}_{\mathrm{DD}}") + ")",
        "log_poblacion": "Logaritmo de población",
        "empleo_mil": "Empleo por mil habitantes",
        "autos_mil": "Autos por mil habitantes",
    }
    index = {(row["termino"], row["modelo"]): row for row in coefficients}
    body = []
    for term, label in labels.items():
        cells = [label]
        digits = 6 if term in ("empleo_mil", "autos_mil") else 3
        for n in range(4):
            row = index.get((term, f"M{n}"))
            if row is None:
                cells.append("—")
                continue
            cells.append(num(row["efecto"], digits) +
                         f'<span class="model-cell-stats">({num(row["ee"], digits)}) · {num(row["p"])}</span>')
        body.append(cells)
    return table(("Variable", *(math(f"M_{n}") for n in range(4))), body)


def wald_p(group):
    row, = (row for row in weekly if row["escenario"] == "principal" and row["muestra"] == "emparejada"
            and row["restricciones"] == "wk-4;wk-3;wk-1" and row["agrupacion"] == group)
    return num(row["p"])


m0 = math("M_0")
base_eq = math(
    r"B_{it}=\frac{1}{21}\sum_{k=-28}^{-8}Y_{i,t+k}"
    r"\qquad"
    r"\bar Y_{ith}=\frac{1}{|h|}\sum_{k\in h}Y_{i,t+k}",
    True,
)
reg_eq = math(
    r"\begin{aligned}Y_{i,d}={}&\underbrace{\alpha_{ith}}_{\text{Par}}"
    r"+\underbrace{\lambda_{th}\mathrm{Post}_s}_{\text{Inicio × bloque}}"
    r"+\underbrace{\delta_{h,\operatorname{ds}(d)}}_{\text{Día de la semana}}\\"
    r"&+\underbrace{\color{#235ca0}{\tau_{\mathrm{DD},h}}(\mathrm{Treat}_{it}\times\mathrm{Post}_s)}"
    r"_{\text{Tratado × Después}}"
    r"+\underbrace{(X_{it}^{\prime}\gamma_h)\mathrm{Post}_s}_{\text{Covariables}}"
    r"+\varepsilon_{ithsd}\end{aligned}",
    True,
)
initial = result()
initial_ci = f'[{num(initial["ic_inf"])}; {num(initial["ic_sup"])}]'
wald_state, wald_two = wald_p("entidad"), wald_p("entidad_fecha")

add("pregunta", "Municipios de México · 2019–2025", "¿Cómo cambian los siniestros viales registrados tras el inicio de narcoataques?", 20, """
<canvas class="cover-art" width="1100" height="1440" role="img" aria-label="Ilustración cenital de un choque entre dos autos en un cruce"></canvas>
<p class="byline"><span class="project-title">Narcoataques y siniestros viales registrados</span>
<strong>Eduardo Garcia Cortez · CU: 207480</strong><br>Inferencia Causal · ITAM</p>""",
"""¿Cómo cambian los siniestros viales registrados tras el inicio de narcoataques? El artículo de Bauernschuster y Rekers inspira el seguimiento diario después de un evento. Aquí observo las dos semanas desde el inicio.""",
"Primero, ¿por qué esperaríamos un cambio?", "Reporte, §1 y §5. Bauernschuster y Rekers (2022).", style="cover")

add("contexto", "Contexto", "Por qué podrían cambiar los siniestros viales registrados", 30, """
<div class="context-layout">
  <div>
    <h3>Mecanismos posibles</h3>
    <div class="context-path">
      <p><strong>Bloqueos o suspensión del transporte</strong></p>
      <span class="context-arrow" aria-hidden="true">→</span>
      <p>Menos circulación</p>
    </div>
    <div class="context-path">
      <p><strong>Desvíos</strong></p>
      <span class="context-arrow" aria-hidden="true">→</span>
      <p>Cambios de ruta y de riesgo por vía</p>
    </div>
    <div class="context-path">
      <p><strong>Factor humano</strong></p>
      <span class="context-arrow" aria-hidden="true">→</span>
      <p>Cambios al conducir, más atención y cuidado</p>
    </div>
  </div>
  <div>
    <h3>Interés</h3>
    <p>Evaluar si los narcoataques tienen un efecto causal sobre los siniestros viales registrados.</p>
  </div>
</div>""",
"""Los bloqueos, los desvíos y los cambios al conducir pueden afectar los siniestros. En este estudio, un narcoataque reúne acciones coordinadas en al menos tres lugares en 24 horas, con afectación del espacio público, los comercios o el transporte. Tres agentes de inteligencia artificial recopilaron prensa y comunicados. Se buscaron fuentes independientes para corroborar fecha y municipio. La cobertura es desigual y no hubo validación humana exhaustiva.""",
"El mapa ubica los municipios que entraron a la muestra.", "Reporte, §2 para la definición y apéndice E para la búsqueda web, la corroboración entre fuentes y los casos pendientes.")

add("datos", "Datos", "La muestra reúne 77 pares tratados", 50, f"""
<div class="map-context">
  <p><strong>31 episodios, 32 fechas</strong><br>Un municipio puede participar en distintas fechas.</p>
  <p><strong>Tratamiento</strong><br>Inicio local de una jornada coordinada de violencia.</p>
  <p><strong>Resultado</strong><br>Siniestros diarios registrados en vías no federales.</p>
</div>
<div class="map-pair">
  <figure><figcaption><span class="dot treated"></span>54 municipios tratados</figcaption>{figure("mapa-tratados.png", "Municipios de la muestra que figuran como tratados al menos una vez")}</figure>
  <figure><figcaption><span class="dot control"></span>765 municipios de control</figcaption>{figure("mapa-controles.png", "Municipios de la muestra que figuran como controles al menos una vez")}</figure>
</div>""",
"""Los mapas cuentan municipios únicos. En el análisis, la unidad es el par municipio–episodio. Un municipio reaparece si participa en otra fecha. Hay 31 episodios y 32 fechas porque un mismo episodio puede empezar en fechas distintas según el municipio. El tratamiento marca el inicio local, aunque la violencia continúe después. Los siniestros y las covariables provienen de fuentes oficiales. ATUS es la Estadística de Accidentes de Tránsito Terrestre en Zonas Urbanas y Suburbanas del Instituto Nacional de Estadística y Geografía, INEGI. Un cero indica cero registros publicados con fecha válida. El conteo tampoco mide el riesgo por viaje.""",
"Con esta unidad, podemos buscar municipios comparables para cada inicio.", "Reporte, §2 y apéndices A, E y F. Los 3 613 pares son 77 tratados y 3 536 controles.", data)

add("matching", "Estrategia empírica", "Cómo elegimos los controles para comparar cambios", 50, """
<div class="matching-flow">
  <div class="match-treated">
    <span class="dot treated" aria-hidden="true"></span>
    <h3>Municipio tratado</h3>
    <p>En su fecha de inicio</p>
  </div>
  <div class="match-arrow" aria-hidden="true"></div>
  <div class="match-pool">
    <h3>Candidatos elegibles</h3>
    <p>Estados ajenos al episodio, con cobertura y sin exposición documentada en la ventana previa.</p>
    <p>Accidentes previos, población, empleo y autos comparables.</p>
    <p class="match-support">≥10 candidatos · ≥5 estados</p>
  </div>
  <div class="match-fork" aria-hidden="true"></div>
  <div class="match-options">
    <div class="match-choice">
      <h3><span class="dot control" aria-hidden="true"></span>1:muchos</h3>
      <p>Todos los elegibles</p>
      <p class="match-weight">El peso se reparte entre ellos.</p>
    </div>
    <div class="match-choice">
      <h3><span class="dot control" aria-hidden="true"></span>1:1</h3>
      <p>El candidato más cercano</p>
      <p class="match-weight">Concentra el peso de los controles.</p>
    </div>
  </div>
</div>""",
"""El contrafactual es cómo habría cambiado el resultado del tratado sin el ataque. Para aproximarlo, busco controles en estados ajenos al episodio. Exijo cobertura en tres meses completos previos, estabilidad territorial y ausencia de exposición documentada desde el Día menos 49. Aplico márgenes de la mitad al doble en accidentes previos, población, empleo y autos. El mínimo es de diez candidatos de al menos cinco estados. Uno a muchos usa todos los elegibles y reparte el peso. Uno a uno elige al más cercano por población, empleo y autos. Después, diferencias en diferencias compara los cambios en las mismas fechas. Queremos estimar el efecto promedio de los pares tratados incluidos, con igual peso por par.""",
"Todos los tramos usan la misma base previa.", "Reporte, §3 y apéndice A. Covariables disponibles con medición anterior a t−28.")

add("base", "Estrategia empírica", "La base reúne 21 días, del −28 al −8", 50, f"""
<p class="lead">{math("Y_{i,d}")} cuenta los siniestros registrados del municipio {math("i")} en la fecha {math("d")}.</p>
{calendar()}
<div class="timeline-key"><span><i class="key-swatch reference"></i> Base común · días −28 a −8</span><span><i class="key-swatch followup"></i> Tramos posteriores</span><span>Semana −1 · diagnóstico previo</span></div>
<div class="math-band">
  {base_eq}
</div>""",
"""La base de cada par es el promedio de los 21 conteos de las semanas menos cuatro, menos tres y menos dos. Incluye tres lunes, tres martes y lo mismo para cada día de la semana. Para el inicio del jueves 17 de octubre de 2019 en Culiacán, abarca del 19 de septiembre al 9 de octubre. La semana menos uno sirve para detectar diferencias previas. Para cada tramo posterior, el resultado es el promedio de sus días. El día cero puede incluir horas anteriores al inicio local.""",
"El ajuste conserva una observación por día en cada bloque.", "Reporte, §3. La base de comparación y el promedio de cada tramo están en siniestros registrados por municipio y día.")

add("regresion", "Estrategia empírica", "Las filas diarias permiten ajustar por día de la semana", 50, f"""
<p class="reg-indices">{math("i")} municipio · {math("t")} inicio local · {math("d")} fecha del conteo · {math("h")} tramo · {math("s")} bloque</p>
<p class="reg-periods">{math(r"\mathrm{Post}_s=0")} en la base <span aria-hidden="true">·</span> {math(r"\mathrm{Post}_s=1")} en el tramo analizado</p>
<div class="math-band reg-equation">{reg_eq}</div>
<p class="reg-reading">Peso por día: {math(r"w_{it}/21")} en la base y {math(r"w_{it}/|h|")} en el tramo. Cada bloque conserva {math(r"w_{it}")}.</p>""",
"""Después indica el bloque que analizo, incluso si es un diagnóstico previo. El ajuste compara los cambios de tratados y controles con el mismo inicio. Cada bloque recibe el mismo peso por par, aunque tenga distinta duración. Uso el día de la semana de cada fecha del conteo, con lunes como referencia. Con dos filas agregadas, los efectos de inicio por bloque absorben esa información. Las filas diarias identifican los seis efectos. En el modelo principal los 77 tratados pesan igual. Los demás modelos ajustan por población, empleo y autos.""",
"Veamos los conteos que dan origen a esa comparación.", "Reporte, §3 y apéndice D. El ajuste absorbe efectos de par y de inicio por bloque. Los seis efectos de día de la semana se identifican por la variación dentro de cada bloque.")

add("eventos", "Estrategia empírica", "Cada grupo se compara con su propia base", 60, f"""
<div class="series-key"><span><i class="series-line treated"></i> Tratados</span><span><i class="series-line control"></i> Controles ponderados</span></div>
<div class="series-layout">
  <figure><figcaption>Promedios diarios · base sombreada</figcaption>{figure("eventos-observados.svg", "Promedio ponderado de los conteos de cada grupo, del día −28 al 13. El sombreado abarca la base de los días −28 a −8.")}</figure>
  <figure><figcaption>Cambio respecto a la base</figcaption>{figure("eventos-cambios.svg", "Cambios medios de tratados y controles en siniestros registrados por municipio y día, del día −7 al 13.")}</figure>
</div>
<p class="axis-caption">Días respecto al inicio local</p>""",
"""A la izquierda están los conteos medios en niveles. Alineo cada serie en el inicio local. Los tratados pesan lo mismo y los controles conservan los pesos del emparejamiento. El fondo sombreado marca los 21 días de la base. A la derecha, resto el promedio de esos días a cada par y después promedio los cambios dentro de cada grupo. El cero indica igualdad con la base propia. En el día menos dos los grupos ya muestran cambios distintos. Su distancia vertical reproduce el coeficiente diario del modelo principal: el ajuste de día de la semana es común dentro de cada fecha de inicio y se cancela al comparar los grupos.""",
"Ahora veamos esa distancia y sus intervalos de confianza.", "Muestra principal 1:muchos. El cotejo verifica los 21 contrastes diarios de M₀ contra la diferencia entre cambios ponderados.", sources)

add("trayectoria", "Supuestos", "Los grupos ya difieren antes del inicio", 45, f"""
<figure class="wide-chart">{figure("trayectoria-principal.svg", "Coeficientes diarios de los días −7 a 13. Los intervalos puntuales de los días −3 y −2 quedan por debajo de cero.")}
  <figcaption class="axis-caption">Días respecto al inicio local · {m0} · Intervalos del 95 % por estado y fecha</figcaption>
</figure>
<div class="diagnostic">
  <p><strong>Tendencias paralelas:</strong> cambios comparables en ausencia del ataque.</p>
  <p><strong>Prueba semanal:</strong> p = {wald_state} por estado y p = {wald_two} por estado y fecha.</p>
</div>""",
"""Cada punto compara el cambio de tratados y controles. En los días menos tres y menos dos, los intervalos puntuales quedan por debajo de cero. La prueba conjunta compara las semanas menos cuatro, menos tres y menos uno con la base común. Las tres semanas de la base suman cero frente a su promedio, así que la semana menos dos queda implícita. Se rechaza al cinco por ciento con agrupación estatal. Con la agrupación por estado y fecha, el valor p es 0,081. Las diferencias previas limitan cuánto podemos atribuir al inicio del ataque.""",
"Con esa cautela, veamos el resultado inicial y cuánto cambia con el ajuste.", "Reporte, §3–4, figura 1 y apéndice D. La gráfica usa el modelo M₀, emparejamiento 1:muchos y base de 21 días. La prueba semanal compara tres semanas con la base de 21 días.", sources)

add("resultados", "Resultados", "Añadir covariables cambia poco la estimación inicial", 35, f"""
{models_table()}
<p class="model-interval">En {m0}, el intervalo del 95 % es {initial_ci}.</p>""",
f"""El modelo inicial estima {num(-float(initial["efecto"]))} siniestros registrados menos por municipio y día en los días cero y uno. El intervalo agrupado por estado y fecha incluye cero. Al añadir logaritmo de población, empleo y autos por mil habitantes, la estimación cambia poco. Los cuatro modelos usan los mismos pares, pesos y efectos fijos.""",
"Veamos qué se estima en los tramos posteriores.", "Reporte, cuadro 2 y apéndices A y B. Los cuatro modelos usan 3 613 pares: 77 tratados y 3 536 de control.", sources,
table_note="Días 0–1 · 1:muchos · Siniestros registrados por municipio y día · Segunda línea: (error estándar) y valor p por estado y fecha.")

add("duracion", "Resultados", "La caída estimada es mayor en los días 0 y 1", 40, f"""
<figure>{figure("duracion.svg", "Los tres tramos muestran estimaciones negativas y sus intervalos incluyen cero.")}
  <figcaption class="axis-caption">{m0} · Intervalos del 95 % por estado y fecha</figcaption>
</figure>
<p class="duration-reading">Los tres intervalos incluyen cero.</p>""",
"""Cada punto resume un tramo. Se estiman menos 0,348 en los dos primeros días, menos 0,145 en los días dos a seis y menos 0,079 en la segunda semana, en siniestros registrados por municipio y día. Los tres intervalos incluyen cero. Los posteriores admiten caídas de magnitud relevante. La muestra que exige continuidad del reporte y aislamiento posterior cambia los pares disponibles. Con estos datos la duración sigue abierta.""",
"Veamos la sensibilidad al calendario y al inicio ficticio.", "Modelo M₀, 1:muchos. Reporte, §4, cuadros B1–B2 y apéndice D. Se permite que el episodio inicial continúe.", sources)

sensitivity_rows = []
for label, row in [
    ("Muestra principal", result()),
    ("Sin feriados ni recesos escolares", result(escenario="sin_laborales_escolares")),
    ("Placebo: inicio 28 días antes", result(escenario="placebo")),
]:
    short, = rows([(label, row)])
    sensitivity_rows.append((short[0], row["tratados"], *short[1:]))

add("sensibilidades", "Resultados", "Sensibilidad del resultado", 30, f"""
{table(("Comparación", "Pares tratados", "Estimación", "Intervalo del 95 %"), sensitivity_rows)}""",
"""Excluir feriados y recesos deja 25 tratados. El placebo ubica el inicio 28 días antes, reconstruye los pares y estima una caída menor. Los tres intervalos incluyen cero. Cada comparación usa la misma regla de base, los días menos veintiocho a menos ocho respecto a su inicio.""",
"¿Qué se puede sostener con ese conjunto de resultados?", "Reporte, cuadros B2–B3 y C1–C3. Siniestros registrados por municipio y día. Intervalos agrupados por estado y fecha. La sensibilidad amplia usa feriados laborales y recesos de educación básica.", sources,
table_note=f"Días 0–1 · {m0} · 1:muchos · Base días −28 a −8 · Siniestros registrados por municipio y día")

add("conclusion", "Conclusión", "La mayor caída estimada aparece al inicio", 20, f"""
<div class="closing-results">
  <div class="closing-estimate">
    <p class="closing-period">Días 0–1</p>
    <p class="closing-number">{num(initial["efecto"])} <span class="closing-scale">siniestros registrados por municipio y día</span></p>
    <p class="closing-interval">Intervalo del 95 % {initial_ci}</p>
  </div>
  <div class="closing-persistence">
    <p class="closing-period">Días 2–6 y 7–13</p>
    <h3>Duración incierta</h3>
    <p>Ambos intervalos incluyen cero.</p>
  </div>
</div>
<p class="closing-limit"><strong>Las diferencias previas</strong> entre tratados y controles limitan la atribución al ataque.</p>
<a class="backup-link" href="#/respaldos">Respaldos para discusión →</a>""",
"""La mayor caída estimada aparece en los días cero y uno. El intervalo incluye cero. La duración sigue abierta y las diferencias previas limitan cuánto podemos atribuir al ataque.""",
"Aquí termina la exposición. Las referencias y los respaldos quedan para consulta.", "Reporte, cuadro 2, §5 y apéndices E–G. El coeficiente mide la diferencia de cambios en siniestros registrados por municipio y día.", sources, style="closing")

add("referencias", "", "Referencias", 0, """
<ul class="reference-list">
  <li>Bauernschuster, S., &amp; Rekers, R. (2022). <a href="https://doi.org/10.1016/j.jpubeco.2022.104663">Speed limit enforcement and road safety</a>. <em>Journal of Public Economics, 210</em>, artículo 104663.</li>
  <li>Cámara de Diputados. (2025). <a href="https://www.ordenjuridico.gob.mx/Documentos/Federal/html/wo125151.html"><em>Ley Federal del Trabajo</em></a> (art. 74).</li>
  <li>Consejo Nacional de Población. (2024). <a href="https://www.gob.mx/conapo/documentos/reconstruccion-y-proyecciones-de-la-poblacion-de-los-municipios-de-mexico-1990-2040"><em>Reconstrucción y proyecciones de la población de los municipios de México, 1990–2040</em></a> [Base de datos].</li>
  <li>Garcia Cortez, E. (2026). <em>Catálogo municipal de narcoataques, 2019–2025</em> [Base de datos de elaboración propia].</li>
  <li>Instituto Nacional de Estadística y Geografía. (2015). <a href="https://www.inegi.org.mx/programas/intercensal/2015/"><em>Encuesta Intercensal 2015</em></a> [Tabulados de población y vivienda].</li>
  <li>Instituto Nacional de Estadística y Geografía. (2021). <a href="https://www.inegi.org.mx/programas/ccpv/2020/"><em>Censo de Población y Vivienda 2020</em></a> [Principales resultados por localidad, ITER].</li>
  <li>Instituto Nacional de Estadística y Geografía. (2025a). <a href="https://www.inegi.org.mx/temas/mg/"><em>Marco geoestadístico</em></a> [Cartografía municipal de diciembre de 2025].</li>
  <li>Instituto Nacional de Estadística y Geografía. (2025b). <a href="https://www.inegi.org.mx/app/saic/"><em>Sistema Automatizado de Información Censal</em></a> [Tabulados de empleo de 2018 y 2023].</li>
  <li>Instituto Nacional de Estadística y Geografía. (2026a). <a href="https://www.inegi.org.mx/programas/accidentes/"><em>Accidentes de Tránsito Terrestre en Zonas Urbanas y Suburbanas</em></a> [Microdatos, 2018–2025].</li>
  <li>Instituto Nacional de Estadística y Geografía. (2026b). <a href="https://www.inegi.org.mx/app/ageeml/"><em>Catálogo Único de Claves de Áreas Geoestadísticas Estatales, Municipales y Localidades</em></a>.</li>
  <li>Instituto Nacional de Estadística y Geografía. (2026c). <a href="https://www.inegi.org.mx/programas/vehiculosmotor/"><em>Vehículos de Motor Registrados en Circulación</em></a> [Registros municipales, 2018–2024].</li>
  <li>Secretaría de Educación de Veracruz. (2026). <a href="https://www.sev.gob.mx/educacion-basica/calendario-escolar/"><em>Calendarios escolares históricos de educación básica</em></a>.</li>
</ul>
<a class="backup-link" href="#/respaldos">Respaldos para discusión →</a>""",
"Las referencias quedan disponibles para consulta.", "Pasar al índice de respaldos si hay preguntas.", "Reporte, referencias y apéndices E y F.")

add("respaldos", "Discusión", "Respaldos para la discusión", 0, """
<nav class="backup-index" aria-label="Respaldos">
  <a href="#/soporte">¿Cómo se construye el grupo de control?</a>
  <a href="#/inferencia">¿Qué mide la incertidumbre?</a>
  <a href="#/contrastes">¿Qué cambia con el emparejamiento 1:1?</a>
  <a href="#/alternativas">¿Cómo se comparan las trayectorias diarias?</a>
</nav>""",
"Abre la pregunta correspondiente. Cada respaldo termina con un enlace al índice.", "Volver a la conclusión cuando termine la discusión.", "Reporte, apéndices A–H.")

add("soporte", "Discusión", "Soporte, balance y pesos", 0, f"""
<div class="backup-grid">
  <div><h3>Reglas de elegibilidad</h3><p>Tres meses completos con registros, territorio estable y ventana previa libre de exposición documentada.</p><p>Covariables con medición anterior a {math("t-28")} y razones entre 0,5 y 2.</p></div>
  <div><h3>Cómo se reparte el peso</h3><p>{math(r"C_{it}")} reúne los controles elegibles del tratado {math("i")} en {math("t")}.</p>
  <div class="math-band">{math(r"w_{it}=1\quad(\mathrm{Treat}_{it}=1),\qquad w_{ct}=\sum_{i:\,c\in C_{it}}\frac{1}{|C_{it}|}",True)}</div></div>
</div>
<p class="takeaway">La mayor diferencia estandarizada observada en 1:muchos es 0,082 en valor absoluto.</p>""",
"""El filtro de comparabilidad usa la media de los días menos 28 a menos 15. Su razón usa un desplazamiento de 0,5 en numerador y denominador. Las tres covariables cumplen por separado el margen. En uno a muchos, si un control se reutiliza en una fecha, se suman sus aportes; un tratado con cuarenta controles reparte una unidad en cuarenta partes. En uno a uno se elige el vecino por población, empleo y autos. La cobertura previa predice el universo, y los cambios posteriores de captación pueden afectar el resultado. El comparador observado requiere además ausencia de contagio y cambios paralelos.""",
"Volver al índice de respaldos.", "Reporte, cuadro 1, §3 y apéndices A y D.", sources)

add("inferencia", "Discusión", "La agrupación permite errores dependientes", 0, f"""
<div class="backup-grid">
  <div><h3>Intervalos puntuales</h3><p>Estado: dependencia entre municipios del mismo estado.</p><p>Fecha: dependencia entre municipios con el mismo inicio.</p><p>Omisión de estados: sensibilidad a la concentración del peso.</p></div>
  <div><h3>Diagnóstico previo por semanas</h3><p>Compara las semanas −4, −3 y −1 con la base de los días −28 a −8.</p><p>Por estado: p = {wald_state}.<br>Por estado y fecha: p = {wald_two}.</p></div>
</div>
<p class="takeaway">La agrupación cambia la precisión. El diagnóstico examina una fuente de sesgo.</p>""",
"""Se suma la covarianza por estado y por fecha y se resta la de su intersección. En los días cero y uno el panel tiene 83 099 filas. La corrección de muestra finita cuenta 3 613 pares y el rango del contraste entre bloques. Las desviaciones diarias dentro de cada bloque se cancelan al sumar las contribuciones a la varianza del contraste. La inferencia principal tiene 31 grados de libertad. El intervalo alternativo omite un estado por turno. Con la agrupación por estado y fecha, el efecto mínimo detectable del contraste inmediato es 0,690 siniestros registrados por municipio y día.""",
"Volver al índice de respaldos.", "Reporte, §3.1, §4 y apéndice D. El efecto mínimo detectable usa una prueba bilateral al 5 % y potencia del 80 %.", sources)

contrast_table = table(("Emparejamiento", "Estimación", "Intervalo del 95 %"), rows([
    ("1:muchos", result()),
    ("1:1", result(muestra="emparejada_1a1")),
]))
add("contrastes", "Discusión", "La estimación inmediata es negativa con ambos métodos", 0, f"""
<p class="lead">Días 0–1 · {m0} · 77 pares tratados · intervalos por estado y fecha</p>
{contrast_table}
<p class="takeaway">Ambos intervalos incluyen cero.</p>""",
"""El emparejamiento uno a uno conserva los 77 tratados. Se estiman 0,311 siniestros registrados menos por municipio y día. Los intervalos de ambos métodos incluyen cero. Cambian los controles y sus pesos.""",
"Volver al índice de respaldos.", "Reporte, §4, cuadro A5 y cuadros B1–B2. Estimaciones en siniestros registrados por municipio y día.", sources)

add("alternativas", "Discusión", "Trayectorias diarias de ambos emparejamientos", 0, f"""
<p class="lead">{m0} · Intervalos del 95 % por estado y fecha</p>
<div class="series-key"><span><i class="series-line estimate"></i> 1:muchos</span><span><i class="series-line control"></i> 1:1</span></div>
<figure class="wide-chart">{figure("trayectoria-niveles.svg", "Contrastes diarios en siniestros registrados por municipio y día con ambos emparejamientos.")}</figure>
<p class="axis-caption">Días respecto al inicio local</p>""",
"""Los dos métodos usan la base de 21 días y el ajuste por día de la semana. Uno a uno conserva los mismos 77 pares tratados. El cuadro de resultados y la trayectoria permiten ver cómo cambian la magnitud y la precisión al seleccionar otro conjunto de controles.""",
"Volver al índice de respaldos.", "Reporte, figura 1 y apéndices A–C.", sources)

assert sum(s["seconds"] for s in slides) == 480
assert len({s["id"] for s in slides}) == len(slides)


def clock(seconds):
    return f"{seconds // 60}:{seconds % 60:02d}"


elapsed = 0
html = []
script = ["# Guion de exposición", "", "**Narcoataques y siniestros viales registrados**", "",
          "Eduardo Garcia Cortez · CU: 207480 · Inferencia Causal · ITAM", "",
          "Ruta principal de **480 segundos (8:00)**. Los tiempos incluyen las transiciones. "
          "Para ensayar, lee la explicación oral y la transición. Las referencias y los respaldos quedan fuera del tiempo.", ""]
for slide in slides:
    id, title, seconds = (slide[k] for k in ("id", "title", "seconds"))
    kind = "main" if seconds else "references" if id == "referencias" else "backup"
    time = f"{clock(elapsed)}–{clock(elapsed + seconds)} ({seconds} s)" if seconds else "Fuera de la ruta cronometrada"
    elapsed += seconds
    if id == "respaldos":
        script += ["# Respaldos", ""]
    script += [f"## {title}", "", f"**Identificador** `{id}` · **Tiempo** {time}", "",
               "**Explicación oral**", "", slide["speech"], "", "**Transición**", "", slide["transition"], "",
               f"**Referencia para consulta.** {slide['locator']}", ""]
    source = f'<p class="source">Elaboración propia con datos de: {slide["source"]}</p>' if slide["source"] else ""
    footer = source
    if slide["table_note"]:
        footer = f'<footer class="table-footer"><p class="table-caption">{slide["table_note"]}</p>{source}</footer>'
    back = ('<a class="back-link" href="#/respaldos">← Índice de respaldos</a>'
            if kind == "backup" and id != "respaldos" else
            '<a class="back-link" href="#/conclusion">← Conclusión</a>' if id == "respaldos" else "")
    notes = (f'<p><strong>{escape(id)} · {escape(time)}</strong></p><p>{escape(slide["speech"])}</p>'
             f'<p><strong>Transición.</strong> {escape(slide["transition"])}</p>'
             f'<p><strong>Referencia para consulta.</strong> {escape(slide["locator"])}</p>')
    eyebrow = f'<p class="eyebrow">{slide["chapter"]}</p>' if slide["chapter"] else ""
    html.append(f'''<section id="{id}" class="{kind} {slide['style']}" data-timing="{seconds}">
  <div class="slide-surface">
    <header>{eyebrow}<{'h1' if id == 'pregunta' else 'h2'}>{escape(title)}</{'h1' if id == 'pregunta' else 'h2'}></header>
    {slide['body']}
    {footer}
    {back}
  </div>
  <aside class="notes">{notes}</aside>
</section>''')

document = '''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Narcoataques y siniestros viales registrados</title>
  <link rel="icon" href="data:,">
  <link rel="stylesheet" href="assets/vendor/reveal/reveal.css">
  <link rel="stylesheet" href="assets/vendor/katex/katex.min.css">
  <link rel="stylesheet" href="presenter.css">
  <link rel="stylesheet" href="theme.css">
</head>
<body>
  <div class="reveal"><div class="slides">
SLIDES
  </div></div>
  <script src="assets/vendor/reveal/reveal.js"></script>
  <script src="assets/vendor/reveal/plugin/notes.js"></script>
  <script src="assets/vendor/katex/katex.min.js"></script>
  <script src="deck.js"></script>
  <script src="presenter.js"></script>
</body>
</html>
'''
rendered = document.replace("SLIDES", "\n".join(html))
(DECK / "index.html").write_text("\n".join(line.rstrip() for line in rendered.splitlines()) + "\n", encoding="utf-8")
(DECK / "guion.md").write_text("\n".join(script), encoding="utf-8")
print(f"{sum(s['seconds'] > 0 for s in slides)} diapositivas en 480 segundos, "
      f"una de referencias y {sum(not s['seconds'] and s['id'] != 'referencias' for s in slides)} respaldos.")

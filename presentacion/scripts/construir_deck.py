"""Genera la presentación y el guion desde una sola fuente editorial."""
import csv
from html import escape
from pathlib import Path

DECK = Path(__file__).resolve().parents[1]
with (DECK / "assets/datos/efectos.csv").open(encoding="utf-8", newline="") as stream:
    effects = list(csv.DictReader(stream))

slides = []
data = "INEGI (ATUS y covariables), Consejo Nacional de Población (CONAPO) y catálogo propio."
sources = "INEGI (ATUS y covariables), CONAPO y catálogo propio."


def add(id, chapter, title, seconds, body, speech, transition, locator, source=None, style=""):
    slides.append(dict(id=id, chapter=chapter, title=title, seconds=seconds, body=body,
                       speech=speech, transition=transition, locator=locator, source=source, style=style))


def math(tex, block=False):
    cls = ' class="equation"' if block else ""
    return f'<span{cls} data-tex="{escape(tex, quote=True)}"></span>'


def figure(file, alt, *, extension="png"):
    return f'<img src="assets/{file}.{extension}" alt="{escape(alt, quote=True)}">'


def num(n):
    return f"{float(n):.3f}".replace(".", ",").replace("-", "−")


def result(tramo="d0..1", **options):
    key = dict(tramo=tramo, escenario="principal", muestra="emparejada", modelo="M0",
               escala="log1p", base="tres_semanas", agrupacion="entidad_fecha") | options
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
            cls = "reference" if h in {-28, -21, -14} else "prior" if h < 0 else "followup"
            cells.append(f'<span class="{cls}">{str(h).replace("-", "−")}</span>')
        return f'<div class="{group}"><strong>{label}</strong><div class="days" style="--day-count:{end - start + 1}">{"".join(cells)}</div></div>'

    before = "".join(period(f"Semana −{n}", -7 * n, -7 * n + 6) for n in (4, 3, 2, 1))
    immediate = period("Días 0–1", 0, 1)
    after = period("Días 2–6", 2, 6, "period-mid")
    week = period("Días 7–13", 7, 13, "period-late")
    return (f'<div class="calendar" aria-label="Días −28 a 13. El seguimiento posterior abarca tres tramos.">'
            f'{before}<div class="split-period">{immediate}{after}</div>{week}</div>')


def models_table():
    report = (DECK.parent / "reporte/reporte.md").read_text(encoding="utf-8")
    panel = report.split("**Panel A. Resultado:", 1)[1].split("\n\nCada celda", 1)[0]
    labels = {
        "Tratamiento": "Tratamiento (" + math(r"\widehat{\beta}") + ")",
        "Logaritmo de la población": "Logaritmo de población",
        "Empleo por cada mil habitantes": "Empleo por mil habitantes",
        "Automóviles por cada mil habitantes": "Autos por mil habitantes",
        "$R^2$ ponderado": math("R^2") + " ponderado",
        "$R^2$ tras descontar las fechas": math("R^2") + " tras descontar fechas",
    }
    body = []
    for line in panel.splitlines():
        if not line.startswith("|"):
            continue
        label, *values = [value.strip() for value in line.strip("|").split("|")]
        if label not in labels:
            continue
        cells = []
        for value in values:
            coefficient, *stats = value.replace("-", "−").split("<br>")
            detail = ""
            if stats:
                p_value = stats[2].removeprefix("$p=").removesuffix("$").replace("{,}", ",")
                p_number = float(p_value.replace(",", "."))
                stars = next((mark for limit, mark in ((0.001, "***"), (0.01, "**"), (0.05, "*"))
                              if p_number <= limit), "")
                if stars:
                    coefficient += f'<sup class="model-stars">{stars}</sup>'
                detail = f'<span class="model-cell-stats">{stats[0]} · {p_value}</span>'
            cells.append(coefficient + detail)
        body.append((labels[label], *cells))
    if len(body) != len(labels) or any(len(row) != 5 for row in body):
        raise ValueError("El cuadro de regresiones del reporte no tiene la estructura esperada")
    models = tuple(math(f"M_{n}") for n in range(4))
    return table(("Variable / estadístico", *models), body)


log = math(r"\log(1+Y)")
outcome = f'{math("Y")} = siniestros registrados por municipio y día'
m0 = math("M_0")
base_eq = math(
    r"\left.\begin{aligned}"
    r"g(y)&=\log(1+y)\\"
    r"B_{ith}^{g}&=\tfrac13\sum_{k\in\{28,21,14\}}g(Y_{i,r(t,h)-k})"
    r"\end{aligned}\right\}"
    r"\quad{\color{#235ca0}\longrightarrow}\quad"
    r"\Delta_{ith}^{g}=g(Y_{i,t+h})-B_{ith}^{g}",
    True,
)
reg_eq = math(
    r"\underbrace{\Delta_{ith}^{g}}_{\text{cambio}}"
    r"=\underbrace{\lambda_{th}}_{\text{FE de fecha}}"
    r"+\underbrace{\color{#235ca0}{\beta_h^{g}D_{it}}}_{\text{tratamiento}}"
    r"+\underbrace{X_{it}^{\prime}\gamma_h}_{\text{covariables}}"
    r"+\underbrace{u_{ith}}_{\text{residuo}}",
    True,
)

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
  <p><strong>Resultado</strong><br>Accidentes registrados en vías no federales.</p>
</div>
<div class="map-pair">
  <figure><figcaption><span class="dot treated"></span>54 municipios tratados</figcaption>{figure("mapa-tratados", "Municipios de la muestra que figuran como tratados al menos una vez")}</figure>
  <figure><figcaption><span class="dot control"></span>765 municipios de control</figcaption>{figure("mapa-controles", "Municipios de la muestra que figuran como controles al menos una vez")}</figure>
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
"La comparación requiere una base previa para cada día analizado.", "Reporte, §3 y apéndice A. Covariables disponibles con medición anterior a t−28.")

add("base", "Estrategia empírica", "Cada día tiene tres referencias previas", 50, f"""
<p class="lead">Para el Día 0, se promedian las tres fechas resaltadas del mismo día de la semana.</p>
{calendar()}
<div class="timeline-key"><span><i class="key-swatch reference"></i> Referencias del Día 0</span><span><i class="key-swatch followup"></i> Tramos analizados</span><span>Semana −1 · diagnóstico previo</span></div>
<div class="math-band">
  {base_eq}
</div>""",
"""Analizo tres tramos posteriores: días cero a uno, dos a seis y siete a trece. Si el inicio es jueves, uso los jueves menos 28, menos 21 y menos 14. El jueves siguiente reutiliza esas referencias. Dejo fuera la semana menos uno para ver si los grupos ya divergían. En la fórmula, i indica municipio, t el inicio local, h el día relativo y r conserva el día de la semana. Aplico logaritmo de uno más Y a cada conteo antes de promediar las tres referencias. Resto esa base del valor observado. Cada tramo promedia cambios diarios. El Día 0 puede incluir horas anteriores al inicio.""",
"Una vez que cada municipio tiene un cambio, podemos contrastarlo con el de sus controles.", "Reporte, §3. La regla r(t,h) = t + (h mod 7) mantiene la base entre los días −28 y −8. El ejemplo usa el jueves 17 de octubre de 2019 en Culiacán.")

add("regresion", "Estrategia empírica", "Estimación por mínimos cuadrados ponderados", 50, f"""
<div class="math-band reg-equation">{reg_eq}</div>
<p class="reg-reading"><strong>{math(r"\boldsymbol{\beta_h^g}")} mide la diferencia entre cambios.</strong></p>
<p class="reg-estimand"><strong>Estimamos ATT en escala {math(r"\boldsymbol{\log(1+Y)}")}.</strong></p>""",
"""La variable dependiente es el cambio que acabamos de construir. D vale uno para el tratado y cero para un control. Lambda es el efecto fijo de fecha y descuenta cambios comunes a cada inicio. Beta es la diferencia entre cambios. Buscamos estimar el efecto promedio del tratamiento sobre los tratados, el ATT. X reúne covariables previas, gamma sus coeficientes y u el residuo. La regresión usa mínimos cuadrados ponderados. En M cero, cada tratado pesa uno y distribuye una unidad de peso entre sus controles. Equivale a promediar 77 contrastes, uno por par tratado. M uno añade logaritmo de población, M dos empleo por mil habitantes y M tres autos por mil. La muestra y los pesos explícitos se conservan.""",
"Veamos las trayectorias que dan origen a ese contraste.", "Reporte, §3 y §3.1. Los modelos ajustados pueden cambiar la ponderación implícita.")

add("eventos", "Estrategia empírica", "Promedios y cambios de tratados y controles", 60, f"""
<p class="lead">1:muchos · 77 pares tratados y 3 536 de control</p>
<div class="series-key"><span><i class="series-line treated"></i> Tratados</span><span><i class="series-line control"></i> Controles ponderados</span><span>{outcome}</span></div>
<div class="series-layout">
  <figure><figcaption>Promedio observado</figcaption>{figure("eventos-observados", "Promedios observados por grupo, del día −28 al 13.")}</figure>
  <figure><figcaption>Cambio medio respecto a la base</figcaption>{figure("eventos-cambios", "Cambios medios de tratados y controles en log(1+Y), del día −7 al 13.")}</figure>
</div>
<p class="axis-caption">Días respecto al inicio local · Día 0 en línea punteada</p>""",
"""A la izquierda, cada línea promedia los valores observados de logaritmo de uno más Y. Alineo cada serie en su inicio local. Los tratados pesan lo mismo y los controles conservan los pesos del emparejamiento. A la derecha, resto a cada par su propia base del mismo día semanal y después promedio por grupo. El cero de este panel indica igualdad con la base propia. Justo antes del inicio, por ejemplo en el Día menos dos, las dos líneas registran cambios distintos. La distancia vertical entre ellas da el coeficiente diario del modelo M cero. Así llegamos a un contraste de cambios con unidades y pesos definidos.""",
"Ahora podemos ver esa distancia como una sola trayectoria, con su incertidumbre.", "Conteos diarios limpios y pares y pesos guardados. Las 21 diferencias de cambios reproducen los coeficientes de M₀.", sources)

add("trayectoria", "Supuestos", "Diagnóstico de tendencias paralelas", 45, f"""
<p class="lead">{outcome} <span class="chart-meta"> · {m0} · 1:muchos · Intervalos puntuales del 95 %</span></p>
<figure class="wide-chart">{figure("trayectoria-principal", "Coeficientes de los días −7 a 13. Los días −5 y −2 muestran diferencias negativas antes del inicio.")}</figure>
<p class="axis-caption">Días respecto al inicio local</p>
<div class="diagnostic">
  <p><strong>Tendencias paralelas:</strong> cambios comparables en ausencia del ataque.</p>
  <p><strong>Prueba previa por semanas:</strong> rechaza por estado; es inconclusa por estado y fecha.</p>
</div>""",
"""Cada punto es la diferencia entre los cambios de tratados y controles. Es el coeficiente estimado, beta gorro. Las barras muestran la incertidumbre de esa diferencia. Antes del Día 0 esperamos que los puntos fluctúen alrededor de cero. Aquí aparecen diferencias puntuales, como en el Día −2. La prueba por semanas detecta diferencias al agrupar por estado y es inconclusa al agrupar por estado y fecha. Por eso interpreto con cautela la caída que aparece al inicio.""",
"Con esa cautela, veamos el resultado inicial y cuánto cambia con el ajuste.", "Reporte, §3–4, figura 1 y apéndice D. La prueba semanal compara Sem. −4, −3 y −1 con Sem. −2.", sources)

add("resultados", "Resultados", "Añadir covariables cambia poco la estimación inicial", 35, f"""
<p class="lead">Días 0–1 · 1:muchos · Cambio en {log} · Efectos fijos de fecha</p>
{models_table()}
<p class="model-caption">3 613 pares municipio–fecha · Segunda línea con (error estándar) y valor p bilateral, por estado y fecha.</p>""",
"""En M cero, menos 0,107 es el coeficiente estimado del tratamiento. Resta al cambio medio de los tratados el de sus controles, respecto a la base y en la escala de logaritmo de uno más Y. Su valor p es 0,019. Cada columna añade al modelo anterior logaritmo de población, empleo o autos por mil habitantes. El coeficiente cambia poco. En conteos y con el emparejamiento uno a uno, los intervalos del tratamiento incluyen cero.""",
"Veamos si la caída persiste después del primer tramo.", "Reporte, cuadro 2, Panel A, y apéndices A y B. Los asteriscos siguen los umbrales de R: 0,001 (***), 0,01 (**) y 0,05 (*). Los coeficientes de las covariables son ajustes estadísticos.", sources)

add("duracion", "Resultados", "La caída estimada es mayor en los días 0 y 1", 40, f"""
<p class="lead">{m0} · 1:muchos · {outcome} <span class="chart-meta"> · Intervalos del 95 % por estado y fecha</span></p>
<figure class="duration-chart">{figure("duracion", "La mayor caída se estima para los días 0 y 1. Los intervalos de 2 a 6 y 7 a 13 incluyen cero.", extension="svg")}
  <figcaption>Los intervalos de los <strong>días 2–6 y 7–13</strong> incluyen cero.</figcaption>
</figure>""",
"""Cada punto resume un tramo y tiene su propio intervalo. La mayor caída se estima en los días cero a uno: menos 0,107 en la escala logarítmica. Después, los coeficientes están más cerca de cero y sus intervalos admiten una caída y un cambio nulo. La señal de los días siete a trece depende de la agrupación y las exclusiones. Si exijo continuidad del registro y ausencia de otro ataque posterior, cambia la muestra. El seguimiento hasta el Día trece deja abierta la duración.""",
"La base y el calendario también afectan la lectura del resultado inicial.", "Reporte, §4, cuadros B1–B2 y apéndice D. Se permite que el episodio inicial continúe.", sources)

sensitivity_rows = []
for label, row in [
    ("Base principal: tres fechas", result()), ("Base: semana anterior", result(base="wk-1")),
    ("Base: Día −2", result(base="-2")), ("Sin feriados ni recesos escolares", result(escenario="sin_laborales_escolares")),
    ("Placebo: inicio 28 días antes", result(escenario="placebo")),
]:
    short, = rows([(label, row)])
    sensitivity_rows.append((short[0], row["tratados"], *short[1:]))

add("sensibilidades", "Resultados", "La referencia previa y el calendario importan", 30, f"""
<p class="lead">Días 0–1 · {m0}, 1:muchos, {log} · intervalos por estado y fecha</p>
{table(("Comparación", "Pares tratados", "Estimación", "Intervalo del 95 %"), sensitivity_rows)}
<p class="takeaway">Cambiar la base conserva los pares. Excluir fechas cambia la muestra.</p>""",
"""Con los mismos pares y pesos, la semana previa reduce la magnitud de la caída y el Día menos dos cambia el signo. Ambos intervalos incluyen cero. Sin feriados ni recesos, la muestra queda en 25 tratados y aumenta la incertidumbre. El placebo reconstruye la comparación 28 días antes y da una caída de menor magnitud, con un intervalo que incluye cero.""",
"¿Qué se puede sostener con ese conjunto de resultados?", "Reporte, cuadros B2–B3 y C1–C4. La sensibilidad amplia usa feriados laborales y recesos de educación básica.", sources)

add("conclusion", "Conclusión", "La mayor caída relativa aparece al inicio", 20, """
<p class="closing-summary">La caída destaca en los días 0–1. Después, las estimaciones son menores y la duración sigue abierta.</p>
<p class="closing-limit"><strong>Limitación</strong><br>Las diferencias previas entre los grupos limitan la atribución causal.</p>
<a class="backup-link" href="#/respaldos">Respaldos para discusión →</a>""",
"""La mayor caída relativa de registros aparece al inicio. Después, las estimaciones son menores y queda abierta la duración. La limitación central para atribuir la caída al ataque es que tratados y controles ya mostraban diferencias antes del inicio.""",
"Aquí termina la exposición. Los respaldos sirven para la discusión.", "Reporte, §5 y apéndices E–G.", style="closing")

add("respaldos", "Discusión", "Respaldos para la discusión", 0, """
<nav class="backup-index" aria-label="Respaldos">
  <a href="#/soporte">¿Cómo se construye el grupo de control?</a>
  <a href="#/inferencia">¿Qué mide la incertidumbre?</a>
  <a href="#/contrastes">¿Qué pasa con 1:1 o en niveles?</a>
  <a href="#/alternativas">¿Cómo cambian las trayectorias?</a>
  <a href="#/alcance">¿Qué cubren el catálogo y los registros?</a>
  <a href="#/fuentes">¿Qué aporta el antecedente alemán?</a>
</nav>""",
"Abre la pregunta correspondiente. Cada respaldo termina con un enlace al índice.", "Volver a la conclusión cuando termine la discusión.", "Reporte, apéndices A–H.")

add("soporte", "Discusión", "Soporte, balance y pesos", 0, f"""
<div class="backup-grid">
  <div><h3>Reglas de elegibilidad</h3><p>Tres meses completos con registros, territorio estable y ventana previa libre de exposición documentada.</p><p>Covariables con medición anterior a {math("t-28")} y razones entre 0,5 y 2.</p></div>
  <div><h3>Cómo se reparte el peso</h3><p>{math(r"C_{it}")} reúne los controles elegibles del tratado {math("i")} en {math("t")}.</p>
  <div class="math-band">{math(r"w_{it}=1\quad(D_{it}=1),\qquad w_{ct}=\sum_{i:\,c\in C_{it}}\frac{1}{|C_{it}|}",True)}</div></div>
</div>
<p class="takeaway">La mayor diferencia estandarizada observada en 1:muchos es 0,082 en valor absoluto.</p>""",
"""El nivel de accidentes se calcula en Días menos 28 a menos 15. Su razón usa un desplazamiento de 0,5 en numerador y denominador. Las tres covariables cumplen por separado el margen. En uno a muchos, si un control se reutiliza en una fecha, se suman sus aportes; un tratado con cuarenta controles reparte una unidad en cuarenta partes. En uno a uno se elige el vecino por población, empleo y autos. La cobertura previa predice el universo, y los cambios posteriores de captación pueden afectar el resultado. El comparador observado requiere además ausencia de contagio y cambios paralelos.""",
"Volver al índice de respaldos.", "Reporte, cuadro 1, §3 y apéndices A y D.", sources)

add("inferencia", "Discusión", "La agrupación permite errores dependientes", 0, f"""
<div class="backup-grid">
  <div><h3>Intervalos puntuales</h3><p>Estado: dependencia entre municipios del mismo estado.</p><p>Fecha: dependencia entre municipios con el mismo inicio.</p><p>Omisión de estados: sensibilidad a la concentración del peso.</p></div>
  <div><h3>Diagnóstico previo por semanas</h3><p>Compara las semanas −4, −3 y −1 con la −2.</p><p>Por estado: {math(r"p<0{,}001")}.<br>Por estado y fecha: {math(r"p=0{,}109")}.</p></div>
</div>
<p class="takeaway">La agrupación cambia la precisión. El diagnóstico examina una fuente de sesgo.</p>""",
"""La agrupación en dos dimensiones admite dependencia por estado y por fecha, descuenta su intersección y conserva el coeficiente. Se distingue de un ajuste de Bonferroni: los intervalos de la trayectoria tienen cobertura nominal por punto. Catorce estados aportan tratados y el peso está concentrado. El intervalo alternativo omite un estado a la vez, conserva los pesos de las filas restantes y vuelve a absorber las fechas. En la prueba previa, la semana menos dos es el punto de referencia para una comparación conjunta distinta de la base diaria y del placebo. El efecto mínimo detectable en niveles para Días 0–1 es de 0,664 registros por municipio y día, bajo prueba bilateral del 5 por ciento y potencia del 80 por ciento.""",
"Volver al índice de respaldos.", "Reporte, §3.1, §4 y apéndice D.", sources)

contrast_table = table(("Modelo y escala", "Estimación", "Intervalo del 95 %"), rows([
    (f"{m0} · 1:muchos · {log}", result()),
    (f"{m0} · 1:1 · {log}", result(muestra="emparejada_1a1")),
    (f"{m0} · 1:muchos · registros por municipio y día", result(escala="niveles")),
]))
add("contrastes", "Discusión", "El signo se mantiene con 1:1 y en niveles", 0, f"""
<p class="lead">Días 0–1 · 77 pares tratados · intervalos por estado y fecha</p>
{contrast_table}
<p class="takeaway">Con 1:1 y en niveles, el intervalo incluye cero.</p>""",
"""En uno a uno la magnitud es similar y el intervalo se amplía. En niveles se estiman 0,397 registros menos por municipio y día. El intervalo admite otras magnitudes y un cambio nulo. La transformación exponencial del coeficiente principal da una caída del 10,2 por ciento en la escala geométrica de uno más Y. La media aritmética de los accidentes corresponde a otra cantidad.""",
"Volver al índice de respaldos.", "Reporte, §4 y cuadros B1–B2.", sources)

add("alternativas", "Discusión", "En niveles cambia la precisión", 0, f"""
<p class="lead">{m0} · Intervalos del 95 %</p>
<div class="series-key"><span><i class="series-line estimate"></i> 1:muchos</span><span><i class="series-line control"></i> 1:1</span></div>
<figure class="wide-chart">{figure("trayectoria-niveles", "Comparación diaria a escala de conteos para ambos emparejamientos.")}</figure>
<p class="axis-caption">Días respecto al inicio local · agrupación por estado y fecha</p>""",
"""En niveles, el punto se interpreta como registros por municipio y día. En uno a uno usamos los mismos 77 pares tratados y cambiamos comparadores y pesos. Un intervalo que incluye cero admite un cambio nulo y también otros efectos. Que un método excluya cero y otro lo incluya no establece una diferencia estadística entre métodos. Las tendencias paralelas se requieren en la escala empleada. La comparación semanal de la crisis prolongada de Culiacán desde septiembre de 2024 queda fuera del reporte y de esta exposición.""",
"Volver al índice de respaldos.", "Reporte, figura 1, apéndices A–C y README del repositorio.", sources)

add("alcance", "Discusión", "Los registros y el catálogo tienen coberturas distintas", 0, """
<div class="backup-grid">
  <div><h3>Accidentes y covariables</h3><p>ATUS cuenta registros publicados. Población, empleo, automóviles y territorio proceden de fuentes oficiales.</p><p>La población anual de CONAPO sirve de denominador para las tasas por mil.</p></div>
  <div><h3>Catálogo de ataques</h3><p>Tres agentes de inteligencia artificial asistieron la búsqueda web, con cobertura desigual y sin validación humana exhaustiva.</p><p>La muestra conserva los episodios puntuales de Culiacán de 2019 y 2023.</p></div>
</div>""",
"""El catálogo recoge prensa y comunicados sobre acciones coordinadas. Los cotejos entre agentes ayudan a corroborar casos y dejan incertidumbre en la cobertura. Las exclusiones de casos pendientes o señales en controles corresponden a sensibilidades del reporte. ATUS se concentra en vías no federales. El registro puede cambiar si se altera la atención de emergencias o el proceso de publicación. Las covariables se enlazan con medición previa a la base, aunque las ediciones consultadas son retrospectivas. El apéndice H contiene el código R reproducible.""",
"Volver al índice de respaldos.", "Reporte, §2 y apéndices A, C, E, F y H.")

add("fuentes", "Discusión", "El antecedente alemán orienta la pregunta temporal", 0, """
<div class="backup-grid">
  <div><h3>Artículo de referencia</h3><p>Bauernschuster, S. y Rekers, R. (2022). <em>Speed limit enforcement and road safety.</em> Journal of Public Economics, 210, 104663.</p><p>Frecuencia diaria, exposición transitoria y duración.</p></div>
  <div><h3>Proyecto de Inferencia Causal</h3><p>Eduardo Garcia Cortez · ITAM · Mauricio Romero.</p><p>El diseño adapta el emparejamiento y la base al contexto mexicano.</p></div>
</div>""",
"""El artículo aprovecha fechas de operativos y participación por estado en Alemania. Le tomo la pregunta por la duración de un cambio tras una exposición transitoria y la frecuencia diaria. El diseño mexicano usa inicios locales que pueden repetirse y compara municipios seleccionados para las mismas fechas. La base y las reglas de emparejamiento responden a ese problema.""",
"Volver al índice de respaldos.", "Bauernschuster y Rekers (2022), figuras 1 y 4. Reporte, §1 y §3.")

assert sum(s["seconds"] for s in slides) == 480
assert len({s["id"] for s in slides}) == len(slides)


def clock(seconds):
    return f"{seconds // 60}:{seconds % 60:02d}"


elapsed = 0
html = []
script = ["# Guion de exposición", "", "**Narcoataques y siniestros viales registrados**", "",
          "Eduardo Garcia Cortez · CU: 207480 · Inferencia Causal · ITAM", "",
          "Ruta principal de **480 segundos (8:00)**. Los tiempos incluyen las transiciones. "
          "Para ensayar, lee la explicación oral y la transición. Los respaldos quedan fuera del tiempo.", ""]
for slide in slides:
    id, title, seconds = (slide[k] for k in ("id", "title", "seconds"))
    kind = "main" if seconds else "backup"
    time = f"{clock(elapsed)}–{clock(elapsed + seconds)} ({seconds} s)" if seconds else "Fuera de la ruta cronometrada"
    elapsed += seconds
    if id == "respaldos":
        script += ["# Respaldos", ""]
    script += [f"## {title}", "", f"**Identificador** `{id}` · **Tiempo** {time}", "",
               "**Explicación oral**", "", slide["speech"], "", "**Transición**", "", slide["transition"], "",
               f"**Referencia para consulta.** {slide['locator']}", ""]
    source = f'<p class="source">Elaboración propia con datos de: {slide["source"]}</p>' if slide["source"] else ""
    back = ('<a class="back-link" href="#/respaldos">← Índice de respaldos</a>'
            if kind == "backup" and id != "respaldos" else
            '<a class="back-link" href="#/conclusion">← Conclusión</a>' if id == "respaldos" else "")
    notes = (f'<p><strong>{escape(id)} · {escape(time)}</strong></p><p>{escape(slide["speech"])}</p>'
             f'<p><strong>Transición.</strong> {escape(slide["transition"])}</p>'
             f'<p><strong>Referencia para consulta.</strong> {escape(slide["locator"])}</p>')
    html.append(f'''<section id="{id}" class="{kind} {slide['style']}" data-timing="{seconds}">
  <div class="slide-surface">
    <header><p class="eyebrow">{slide['chapter']}</p><{'h1' if id == 'pregunta' else 'h2'}>{escape(title)}</{'h1' if id == 'pregunta' else 'h2'}></header>
    {slide['body']}
    {source}
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
print(f"{sum(s['seconds'] > 0 for s in slides)} diapositivas en 480 segundos, {sum(not s['seconds'] for s in slides)} respaldos.")

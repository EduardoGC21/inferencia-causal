"""Adapta observaciones y estimaciones guardadas al lienzo de exposición."""
from io import StringIO
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd
from PIL import Image

ASSETS = Path(__file__).resolve().parents[1] / "assets"
INK, BLUE, AMBER, MUTED = "#142e4b", "#235ca0", "#a04a21", "#555f70"
UNIT = "Siniestros registrados por municipio y día"
POINTS = list(range(-7, 14))
effects = pd.read_csv(ASSETS / "datos/efectos.csv", dtype={"tramo": str})

plt.rcParams.update({
    "font.family": ["Arial", "sans-serif"], "font.size": 14.4,
    "svg.fonttype": "none",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False, "axes.spines.bottom": False,
    "xtick.color": INK, "ytick.color": INK,
    "text.color": INK, "axes.labelcolor": INK,
    "figure.facecolor": "white",
})


def decimal(x, _):
    return f"{0 if x == 0 else x:g}".replace("-", "−").replace(".", ",")


def canvas(width, height, left, right, bottom=.15, top=.96):
    fig, ax = plt.subplots(figsize=(width / 100, height / 100))
    fig.subplots_adjust(left=left, right=right, bottom=bottom, top=top)
    ax.tick_params(axis="both", length=0, pad=8)
    return fig, ax


def days(ax, first, ticks):
    ax.set_xlim(first - .6, 13.6)
    ax.set_xticks(ticks, [str(i).replace("-", "−") for i in ticks])
    ax.axvline(0, color=MUTED, linewidth=1.4, linestyle=(0, (3, 3)), zorder=1)


def save(fig, name):
    output = StringIO()
    with plt.rc_context({"svg.hashsalt": f"inferencia-{name}"}):
        fig.savefig(output, format="svg", metadata={"Date": None})
    svg = "\n".join(line.rstrip() for line in output.getvalue().splitlines()) + "\n"
    (ASSETS / f"{name}.svg").write_text(svg, encoding="utf-8", newline="\n")
    plt.close(fig)


def descriptive(series, field, name, first, ticks):
    fig, ax = canvas(552, 362, .22, .97, bottom=.13)
    for group, color, marker, line in [
        ("tratados", AMBER, "o", "-"), ("controles", BLUE, "s", (0, (4, 2))),
    ]:
        ax.plot(series.index, series[f"{field}_{group}"], color=color,
                marker=marker, markersize=2.5, linestyle=line, linewidth=1.65)
    days(ax, first, ticks)
    if field == "observado":
        ax.set_ylabel("Siniestros registrados\npor municipio y día")
        ax.axvspan(-28.6, -7.5, color="#edf2f7", zorder=0)
    else:
        ax.set_ylabel("Cambio en siniestros\npor municipio y día")
        ax.axhline(0, color=MUTED, linewidth=1, alpha=.67)
    ax.margins(y=.12)
    ax.yaxis.set_major_formatter(FuncFormatter(decimal))
    save(fig, name)


def trajectory(methods, name, *, height=332):
    fig, ax = canvas(1128, height, .112, .984, bottom=.15)
    ax.set_ylabel("Siniestros registrados\npor municipio y día")
    for j, (method, color, marker, line) in enumerate(methods):
        data = effects.loc[
            effects.escenario.eq("principal") & effects.muestra.eq(method)
            & effects.modelo.eq("M0") & effects.base.eq("tres_semanas")
            & effects.escala.eq("niveles") & effects.agrupacion.eq("entidad_fecha")
        ].set_index("tramo").loc[list(map(str, POINTS))]
        x = np.array(POINTS) + (j - (len(methods) - 1) / 2) * .23
        y = data.efecto.to_numpy()
        ax.errorbar(x, y, yerr=np.vstack((y - data.ic_inf, data.ic_sup - y)),
                    color=color, fmt=marker, markersize=4.6, capsize=3.4,
                    elinewidth=1.3, linestyle=line, linewidth=1.25, zorder=2 + j)
    ax.axhline(0, color=MUTED, linewidth=1, alpha=.67)
    days(ax, -7, POINTS)
    ax.yaxis.set_major_formatter(FuncFormatter(decimal))
    save(fig, name)


def duration():
    data = effects.query("escenario == 'principal' and muestra == 'emparejada' and modelo == 'M0' "
                         "and base == 'tres_semanas' and escala == 'niveles' and agrupacion == 'entidad_fecha'")
    rows = data.set_index("tramo").loc[["d0..1", "d2..6", "wk+1"]]
    fig, ax = canvas(1128, 374, .176, .978, bottom=.19)
    ax.set_ylabel("Tramo analizado")
    ax.set_xlabel(UNIT)
    ax.axvline(0, color=MUTED, linewidth=1.2, alpha=.68)
    for y, (_, row), color in zip([2, 1, 0], rows.iterrows(), [BLUE, INK, INK]):
        ax.errorbar(row.efecto, y, xerr=[[row.efecto - row.ic_inf], [row.ic_sup - row.efecto]],
                    fmt="o", color=color, markersize=7, linewidth=2, capsize=5)
    ax.set_yticks([2, 1, 0], ["Días 0–1", "Días 2–6", "Días 7–13"])
    ax.margins(x=.12)
    ax.set_ylim(-.5, 2.5)
    ax.xaxis.set_major_formatter(FuncFormatter(decimal))
    save(fig, "duracion")


series = pd.read_csv(ASSETS / "datos/series-eventos.csv", index_col="h")
descriptive(series, "observado", "eventos-observados", -28, [-28, -21, -14, -7, 0, 7, 13])
descriptive(series, "cambio", "eventos-cambios", -7, [-7, -5, -2, 0, 3, 7, 10, 13])
methods = [("emparejada", INK, "o", "-"), ("emparejada_1a1", BLUE, "s", "--")]
trajectory(methods[:1], "trayectoria-principal", height=364)
trajectory(methods, "trayectoria-niveles")
duration()

original = Image.open(ASSETS.parent.parent / "reporte/figuras/mapa-municipios.png").convert("RGB")
w, h = original.size
for name, (start, end) in [("tratados", (.060, .488)), ("controles", (.533, .96))]:
    panel = original.crop((0, int(h * start), w, int(h * end)))
    gray = panel.convert("L").point(lambda x: 255 if x < 249 else 0)
    panel.crop(gray.getbbox()).save(ASSETS / f"mapa-{name}.png")

print("Figuras listas: dos mapas, dos series descriptivas, dos trayectorias y duración.")

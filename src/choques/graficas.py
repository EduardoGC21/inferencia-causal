import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


BLUE = "#135a76"
GRAY = "#686d70"
ACCENT = "#974421"


def axes(size, title, x, y):
    fig, ax = plt.subplots(figsize=size, layout="constrained")
    ax.set(title=title, xlabel=x, ylabel=y)
    ax.title.set_fontweight("bold")
    ax.grid(axis="y", color="#e0e6e8", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    return fig, ax


def save(fig, directory, name):
    fig.savefig(directory / f"{name}.pdf", metadata={"CreationDate": None})
    fig.savefig(directory / f"{name}.png", dpi=150)
    plt.close(fig)


def weekly_figure(cul, cfg):
    comparable = cul.brecha.notna().any()
    title = ("Brecha semanal del perímetro histórico de Culiacán"
             if comparable else "Sin comparadores para la brecha semanal de Culiacán")
    fig, ax = axes((7.35, 2.9), title, "Semana respecto al inicio local", "Accidentes por semana")
    if comparable:
        gap = cul.set_index("semana").brecha.reindex(range(cul.semana.min(), cul.semana.max() + 1))
        if -1 in gap.index:
            gap.loc[-1] = np.nan
        ax.plot(gap.index, gap.to_numpy(), color=BLUE, marker="o", linewidth=1.3, markersize=2.8)
    else:
        ax.text(0.5, 0.55, "Brecha sin estimar", ha="center", transform=ax.transAxes)
    ax.axhline(0, color=GRAY, linewidth=0.7)
    ax.axvline(0, color=GRAY, linewidth=1, linestyle="--", label="Inicio de la crisis")
    onset = pd.Timestamp(cfg["onset"])
    split = (pd.Timestamp(cfg["boundary"]) - onset).days // 7
    ax.axvline(split, color=ACCENT, linewidth=1, linestyle=":", label="Cambio territorial")
    if "reporting_from" in cfg:
        start = (pd.Timestamp(cfg["reporting_from"]) - onset).days // 7
        last = (pd.Timestamp(cfg["reporting_through"]) - onset).days // 7
        ax.axvspan(start - 0.5, last + 0.5, color="#f2e5d9", zorder=0, label="Captación en revisión")
    ax.legend(loc="best", frameon=False)
    return fig


def municipal_figure(trajectory):
    fig, ax = axes((8.4, 4.0), "Cómo cambia la trayectoria al emparejar controles",
                   "Día respecto al inicio", "Choques registrados por municipio y día")
    ax.axhline(0, color=GRAY, linewidth=0.7)
    ax.axvline(-0.5, color=GRAY, linewidth=0.8, linestyle=":")
    for sample, color, marker, offset, label in [
        ("mismos_tratados", GRAY, "s", -0.15, "Controles auditados"),
        ("emparejada", BLUE, "o", 0.15, "Controles emparejados"),
    ]:
        rows = trajectory.loc[trajectory.muestra.eq(sample)].sort_values("h")
        if rows.efecto.notna().any():
            pairs = int(rows.tratados.iloc[0])
            ax.errorbar(rows.h + offset, rows.efecto,
                        yerr=[rows.efecto - rows.ic_inf, rows.ic_sup - rows.efecto],
                        fmt=marker, color=color, capsize=1.8, markersize=3, elinewidth=0.8,
                        label=f"{label} · {pairs} tratados")
    ax.scatter([-2], [0], marker="D", facecolors="white", edgecolors=GRAY, s=24,
               label="Base −2")
    ax.set_xticks([-14, -10, -6, -2, 0, 3, 7, 11, 15])
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncols=3,
              frameon=False, title="IC del 95 % agrupado por entidad")
    return fig


def run(config):
    plt.rcParams.update({"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 10.5,
                         "legend.fontsize": 9, "pdf.fonttype": 42})
    out = config["paths"]["outputs"]
    destination = out / "figuras"
    destination.mkdir(parents=True, exist_ok=True)
    e = pd.read_csv(out / "tablas" / "efectos.csv").query("especificacion == 'principal'")
    fig, ax = axes((7.35, 3.0), "Las brechas positivas aparecen antes y después del inicio",
                   "Día respecto al inicio", "Accidentes por municipio y día")
    relevant = config["design"]["pre_important"]
    ax.axhspan(-relevant, relevant, color="#edf2f3", zorder=0)
    ax.axhline(0, color="#353c40", linewidth=0.9)
    ax.axvline(-0.5, color="#777f83", linewidth=0.85, linestyle="--")
    for subset, color, marker in ((e[e.h < 0], GRAY, "s"), (e[e.h >= 0], BLUE, "o")):
        ax.errorbar(subset.h, subset.efecto, yerr=np.vstack([subset.efecto - subset.ic_inf,
                    subset.ic_sup - subset.efecto]), fmt=marker + "-", color=color,
                    capsize=2.0, markersize=3, linewidth=1.1, elinewidth=0.9)
    ax.plot(-config["design"]["anticipation"] - 1, 0, "D", mfc="white", mec=GRAY,
            markersize=5, label="Base fijada")
    ax.set_xticks([-14, -10, -6, -2, 0, 3, 7, 11, 15])
    ax.legend(loc="best", frameon=False)
    save(fig, destination, "dinamica")

    calendar = pd.read_csv(out / "tablas" / "calendario.csv", parse_dates=["indice"])
    fig, ax = axes((7.35, 2.8), "La muestra retiene parte de los municipios expuestos",
                   "Inicio local del episodio", "Pares municipio–episodio")
    ax.vlines(calendar.indice, 0, calendar.tratados_candidatos, color="#a7afb3", linewidth=1)
    ax.scatter(calendar.indice, calendar.tratados_candidatos, facecolors="white", edgecolors=GRAY,
               marker="o", s=24, label="Confirmados")
    used = calendar[calendar.tratados_incluidos.gt(0)]
    ax.scatter(used.indice, used.tratados_incluidos, color=BLUE, marker="D", s=20,
               label="En la muestra principal")
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper left", frameon=False)
    save(fig, destination, "calendario")

    cul = pd.read_csv(out / "modelos" / "culiacan.csv")
    save(weekly_figure(cul, config["culiacan"]), destination, "culiacan")
    trajectory = pd.read_csv(out / "modelos" / "comparaciones_municipales.csv").query("diseno == 'principal'")
    save(municipal_figure(trajectory), destination, "dinamica_municipal")
    print(f"Figuras vectoriales y sus PNG en {destination}")

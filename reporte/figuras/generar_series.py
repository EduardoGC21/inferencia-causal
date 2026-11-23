"""Grafica las series diarias de tratados y controles de la muestra principal."""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def graficar(series, campo, destino):
    dias = series.index
    with plt.rc_context({"pdf.fonttype": 42, "font.size": 9}):
        fig, ax = plt.subplots(figsize=(6.65, 2.25 if campo == "cambio" else 2.15))
        ax.set_axisbelow(True)
        ax.grid(axis="y", color="#e0e0e0", linewidth=0.65)
        if campo == "cambio":
            ax.axhline(0, color="#656565", linewidth=0.8)
            ax.set_xticks(dias)
            ax.set_yticks([-0.6, -0.4, -0.2, 0, 0.2])
            ax.set_ylabel("Cambio en siniestros\npor municipio y día")
        else:
            ax.axvspan(-28.5, -7.5, color="#edf2f7", zorder=0)
            ax.set_xticks([-28, -21, -14, -8, 0, 7, 13])
            ax.set_yticks([1.5, 1.75, 2, 2.25])
            ax.set_ylabel("Siniestros registrados\npor municipio y día")
        ax.axvline(0, color="#656565", linewidth=0.8, linestyle=":")
        ax.plot(dias, series[f"{campo}_tratados"], color="#a04a21", marker="o",
                markersize=3.7, linewidth=1.6, label="Tratados")
        ax.plot(dias, series[f"{campo}_controles"], color="#235ca0", marker="s",
                markersize=3.3, linewidth=1.35, linestyle="--", label="Controles ponderados")
        ax.set_xlim(dias[0] - 0.5, dias[-1] + 0.5)
        ax.set_xlabel("Días respecto al inicio local")
        ax.yaxis.set_major_formatter(FuncFormatter(
            lambda valor, _: f"{valor:g}".replace("-", "−").replace(".", ",")
        ))
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[["left", "bottom"]].set_color("#777777")
        ax.tick_params(length=2.5, color="#777777")
        ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.01), ncol=2, frameon=False)
        fig.tight_layout(pad=0.45)
        fig.savefig(destino, metadata={"CreationDate": None})
        plt.close(fig)


def main():
    carpeta = Path(__file__).resolve().parent
    datos = carpeta.parents[1] / "presentacion/assets/datos"
    series = pd.read_csv(datos / "series-eventos.csv", index_col="h").loc[list(range(-28, 14))]
    cambios = series.loc[-7:13]
    efectos = pd.read_csv(datos / "efectos.csv", dtype={"tramo": str})
    principal = efectos.query(
        "escenario == 'principal' and muestra == 'emparejada' and modelo == 'M0' "
        "and base == 'tres_semanas' and escala == 'niveles' and agrupacion == 'entidad_fecha'"
    ).set_index("tramo")
    coeficientes = principal.loc[cambios.index.astype(str), "efecto"].to_numpy()
    brecha = (cambios.cambio_tratados - cambios.cambio_controles).to_numpy()
    np.testing.assert_allclose(brecha, coeficientes, rtol=0, atol=1e-10, equal_nan=False)

    graficar(series, "observado", carpeta / "conteos-por-grupo.pdf")
    graficar(cambios, "cambio", carpeta / "cambios-por-grupo.pdf")
    print(f"{len(series)} días de conteos observados.")
    print(f"{len(cambios)} contrastes diarios cotejados. "
          f"Diferencia máxima: {np.max(np.abs(brecha - coeficientes)):.3g}.")


if __name__ == "__main__":
    main()

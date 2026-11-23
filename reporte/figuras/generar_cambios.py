"""Grafica los cambios diarios de tratados y controles de la muestra principal."""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def main():
    destino = Path(__file__).with_name("cambios-por-grupo.pdf")
    datos = destino.resolve().parents[2] / "presentacion/assets/datos"
    dias = list(range(-7, 14))
    series = pd.read_csv(datos / "series-eventos.csv", index_col="h").loc[dias]
    efectos = pd.read_csv(datos / "efectos.csv", dtype={"tramo": str})
    principal = efectos.query(
        "escenario == 'principal' and muestra == 'emparejada' and modelo == 'M0' "
        "and base == 'tres_semanas' and escala == 'niveles' and agrupacion == 'entidad_fecha'"
    ).set_index("tramo")
    coeficientes = principal.loc[[str(dia) for dia in dias], "efecto"].to_numpy()
    brecha = (series.cambio_tratados - series.cambio_controles).to_numpy()
    np.testing.assert_allclose(brecha, coeficientes, rtol=0, atol=1e-10, equal_nan=False)

    with plt.rc_context({"pdf.fonttype": 42, "font.size": 9}):
        fig, ax = plt.subplots(figsize=(6.65, 2.25))
        ax.set_axisbelow(True)
        ax.grid(axis="y", color="#e0e0e0", linewidth=0.65)
        ax.axhline(0, color="#656565", linewidth=0.8)
        ax.axvline(0, color="#656565", linewidth=0.8, linestyle=":")
        ax.plot(dias, series.cambio_tratados, color="#a04a21", marker="o",
                markersize=3.7, linewidth=1.6, label="Tratados")
        ax.plot(dias, series.cambio_controles, color="#235ca0", marker="s",
                markersize=3.3, linewidth=1.35, linestyle="--", label="Controles ponderados")
        ax.set_xticks(dias)
        ax.set_xlim(-7.5, 13.5)
        ax.set_xlabel("Días respecto al inicio local")
        ax.set_ylabel("Cambio en siniestros\npor municipio y día")
        ax.set_yticks([-0.6, -0.4, -0.2, 0, 0.2])
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

    print(f"{len(dias)} contrastes diarios cotejados. "
          f"Diferencia máxima: {np.max(np.abs(brecha - coeficientes)):.3g}.")


if __name__ == "__main__":
    main()

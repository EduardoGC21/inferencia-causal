"""Extrae resultados de Ruta B y coteja la lectura descriptiva de la trayectoria."""
import argparse
import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

DECK = Path(__file__).resolve().parents[1]
REPO = DECK.parent
OUT = DECK / "assets/datos"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("modelos", type=Path, help="Salidas Python vigentes de Ruta B")
parser.add_argument("conteos", type=Path, help="Parquet de conteos diarios limpios")
args = parser.parse_args()

effects_path = args.modelos / "causal_efectos.csv"
terms_path = args.modelos / "causal_coeficientes.csv"
sample_path = args.modelos / "causal_muestras.csv"
wald_path = args.modelos / "causal_wald_semanal.csv"
balance_path = args.modelos / "causal_balance.csv"
effects = pd.read_csv(effects_path, dtype={"tramo": str})
sel = effects.loc[effects.muestra.isin(["emparejada", "emparejada_1a1"])]
if set(sel.escala) != {"niveles"} or set(sel.base) != {"tres_semanas"}:
    raise ValueError("La presentación requiere niveles y una sola base de 21 días")

primary = sel.query("escenario == 'principal' and muestra == 'emparejada' and modelo == 'M0' "
                    "and base == 'tres_semanas' and agrupacion == 'entidad_fecha'").set_index("tramo")
initial = primary.loc["d0..1"]
terms = pd.read_csv(terms_path).query("escenario == 'principal' and muestra == 'emparejada'")
np.testing.assert_allclose(initial[["efecto", "ee", "ic_inf", "ic_sup", "p"]].to_numpy(dtype=float),
                           terms.query("modelo == 'M0' and termino == 'tratado'").iloc[0]
                           [["efecto", "ee", "ic_inf", "ic_sup", "p"]].to_numpy(dtype=float))

sample = pd.read_csv(sample_path, usecols=["clave", "indice", "tratado", "peso", "escenario", "muestra"],
                     dtype={"clave": str}, parse_dates=["indice"])
sample = sample.query("escenario == 'principal' and muestra == 'emparejada'")
counts = pd.read_parquet(args.conteos, columns=["clave", "fecha", "dia", "noche", "hora_desconocida"])
published = counts.set_index(["clave", "fecha"])[["dia", "noche", "hora_desconocida"]].sum(axis=1)

# Las masas de ambos grupos son iguales dentro de cada inicio. La diferencia
# entre cambios cancela cualquier ajuste de día de la semana común a esa fecha.
masses = sample.groupby(["indice", "tratado"]).peso.sum().unstack()
np.testing.assert_allclose(masses[0], masses[1], rtol=0, atol=1e-10)
offsets = range(-28, 14)
observed = pd.DataFrame({
    h: published.reindex(pd.MultiIndex.from_arrays([
        sample.clave, sample.indice + pd.Timedelta(days=h)
    ]), fill_value=0).to_numpy()
    for h in offsets
}, index=sample.index)
baseline = observed.loc[:, -28:-8].mean(axis=1)
changes = observed.loc[:, -7:13].sub(baseline, axis=0)
series = pd.DataFrame(index=pd.Index(offsets, name="h"))
for group, role, n in [("tratados", 1, initial.tratados), ("controles", 0, initial.controles)]:
    mask = sample.tratado.eq(role)
    weights = sample.loc[mask, "peso"]
    if len(weights) != n or not np.isclose(weights.sum(), initial.tratados):
        raise ValueError(f"Tamaño o pesos incompatibles: {group}")
    series[f"observado_{group}"] = observed.loc[mask].mul(weights, axis=0).sum() / weights.sum()
    series[f"cambio_{group}"] = changes.loc[mask].mul(weights, axis=0).sum() / weights.sum()

daily = primary.loc[[str(h) for h in range(-7, 14)], "efecto"].to_numpy()
difference = (series.cambio_tratados - series.cambio_controles).dropna().to_numpy()
np.testing.assert_allclose(difference, daily, rtol=0, atol=1e-10)

sel.to_csv(OUT / "efectos.csv", index=False)
terms.to_csv(OUT / terms_path.name, index=False)
for path in (wald_path, balance_path):
    frame = pd.read_csv(path)
    frame.loc[frame.muestra.isin(["emparejada", "emparejada_1a1", "mismos_tratados"])].to_csv(
        OUT / path.name, index=False)
series.to_csv(OUT / "series-eventos.csv", float_format="%.12f")

paths = [effects_path, terms_path, wald_path, balance_path, sample_path, args.conteos]
paths += [REPO / path for path in ["reporte/reporte.md", "reporte/reporte.pdf", "reporte/main.tex",
                                   "reporte/figuras/mapa-municipios.png"]]
manifest = {"alcance": "Resultados en niveles y medias descriptivas de la muestra verificada",
            "dias_base": list(range(-28, -7)), "contrastes_diarios_cotejados": len(daily),
            "diferencia_maxima": float(np.max(np.abs(difference - daily))), "archivos": []}
for path in paths:
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    manifest["archivos"].append({"ruta_desde_repo": Path(os.path.relpath(path, REPO)).as_posix(), "sha256": digest})
(OUT / "procedencia.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Extraídas {len(sel)} filas en niveles. Principal: {initial.efecto:.9f}.")

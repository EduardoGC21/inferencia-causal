"""Extrae resultados ya estimados; no importa ni ejecuta el paquete analítico."""
import hashlib
import json
import os
from pathlib import Path
import numpy as np
import pandas as pd

DECK = Path(__file__).resolve().parents[1]
REPO = DECK.parent
ORIGEN = REPO.parent / "data/outputs/apendice-r-verificado/resultados/modelos"
OUT = DECK / "assets/datos"
OUT.mkdir(parents=True, exist_ok=True)

d = pd.read_csv(ORIGEN / "causal_efectos.csv", dtype={"tramo": str})
# Todas las variantes necesarias para evidencia principal, respaldos y contrastes.
sel = d[d.muestra.isin(["emparejada", "emparejada_1a1"])].copy()
sel.to_csv(OUT / "efectos.csv", index=False)
for name in ["causal_wald_semanal.csv", "causal_balance.csv"]:
    frame = pd.read_csv(ORIGEN / name)
    frame[frame.muestra.isin(["emparejada", "emparejada_1a1", "mismos_tratados"])].to_csv(OUT / name, index=False)
row = sel[(sel.escenario == "principal") & (sel.muestra == "emparejada") &
          (sel.modelo == "M0") & (sel.escala == "log1p") &
          (sel.base == "tres_semanas") & (sel.agrupacion == "entidad_fecha") & (sel.tramo == "d0..1")].iloc[0]
if abs(row.efecto - (-0.1071355)) > 0.000001 or int(row.tratados) != 77:
    raise ValueError("El resultado no coincide con el reporte aprobado")

# Las dos series descriptivas usan los pares y pesos finales, sin volver a
# seleccionar controles ni estimar. La ausencia de filas indica cero publicados.
muestra_path = ORIGEN / "causal_muestras.csv"
conteos_path = ORIGEN.parents[1] / "replica_limpia/datos_limpios_R/conteos_diarios.csv.gz"
muestra = pd.read_csv(muestra_path, usecols=["clave", "indice", "tratado", "peso", "escenario", "muestra"],
                     parse_dates=["indice"]).query("escenario == 'principal' and muestra == 'emparejada'")
conteos = pd.read_csv(conteos_path, usecols=["clave", "fecha", "dia", "noche", "hora_desconocida"],
                     parse_dates=["fecha"])
publicados = conteos.set_index(["clave", "fecha"])[["dia", "noche", "hora_desconocida"]].sum(axis=1)
horizontes = range(-28, 14)
observados = pd.DataFrame({
    h: np.log1p(publicados.reindex(pd.MultiIndex.from_arrays([
        muestra.clave, muestra.indice + pd.Timedelta(days=h)
    ]), fill_value=0).to_numpy())
    for h in horizontes
}, index=muestra.index)
centrados = pd.DataFrame({
    h: observados[h] - observados[[h % 7 - k for k in (28, 21, 14)]].mean(axis=1)
    for h in range(-7, 14)
})
series = pd.DataFrame(index=pd.Index(horizontes, name="h"))
for grupo, indicador, n in [("tratados", 1, 77), ("controles", 0, 3536)]:
    mask = muestra.tratado.eq(indicador)
    pesos = muestra.loc[mask, "peso"]
    if len(pesos) != n or not np.isclose(pesos.sum(), 77):
        raise ValueError(f"Tamaño o pesos incompatibles: {grupo}")
    series[f"observado_{grupo}"] = observados.loc[mask].mul(pesos, axis=0).sum() / pesos.sum()
    series[f"cambio_{grupo}"] = centrados.loc[mask].mul(pesos, axis=0).sum() / pesos.sum()
diarios = sel.query("escenario == 'principal' and muestra == 'emparejada' and modelo == 'M0' "
                    "and escala == 'log1p' and base == 'tres_semanas' and agrupacion == 'entidad_fecha'")
diarios = diarios.set_index("tramo").loc[[str(h) for h in range(-7, 14)], "efecto"].to_numpy()
np.testing.assert_allclose((series.cambio_tratados - series.cambio_controles).dropna(), diarios,
                           rtol=0, atol=1e-10)
series.to_csv(OUT / "series-eventos.csv", float_format="%.12f")

paths = [ORIGEN / x for x in ["causal_efectos.csv", "causal_wald_semanal.csv", "causal_balance.csv"]]
paths += [muestra_path, conteos_path]
paths += [REPO / x for x in ["reporte/reporte.md", "reporte/reporte.pdf", "reporte/main.tex", "reporte/figuras/mapa-municipios.png"]]
manifest = {"alcance": "Extractos de resultados existentes; ninguna estimación nueva", "archivos": []}
for p in paths:
    manifest["archivos"].append({"ruta_desde_repo": Path(os.path.relpath(p, REPO)).as_posix(),
                                  "sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
(OUT / "procedencia.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Extraídas {len(sel)} filas; principal: {row.efecto:.9f}. Las 21 diferencias descriptivas coinciden con M0.")

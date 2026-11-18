import numpy as np
import pandas as pd

from .conteos import HOURS, METRICS, SEVERITY
from .estadistica import estimate, interval
from .seleccion import uniform


WINDOWS = {"1–7": tuple(range(1, 8)), "8–15": tuple(range(8, 16))}
PAIRS = ["clave", "fecha"]


class Counts:
    def __init__(self, path):
        self.counts = pd.read_parquet(path).set_index(PAIRS)

    def average(self, sample, window):
        values = []
        for h in window:
            dates = sample.indice + pd.Timedelta(days=h)
            keys = pd.MultiIndex.from_arrays([sample.clave, dates], names=PAIRS)
            values.append(self.counts.reindex(keys, fill_value=0).to_numpy(dtype=float))
        return np.mean(values, axis=0)


def average(matrix, sample, window):
    return np.mean([matrix.extract(sample, day) for day in window], axis=0)


def by_category(path, samples, matrix, design, output):
    counts = Counts(path)
    baselines = {"-2": (-2,), "media_previa": tuple(range(-design["pre"], -design["anticipation"]))}
    estimates, frequencies = [], []
    for name, sample in samples.items():
        for baseline, days in baselines.items():
            before = counts.average(sample, days)
            total_before = average(matrix, sample, days)
            windows = {"base": tuple(days)} | WINDOWS
            for label, span in windows.items():
                after = counts.average(sample, span)
                total_after = average(matrix, sample, span)
                if (not np.allclose(after[:, :3].sum(axis=1), total_after, rtol=0, atol=1e-12)
                        or not np.allclose(after[:, 3:].sum(axis=1), total_after, rtol=0, atol=1e-12)):
                    raise ValueError("Las clases no concilian en las celdas de comparación")
                delta = after - before
                contrasted = np.column_stack([delta, delta[:, 1] - delta[:, 0]])
                if label != "base":
                    coefficients, covariances, dfs = estimate(sample, ["tratado"], contrasted, design)
                    for j, metric in enumerate(METRICS + ["noche_menos_dia"]):
                        for cluster, covariance in covariances.items():
                            variance = np.nan if covariance is None else covariance[j, j]
                            estimates.append(dict(muestra=name, base=baseline, tramo=label,
                                                  categoria=metric, agrupacion=cluster,
                                                  **interval(coefficients[j, 0], variance, dfs[cluster], design["alpha"])))
                for role in (0, 1):
                    subset = sample.tratado.eq(role).to_numpy()
                    weights = sample.loc[subset, "peso"]
                    for j, metric in enumerate(METRICS):
                        frequencies.append(dict(muestra=name, base=baseline, tramo=label, tratado=role,
                                                categoria=metric, pares=int(subset.sum()), dias=len(span),
                                                choques=int(round(after[subset, j].sum() * len(span))),
                                                media=np.average(after[subset, j], weights=weights) if subset.any() else np.nan))
            # Day zero is also reported by severity. Hourly changes start on day one.
            delta = counts.average(sample, (0,))[:, 3:] - before[:, 3:]
            coefficients, covariances, dfs = estimate(sample, ["tratado"], delta, design)
            for j, metric in enumerate(SEVERITY):
                for cluster, covariance in covariances.items():
                    variance = np.nan if covariance is None else covariance[j, j]
                    estimates.append(dict(muestra=name, base=baseline, tramo="0", categoria=metric,
                                          agrupacion=cluster,
                                          **interval(coefficients[j, 0], variance, dfs[cluster], design["alpha"])))
    pd.DataFrame(estimates).to_csv(output / "franjas_y_gravedad.csv", index=False)
    pd.DataFrame(frequencies).to_csv(output / "frecuencias_franjas_y_gravedad.csv", index=False)


def history(sample, matrix, events, first, design, output):
    cases = events.loc[events.estado.eq("confirmado") & events.clave.ne("") & events.inicio.notna()]
    treated = sample.loc[sample.tratado.eq(1)]
    controls = sample.loc[sample.tratado.eq(0)]
    history_start = pd.Timestamp(f"{first}-01-01")
    classified = []
    for unit in treated.itertuples():
        start = unit.indice - pd.Timedelta(days=365)
        previous = cases.clave.eq(unit.clave) & cases.id_episodio.ne(unit.id_episodio)
        previous &= cases.inicio.ge(start) & cases.inicio.lt(unit.indice)
        status = "documentado" if previous.any() else "sin_antecedente_documentado"
        if start < history_start:
            status = "ventana_incompleta"
        classified.append(status)
    treated = treated.assign(historial=classified)
    treated[["clave", "indice", "estado", "id_episodio", "historial"]].to_csv(
        output / "historial_pares.csv", index=False)
    established = treated.loc[treated.historial.ne("ventana_incompleta")]
    overlap = established.groupby("indice").historial.nunique()
    shared = overlap[overlap.eq(2)].index
    tables = []
    for scope, candidates in (("todos", treated), ("fechas_compartidas", established.loc[established.indice.isin(shared)])):
        for name, group in candidates.groupby("historial", sort=True):
            for label, span in WINDOWS.items():
                blocks = []
                for index, cohort in group.groupby("indice", sort=True):
                    comp = controls.loc[controls.indice.eq(index)]
                    blocks.append(uniform(cohort, comp, sample.iloc[:0]))
                core = pd.concat(blocks, ignore_index=True)
                baseline = range(-design["pre"], -design["anticipation"])
                delta = average(matrix, core, span) - average(matrix, core, baseline)
                roles = core.tratado.eq(1)
                effect = (np.average(delta[roles], weights=core.loc[roles, "peso"])
                          - np.average(delta[~roles], weights=core.loc[~roles, "peso"]))
                tables.append(dict(ambito=scope, historial=name, tramo=label, tratados=len(group),
                                   fechas=group.indice.nunique(), estados=group.estado.nunique(),
                                   fechas_compartidas=len(shared), contraste_descriptivo=effect))
    pd.DataFrame(tables).to_csv(output / "historial.csv", index=False)

import numpy as np
import pandas as pd

from .conteos import CROSS, HOURS, METRICS, SEVERITY
from .estadistica import estimate, interval
from .seleccion import uniform


WINDOWS = {"1–7": tuple(range(1, 8)), "8–15": tuple(range(8, 16))}
PAIRS = ["clave", "fecha"]


class Counts:
    def __init__(self, path):
        self.counts = pd.read_parquet(path, columns=PAIRS + METRICS + list(CROSS.values())).set_index(PAIRS)

    def average(self, sample, window):
        values = []
        for h in window:
            dates = sample.indice + pd.Timedelta(days=h)
            keys = pd.MultiIndex.from_arrays([sample.clave, dates], names=PAIRS)
            values.append(self.counts.reindex(keys, fill_value=0).to_numpy(dtype=float))
        return np.mean(values, axis=0)


def average(matrix, sample, window):
    return np.mean([matrix.extract(sample, day) for day in window], axis=0)


def effect_rows(sample, outcomes, design):
    coefficients, covariances, dfs = estimate(sample, ["tratado"], outcomes, design)
    for j in range(outcomes.shape[1]):
        for cluster, covariance in covariances.items():
            variance = np.nan if covariance is None else covariance[j, j]
            yield j, dict(agrupacion=cluster, **interval(coefficients[j, 0], variance, dfs[cluster], design["alpha"]))


def by_category(path, samples, matrix, design, output):
    counts = Counts(path)
    baselines = {"-2": (-2,), "media_previa": tuple(range(-design["pre"], -design["anticipation"]))}
    estimates, frequencies = [], []
    crossed_estimates, crossed_frequencies = [], []
    intersections = list(CROSS)
    comparisons = intersections + [("noche_menos_dia", severity) for severity in SEVERITY]
    n_hours, n_marginal = len(HOURS), len(METRICS)
    for name, sample in samples.items():
        for baseline, days in baselines.items():
            before = counts.average(sample, days)
            windows = {"base": tuple(days)} | WINDOWS
            for label, span in windows.items():
                after = counts.average(sample, span)
                total_after = average(matrix, sample, span)
                if (not np.allclose(after[:, :n_hours].sum(axis=1), total_after, rtol=0, atol=1e-12)
                        or not np.allclose(after[:, n_hours:n_marginal].sum(axis=1), total_after, rtol=0, atol=1e-12)):
                    raise ValueError("Las clases no concilian en las celdas de comparación")
                delta = after - before
                labels = dict(muestra=name, base=baseline, tramo=label)
                if label != "base":
                    contrasted = np.column_stack([delta[:, :n_marginal], delta[:, 1] - delta[:, 0]])
                    for j, stats in effect_rows(sample, contrasted, design):
                        metric = (METRICS + ["noche_menos_dia"])[j]
                        estimates.append(dict(**labels, categoria=metric, **stats))

                    cross_delta = delta[:, n_marginal:]
                    day, night, _ = np.split(cross_delta, n_hours, axis=1)
                    present = (after[:, n_marginal:] + before[:, n_marginal:]).any(axis=0)
                    day_present, night_present, _ = np.split(present, n_hours)
                    present = np.r_[present, day_present | night_present]
                    for j, stats in effect_rows(sample, np.column_stack([cross_delta, night - day]), design):
                        franja, gravedad = comparisons[j]
                        status = "estimado" if np.isfinite(stats["ic_inf"]) else "ic_no_disponible"
                        if not present[j]:
                            status = "sin_registros"
                            stats.update(ee=np.nan, ic_inf=np.nan, ic_sup=np.nan, p=np.nan)
                        crossed_estimates.append(dict(**labels, franja=franja, gravedad=gravedad, **stats, estado=status))
                for role in (0, 1):
                    subset = sample.tratado.eq(role).to_numpy()
                    weights = sample.loc[subset, "peso"]
                    for j, values in enumerate(after[subset].T):
                        frequency = dict(pares=int(subset.sum()), dias=len(span),
                                         choques=int(round(values.sum() * len(span))),
                                         media=np.average(values, weights=weights) if subset.any() else np.nan)
                        if j < n_marginal:
                            frequencies.append(dict(**labels, tratado=role, categoria=METRICS[j], **frequency))
                        else:
                            franja, gravedad = intersections[j - n_marginal]
                            crossed_frequencies.append(dict(**labels, tratado=role, franja=franja, gravedad=gravedad,
                                                            **frequency))
            # Day zero is also reported by severity. Hourly changes start on day one.
            delta = counts.average(sample, (0,))[:, n_hours:n_marginal] - before[:, n_hours:n_marginal]
            for j, stats in effect_rows(sample, delta, design):
                estimates.append(dict(muestra=name, base=baseline, tramo="0", categoria=SEVERITY[j], **stats))
    pd.DataFrame(estimates).to_csv(output / "franjas_y_gravedad.csv", index=False)
    pd.DataFrame(frequencies).to_csv(output / "frecuencias_franjas_y_gravedad.csv", index=False)
    pd.DataFrame(crossed_estimates).to_csv(output / "franjas_x_gravedad.csv", index=False)
    pd.DataFrame(crossed_frequencies).to_csv(output / "frecuencias_franjas_x_gravedad.csv", index=False)


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

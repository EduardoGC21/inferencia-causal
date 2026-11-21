from copy import copy

import numpy as np
import pandas as pd

from . import modelos, municipios
from .diagnosticos import WINDOWS, average
from .estadistica import estimate, interval
from .seleccion import match, one_to_one


MATCHES = ("emparejada", "emparejada_1a1")


def monthly_flags(matrix, reported, invalid):
    periods = matrix.dates[[0, -1]].to_period("M")
    calendar = pd.period_range(periods[0] - 3, periods[1], freq="M")
    seen = (reported.assign(mes=reported.fecha.dt.to_period("M"))
            .groupby(["clave", "mes"]).size().unstack(fill_value=0)
            .reindex(index=matrix.keys, columns=calendar, fill_value=0).gt(0))
    known = invalid.loc[invalid.mes.between(1, 12).fillna(False)]
    unknown = invalid.loc[~invalid.mes.between(1, 12).fillna(False)]
    bad = pd.DataFrame(False, index=matrix.keys, columns=calendar)
    for row in known[["clave", "anio", "mes"]].drop_duplicates().itertuples():
        month = pd.Period(year=row.anio, month=int(row.mes), freq="M")
        if month in calendar and row.clave in matrix.keys:
            bad.loc[row.clave, month] = True
    for row in unknown[["clave", "anio"]].drop_duplicates().itertuples():
        if row.clave in matrix.keys:
            bad.loc[row.clave, calendar.year == row.anio] = True
    return seen, bad


def select(matrix, events, design, flags=None, end_at_start=False):
    rules = design | {"horizon": 0, "anticipation": 0} if end_at_start else design
    if flags is None:
        sample, _ = modelos.legacy_comparison(matrix, events, rules, "principal")
        return sample, matrix

    seen, bad = flags
    published = copy(matrix)
    published.values = np.nan_to_num(matrix.values, nan=0.0)
    focal = events.estado.eq("confirmado") & events.clase_final.eq("extensa")
    parts = []
    for index in sorted(events.loc[focal, "inicio"].dropna().unique()):
        index = pd.Timestamp(index)
        start = (index - pd.Timedelta(days=rules["pre"] + rules["scale_days"])).to_period("M")
        end = (index + pd.Timedelta(days=rules["horizon"])).to_period("M")
        earlier = seen.reindex(columns=pd.period_range(start - 3, start - 1), fill_value=False)
        clean = earlier.all(axis=1) & ~bad.loc[:, start:end].any(axis=1)
        view = copy(published)
        view.coverage = np.broadcast_to(clean.to_numpy()[:, None], matrix.coverage.shape)
        # Only the focal designation changes. Other events stay in the contamination inventory.
        cohort = events.assign(estado=events.estado.mask(focal & events.inicio.ne(index), "pendiente"))
        part, _ = modelos.legacy_comparison(view, cohort, rules, "principal")
        if not part.empty:
            parts.append(part)
    sample = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=modelos.SAMPLE)
    return sample, published


def contrasts(sample, matrix, design, end_at_start):
    windows = {"0": (0,)} if end_at_start else {"0": (0,)} | WINDOWS
    baselines = {"-2": (-2,), "media_previa": tuple(range(-design["pre"], -design["anticipation"]))}
    for base, days in baselines.items():
        baseline = average(matrix, sample, days)
        deltas = np.column_stack([average(matrix, sample, days) - baseline for days in windows.values()])
        coefficients, covariances, dfs = estimate(sample, ["tratado"], deltas, design)
        for i, span in enumerate(windows):
            for cluster, vcov in covariances.items():
                variance = np.nan if vcov is None else vcov[i, i]
                yield dict(base=base, tramo=span, agrupacion=cluster,
                           **interval(coefficients[i, 0], variance, dfs[cluster], design["alpha"]))


def run(config, matrix, events, municipal, reference, output):
    paths, design = config["paths"], config["design"]
    tables, changes, state_aggregates = municipal
    reported = pd.read_parquet(paths["interim"] / "atus.parquet", columns=["clave", "fecha"])
    invalid = pd.read_parquet(paths["interim"] / "fecha_invalida.parquet", columns=["clave", "anio", "mes"])
    flags = monthly_flags(matrix, reported, invalid)
    alerts = pd.read_csv(config["root"] / "config" / "cotejo_controles.csv", dtype={"clave": str},
                         parse_dates=["inicio", "fin"])
    if (not alerts.clave.isin(matrix.keys).all() or not alerts.fin.ge(alerts.inicio).all()
            or not alerts.id_episodio.is_unique or alerts.id_episodio.isin(events.id_episodio).any()):
        raise ValueError("Las señales del cotejo requieren clave, fechas e identificador propios")
    reviewed = pd.concat([events, alerts.assign(cve_ent=alerts.clave.str[:2], estado="pendiente",
                                               clase_final="incierta")], ignore_index=True)
    scenarios = [
        ("cobertura_predicha", events, flags, False),
        ("hasta_inicio", events, None, True),
        ("hasta_inicio_cobertura_predicha", events, flags, True),
        ("senales_cotejadas", reviewed, None, False),
    ]
    results, composition, weights = [], [], []
    for name, catalog, coverage, until_start in [("referencia", events, None, False)] + scenarios:
        if name == "referencia":
            groups, outcome = reference, matrix
        else:
            selected, outcome = select(matrix, catalog, design, coverage, until_start)
            geographic_window = design | {"horizon": 0, "anticipation": 0} if until_start else design
            candidates = municipios.attach(selected, tables, changes, geographic_window, state_aggregates)
            matched, _, edges = match(candidates, design)
            paired, _ = one_to_one(matched, edges)
            groups = dict(zip(MATCHES, (matched, paired)))
        for method in MATCHES:
            sample = groups[method]
            totals = modelos.summarize(sample)
            results.extend(dict(escenario=name, muestra=method, **totals, **result)
                           for result in contrasts(sample, outcome, design, until_start))
            weights.append(sample[modelos.SAMPLE].assign(escenario=name, muestra=method))
            for role in (0, 1):
                keys = ["indice", "clave"]
                old = pd.MultiIndex.from_frame(reference[method].loc[lambda x: x.tratado.eq(role), keys])
                new = pd.MultiIndex.from_frame(sample.loc[sample.tratado.eq(role), keys])
                composition.append(dict(escenario=name, muestra=method, tratado=role,
                                        conservados=len(old.intersection(new)), salen=len(old.difference(new)),
                                        entran=len(new.difference(old))))
    pd.DataFrame(results).to_csv(output / "sensibilidades_seleccion.csv", index=False)
    pd.DataFrame(composition).to_csv(output / "composicion_sensibilidades.csv", index=False)
    pd.concat(weights, ignore_index=True).to_csv(output / "muestras_sensibilidades.csv", index=False)

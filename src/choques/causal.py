"""Ruta B aprobada después de observar T05. Las salidas causal_* son el diseño final.

Las salidas sin ese prefijo conservan la referencia auditada de 73 tratados.
El resultado es el número de registros publicados con fecha válida en el release,
incluidos ceros de registros en municipios con cobertura predicha previamente.
"""
from copy import copy

import numpy as np
import pandas as pd

from . import modelos, municipios
from .analisis import mde
from .comparaciones import coverage
from .estadistica import estimate, interval, wald
from .seleccion import COVARIATES, balance, match, one_to_one, same_treated


SPANS = {"d0": (0,), "d1": (1,), "d0..1": (0, 1), "d2..6": tuple(range(2, 7)),
         "wk0": tuple(range(7)), "wk+1": tuple(range(7, 14)), "wk-1": tuple(range(-7, 0))}
HORIZONS = {**{str(h): (h,) for h in range(-7, 14)}, **SPANS}
MODEL_COLUMNS = ["tratado", "log_poblacion", "empleo_mil", "autos_mil"]
AUDIT_DATES = pd.to_datetime(["2019-12-31", "2023-01-05", "2023-04-09", "2024-01-07", "2025-04-23"])


def baseline_offsets(h):
    """r=t+(h mod 7); tres fechas del mismo día dentro de [-28,-8]."""
    return tuple(h % 7 - k for k in (28, 21, 14))


def transform(values, scale):
    values = np.asarray(values, dtype=float)
    if not np.isfinite(values).all() or (values < 0).any():
        raise ValueError("El resultado requiere conteos finitos y no negativos")
    if scale not in ("niveles", "log1p"):
        raise ValueError("Escala desconocida")
    return np.log1p(values) if scale == "log1p" else values


def contrasts(matrix, sample, scale, base="tres_semanas", spans=HORIZONS, *, panel=False):
    days = set(h for span in spans.values() for h in span)
    references = {h: baseline_offsets(h) if base == "tres_semanas" else
                  tuple(range(-7, 0)) if base == "wk-1" else (-2,) for h in days}
    needed = days | {b for refs in references.values() for b in refs}
    values = {h: transform(matrix.extract(sample, h), scale) for h in sorted(needed)}
    baselines = {h: np.mean([values[b] for b in references[h]], axis=0) for h in days}

    def aggregate(series):
        return np.column_stack([np.mean([series[h] for h in span], axis=0) for span in spans.values()])

    if panel:
        return aggregate(baselines), aggregate(values)
    return aggregate({h: values[h] - baselines[h] for h in days})


def published_matrix(matrix, counts):
    """Construye el conteo de filas publicadas; no rellena el panel de continuidad."""
    result = copy(matrix)
    result.values = np.zeros_like(matrix.values)
    i, j = matrix.keys.get_indexer(counts.clave), matrix.dates.get_indexer(counts.fecha)
    if (i < 0).any() or (j < 0).any() or counts.duplicated(["clave", "fecha"]).any():
        raise ValueError("Conteos fuera del calendario o duplicados")
    result.values[i, j] = counts[["dia", "noche", "hora_desconocida"]].sum(axis=1).to_numpy()
    return result


def predicted_coverage(keys, reported, invalid, index):
    """Sólo tres meses completos anteriores al mes del inicio, hasta t-1."""
    previous = pd.period_range(index.to_period("M") - 3, index.to_period("M") - 1, freq="M")
    months = reported.fecha.dt.to_period("M")
    seen = (reported.loc[months.isin(previous)].assign(mes=months.loc[months.isin(previous)])
            .groupby(["clave", "mes"]).size().unstack(fill_value=0)
            .reindex(index=keys, columns=previous, fill_value=0).gt(0).all(axis=1))
    bad = invalid.loc[invalid.mes.between(1, 12).fillna(False)].copy()
    bad_month = pd.to_datetime(dict(year=bad.anio, month=bad.mes, day=1)).dt.to_period("M")
    blocked = set(bad.loc[bad_month.isin(previous), "clave"])
    # Un mes desconocido del año corriente no puede fecharse antes de t: no se
    # usa para elegir la muestra. Su incertidumbre se publica por separado.
    unknown = invalid.loc[~invalid.mes.between(1, 12).fillna(False) & invalid.anio.lt(index.year)]
    blocked |= set(unknown.loc[unknown.anio.isin(previous.year), "clave"])
    return seen.to_numpy() & ~keys.isin(blocked)


def select_pre(matrix, published, events, reported, invalid, changes, design,
               placebo=False, persistence=False):
    active = modelos.active_events(events)
    focal = active.loc[active.estado.eq("confirmado") & active.clase_final.eq("extensa")].copy()
    focal["indice"] = focal.inicio - pd.Timedelta(days=28 if placebo else 0)
    parts, audits = [], []
    for index, cohort in focal.groupby("indice", sort=True):
        if cohort.clave.duplicated().any():
            raise ValueError("Focales repetidos en municipio y fecha")
        first, cutoff = index - pd.Timedelta(days=49), index - pd.Timedelta(days=1)
        right = index + pd.Timedelta(days=14) if persistence else cutoff
        local = matrix.keys.isin(cohort.clave)
        known = active.loc[active.inicio.le(right) & active.hasta.ge(first)]
        named = set(known.loc[known.clave.ne(""), "clave"])
        broad = set(known.loc[known.clave.eq(""), "cve_ent"])
        blocked = matrix.keys.isin(named) | matrix.states.isin(broad)
        if persistence:
            # La excepción del episodio focal sólo vale para su propio tratado
            # desde t. No habilita un antecedente ni un donante expuesto después.
            blocked = np.asarray(blocked).copy()
            for row in cohort.itertuples():
                conflicts = known.loc[known.id_episodio.ne(row.id_episodio) | known.inicio.le(cutoff)]
                hit = conflicts.clave.eq(row.clave) | (conflicts.clave.eq("") & conflicts.cve_ent.eq(row.cve_ent))
                location = matrix.keys.get_indexer([row.clave])[0]
                if location >= 0:
                    blocked[location] = bool(hit.any())
        geography = matrix.states.isin(set(cohort.cve_ent))
        prediction = predicted_coverage(matrix.keys, reported, invalid, index)
        keys = pd.Series(matrix.keys)
        territorial = municipios.territories(keys, index - pd.Timedelta(days=28), changes, atus=True).eq(
            municipios.territories(keys, right, changes, atus=True)).to_numpy()
        complete = np.ones(len(keys), dtype=bool)
        if persistence:
            span = matrix.dates.to_series().between(index - pd.Timedelta(days=28), index + pd.Timedelta(days=13)).to_numpy()
            complete = (matrix.coverage[:, span].all(axis=1) & np.isfinite(matrix.values[:, span]).all(axis=1)
                        if span.sum() == 42 else np.zeros(len(keys), dtype=bool))
        calendar = first >= matrix.dates[0] and index + pd.Timedelta(days=13) <= matrix.dates[-1]
        eligible = prediction & ~blocked & territorial & complete & (local | ~geography) & calendar
        scale_days = (published.dates >= index - pd.Timedelta(days=28)) & (published.dates <= index - pd.Timedelta(days=15))
        levels = published.values[:, scale_days].mean(axis=1)
        audit = pd.DataFrame(dict(clave=matrix.keys, indice=index, tratado=local.astype(int),
                                  cobertura_predicha=prediction, exposicion_en_ventana=blocked,
                                  territorio_compatible=territorial, cobertura_completa=complete,
                                  estado_focal=geography, elegible=eligible))
        audits.append(audit)
        if not (eligible & local).any():
            continue
        chosen = matrix.keys[eligible]
        lookup = cohort.set_index("clave").id_episodio
        roles = local[eligible].astype(int)
        parts.append(pd.DataFrame(dict(clave=chosen, estado=matrix.states[eligible], indice=index,
                                       tratado=roles, id_episodio=lookup.reindex(chosen).fillna("").to_numpy(),
                                       peso=np.ones(len(chosen)), pre_nivel=levels[eligible])))
    return (pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=modelos.SAMPLE),
            pd.concat(audits, ignore_index=True))


def jackknife(frame, columns, outcomes, design, *, baseline=None, beta=None):
    """CRV3 con pesos fijos y efectos fijos reestimados en cada réplica."""
    if beta is None:
        beta, _, _ = estimate(frame, columns, outcomes, design, baseline=baseline, inference=False)
    states = sorted(frame.estado.unique())
    replicas = []
    for state in states:
        keep = frame.estado.ne(state).to_numpy()
        b, _, _ = estimate(frame.loc[keep].reset_index(drop=True), columns, outcomes[keep], design,
                           baseline=None if baseline is None else baseline[keep], inference=False)
        replicas.append(b)
    replicas = np.asarray(replicas)
    delta = (replicas - beta).reshape(len(states), -1)
    variance = (len(states) - 1) / len(states) * delta.T @ delta if len(states) > 1 else np.full((beta.size, beta.size), np.nan)
    return variance, states, replicas


def results(matrix, sample, design, scale, base, models=(0,), with_jackknife=False):
    sample = sample.reset_index(drop=True)
    y = contrasts(matrix, sample, scale, base)
    totals = modelos.summarize(sample)
    treated = sample.loc[sample.tratado.eq(1)]
    pre = np.concatenate([matrix.extract(treated, h) for h in range(-28, -7)])
    sigma = transform(pre, scale).std(ddof=1) if len(pre) > 1 else np.nan
    mean = pre.mean() if len(pre) else np.nan
    rows, omitted = [], []
    for model in models:
        columns = MODEL_COLUMNS[:model + 1]
        frame = sample.assign(log_poblacion=np.log(sample.poblacion)) if model else sample
        b, covariances, dfs = estimate(frame, columns, y, design)
        if with_jackknife:
            v, states, replicates = jackknife(frame, columns, y, design, beta=b)
            covariances["CRV3"], dfs["CRV3"] = v, len(states) - 1
            for g, state in enumerate(states):
                for j, span in enumerate(HORIZONS):
                    omitted.append(dict(estado_omitido=state, modelo=f"M{model}", tramo=span,
                                        efecto=replicates[g, j, 0], identificada=bool(np.isfinite(replicates[g, j, 0]))))
        for cluster, v in covariances.items():
            for j, span in enumerate(HORIZONS):
                variance = np.nan if v is None else v[j * len(columns), j * len(columns)]
                stats = interval(b[j, 0], variance, dfs[cluster], design["alpha"])
                rows.append(dict(modelo=f"M{model}", tramo=span, agrupacion=cluster, base=base, escala=scale,
                                 **totals, **stats, sigma_pre=sigma, media_pre=mean,
                                 estado_inferencia="sin_identificar" if not np.isfinite(b[j, 0]) else
                                 "sin_covarianza" if v is None else "varianza_negativa" if variance < 0 else
                                 "varianza_cero" if variance == 0 else "calculada",
                                 efecto_sigma=stats["efecto"] / sigma if sigma > 0 else np.nan,
                                 mde=mde(dfs[cluster], stats["ee"], design["alpha"], design["power"])))
    return rows, omitted


def weekly_tests(matrix, sample, design, scale, *, panel=False):
    # wk-2 se omite: las cuatro semanas normalizadas por su promedio son redundantes.
    ref = np.mean([transform(matrix.extract(sample, h), scale) for h in range(-14, -7)], axis=0)
    spans = {"wk-4": range(-28, -21), "wk-3": range(-21, -14), "wk-1": range(-7, 0)}
    y = np.column_stack([np.mean([transform(matrix.extract(sample, h), scale) for h in days], axis=0)
                         for days in spans.values()])
    baseline = np.broadcast_to(ref[:, None], y.shape)
    b, covariances, dfs = (estimate(sample, ["tratado"], y, design, baseline=baseline) if panel else
                           estimate(sample, ["tratado"], y - baseline, design))
    rows = []
    for cluster, v in covariances.items():
        eig = np.linalg.eigvalsh(v) if v is not None and np.isfinite(v).all() else [np.nan]
        rows.append(dict(escala=scale, agrupacion=cluster, referencia="wk-2 [-14,-8]", restricciones="wk-4;wk-3;wk-1",
                         rango=np.linalg.matrix_rank(v) if v is not None else 0,
                         condicion=np.linalg.cond(v) if v is not None else np.nan,
                         autovalor_min=min(eig), **wald(b[:, 0], v, dfs[cluster])))
        for j, label in enumerate(spans):
            rows.append(dict(escala=scale, agrupacion=cluster, referencia="wk-2 [-14,-8]", restricciones=label,
                             **interval(b[j, 0], np.nan if v is None else v[j, j], dfs[cluster], design["alpha"])))
    return rows


def cross_outcomes(crossed, frame, *, panel=False):
    """Días 0–1 por franja y gravedad, y contraste noche menos día."""
    def at(h):
        keys = pd.MultiIndex.from_arrays([frame.clave, frame.indice + pd.Timedelta(days=h)])
        return crossed.reindex(keys, fill_value=0).to_numpy(dtype=float)

    def with_night_gap(values):
        day, night, _ = np.split(values, 3, axis=1)
        return np.column_stack([values, night - day])

    observed = [at(h) for h in (0, 1)]
    baseline = [np.mean([at(b) for b in baseline_offsets(h)], axis=0) for h in (0, 1)]
    activity = np.sum(observed + baseline, axis=0).any(axis=0)
    present = np.r_[activity, activity[:3] | activity[3:6]]
    if panel:
        return with_night_gap(np.mean(baseline, axis=0)), with_night_gap(np.mean(observed, axis=0)), present
    return with_night_gap(np.mean(np.subtract(observed, baseline), axis=0)), present


def calendar_flags(root, dates):
    """Reglas federales LFT y calendario nacional SEP básico; domingos ordinarios no."""
    calendar = pd.read_csv(root / "config" / "calendario_escolar.csv", parse_dates=["inicio", "fin"])
    answer = []
    for date in sorted(set(pd.to_datetime(dates))):
        year = date.year
        mondays = lambda month: pd.date_range(f"{year}-{month:02}-01", periods=31, freq="D").to_series().loc[
            lambda x: (x.dt.month == month) & (x.dt.day_of_week == 0)].tolist()
        labor = date in pd.to_datetime([f"{year}-01-01", f"{year}-05-01", f"{year}-09-16", f"{year}-12-25"])
        labor |= date in [mondays(2)[0], mondays(3)[2], mondays(11)[2], pd.Timestamp("2024-10-01")]
        hits = calendar.loc[calendar.inicio.le(date) & calendar.fin.ge(date)]
        answer.append(dict(fecha=date, laboral=bool(labor), escolar=not hits.empty,
                           tipo_escolar=";".join(sorted(set(hits.tipo))),
                           fuentes=";".join(sorted(set(hits.fuente)))))
    return pd.DataFrame(answer)


def run(config):
    paths, design = config["paths"], config["design"]
    out = paths["outputs"] / "modelos"
    matrix, events = modelos.load(paths)
    counts = pd.read_parquet(paths["processed"] / "conteos_diarios.parquet")
    published = published_matrix(matrix, counts)
    reported = pd.read_parquet(paths["interim"] / "atus.parquet", columns=["clave", "fecha"])
    invalid = pd.read_parquet(paths["interim"] / "fecha_invalida.parquet", columns=["clave", "anio", "mes"])
    tables_m, changes = municipios.load(paths)
    state_rates = municipios.rates(tables_m)
    rules = design | {"individual_caliber": True}
    samples, links_all, losses, audits, coverage_all, balances, supports = {}, [], [], [], [], [], []
    for scenario, placebo, persistence in [("principal", False, False), ("persistencia", False, True), ("placebo", True, False)]:
        pool, audit = select_pre(matrix, published, events, reported, invalid, changes, rules, placebo, persistence)
        audit["escenario"] = scenario
        audits.append(audit)
        attached = municipios.attach(pool, tables_m, changes, design | {"horizon": 14 if persistence else -1,
                                    "anticipation": 0, "pre_only": not persistence}, state_rates)
        coverage_all.append(coverage(attached.assign(especificacion=scenario)))
        many, loss, edges = match(attached, rules)
        one, nearest = one_to_one(many, edges)
        level, _, level_edges = match(attached, rules, covariates=[])
        common, _, common_edges = match(attached.dropna(subset=COVARIATES), rules, covariates=[])
        _, complete_reference = same_treated(attached, many)
        groups = {"sin_covariables": level, "mismos_tratados": complete_reference,
                  "comun_m0_m3": common, "emparejada": many, "emparejada_1a1": one}
        samples[scenario] = groups
        losses.append(loss.assign(escenario=scenario))
        for method, edges_m in [("sin_covariables", level_edges), ("comun_m0_m3", common_edges),
                                ("emparejada", edges), ("emparejada_1a1", nearest)]:
            links_all.append(edges_m.assign(escenario=scenario, muestra=method))
        for method, frame in groups.items():
            supports.append(dict(escenario=scenario, muestra=method, **modelos.summarize(frame)))
        balances.append(balance({"auditada": level, **groups}, COVARIATES + ["pre_nivel"]).assign(escenario=scenario))
    # Calendario predeterminado, calculado antes de consultar estimaciones.
    indices = sorted(set(events.inicio.dropna()))
    calendar = calendar_flags(config["root"], [d + pd.Timedelta(days=h) for d in indices for h in range(-56, 15)])
    calendar.to_csv(out / "causal_calendario.csv", index=False)
    cal = calendar.set_index("fecha")
    treated_pairs = samples["principal"]["emparejada"].loc[lambda x: x.tratado.eq(1), ["clave", "indice"]]
    exclusions = []
    for row in treated_pairs.itertuples():
        flags = cal.loc[[row.indice, row.indice + pd.Timedelta(days=1)]]
        exclusions.append(dict(clave=row.clave, indice=row.indice, audit_cinco=row.indice in AUDIT_DATES,
                               laboral=bool(flags.laboral.any()), escolar=bool(flags.escolar.any())))
    pd.DataFrame(exclusions).to_csv(out / "causal_exclusiones_calendario.csv", index=False)
    # Exclusiones por pareja; se recalculan pesos en cada fecha usando vínculos.
    primary_pool, _ = select_pre(matrix, published, events, reported, invalid, changes, rules)
    base_pool = municipios.attach(primary_pool, tables_m, changes,
                                 design | {"horizon": -1, "anticipation": 0, "pre_only": True}, state_rates)
    alert = pd.read_csv(config["root"] / "config/cotejo_controles.csv", dtype={"clave": str}, parse_dates=["inicio", "fin"])
    for scenario in ("sin_cinco", "sin_laborales", "sin_laborales_escolares", "sin_pendientes", "sin_todos_pendientes", "sin_senales"):
        pool = base_pool.copy()
        if scenario.startswith("sin_laborales") or scenario == "sin_cinco":
            dates = []
            for date in pool.indice.unique():
                flags = cal.loc[[date, date + pd.Timedelta(days=1)]]
                drop = date in AUDIT_DATES if scenario == "sin_cinco" else bool(flags.laboral.any())
                if scenario == "sin_laborales_escolares":
                    drop |= bool(flags.escolar.any())
                if drop:
                    dates.append(date)
            pool = pool.loc[~pool.indice.isin(dates)]
        elif scenario in ("sin_pendientes", "sin_todos_pendientes"):
            pending = ((pool.clave.eq("16025") & pool.indice.eq("2021-07-14")) |
                       (pool.clave.eq("16017") & pool.indice.eq("2025-04-23")))
            if scenario == "sin_todos_pendientes":
                pending |= ((pool.clave.eq("16037") & pool.indice.eq("2025-04-23")) |
                            (pool.clave.eq("28035") & pool.indice.eq("2023-04-30")))
            pool = pool.loc[~(pending & pool.tratado.eq(1))]
        else:
            blocked = np.zeros(len(pool), bool)
            for row in alert.itertuples():
                # Sensibilidad ex post explícita; Coatzacoalcos ocurrió después de t.
                blocked |= (pool.clave.eq(row.clave) & pool.tratado.eq(0) &
                            (pool.indice - pd.Timedelta(days=49)).le(row.fin) &
                            (pool.indice + pd.Timedelta(days=14)).ge(row.inicio)).to_numpy()
            pool = pool.loc[~blocked]
        many, loss, edges = match(pool, rules)
        one, nearest = one_to_one(many, edges)
        samples[scenario] = {"emparejada": many, "emparejada_1a1": one}
        losses.append(loss.assign(escenario=scenario))
        for method, frame, edge in [("emparejada", many, edges), ("emparejada_1a1", one, nearest)]:
            supports.append(dict(escenario=scenario, muestra=method, **modelos.summarize(frame)))
            links_all.append(edge.assign(escenario=scenario, muestra=method))
    rows, loo, tests, sample_records = [], [], [], []
    for scenario, groups in samples.items():
        for method, frame in groups.items():
            sample_records.append(frame.assign(escenario=scenario, muestra=method))
            if frame.empty:
                continue
            for scale in ("log1p", "niveles"):
                bases = ("tres_semanas", "-2", "wk-1") if scenario == "principal" else ("tres_semanas",)
                for base in bases:
                    models = range(4) if method in ("emparejada", "emparejada_1a1", "mismos_tratados", "comun_m0_m3") and base == "tres_semanas" and scenario == "principal" else (0,)
                    fits, omissions = results(published, frame, design, scale, base, models,
                                              with_jackknife=scenario == "principal" and base == "tres_semanas")
                    rows.extend(dict(r, escenario=scenario, muestra=method) for r in fits)
                    loo.extend(dict(r, escala=scale, muestra=method) for r in omissions)
                if scenario in ("principal", "persistencia", "placebo"):
                    tests.extend(dict(r, escenario=scenario, muestra=method) for r in weekly_tests(published, frame, design, scale))
    outputs = {"efectos": pd.DataFrame(rows), "omision_estado": pd.DataFrame(loo),
               "wald_semanal": pd.DataFrame(tests), "soporte": pd.DataFrame(supports),
               "muestras": pd.concat(sample_records, ignore_index=True), "vinculos": pd.concat(links_all, ignore_index=True),
               "descartes": pd.concat(losses, ignore_index=True), "elegibilidad": pd.concat(audits, ignore_index=True),
               "uniones": pd.concat(coverage_all, ignore_index=True), "balance": pd.concat(balances, ignore_index=True)}
    for name, data in outputs.items():
        data.to_csv(out / f"causal_{name}.csv", index=False)
    from .conteos import CROSS
    crossed = counts.set_index(["clave", "fecha"])[list(CROSS.values())]
    cross_rows = []
    for method in ("emparejada", "emparejada_1a1"):
        frame = samples["principal"][method]
        outcomes, present = cross_outcomes(crossed, frame)
        np.testing.assert_allclose(outcomes[:, :len(CROSS)].sum(axis=1),
                                   contrasts(published, frame, "niveles", spans={"d0..1": (0, 1)})[:, 0], atol=1e-12)
        labels = list(CROSS) + [("noche_menos_dia", g) for g in ("fatal", "heridos", "danos")]
        b, cov, dfs = estimate(frame, ["tratado"], outcomes, design)
        for j, (hour, severity) in enumerate(labels):
            for cluster, v in cov.items():
                stats = interval(b[j, 0], np.nan if v is None else v[j, j], dfs[cluster], design["alpha"])
                if not present[j]:
                    stats.update(ee=np.nan, ic_inf=np.nan, ic_sup=np.nan, p=np.nan)
                cross_rows.append(dict(muestra=method, franja=hour, gravedad=severity, tramo="d0..1",
                                       estado="estimado" if present[j] else "sin_registros", agrupacion=cluster, **stats))
    pd.DataFrame(cross_rows).to_csv(out / "causal_cruce.csv", index=False)
    # Fechas exactas de referencia, incluidas las placebo.
    dates = []
    for scenario in ("principal", "placebo"):
        for index in samples[scenario]["emparejada"].indice.unique():
            for h in range(-7, 14):
                refs = [index + pd.Timedelta(days=b) for b in baseline_offsets(h)]
                dates.append(dict(escenario=scenario, indice=index, inicio_real=index + pd.Timedelta(days=28 if scenario == "placebo" else 0),
                                  h=h, resultado=index + pd.Timedelta(days=h), b1=refs[0], b2=refs[1], b3=refs[2]))
    pd.DataFrame(dates).to_csv(out / "causal_fechas_base.csv", index=False)
    pd.DataFrame([dict(registros_fecha_invalida=len(invalid),
                       mes_desconocido=int((~invalid.mes.between(1, 12).fillna(False)).sum()),
                       regla="conteo de filas publicadas con fecha valida; elegibilidad predicha hasta t-1")]).to_csv(out / "causal_medicion.csv", index=False)
    print(f"Ruta B: {len(rows)} estimaciones; soporte principal {modelos.summarize(samples['principal']['emparejada'])}")


def tables(config):
    from .informe_final import tables as make
    make(config)


def figures(config):
    from .informe_final import figures as make
    make(config)

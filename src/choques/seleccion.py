import numpy as np
import pandas as pd


COVARIATES = ["poblacion", "empleo_mil", "autos_mil"]


def has_support(controls, design):
    return (len(controls) >= design["min_controls"]
            and controls.estado.nunique() >= design["min_control_states"])


def check_weights(sample):
    if sample.empty:
        return
    if sample.duplicated(["clave", "indice"]).any() or not sample.peso.gt(0).all():
        raise ValueError("Una muestra ponderada requiere pares únicos y pesos positivos")
    totals = sample.groupby(["indice", "tratado"]).peso.sum().unstack()
    if not np.allclose(totals[0], totals[1], rtol=0, atol=1e-10):
        raise ValueError("Los pesos de ambos grupos deben coincidir por fecha")


def uniform(treated, controls, empty):
    if treated.empty or controls.empty:
        return empty
    return pd.concat([treated.assign(peso=1.0), controls.assign(peso=len(treated) / len(controls))])


def complete_sample(sample, design):
    selected, diagnostics = [], []
    empty = sample.iloc[:0].copy()
    for index, cohort in sample.groupby("indice", sort=True):
        available = cohort.dropna(subset=COVARIATES)
        treated = available.loc[available.tratado.eq(1)]
        controls = available.loc[available.tratado.eq(0)]
        accepted = not treated.empty and has_support(controls, design)
        diagnostics.append(dict(indice=index, tratados_auditados=int(cohort.tratado.sum()),
                                tratados_completos=len(treated), controles_completos=len(controls),
                                estados_controles=controls.estado.nunique(), incluida=accepted))
        if accepted:
            selected.append(uniform(treated, controls, empty))
    result = pd.concat(selected, ignore_index=True) if selected else empty
    check_weights(result)
    return result, pd.DataFrame(diagnostics)


def match(sample, design, covariates=None):
    from .modelos import caliber_mask
    covariates = COVARIATES if covariates is None else covariates
    selected, diagnostics, links = [], [], []
    for index, cohort in sample.groupby("indice", sort=True):
        treated = cohort.loc[cohort.tratado.eq(1)]
        controls = cohort.loc[cohort.tratado.eq(0)].set_index("clave", drop=False)
        complete = controls.dropna(subset=covariates)
        keep_t, weights = [], {}
        for row in treated.itertuples():
            missing = [name for name in covariates if pd.isna(getattr(row, name))]
            candidates = complete if not missing else complete.iloc[:0]
            counts = {}
            failure = "faltantes_tratado" if missing else ""
            if not failure and not has_support(candidates, design):
                failure = "datos_completos"
            if design.get("individual_caliber", False):
                candidates = candidates.loc[caliber_mask(candidates.pre_nivel, row.pre_nivel, design.get("caliber", 2.0))]
                counts["despues_pre_nivel"] = len(candidates)
                counts["estados_despues_pre_nivel"] = candidates.estado.nunique()
                if not failure and not has_support(candidates, design):
                    failure = "pre_nivel"
            for name in covariates:
                value = getattr(row, name)
                candidates = candidates.loc[candidates[name].between(value / 2, value * 2)]
                counts[f"despues_{name}"] = len(candidates)
                counts[f"estados_despues_{name}"] = candidates.estado.nunique()
                if not failure and not has_support(candidates, design):
                    failure = name
            accepted = not failure
            diagnostics.append(dict(indice=index, clave=row.clave, estado=row.estado,
                                    id_episodio=row.id_episodio, faltantes_tratado=";".join(missing),
                                    controles_auditados=len(controls), controles_completos=len(complete),
                                    estados_completos=complete.estado.nunique(), **counts,
                                    motivo=failure, incluida=accepted))
            if accepted:
                keep_t.append(row.clave)
                weight = 1 / len(candidates)
                for key in candidates.index:
                    weights[key] = weights.get(key, 0.0) + weight
                    links.append((index, row.clave, key, weight))
        if keep_t:
            picked = controls.loc[list(weights)].copy()
            picked["peso"] = picked.index.map(weights)
            selected.extend([treated.loc[treated.clave.isin(keep_t)].assign(peso=1.0), picked])
    result = pd.concat(selected, ignore_index=True) if selected else sample.iloc[:0].copy()
    check_weights(result)
    return result, pd.DataFrame(diagnostics), pd.DataFrame(
        links, columns=["indice", "tratado_clave", "control_clave", "contribucion"])


def one_to_one(matched, links):
    if links.empty:
        return matched, links.assign(distancia_log2=pd.Series(dtype=float))
    pairs = matched.set_index(["indice", "clave"], drop=False)
    treated_keys = pd.MultiIndex.from_frame(links[["indice", "tratado_clave"]])
    control_keys = pd.MultiIndex.from_frame(links[["indice", "control_clave"]])
    treated_values = pairs.loc[treated_keys, COVARIATES].to_numpy(dtype=float)
    control_values = pairs.loc[control_keys, COVARIATES].to_numpy(dtype=float)
    # The eligibility ranges allow a zero only when both values are zero.
    ratios = np.divide(control_values, treated_values, out=np.ones_like(control_values),
                       where=treated_values != 0)
    chosen = (links.assign(distancia_log2=np.linalg.norm(np.log2(ratios), axis=1))
              .sort_values(["distancia_log2", "control_clave"])
              .drop_duplicates(["indice", "tratado_clave"])
              .assign(contribucion=1.0))
    weights = chosen.groupby(["indice", "control_clave"]).contribucion.sum()
    controls = pairs.loc[weights.index].assign(peso=weights.to_numpy())
    result = pd.concat([matched.loc[matched.tratado.eq(1)], controls], ignore_index=True)
    check_weights(result)
    return result, chosen


def same_treated(audited, matched):
    selected = []
    empty = audited.iloc[:0].copy()
    for index, treated in matched.loc[matched.tratado.eq(1)].groupby("indice", sort=True):
        controls = audited.loc[audited.indice.eq(index) & audited.tratado.eq(0)]
        selected.append((uniform(treated, controls, empty),
                         uniform(treated, controls.dropna(subset=COVARIATES), empty)))
    results = tuple(pd.concat(group, ignore_index=True) for group in zip(*selected)) if selected else (empty, empty)
    for sample in results:
        check_weights(sample)
    return results


def balance(samples, columns):
    def moments(frame, column):
        observed = frame.dropna(subset=[column]).sort_values(column)
        x, w = observed[column].to_numpy(), observed.peso.to_numpy()
        if not len(x):
            return dict(n=0, peso=0.0, media=np.nan, de=np.nan, p10=np.nan, p50=np.nan, p90=np.nan)
        mean = np.average(x, weights=w)
        quantiles = x[np.searchsorted(np.cumsum(w) / w.sum(), [0.1, 0.5, 0.9])]
        return dict(n=len(x), peso=w.sum(), media=mean, de=np.sqrt(np.average((x - mean)**2, weights=w)),
                    p10=quantiles[0], p50=quantiles[1], p90=quantiles[2])

    rows = []
    for column in columns:
        reference = samples["auditada"]
        scales = [moments(reference.loc[reference.tratado.eq(role)], column)["de"] for role in (0, 1)]
        scale = np.sqrt(np.mean(np.square(scales)))
        for name, frame in samples.items():
            control, treated = [moments(frame.loc[frame.tratado.eq(role)], column) for role in (0, 1)]
            difference = treated["media"] - control["media"]
            standardized = difference / scale if scale > 0 else np.nan
            for role, stats in enumerate((control, treated)):
                rows.append(dict(muestra=name, covariable=column, tratado=role, **stats,
                                 diferencia=difference, escala_auditada=scale, dme=standardized))
    return pd.DataFrame(rows)

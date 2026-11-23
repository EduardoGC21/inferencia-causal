"""Cotejo reproducible sobre los pares y pesos exportados por Ruta B."""
import hashlib
import json

import numpy as np
import pandas as pd
from scipy.stats import f, t

from . import causal, modelos
from .conteos import CROSS
from .estadistica import estimate, interval


TOLERANCE = 1e-9
STATS = ["efecto", "ee", "ic_inf", "ic_sup", "p", "gl"]
EFFECT_KEYS = ["escenario", "muestra", "base", "escala", "modelo", "tramo", "agrupacion"]
WALD_KEYS = ["escenario", "muestra", "escala", "agrupacion", "referencia", "restricciones"]
CROSS_KEYS = ["muestra", "tramo", "franja", "gravedad", "agrupacion"]


def fitted(frame, columns, delta, baseline, observed, design, with_jackknife):
    np.testing.assert_allclose(observed - baseline, delta, rtol=0, atol=1e-12)
    for label, y, base in (("cambios", delta, None), ("largo", observed, baseline)):
        beta, cov, dfs = estimate(frame, columns, y, design, baseline=base)
        if with_jackknife:
            v, states, _ = causal.jackknife(frame, columns, y, design, baseline=base, beta=beta)
            cov["CRV3"], dfs["CRV3"] = v, len(states) - 1
        units = range(0, beta.size, len(columns))
        for cluster, v in cov.items():
            variances = np.diag(v)[list(units)] if v is not None else np.full(y.shape[1], np.nan)
            yield label, cluster, [
                interval(b, variance, dfs[cluster], design["alpha"])
                for b, variance in zip(beta[:, 0], variances, strict=True)
            ]


def compare(name, reference, fitted_rows, keys, numbers, categories, output, replica, alpha):
    ref = reference.set_index(keys).sort_index()
    frames = {"referencia": ref}
    for label, rows in fitted_rows.items():
        frames[label] = pd.DataFrame(rows).set_index(keys).sort_index()
    if replica is not None:
        frames["largo_R"] = replica.set_index(keys).sort_index()
    flag = frames["cambios"].degenerado
    degenerate_details = {}
    for label, frame in frames.items():
        pd.testing.assert_index_equal(ref.index, frame.index)
        if name == "efectos":
            # Los horizontes idénticos a su base tienen cambio nulo por
            # definición. El redondeo puede generar incluso una varianza
            # negativa ínfima. Cotejar el cero analítico y omitir la prueba t.
            metrics = ["efecto", "ee", "ic_inf", "ic_sup"]
            values = frame.loc[flag, metrics]
            assert values.abs().max().max() < TOLERANCE or not flag.any()
            degenerate_details[label] = {"ee_indefinidos": int(values.ee.isna().sum()),
                                         "p_de_redondeo": int(frame.loc[flag, "p"].notna().sum())}
            frame.loc[flag, metrics] = 0.0
        frame.loc[flag, "p"] = np.nan
        if label != "referencia":
            for column in categories:
                pd.testing.assert_series_equal(frame[column], ref[column], check_dtype=False)

    differences = {}
    for actual, expected in (("cambios", "referencia"), ("largo", "cambios"), ("largo_R", "largo")):
        if actual not in frames:
            continue
        differences[actual] = {}
        for column in numbers:
            a, b = (frames[label][column].to_numpy(dtype=float) for label in (actual, expected))
            np.testing.assert_allclose(a, b, atol=TOLERANCE, rtol=0, equal_nan=True,
                                       err_msg=f"{name}: {actual} / {expected}, {column}")
            valid = np.isfinite(a) & np.isfinite(b)
            differences[actual][column] = float(np.max(np.abs(a[valid] - b[valid]), initial=0))

    long = frames["largo"]
    raw = long[numbers].copy()
    count = long["n"]
    # Si se usa el número de filas, el rango completo es N+K y el
    # denominador 2N-(N+K)=N-K. Los grados de libertad por grupos no varían.
    ratio = ((2 * count - 1) / (count - 1)).where(long.index.get_level_values("agrupacion") != "CRV3", 1)
    raw["ee"] *= np.sqrt(ratio)
    margin = t.ppf(1 - alpha / 2, raw.gl) * raw.ee
    raw["ic_inf"], raw["ic_sup"] = raw.efecto - margin, raw.efecto + margin
    raw["p"] = 2 * t.sf((raw.efecto / raw.ee.where(raw.ee.gt(0))).abs(), raw.gl)
    if "f" in raw:
        joint = raw.f.notna()
        raw.loc[joint, "f"] /= ratio[joint]
        raw.loc[joint, "p"] = f.sf(raw.loc[joint, "f"], raw.loc[joint, "gl_num"], raw.loc[joint, "gl_den"])
        raw["autovalor_min"] *= ratio
    raw.loc[long.degenerado, "p"] = np.nan
    shifts = (raw.p.le(alpha) != long.p.le(alpha)) & raw.p.notna() & long.p.notna()
    frames["largo_2N"] = raw
    details = pd.concat({label: frame[numbers] for label, frame in frames.items()}, axis=1)
    details.columns = [f"{metric}_{label}" for label, metric in details.columns]
    details = long[list(dict.fromkeys(["n", "degenerado", *categories]))].join(details)
    details["cambia_rechazo_5pct"] = shifts
    details.to_csv(output / f"{name}.csv")
    summary = {"filas": len(ref), "diferencias_maximas": differences,
               "contrastes_degenerados": int(long.degenerado.sum()), "cambia_rechazo_5pct": int(shifts.sum())}
    if degenerate_details:
        summary["artefactos_de_redondeo_en_contrastes_identicos"] = degenerate_details
    return summary


def covariate_fits(frame, columns, delta, base, observed, design):
    """Inferencia de las covariables impresas en los paneles A y B."""
    j = list(causal.HORIZONS).index("d0..1")
    for label, y, baseline in (("cambios", delta[:, [j]], None),
                               ("largo", observed[:, [j]], base[:, [j]])):
        beta, cov, dfs = estimate(frame, columns, y, design, baseline=baseline)
        for k, column in enumerate(columns[1:], start=1):
            cluster = "entidad_fecha"
            yield label, column, interval(beta[0, k], cov[cluster][k, k], dfs[cluster], design["alpha"])


def run(config, reference, processed, output, replica=None):
    design = config["design"]
    alpha = design["alpha"]
    paths = {"processed": processed}
    matrix, _ = modelos.load(paths)
    counts = pd.read_parquet(processed / "conteos_diarios.parquet")
    published = causal.published_matrix(matrix, counts)
    crossed = counts.set_index(["clave", "fecha"])[list(CROSS.values())]
    pair_keys = ["escenario", "muestra", "clave", "indice"]
    sample_columns = pair_keys + ["estado", "id_episodio", "tratado", "peso", *causal.COVARIATES]
    sample_options = dict(parse_dates=["indice"], dtype={"clave": str, "estado": str}, usecols=sample_columns)
    sample = pd.read_csv(reference / "causal_muestras.csv", **sample_options)
    samples = sample.groupby(["escenario", "muestra"], sort=False)
    effects, weekly, cross = [pd.read_csv(reference / f"causal_{suffix}.csv")
                              for suffix in ("efectos", "wald_semanal", "cruce")]
    rows = {name: {"cambios": [], "largo": []} for name in ("efectos", "wald_semanal", "cruce")}
    covariates = {"cambios": [], "largo": []}
    groups = ["escenario", "muestra", "base", "escala"]
    for (scenario, method, base, scale), group in effects.groupby(groups, sort=False):
        frame = samples.get_group((scenario, method))
        delta = causal.contrasts(published, frame, scale, base)
        baseline, observed = causal.contrasts(published, frame, scale, base, panel=True)
        for model, specifications in group.groupby("modelo", sort=False):
            columns = causal.MODEL_COLUMNS[:int(model[1:]) + 1]
            data = frame.assign(log_poblacion=np.log(frame.poblacion)) if len(columns) > 1 else frame
            totals = modelos.summarize(data)
            with_jackknife = specifications.agrupacion.eq("CRV3").any()
            if (scenario, method, base) == ("principal", "emparejada", "tres_semanas") and model != "M0":
                for label, column, stats in covariate_fits(data, columns, delta, baseline, observed, design):
                    covariates[label].append(dict(escala=scale, modelo=model, variable=column, **stats))
            for label, cluster, fits in fitted(data, columns, delta, baseline, observed, design, with_jackknife):
                for horizon, stats in zip(causal.HORIZONS, fits, strict=True):
                    rows["efectos"][label].append(dict(escenario=scenario, muestra=method, base=base,
                        escala=scale, modelo=model, tramo=horizon, agrupacion=cluster, **stats,
                        **{key: totals[key] for key in ("n", "tratados", "controles")},
                        degenerado=base == horizon and base in ("wk-1", "-2")))

    for scenario, method, scale in weekly[["escenario", "muestra", "escala"]].drop_duplicates().itertuples(index=False):
        frame = samples.get_group((scenario, method))
        for label in ("cambios", "largo"):
            fits = causal.weekly_tests(published, frame, design, scale, panel=label == "largo")
            rows["wald_semanal"][label].extend(
                dict(stats, escenario=scenario, muestra=method, n=len(frame), degenerado=False) for stats in fits)

    labels = list(CROSS) + [("noche_menos_dia", severity) for severity in ("fatal", "heridos", "danos")]
    for method in cross.muestra.unique():
        frame = samples.get_group(("principal", method))
        delta, _ = causal.cross_outcomes(crossed, frame)
        baseline, observed, present = causal.cross_outcomes(crossed, frame, panel=True)
        for label, cluster, fits in fitted(frame, ["tratado"], delta, baseline, observed, design, False):
            for (hour, severity), active, stats in zip(labels, present, fits, strict=True):
                if not active:
                    stats.update(ee=np.nan, ic_inf=np.nan, ic_sup=np.nan, p=np.nan)
                rows["cruce"][label].append(dict(muestra=method, tramo="d0..1", franja=hour,
                    gravedad=severity, agrupacion=cluster, n=len(frame), degenerado=not active,
                    estado="estimado" if active else "sin_registros", **stats))

    output.mkdir(parents=True, exist_ok=True)
    summary = {"tolerancia_absoluta": TOLERANCE, "filas_muestras_exportadas": len(sample),
               "sha256_insumos": {}}
    for path in (reference / f"causal_{name}.csv" for name in ("muestras", "efectos", "wald_semanal", "cruce")):
        with path.open("rb") as stream:
            summary["sha256_insumos"][path.name] = hashlib.file_digest(stream, "sha256").hexdigest()
    if replica:
        replica_sample = pd.read_csv(replica / "causal_muestras.csv", **sample_options)
        pd.testing.assert_frame_equal(sample[sample_columns].set_index(pair_keys).sort_index(),
                                      replica_sample[sample_columns].set_index(pair_keys).sort_index(),
                                      check_dtype=False, check_exact=False, atol=1e-8, rtol=0)
        summary["pares_y_pesos_R_cotejados"] = len(sample)
    cov_frames = [pd.DataFrame(data).set_index(["escala", "modelo", "variable"]) for data in covariates.values()]
    pd.testing.assert_frame_equal(*cov_frames, check_exact=False, atol=TOLERANCE, rtol=0)
    pd.concat(cov_frames, axis=1, keys=covariates.keys()).to_csv(output / "covariables_d0_1.csv")
    summary["covariables_d0_1"] = {"filas": len(cov_frames[0]),
                                  "diferencias_maximas": (cov_frames[0] - cov_frames[1]).abs().max().to_dict()}
    wald_stats = ["f", "gl_num", "gl_den", "rango", "condicion", "autovalor_min"]
    for name, verified, keys, numbers, categories in (
        ("efectos", effects, EFFECT_KEYS, STATS, ["n", "tratados", "controles"]),
        ("wald_semanal", weekly, WALD_KEYS, STATS + wald_stats, ["estado"]),
        ("cruce", cross, CROSS_KEYS, STATS, ["estado"]),
    ):
        r = pd.read_csv(replica / f"causal_{name}.csv") if replica else None
        summary[name] = compare(name, verified, rows[name], keys, numbers, categories, output, r, alpha)
    result = json.dumps(summary, ensure_ascii=False, indent=2)
    (output / "resumen.json").write_text(result + "\n", encoding="utf-8")
    print(result)

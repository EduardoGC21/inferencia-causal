import json
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd

from . import modelos, municipios
from .descarga import hash_file
from .diagnosticos import WINDOWS, average, by_category, history
from .estadistica import estimate, interval, wald
from .seleccion import COVARIATES, balance, complete_sample, match, same_treated


MODELS = ["tratado", "log_poblacion", "empleo_mil", "autos_mil"]
BALANCE = COVARIATES + ["pre_nivel", "auto_vivienda", "vacb_pc_2023"]


def csv(frame, folder, name):
    frame.to_csv(folder / f"{name}.csv", index=False)


def coverage(sample):
    rows = []
    for keys, group in sample.groupby(["especificacion", "indice", "tratado"], sort=True):
        specification, index, role = keys
        for source, column in [("censo", "poblacion"), ("saic", "empleo"), ("vmrc", "autos")]:
            join = group[f"{source}_union"]
            cut = group[f"corte_{source}"].iloc[0]
            status = group[f"{column}_estado"]
            value = {"poblacion": "poblacion", "empleo": "empleo_mil", "autos": "autos_mil"}[column]
            denominator = group.get(f"{source}_conapo_union")
            rows.append(dict(especificacion=specification, indice=index, tratado=role, fuente=source,
                             corte=cut, pares=len(group), unidas=int(join.eq("unida").sum()),
                             tasa_union=join.eq("unida").mean(), utilizables=int(group[value].notna().sum()),
                             ceros=int(status.eq("cero").sum()), confidenciales=int(status.eq("confidencial").sum()),
                             faltantes_declarados=int(status.eq("faltante").sum()),
                             conapo_sin_clave=int(denominator.eq("sin_clave").sum()) if denominator is not None else None,
                             conapo_territorio_incompatible=int(denominator.eq("territorio_incompatible").sum())
                             if denominator is not None else None,
                             sin_clave=int(join.eq("sin_clave").sum()), solo_entidad=int(join.eq("solo_entidad").sum()),
                             territorio_incompatible=int(join.eq("territorio_incompatible").sum()),
                             quiebre_en_ventana=int(join.eq("quiebre_en_ventana").sum()),
                             perimetro_no_confirmado=int(join.eq("perimetro_no_confirmado").sum()),
                             medicion_posterior=int(join.eq("medicion_posterior").sum())))
    return pd.DataFrame(rows)


def build(config, output):
    paths, design = config["paths"], config["design"]
    sample_path = paths["outputs"] / "modelos" / "muestra.csv"
    release = paths["tasks"] / "revision-auditoria" / "revision_auditada.json"
    revision = json.loads(release.read_text(encoding="utf-8"))
    if hash_file(sample_path) != revision["muestra_sha256"]:
        raise ValueError("La elegibilidad previa difiere de la muestra auditada")
    original = pd.read_csv(sample_path, dtype={"clave": str, "estado": str},
                           parse_dates=["indice"], keep_default_na=False)
    tables, changes = municipios.load(paths)
    state_aggregates = municipios.rates(tables)
    csv(state_aggregates, output, "vmrc_registros_no_municipales")
    csv(municipios.vehicle_diagnostics(tables["vmrc"]), output, "vmrc_cobertura")
    for source in ("saic", "vmrc"):
        csv(tables[source], output, f"tasas_{source}")
    combined = municipios.attach(original.loc[original.especificacion.isin(["principal", "placebo"])],
                                 tables, changes, design, state_aggregates)
    csv(combined, output, "covariables_por_fecha")
    csv(coverage(combined), output, "cobertura_covariables")
    samples, counts, edges, scope, denominator, loss, complete_loss, alternate_loss = {}, [], [], [], [], [], [], []
    for name in ("principal", "placebo"):
        reference = combined.loc[combined.especificacion.eq(name)].copy()
        matched, diagnostics, links = match(reference, design)
        entire, observed = same_treated(reference, matched)
        common, losses = complete_sample(reference, design)
        alternative = reference.assign(empleo_mil=reference.empleo_mil_alt, autos_mil=reference.autos_mil_alt)
        matched_alt, alt_diagnostics, _ = match(alternative, design)
        common_alt, alt_complete = complete_sample(alternative, design)
        sample_set = {"auditada": reference, "mismos_tratados": entire, "mismos_tratados_completos": observed,
                      "emparejada": matched, "comun_m0_m3": common}
        samples[name] = sample_set
        edges.append(links.assign(diseno=name))
        loss.append(diagnostics.assign(diseno=name))
        complete_loss.append(losses.assign(diseno=name))
        alternate_loss.extend([alt_diagnostics.assign(diseno=name, metodo="emparejada"),
                               alt_complete.assign(diseno=name, metodo="comun_m0_m3")])
        for label, frame in sample_set.items():
            counts.append(dict(diseno=name, muestra=label, **modelos.summarize(frame)))
            scope.append(frame[modelos.SAMPLE + COVARIATES].assign(diseno=name, muestra=label))
        comparison = {"conapo_emparejada": matched, "censo_emparejada": matched_alt,
                      "conapo_comun": common, "censo_comun": common_alt}
        for label, frame in comparison.items():
            denominator.append(dict(diseno=name, denominador_muestra=label, **modelos.summarize(frame)))
    results = {
        "muestras_municipales": pd.concat(scope, ignore_index=True),
        "soporte_municipal": pd.DataFrame(counts),
        "descartes_municipales": pd.concat(loss, ignore_index=True),
        "descartes_muestra_comun": pd.concat(complete_loss, ignore_index=True),
        "descartes_denominador_censal": pd.concat(alternate_loss, ignore_index=True),
        "reparto_controles": pd.concat(edges, ignore_index=True),
        "soporte_denominador_censal": pd.DataFrame(denominator),
        "balance": pd.concat([balance(groups, BALANCE).assign(diseno=name) for name, groups in samples.items()],
                             ignore_index=True),
    }
    for name, table in results.items():
        csv(table, output, name)
    sample = results["muestras_municipales"]
    weights = (sample.groupby(["diseno", "muestra", "indice", "tratado"], sort=True)
               .agg(n=("clave", "size"), estados=("estado", "nunique"), peso=("peso", "sum")).reset_index())
    csv(weights, output, "pesos_por_fecha")
    return samples


def support(config):
    destination = config["paths"]["outputs"] / "modelos"
    with TemporaryDirectory(dir=destination) as temporary:
        working = Path(temporary)
        build(config, working)
        for file in working.iterdir():
            file.replace(destination / file.name)


def sample_result(matrix, sample, horizons, pre, design):
    main, windows, joint = [], [], []
    for h in horizons:
        main.append(dict(h=h, **modelos.fit(matrix, sample, h, design)))
    for name, baseline in [("-2", (-2,)), ("media_previa", pre)]:
        baseline_mean = average(matrix, sample, baseline)
        spans = WINDOWS if name == "-2" else {str(h): (h,) for h in horizons} | WINDOWS
        delta = np.column_stack([average(matrix, sample, span) - baseline_mean for span in spans.values()])
        coefficients, covariances, dfs = estimate(sample, ["tratado"], delta, design)
        for offset, span in enumerate(spans):
            for cluster, v in covariances.items():
                var = np.nan if v is None else v[offset, offset]
                windows.append(dict(base=name, tramo=span, agrupacion=cluster,
                                    **interval(coefficients[offset, 0], var, dfs[cluster], design["alpha"])))
    before = [h for h in horizons if h < -2]
    delta = np.column_stack([matrix.extract(sample, h) - matrix.extract(sample, -2) for h in before])
    coefficients, covariances, dfs = estimate(sample, ["tratado"], delta, design)
    for cluster, variance in covariances.items():
        joint.append(dict(prueba="previos", agrupacion=cluster,
                          **wald(coefficients[:, 0], variance, dfs[cluster])))
    return main, windows, joint


def adjusted(matrix, common, horizons, design, is_placebo):
    sample = common.assign(log_poblacion=np.log(common.poblacion))
    baseline = matrix.extract(sample, -2)
    delta = np.column_stack([matrix.extract(sample, h) - baseline for h in horizons])
    estimates, tests = [], []
    pre = [i for i, h in enumerate(horizons) if h < -2]
    zero = horizons.index(0)
    totals = modelos.summarize(sample)
    for k in range(1, len(MODELS) + 1):
        coefficients, covariances, dfs = estimate(sample, MODELS[:k], delta, design)
        for cluster, v in covariances.items():
            df = dfs[cluster]
            for index, h in enumerate(horizons):
                variance = np.nan if v is None else v[index * k, index * k]
                estimates.append(dict(modelo=f"M{k - 1}", h=h, agrupacion=cluster, **totals,
                                      **interval(coefficients[index, 0], variance, df, design["alpha"])))
            pos = np.asarray(pre) * k
            covariance = None if v is None else v[np.ix_(pos, pos)]
            tests.append(dict(modelo=f"M{k - 1}", prueba="previos", agrupacion=cluster,
                              **wald(coefficients[pre, 0], covariance, df)))
            if k > 1 and not is_placebo:
                restrictions = [(MODELS[k - 1], [k - 1])]
                if k == len(MODELS):
                    restrictions.append(("conjunta_covariables", list(range(1, k))))
                for label, r in restrictions:
                    at_zero = np.asarray(r) + zero * k
                    covariance = None if v is None else v[np.ix_(at_zero, at_zero)]
                    tests.append(dict(modelo=f"M{k - 1}", prueba=label, agrupacion=cluster,
                                      **wald(coefficients[zero, r], covariance, df)))
        if k == 1 and not sample.empty:
            plain = modelos.fit(matrix, sample, 0, design)
            np.testing.assert_allclose(coefficients[zero, 0], plain["efecto"], rtol=0, atol=1e-10)
            np.testing.assert_allclose(covariances["entidad"][zero, zero], plain["ee"]**2, rtol=0, atol=1e-10)
    return estimates, tests


def run(config):
    destination = config["paths"]["outputs"] / "modelos"
    with TemporaryDirectory(dir=destination) as temporary:
        working = Path(temporary)
        estimate_daily(config, working)
        for file in working.iterdir():
            file.replace(destination / file.name)


def estimate_daily(config, output):
    paths, design = config["paths"], config["design"]
    groups = build(config, output)
    matrix, events = modelos.load(paths)
    pre = tuple(range(-design["pre"], -design["anticipation"]))
    horizons = [h for h in pre if h < -2] + list(range(design["horizon"] + 1))
    trajectories, periods, joint, regressions, specifications = [], [], [], [], []
    for name, samples in groups.items():
        fits, tests = adjusted(matrix, samples["comun_m0_m3"], horizons, design, name == "placebo")
        regressions.extend(dict(row, diseno=name) for row in fits)
        specifications.extend(dict(row, diseno=name) for row in tests)
        for label, sample in samples.items():
            if label == "comun_m0_m3":
                continue
            main, windows, diagnostic = sample_result(matrix, sample, horizons, pre, design)
            trajectories.extend(dict(row, diseno=name, muestra=label) for row in main)
            periods.extend(dict(row, diseno=name, muestra=label) for row in windows)
            joint.extend(dict(row, diseno=name, muestra=label) for row in diagnostic)
    for table, name in [(trajectories, "comparaciones_municipales"), (periods, "tramos_y_base"),
                        (joint, "wald_previos"), (regressions, "modelos_m0_m3"), (specifications, "wald_modelos")]:
        csv(pd.DataFrame(table), output, name)
    principal = groups["principal"]
    benchmark = next(x for x in trajectories if x["diseno"] == "principal" and x["muestra"] == "auditada" and x["h"] == 0)
    if (tuple(benchmark[k] for k in ("tratados", "controles", "fechas")) != (73, 7351, 30)
            or abs(benchmark["efecto"] - 0.237468) > 1e-6):
        raise ValueError("Las cifras de la muestra auditada no cumplen la referencia")
    by_category(paths["processed"] / "conteos_diarios.parquet",
                {key: principal[key] for key in ("auditada", "emparejada")}, matrix, design, output)
    history(principal["auditada"], matrix, events, config["atus"]["first"], design, output)
    print(f"Comparaciones municipales estimadas: {len(trajectories)} contrastes y {len(regressions)} regresiones agrupadas.")

"""Verificación del panel diario y cotejo de las ejecuciones Python y R."""
import hashlib
import json

import numpy as np
import pandas as pd

from .estadistica import estimate


TOLERANCE = 1e-9
STATS = ["efecto", "ee", "ic_inf", "ic_sup", "p", "gl"]
PAIR = ["escenario", "muestra", "clave", "indice"]
FIT = ["escenario", "muestra"]
PANEL = FIT + ["base", "tramo"]


def check_startup(sample, matrix, design, output):
    from .causal import BASE_DAYS, SPANS, panel_changes

    dates = sample.indice.sort_values().unique()[:2].to_numpy()
    frame = (sample.loc[sample.indice.isin(dates)].groupby(["indice", "tratado"])
             .head(3).reset_index(drop=True))
    span = SPANS["d0..1"]
    assert BASE_DAYS == tuple(range(-28, -7))
    offsets = (*BASE_DAYS, *span)
    daily = {h: matrix.extract(frame, h)[:, None] for h in offsets}
    weights, rows, outcome, days = [], [], [], []
    n = len(frame)
    for s, block in enumerate((BASE_DAYS, span)):
        for h in block:
            calendar = frame.indice + pd.to_timedelta(h, unit="D")
            weekday = calendar.dt.day_of_week.to_numpy()
            assert weekday.tolist() == [d.date().weekday() for d in calendar]
            days.append(weekday)
            weights.append(frame.peso.to_numpy() / len(block))
            rows.append(np.column_stack((np.eye(n), (frame.indice.to_numpy()[:, None] == dates) * s,
                                         frame.tratado * s, np.eye(7)[weekday, 1:])))
            outcome.append(daily[h])
    weights = np.asarray(weights)
    for block in (weights[:21], weights[21:]):
        np.testing.assert_allclose(block.sum(axis=0), frame.peso, rtol=0, atol=1e-12)
    np.testing.assert_array_equal(np.sort(days[:21], axis=0), np.tile(np.repeat(np.arange(7), 3)[:, None], (1, n)))

    # Each cohort/block has a single aggregated weekday profile. Use one row
    # per cell to check the incremental rank over the cell indicators.
    aggregated = np.vstack([np.eye(7)[days[:21], 1:].mean(axis=0),
                            np.eye(7)[days[21:], 1:].mean(axis=0)])
    cells = np.eye(2 * len(dates))[np.r_[np.searchsorted(dates, frame.indice),
                                        len(dates) + np.searchsorted(dates, frame.indice)]]
    saturated = np.column_stack([cells, aggregated])
    absorbed = np.linalg.matrix_rank(saturated) - np.linalg.matrix_rank(cells)
    assert absorbed == 0
    daily_x = np.vstack(rows)
    assert np.linalg.matrix_rank(daily_x) - np.linalg.matrix_rank(daily_x[:, :-6]) == 6
    changes, audit = panel_changes(frame, daily, {"d0..1": span})
    collapsed, _, _ = estimate(frame, ["tratado"], changes, design)
    sw = np.sqrt(weights.reshape(-1, 1))
    explicit = np.linalg.lstsq(daily_x * sw, np.vstack(outcome) * sw, rcond=None)[0][-7:, 0]
    reduced = [collapsed[0, 0], *[audit[0][f"d{j}"] for j in range(1, 7)]]
    np.testing.assert_allclose(explicit, reduced, atol=1e-10, rtol=0)
    output.mkdir(parents=True, exist_ok=True)
    report = dict(pares=n, fechas=len(dates), offsets_base=list(BASE_DAYS), dia_semana="lunes=0",
                  error_maximo_masa=float(max(abs(weights[:21].sum(axis=0) - frame.peso).max(),
                                              abs(weights[21:].sum(axis=0) - frame.peso).max())),
                  rango_incremental_agregado=int(absorbed), rango_incremental_diario=6,
                  diferencia_maxima_ajuste_explicito=float(np.max(np.abs(explicit - reduced))))
    (output / "arranque.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))


def run(python, replica, output, previous=None):
    output.mkdir(parents=True, exist_ok=True)
    summary = {"tolerancia_absoluta": TOLERANCE, "sha256": {}}

    def read(directory, name):
        path = directory / f"causal_{name}.csv"
        with path.open("rb") as stream:
            summary["sha256"].setdefault(str(directory), {})[path.name] = hashlib.file_digest(stream, "sha256").hexdigest()
        return pd.read_csv(path, dtype={"clave": str, "estado_omitido": str, "tramo": str,
                                        "tratado_clave": str, "control_clave": str}, low_memory=False)

    def compare(name, keys, numbers, categories=(), right=replica, label=None):
        a, b = (read(directory, name).set_index(keys, verify_integrity=True).sort_index()
                for directory in (python, right))
        pd.testing.assert_index_equal(a.index, b.index, exact=False)
        for column in categories:
            pd.testing.assert_series_equal(a[column], b[column], check_dtype=False)
        maxima = {}
        for column in numbers:
            x, y = (frame[column].to_numpy(dtype=float) for frame in (a, b))
            np.testing.assert_allclose(x, y, atol=TOLERANCE, rtol=0, equal_nan=True,
                                       err_msg=f"{name}: {column}")
            finite = np.isfinite(x) & np.isfinite(y)
            maxima[column] = float(np.max(np.abs(x[finite] - y[finite]), initial=0))
        if name not in ("muestras", "vinculos", "elegibilidad"):
            pd.concat([a[list(numbers)], b[list(numbers)]], keys=["Python", "R"], axis=1).to_csv(output / f"{name}.csv")
        summary[label or name] = {"filas": len(a), "diferencias_maximas": maxima}
        return a

    sample_metrics = ["estado", "tratado", "peso", "poblacion", "empleo_mil", "autos_mil", "pre_nivel"]
    compare("muestras", PAIR, sample_metrics, ["id_episodio"])
    link_keys = FIT + ["indice", "tratado_clave", "control_clave"]
    compare("vinculos", link_keys, ["contribucion", "distancia_log2"])
    eligibility_keys = ["escenario", "clave", "indice"]
    flags = ["cobertura_predicha", "exposicion_en_ventana", "territorio_compatible",
             "cobertura_completa", "estado_focal", "elegible"]
    compare("elegibilidad", eligibility_keys, ["tratado"], flags)
    if previous is not None:
        compare("muestras", PAIR, sample_metrics, ["id_episodio"], right=previous, label="muestra_vs_anterior")
        compare("elegibilidad", eligibility_keys, ["tratado"], flags, right=previous,
                label="elegibilidad_vs_anterior")
    effects = compare("efectos", PANEL + ["escala", "modelo", "agrupacion"],
                      STATS + ["n", "tratados", "controles", "fechas", "mde", "efecto_sigma", "media_pre", "sigma_pre"],
                      ["estado_inferencia"])
    assert set(effects.index.get_level_values("escala")) == {"niveles"}
    assert set(effects.index.get_level_values("base")) == {"tres_semanas"}
    compare("coeficientes", FIT + ["modelo", "tramo", "agrupacion", "termino"], STATS)
    weekly = compare("wald_semanal", FIT + ["escala", "agrupacion", "referencia", "restricciones"],
            STATS + ["f", "gl_num", "gl_den", "rango", "condicion", "autovalor_min"], ["estado"])
    assert set(weekly.index.get_level_values("referencia")) == {"tres_semanas [-28,-8]"}
    compare("omision_estado", ["muestra", "escala", "modelo", "tramo", "estado_omitido"],
            ["efecto"], ["identificada"])
    compare("cruce", ["muestra", "tramo", "franja", "gravedad", "agrupacion"], STATS, ["estado"])
    ranks = compare("dia_semana", PANEL, ["dias_base", "dias_tramo", "filas", "rango_dia_semana"]
                    + [f"d{j}" for j in range(1, 7)])
    assert ranks.dias_base.eq(21).all()
    assert ranks.rango_dia_semana.eq(6).all()
    assert set(ranks.index.get_level_values("base")) == {"tres_semanas"}
    dates = compare("fechas_base", ["escenario", "indice", "h"], ["dia_semana"], ["inicio_real", "fecha"])
    for _, date in dates.reset_index().groupby(["escenario", "indice"], sort=False):
        assert date.h.tolist() == list(range(-28, -7))
    observed = pd.to_datetime(dates.fecha)
    np.testing.assert_array_equal(observed.dt.day_of_week, dates.dia_semana)
    result = json.dumps(summary, ensure_ascii=False, indent=2)
    (output / "resumen.json").write_text(result + "\n", encoding="utf-8")
    print("Cotejo Python–R completado. " + str(output / "resumen.json"))

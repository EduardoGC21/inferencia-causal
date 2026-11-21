from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd
from scipy.stats import f

from choques.conteos import CROSS, classes
from choques.diagnosticos import by_category
from choques.estadistica import estimate, wald
from choques.municipios import choose_cut, join_cut, numeric
from choques.modelos import Matrix, legacy_comparison as comparison
from choques.seleccion import complete_sample, match, one_to_one
from choques.sensibilidades import monthly_flags, select


def cuts_and_join():
    cuts = {2015: "2015-03-15", 2020: "2020-03-15", 2025: "2025-10-06"}
    assert choose_cut(pd.Timestamp("2020-04-12"), cuts, 28) == 2015
    assert choose_cut(pd.Timestamp("2020-04-13"), cuts, 28) == 2020
    assert choose_cut(pd.Timestamp("2025-10-03"), cuts, 28) == 2020
    values, states = numeric(pd.Series(["0", "", "*", "4"]))
    assert values.iloc[0] == 0 and pd.isna(values.iloc[1]) and pd.isna(values.iloc[2])
    assert list(states) == ["cero", "faltante", "confidencial", "observado"]
    target = pd.DataFrame({"clave": ["09002", "25006", "09003"], "territorio": ["a", "b", "a"]})
    source = pd.DataFrame({"clave": ["09002", "25006"], "territorio": ["a", "a"], "valor": [0, 20]})
    joined = join_cut(target, source, ["valor"], "prueba")
    assert joined.valor.iloc[0] == 0 and joined.valor.iloc[1:].isna().all()
    assert joined.prueba_union.tolist() == ["unida", "territorio_incompatible", "sin_clave"]
    try:
        join_cut(target, pd.concat([source, source]), ["valor"], "prueba")
    except ValueError:
        pass
    else:
        raise AssertionError("Se aceptaron claves duplicadas")


def weights_and_support():
    rows = [
        ("09002", 1, 1000, 20, 1, 8), ("09003", 1, 1400, 20, 1, 7),
        ("09004", 1, 1400, 0, 1, 2), ("09005", 1, 5000, 20, 1, 0),
        ("01001", 0, 1000, 20, 1, 1), ("02001", 0, 500, 20, 1, 3),
        ("03001", 0, 2200, 20, 1, 5), ("04001", 0, 200, 20, 1, 9),
        ("05001", 0, 1000, 50, 1, 9), ("06001", 0, 1000, np.nan, 1, 9),
        ("07001", 0, 1000, 0, 1, 9),
    ]
    sample = pd.DataFrame(rows, columns=["clave", "tratado", "poblacion", "empleo_mil", "autos_mil", "delta"])
    sample = sample.assign(indice=pd.Timestamp("2021-02-01"), estado=sample.clave.str[:2],
                           id_episodio="x", peso=1.0, pre_nivel=2.0)
    design = {"min_controls": 2, "min_control_states": 2}
    matched, losses, links = match(sample, design)
    assert matched[matched.tratado.eq(1)].clave.tolist() == ["09002", "09003"]
    w = matched[matched.tratado.eq(0)].set_index("clave").peso.to_dict()
    assert w == {"01001": 1.0, "02001": 0.5, "03001": 0.5}
    assert len(links) == 4 and losses.incluida.sum() == 2
    assert losses.set_index("clave").loc["09004", "despues_empleo_mil"] == 1
    beta, _, _ = estimate(matched, ["tratado"], matched[["delta"]].to_numpy(), design)
    assert np.isclose(beta[0, 0], (8 + 7) / 2 - (1 + 0.5 * 3 + 0.5 * 5) / 2)
    common, _ = complete_sample(sample, design)
    assert "06001" not in set(common.clave)
    assert common.groupby("tratado").peso.sum().round(10).tolist() == [4.0, 4.0]

    extra = sample.set_index("clave", drop=False).loc[["01001", "07001"]].copy()
    extra = extra.assign(clave=["01002", "08001"], estado=["01", "08"])
    expanded, _, eligible = match(pd.concat([extra, sample], ignore_index=True), design)
    paired, chosen = one_to_one(expanded, eligible.iloc[::-1])
    assert paired.loc[paired.tratado.eq(1), "clave"].tolist() == ["09002", "09003", "09004"]
    assert chosen.set_index("tratado_clave").control_clave.to_dict() == {
        "09002": "01001", "09003": "01001", "09004": "07001",
    }
    assert paired.loc[paired.tratado.eq(0)].set_index("clave").peso.to_dict() == {"01001": 2.0, "07001": 1.0}
    assert chosen.contribucion.eq(1.0).all()
    distances = chosen.set_index("tratado_clave").distancia_log2
    np.testing.assert_allclose(distances.loc[["09002", "09003", "09004"]],
                               [0, np.log2(1.4), np.log2(1.4)])
    beta, _, _ = estimate(paired, ["tratado"], paired[["delta"]].to_numpy(), design)
    assert np.isclose(beta[0, 0], (8 + 7 + 2 - 2 * 1 - 9) / 3)
    empty, _, no_links = match(sample.loc[sample.clave.eq("09005")], design)
    assert all(frame.empty for frame in one_to_one(empty, no_links))


def models_and_wald():
    rng = np.random.default_rng(63)
    frame = pd.DataFrame({
        "indice": np.repeat(pd.date_range("2022-01-01", periods=7), 18),
        "estado": np.tile(np.repeat(list("abcdef"), 3), 7),
        "tratado": np.tile([0, 1, 0, 0, 0, 0], 21),
        "poblacion": np.exp(rng.normal(10, 1, 126)),
        "empleo_mil": rng.uniform(1, 20, 126), "autos_mil": rng.uniform(30, 80, 126),
        "respuesta": rng.normal(size=126),
    })
    frame["clave"] = frame.estado + frame.groupby(["indice", "estado"]).cumcount().astype(str)
    frame.loc[0, "empleo_mil"] = np.nan
    common, _ = complete_sample(frame, {"min_controls": 2, "min_control_states": 2})
    common = common.assign(log_poblacion=np.log(common.poblacion))
    signature = common[["clave", "indice", "peso"]].copy()
    y = common.respuesta.to_numpy()
    weights = common.peso.to_numpy()
    full = ["tratado", "log_poblacion", "empleo_mil", "autos_mil"]
    for size in range(1, 5):
        names = full[:size]
        X = np.column_stack([common[names].to_numpy(), pd.get_dummies(common.indice).to_numpy()])
        beta, covariances, dfs = estimate(common, names, y[:, None], {})
        assert signature.equals(common[["clave", "indice", "peso"]])
        assert len(common) == 125
        b = np.linalg.lstsq(X * np.sqrt(weights[:, None]), y * np.sqrt(weights), rcond=None)[0]
        np.testing.assert_allclose(beta[0], b[:size], atol=1e-10)
        if size == 1:
            np.testing.assert_allclose(beta[0, 0], np.average(y[common.tratado.eq(1)], weights=weights[common.tratado.eq(1)]) -
                                       np.average(y[common.tratado.eq(0)], weights=weights[common.tratado.eq(0)]))
    bread = np.linalg.inv(X.T @ (X * weights[:, None]))
    scores = X * (weights * (y - X @ b))[:, None]
    grouped = pd.DataFrame(scores).groupby(common.estado.to_numpy()).sum().to_numpy()
    vcov = bread @ grouped.T @ grouped @ bread * (6 / 5) * (124 / (125 - X.shape[1]))
    np.testing.assert_allclose(covariances["entidad"], vcov[:4, :4], atol=1e-10)
    R = np.eye(4)[1:]
    statistic = (R @ b[:4]) @ np.linalg.solve(R @ vcov[:4, :4] @ R.T, R @ b[:4]) / 3
    result = wald(beta[0, 1:], covariances["entidad"][1:, 1:], dfs["entidad"])
    assert result["gl_num"] == 3 and result["gl_den"] == 5
    assert np.isclose(result["f"], statistic) and np.isclose(result["p"], f.sf(statistic, 3, 5))
    assert wald(np.ones(2), np.ones((2, 2)), 5)["estado"] != "calculada"


def hourly_and_severity():
    rows = pd.DataFrame({"clave": ["09002"] * 6, "fecha": [pd.Timestamp("2022-01-01")] * 6,
                         "ID_HORA": ["00", "05", "06", "17", "18", "99"],
                         "CLASACC": ["Fatal", "No fatal", "Sólo daños"] * 2})
    counts = classes(rows).iloc[0]
    assert [counts[c] for c in ("dia", "noche", "hora_desconocida")] == [2, 3, 1]
    assert [counts[c] for c in ("fatal", "heridos", "danos")] == [2, 2, 2]
    assert [counts[c] for c in CROSS.values()] == [1, 0, 1, 1, 2, 0, 0, 0, 1]


def hourly_cross_effects():
    keys = ["01001", "02001", "03001", "04001"]
    index = pd.Timestamp("2022-03-01")
    dates = pd.date_range(index - pd.Timedelta(days=2), index + pd.Timedelta(days=15))
    sample = pd.DataFrame(dict(clave=keys, indice=index, estado=["01", "02", "03", "04"],
                               tratado=[1, 1, 0, 0], peso=1.0))
    records = []
    for key, day, night in zip(keys, [1, 0, 1, 0], [4, 1, 1, 0]):
        for date in dates[dates > index]:
            records.extend([(key, date, "06", "Fatal")] * day)
            records.extend([(key, date, "18", "Fatal")] * night)
    rows = pd.DataFrame(records, columns=["clave", "fecha", "ID_HORA", "CLASACC"])
    panel = pd.MultiIndex.from_product([keys, dates], names=["clave", "fecha"]).to_frame(index=False)
    totals = rows.groupby(["clave", "fecha"]).size().rename("accidentes")
    panel = panel.join(totals, on=["clave", "fecha"]).fillna({"accidentes": 0}).assign(continuidad=True)
    design = dict(pre=2, anticipation=1, alpha=0.05)
    with TemporaryDirectory() as temporary:
        folder = Path(temporary)
        path = folder / "conteos.parquet"
        classes(rows).reset_index().to_parquet(path, index=False)
        by_category(path, {"sintetica": sample}, Matrix(panel), design, folder)
        effects = pd.read_csv(folder / "franjas_x_gravedad.csv")
        frequencies = pd.read_csv(folder / "frecuencias_franjas_x_gravedad.csv")
    first = effects.query("base == '-2' and tramo == '1–7' and agrupacion == 'entidad'")
    both = first.set_index(["franja", "gravedad"])
    assert len(both) == 12 and both.index.is_unique
    assert set(effects.tramo) == {"1–7", "8–15"}
    difference = both.loc["noche_menos_dia", "fatal"]
    np.testing.assert_allclose([difference.efecto, difference.ee], [2, 1])
    marginal_day = both.loc["dia", "fatal"]
    marginal_night = both.loc["noche", "fatal"]
    assert np.isclose(difference.efecto, marginal_night.efecto - marginal_day.efecto)
    assert not np.isclose(difference.ee**2, marginal_night.ee**2 + marginal_day.ee**2)
    empty = both.loc["hora_desconocida", "fatal"]
    assert empty.estado == "sin_registros" and pd.isna(empty.ic_inf)
    first_counts = frequencies.query("base == '-2' and tramo == '1–7'")
    assert first_counts.groupby("tratado").choques.sum().tolist() == [14, 42]


def coverage_and_isolation():
    keys = ["01001", "02001", "03001", "04001", "05001", "06001"]
    dates = pd.date_range("2021-01-01", "2021-08-01")
    frame = pd.MultiIndex.from_product([keys, dates], names=["clave", "fecha"]).to_frame(index=False)
    day = pd.Timestamp("2021-06-15")
    no_report = frame.clave.isin(["02001", "03001", "04001"]) & frame.fecha.ge(day)
    frame["continuidad"] = ~no_report
    frame["accidentes"] = np.where(no_report, np.nan, 1.0)
    matrix = Matrix(frame)
    months = frame.loc[frame.continuidad & ~(frame.clave.eq("03001") & frame.fecha.dt.month.eq(3))]
    invalid = pd.DataFrame({"clave": ["04001"], "anio": [2021], "mes": [6]})
    flags = monthly_flags(matrix, months, invalid)
    events = pd.DataFrame([
        ("A", "01001", "01", day, day, "confirmado", "extensa"),
        ("B", "05001", "05", day + pd.Timedelta(days=1), day + pd.Timedelta(days=1), "confirmado", "extensa"),
    ], columns=["id_episodio", "clave", "cve_ent", "inicio", "fin", "estado", "clase_final"])
    design = dict(anticipation=1, pre=14, horizon=15, scale_days=14, washout=21,
                  min_controls=1, min_control_states=1)
    audited, _ = comparison(matrix, events, design, "principal")
    assert set(audited.loc[audited.indice.eq(day), "clave"]) == {"01001", "06001"}
    predicted, published = select(matrix, events, design, flags)
    assert set(predicted.loc[predicted.indice.eq(day), "clave"]) == {"01001", "02001", "06001"}
    assert published.extract(predicted.loc[predicted.indice.eq(day) & predicted.clave.eq("02001")], 0).item() == 0
    combined, _ = select(matrix, events, design, flags, end_at_start=True)
    assert set(combined.loc[combined.indice.eq(day), "clave"]) == {"01001", "02001", "05001", "06001"}
    assert np.isnan(matrix.values[matrix.keys.get_loc("02001"), matrix.dates.get_loc(day)])


def run():
    cuts_and_join()
    weights_and_support()
    models_and_wald()
    hourly_and_severity()
    hourly_cross_effects()
    coverage_and_isolation()

"""Small end-to-end case for the preparation and repeated-event estimators."""
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import numpy as np
import pandas as pd

from choques.panel import run as prepare
from choques.modelos import Matrix, comparison, fit, regression, run as estimate
from choques.descarga import hash_file
from choques.consolidacion import run as consolidate
from choques.persistente import run as persistent
from choques.graficas import weekly_figure
import json

EVENT = ["id_episodio", "id_fila", "entidad", "municipio", "clave", "inicio", "fin",
         "precision_fecha", "precision_lugar", "descripcion", "clase_propuesta",
         "clase_final", "lugares", "estado", "motivo"]
SOURCE = ["id_fila", "url", "titulo", "medio", "publicacion", "consulta", "origen",
          "fecha_hecho", "evidencia"]


def fixture_event(key, day, event, state="Aguascalientes", cls="extensa"):
    return [event, f"{event}-{key}", state, key, key, day, day, "día", "municipio",
            "Ejemplo sintético", cls, cls, "tres lugares", "confirmado", "fixture"]


def preparation_check(root):
    paths = {key: root / "data" / key for key in ("inputs", "outputs", "interim", "processed", "raw")}
    paths["tasks"] = root / "tasks"
    paths["raw"].mkdir(parents=True)
    paths["inputs"].mkdir()
    municipal = "CVEGEO,CVE_ENT,CVE_MUN,NOM_MUNICIPIO\n01001,01,001,Aguascalientes\n01002,01,002,Asientos\n"
    columns = "COBERTURA,CVEGEO,CVE_ENT,CVE_MUN,ANIO,MES,ID_DIA,CLASACC,ESTATUS\n"
    records = "".join(f"Municipal,01001,01,001,2020,{i:02},01,No fatal,Cifras Definitivas\n"
                      for i in range(1, 6))
    records += ("Municipal,01001,01,001,2020,04,01,No fatal,Cifras Definitivas\n"
                "Municipal,01001,01,001,2020,02,29,No fatal,Cifras Definitivas\n"
                "Municipal,01001,01,001,2020,05,32,No fatal,Cifras Definitivas\n"
                "Municipal,01001,01,001,2021,04,01,No fatal,Cifras Definitivas\n"
                "Municipal,01002,01,002,2020,04,01,No fatal,Cifras Definitivas\n"
                "Municipal,01002,01,002,2020,99,01,No fatal,Cifras Definitivas\n")
    records += "".join(f"Municipal,01002,01,002,2020,{i:02},01,No fatal,Cifras Definitivas\n"
                       for i in range(1, 4))
    with ZipFile(paths["raw"] / "ejemplo.zip", "w") as archive:
        archive.writestr("catalogos/tc_municipio.csv", municipal)
        archive.writestr("diccionario_de_datos/diccionario.csv",
                         "COLUMNA\n" + columns.strip().replace(",", "\n") + "\n")
        archive.writestr("conjunto_de_datos/atus_anual_2020.csv", columns + records)
    raw = paths["raw"] / "ejemplo.zip"
    manifest = pd.DataFrame([{"fuente": "atus", "archivo": raw.name,
                              "sha256": hash_file(raw)}])
    manifest.to_csv(
        paths["raw"] / "manifiesto.csv", index=False)
    date = "2020-04-01"
    catalog = pd.DataFrame([fixture_event("01001", date, "E1")], columns=EVENT)
    catalog["municipio"] = "Aguascalientes"
    catalog.to_csv(paths["inputs"] / "episodios.csv", index=False)
    sources = [[f"E1-01001", f"https://example.org/{x}", "Ejemplo", x, date, date, x, date, "Texto"]
               for x in ("primero", "segundo")]
    pd.DataFrame(sources, columns=SOURCE).to_csv(paths["inputs"] / "fuentes_eventos.csv", index=False)
    config = {"root": root / "repo", "paths": paths, "atus": {"first": 2020, "last": 2020}}
    prepare(config)
    panel = pd.read_parquet(paths["processed"] / "panel_diario.parquet")
    values = panel.set_index(["clave", "fecha"])
    assert len(panel) == 2 * 366 and not values.index.has_duplicates
    assert values.loc[("01001", pd.Timestamp(date)), "accidentes"] == 2
    assert values.loc[("01001", pd.Timestamp("2020-02-29")), "accidentes"] == 1
    assert values.loc[("01001", pd.Timestamp("2020-04-02")), "accidentes"] == 0
    assert pd.isna(values.loc[("01002", pd.Timestamp("2020-04-02")), "accidentes"])
    assert values.loc[("01001", pd.Timestamp(date)), "inicios"] == "E1"
    assert pd.read_csv(paths["outputs"] / "tablas" / "calidad.csv").query("metrica == 'fecha_invalida'")["n"].sum() == 2
    assert pd.read_csv(paths["outputs"] / "tablas" / "calidad.csv").query("metrica == 'fuera_anio'")["n"].sum() == 1

    saved_panel = paths["processed"] / "panel_diario.parquet"
    before_panel = hash_file(saved_panel)
    catalog_file = paths["inputs"] / "episodios.csv"
    source_file = paths["inputs"] / "fuentes_eventos.csv"
    source_bytes = source_file.read_bytes()
    catalog_bytes = catalog_file.read_bytes()
    valid_sources = pd.DataFrame(sources, columns=SOURCE)

    manifest.assign(sha256="0" * 64).to_csv(paths["raw"] / "manifiesto.csv", index=False)
    rejected(lambda: prepare(config), "SHA-256")
    manifest.to_csv(paths["raw"] / "manifiesto.csv", index=False)

    catalog.assign(municipio="Irapuato").to_csv(catalog_file, index=False)
    rejected(lambda: prepare(config), "Nombre municipal")
    catalog_file.write_bytes(catalog_bytes)

    duplicated = valid_sources.copy()
    duplicated.loc[1, "url"] = "http://www.example.org/primero/?utm_source=prueba#p"
    duplicated.to_csv(source_file, index=False)
    rejected(lambda: prepare(config), "misma URL")
    future = valid_sources.copy()
    future.loc[0, "publicacion"] = "2020-03-31"
    future.to_csv(source_file, index=False)
    rejected(lambda: prepare(config), "anterior al hecho")
    source_file.write_bytes(source_bytes)
    assert hash_file(saved_panel) == before_panel

    sheets = paths["tasks"] / "busqueda-eventos" / "evidencia"
    sheets.mkdir(parents=True)
    (sheets / "prueba-episodios.csv").write_bytes(catalog_bytes)
    (sheets / "prueba-fuentes.csv").write_bytes(source_bytes.replace(b"E1-01001", b"no-existe"))
    rejected(lambda: consolidate(config), "Vínculo")
    assert catalog_file.read_bytes() == catalog_bytes and source_file.read_bytes() == source_bytes
    (sheets / "prueba-fuentes.csv").write_bytes(source_bytes)
    (sheets / "prueba-episodios.csv").write_bytes(catalog_bytes.replace(b",Aguascalientes,01001,", b",Irapuato,01001,"))
    rejected(lambda: consolidate(config), "Nombre municipal")
    assert catalog_file.read_bytes() == catalog_bytes and source_file.read_bytes() == source_bytes
    (sheets / "prueba-episodios.csv").write_bytes(catalog_bytes)
    consolidate(config)

    exposures = paths["processed"] / "exposiciones.parquet"
    release = dict(sha256={"data/processed/panel_diario.parquet": before_panel,
                           "data/processed/exposiciones.parquet": hash_file(exposures)})
    release_folder = paths["tasks"] / "revision-auditoria"
    release_folder.mkdir()
    (release_folder / "revision_auditada.json").write_text(json.dumps(release), encoding="utf-8")
    # A change in outcomes with the same coordinates and coverage must fail before selection.
    panel.loc[panel.clave.eq("01001") & panel.fecha.eq(date), "accidentes"] += 77
    panel.to_parquet(saved_panel, index=False)
    rejected(lambda: estimate(config), "panel_diario.parquet")
    assert not (paths["outputs"] / "modelos" / "muestra.csv").exists()



def eligibility_check():
    days = pd.date_range("2021-01-01", "2021-05-01")
    keys = ["01001", "02001", "03001", "04001", "05001", "06001", "07001", "08001"]
    p = pd.MultiIndex.from_product([keys, days], names=["clave", "fecha"]).to_frame(index=False)
    p["accidentes"] = 1.0
    p["continuidad"] = True
    p.loc[(p.clave == "06001") & p.fecha.eq("2021-03-06"), "accidentes"] = np.nan
    p.loc[p.clave.isin(["02001", "04001", "05001"]) & p.fecha.ge("2021-03-01"), "accidentes"] = 101
    p.loc[p.clave.eq("01001") & p.fecha.ge("2021-03-01"), "accidentes"] = 3
    p.loc[p.fecha.ge("2021-04-10") & ~p.clave.eq("01001"), "accidentes"] = np.nan
    events = pd.DataFrame([fixture_event("01001", "2021-03-01", "E1"),
                           fixture_event("01001", "2021-04-10", "E2"),
                           fixture_event("03001", "2021-03-01", "E1", "Baja California Sur"),
                           fixture_event("04001", "2021-02-14", "Prev", "Campeche", "menor"),
                           fixture_event("05001", "2021-03-17", "Next", "Coahuila de Zaragoza", "menor"),
                           fixture_event("02001", "2021-03-02", "Other", "Baja California", "menor"),
                           fixture_event("03001", "2021-02-14", "Prev", "Baja California Sur", "menor")],
                          columns=EVENT)
    events["inicio"] = pd.to_datetime(events["inicio"])
    events["fin"] = pd.to_datetime(events["fin"])
    events["cve_ent"] = events["clave"].str[:2]
    design = dict(anticipation=1, pre=8, horizon=15, washout=14,
                  min_controls=1, min_control_states=1)
    matrix = Matrix(p)
    sample, diag = comparison(matrix, events, design, "principal")
    assert set(sample.clave) == {"01001", "07001", "08001"}
    assert list(sample["indice"].unique()) == [pd.Timestamp("2021-03-01")]
    assert diag["tratados_otro_episodio"].sum() >= 1 and diag["controles_cobertura"].sum() >= 1
    assert diag.loc[diag["indice"].eq(pd.Timestamp("2021-04-10")), "incluida"].item() == False
    assert abs(fit(matrix, sample, 0, design)["efecto"] - 2) < 1e-12
    p.loc[p.clave.eq("01001"), "accidentes"] = 1.0
    assert abs(fit(Matrix(p), sample, 15, design)["efecto"]) < 1e-12


def regression_check():
    records = []
    for index, counts in enumerate([(1, 4), (3, 2)]):
        n_t, n_c = counts
        for i in range(n_t + n_c):
            treated = int(i < n_t)
            records.append((index, str(i % 4), treated, 1 if treated else n_t / n_c,
                            1 + index + treated * [2, 6][index]))
    example = pd.DataFrame(records, columns=["indice", "estado", "tratado", "peso", "delta"])
    assert abs(regression(example, {})["efecto"] - 5) < 1e-12

    records = []
    rng = np.random.default_rng(402)
    for index in range(8):
        for state in range(5):
            for muni in range(3):
                role = int((state + muni + index) % 5 < 2)
                delta = (3 + index / 5 + role * (1 + 0.9 * state + 0.3 * index)
                         + rng.normal(scale=0.15))
                records.append((index, str(state), role, 1 + 0.3 * (state + muni), delta))
    frame = pd.DataFrame(records, columns=example.columns)
    fixed = pd.get_dummies(frame.indice, dtype=float).to_numpy()
    design = np.column_stack([frame.tratado, fixed])
    weights = frame.peso.to_numpy()
    bread = np.linalg.inv(design.T @ (design * weights[:, None]))
    coefficients = bread @ design.T @ (weights * frame.delta.to_numpy())
    scores = design * (weights * (frame.delta - design @ coefficients)).to_numpy()[:, None]

    def variance(groups):
        grouped = pd.DataFrame(scores).groupby(groups).sum().to_numpy()
        return (bread @ grouped.T @ grouped @ bread)[0, 0]

    v1 = variance(frame.estado)
    v2 = variance(frame.indice)
    v12 = variance([frame.estado, frame.indice])
    n = len(frame)
    correction = 5 / 4 * (n - 1) / (n - design.shape[1])
    fitted = regression(frame, {})
    assert np.isclose(fitted["efecto"], coefficients[0], atol=1e-12)
    assert np.isclose(fitted["ee"]**2, correction * v1, atol=1e-12)
    assert np.isclose(fitted["ee_doble"]**2, correction * (v1 + v2 - v12), atol=1e-12)
    assert fitted["gl"] == fitted["gl_doble"] == 4
    return fitted


def adoption_check():
    import pyfixest as pf

    panel = pd.DataFrame(
        [(i, d, 3 if i < 2 else 0, i + d + (4 + i) * (i < 2 and d >= 3))
         for i in range(6) for d in range(1, 6)],
        columns=["unit", "day", "cohort", "y"])
    lpdid = pf.lpdid(panel.copy(), yname="y", idname="unit", tname="day",
                     gname="cohort", vcov="hetero", pre_window=0, post_window=0, att=False)
    sample = pd.DataFrame(dict(indice=3, estado=panel.unit.unique().astype(str),
                               tratado=[1, 1, 0, 0, 0, 0], peso=[1, 1, 0.5, 0.5, 0.5, 0.5],
                               delta=[5, 6, 1, 1, 1, 1]))
    fitted = regression(sample, {})
    assert np.isclose(fitted["efecto"], lpdid.tidy().loc["time_to_treatment::0", "Estimate"])


def rejected(operation, message):
    try:
        operation()
    except ValueError as err:
        assert message in str(err), str(err)
    else:
        raise AssertionError(f"Se esperaba rechazo con {message}")


def simultaneous_check():
    dates = pd.date_range("2020-01-01", "2020-12-31")
    keys = ["01001", "01002", "05001", "06001"]
    frame = pd.MultiIndex.from_product([keys, dates], names=["clave", "fecha"]).to_frame(index=False)
    day = pd.Timestamp("2020-06-04")
    frame["accidentes"] = 1.0
    frame["continuidad"] = True
    frame.loc[frame.clave.eq("01001") & frame.fecha.eq(day), "accidentes"] += 2
    frame.loc[frame.clave.eq("01002") & frame.fecha.eq(day), "accidentes"] += 100
    event = pd.DataFrame([
        ("A", "01001", "01", day, day, "confirmado", "extensa"),
        ("B", "01002", "01", day, day, "confirmado", "extensa"),
        ("A", "", "01", day, day, "pendiente", "incierta"),
    ], columns=["id_episodio", "clave", "cve_ent", "inicio", "fin", "estado", "clase_final"])
    design = dict(anticipation=1, pre=14, horizon=15, washout=21,
                  min_controls=1, min_control_states=1)
    matrix = Matrix(frame)
    sample, _ = comparison(matrix, event, design, "principal")
    assert set(sample.loc[sample.tratado.eq(1), "clave"]) == {"01001"}
    assert set(sample.loc[sample.tratado.eq(0), "clave"]) == {"05001", "06001"}
    assert abs(fit(matrix, sample, 0, design)["efecto"] - 2) < 1e-12


def weekly_check(output):
    onset = pd.Timestamp("2024-09-09")
    dates = pd.date_range(onset - pd.Timedelta(weeks=25), onset + pd.Timedelta(days=76))
    keys = ["25006", "25019"] + [f"{state:02}001" for state in range(1, 13)]
    frame = pd.MultiIndex.from_product([keys, dates], names=["clave", "fecha"]).to_frame(index=False)
    frame["accidentes"] = 1.0
    frame["continuidad"] = True
    events = pd.DataFrame({
        "inicio": pd.to_datetime([]), "fin": pd.to_datetime([]),
        "clase_final": pd.Series(dtype=str), "clave": pd.Series(dtype=str),
        "cve_ent": pd.Series(dtype=str),
    })
    cfg = dict(onset=str(onset.date()), boundary="2024-11-01",
               train_first=-25, train_last=-10, base=-2, neighbors=12, placebos=12)
    persistent(Matrix(frame), events, {"culiacan": cfg}, output)
    support = pd.read_csv(output / "culiacan_soporte.csv").iloc[0]
    assert support.comparadores_elegibles == support.comparadores_usados == 12
    assert pd.read_csv(output / "culiacan_placebos.csv").rol.tolist() == ["tratado"]
    series = pd.read_csv(output / "culiacan.csv").set_index("semana")
    assert series.loc[6, "tratado"] == 7 and series.loc[7, "tratado"] == 10
    assert series.loc[7, "brecha"] == 3 and np.isnan(series.loc[-1, "brecha"])

    truncated = frame[frame.fecha.ge(onset - pd.Timedelta(weeks=23))]
    persistent(Matrix(truncated), events, {"culiacan": cfg}, output)
    support = pd.read_csv(output / "culiacan_soporte.csv").iloc[0]
    assert support.comparadores_usados == 0
    series = pd.DataFrame(dict(semana=[-2, 0], tratado=[123, 246], brecha=[np.nan, np.nan]))
    fig = weekly_figure(series, cfg)
    ax = fig.axes[0]
    assert "Sin comparadores" in ax.get_title()
    assert not any(123 in line.get_ydata() or 246 in line.get_ydata() for line in ax.lines)
    assert not any(len(line.get_xdata()) > 2 for line in ax.lines)
    series["brecha"] = [0, 1]
    fig = weekly_figure(series, cfg)
    line = fig.axes[0].lines[0]
    assert list(line.get_xdata()) == [-2, -1, 0] and np.isnan(line.get_ydata()[1])

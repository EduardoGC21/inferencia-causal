import json
from zipfile import ZipFile

import numpy as np
import pandas as pd

from .fuentes import manifest, verify
from .panel import atomic_parquet


CENSUS = {2015: "2015-03-15", 2020: "2020-03-15"}
ECONOMIC = {year: f"{year}-12-31" for year in (2018, 2023)}
VEHICLES = {year: f"{year}-12-31" for year in range(2018, 2025)}
# Reference time governs selection. The source's map may come from a different date.
MAP_DATES = {
    "censo": {2015: "2015-03-15", 2020: "2020-12-31"},
    "saic": {2018: "2019-12-31", 2023: "2024-12-31"},
    "vmrc": VEHICLES,
    "conapo": {year: "2022-12-31" for year in VEHICLES},
}
FRONTERA_NORTE = {"02", "05", "08", "19", "26", "28"}


def choose_cut(index, cuts, lag):
    deadline = index - pd.Timedelta(days=lag)
    return max((year for year, date in cuts.items() if pd.Timestamp(date) < deadline), default=None)


def numeric(values, confidential_blank=False):
    text = values.astype("string").str.strip()
    confidential = text.isin(["*", "**", "C", "CONFIDENCIAL"])
    blank = text.isna() | text.eq("")
    if confidential_blank:
        confidential |= blank
    missing = blank | text.isin(["N/D", "ND", "N.D.", "N/A", "-", "—", "NS", "N.S."])
    numbers = pd.to_numeric(text.mask(missing | confidential), errors="raise").astype(float)
    status = np.select([confidential.to_numpy(bool), missing.to_numpy(bool), numbers.eq(0).to_numpy(bool)],
                       ["confidencial", "faltante", "cero"], default="observado")
    return numbers, status


def join_cut(target, source, fields, label, state_only=()):
    source = source[["clave", "territorio", *fields]].rename(columns={"territorio": "_source_territory"})
    if source.clave.duplicated().any():
        raise ValueError(f"Claves municipales duplicadas en {label}")
    result = target.merge(source, on="clave", how="left", validate="many_to_one", indicator="_union")
    found = result._union.eq("both")
    compatible = result.territorio.eq(result._source_territory)
    state = result.clave.str[:2].isin(state_only)
    result[f"{label}_union"] = np.select([found & compatible, found, state],
                                        ["unida", "territorio_incompatible", "solo_entidad"],
                                        default="sin_clave")
    result[fields] = result[fields].where(found & compatible, axis=0)
    return result.drop(columns=["_source_territory", "_union"])


def codes(series, width):
    return series.astype("string").str.strip().str.extract(rf"^(\d{{{width}}})(?:\s|$)", expand=False)


def territorial_changes(path):
    frame = pd.read_csv(path, dtype=str, encoding="cp1252")
    changes = pd.DataFrame({
        "origen": frame.CVE_ENT_ORI + frame.CVE_MUN_ORI,
        "destino": frame.CVE_ENT_ACT + frame.CVE_MUN_ACT,
        "fecha": pd.to_datetime(frame.FECHA_ACT),
        "codigo": frame.CGO_ACT, "descripcion": frame.DESCRIP,
    }).drop_duplicates()
    if not changes.codigo.isin(["M", "W"]).all():
        raise ValueError("Revisar un tipo nuevo de equivalencia municipal")
    return changes.sort_values(["fecha", "origen", "destino"]).reset_index(drop=True)


def territories(keys, date, changes, atus=False):
    if date is None:
        return pd.Series("sin_corte", index=keys.index)
    borders = changes.loc[changes.codigo.eq("M")]
    effective = borders.fecha
    if atus:
        sinaloa = borders.destino.isin(["25019", "25020"])
        effective = effective.mask(sinaloa, pd.Timestamp("2024-11-01"))
    current = borders.loc[effective.le(pd.Timestamp(date))]
    by_key = pd.concat([current.set_index(key).fecha for key in ("origen", "destino")])
    latest = by_key.groupby(level=0).max().dt.strftime("%Y-%m-%d")
    return keys.map(latest).astype("string").fillna("inicial")


def eic(raw):
    populations, households = [], []
    for state in range(1, 33):
        prefix = f"eic-{state:02}"
        p = pd.read_excel(raw / f"{prefix}-poblacion.xls", "02", header=None, usecols=range(5))
        p = p.loc[p[2].eq("Total") & p[3].eq("Valor") & codes(p[1], 3).notna()]
        v = pd.read_excel(raw / f"{prefix}-vivienda.xls", "22", header=None, usecols=range(6))
        v = v.loc[v[2].eq("Automóvil") & v[3].eq("Valor") & codes(v[1], 3).notna()]
        if p.empty or v.empty:
            raise ValueError(f"No se encontró el total municipal en {prefix}")
        populations.append(pd.DataFrame({"clave": codes(p[0], 2) + codes(p[1], 3), "poblacion": p[4]}))
        households.append(pd.DataFrame({"clave": codes(v[0], 2) + codes(v[1], 3),
                                        "viviendas": v[4], "porcentaje_auto": v[5]}))
    data = pd.concat(populations).merge(pd.concat(households), on="clave", how="outer", validate="one_to_one")
    data["poblacion"], data["poblacion_estado"] = numeric(data.poblacion)
    data["viviendas"], data["viviendas_estado"] = numeric(data.viviendas)
    fraction, data["auto_vivienda_estado"] = numeric(data.porcentaje_auto)
    data["auto_vivienda"] = fraction / 100
    return data.drop(columns="porcentaje_auto").assign(anio=2015)


def iter_census(path):
    with ZipFile(path) as archive:
        member = next(n for n in archive.namelist() if n.endswith("conjunto_de_datos_iter_00CSV20.csv"))
        data = pd.read_csv(archive.open(member), dtype=str,
                           usecols=["ENTIDAD", "MUN", "LOC", "POBTOT", "VPH_AUTOM", "VIVPARH_CV"])
    totals = data.loc[data.LOC.eq("0000") & data.MUN.ne("000") & data.ENTIDAD.ne("00")].copy()
    pop, pop_status = numeric(totals.POBTOT)
    housing, housing_status = numeric(totals.VIVPARH_CV)
    auto, auto_status = numeric(totals.VPH_AUTOM)
    return pd.DataFrame(dict(clave=totals.ENTIDAD + totals.MUN, anio=2020, poblacion=pop,
                             poblacion_estado=pop_status, viviendas=housing, viviendas_estado=housing_status,
                             viviendas_con_auto=auto, auto_vivienda=auto / housing.where(housing.gt(0)),
                             auto_vivienda_estado=auto_status))


def economics(raw):
    rows = []
    for state in range(1, 33):
        original = json.loads((raw / f"saic-{state:02}.json").read_bytes())
        for row in json.loads(original["data"])["info"]:
            if row["actividad"] != "Total municipal" or len(row["zxc"]) != 1:
                raise ValueError("El tabulado SAIC debe contener sólo totales municipales")
            fields = {key.split("|", 1)[0]: value for key, value in row["zxc"][0].items()}
            rows.append((row["enti"][:2] + row["muni"][:3], int(row["anio"]), fields["H001A"], fields["A131A"]))
    frame = pd.DataFrame(rows, columns=["clave", "anio", "empleo", "vacb_millones"])
    for field in ("empleo", "vacb_millones"):
        frame[field], frame[f"{field}_estado"] = numeric(frame[field], confidential_blank=True)
    frame["vacb_millones_2023"] = frame.vacb_millones * frame.anio.map({2018: 1.26412683998505, 2023: 1.0})
    return frame


def vehicles(path):
    samples = []
    with ZipFile(path) as archive:
        for year in VEHICLES:
            member = f"conjunto_de_datos/vmrc_anual_tr_cifra_{year}.csv"
            data = pd.read_csv(archive.open(member), dtype=str, keep_default_na=False,
                               usecols=["ANIO", "CVEGEO", "CVE_ENT", "CVE_MUN", "AUTO_PARTICULAR",
                                        "COBERTURA", "ESTATUS"])
            if not data.ANIO.eq(str(year)).all() or not data.CVEGEO.eq(data.CVE_ENT + data.CVE_MUN).all():
                raise ValueError(f"Claves o año incoherentes en {member}")
            auto, status = numeric(data.AUTO_PARTICULAR)
            frame = pd.DataFrame(dict(clave=data.CVEGEO, anio=year, autos=auto, autos_estado=status,
                                      vmrc_cobertura=data.COBERTURA, vmrc_edicion=data.ESTATUS))
            samples.append(frame)
    return pd.concat(samples, ignore_index=True)


def population_annual(path):
    with ZipFile(path) as archive:
        member = "00_Republica_mexicana/2_Gran_Gedad_00_RM.xlsx"
        with archive.open(member) as stream:
            data = pd.read_excel(stream, usecols=[0, 4, 5, 10])
    data.columns = ["clave", "sexo", "anio", "conapo"]
    data = data.loc[data.anio.isin(VEHICLES)].copy()
    data["clave"] = data.clave.astype(str).str.zfill(5)
    data = data.loc[data.clave.str.fullmatch(r"\d{5}") & ~data.clave.str.endswith("000")]
    if not data.sexo.isin(["HOMBRES", "MUJERES"]).all() or data.duplicated(["clave", "anio", "sexo"]).any():
        raise ValueError("Desglose por sexo duplicado o inesperado en CONAPO")
    totals = data.pivot(index=["clave", "anio"], columns="sexo", values="conapo")
    result = totals.sum(axis=1, min_count=2).rename("conapo").reset_index()
    result["conapo_origen"] = np.where(result.anio.le(2020), "reconstruccion", "proyeccion")
    return result


def prepare(config):
    paths = config["paths"]
    raw = paths["raw"] / "municipios"
    entries = manifest(config["root"])
    for entry in entries:
        verify(raw / entry["archivo"], entry)
    changes = territorial_changes(raw / "equivalencias-municipios.csv")
    censo = pd.concat([eic(raw), iter_census(raw / "iter-2020.zip")], ignore_index=True)
    conapo = population_annual(raw / "conapo-1990-2040.zip")
    vmrc = vehicles(raw / "vmrc-1980-2025.zip")
    saic = economics(raw)
    tables = {"censo": censo, "conapo": conapo, "vmrc": vmrc, "saic": saic}
    for name, table in tables.items():
        if (table.empty or table.duplicated(["clave", "anio"]).any()
                or not table.clave.str.fullmatch(r"\d{5}").all()):
            raise ValueError(f"Claves no únicas o fuera de esquema en {name}")
        if not set(table.anio) == set(MAP_DATES[name]):
            raise ValueError(f"Inventario de años incompleto en {name}")
        parts = []
        for year, rows in table.groupby("anio", sort=True):
            date = MAP_DATES[name][year]
            known_splits = changes.loc[changes.codigo.eq("M") & changes.fecha.le(pd.Timestamp(date))]
            # A parent key alone cannot establish which side of the split the source counted.
            unconfirmed = set(known_splits.loc[~known_splits.destino.isin(rows.clave), "origen"])
            parts.append(rows.assign(territorio=territories(rows.clave, date, changes),
                                     perimetro_confirmado=~rows.clave.isin(unconfirmed)))
        tables[name] = pd.concat(parts, ignore_index=True).sort_values(["anio", "clave"])
    for column, frame in [("poblacion", censo), ("conapo", conapo), ("viviendas", censo)]:
        if frame[column].dropna().le(0).any():
            raise ValueError(f"Denominador no positivo: {column}")
    if not censo.auto_vivienda.dropna().between(0, 1).all() or saic.empleo.dropna().lt(0).any() or vmrc.autos.dropna().lt(0).any():
        raise ValueError("Fracción de vivienda o conteos municipales fuera de rango")
    for name, table in tables.items():
        atomic_parquet(table, paths["processed"] / "municipios" / f"{name}.parquet")
    changes.to_csv(paths["processed"] / "municipios" / "cambios_territoriales.csv", index=False)
    print("Fuentes normalizadas: " + ", ".join(f"{name}={len(table):,}" for name, table in tables.items()))


def load(paths):
    source = paths["processed"] / "municipios"
    tables = {name: pd.read_parquet(source / f"{name}.parquet") for name in MAP_DATES}
    changes = pd.read_csv(source / "cambios_territoriales.csv", dtype={"origen": str, "destino": str},
                          parse_dates=["fecha"])
    return tables, changes


def rates(tables):
    censo, conapo, vmrc, saic = [tables[name] for name in ("censo", "conapo", "vmrc", "saic")]
    municipal = vmrc.vmrc_cobertura.eq("Municipal") & ~vmrc.clave.str[2:].isin(["000", "996", "998", "999"])
    state_aggregates = vmrc.loc[~municipal].copy()
    state_aggregates["estado"] = state_aggregates.clave.str[:2]
    for name, counts, cuts in (("saic", saic, ECONOMIC), ("vmrc", vmrc.loc[municipal], VEHICLES)):
        counts = counts.assign(medicion=pd.to_datetime(counts.anio.map(cuts)))
        if name == "vmrc":
            colima_2023 = counts.clave.str.startswith("06") & counts.anio.eq(2023)
            counts.loc[colima_2023, "medicion"] = pd.Timestamp("2024-04-30")
        parts = []
        for closing, rows in counts.groupby("medicion", sort=True):
            annual = join_cut(rows, conapo.loc[conapo.anio.eq(closing.year)], ["conapo", "conapo_origen"], "conapo")
            annual["anio_denominador"] = closing.year
            census_year = choose_cut(closing, CENSUS, 0)
            census = censo.loc[censo.anio.eq(census_year)].rename(columns={"poblacion": "poblacion_alt"})
            annual = join_cut(annual, census, ["poblacion_alt"], "censo_alt")
            annual["anio_censo_alt"] = census_year
            annual["desfase_censo_dias"] = (closing - pd.Timestamp(CENSUS[census_year])).days
            parts.append(annual)
        table = pd.concat(parts, ignore_index=True)
        numerator, output = ("empleo", "empleo_mil") if name == "saic" else ("autos", "autos_mil")
        table[output] = 1000 * table[numerator] / table.conapo
        table[f"{output}_alt"] = 1000 * table[numerator] / table.poblacion_alt
        table[[output, f"{output}_alt"]] = table[[output, f"{output}_alt"]].where(table.perimetro_confirmado, axis=0)
        if name == "saic":
            table["vacb_pc_2023"] = (table.vacb_millones_2023 * 1e6 / table.conapo).where(table.perimetro_confirmado)
        else:
            table = table.rename(columns={"medicion": "medicion_vmrc"})
        tables[name] = table
    return state_aggregates


def attach(sample, tables, changes, design, state_aggregates):
    specifications = {
        "censo": (CENSUS, ["poblacion", "poblacion_estado", "auto_vivienda", "auto_vivienda_estado"]),
        "saic": (ECONOMIC, ["empleo", "empleo_estado", "empleo_mil", "empleo_mil_alt", "vacb_pc_2023",
                            "vacb_millones_estado"]),
        "vmrc": (VEHICLES, ["autos", "autos_estado", "autos_mil", "autos_mil_alt", "medicion_vmrc"]),
    }
    lag = design["pre"] + design["scale_days"]
    frames = []
    for index, cohort in sample.groupby("indice", sort=True):
        end = index + pd.Timedelta(days=design["horizon"] + design["anticipation"])
        start = index - pd.Timedelta(days=lag)
        territory = territories(cohort.clave, end if design.get("pre_only") else index, changes, atus=True)
        window_ok = territories(cohort.clave, start, changes, atus=True).eq(
            territories(cohort.clave, end, changes, atus=True))
        cohort = cohort.assign(territorio=territory, territorio_ventana=window_ok)
        for name, (cuts, fields) in specifications.items():
            year = choose_cut(index, cuts, lag)
            extras = ["perimetro_confirmado"]
            if name != "censo":
                extras += ["conapo", "conapo_union", "conapo_origen", "anio_denominador",
                           "poblacion_alt", "censo_alt_union", "anio_censo_alt", "desfase_censo_dias"]
            table = tables[name].loc[tables[name].anio.eq(year)].rename(
                columns={field: f"{name}_{field}" for field in extras})
            state_only = set()
            if name == "vmrc":
                state_only = (set(state_aggregates.loc[state_aggregates.anio.eq(year), "estado"])
                              - set(table.clave.str[:2]))
            cohort = join_cut(cohort, table, fields + [f"{name}_{field}" for field in extras], name, state_only)
            cohort[f"corte_{name}"] = year
            crossed = cohort[f"{name}_union"].eq("unida") & ~cohort.territorio_ventana
            cohort.loc[crossed, f"{name}_union"] = "quiebre_en_ventana"
            unconfirmed = cohort[f"{name}_union"].eq("unida") & cohort[f"{name}_perimetro_confirmado"].eq(False)
            cohort.loc[unconfirmed, f"{name}_union"] = "perimetro_no_confirmado"
            cohort[fields] = cohort[fields].where(~(crossed | unconfirmed), axis=0)
        midyear = pd.to_datetime(cohort.vmrc_anio_denominador.astype("Int64").astype("string") + "-07-01")
        late = cohort.vmrc_union.eq("unida") & (cohort.medicion_vmrc.ge(start) | midyear.ge(start))
        cohort.loc[late, ["autos_mil", "autos_mil_alt"]] = np.nan
        cohort.loc[late, "vmrc_union"] = "medicion_posterior"
        frames.append(cohort)
    if not frames:
        raise ValueError("La comparación auditada no produjo fechas para unir")
    return pd.concat(frames, ignore_index=True)


def vehicle_diagnostics(vmrc):
    counts = (vmrc.assign(estado=vmrc.clave.str[:2])
              .groupby(["estado", "anio"]).agg(municipios=("clave", "nunique"), autos=("autos", "sum"))
              .reset_index())
    counts["frontera_norte"] = counts.estado.isin(FRONTERA_NORTE)
    counts["cambio_anual"] = counts.groupby("estado").autos.pct_change()
    return counts

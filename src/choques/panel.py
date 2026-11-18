import pandas as pd

from . import eventos, limpieza


def atomic_parquet(frame, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_suffix(".part")
    frame.to_parquet(partial, index=False, compression="zstd")
    partial.replace(path)


def create(keys, accidents, invalid, certificates, events, first, last):
    dates = pd.date_range(f"{first}-01-01", f"{last}-12-31")
    part = pd.MultiIndex.from_product([keys, dates], names=["clave", "fecha"]).to_frame(index=False)
    daily = accidents.groupby(["clave", "fecha"]).size().rename("filas_registradas").reset_index()
    part = part.merge(daily, on=["clave", "fecha"], how="left", validate="one_to_one")
    part["filas_registradas"] = part.filas_registradas.fillna(0).astype("int32")
    part["periodo"] = part.fecha.dt.to_period("M")
    observed = accidents.assign(periodo=accidents.fecha.dt.to_period("M")).groupby(
        ["clave", "periodo"]).size()
    calendar = pd.period_range(f"{first - 1}-10", f"{last}-12", freq="M")
    coverage = observed.unstack(fill_value=0).reindex(index=keys, columns=calendar, fill_value=0).gt(0)
    history = coverage.T.rolling(4, min_periods=4).sum().T.eq(4)
    supported = history.rename_axis(index="clave", columns="periodo").stack().rename(
        "continuidad").reset_index()
    part = part.merge(supported, on=["clave", "periodo"], how="left", validate="many_to_one")
    unknown_month = invalid.dropna(subset=["mes"])
    unknown_month = unknown_month.loc[unknown_month.mes.between(1, 12)].copy()
    unknown_month["periodo"] = pd.PeriodIndex.from_fields(
        year=unknown_month.anio, month=unknown_month.mes.astype(int), freq="M")
    unknown_month = unknown_month[["clave", "periodo"]].drop_duplicates().assign(dia_invalido=True)
    part = part.merge(unknown_month, on=["clave", "periodo"], how="left", validate="many_to_one")
    # A date code such as day 32 cannot support a certified daily zero in that month.
    part["continuidad"] &= ~part["dia_invalido"].eq(True)
    year_unknown = invalid.loc[~invalid.mes.between(1, 12).fillna(False), ["clave", "anio"]]
    if not year_unknown.empty:
        month_keys = pd.MultiIndex.from_arrays([part.clave, part.fecha.dt.year])
        part["continuidad"] &= ~month_keys.isin(pd.MultiIndex.from_frame(year_unknown))
    cert = certificates.loc[certificates.mes.between(1, 12).fillna(False)].copy()
    cert["periodo"] = pd.PeriodIndex.from_fields(year=cert.anio, month=cert.mes.astype(int), freq="M")
    cert = cert[["clave", "periodo"]].drop_duplicates().assign(certificado=True)
    part = part.merge(cert, on=["clave", "periodo"], how="left", validate="many_to_one")
    certified = part.certificado.eq(True)
    if (certified & part.filas_registradas.gt(0)).any():
        raise ValueError("Certificado cero y accidente en el mismo municipio-mes")
    has_row = part.filas_registradas.gt(0)
    part["accidentes"] = part.filas_registradas.where(has_row | part.continuidad | certified).astype("Int32")
    part["cobertura"] = "desconocida"
    part.loc[part.continuidad, "cobertura"] = "cero_por_continuidad"
    part.loc[certified, "cobertura"] = "cero_certificado"
    part.loc[has_row, "cobertura"] = "positivo"
    part["continuidad"] |= certified
    starts = events.loc[events.clave.ne("") & events.inicio.notna()].groupby(
        ["clave", "inicio"])["id_episodio"].agg(lambda ids: ";".join(sorted(set(ids)))).rename("inicios")
    part = part.merge(starts, left_on=["clave", "fecha"], right_index=True,
                      how="left", validate="one_to_one")
    assert not part.duplicated(["clave", "fecha"]).any() and len(part) == len(keys) * len(dates)
    assert part.filas_registradas.sum() == accidents.fecha.between(dates[0], dates[-1]).sum()
    return part.drop(columns=["periodo", "dia_invalido", "certificado"])


def run(config):
    paths = config["paths"]
    first, last = config["atus"]["first"], config["atus"]["last"]
    names, accidents, invalid, certificates, quality = limpieza.load(paths["raw"], first, last)
    events, sources = eventos.read(paths, names)
    keys = sorted(names)
    atomic_parquet(accidents, paths["interim"] / "atus.parquet")
    atomic_parquet(invalid, paths["interim"] / "fecha_invalida.parquet")
    panel = create(keys, accidents, invalid, certificates, events, first, last)
    atomic_parquet(panel, paths["processed"] / "panel_diario.parquet")
    atomic_parquet(events, paths["processed"] / "exposiciones.parquet")
    observed_starts = panel.inicios.notna().sum()
    named = events.clave.ne("")
    local_starts = events.loc[named & events.inicio.between(f"{first}-01-01", f"{last}-12-31"),
                              ["clave", "inicio"]].drop_duplicates()
    assert observed_starts == len(local_starts)
    quality.extend([dict(anio="", metrica=metric, n=n, denominador=d) for metric, n, d in [
        ("municipios_catalogo", len(keys), len(keys)),
        ("filas_catalogo_georreferenciadas", int(named.sum()), len(events)),
        ("inicios_locales_emparejados", int(observed_starts), len(local_starts)),
        ("referencias_enlazadas", len(sources), len(sources)),
    ]])
    coverage = (panel.assign(anio=panel.fecha.dt.year)
                .groupby(["anio", "cobertura"]).size().reset_index(name="n"))
    coverage["denominador"] = coverage.groupby("anio").n.transform("sum")
    coverage = coverage.rename(columns={"cobertura": "metrica"})
    table = paths["outputs"] / "tablas"
    table.mkdir(parents=True, exist_ok=True)
    pd.concat([pd.DataFrame(quality), coverage]).to_csv(table / "calidad.csv", index=False)
    pd.DataFrame({"anio": range(first, last + 1), "apto_para_preparar": True}).to_csv(
        table / "releases.csv", index=False)
    print(f"Panel reconstruido: {len(panel):,} filas, {len(keys)} claves, {observed_starts} inicios.")

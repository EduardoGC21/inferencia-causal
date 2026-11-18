from zipfile import ZipFile

import pandas as pd

from .descarga import archive_members, hash_file


COLS = {"COBERTURA", "CVEGEO", "CVE_ENT", "CVE_MUN", "ANIO", "MES",
        "ID_DIA", "CLASACC", "ESTATUS"}


def parse_year(frame, year, keys):
    geo = frame["CVEGEO"].isin(keys) & frame["CVEGEO"].eq(frame["CVE_ENT"] + frame["CVE_MUN"])
    correct_year = frame["ANIO"].eq(str(year)).fillna(False)
    day = pd.to_datetime(frame["ANIO"] + "-" + frame["MES"] + "-" + frame["ID_DIA"],
                         format="%Y-%m-%d", errors="coerce")
    accident = frame["CLASACC"].isin(["Fatal", "No fatal", "Sólo daños", "Solo daños"])
    certificate = frame["CLASACC"].str.contains("certificado|sin accidente", case=False, na=False)
    if (~(accident | certificate)).any() or not frame["COBERTURA"].eq("Municipal").all():
        raise ValueError(f"Clase o cobertura no prevista en {year}")
    accepted = geo & correct_year & day.notna() & accident
    observables = pd.DataFrame({
        "clave": frame.CVEGEO, "fecha": day, "anio": year,
        "mes": pd.to_numeric(frame.MES, errors="coerce").astype("Int64"),
        "renglon_csv": frame.index + 2,
    })
    invalid = observables.loc[geo & correct_year & day.isna() & accident]
    zero_months = observables.loc[geo & correct_year & certificate, ["clave", "anio", "mes"]]
    quality = {
        "filas_originales": len(frame), "geo_coincide": int(geo.sum()),
        "geo_no_en_catalogo": int((~geo).sum()),
        "fuera_anio": int((geo & accident & ~correct_year).sum()),
        "fecha_invalida": len(invalid), "certificados_cero": int(certificate.sum()),
        "duplicados_exactos_retenidos": int(frame.duplicated().sum()),
        "accidentes_validos": int(accepted.sum()),
    }
    return observables.loc[accepted], invalid, zero_months, quality


def verified_atus(raw):
    entry = pd.read_csv(raw / "manifiesto.csv", dtype=str).set_index("fuente").loc["atus"]
    path = raw / entry["archivo"]
    if hash_file(path) != entry.get("sha256"):
        raise ValueError(f"El SHA-256 del ZIP de ATUS no coincide con el manifiesto: {path.name}")
    return path


def municipalities(archive):
    catalog = pd.read_csv(archive.open("catalogos/tc_municipio.csv"), dtype=str)
    named = ~catalog.CVE_MUN.isin(["000", "996", "998", "999"])
    named &= catalog.CVEGEO.str.fullmatch(r"\d{5}", na=False)
    names = catalog.loc[named].set_index("CVEGEO").NOM_MUNICIPIO
    if not names.index.is_unique:
        raise ValueError("Claves municipales duplicadas en el catálogo ATUS")
    return names.to_dict()


def load(raw, first, last):
    path = verified_atus(raw)
    members = archive_members(path)
    all_years = list(range(first, last + 1))
    years = ([first - 1] if first - 1 in members else []) + all_years
    if missing := set(all_years) - members.keys():
        raise ValueError(f"CSV de ATUS faltantes: {sorted(missing)}")
    cleaned, unknown, certificates, checks = [], [], [], []
    with ZipFile(path) as archive:
        names = municipalities(archive)
        keys = set(names)
        dic = next(name for name in archive.namelist()
                   if name.startswith("diccionario_de_datos/") and name.endswith(".csv"))
        dictionary = pd.read_csv(archive.open(dic), dtype=str)
        if not COLS <= set(dictionary.COLUMNA):
            raise ValueError("Campos previstos ausentes en diccionario")
        for year in years:
            table = pd.read_csv(archive.open(members[year]), dtype=str)
            if not COLS <= set(table.columns):
                raise ValueError(f"Esquema inesperado de ATUS en {year}")
            rows, bad_day, zeros, quality = parse_year(table, year, keys)
            cleaned.append(rows)
            unknown.append(bad_day)
            certificates.append(zeros)
            checks.extend(dict(anio=year, metrica=metric, n=value,
                               denominador=len(table)) for metric, value in quality.items())
    return (names, pd.concat(cleaned, ignore_index=True),
            pd.concat(unknown, ignore_index=True), pd.concat(certificates, ignore_index=True), checks)

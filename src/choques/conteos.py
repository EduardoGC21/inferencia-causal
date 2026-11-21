from zipfile import ZipFile

import numpy as np
import pandas as pd

from .descarga import archive_members
from .limpieza import verified_atus
from .panel import atomic_parquet


HOURS = ["dia", "noche", "hora_desconocida"]
SEVERITY = ["fatal", "heridos", "danos"]
METRICS = HOURS + SEVERITY
CROSS = {(hour, severity): f"{hour}_{severity}" for hour in HOURS for severity in SEVERITY}


def classes(rows):
    hour = pd.to_numeric(rows.ID_HORA, errors="raise")
    day = hour.between(6, 17)
    night = hour.between(0, 5) | hour.between(18, 23)
    unknown = hour.eq(99)
    severity = rows.CLASACC.map({"Fatal": "fatal", "No fatal": "heridos",
                                "Sólo daños": "danos", "Solo daños": "danos"})
    if not (day | night | unknown).all() or severity.isna().any():
        raise ValueError("Código de hora o clase de gravedad fuera del diccionario de ATUS")
    tagged = rows[["clave", "fecha"]].assign(
        dia=day, noche=night, hora_desconocida=unknown,
        fatal=severity.eq("fatal"), heridos=severity.eq("heridos"), danos=severity.eq("danos"))
    crossed = {name: tagged[hour] & tagged[severity] for (hour, severity), name in CROSS.items()}
    return tagged.assign(**crossed).groupby(["clave", "fecha"])[METRICS + list(CROSS.values())].sum().astype("int32")


def prepare(config):
    paths = config["paths"]
    path = verified_atus(paths["raw"])
    members = archive_members(path)
    accepted = pd.read_parquet(paths["interim"] / "atus.parquet",
                               columns=["clave", "fecha", "anio", "renglon_csv"])
    accepted = accepted.loc[accepted.anio.between(config["atus"]["first"], config["atus"]["last"])]
    summaries = []
    with ZipFile(path) as archive:
        for year, records in accepted.groupby("anio", sort=True):
            fields = pd.read_csv(archive.open(members[year]), dtype=str, usecols=["ID_HORA", "CLASACC"])
            records = records.join(fields, on=records.renglon_csv - 2, validate="one_to_one")
            summaries.append(classes(records))
    by_day = pd.concat(summaries).sort_index()
    panel = pd.read_parquet(paths["processed"] / "panel_diario.parquet",
                            columns=["clave", "fecha", "filas_registradas"],
                            filters=[("filas_registradas", ">", 0)])
    totals = panel.set_index(["clave", "fecha"]).filas_registradas.sort_index()
    if (not by_day.index.equals(totals.index)
            or not by_day[HOURS].sum(axis=1).eq(totals).all()
            or not by_day[SEVERITY].sum(axis=1).eq(totals).all()):
        raise ValueError("Los conteos por hora o gravedad difieren del total diario auditado")
    crossed = by_day[list(CROSS.values())].to_numpy().reshape(-1, len(HOURS), len(SEVERITY))
    if (not np.array_equal(crossed.sum(axis=2), by_day[HOURS].to_numpy())
            or not np.array_equal(crossed.sum(axis=1), by_day[SEVERITY].to_numpy())):
        raise ValueError("El cruce de franja y gravedad difiere de los conteos marginales")
    atomic_parquet(by_day.reset_index(), paths["processed"] / "conteos_diarios.parquet")
    print(f"Conteos por hora, gravedad y su cruce reconciliados en {len(by_day):,} municipio-días con registros.")

from collections.abc import Mapping
import unicodedata
from urllib.parse import parse_qsl, urlsplit

import pandas as pd


STATE_NAMES = (
    "Aguascalientes;Baja California;Baja California Sur;Campeche;Coahuila de Zaragoza;"
    "Colima;Chiapas;Chihuahua;Ciudad de México;Durango;Guanajuato;Guerrero;Hidalgo;"
    "Jalisco;México;Michoacán de Ocampo;Morelos;Nayarit;Nuevo León;Oaxaca;Puebla;"
    "Querétaro;Quintana Roo;San Luis Potosí;Sinaloa;Sonora;Tabasco;Tamaulipas;"
    "Tlaxcala;Veracruz de Ignacio de la Llave;Yucatán;Zacatecas"
).split(";")


def normalized(value):
    return "".join(c for c in unicodedata.normalize("NFD", value.casefold().strip())
                   if not unicodedata.combining(c))


STATE_CODES = {normalized(name): f"{index:02}" for index, name in enumerate(STATE_NAMES, 1)}
STATE_CODES.update({"coahuila": "05", "edomex": "15", "estado de mexico": "15",
                    "michoacan": "16", "veracruz": "30", "cdmx": "09"})


def source_address(url):
    parts = urlsplit(url.strip())
    if parts.scheme not in {"http", "https"} or not parts.hostname:
        raise ValueError(f"Vínculo a fuente inválido: {url}")
    query = tuple(sorted((key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True)
                         if not key.casefold().startswith("utm_")))
    return parts.hostname.removeprefix("www.").rstrip("."), parts.port, parts.path.rstrip("/"), query


def read(paths, keys=None):
    events = pd.read_csv(paths["inputs"] / "episodios.csv", dtype=str, keep_default_na=False)
    sources = pd.read_csv(paths["inputs"] / "fuentes_eventos.csv", dtype=str, keep_default_na=False)
    for col in ("inicio", "fin"):
        events[col] = pd.to_datetime(events[col].replace("", None), format="%Y-%m-%d")
    named = events["clave"].ne("")
    confirmed = events["estado"].eq("confirmado")
    events["cve_ent"] = events["entidad"].map(lambda x: STATE_CODES.get(normalized(x)))
    if events.id_fila.duplicated().any() or events.loc[named].duplicated(["id_episodio", "clave"]).any():
        raise ValueError("Catálogo con identificadores duplicados")
    if (events.loc[named, "clave"].str.fullmatch(r"\d{5}").eq(False).any()
            or not events.loc[named, "clave"].str[:2].eq(events.loc[named, "cve_ent"]).all()):
        raise ValueError("Claves geográficas inconsistentes")
    if not events.estado.isin(["confirmado", "pendiente", "excluido"]).all():
        raise ValueError("Estado de verificación desconocido")
    if not events.clase_final.isin(["extensa", "menor", "persistente", "incierta"]).all():
        raise ValueError("Clase de exposición desconocida")
    if (events.inicio.gt(events.fin).any() or events.loc[confirmed, "inicio"].isna().any()
            or events.loc[confirmed & events.clase_final.eq("extensa"), "clave"].eq("").any()
            or (events.fin.isna() & confirmed & events.clase_final.eq("extensa")).any()):
        raise ValueError("Inicio, fin o municipio sin resolución para una jornada confirmada")
    if keys is not None and (missing := set(events.loc[named, "clave"]) - set(keys)):
        raise ValueError(f"Claves fuera del catálogo ATUS: {sorted(missing)}")
    if isinstance(keys, Mapping):
        for row in events.loc[named].itertuples():
            if normalized(row.municipio) != normalized(keys[row.clave]):
                raise ValueError(f"Nombre municipal incompatible con la clave en {row.id_fila}")
    if set(sources.id_fila) != set(events.id_fila):
        raise ValueError("Vínculo a fuente inválido")
    addresses = sources.url.map(source_address)
    if sources.assign(address=addresses).duplicated(["id_fila", "address"]).any():
        raise ValueError("La misma URL se repite para una fila del catálogo")
    dates = sources[["publicacion", "consulta", "fecha_hecho"]].apply(
        lambda col: pd.to_datetime(col.replace("", None), format="%Y-%m-%d"))
    early = dates.publicacion.lt(dates.fecha_hecho)
    if early.any():
        raise ValueError(f"Publicación anterior al hecho en {sources.loc[early, 'id_fila'].iloc[0]}")
    origin_id = sources.origen.map(normalized)
    origins = origin_id[origin_id.ne("")].groupby(sources.id_fila).nunique()
    requires_two = confirmed & events.clase_final.isin(["extensa", "persistente"])
    if events.loc[requires_two, "id_fila"].map(origins).fillna(0).lt(2).any():
        raise ValueError("Jornadas o crisis confirmadas sin dos orígenes documentados")
    return events, sources

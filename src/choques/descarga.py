from concurrent.futures import ThreadPoolExecutor
from datetime import date
from hashlib import file_digest
from pathlib import PurePosixPath
import re
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def hash_file(path):
    with path.open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def archive_members(path):
    with ZipFile(path) as archive:
        return {int(match[1]): member for member in archive.namelist()
                if (match := re.fullmatch(r"atus_anual_(\d{4})\.csv",
                                          PurePosixPath(member.lower()).name))}


def inspect(path, kind):
    if kind == "atus":
        years = archive_members(path)
        with ZipFile(path) as archive:
            names = archive.namelist()
            if (bad := archive.testzip()) is not None:
                raise ValueError(f"CRC incorrecto: {bad}")
        if not years or not any("diccionario" in name.lower() for name in names):
            raise ValueError("Faltan tablas anuales o diccionarios de ATUS")
        return years
    import json
    entries = json.loads(path.read_bytes())["datos"]
    if not {"25006", "25019"} <= {entry["cvegeo"] for entry in entries}:
        raise ValueError("El catálogo geográfico no identifica Culiacán y Eldorado")
    return {}


def transfer(session, url, stream, kind):
    if kind != "atus":
        with session.get(url, stream=True, timeout=(15, 45)) as response:
            response.raise_for_status()
            for block in response.iter_content(chunk_size=1024 * 1024):
                stream.write(block)
        return
    # The official server responds to bounded ranges even when a full GET stalls.
    block_size = 4 * 1024 * 1024
    with session.get(url, headers={"Range": f"bytes=0-{block_size - 1}"},
                     stream=True, timeout=(15, 45)) as first:
        first.raise_for_status()
        if first.status_code == 200:
            for block in first.iter_content(chunk_size=1024 * 1024):
                stream.write(block)
            return
        total = int(first.headers["Content-Range"].split("/")[-1])
        identity = first.headers.get("ETag")
        expected = min(block_size, total)
        if (first.headers["Content-Range"] != f"bytes 0-{expected - 1}/{total}"
                or len(first.content) != expected):
            raise ValueError("Primer rango de ATUS incompleto")
        stream.write(first.content)

    def get_part(start):
        end = min(start + block_size, total) - 1
        headers = {"Range": f"bytes={start}-{end}"}
        if identity is not None:
            headers["If-Range"] = identity
        with session.get(url, headers=headers, stream=True, timeout=(15, 45)) as response:
            response.raise_for_status()
            if (response.status_code != 206
                    or response.headers.get("Content-Range") != f"bytes {start}-{end}/{total}"
                    or response.headers.get("ETag") != identity
                    or len(response.content) != end - start + 1):
                raise ValueError(f"Rango incompleto o cambio de edición en ATUS: {start}-{end}")
            return response.content

    with ThreadPoolExecutor(max_workers=3) as pool:
        for block in pool.map(get_part, range(expected, total, block_size)):
            stream.write(block)


def run(config):
    raw = config["paths"]["raw"]
    raw.mkdir(parents=True, exist_ok=True)
    atus = config["atus"]
    manifest = raw / "manifiesto.csv"
    prior = pd.read_csv(manifest, dtype=str).set_index("fuente") if manifest.exists() else None
    rows = []
    targets = [
        ("atus", "atus-" + atus["version"] + ".zip", atus["url"], atus["version"]),
        ("geo_sinaloa", "geo-sinaloa.json", "https://gaia.inegi.org.mx/wscatgeo/v2/mgem/25",
         "Catálogo Único, áreas municipales de Sinaloa, consulta fechada"),
    ]
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=Retry(
        total=2, backoff_factor=0.7, status_forcelist=[429, 500, 502, 503, 504],
        respect_retry_after_header=False)))
    for kind, filename, url, version in targets:
        previous = prior.loc[kind] if prior is not None and kind in prior.index else None
        if previous is not None and (previous["url"] != url or previous["edicion"] != version):
            previous = None
        path = raw / (previous["archivo"] if previous is not None else filename)
        if previous is not None and path.is_file() and hash_file(path) == previous["sha256"]:
            years = archive_members(path) if kind == "atus" else {}
            row = previous.to_dict()
            print(f"Reutilizado: {path.name}")
        else:
            temporary = None
            try:
                with NamedTemporaryFile(dir=raw, suffix=".part", delete=False) as stream:
                    temporary = raw / PurePosixPath(stream.name.replace("\\", "/")).name
                    transfer(session, url, stream, kind)
                years = inspect(temporary, kind)
                digest = hash_file(temporary)
                if previous is not None and digest != previous["sha256"]:
                    raise ValueError(f"El original remoto cambió ({kind}): {digest}. Revisar edición.")
                if path.exists() and hash_file(path) != digest:
                    path = raw / f"{path.stem}-{digest[:12]}{path.suffix}"
                temporary.replace(path)
                row = dict(archivo=path.name, url=url, consulta=date.today().isoformat(),
                           edicion=version, bytes=path.stat().st_size, sha256=digest,
                           verificacion="SHA-256 local; CRC ZIP" if kind == "atus" else "SHA-256 local; JSON")
                print(f"Descargado: {path.name} ({row['bytes']} bytes)")
            finally:
                if temporary is not None:
                    temporary.unlink(missing_ok=True)
        row["fuente"] = kind
        row["anios_archivo"] = " ".join(map(str, sorted(years)))
        rows.append(row)
    columns = ["archivo", "url", "consulta", "edicion", "bytes", "sha256",
               "verificacion", "fuente", "anios_archivo"]
    pd.DataFrame(rows, columns=columns).to_csv(manifest, index=False)
    requested = set(range(atus["first"], atus["last"] + 1))
    if not requested:
        raise ValueError("El periodo solicitado está vacío")
    available = set(map(int, rows[0]["anios_archivo"].split()))
    years_status = pd.DataFrame(
        [{"anio": year, "publicado": year in available, "descargado": year in available,
          "incidencia": "" if year in available else "No consta en el release verificado"}
         for year in sorted(requested)])
    years_status.to_csv(raw / "anios.csv", index=False)
    print(years_status.to_string(index=False))
    if requested - available:
        raise ValueError(f"Años solicitados ausentes: {sorted(requested - available)}")

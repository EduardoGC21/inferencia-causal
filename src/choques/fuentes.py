import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import NamedTemporaryFile

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .descarga import hash_file


def manifest(root):
    return json.loads((root / "config" / "fuentes_municipales.json").read_text(encoding="utf-8"))


def verify(path, entry):
    if not path.is_file() or hash_file(path) != entry["sha256"]:
        raise ValueError(f"Original ausente o distinto de la edición fijada: {path}")


def download(config):
    raw = config["paths"]["raw"] / "municipios"
    raw.mkdir(parents=True, exist_ok=True)
    entries = manifest(config["root"])

    def acquire(entry):
        target = raw / entry["archivo"]
        if target.exists():
            verify(target, entry)
            return
        with requests.Session() as session:
            session.mount("https://", HTTPAdapter(max_retries=Retry(
                total=2, backoff_factor=0.6, status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods={"GET", "POST"}, respect_retry_after_header=False
            )))
            with NamedTemporaryFile(dir=raw, delete=False) as stream:
                temporary = Path(stream.name)
                try:
                    query = entry.get("consulta")
                    with session.request("POST" if query else "GET", entry["url"], json=query,
                                         stream=True, timeout=(15, 60)) as response:
                        response.raise_for_status()
                        for block in response.iter_content(chunk_size=1024**2):
                            stream.write(block)
                    stream.close()
                    verify(temporary, entry)
                    temporary.replace(target)
                finally:
                    stream.close()
                    temporary.unlink(missing_ok=True)

    with ThreadPoolExecutor(max_workers=6) as pool:
        for number, _ in enumerate(pool.map(acquire, entries), start=1):
            if number % 20 == 0 or number == len(entries):
                print(f"Fuentes municipales verificadas: {number}/{len(entries)}.", flush=True)

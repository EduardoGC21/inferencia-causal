from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import pandas as pd

from .eventos import read
from .limpieza import municipalities, verified_atus


def run(config):
    paths = config["paths"]
    evidence = paths["tasks"] / "busqueda-eventos" / "evidencia"
    inputs = paths["inputs"]
    inputs.mkdir(parents=True, exist_ok=True)
    names = None
    if (paths["raw"] / "manifiesto.csv").is_file():
        with ZipFile(verified_atus(paths["raw"])) as archive:
            names = municipalities(archive)

    with TemporaryDirectory(dir=inputs) as directory:
        stage = Path(directory)
        products = []
        for kind, filename in (("episodios", "episodios.csv"), ("fuentes", "fuentes_eventos.csv")):
            tables = [pd.read_csv(file, dtype=str, keep_default_na=False)
                      for file in sorted(evidence.glob(f"*-{kind}.csv"))]
            merged = pd.concat(tables, ignore_index=True)
            order = ["id_fila"] + (["url"] if kind == "fuentes" else [])
            product = stage / filename
            merged.sort_values(order).to_csv(product, index=False, lineterminator="\n")
            products.append(product)

        events, sources = read(paths | {"inputs": stage}, names)
        prior = {file.name: (inputs / file.name).read_bytes()
                 for file in products if (inputs / file.name).is_file()}
        published = []
        try:
            for file in products:
                file.replace(inputs / file.name)
                published.append(file)
        except OSError:
            for file in published:
                target = inputs / file.name
                if file.name in prior:
                    file.write_bytes(prior[file.name])
                    file.replace(target)
                else:
                    target.unlink()
            raise
    print(f"Catálogo: {len(events)} filas, {events.id_episodio.nunique()} episodios candidatos, "
          f"{len(sources)} vínculos, {sources.url.nunique()} URLs.")


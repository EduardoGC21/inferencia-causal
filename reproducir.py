"""Rebuild the written project from a fresh copy and compare its products."""
from datetime import datetime
import hashlib
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import mkdtemp
from time import perf_counter


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def readable_pdf(root):
    result = subprocess.run(["pdftotext", "-layout", "repo/reporte/main.pdf", "-"], cwd=root,
                            capture_output=True, check=True)
    return result.stdout


def run():
    root = Path(__file__).resolve().parent.parent
    parent = root / "worktrees"
    parent.mkdir(exist_ok=True)
    clean = Path(mkdtemp(prefix="reproduccion-", dir=parent))
    clean_repo = clean / "repo"
    out = root / "data" / "outputs" / "qa"
    out.mkdir(parents=True, exist_ok=True)
    for directory in ("repo/config", "repo/tests", "tasks", "repo/src"):
        shutil.copytree(root / directory, clean / directory,
                        ignore=shutil.ignore_patterns("__pycache__", "*.egg-info"))
    for name in ("repo/README.md", "repo/pyproject.toml", "repo/requirements-lock.txt",
                 "repo/reporte/main.tex", "repo/reporte/referencias.bib"):
        target = clean / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / name, target)
    raw = clean / "data" / "raw"
    raw.mkdir(parents=True)
    for name in ("manifiesto.csv", "geo-sinaloa.json"):
        shutil.copy2(root / "data" / "raw" / name, raw / name)
    for original in (root / "data" / "raw").glob("atus-*.zip"):
        shutil.copy2(original, raw / original.name)

    shutil.copytree(root / "data" / "raw" / "municipios", raw / "municipios")

    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(clean_repo / "src"), env.get("PYTHONPATH")]))
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess.run([sys.executable, "-c",
                    "import choques; from pathlib import Path; "
                    "assert Path(choques.__file__).resolve().is_relative_to(Path.cwd())"],
                   cwd=clean_repo, check=True, env=env)
    stages = ("descargar", "consolidar", "preparar", "validar", "estimar", "analizar",
              "graficar", "compilar")
    measures = []
    with (out / "reproduccion-ejecucion.txt").open("wb") as stream:
        for stage in stages:
            stream.write(f"\n> python -m choques {stage}\n".encode())
            stream.flush()
            start = perf_counter()
            subprocess.run([sys.executable, "-u", "-m", "choques", stage], cwd=clean_repo,
                           env=env, check=True, stdout=stream, stderr=subprocess.STDOUT)
            measures.append((stage, perf_counter() - start))
    compared = []
    for original in sorted((raw / "municipios").iterdir()):
        name = original.relative_to(clean)
        if digest(original) != digest(root / name):
            raise RuntimeError(f"El original municipal copiado difiere: {name}")
    for directory, extensions in (
        ("data/inputs", {".csv"}), ("data/interim", {".parquet"}), ("data/processed", {".parquet"}),
        ("data/processed/municipios", {".parquet", ".csv"}),
        ("data/outputs/modelos", {".csv"}), ("data/outputs/tablas", {".csv", ".tex"}),
        ("data/outputs/figuras", {".pdf", ".png"}),
    ):
        indices = {path.relative_to(root) for path in (root / directory).iterdir()
                   if path.suffix in extensions}
        other = {path.relative_to(clean) for path in (clean / directory).iterdir()
                 if path.suffix in extensions}
        if indices != other:
            raise RuntimeError(f"El inventario regenerado difiere: {directory}")
        for name in sorted(indices):
            if digest(root / name) != digest(clean / name):
                raise RuntimeError(f"El producto regenerado difiere: {name}")
            compared.append(name.as_posix())
    for name in ("data/raw/manifiesto.csv", "data/raw/anios.csv"):
        if digest(root / name) != digest(clean / name):
            raise RuntimeError(f"La procedencia regenerada difiere: {name}")
        compared.append(name)
    validation = "data/outputs/modelos/validacion.md"
    reports = [re.sub(r"Tiempo total [0-9.]+ s", "Tiempo total medido",
                      (path / validation).read_text(encoding="utf-8")) for path in (root, clean)]
    if reports[0] != reports[1]:
        raise RuntimeError("El contenido de la validación sintética difiere")
    if readable_pdf(root) != readable_pdf(clean):
        raise RuntimeError("El texto con paginación del PDF regenerado difiere")
    pdf = digest(root / "repo/reporte/main.pdf") == digest(clean_repo / "reporte/main.pdf")
    markdown = [
        "# Reproducción del escrito en una copia limpia", "",
        f"Fecha local {datetime.now().isoformat(timespec='seconds')}.",
        f"Copia {clean.relative_to(root).as_posix()}. La misma .venv cargó el código de la copia.",
        "La descarga verificó los originales copiados por SHA-256 contra el manifiesto.",
        f"Se regeneraron {len(compared)} productos con SHA-256 idéntico.",
        "El PDF conserva texto, distribución de líneas y saltos de página por pdftotext -layout.",
        f"PDF binario idéntico: {'sí' if pdf else 'no; se verificó la huella de las figuras y el texto paginado'}.",
        "La validación sintética coincide al omitir el tiempo variable de ejecución.",
        "El log completo se guarda en reproduccion-ejecucion.txt.", "",
        "| Etapa | Segundos |", "| --- | ---: |",
        *(f"| {stage} | {seconds:.2f} |" for stage, seconds in measures), "",
        "## Productos cotejados", "",
        *(f"- {item}" for item in compared),
    ]
    (out / "reproduccion.md").write_text("\n".join(markdown) + "\n", encoding="utf-8")
    print(f"Reproducción verificada en {clean}. {len(compared)} productos coinciden.")
    print(measures)


if __name__ == "__main__":
    run()

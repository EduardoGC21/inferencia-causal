import argparse
from importlib import import_module
from pathlib import Path
import tomllib


STAGES = {
    "descargar": ("descarga", "run"),
    "consolidar": ("consolidacion", "run"),
    "preparar": ("panel", "run"),
    "validar": ("validacion", "run"),
    "soporte": ("modelos", "support"),
    "estimar": ("modelos", "run"),
    "analizar": ("analisis", "run"),
    "graficar": ("graficas", "run"),
    "compilar": ("escrito", "run"),
}


def main():
    parser = argparse.ArgumentParser(description="Accidentes registrados y episodios de violencia")
    parser.add_argument("stage", choices=["configuracion", *STAGES, "todo"])
    parser.add_argument("--config", type=Path, default=Path("config/proyecto.toml"))
    parser.add_argument("--fuente", choices=["atus"], default="atus")
    parser.add_argument("--desde", type=int)
    parser.add_argument("--hasta", type=int)
    args = parser.parse_args()
    config = tomllib.loads(args.config.read_text(encoding="utf-8"))
    root = args.config.resolve().parent.parent
    config["root"] = root
    config["paths"] = {key: (root / path).resolve() for key, path in config["paths"].items()}
    if args.stage == "configuracion":
        for key, path in config["paths"].items():
            print(f"{key}: {path}")
        return
    if args.desde is not None:
        config["atus"]["first"] = args.desde
    if args.hasta is not None:
        config["atus"]["last"] = args.hasta
    stages = ("descargar", "preparar", "validar", "estimar", "analizar", "graficar")
    for stage in stages if args.stage == "todo" else (args.stage,):
        module, function = STAGES[stage]
        getattr(import_module(f".{module}", __package__), function)(config)

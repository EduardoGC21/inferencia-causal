import argparse
from importlib import import_module
from pathlib import Path
import tomllib


STAGES = {
    "descargar": [("descarga", "run"), ("fuentes", "download")],
    "consolidar": [("consolidacion", "run")],
    "preparar": [("panel", "run"), ("conteos", "prepare"), ("municipios", "prepare")],
    "validar": [("validacion", "run")],
    "soporte": [("modelos", "support"), ("comparaciones", "support")],
    "estimar": [("modelos", "run"), ("comparaciones", "run"), ("causal", "run")],
    "analizar": [("analisis", "run"), ("causal", "tables")],
    "graficar": [("graficas", "run"), ("causal", "figures")],
    "compilar": [("escrito", "run")],
    "cotejar-panel": [("cotejo_panel", "run")],
}


def main():
    parser = argparse.ArgumentParser(description="Accidentes registrados y episodios de violencia")
    parser.add_argument("stage", choices=["configuracion", *STAGES, "todo"])
    parser.add_argument("--config", type=Path, default=Path("config/proyecto.toml"))
    parser.add_argument("--fuente", choices=["todas", "atus", "municipios"], default="todas")
    parser.add_argument("--desde", type=int)
    parser.add_argument("--hasta", type=int)
    parser.add_argument("--datos", type=Path, help="Carpeta con raw, interim, processed e inputs")
    parser.add_argument("--resultados", type=Path, help="Carpeta de salidas de estimación y reporte")
    parser.add_argument("--arranque", action="store_true", help="Comprueba el panel de Ruta B con una muestra breve")
    parser.add_argument("--anterior", type=Path, help="Modelos anteriores permitidos como referencia de muestra y pesos")
    parser.add_argument("--referencia", type=Path, help="Carpeta de modelos Python del panel diario")
    parser.add_argument("--salida", type=Path, help="Destino del cotejo del panel diario")
    parser.add_argument("--replica-r", type=Path, help="Carpeta de modelos R del panel diario")
    args = parser.parse_args()
    config = tomllib.loads(args.config.read_text(encoding="utf-8"))
    root = args.config.resolve().parent.parent
    config["root"] = root
    config["paths"] = {key: (root / path).resolve() for key, path in config["paths"].items()}
    if args.datos is not None:
        data = args.datos.resolve()
        config["paths"].update({key: data / key for key in ("raw", "interim", "processed", "inputs")})
        config["paths"]["tasks"] = data.parent / "tasks"
    if args.resultados is not None:
        config["paths"]["outputs"] = args.resultados.resolve()
    if args.arranque:
        if args.stage != "estimar":
            parser.error("--arranque requiere estimar")
        from .causal import run
        run(config, smoke=True)
        return
    if args.stage == "cotejar-panel":
        if args.referencia is None or args.salida is None or args.replica_r is None:
            parser.error("cotejar-panel requiere --referencia, --replica-r y --salida")
        from .cotejo_panel import run
        run(args.referencia, args.replica_r, args.salida, args.anterior)
        return
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
        steps = STAGES[stage]
        if args.stage == "descargar" and args.fuente != "todas":
            steps = steps[:1] if args.fuente == "atus" else steps[1:]
        for module, function in steps:
            selected = config
            legacy = root / "config" / "legado.toml"
            if module in ("modelos", "comparaciones", "analisis", "graficas") and legacy.exists():
                selected = config | {"design": tomllib.loads(legacy.read_text(encoding="utf-8"))["design"]}
            getattr(import_module(f".{module}", __package__), function)(selected)

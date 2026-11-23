import os
import shutil
import subprocess


def run(config):
    root = config["root"]
    report = root / "reporte"
    output = config["paths"]["outputs"] / "qa"
    output.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["SOURCE_DATE_EPOCH"] = "1795269600"  # 21/11/2026, fecha de autorización del rediseño.
    env["FORCE_SOURCE_DATE"] = "1"
    latex = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
    with (output / "compilacion.txt").open("wb") as log:
        def compile_step(command):
            log.write(("\n\n> " + " ".join(command) + "\n").encode())
            log.flush()
            subprocess.run(command, cwd=report, check=True, env=env,
                           stdout=log, stderr=subprocess.STDOUT)

        compile_step(latex)
        compile_step(["biber", "main"])
        for attempt in range(5):
            compile_step(latex)
            final = (report / "main.log").read_text(encoding="utf-8", errors="replace")
            if attempt and not any(s in final for s in ("Rerun to get", "undefined references", "undefined citations")):
                break
        else:
            raise ValueError("La compilación no estabilizó las referencias cruzadas")
    shutil.copy2(report / "main.pdf", report / "reporte.pdf")
    print(f"PDF compilado: {report / 'reporte.pdf'}")

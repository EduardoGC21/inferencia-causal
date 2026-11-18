from pathlib import Path
import runpy
from tempfile import TemporaryDirectory
from time import perf_counter

import pyfixest as pf


def run(config):
    start = perf_counter()
    case = runpy.run_path(str(config["root"] / "tests" / "caso_sintetico.py"))
    output = config["paths"]["outputs"] / "modelos"
    output.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output) as directory:
        case["preparation_check"](Path(directory))
        case["weekly_check"](Path(directory))
    case["eligibility_check"]()
    case["simultaneous_check"]()
    result = case["regression_check"]()
    case["adoption_check"]()
    runpy.run_path(str(config["root"] / "tests" / "caso_municipal.py"))["run"]()
    evidence = (
        "# Validación con datos sintéticos\n\n"
        "Comando desde la raíz: python -m choques validar.\n\n"
        f"PyFixest {pf.__version__}. Tiempo total {perf_counter() - start:.2f} s.\n\n"
        "- Preparación: 366 días bisiestos por clave, dos accidentes con campos idénticos "
        "se retienen, un cero con continuidad, un faltante, día inválido, año ajeno y "
        "una exposición enlazada a dos fuentes sin duplicar el panel.\n"
        "- Trazabilidad: rechazo de ZIP o panel alterado, fuente duplicada, nombre y fecha "
        "incompatibles. Una consolidación fallida conserva los insumos anteriores.\n"
        "- Pista estatal: la excepción se aplica al par focal y el efecto conocido es 2.\n"
        "- Culiacán: se exige el calendario previo completo, se aceptan 12 donantes para la "
        "comparación focal y la figura omite la brecha cuando no se puede calcular.\n"
        "- Elegibilidad: control contaminado con cambio de 100, arrastre previo, "
        "anticipación, cobertura incompleta, fecha sin controles y efecto nulo.\n"
        "- Reponderación: ATT de 5 con 1 y 3 tratados y efectos de 2 y 6.\n"
        "- Regresión: matriz explícita de efectos fijos y congruencias con PyFixest en "
        f"coeficiente y correcciones CRV1. EE estado {result['ee']:.10f}, "
        f"GL {result['gl']}; EE estado-fecha {result['ee_doble']:.10f}, "
        f"GL {result['gl_doble']}.\n"
        "- Adopción única: comparación del día cero con pyfixest.lpdid "
        "en una cohorte y controles nunca tratados.\n"
        "- Covariables municipales: cierre estricto, faltantes, confidencialidad y cero; "
        "claves y territorio; soporte y pesos compartidos; vecino 1:1, distancia, cero, "
        "desempate y reutilización; muestra común M0–M3; "
        "regresión ponderada, Wald matricial y conciliación de hora y gravedad.\n"
    )
    (output / "validacion.md").write_text(evidence, encoding="utf-8")
    print(evidence)

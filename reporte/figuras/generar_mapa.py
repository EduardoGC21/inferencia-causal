"""Mapa de referencia del apéndice, con geometría local y muestra ya estimada."""
from pathlib import Path
import argparse
import hashlib
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
from matplotlib.path import Path as MplPath
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent

def project(coordinates):
    # Equirectangular, paralelo 23 N. Sólo representación; no distancias ni áreas.
    xy = np.asarray(coordinates, dtype=float)[:, :2]
    if not np.isfinite(xy).all() or (np.abs(xy[:, 0]) > 180).any() or (np.abs(xy[:, 1]) > 90).any():
        raise ValueError("Coordenadas geográficas no válidas")
    return np.column_stack([(xy[:, 0] + 102) * np.cos(np.deg2rad(23)), xy[:, 1] - 23])


def patches(geometry):
    polygons = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
    if geometry["type"] not in ("Polygon", "MultiPolygon"):
        raise ValueError("Geometría no poligonal")
    answer = []
    for polygon in polygons:
        rings, codes = [], []
        outer_sign = None
        for ring in polygon:
            xy = project(ring)
            if len(xy) < 4 or not np.allclose(xy[0], xy[-1]):
                raise ValueError("Anillo abierto o vacío")
            sign = np.sign(np.sum(xy[:-1, 0] * xy[1:, 1] - xy[1:, 0] * xy[:-1, 1]))
            if outer_sign is None:
                outer_sign = sign
            elif sign == outer_sign:
                xy = xy[::-1]
            rings.extend(xy)
            codes.extend([MplPath.MOVETO] + [MplPath.LINETO] * (len(xy) - 2) + [MplPath.CLOSEPOLY])
        answer.append(PathPatch(MplPath(np.asarray(rings), codes)))
    return answer


def draw(features, main):
    treated = set(main.loc[main.tratado.eq(1), "clave"])
    controls = set(main.loc[main.tratado.eq(0), "clave"])
    shapes = {f["properties"]["cvegeo"]: patches(f["geometry"]) for f in features}
    missing = (treated | controls) - shapes.keys()
    if missing:
        raise ValueError(f"Municipios de la muestra sin geometría: {sorted(missing)}")
    names = {f["properties"]["cvegeo"]: f["properties"]["nomgeo"] for f in features}
    roles = pd.DataFrame([dict(clave=k, municipio=names[k], tratado=k in treated, control=k in controls)
                          for k in sorted(treated | controls)])
    roles.to_csv(OUT / "municipios_roles.csv", index=False)
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 11, "pdf.fonttype": 42, "ps.fonttype": 42}):
        fig, axes = plt.subplots(2, 1, figsize=(12, 13), layout="constrained")
        for ax, keys, color, title in zip(axes, [treated, controls], ["#C9510C", "#1479A6"],
                                          [f"Alguna vez tratados: {len(treated)} municipios", f"Alguna vez controles: {len(controls)} municipios"]):
            background = [p for group in shapes.values() for p in group]
            ax.add_collection(PatchCollection(background, facecolor="#E6EAEC", edgecolor="white", linewidth=.10, rasterized=True))
            selected = [p for key in sorted(keys) for p in shapes[key]]
            ax.add_collection(PatchCollection(selected, facecolor=color, edgecolor=color, linewidth=.45, rasterized=True))
            ax.autoscale_view()
            ax.set_aspect("equal")
            ax.margins(.025)
            ax.set_axis_off()
            ax.set_title(title, weight="bold", fontsize=15, loc="left", pad=9)
        fig.suptitle("Municipios de la muestra principal, 2019–2025", weight="bold", fontsize=20)
        fig.supxlabel("32 fechas · emparejamiento 1:muchos · 47 municipios aparecen en ambos papeles en fechas distintas\n"
                       "Color = participación, no efecto ni peso. Geometría INEGI vigente al consultar; no reconstruye límites históricos.", fontsize=10)
        fig.savefig(OUT / "mapa_muestra.png", dpi=180, facecolor="white")
        fig.savefig(OUT / "mapa_muestra.pdf", dpi=180, facecolor="white", metadata={"CreationDate": None})
        plt.close(fig)
    return dict(tratados_mapeados=len(treated), controles_mapeados=len(controls),
                interseccion=len(treated & controls), union=len(treated | controls),
                claves_sin_geometria=sorted(missing), municipios_cartografia=len(shapes))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cartografia", type=Path, required=True)
    parser.add_argument("--muestra", type=Path, required=True)
    args = parser.parse_args()
    sample = pd.read_csv(args.muestra, usecols=["clave", "tratado", "escenario", "muestra"], dtype={"clave": str})
    main = sample.loc[sample.escenario.eq("principal") & sample.muestra.eq("emparejada")]
    features, sources = [], []
    for state in range(1, 33):
        path = args.cartografia / f"municipios-{state:02}.geojson"
        content = path.read_bytes()
        data = json.loads(content)
        features.extend(data["features"])
        sources.append({"file": path.name, "sha256": hashlib.sha256(content).hexdigest(),
                        "url": f"https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgem/{state:02}",
                        "metadata": data.get("metadatos")})
    result = draw(features, main)
    metadata = {"sample_sha256": hashlib.sha256(args.muestra.read_bytes()).hexdigest(),
                "geometry": "INEGI, diciembre de 2025; WGS84/CRS84; equirectangular, paralelo 23 N",
                "purpose": "Referencia geografica; no representa efectos, pesos ni limites historicos",
                "sources": sources, "coverage": result}
    (OUT / "mapa_muestra.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(result)

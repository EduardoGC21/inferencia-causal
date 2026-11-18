import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import nct, t


LABELS = {"sin_calibre": "Sin calibre de nivel previo", "principal": "Principal",
          "lavado_largo": "Lavado de 42 días", "geografia": "Fuera de estados colindantes",
          "placebo": "Placebo 28 días antes"}


def fmt(value, digits=2):
    if not np.isfinite(value):
        return "—"
    if abs(value) < 0.5 * 10**(-digits):
        value = 0
    return f"{value:,.{digits}f}".replace(",", " ").replace(".", ",")


def texesc(value):
    return str(value).replace("_", r"\_").replace("%", r"\%").replace("&", r"\&")


def table(path, headers, rows, alignment=None):
    alignment = alignment or ("l" + "r" * (len(headers) - 1))
    text = [r"\begin{tabular}{" + alignment + "}", r"\toprule",
            " & ".join(headers) + r" \\", r"\midrule"]
    text.extend(" & ".join(map(str, row)) + r" \\" for row in rows)
    text.extend([r"\bottomrule", r"\end{tabular}", ""])
    path.write_text("\n".join(text), encoding="utf-8")


def mde(df, se, alpha, power):
    if not np.isfinite(df) or not np.isfinite(se) or se <= 0:
        return np.nan
    critical = t.ppf(1 - alpha / 2, df)

    def rejection(ncp):
        return nct.sf(critical, df, ncp) + nct.cdf(-critical, df, ncp) - power

    return se * brentq(rejection, 0, critical + 5)


def weighted_description(frame):
    weights = frame.peso.to_numpy()
    values = frame.pre_nivel.to_numpy()
    mean = np.average(values, weights=weights)
    sd = np.sqrt(np.average((values - mean) ** 2, weights=weights))
    return dict(n=len(frame), media=mean, sd=sd, minimo=values.min(), maximo=values.max())


def run(config):
    paths = config["paths"]
    mod, out = (paths["outputs"] / directory for directory in ("modelos", "tablas"))
    out.mkdir(parents=True, exist_ok=True)
    e = pd.read_csv(mod / "estimaciones.csv")
    sample = pd.read_csv(mod / "muestra.csv", dtype={"clave": str, "estado": str})
    q = pd.read_csv(out / "calidad.csv")
    d = config["design"]
    e["efecto_sigma"] = e.efecto / e.sigma_pre
    e["mde"] = [mde(r.gl, r.ee, d["alpha"], d["power"]) for r in e.itertuples()]
    e["p_estado"] = 2 * t.sf(np.abs(e.efecto / e.ee), e.gl)
    e.to_csv(out / "efectos.csv", index=False)
    p = e.loc[e.especificacion.eq("principal")].set_index("h")
    base = p.loc[0]
    main_sample = sample[sample.especificacion.eq("principal")]
    treated = main_sample[main_sample.tratado.eq(1)]
    indices = pd.to_datetime(main_sample.indice)
    base_dates = indices - pd.Timedelta(days=d["anticipation"] + 1)
    dates = sorted(set(indices) | set(base_dates))
    level_rows = pd.read_parquet(paths["processed"] / "panel_diario.parquet",
                                 columns=["clave", "fecha", "accidentes"],
                                 filters=[("fecha", "in", dates)])
    index_values = level_rows.set_index(["clave", "fecha"]).accidentes

    def level_gap(days):
        values = index_values.reindex(pd.MultiIndex.from_arrays([main_sample.clave, days])).to_numpy(dtype=float)
        role = main_sample.tratado.eq(1).to_numpy()
        weights = main_sample.peso.to_numpy()
        return np.average(values[role], weights=weights[role]) - np.average(values[~role], weights=weights[~role])

    base_gap, onset_gap = level_gap(base_dates), level_gap(indices)
    assert np.isclose(onset_gap - base_gap, base.efecto, atol=1e-10)

    desc = pd.DataFrame({
        "Tratados": weighted_description(treated),
        "Controles": weighted_description(main_sample[main_sample.tratado.eq(0)]),
    }).T
    desc.to_csv(out / "descriptivos.csv", index_label="grupo")
    table(out / "descriptivos.tex", ["Grupo", "Pares", "Media", "DE", "Mín.", "Máx."],
          [[label, fmt(row.n, 0), fmt(row.media), fmt(row.sd), fmt(row.minimo), fmt(row.maximo)]
           for label, row in desc.iterrows()])
    table(out / "principales.tex",
          ["Especificación", "Día", "Efecto", "EE", "IC 95\\%", "Efecto/DE", "$N$"],
          [[LABELS[r.especificacion], r.h, fmt(r.efecto), fmt(r.ee),
            f"[{fmt(r.ic_inf)} a {fmt(r.ic_sup)}]" if np.isfinite(r.ic_inf) else "—",
            fmt(r.efecto_sigma), fmt(r.n, 0)]
           for name in LABELS for r in e[e.especificacion.eq(name) & e.h.isin([0, 7, 15])].itertuples()])
    table(out / "horizontes.tex",
          ["Día", "Efecto", "EE", "IC 95\\% estado", "EE doble", "IC 95\\% doble", "MDE"],
          [[h, fmt(r.efecto), fmt(r.ee), f"[{fmt(r.ic_inf)} a {fmt(r.ic_sup)}]", fmt(r.ee_doble),
            f"[{fmt(r.ic_doble_inf)} a {fmt(r.ic_doble_sup)}]" if np.isfinite(r.ee_doble) else "—",
            fmt(r.mde)] for h, r in p.iterrows()])
    detailed = e[e.especificacion.str.startswith("omitir_")].copy()
    detailed.to_csv(out / "influencia.csv", index=False)
    influence = detailed[detailed.h.eq(0)].copy()
    table(out / "influencia.tex", ["Episodio omitido", "Tratados", "$N$", "Efecto", "EE", "IC 95\\%"],
          [[texesc(r.especificacion.removeprefix("omitir_")), fmt(r.tratados, 0), fmt(r.n, 0),
            fmt(r.efecto), fmt(r.ee), f"[{fmt(r.ic_inf)} a {fmt(r.ic_sup)}]"]
           for r in influence.itertuples()])
    for column in ("id_episodio", "estado"):
        shares = treated.groupby(column).peso.sum().sort_values(ascending=False).rename("peso")
        (shares / shares.sum()).to_csv(out / f"peso_{column}.csv", header=True)
    diag = pd.read_csv(mod / "diagnosticos.csv")
    calendar = diag[diag.especificacion.eq("principal")].copy()
    calendar["tratados_incluidos"] = calendar.tratados.where(calendar.incluida, 0)
    calendar.to_csv(out / "calendario.csv", index=False)
    raw = q[q.anio.between(config["atus"]["first"], config["atus"]["last"])]
    annual = raw.pivot(index="anio", columns="metrica", values="n").fillna(0)
    table(out / "calidad.tex", ["Año", "Originales", "Válidos", "Positivos", "Ceros por continuidad", "Faltantes"],
          [[str(int(y)), *[fmt(row[k], 0) for k in
                            ["filas_originales", "accidentes_validos", "positivo",
                             "cero_por_continuidad", "desconocida"]]] for y, row in annual.iterrows()])
    events = pd.read_parquet(paths["processed"] / "exposiciones.parquet")
    catalog = (events.groupby(["clase_final", "estado"])
               .agg(filas=("id_fila", "size"), episodios=("id_episodio", "nunique")).reset_index())
    catalog.to_csv(out / "resumen_catalogo.csv", index=False)
    post = p.loc[p.index >= 0]
    pre = p.loc[p.index < 0]
    max_pre = pre.loc[pre.efecto.abs().idxmax()]
    precise_pre = int((pre.ic_inf.ge(-d["pre_important"]) & pre.ic_sup.le(d["pre_important"])).sum())
    named = q[q.metrica.eq("filas_catalogo_georreferenciadas")].iloc[0]
    placebo_seven = e.loc[e.especificacion.eq("placebo") & e.h.eq(7)].iloc[0]
    base_media = e.loc[e.especificacion.eq("explora_base_media")].set_index("h")
    base_semana = e.loc[e.especificacion.eq("explora_base_semana")].iloc[0]
    weekly = pd.read_csv(mod / "culiacan.csv", parse_dates=["inicio"])
    observed = weekly.loc[weekly.semana.ge(0) & weekly.brecha.notna()]
    c = config["culiacan"]
    review = (observed.inicio.le(c["reporting_through"])
              & (observed.inicio + pd.Timedelta(days=6)).ge(c["reporting_from"]))
    later = observed.loc[observed.inicio.ge(c["boundary"])]

    cul = pd.read_csv(mod / "culiacan_soporte.csv").iloc[0]
    placebos = pd.read_csv(mod / "culiacan_placebos.csv")
    place = placebos[placebos.rol.eq("placebo")]
    real = placebos[placebos.rol.eq("tratado")].iloc[0] if (placebos.rol == "tratado").any() else None
    if real is not None:
        cul_result = (f"La brecha media observada fue de {fmt(real.brecha_media_post)} accidentes por semana "
                      f"y el error cuadrático medio previo, en raíz, fue {fmt(real.rmse_pre_validacion)}. "
                      f"En los {len(place)} placebos, el error previo tuvo mediana de "
                      f"{fmt(place.rmse_pre_validacion.median())} y las brechas medias fueron de "
                      f"{fmt(place.brecha_media_post.min())} a {fmt(place.brecha_media_post.max())}.")
    else:
        cul_result = "La cobertura o la falta de comparadores impidió construir una brecha semanal ajustada."
    astro = events[events.estado.eq("confirmado") & events.clase_final.eq("extensa")]
    stats = {
        "TotalINEGI": fmt(annual.loc[2025, "filas_originales"], 0),
        "FilasMicro": fmt(annual.filas_originales.sum(), 0),
        "AccValidos": fmt(annual.accidentes_validos.sum(), 0),
        "FechaInvalida": fmt(annual.fecha_invalida.sum(), 0),
        "Duplicados": fmt(annual.duplicados_exactos_retenidos.sum(), 0),
        "PanelTotal": fmt(annual[["positivo", "cero_por_continuidad", "desconocida"]].sum().sum(), 0),
        "PanelPos": fmt(annual.positivo.sum(), 0),
        "PanelCeros": fmt(annual.cero_por_continuidad.sum(), 0),
        "PanelFalta": fmt(annual.desconocida.sum(), 0),
        "CatFilas": fmt(len(events), 0),
        "CatGeo": fmt(named.n, 0),
        "CatPct": fmt(100 * named.n / named.denominador, 1),
        "CatExtensas": fmt(astro.id_episodio.nunique(), 0),
        "CatTrat": fmt(len(astro), 0),
        "CatMenor": fmt(len(events[events.clase_final.eq("menor")]), 0),
        "FechasPrincipal": fmt(base.fechas, 0),
        "EpisPrincipal": fmt(base.episodios, 0),
        "TratPrincipal": fmt(base.tratados, 0),
        "TratSinCobertura": fmt(calendar.tratados_cobertura.sum(), 0),
        "TratConTraslape": fmt(calendar.tratados_otro_episodio.sum(), 0),
        "ControlPrincipal": fmt(base.controles, 0),
        "MuniTrat": fmt(base.municipios_tratados, 0),
        "MuniControl": fmt(base.municipios_controles, 0),
        "Estados": fmt(base.estados, 0),
        "EstadosTrat": fmt(base.estados_tratados, 0),
        "EstadosControl": fmt(base.estados_controles, 0),
        "PesoEstado": fmt(100 * base.max_peso_estado, 1),
        "PesoEpi": fmt(100 * base.max_peso_episodio, 1),
        "EstadosEf": fmt(base.estados_tratados_efectivos, 1),
        "EpisEf": fmt(base.episodios_efectivos, 1),
        "Reuso": fmt(base.max_reuso_control, 0),
        "EfectoCero": fmt(base.efecto),
        "EECero": fmt(base.ee),
        "InfCero": fmt(base.ic_inf),
        "SupCero": fmt(base.ic_sup),
        "GlCero": fmt(base.gl, 0),
        "Pcero": fmt(base.p_estado, 3),
        "SigmaCero": fmt(base.efecto_sigma),
        "MdeCero": fmt(base.mde),
        "MediaBase": fmt(base.media_base),
        "MdePct": fmt(100 * base.mde / base.media_base, 1),
        "EfectoPct": fmt(100 * base.efecto / base.media_base, 1),
        "DobleInf": fmt(base.ic_doble_inf),
        "DobleSup": fmt(base.ic_doble_sup),
        "DobleGl": fmt(base.gl_doble, 0),
        "DoblePerdidas": fmt((post.estado_doble != "calculada").sum(), 0),
        "DiaPreMax": fmt(max_pre.name, 0),
        "EstPreMax": fmt(max_pre.efecto),
        "EstPreInf": fmt(max_pre.ic_inf),
        "EstPreSup": fmt(max_pre.ic_sup),
        "PreAcotados": fmt(precise_pre, 0),
        "PreExcluye": fmt(((pre.ic_inf > 0) | (pre.ic_sup < 0)).sum(), 0),
        "DiaSiete": fmt(p.loc[7, "efecto"]),
        "DiaQuince": fmt(p.loc[15, "efecto"]),
        "PlaceboSiete": fmt(placebo_seven.efecto),
        "PlaceboSieteInf": fmt(placebo_seven.ic_inf),
        "PlaceboSieteSup": fmt(placebo_seven.ic_sup),
        "PlaceboDobleInf": fmt(placebo_seven.ic_doble_inf),
        "PlaceboDobleSup": fmt(placebo_seven.ic_doble_sup),
        "PreDobleExcluye": fmt(((pre.ic_doble_inf > 0) | (pre.ic_doble_sup < 0)).sum(), 0),
        "BrechaBase": fmt(base_gap),
        "BrechaCero": fmt(onset_gap),
        "BaseMediaCero": fmt(base_media.loc[0, "efecto"]),
        "BaseMediaInf": fmt(base_media.loc[0, "ic_inf"]),
        "BaseMediaSup": fmt(base_media.loc[0, "ic_sup"]),
        "BaseMediaSiete": fmt(base_media.loc[7, "efecto"]),
        "BaseMediaQuince": fmt(base_media.loc[15, "efecto"]),
        "BaseSemanaCero": fmt(base_semana.efecto),
        "BaseSemanaInf": fmt(base_semana.ic_inf),
        "BaseSemanaSup": fmt(base_semana.ic_sup),
        "PreTotal": fmt(len(pre), 0),
        "PostExcluye": fmt(((post.ic_inf > 0) | (post.ic_sup < 0)).sum(), 0),
        "PostMin": fmt(post.efecto.min()),
        "PostMax": fmt(post.efecto.max()),
        "LooMin": fmt(influence.efecto.min()),
        "LooMax": fmt(influence.efecto.max()),
        "LooMinEpi": texesc(influence.loc[influence.efecto.idxmin(), "especificacion"].removeprefix("omitir_")),
        "LooMaxEpi": texesc(influence.loc[influence.efecto.idxmax(), "especificacion"].removeprefix("omitir_")),
        "CulObs": fmt(cul.semanas_post_observadas, 0),
        "CulTotal": fmt(cul.semanas_post_totales, 0),
        "CulEleg": fmt(cul.comparadores_elegibles, 0),
        "CulIgu": fmt(cul.comparadores_usados, 0),
        "CulFalta": fmt(cul.semanas_post_totales - cul.semanas_post_observadas, 0),
        "CulRevision": fmt(review.sum(), 0),
        "CulRevisionBrecha": fmt(observed.loc[review, "brecha"].mean()),
        "CulFuera": fmt((~review).sum(), 0),
        "CulFueraBrecha": fmt(observed.loc[~review, "brecha"].mean()),
        "CulDespues": fmt(len(later), 0),
        "CulDespuesBrecha": fmt(later.brecha.mean()),
        "CulRes": cul_result,
    }
    (out / "cifras.tex").write_text("".join(r"\newcommand{\F" + k + "}{" + v + "}\n"
                                           for k, v in stats.items()), encoding="utf-8")
    print(f"Tablas y cifras generadas en {out}")

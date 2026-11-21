import numpy as np
import pandas as pd

from .modelos import active_events


def territorial_donors(keys, changes, first, last):
    """Cambios M en semanas usadas: se excluyen origen y destino; W no divide."""
    active = changes.loc[changes.codigo.eq("M") & changes.fecha.between(first, last)]
    affected = set(active.origen) | set(active.destino)
    return ~keys.isin(affected)


def run(matrix, events, config, output):
    design = config["culiacan"]
    onset = pd.Timestamp(design["onset"])
    boundary = pd.Timestamp(design["boundary"])
    week = (matrix.dates - onset).days // 7
    values = np.where(matrix.coverage, matrix.values, np.nan)
    c, e = matrix.keys.get_indexer(["25006", "25019"])
    if c < 0 or e < 0:
        raise ValueError("Faltan Culiacán o Eldorado en el panel")
    before_split = matrix.dates < boundary
    values[c, ~before_split] = values[c, ~before_split] + values[e, ~before_split]
    weeks = np.array([int(w) for w in week.unique() if (week == w).sum() == 7
                      and w >= design["train_first"]])
    weekly = (np.column_stack([values[:, week == w].sum(axis=1) for w in weeks])
              if len(weeks) else np.empty((len(matrix.keys), 0)))
    train = (weeks >= design["train_first"]) & (weeks <= design["train_last"])
    base = weeks == design["base"]
    check = (weeks > design["train_last"]) & (weeks < -1) & ~base
    observed_post = (weeks >= 0) & np.isfinite(weekly[c])
    common = train | check | base | observed_post
    active = active_events(events)
    span_first = onset + pd.Timedelta(weeks=design["train_first"], days=-21)
    exposed = active.loc[active.hasta.ge(span_first) & active.inicio.le(matrix.dates[-1])]
    named = set(exposed.loc[exposed.clave.ne(""), "clave"])
    broad = set(exposed.loc[exposed.clave.eq(""), "cve_ent"].dropna())
    eligible = np.flatnonzero((matrix.states != "25") & ~matrix.states.isin(broad)
                              & ~matrix.keys.isin(named) & np.isfinite(weekly[:, common]).all(axis=1))
    if "paths" in config:
        changes = pd.read_csv(config["paths"]["processed"] / "municipios" / "cambios_territoriales.csv",
                              dtype={"origen": str, "destino": str}, parse_dates=["fecha"])
        first = onset + pd.Timedelta(weeks=int(weeks[common].min()))
        last = onset + pd.Timedelta(weeks=int(weeks[common].max()), days=6)
        allowed = territorial_donors(matrix.keys, changes, first, last)
        excluded = eligible[~allowed[eligible]]
        pd.DataFrame({"clave": matrix.keys[excluded], "desde": first, "hasta": last,
                      "motivo": "segregacion_M"}).to_csv(output / "culiacan_descartes_territoriales.csv", index=False)
        eligible = eligible[allowed[eligible]]
    size = design["neighbors"]
    frame = pd.DataFrame({"semana": weeks, "inicio": onset + pd.to_timedelta(7 * weeks, unit="D"),
                          "tratado": weekly[c], "control": np.nan, "brecha": np.nan})
    summary = {"comparadores_elegibles": len(eligible), "comparadores_usados": 0,
               "semanas_post_observadas": int(observed_post.sum()),
               "semanas_post_totales": int((weeks >= 0).sum()),
               "estado": "Sin ajuste previo o sin comparadores"}
    comparison = pd.DataFrame(columns=["clave", "rol", "rmse_pre_validacion", "brecha_media_post"])
    control_keys = pd.DataFrame(columns=["clave"])

    def compare(row, pool):
        distance = np.sqrt(np.mean((weekly[pool][:, train] - weekly[row, train]) ** 2, axis=1))
        chosen = pool[np.argsort(distance, kind="stable")[:size]]
        selected = weekly[chosen]
        complete = np.isfinite(selected).all(axis=0)
        control = np.full(len(weeks), np.nan)
        control[complete] = selected[:, complete].mean(axis=0)
        difference = weekly[row] - control
        return chosen, control, difference - difference[base].item()

    prior_weeks = np.arange(design["train_first"], -1)
    complete_prior = np.isin(prior_weeks, weeks).all() and base.sum() == 1
    if complete_prior and np.isfinite(weekly[c, train | check | base]).all() and len(eligible) >= size:
        chosen, control, gap = compare(c, eligible)
        control[~np.isfinite(weekly[c])] = np.nan
        gap[weeks == -1] = np.nan
        frame = frame.assign(control=control, brecha=gap)
        control_keys = pd.DataFrame({"clave": matrix.keys[chosen]})
        records = []
        # A placebo needs size donors after excluding the pseudo-treated unit.
        placebo_rows = chosen[:design["placebos"]] if len(eligible) > size else chosen[:0]
        for row in np.r_[c, placebo_rows]:
            _, _, candidate = compare(row, eligible[eligible != row])
            records.append(dict(clave=matrix.keys[row], rol="tratado" if row == c else "placebo",
                                rmse_pre_validacion=float(np.sqrt(np.mean(candidate[check] ** 2))),
                                brecha_media_post=float(candidate[observed_post].mean())))
        comparison = pd.DataFrame(records)
        summary.update(comparadores_usados=len(chosen), estado="comparación descriptiva")
    frame.to_csv(output / "culiacan.csv", index=False)
    comparison.to_csv(output / "culiacan_placebos.csv", index=False)
    control_keys.to_csv(output / "culiacan_controles.csv", index=False)
    pd.DataFrame([summary]).to_csv(output / "culiacan_soporte.csv", index=False)

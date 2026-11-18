import json
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd
import pyfixest as pf
from scipy.stats import t

from .descarga import hash_file


# State boundary adjacency. Used only as a stricter proxy for cross-state spillovers.
BORDERS = {
    "01": "14 32", "02": "03 26", "03": "02", "04": "23 27 31",
    "05": "08 10 19 32", "06": "14 16", "07": "20 27 30", "08": "05 10 25 26",
    "09": "15 17", "10": "05 08 18 25 32", "11": "14 16 22 24 32",
    "12": "15 16 17 20 21", "13": "15 21 22 24 29 30", "14": "01 06 11 16 18 32",
    "15": "09 12 13 16 17 21 22 29", "16": "06 11 12 14 15 22",
    "17": "09 12 15 21", "18": "10 14 25 32", "19": "05 24 28 32", "20": "07 12 21 30",
    "21": "12 13 15 17 20 29 30", "22": "11 13 15 16 24", "23": "04 31",
    "24": "11 13 19 22 28 30 32", "25": "08 10 18 26", "26": "02 08 25",
    "27": "04 07 30", "28": "19 24 30", "29": "13 15 21", "30": "07 13 20 21 24 27 28",
    "31": "04 23", "32": "01 05 10 11 14 18 19 24",
}
BOUNDARY = pd.Timestamp("2024-11-01")
TERRITORIAL = {"25001", "25006", "25010", "25011", "25017", "25019", "25020"}
SAMPLE = ["clave", "estado", "indice", "tratado", "id_episodio", "peso", "pre_nivel"]


class Matrix:
    """Calendar-aligned values. Every estimator uses exact calendar offsets."""

    def __init__(self, panel):
        pivot = panel.pivot(index="clave", columns="fecha", values="accidentes")
        continued = panel.pivot(index="clave", columns="fecha", values="continuidad")
        self.dates = pivot.columns
        self.keys = pivot.index
        self.states = self.keys.str[:2]
        self.values = pivot.to_numpy(dtype=float, na_value=np.nan)
        self.coverage = continued.to_numpy(dtype=bool, na_value=False)

    def extract(self, sample, offset):
        i = self.keys.get_indexer(sample["clave"])
        j = self.dates.get_indexer(pd.DatetimeIndex(sample["indice"]) + pd.to_timedelta(offset, unit="D"))
        if (i < 0).any() or (j < 0).any():
            raise ValueError("La muestra pide claves o fechas fuera del panel")
        return self.values[i, j]


def day(value, n):
    return value + pd.Timedelta(days=n)


def active_events(events):
    # An open-ended persistent crisis stays a possible source of contamination.
    events = events.loc[events["inicio"].notna()].copy()
    end = events["fin"].fillna(events["inicio"])
    events["hasta"] = end.mask(events.clase_final.eq("persistente") & events.fin.isna(),
                                pd.Timestamp.max.normalize())
    return events


def comparison(matrix, events, design, name):
    events = active_events(events)
    focal = events.loc[events.estado.eq("confirmado") & events.clase_final.eq("extensa")].copy()
    omitted = name.removeprefix("omitir_") if name.startswith("omitir_") else None
    focal = focal.loc[focal.id_episodio.ne(omitted)]
    placebo = name == "placebo"
    offset = -design.get("placebo_days", 28) if placebo else 0
    focal["indice"] = focal["inicio"] + pd.to_timedelta(offset, unit="D")
    pre = design["pre"]
    scale = design.get("scale_days", 14)
    horizon = design["horizon"]
    washout = design.get("washout_long", 42) if name == "lavado_largo" else design["washout"]
    sample, diagnostic = [], []

    for index, cohort in focal.groupby("indice", sort=True):
        left = day(index, -pre - scale - washout)
        right = day(index, horizon + design["anticipation"])
        local = set(cohort.clave)
        now_ids = set(cohort.id_episodio)
        lookup = cohort.drop_duplicates("clave").set_index("clave").id_episodio
        if cohort.clave.duplicated().any():
            raise ValueError(f"Más de un focal para un municipio en {index.date()}")
        geography = set(events.loc[events.id_episodio.isin(now_ids), "cve_ent"].dropna())
        if name == "geografia":
            geography |= {neighbor for state in geography for neighbor in BORDERS[state].split()}
        window_events = events.loc[events.inicio.le(right) & events.hasta.ge(left)]
        named = window_events.clave.ne("")
        contaminated = set(window_events.loc[named, "clave"])
        blocked_states = set(window_events.loc[~named, "cve_ent"].dropna())
        # A state-wide clue for this exact focal event excludes controls,
        # but leaves the location-confirmed treated municipalities eligible.
        treatment_block = {row.clave for row in window_events.loc[named & window_events.clave.isin(local)].itertuples()
                           if placebo or row.id_episodio != lookup[row.clave]}
        for state, clues in window_events.loc[~named].groupby("cve_ent"):
            clue_ids = set(clues.id_episodio)
            for row in cohort.loc[cohort.cve_ent.eq(state)].itertuples():
                if placebo or clue_ids - {row.id_episodio}:
                    treatment_block.add(row.clave)
        geo_change = matrix.keys.isin(TERRITORIAL) & (right >= BOUNDARY)
        mask_span = ((matrix.dates >= day(index, -pre - scale))
                     & (matrix.dates <= day(index, horizon)))
        width = pre + scale + horizon + 1
        valid_span = mask_span.sum() == width and left >= matrix.dates[0] and right <= matrix.dates[-1]
        keep = matrix.coverage[:, mask_span].all(axis=1) if valid_span else np.zeros(len(matrix.keys), bool)
        keep &= np.isfinite(matrix.values[:, mask_span]).all(axis=1)
        scale_dates = (matrix.dates >= day(index, -pre - scale)) & (matrix.dates < day(index, -pre))
        levels = (matrix.values[:, scale_dates].mean(axis=1) if scale_dates.sum() == scale
                  else np.full(len(matrix.keys), np.nan))
        focal_mask = matrix.keys.isin(local)
        blocked_t = matrix.keys.isin(treatment_block)
        treated = focal_mask & ~blocked_t & ~geo_change & keep
        zone = matrix.states.isin(geography)
        blocked_c = matrix.keys.isin(contaminated) | matrix.states.isin(blocked_states)
        eligible = ~focal_mask & ~zone & ~blocked_c & ~geo_change
        available = eligible & keep
        center = levels[treated].mean() if treated.any() else np.nan
        ratio = design.get("caliber", 2.0)
        if name == "sin_calibre" or not treated.any():
            comparable = available
        else:
            # Half-accident offset retains comparators at small pre-treatment levels.
            scaled = (levels + 0.5) / (center + 0.5)
            comparable = available & (scaled >= 1 / ratio) & (scaled <= ratio)
        n_t = int(treated.sum())
        n_c = int(comparable.sum())
        state_c = matrix.states[comparable].nunique()
        accepted = n_t > 0 and n_c >= design["min_controls"] and state_c >= design["min_control_states"]
        diagnostic.append(dict(
            especificacion=name, indice=index, episodios=";".join(sorted(now_ids)),
            tratados_candidatos=len(local), tratados_otro_episodio=int((focal_mask & blocked_t).sum()),
            tratados_geografia=int((focal_mask & ~blocked_t & geo_change).sum()),
            tratados_cobertura=int((focal_mask & ~blocked_t & ~geo_change & ~keep).sum()),
            controles_geografia=int((~focal_mask & zone).sum()),
            controles_exposicion=int((~focal_mask & ~zone & blocked_c).sum()),
            controles_quiebre=int((~focal_mask & ~zone & ~blocked_c & geo_change).sum()),
            controles_cobertura=int((eligible & ~keep).sum()),
            controles_calibre=int((available & ~comparable).sum()), tratados=n_t, controles=n_c,
            estados_tratados=matrix.states[treated].nunique(), estados_controles=state_c,
            base=day(index, -design["anticipation"] - 1), primer_dia_pre=day(index, -pre),
            libre_desde=left, libre_hasta=right, incluida=accepted))
        if not accepted:
            continue
        selected = treated | comparable
        key = matrix.keys[selected]
        roles = treated[selected].astype(int)
        rows = pd.DataFrame(dict(clave=key, estado=matrix.states[selected], indice=index,
                                 tratado=roles, id_episodio=lookup.reindex(key).fillna("").to_numpy(),
                                 peso=np.where(roles, 1.0, n_t / n_c), pre_nivel=levels[selected]))
        assert rows.groupby("tratado").peso.sum().sub(n_t).abs().max() < 1e-9
        sample.append(rows)
    return (pd.concat(sample, ignore_index=True) if sample else pd.DataFrame(columns=SAMPLE),
            pd.DataFrame(diagnostic))


def summarize(sample):
    treated = sample.loc[sample.tratado.eq(1)]
    controls = sample.loc[sample.tratado.eq(0)]
    l1, l2 = (treated.groupby(key).peso.sum() / len(treated) for key in ("id_episodio", "estado"))
    return dict(
        n=len(sample), municipios=sample.clave.nunique(), tratados=len(treated), controles=len(controls),
        municipios_tratados=treated.clave.nunique(), municipios_controles=controls.clave.nunique(),
        fechas=sample.indice.nunique(), episodios=treated.id_episodio.nunique(),
        estados=sample.estado.nunique(), estados_tratados=treated.estado.nunique(),
        estados_controles=controls.estado.nunique(), max_peso_episodio=l1.max(),
        max_peso_estado=l2.max(), episodios_efectivos=1 / (l1**2).sum() if len(l1) else np.nan,
        estados_tratados_efectivos=1 / (l2**2).sum() if len(l2) else np.nan,
        max_reuso_control=controls.groupby("clave").size().max(),
    )


def regression(frame, design):
    result = pf.feols("delta ~ tratado | indice", frame, weights="peso", weights_type="aweights",
                      vcov={"CRV1": "estado"}, fixef_rm="none",
                      ssc=pf.ssc(k_adj=True, k_fixef="full", G_adj=True, G_df="min"))
    effect = float(result.coef()["tratado"])
    se = float(result.se()["tratado"])
    df = frame.estado.nunique() - 1
    assert result.variance_covariance.df_t == df
    q = t.ppf(1 - design.get("alpha", 0.05) / 2, df)
    two_way, df_two, status = np.nan, np.nan, "fechas insuficientes"
    dates = frame.indice.nunique()
    if dates >= design.get("min_two_way_dates", 6):
        result.vcov({"CRV1": "estado + indice"})
        variance = float(result.variance_covariance.vcov[0, 0])
        df_two = min(df, dates - 1)
        assert result.variance_covariance.df_t == df_two
        if variance >= 0:
            two_way = np.sqrt(variance)
            status = "calculada"
        else:
            status = "varianza negativa"
    q_two = t.ppf(1 - design.get("alpha", 0.05) / 2, df_two)
    return dict(efecto=effect, ee=se, gl=df, ic_inf=effect - q * se, ic_sup=effect + q * se,
                ee_doble=two_way, gl_doble=df_two, ic_doble_inf=effect - q_two * two_way,
                ic_doble_sup=effect + q_two * two_way, estado_doble=status)


def fit(matrix, sample, h, design, reference=None):
    totals = summarize(sample)
    if sample.empty:
        return totals | dict(efecto=np.nan, ee=np.nan, gl=np.nan, ic_inf=np.nan, ic_sup=np.nan,
                             ee_doble=np.nan, gl_doble=np.nan, ic_doble_inf=np.nan,
                             ic_doble_sup=np.nan, estado_doble="sin muestra")
    days = reference if reference is not None else (-design["anticipation"] - 1,)
    baseline = np.stack([matrix.extract(sample, day) for day in days]).mean(axis=0)
    delta = matrix.extract(sample, h) - baseline
    frame = sample.assign(delta=delta)
    fitted = regression(frame, design)
    treated = frame.tratado.eq(1)
    contrast = (np.average(delta[treated], weights=frame.loc[treated, "peso"])
                - np.average(delta[~treated], weights=frame.loc[~treated, "peso"]))
    if not np.isclose(fitted["efecto"], contrast, rtol=1e-9, atol=1e-10):
        raise ValueError("La pendiente difiere del contraste de cambios reponderado")
    return totals | fitted


def load(paths):
    panel = pd.read_parquet(paths["processed"] / "panel_diario.parquet",
                            columns=["clave", "fecha", "accidentes", "continuidad"])
    events = pd.read_parquet(paths["processed"] / "exposiciones.parquet")
    return Matrix(panel), events


def support(config, expected_sha=None):
    paths = config["paths"]
    matrix, events = load(paths)
    design = config["design"]
    output = paths["outputs"] / "modelos"
    output.mkdir(parents=True, exist_ok=True)
    principal, _ = comparison(matrix, events, design, "principal")
    ids = sorted(principal.loc[principal.tratado.eq(1), "id_episodio"].unique())
    names = ["principal", "sin_calibre", "lavado_largo", "geografia", "placebo"]
    names.extend(f"omitir_{eid}" for eid in ids)
    samples, diagnostics = [], []
    for name in names:
        sample, diag = comparison(matrix, events, design, name)
        samples.append(sample.assign(especificacion=name))
        diagnostics.append(diag)
    diag = pd.concat(diagnostics, ignore_index=True)
    with TemporaryDirectory(dir=output) as directory:
        stage = Path(directory)
        sample_path = stage / "muestra.csv"
        pd.concat(samples, ignore_index=True).to_csv(sample_path, index=False)
        if expected_sha is not None and hash_file(sample_path) != expected_sha:
            raise ValueError("La muestra reconstruida difiere de la revisión auditada")
        diag.to_csv(stage / "diagnosticos.csv", index=False)
        for file in (sample_path, stage / "diagnosticos.csv"):
            file.replace(output / file.name)
    counts = diag.groupby("especificacion").incluida.sum()
    print(f"Fechas elegibles, sin estimar: {counts.to_dict()}")


def run(config):
    paths = config["paths"]
    output = paths["outputs"] / "modelos"
    project = config["root"].parent
    release = paths["tasks"] / "revision-auditoria" / "revision_auditada.json"
    revision = json.loads(release.read_text(encoding="utf-8"))
    fingerprints = revision["sha256"]
    required = {(paths["processed"] / name).relative_to(project).as_posix()
                for name in ("panel_diario.parquet", "exposiciones.parquet")}
    if not required <= fingerprints.keys():
        raise ValueError("Faltan huellas del panel o de exposiciones en la revisión auditada")
    for relative_path, digest in fingerprints.items():
        if hash_file(project / relative_path) != digest:
            raise ValueError(f"El insumo de la revisión auditada cambió: {relative_path}")
    support(config, expected_sha=revision["muestra_sha256"])
    matrix, events = load(paths)
    sample = pd.read_csv(output / "muestra.csv", dtype={"clave": str, "estado": str},
                         parse_dates=["indice"], keep_default_na=False)
    diag = pd.read_csv(output / "diagnosticos.csv")
    design = config["design"]
    estimates = []
    for name in diag.especificacion.unique():
        subset = sample.loc[sample.especificacion.eq(name)].copy()
        base = -design["anticipation"] - 1
        if name == "principal":
            horizons = [h for h in range(-design["pre"], design["horizon"] + 1)
                        if h < base or h >= 0]
        else:
            horizons = [0, 7, design["horizon"]]
        if not subset.empty:
            baseline = matrix.extract(subset[subset.tratado.eq(1)], base)
            pre_days = range(-design["pre"], base + 1)
            pre_treated = np.concatenate([matrix.extract(subset[subset.tratado.eq(1)], h) for h in pre_days])
            mean, sigma = float(baseline.mean()), float(pre_treated.std(ddof=1))
        else:
            mean, sigma = np.nan, np.nan
        for h in horizons:
            estimates.append(dict(especificacion=name, h=h, media_base=mean, sigma_pre=sigma)
                             | fit(matrix, subset, h, design))
    principal = sample.loc[sample.especificacion.eq("principal")]
    treated = principal.loc[principal.tratado.eq(1)]
    # These alternatives were proposed after the frozen results and keep the revised sample.
    for name, reference, horizons in (
        ("explora_base_media", range(-design["pre"], -design["anticipation"]), [0, 7, design["horizon"]]),
        ("explora_base_semana", (-14, -7), [0]),
    ):
        mean = np.stack([matrix.extract(treated, day) for day in reference]).mean()
        for h in horizons:
            estimates.append(dict(especificacion=name, h=h, media_base=mean,
                                  sigma_pre=estimates[0]["sigma_pre"])
                             | fit(matrix, principal, h, design, reference))
    pd.DataFrame(estimates).to_csv(output / "estimaciones.csv", index=False)
    from .persistente import run as persistent
    persistent(matrix, events, config, output)
    print(f"Estimadas {len(estimates)} especificaciones y horizontes.")

import numpy as np
import pandas as pd
from scipy.stats import f, t


def estimate(frame, columns, outcomes, design):
    """Weighted date fixed effects and CRV1, with outcomes in row order."""
    y = np.asarray(outcomes, dtype=float)
    x = frame[columns].to_numpy(dtype=float)
    n, k = x.shape
    if y.ndim != 2 or len(y) != n or not np.isfinite(y).all() or not np.isfinite(x).all():
        raise ValueError("La regresión requiere resultados y covariables finitos sobre las mismas filas")
    n_outcomes = y.shape[1]
    coefficients = np.full((n_outcomes, k), np.nan)
    dfs = {"entidad": np.nan, "entidad_fecha": np.nan}
    covariances = dict.fromkeys(dfs)
    dates = frame.indice.nunique()
    states = frame.estado.nunique()
    if n == 0:
        return coefficients, covariances, dfs
    weights = frame.peso.to_numpy(dtype=float)
    w = np.sqrt(weights)[:, None]
    values = pd.DataFrame(np.column_stack([x, y]))
    groups = frame.indice.to_numpy()
    means = values.mul(weights, axis=0).groupby(groups).transform("sum").to_numpy()
    denominators = pd.Series(weights).groupby(groups).transform("sum").to_numpy()
    within = (values.to_numpy() - means / denominators[:, None]) * w
    xw, yw = within[:, :k], within[:, k:]
    # Keep treatment and each independent variable in block order.
    independent = []
    for column in range(k):
        block = xw[:, independent + [column]]
        if np.linalg.matrix_rank(block) > len(independent):
            independent.append(column)
    if not independent:
        return coefficients, covariances, dfs
    xw = xw[:, independent]
    b = np.linalg.lstsq(xw, yw, rcond=None)[0]
    coefficients[:, independent] = b.T
    residual = yw - xw @ b
    if states < 2 or n <= dates + len(independent):
        return coefficients, covariances, dfs
    influence = xw @ np.linalg.inv(xw.T @ xw)
    scores = (residual[:, :, None] * influence[:, None, :]).reshape(n, -1)
    retained = (np.arange(n_outcomes)[:, None] * k + independent).ravel()
    correction = (n - 1) / (n - dates - len(independent))

    def meat(keys):
        by_group = pd.DataFrame(scores).groupby(keys, sort=False).sum().to_numpy()
        return by_group.T @ by_group

    def expanded(v):
        result = np.full((k * n_outcomes, k * n_outcomes), np.nan)
        result[np.ix_(retained, retained)] = v
        return result

    entity = frame.estado.to_numpy()
    v1 = meat(entity)
    dfs["entidad"] = states - 1
    covariances["entidad"] = expanded(v1 * correction * states / (states - 1))
    if dates >= design.get("min_two_way_dates", 6):
        groups_min = min(states, dates)
        v2 = meat(groups)
        overlap = meat([entity, groups])
        dfs["entidad_fecha"] = groups_min - 1
        covariances["entidad_fecha"] = expanded((v1 + v2 - overlap) * correction * groups_min / (groups_min - 1))
    return coefficients, covariances, dfs


def wald(coefficients, covariance, denominator):
    q = len(coefficients)
    result = dict(f=np.nan, gl_num=q, gl_den=denominator, p=np.nan)
    if covariance is None or not np.isfinite(denominator):
        return result | {"estado": "conglomerados o grados de libertad insuficientes"}
    if not np.isfinite(coefficients).all() or not np.isfinite(covariance).all():
        return result | {"estado": "coeficientes sin identificar"}
    v = (covariance + covariance.T) / 2
    eigen = np.linalg.eigvalsh(v)
    tolerance = np.max(np.abs(eigen)) * q * np.finfo(float).eps
    if eigen.min() < -tolerance:
        return result | {"estado": "covarianza indefinida"}
    if eigen.min() <= tolerance:
        return result | {"estado": "covarianza sin rango"}
    statistic = float(coefficients @ np.linalg.solve(v, coefficients) / q)
    return result | {"f": statistic, "p": f.sf(statistic, q, denominator), "estado": "calculada"}


def interval(coefficient, variance, df, alpha):
    se = np.sqrt(variance) if variance >= 0 else np.nan
    critical = t.ppf(1 - alpha / 2, df)
    return dict(efecto=coefficient, ee=se, gl=df, ic_inf=coefficient - critical * se,
                ic_sup=coefficient + critical * se,
                p=2 * t.sf(abs(coefficient / se), df) if se > 0 else np.nan)

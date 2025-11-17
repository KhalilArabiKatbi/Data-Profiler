from typing import Dict, List, Tuple
import numpy as np
import pandas as pd


def detect_column_types(df: pd.DataFrame) -> Dict[str, str]:
    types: Dict[str, str] = {}
    for col in df.columns:
        s = df[col]
        if pd.api.types.is_datetime64_any_dtype(s) or pd.api.types.is_datetimetz(s):
            types[col] = "datetime"
        elif pd.api.types.is_bool_dtype(s):
            types[col] = "boolean"
        elif pd.api.types.is_numeric_dtype(s):
            types[col] = "numeric"
        else:
            types[col] = "categorical"
    return types


def memory_usage_bytes(df: pd.DataFrame) -> int:
    return int(df.memory_usage(index=True, deep=True).sum())


def series_mode(s: pd.Series) -> List:
    try:
        m = s.mode(dropna=True)
        return list(m.values)
    except Exception:
        return []


def freedman_diaconis_bins(s: pd.Series) -> int:
    x = s.dropna().astype(float).values
    n = x.size
    if n == 0:
        return 10
    q75, q25 = np.percentile(x, [75, 25])
    iqr = q75 - q25
    if iqr == 0:
        return int(np.ceil(np.sqrt(n)))
    width = 2 * iqr * (n ** (-1 / 3))
    if width <= 0:
        return 10
    bins = int(np.ceil((x.max() - x.min()) / width))
    return max(bins, 1)


def histogram_for_series(s: pd.Series, bins: int = None) -> Tuple[List[float], List[int]]:
    arr = s.dropna().astype(float).values
    if arr.size == 0:
        return [], []
    b = bins if bins and bins > 0 else freedman_diaconis_bins(s)
    counts, edges = np.histogram(arr, bins=b)
    return list(edges.tolist()), list(counts.tolist())


def iqr_bounds(s: pd.Series) -> Tuple[float, float]:
    q1 = float(s.quantile(0.25))
    q3 = float(s.quantile(0.75))
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return lower, upper


def zscore_bounds(s: pd.Series, threshold: float = 3.0) -> Tuple[float, float]:
    x = s.dropna().astype(float)
    mu = float(x.mean())
    sigma = float(x.std(ddof=0))
    if sigma == 0:
        return mu, mu
    return mu - threshold * sigma, mu + threshold * sigma


def entropy_from_counts(counts: Dict) -> float:
    total = sum(counts.values())
    if total == 0:
        return 0.0
    probs = [c / total for c in counts.values() if c > 0]
    return float(-sum(p * np.log(p) for p in probs))


def cramer_v(col_x: pd.Series, col_y: pd.Series) -> float:
    table = pd.crosstab(col_x, col_y)
    n = table.values.sum()
    if n == 0:
        return 0.0
    obs = table.values.astype(float)
    row_sums = obs.sum(axis=1)[:, None]
    col_sums = obs.sum(axis=0)[None, :]
    expected = row_sums * col_sums / n
    with np.errstate(divide="ignore", invalid="ignore"):
        chi2 = np.nansum((obs - expected) ** 2 / expected)
    k = obs.shape[1]
    r = obs.shape[0]
    denom = n * float(min(k - 1, r - 1))
    if denom <= 0:
        return 0.0
    return float(np.sqrt(chi2 / denom))
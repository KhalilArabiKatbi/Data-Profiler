from typing import Dict
import numpy as np
import pandas as pd

from .helpers import series_mode


def compute_numeric(df: pd.DataFrame) -> Dict[str, Dict]:
    out: Dict[str, Dict] = {}
    num_cols = df.select_dtypes(include=["number"]).columns
    for col in num_cols:
        s = df[col].dropna()
        if s.empty:
            out[col] = {
                "mean": None,
                "median": None,
                "mode": [],
                "std": None,
                "variance": None,
                "skewness": None,
                "kurtosis": None,
                "quantiles": {"q25": None, "q50": None, "q75": None},
                "missing_pct": float(df[col].isna().mean() * 100.0),
            }
            continue
        mean = float(s.mean())
        median = float(s.median())
        mode_vals = series_mode(s)
        std = float(s.std(ddof=1))
        var = float(s.var(ddof=1))
        skew = float(s.skew())
        kurt = float(s.kurt())
        q25 = float(s.quantile(0.25))
        q50 = float(s.quantile(0.5))
        q75 = float(s.quantile(0.75))
        out[col] = {
            "mean": mean,
            "median": median,
            "mode": mode_vals,
            "std": std,
            "variance": var,
            "skewness": skew,
            "kurtosis": kurt,
            "quantiles": {"q25": q25, "q50": q50, "q75": q75},
            "missing_pct": float(df[col].isna().mean() * 100.0),
        }
    return out
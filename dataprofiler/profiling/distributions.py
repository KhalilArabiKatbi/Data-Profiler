from typing import Dict
import pandas as pd
from .helpers import histogram_for_series, iqr_bounds, zscore_bounds


def compute_distributions(df: pd.DataFrame) -> Dict[str, Dict]:
    out: Dict[str, Dict] = {}
    num_cols = df.select_dtypes(include=["number"]).columns
    for col in num_cols:
        s = df[col]
        edges, counts = histogram_for_series(s)
        lb_iqr, ub_iqr = iqr_bounds(s)
        lb_z, ub_z = zscore_bounds(s)
        out[col] = {
            "histogram": {"edges": edges, "counts": counts},
            "outlier_ranges": {
                "iqr": {"lower": float(lb_iqr), "upper": float(ub_iqr)},
                "zscore": {"lower": float(lb_z), "upper": float(ub_z)},
            },
        }
    return out
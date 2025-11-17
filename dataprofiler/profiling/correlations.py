from typing import Dict
import numpy as np
import pandas as pd
from .helpers import cramer_v


def compute_correlations(df: pd.DataFrame) -> Dict:
    out = {
        "pearson_matrix": {},
        "spearman_matrix": {},
        "cramer_v_matrix": {},
    }
    num_cols = df.select_dtypes(include=["number"]).columns
    if len(num_cols) > 0:
        pear = df[num_cols].corr(method="pearson").fillna(0.0)
        spear = df[num_cols].corr(method="spearman").fillna(0.0)
        out["pearson_matrix"] = {c: {r: float(pear.loc[r, c]) for r in pear.index} for c in pear.columns}
        out["spearman_matrix"] = {c: {r: float(spear.loc[r, c]) for r in spear.index} for c in spear.columns}
    cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns
    cv: Dict[str, Dict[str, float]] = {}
    for i, c1 in enumerate(cat_cols):
        cv.setdefault(c1, {})
        for c2 in cat_cols:
            if c2 in cv and c1 in cv[c2]:
                cv[c1][c2] = cv[c2][c1]
                continue
            v = cramer_v(df[c1], df[c2])
            cv[c1][c2] = float(v)
    out["cramer_v_matrix"] = cv
    return out
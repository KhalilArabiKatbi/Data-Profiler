from typing import Dict, List, Optional
import pandas as pd
import numpy as np


def detect_zscore(df: pd.DataFrame, columns: Optional[List[str]] = None, threshold: float = 3.0, ddof: int = 0) -> Dict[str, Dict]:
    cols = columns or df.select_dtypes(include=["number"]).columns.tolist()
    out: Dict[str, Dict] = {}
    for col in cols:
        s = df[col].astype(float)
        mu = float(s.mean())
        sigma = float(s.std(ddof=ddof))
        if sigma == 0 or s.dropna().empty:
            out[col] = {"mean": mu, "std": sigma, "threshold": float(threshold), "indices": [], "count": 0}
            continue
        z = (s - mu) / sigma
        mask = z.abs() > threshold
        idx = df.index[mask.fillna(False)].tolist()
        out[col] = {"mean": mu, "std": sigma, "threshold": float(threshold), "indices": idx, "count": int(mask.sum())}
    return out
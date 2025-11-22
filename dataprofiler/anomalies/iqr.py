from typing import Dict, List, Optional
import pandas as pd


def detect_iqr(df: pd.DataFrame, columns: Optional[List[str]] = None, factor: float = 1.5) -> Dict[str, Dict]:
    cols = columns or df.select_dtypes(include=["number"]).columns.tolist()
    out: Dict[str, Dict] = {}
    for col in cols:
        s = df[col].dropna().astype(float)
        if s.empty:
            out[col] = {"lower": None, "upper": None, "indices": [], "count": 0}
            continue
        q1 = float(s.quantile(0.25))
        q3 = float(s.quantile(0.75))
        iqr = q3 - q1
        lower = q1 - factor * iqr
        upper = q3 + factor * iqr
        mask = (df[col] < lower) | (df[col] > upper)
        idx = df.index[mask].tolist()
        out[col] = {"lower": lower, "upper": upper, "indices": idx, "count": int(mask.sum())}
    return out
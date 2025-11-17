from typing import Dict
import pandas as pd
import numpy as np


def compute_datetime(df: pd.DataFrame) -> Dict[str, Dict]:
    out: Dict[str, Dict] = {}
    dt_cols = df.select_dtypes(include=["datetime", "datetimetz", "datetime64[ns]"]).columns
    for col in dt_cols:
        s = df[col].dropna()
        if s.empty:
            out[col] = {
                "min": None,
                "max": None,
                "earliest": None,
                "latest": None,
                "gaps": [],
                "weekday_distribution": {},
                "missing_pct": float(df[col].isna().mean() * 100.0),
            }
            continue
        mn = s.min()
        mx = s.max()
        wd = s.dt.weekday.value_counts()
        weekday_distribution = {int(k): int(v) for k, v in wd.items()}
        ss = s.sort_values()
        diffs = ss.diff().dropna()
        if diffs.empty:
            gaps = []
        else:
            med = diffs.median()
            thr = med * 5
            large = diffs[diffs > thr]
            gaps = []
            if not large.empty:
                idxs = large.index
                for i in range(len(idxs)):
                    end = ss.loc[idxs[i]]
                    j = ss.index.get_loc(idxs[i])
                    if j > 0:
                        start = ss.iloc[j - 1]
                        gaps.append({"start": str(start), "end": str(end), "delta": large.iloc[i].total_seconds()})
        out[col] = {
            "min": str(mn),
            "max": str(mx),
            "earliest": str(mn),
            "latest": str(mx),
            "gaps": gaps,
            "weekday_distribution": weekday_distribution,
            "missing_pct": float(df[col].isna().mean() * 100.0),
        }
    return out
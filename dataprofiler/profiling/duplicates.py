from typing import Dict, List
import pandas as pd


def compute_duplicates(df: pd.DataFrame) -> Dict:
    dup_rows_count = int(df.duplicated(keep="first").sum())
    total_rows = int(len(df))
    dup_rows_pct = float((dup_rows_count / total_rows) * 100.0) if total_rows > 0 else 0.0
    fingerprints = {}
    for col in df.columns:
        s = df[col]
        fp = hash(tuple(s.fillna("<NA>").tolist()))
        fingerprints.setdefault(fp, []).append(col)
    dup_cols: List[List[str]] = [cols for cols in fingerprints.values() if len(cols) > 1]
    return {
        "duplicate_rows_count": dup_rows_count,
        "duplicate_rows_percentage": dup_rows_pct,
        "duplicate_columns": dup_cols,
    }
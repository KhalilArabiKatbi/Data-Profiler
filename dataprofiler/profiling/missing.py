from typing import Dict, List, Tuple
from collections import Counter
import pandas as pd


def compute_missing(df: pd.DataFrame) -> Dict:
    per_column = {}
    for col in df.columns:
        miss = int(df[col].isna().sum())
        per_column[col] = {
            "missing_count": miss,
            "missing_pct": float(df[col].isna().mean() * 100.0),
        }
    total_missing_pct = float(df.isna().mean().mean() * 100.0)
    patterns: List[Tuple[List[str], int]] = []
    cols = list(df.columns)
    mask = df[cols].isna()
    combos = Counter()
    for i in range(len(df)):
        missing_cols = [c for c in cols if mask.at[i, c]]
        if missing_cols:
            combos[frozenset(missing_cols)] += 1
    for combo, count in combos.most_common(5):
        patterns.append((sorted(list(combo)), int(count)))
    return {
        "per_column": per_column,
        "overall_missing_pct": total_missing_pct,
        "patterns": patterns,
    }
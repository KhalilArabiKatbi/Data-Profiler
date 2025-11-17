from typing import Dict, List
import pandas as pd
from .helpers import entropy_from_counts


def compute_categorical(df: pd.DataFrame) -> Dict[str, Dict]:
    out: Dict[str, Dict] = {}
    cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns
    for col in cat_cols:
        s = df[col]
        vc = s.value_counts(dropna=True)
        frequencies = {str(k): int(v) for k, v in vc.items()}
        top_values: List[str] = [str(k) for k in vc.head(10).index.tolist()]
        cardinality = int(vc.shape[0])
        entropy = float(entropy_from_counts(frequencies))
        out[col] = {
            "cardinality": cardinality,
            "top_values": top_values,
            "frequencies": frequencies,
            "entropy": entropy,
            "missing_pct": float(s.isna().mean() * 100.0),
        }
    return out
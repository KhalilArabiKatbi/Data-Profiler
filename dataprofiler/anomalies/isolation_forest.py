from typing import Dict, List, Optional
import pandas as pd


def detect_isolation_forest(df: pd.DataFrame, columns: Optional[List[str]] = None, contamination: float = 0.01, random_state: Optional[int] = 42) -> Dict:
    try:
        from sklearn.ensemble import IsolationForest
    except Exception as e:
        raise ImportError("scikit-learn is required for isolation forest. Install with `pip install scikit-learn`") from e
    cols = columns or df.select_dtypes(include=["number"]).columns.tolist()
    X = df[cols].copy()
    for c in cols:
        med = X[c].median()
        X[c] = X[c].fillna(med)
    model = IsolationForest(n_estimators=100, contamination=contamination, random_state=random_state)
    model.fit(X.values)
    scores = model.decision_function(X.values)
    labels = model.predict(X.values)
    idx = df.index[labels == -1].tolist()
    return {"scores": list(scores), "labels": list(map(int, labels)), "indices": idx, "count": int((labels == -1).sum())}
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime


_MISSING = {"", "na", "n/a", "null", "none", "nan"}


def _normalize_missing(v: str) -> Optional[str]:
    s = v.strip()
    return None if s.lower() in _MISSING else s


def _to_bool(s: str) -> Optional[bool]:
    m = s.lower()
    if m in {"true", "yes", "1"}:
        return True
    if m in {"false", "no", "0"}:
        return False
    return None


def _to_int(s: str) -> Optional[int]:
    try:
        return int(s)
    except Exception:
        return None


def _to_float(s: str) -> Optional[float]:
    try:
        return float(s)
    except Exception:
        return None


_DATE_FORMATS = [
    "%Y-%m-%d",
    "%m/%d/%Y",
    "%d/%m/%Y",
    "%Y-%m-%d %H:%M:%S",
    "%d-%b-%Y",
    "%Y/%m/%d",
]


def _to_datetime(s: str) -> Optional[datetime]:
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            continue
    return None


def sanitize_rows(rows: List[Dict[str, str]], dtypes: Dict[str, str]) -> Tuple[List[Dict[str, Any]], int]:
    out: List[Dict[str, Any]] = []
    bad_rows = 0
    for r in rows:
        new_r: Dict[str, Any] = {}
        row_bad = False
        for col, dtype in dtypes.items():
            raw = str(r.get(col, ""))
            norm = _normalize_missing(raw)
            if norm is None:
                new_r[col] = None
                continue
            if dtype == "bool":
                val = _to_bool(norm)
            elif dtype == "int":
                val = _to_int(norm)
            elif dtype == "float":
                val = _to_float(norm)
            elif dtype == "datetime":
                val = _to_datetime(norm)
            else:
                val = norm
            if val is None and dtype in {"bool", "int", "float", "datetime"}:
                row_bad = True
            new_r[col] = val
        if row_bad:
            bad_rows += 1
        out.append(new_r)
    return out, bad_rows
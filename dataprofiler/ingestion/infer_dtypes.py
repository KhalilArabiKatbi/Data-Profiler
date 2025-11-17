import re
from typing import Dict, List, Iterable
from datetime import datetime


_INT_RE = re.compile(r"^[+-]?\d+$")
_FLOAT_RE = re.compile(r"^[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?$")
_BOOL_VALUES = {"true", "false", "yes", "no", "0", "1"}
_DATE_FORMATS = [
    "%Y-%m-%d",
    "%m/%d/%Y",
    "%d/%m/%Y",
    "%Y-%m-%d %H:%M:%S",
    "%d-%b-%Y",
    "%Y/%m/%d",
]


def _is_int(s: str) -> bool:
    return bool(_INT_RE.match(s))


def _is_float(s: str) -> bool:
    return bool(_FLOAT_RE.match(s))


def _is_bool(s: str) -> bool:
    return s.lower() in _BOOL_VALUES


def _is_datetime(s: str) -> bool:
    for fmt in _DATE_FORMATS:
        try:
            datetime.strptime(s, fmt)
            return True
        except Exception:
            continue
    return False


def infer_dtypes(rows: List[Dict[str, str]], columns: List[str], max_rows: int = 500) -> Dict[str, str]:
    sample = rows[:max_rows]
    dtypes: Dict[str, str] = {}
    for col in columns:
        values: Iterable[str] = (str(r.get(col, "")).strip() for r in sample)
        non_empty = [v for v in values if v != ""]
        if not non_empty:
            dtypes[col] = "string"
            continue
        checks = {
            "bool": sum(_is_bool(v) for v in non_empty),
            "int": sum(_is_int(v) for v in non_empty),
            "float": sum(_is_float(v) for v in non_empty),
            "datetime": sum(_is_datetime(v) for v in non_empty),
        }
        n = len(non_empty)
        if checks["datetime"] / n > 0.8:
            dtypes[col] = "datetime"
        elif checks["bool"] / n > 0.9:
            dtypes[col] = "bool"
        elif checks["int"] / n > 0.9:
            dtypes[col] = "int"
        elif (checks["float"] + checks["int"]) / n > 0.9:
            dtypes[col] = "float"
        else:
            unique = len(set(non_empty))
            if unique <= 20 and unique / max(1, n) <= 0.1:
                dtypes[col] = "category"
            else:
                dtypes[col] = "string"
    return dtypes
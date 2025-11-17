from dataclasses import dataclass, field
from typing import Dict, List, Any
import pandas as pd

from .helpers import detect_column_types, memory_usage_bytes
from .statistics import compute_numeric
from .missing import compute_missing
from .duplicates import compute_duplicates
from .categories import compute_categorical
from .correlations import compute_correlations
from .datetime_profile import compute_datetime
from .distributions import compute_distributions


@dataclass
class DatasetStats:
    rows: int
    columns: int
    memory_usage: int
    column_types: Dict[str, str]


@dataclass
class Correlations:
    pearson_matrix: Dict[str, Dict[str, float]]
    spearman_matrix: Dict[str, Dict[str, float]]
    cramer_v_matrix: Dict[str, Dict[str, float]]


@dataclass
class DuplicatesSummary:
    duplicate_rows_count: int
    duplicate_rows_percentage: float
    duplicate_columns: List[List[str]]


@dataclass
class OverallMissingness:
    total_missing_pct: float


@dataclass
class ProfileResult:
    dataset_stats: DatasetStats
    numeric_columns: Dict[str, Dict[str, Any]]
    categorical_columns: Dict[str, Dict[str, Any]]
    datetime_columns: Dict[str, Dict[str, Any]]
    correlations: Correlations
    duplicates: DuplicatesSummary
    overall_missingness: OverallMissingness


def combine_into_profile_result(df: pd.DataFrame) -> ProfileResult:
    ct = detect_column_types(df)
    ds = DatasetStats(
        rows=int(len(df)),
        columns=int(df.shape[1]),
        memory_usage=memory_usage_bytes(df),
        column_types=ct,
    )
    numeric_stats = compute_numeric(df)
    categorical_stats = compute_categorical(df)
    datetime_stats = compute_datetime(df)
    missing_stats = compute_missing(df)
    dup_stats = compute_duplicates(df)
    correlations = compute_correlations(df)
    distributions = compute_distributions(df)
    for col, dist in distributions.items():
        if col in numeric_stats:
            numeric_stats[col].update(dist)
    corr = Correlations(
        pearson_matrix=correlations.get("pearson_matrix", {}),
        spearman_matrix=correlations.get("spearman_matrix", {}),
        cramer_v_matrix=correlations.get("cramer_v_matrix", {}),
    )
    dups = DuplicatesSummary(
        duplicate_rows_count=dup_stats["duplicate_rows_count"],
        duplicate_rows_percentage=dup_stats["duplicate_rows_percentage"],
        duplicate_columns=dup_stats["duplicate_columns"],
    )
    overall = OverallMissingness(total_missing_pct=missing_stats["overall_missing_pct"]) 
    return ProfileResult(
        dataset_stats=ds,
        numeric_columns=numeric_stats,
        categorical_columns=categorical_stats,
        datetime_columns=datetime_stats,
        correlations=corr,
        duplicates=dups,
        overall_missingness=overall,
    )


def profile_data(df: pd.DataFrame) -> ProfileResult:
    return combine_into_profile_result(df)
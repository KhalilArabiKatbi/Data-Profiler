from typing import Dict
import pandas as pd

from dataprofiler.utils import detect_column_types, memory_usage_bytes
from dataprofiler.model import DatasetStats, Correlations, DuplicatesSummary, OverallMissingness, ProfileResult
from .statistics import compute_numeric
from .missing import compute_missing
from .duplicates import compute_duplicates
from .categories import compute_categorical
from .correlations import compute_correlations
from .datetime_profile import compute_datetime


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
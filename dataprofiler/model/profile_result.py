from dataclasses import dataclass
from typing import Dict, List, Any


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
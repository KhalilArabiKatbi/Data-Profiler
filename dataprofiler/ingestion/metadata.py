from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime


@dataclass
class FileMetadata:
    path: str
    size_bytes: int
    modified_at: datetime
    encoding: str
    delimiter: str
    has_header: bool
    columns: List[str] = field(default_factory=list)


@dataclass
class IngestionStats:
    rows_read: int
    bad_rows: int


@dataclass
class IngestionResult:
    rows: List[Dict[str, Any]]
    metadata: FileMetadata
    stats: IngestionStats
    dtypes: Dict[str, str]
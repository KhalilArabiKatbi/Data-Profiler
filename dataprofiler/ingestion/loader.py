import csv
import os
from typing import List, Dict, Any
from datetime import datetime

from .validators import ensure_path_exists, ensure_extension_allowed, sample_file, is_probably_text
from .detect_encoding import detect_encoding
from .detect_delimiter import detect_delimiter_and_header
from .infer_dtypes import infer_dtypes
from .sanitizer import sanitize_rows
from .metadata import FileMetadata, IngestionStats, IngestionResult


def load_data(path: str, sample_size: int = 8192) -> IngestionResult:
    ensure_path_exists(path)
    ensure_extension_allowed(path)

    sample = sample_file(path, sample_size)
    if not is_probably_text(sample):
        raise ValueError("File does not appear to be a text-based delimited file")

    encoding = detect_encoding(sample)
    sample_text = sample.decode(encoding, errors="replace")
    delimiter, has_header = detect_delimiter_and_header(sample_text)

    rows: List[Dict[str, str]] = []
    columns: List[str] = []
    with open(path, "r", encoding=encoding, newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        if has_header:
            try:
                columns = next(reader)
            except StopIteration:
                columns = []
        for i, row in enumerate(reader):
            if not columns:
                columns = [f"col_{j+1}" for j in range(len(row))]
            record = {columns[j]: (row[j] if j < len(row) else "") for j in range(len(columns))}
            rows.append(record)

    dtypes = infer_dtypes(rows, columns)
    typed_rows, bad_rows = sanitize_rows(rows, dtypes)

    size_bytes = os.path.getsize(path)
    modified_at = datetime.fromtimestamp(os.path.getmtime(path))

    meta = FileMetadata(
        path=path,
        size_bytes=size_bytes,
        modified_at=modified_at,
        encoding=encoding,
        delimiter=delimiter,
        has_header=has_header,
        columns=columns,
    )
    stats = IngestionStats(rows_read=len(rows), bad_rows=bad_rows)
    return IngestionResult(rows=typed_rows, metadata=meta, stats=stats, dtypes=dtypes)
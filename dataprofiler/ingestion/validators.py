import os
from typing import Optional


def ensure_path_exists(path: str) -> None:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")


def ensure_extension_allowed(path: str, allowed: Optional[set] = None) -> None:
    allowed = allowed or {"csv", "tsv", "txt"}
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    if ext not in allowed:
        raise ValueError(f"Unsupported file extension: .{ext}")


def sample_file(path: str, max_bytes: int = 8192) -> bytes:
    with open(path, "rb") as f:
        return f.read(max_bytes)


def is_probably_text(sample: bytes) -> bool:
    if b"\x00" in sample:
        return False
    return True
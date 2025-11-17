import csv
from typing import Tuple

def detect_delimiter_and_header(sample_text: str) -> Tuple[str, bool]:
    try:
        sniffer = csv.Sniffer()
        
        # FIX 1: delimiters must be a string, not a list
        dialect = sniffer.sniff(sample_text, delimiters=";,|\t")
        delim = dialect.delimiter
        
        try:
            has_header = sniffer.has_header(sample_text)
        except Exception:
            has_header = False
        
        return delim, has_header

    except Exception:
        lines = sample_text.splitlines()
        first_line = lines[0] if lines else ""

        candidates = [",", ";", "\t", "|"]
        counts = {c: first_line.count(c) for c in candidates}

        # FIX 2: use lambda to avoid Pylance overload conflict
        delim = max(counts.keys(), key=lambda c: counts[c]) if counts else ","

        return delim, False

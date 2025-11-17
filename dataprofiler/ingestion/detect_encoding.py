def detect_encoding(sample: bytes) -> str:
    candidates = [
        "utf-8",
        "utf-8-sig",
        "utf-16",
        "utf-16le",
        "utf-16be",
        "latin-1",
        "ascii",
    ]
    for enc in candidates:
        try:
            sample.decode(enc)
            return enc
        except Exception:
            continue
    return "utf-8"
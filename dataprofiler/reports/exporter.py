import json
from pathlib import Path
from dataclasses import asdict, is_dataclass


def export_html(html: str, path: str) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")
    return str(p)


def export_json(profile_result, path: str) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if is_dataclass(profile_result):
        data = asdict(profile_result)
    else:
        try:
            data = profile_result.as_dict()
        except Exception:
            data = {}
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(p)


def export_pdf(html_path: str, pdf_path: str) -> str:
    try:
        from weasyprint import HTML
    except Exception as e:
        raise ImportError("WeasyPrint is required for PDF export. Install with `pip install weasyprint`.") from e
    src = Path(html_path)
    dst = Path(pdf_path)
    dst.parent.mkdir(parents=True, exist_ok=True)
    HTML(filename=str(src)).write_pdf(str(dst))
    return str(dst)
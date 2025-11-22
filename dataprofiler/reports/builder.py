from pathlib import Path
from typing import Any, Dict

from .charts import histogram_html, correlation_heatmap_html


def _load_template() -> str:
    base = Path(__file__).resolve().parent / "templates"
    tpl = (base / "report.html").read_text(encoding="utf-8")
    return tpl


def _ensure_assets(output_dir: Path) -> None:
    src = Path(__file__).resolve().parent / "templates" / "style.css"
    dst = output_dir / "style.css"
    output_dir.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")


def _summary_section(profile) -> str:
    ds = profile.dataset_stats
    rows = [
        ("Rows", ds.rows),
        ("Columns", ds.columns),
        ("Memory Usage (bytes)", ds.memory_usage),
    ]
    table = "<table><tr><th>Metric</th><th>Value</th></tr>" + "".join(
        f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in rows
    ) + "</table"
    types_table = "<table><tr><th>Column</th><th>Type</th></tr>" + "".join(
        f"<tr><td>{c}</td><td>{t}</td></tr>" for c, t in ds.column_types.items()
    ) + "</table>"
    return "<div class=\"card\"><div class=\"section-title\">Dataset</div>" + table + types_table + "</div>"


def _numeric_section(profile) -> str:
    items = []
    for col, stats in profile.numeric_columns.items():
        rows = [
            ("Mean", stats.get("mean")),
            ("Median", stats.get("median")),
            ("Mode", ", ".join(map(str, stats.get("mode", [])))),
            ("Std", stats.get("std")),
            ("Variance", stats.get("variance")),
            ("Skewness", stats.get("skewness")),
            ("Kurtosis", stats.get("kurtosis")),
            ("Q25", stats.get("quantiles", {}).get("q25")),
            ("Q50", stats.get("quantiles", {}).get("q50")),
            ("Q75", stats.get("quantiles", {}).get("q75")),
            ("Missing %", stats.get("missing_pct")),
        ]
        table = "<table><tr><th>Metric</th><th>Value</th></tr>" + "".join(
            f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in rows
        ) + "</table>"
        hist = stats.get("histogram", {})
        edges = hist.get("edges", [])
        counts = hist.get("counts", [])
        hhtml = histogram_html(col, edges, counts)
        items.append("<div class=\"card\"><div class=\"subhdr\">" + col + "</div>" + table + hhtml + "</div>")
    return "<div class=\"section-title\">Numeric Columns</div><div class=\"grid\">" + "".join(items) + "</div>"


def _categorical_section(profile) -> str:
    items = []
    for col, stats in profile.categorical_columns.items():
        rows = [
            ("Cardinality", stats.get("cardinality")),
            ("Entropy", stats.get("entropy")),
            ("Missing %", stats.get("missing_pct")),
        ]
        table = "<table><tr><th>Metric</th><th>Value</th></tr>" + "".join(
            f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in rows
        ) + "</table>"
        freq = stats.get("frequencies", {})
        ftable = "<table><tr><th>Value</th><th>Count</th></tr>" + "".join(
            f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in list(freq.items())[:20]
        ) + "</table>"
        items.append("<div class=\"card\"><div class=\"subhdr\">" + col + "</div>" + table + ftable + "</div>")
    return "<div class=\"section-title\">Categorical Columns</div><div class=\"grid\">" + "".join(items) + "</div>"


def _datetime_section(profile) -> str:
    items = []
    for col, stats in profile.datetime_columns.items():
        rows = [
            ("Earliest", stats.get("earliest")),
            ("Latest", stats.get("latest")),
            ("Missing %", stats.get("missing_pct")),
        ]
        table = "<table><tr><th>Metric</th><th>Value</th></tr>" + "".join(
            f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in rows
        ) + "</table>"
        wd = stats.get("weekday_distribution", {})
        wtable = "<table><tr><th>Weekday</th><th>Count</th></tr>" + "".join(
            f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in wd.items()
        ) + "</table>"
        items.append("<div class=\"card\"><div class=\"subhdr\">" + col + "</div>" + table + wtable + "</div>")
    return "<div class=\"section-title\">Datetime Columns</div><div class=\"grid\">" + "".join(items) + "</div>"


def _correlations_section(profile) -> str:
    pm = profile.correlations.pearson_matrix
    heat = correlation_heatmap_html(pm)
    return "<div class=\"section-title\">Correlations (Pearson)</div>" + heat


def _duplicates_section(profile) -> str:
    d = profile.duplicates
    rows = [
        ("Duplicate Rows", d.duplicate_rows_count),
        ("Duplicate Rows %", d.duplicate_rows_percentage),
    ]
    table = "<table><tr><th>Metric</th><th>Value</th></tr>" + "".join(
        f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in rows
    ) + "</table>"
    groups = d.duplicate_columns
    gtable = "<table><tr><th>Columns</th></tr>" + "".join(
        f"<tr><td>{', '.join(g)}</td></tr>" for g in groups
    ) + "</table>"
    return "<div class=\"section-title\">Duplicates</div>" + table + gtable


def _missing_section(profile) -> str:
    pct = profile.overall_missingness.total_missing_pct
    card = "<div class=\"kpi\"><div class=\"item\"><div class=\"label\">Overall Missing %</div><div class=\"value\">" + str(round(float(pct), 2)) + "%</div></div></div>"
    return "<div class=\"section-title\">Missingness</div>" + card


def build_report(profile, output_dir: str = None, title: str = "Data Profile") -> str:
    tpl = _load_template()
    content = []
    content.append(_summary_section(profile))
    content.append(_missing_section(profile))
    content.append(_numeric_section(profile))
    content.append(_categorical_section(profile))
    content.append(_datetime_section(profile))
    content.append(_correlations_section(profile))
    html = tpl.replace("{{title}}", title).replace("{{content}}", "".join(content))
    if output_dir:
        out_dir = Path(output_dir)
        _ensure_assets(out_dir)
        (out_dir / "report.html").write_text(html, encoding="utf-8")
    return html
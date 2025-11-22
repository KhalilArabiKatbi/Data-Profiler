from typing import Dict, List


def histogram_html(col: str, edges: List[float], counts: List[int]) -> str:
    if not edges or not counts:
        return f"<div class=\"histogram\"><div class=\"hist-title\">{col}</div><div class=\"hist-empty\">No data</div></div>"
    m = max(counts) if counts else 1
    bars = []
    for i, c in enumerate(counts):
        width = int(200 * (c / m))
        label = f"[{edges[i]:.2f}, {edges[i+1]:.2f}]"
        bars.append(f"<div class=\"bar\"><div class=\"bar-label\">{label}</div><div class=\"bar-fill\" style=\"width:{width}px\"></div><div class=\"bar-count\">{c}</div></div>")
    inner = "".join(bars)
    return f"<div class=\"histogram\"><div class=\"hist-title\">{col}</div>{inner}</div>"


def correlation_heatmap_html(matrix: Dict[str, Dict[str, float]]) -> str:
    labels = list(matrix.keys())
    if not labels:
        return "<div class=\"heatmap\">No data</div>"
    header = "<tr><th></th>" + "".join(f"<th>{c}</th>" for c in labels) + "</tr>"
    rows = []
    for r in labels:
        cells = [f"<th>{r}</th>"]
        for c in labels:
            v = float(matrix.get(r, {}).get(c, 0.0))
            x = max(min(v, 1.0), -1.0)
            if x >= 0:
                a = int(255 * x)
                color = f"rgba(0, 128, 255, {abs(x)})"
            else:
                color = f"rgba(255, 64, 64, {abs(x)})"
            cells.append(f"<td style=\"background-color:{color}\">{x:.2f}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    body = "".join(rows)
    return f"<table class=\"heatmap\">{header}{body}</table>"
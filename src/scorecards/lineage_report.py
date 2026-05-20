from __future__ import annotations

import json

import pandas as pd

from src.common.paths import ensure_dir, project_path
from src.semantic.metric_loader import load_metric_definitions


def write_lineage_completeness_report(nodes: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    """Write lineage completeness report."""
    rows = []
    for metric in load_metric_definitions():
        has_sources = bool((edges["target"] == metric["metric_name"]).any())
        has_consumers = bool((edges["source"] == metric["metric_name"]).any())
        score = (has_sources + has_consumers + bool(metric["owner"])) / 3 * 100
        rows.append(
            {
                "metric_id": metric["metric_id"],
                "metric_name": metric["metric_name"],
                "lineage_completeness_score": round(score, 2),
                "has_sources": has_sources,
                "has_consumers": has_consumers,
            }
        )
    report = pd.DataFrame(rows)
    out = ensure_dir(project_path("data/scorecards"))
    report.to_csv(out / "lineage_completeness_report.csv", index=False)
    summary = {"average_lineage_completeness": round(float(report["lineage_completeness_score"].mean()), 2)}
    (out / "lineage_completeness_report.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=2), encoding="utf-8")
    return report

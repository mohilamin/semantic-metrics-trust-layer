from __future__ import annotations

import json

import pandas as pd

from src.common.paths import ensure_dir, project_path


def write_metric_consistency_report(reconciliation: pd.DataFrame | None = None) -> pd.DataFrame:
    """Write metric consistency report."""
    report = reconciliation if reconciliation is not None else pd.read_csv(project_path("data/metrics/metric_reconciliation_results.csv"))
    out = ensure_dir(project_path("data/scorecards"))
    report.to_csv(out / "metric_consistency_report.csv", index=False)
    summary = {"conflict_count": int(report["conflict_detected"].sum()), "metrics_compared": int(report["metric_name"].nunique())}
    (out / "metric_consistency_report.json").write_text(
        json.dumps({"summary": summary, "rows": report.to_dict(orient="records")}, indent=2), encoding="utf-8"
    )
    return report

from __future__ import annotations

import json

import pandas as pd

from src.common.paths import ensure_dir, project_path


def detect_metric_drift(reconciliation: pd.DataFrame | None = None) -> pd.DataFrame:
    """Create metric drift report from reconciliation variance."""
    recon = reconciliation if reconciliation is not None else pd.read_csv(project_path("data/metrics/metric_reconciliation_results.csv"))
    report = recon.copy()
    report["drift_severity"] = pd.cut(
        report["variance_pct"], bins=[-1, 5, 20, 100, float("inf")], labels=["none", "low", "medium", "high"]
    ).astype(str)
    out = ensure_dir(project_path("data/scorecards"))
    report.to_csv(out / "metric_drift_report.csv", index=False)
    summary = {
        "drifted_metrics": int((report["drift_severity"] != "none").sum()),
        "high_drift_metrics": int((report["drift_severity"] == "high").sum()),
    }
    (out / "metric_drift_report.json").write_text(
        json.dumps({"summary": summary, "rows": report.to_dict(orient="records")}, indent=2), encoding="utf-8"
    )
    return report

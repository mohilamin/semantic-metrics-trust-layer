from __future__ import annotations

import pandas as pd

from src.common.config import settings
from src.common.paths import ensure_dir, project_path


def reconcile_metrics(certified: pd.DataFrame | None = None, uncertified: pd.DataFrame | None = None) -> pd.DataFrame:
    """Compare certified and uncertified metric values."""
    metrics_dir = project_path("data/metrics")
    cert = certified if certified is not None else pd.read_csv(metrics_dir / "certified_metric_results.csv")
    uncert = uncertified if uncertified is not None else pd.read_csv(metrics_dir / "uncertified_metric_results.csv")
    rows = []
    for _, row in uncert.iterrows():
        match = cert.loc[cert["metric_name"] == row["metric_name"]]
        if match.empty:
            continue
        certified_value = float(match.iloc[0]["metric_value"])
        uncertified_value = float(row["metric_value"])
        variance = uncertified_value - certified_value
        variance_pct = abs(variance) / max(abs(certified_value), 1) * 100
        rows.append(
            {
                "metric_name": row["metric_name"],
                "definition_name": row["definition_name"],
                "certified_value": certified_value,
                "uncertified_value": uncertified_value,
                "variance": round(variance, 4),
                "variance_pct": round(variance_pct, 4),
                "conflict_detected": bool(variance_pct > settings().get("drift_threshold_pct", 5.0)),
            }
        )
    report = pd.DataFrame(rows)
    report.to_csv(ensure_dir(metrics_dir) / "metric_reconciliation_results.csv", index=False)
    return report

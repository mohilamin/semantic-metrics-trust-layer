from __future__ import annotations

import pandas as pd

from src.common.paths import ensure_dir, project_path
from src.common.time import utc_now_iso
from src.metrics_engine.certified_metrics import calculate_certified_values
from src.metrics_engine.uncertified_metrics import calculate_uncertified_values
from src.semantic.metric_loader import load_metric_definitions


def calculate_metrics() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calculate certified and uncertified metric result tables."""
    metric_defs = {metric["metric_name"]: metric for metric in load_metric_definitions()}
    certified_values = calculate_certified_values()
    uncertified_values, _ = calculate_uncertified_values()
    run_id = f"RUN-{pd.Timestamp.utcnow().strftime('%Y%m%d%H%M%S')}"
    certified_rows = []
    for name, value in certified_values.items():
        definition = metric_defs[name]
        certified_rows.append(
            {
                "run_id": run_id,
                "metric_id": definition["metric_id"],
                "metric_name": name,
                "metric_value": round(float(value), 4),
                "grain": definition["grain"],
                "certification_status": definition["certification_status"],
                "calculated_at": utc_now_iso(),
            }
        )
    uncertified_rows = [
        {
            "run_id": run_id,
            "metric_name": key.replace("_sales", ""),
            "definition_name": key,
            "metric_value": round(float(value), 4),
            "certification_status": "uncertified",
            "calculated_at": utc_now_iso(),
        }
        for key, value in uncertified_values.items()
    ]
    out = ensure_dir(project_path("data/metrics"))
    certified = pd.DataFrame(certified_rows)
    uncertified = pd.DataFrame(uncertified_rows)
    certified.to_csv(out / "certified_metric_results.csv", index=False)
    uncertified.to_csv(out / "uncertified_metric_results.csv", index=False)
    pd.DataFrame([{"run_id": run_id, "metrics_calculated": len(certified), "calculated_at": utc_now_iso()}]).to_csv(
        out / "metric_run_history.csv", index=False
    )
    return certified, uncertified


if __name__ == "__main__":
    calculate_metrics()

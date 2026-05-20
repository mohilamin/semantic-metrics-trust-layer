from __future__ import annotations

import json

import pandas as pd

from src.common.paths import ensure_dir, project_path


def write_semantic_layer_health_summary() -> dict[str, object]:
    """Write semantic layer health summary."""
    trust = pd.read_csv(project_path("data/scorecards/metric_trust_scorecard.csv"))
    ai = pd.read_csv(project_path("data/scorecards/ai_agent_metric_readiness_report.csv"))
    data_contracts = pd.read_csv(project_path("data/scorecards/data_contract_validation_report.csv"))
    metric_contracts = pd.read_csv(project_path("data/scorecards/metric_contract_validation_report.csv"))
    consistency = pd.read_csv(project_path("data/scorecards/metric_consistency_report.csv"))
    summary = {
        "total_metrics": int(len(trust)),
        "average_trust_score": round(float(trust["trust_score"].mean()), 2),
        "trusted_metrics": int((trust["trust_tier"] == "trusted").sum()),
        "ai_safe_metrics": int(ai["safe_for_ai_agent"].sum()),
        "data_contract_pass_rate": round(float((data_contracts["status"] == "pass").mean() * 100), 2),
        "metric_contract_pass_rate": round(float((metric_contracts["status"] == "pass").mean() * 100), 2),
        "metric_conflicts": int(consistency["conflict_detected"].sum()),
    }
    out = ensure_dir(project_path("data/scorecards"))
    pd.DataFrame([summary]).to_csv(out / "semantic_layer_health_summary.csv", index=False)
    (out / "semantic_layer_health_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary

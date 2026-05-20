from __future__ import annotations

import json

import pandas as pd

from src.common.paths import ensure_dir, project_path
from src.semantic.metric_loader import load_metric_definitions


def calculate_metric_trust_scores(
    data_contracts: pd.DataFrame | None = None,
    metric_contracts: pd.DataFrame | None = None,
    drift: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Calculate explainable metric trust scores."""
    data_report = (
        data_contracts if data_contracts is not None else pd.read_csv(project_path("data/scorecards/data_contract_validation_report.csv"))
    )
    metric_report = (
        metric_contracts
        if metric_contracts is not None
        else pd.read_csv(project_path("data/scorecards/metric_contract_validation_report.csv"))
    )
    drift_report = drift if drift is not None else pd.read_csv(project_path("data/scorecards/metric_drift_report.csv"))
    data_pass = float((data_report["status"] == "pass").mean() * 100)
    rows = []
    for metric in load_metric_definitions():
        metric_checks = metric_report.loc[metric_report["metric_name"] == metric["metric_name"]]
        contract_pass = float((metric_checks["status"] == "pass").mean() * 100)
        conflict_count = int((drift_report["metric_name"] == metric["metric_name"]).sum())
        high_drift = int(((drift_report["metric_name"] == metric["metric_name"]) & (drift_report["drift_severity"] == "high")).sum())
        score = (
            data_pass * 0.15
            + contract_pass * 0.20
            + 100 * 0.10
            + (100 if metric["owner"] else 0) * 0.10
            + (100 if metric["certification_status"] == "certified" else 40) * 0.15
            + max(0, 100 - conflict_count * 18) * 0.15
            + max(0, 100 - high_drift * 40) * 0.10
            + (100 if metric.get("business_definition") and metric.get("examples") else 60) * 0.05
        )
        rows.append(
            {
                "metric_id": metric["metric_id"],
                "metric_name": metric["metric_name"],
                "owner": metric["owner"],
                "domain": metric["domain"],
                "trust_score": round(score, 2),
                "data_contract_pass_rate": round(data_pass, 2),
                "metric_contract_pass_rate": round(contract_pass, 2),
                "conflict_count": conflict_count,
                "high_drift_count": high_drift,
                "certification_status": metric["certification_status"],
                "trust_tier": "trusted" if score >= 85 else "watch" if score >= 70 else "not_trusted",
            }
        )
    scorecard = pd.DataFrame(rows)
    out = ensure_dir(project_path("data/scorecards"))
    scorecard.to_csv(out / "metric_trust_scorecard.csv", index=False)
    summary = {
        "average_trust_score": round(float(scorecard["trust_score"].mean()), 2),
        "trusted_metrics": int((scorecard["trust_tier"] == "trusted").sum()),
    }
    (out / "metric_trust_scorecard.json").write_text(json.dumps({"summary": summary, "metrics": rows}, indent=2), encoding="utf-8")
    return scorecard

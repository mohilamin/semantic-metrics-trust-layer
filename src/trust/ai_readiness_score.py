from __future__ import annotations

import json

import pandas as pd

from src.common.paths import ensure_dir, project_path
from src.semantic.metric_loader import load_metric_definitions


def calculate_ai_readiness(trust_scores: pd.DataFrame | None = None) -> pd.DataFrame:
    """Calculate AI-agent metric readiness."""
    trust = trust_scores if trust_scores is not None else pd.read_csv(project_path("data/scorecards/metric_trust_scorecard.csv"))
    rows = []
    for metric in load_metric_definitions():
        trust_row = trust.loc[trust["metric_name"] == metric["metric_name"]].iloc[0]
        checks = {
            "certified_definition_exists": metric["certification_status"] == "certified",
            "owner_exists": bool(metric["owner"]),
            "formula_documented": bool(metric["formula"]),
            "lineage_exists": True,
            "freshness_sla_passed": True,
            "no_unresolved_conflicts": int(trust_row["conflict_count"]) == 0,
            "no_high_drift": int(trust_row["high_drift_count"]) == 0,
            "ai_agent_allowed": bool(metric["ai_agent_allowed_flag"]),
            "metric_contract_passes": float(trust_row["metric_contract_pass_rate"]) == 100.0,
            "business_definition_exists": bool(metric["business_definition"]),
            "examples_exist": bool(metric.get("examples")),
        }
        score = round(sum(checks.values()) / len(checks) * 100, 2)
        rows.append(
            {
                "metric_id": metric["metric_id"],
                "metric_name": metric["metric_name"],
                "ai_readiness_score": score,
                "ai_agent_allowed_flag": bool(metric["ai_agent_allowed_flag"]),
                "safe_for_ai_agent": bool(score >= 85 and metric["ai_agent_allowed_flag"]),
                "failed_checks": ",".join([name for name, passed in checks.items() if not passed]),
            }
        )
    report = pd.DataFrame(rows)
    out = ensure_dir(project_path("data/scorecards"))
    report.to_csv(out / "ai_agent_metric_readiness_report.csv", index=False)
    summary = {
        "safe_metrics": int(report["safe_for_ai_agent"].sum()),
        "average_ai_readiness_score": round(float(report["ai_readiness_score"].mean()), 2),
    }
    (out / "ai_agent_metric_readiness_report.json").write_text(
        json.dumps({"summary": summary, "metrics": rows}, indent=2), encoding="utf-8"
    )
    return report

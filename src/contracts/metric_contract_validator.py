from __future__ import annotations

import json

import pandas as pd

from src.common.config import load_yaml
from src.common.paths import ensure_dir, project_path


def validate_metric_contracts() -> pd.DataFrame:
    """Validate metric definitions against contract requirements."""
    contract = load_yaml("config/metric_contracts.yaml")
    metrics = load_yaml("config/metric_definitions.yaml")["metrics"]
    rows: list[dict[str, object]] = []
    for metric in metrics:
        missing = [field for field in contract["required_fields"] if field not in metric or metric[field] in [None, "", []]]
        rows.append(
            {
                "metric_id": metric["metric_id"],
                "metric_name": metric["metric_name"],
                "check_type": "required_fields",
                "status": "pass" if not missing else "fail",
                "severity": "critical",
                "expected_value": ",".join(contract["required_fields"]),
                "actual_value": "missing:" + ",".join(missing) if missing else "complete",
                "recommended_action": "Complete metric contract." if missing else "No action.",
            }
        )
        rows.append(
            {
                "metric_id": metric["metric_id"],
                "metric_name": metric["metric_name"],
                "check_type": "approval_status",
                "status": "pass" if metric["approval_status"] in contract["allowed_approval_statuses"] else "fail",
                "severity": "high",
                "expected_value": ",".join(contract["allowed_approval_statuses"]),
                "actual_value": metric["approval_status"],
                "recommended_action": "Route metric through approval workflow."
                if metric["approval_status"] != "approved"
                else "No action.",
            }
        )
        rows.append(
            {
                "metric_id": metric["metric_id"],
                "metric_name": metric["metric_name"],
                "check_type": "certification_status",
                "status": "pass" if metric["certification_status"] == "certified" else "fail",
                "severity": "high",
                "expected_value": "certified",
                "actual_value": metric["certification_status"],
                "recommended_action": "Certify or deprecate metric." if metric["certification_status"] != "certified" else "No action.",
            }
        )
    report = pd.DataFrame(rows)
    out = ensure_dir(project_path("data/scorecards"))
    report.to_csv(out / "metric_contract_validation_report.csv", index=False)
    summary = {
        "total_checks": len(report),
        "passed_checks": int((report["status"] == "pass").sum()),
        "pass_rate": round(float((report["status"] == "pass").mean() * 100), 2),
    }
    (out / "metric_contract_validation_report.json").write_text(
        json.dumps({"summary": summary, "checks": rows}, indent=2), encoding="utf-8"
    )
    return report


if __name__ == "__main__":
    validate_metric_contracts()

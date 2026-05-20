from __future__ import annotations

import json

import pandas as pd

from src.common.config import load_yaml
from src.common.paths import ensure_dir, project_path
from src.ingestion.loaders import load_raw_tables


def validate_data_contracts(frames: dict[str, pd.DataFrame] | None = None) -> pd.DataFrame:
    """Validate source data contracts and write reports."""
    data = frames or load_raw_tables()
    contracts = load_yaml("config/data_contracts.yaml")
    rows: list[dict[str, object]] = []
    for table, spec in contracts["tables"].items():
        frame = data[table]
        required = spec["required_columns"]
        missing = sorted(set(required) - set(frame.columns))
        key = spec["unique_key"]
        rows.append(
            {
                "table_name": table,
                "check_type": "required_columns",
                "status": "pass" if not missing else "fail",
                "severity": "critical",
                "expected_value": ",".join(required),
                "actual_value": ",".join(frame.columns),
                "affected_rows": 0,
                "affected_columns": ",".join(missing),
                "recommended_action": "Update source or contract before certification." if missing else "No action.",
            }
        )
        duplicate_count = int(frame[key].duplicated().sum()) if key in frame else len(frame)
        rows.append(
            {
                "table_name": table,
                "check_type": "uniqueness",
                "status": "pass" if duplicate_count == 0 else "fail",
                "severity": "high",
                "expected_value": "unique",
                "actual_value": str(duplicate_count),
                "affected_rows": duplicate_count,
                "affected_columns": key,
                "recommended_action": "Deduplicate source records." if duplicate_count else "No action.",
            }
        )
        null_rate = float(frame[required].isna().mean().max()) if not missing else 1.0
        rows.append(
            {
                "table_name": table,
                "check_type": "null_rate",
                "status": "pass" if null_rate <= contracts["defaults"]["allowed_null_rate"] else "fail",
                "severity": "medium",
                "expected_value": str(contracts["defaults"]["allowed_null_rate"]),
                "actual_value": f"{null_rate:.4f}",
                "affected_rows": int(frame[required].isna().any(axis=1).sum()) if not missing else len(frame),
                "affected_columns": "",
                "recommended_action": "Review null source fields." if null_rate else "No action.",
            }
        )
        rows.append(
            {
                "table_name": table,
                "check_type": "row_count",
                "status": "pass" if len(frame) > 0 else "fail",
                "severity": "critical",
                "expected_value": ">0",
                "actual_value": str(len(frame)),
                "affected_rows": 0 if len(frame) > 0 else 1,
                "affected_columns": "",
                "recommended_action": "Investigate missing source load." if len(frame) == 0 else "No action.",
            }
        )
    report = pd.DataFrame(rows)
    out = ensure_dir(project_path("data/scorecards"))
    report.to_csv(out / "data_contract_validation_report.csv", index=False)
    summary = {
        "total_checks": len(report),
        "passed_checks": int((report["status"] == "pass").sum()),
        "pass_rate": round(float((report["status"] == "pass").mean() * 100), 2),
    }
    (out / "data_contract_validation_report.json").write_text(json.dumps({"summary": summary, "checks": rows}, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    validate_data_contracts()

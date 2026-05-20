from __future__ import annotations

import pandas as pd

from src.common.paths import ensure_dir, project_path
from src.common.time import utc_now_iso
from src.semantic.metric_loader import load_metric_definitions


def simulate_approval_workflow() -> pd.DataFrame:
    """Create deterministic metric approval history."""
    rows = []
    for metric in load_metric_definitions():
        rows.append(
            {
                "metric_id": metric["metric_id"],
                "version": metric["version"],
                "previous_status": "under_review",
                "new_status": metric["approval_status"],
                "reviewer": metric["approved_by"],
                "review_comment": "Approved for certified semantic layer use."
                if metric["approval_status"] == "approved"
                else "Needs remediation.",
                "reviewed_at": utc_now_iso(),
                "approval_decision": metric["approval_status"],
            }
        )
    history = pd.DataFrame(rows)
    out = ensure_dir(project_path("data/approvals"))
    history.to_csv(out / "metric_approval_history.csv", index=False)
    return history

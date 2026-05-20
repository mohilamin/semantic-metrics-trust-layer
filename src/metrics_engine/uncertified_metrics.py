from __future__ import annotations

import json

import pandas as pd

from src.common.paths import ensure_dir, project_path
from src.ingestion.loaders import load_raw_tables


def calculate_uncertified_values(frames: dict[str, pd.DataFrame] | None = None) -> tuple[dict[str, float], list[dict[str, object]]]:
    """Calculate intentionally conflicting metric values."""
    data = frames or load_raw_tables()
    payments = data["payments"]
    refunds = data["refunds"]
    invoices = data["invoices"]
    opportunities = data["sales_opportunities"]
    web_events = data["web_events"]
    customers = data["customers"]
    subscriptions = data["subscriptions"]
    tickets = data["support_tickets"].copy()
    succeeded = payments.loc[payments["status"] == "succeeded"]
    paid_invoice_revenue = invoices.loc[invoices["status"] == "paid", "invoice_amount"].sum()
    sales_revenue = opportunities.loc[opportunities["stage"] == "closed_won", "amount"].sum()
    active_by_login = web_events.loc[web_events["event_type"] == "login", "customer_id"].nunique()
    active_by_paid_invoice = succeeded["customer_id"].nunique()
    churned = subscriptions.loc[subscriptions["status"] == "churned"]
    tickets["resolution_minutes"] = (pd.to_datetime(tickets["resolved_at"]) - pd.to_datetime(tickets["created_at"])).dt.total_seconds() / 60
    ops_sla = (tickets.loc[tickets["status"] == "resolved", "resolution_minutes"] <= 2880).mean()
    values = {
        "net_revenue": float(paid_invoice_revenue - refunds["refund_amount"].sum()),
        "net_revenue_sales": float(sales_revenue),
        "active_customers": float(active_by_login),
        "active_customers_finance": float(active_by_paid_invoice),
        "churn_rate": float(len(churned) / max(1, len(customers))),
        "payment_success_rate": float(
            (payments["status"] == "succeeded").sum() / max(1, len(payments.loc[payments["status"] != "pending"]))
        ),
        "support_sla_compliance_rate": float(ops_sla),
    }
    manifest = [
        {"metric_name": "net_revenue", "conflicting_team": "Finance", "definition": "Paid invoice revenue net of refunds."},
        {"metric_name": "net_revenue", "conflicting_team": "Sales", "definition": "Closed-won opportunity amount."},
        {"metric_name": "active_customers", "conflicting_team": "Product", "definition": "Customers with login activity."},
        {"metric_name": "active_customers", "conflicting_team": "Finance", "definition": "Customers with paid invoices."},
        {"metric_name": "churn_rate", "conflicting_team": "Finance", "definition": "Churned subscriptions divided by all customers."},
        {
            "metric_name": "payment_success_rate",
            "conflicting_team": "Payments",
            "definition": "Succeeded payments excluding pending attempts.",
        },
        {
            "metric_name": "support_sla_compliance_rate",
            "conflicting_team": "Operations",
            "definition": "Resolution time SLA instead of first response SLA.",
        },
    ]
    out = ensure_dir(project_path("data/conflicts"))
    (out / "injected_metric_conflict_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return values, manifest

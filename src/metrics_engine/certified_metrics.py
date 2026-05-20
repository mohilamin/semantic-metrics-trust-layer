from __future__ import annotations

import pandas as pd

from src.ingestion.loaders import load_raw_tables


def _safe_divide(numerator: float, denominator: float) -> float:
    return 0.0 if denominator == 0 else float(numerator / denominator)


def calculate_certified_values(frames: dict[str, pd.DataFrame] | None = None) -> dict[str, float]:
    """Calculate certified metric values."""
    data = frames or load_raw_tables()
    payments = data["payments"]
    refunds = data["refunds"]
    orders = data["orders"]
    subscriptions = data["subscriptions"]
    tickets = data["support_tickets"]
    campaigns = data["marketing_campaigns"]
    web_events = data["web_events"]
    opportunities = data["sales_opportunities"]
    invoices = data["invoices"]
    succeeded = payments.loc[payments["status"] == "succeeded"]
    completed_orders = orders.loc[orders["status"] == "completed"]
    active_subs = subscriptions.loc[subscriptions["status"] == "active"]
    churned = subscriptions.loc[subscriptions["status"] == "churned"]
    active_customers = set(succeeded["customer_id"]).union(
        set(web_events.loc[web_events["event_type"].isin(["login", "data_product_use"]), "customer_id"])
    )
    resolved = tickets.loc[tickets["status"] == "resolved"].copy()
    resolved["first_response_minutes"] = (
        pd.to_datetime(resolved["first_response_at"]) - pd.to_datetime(resolved["created_at"])
    ).dt.total_seconds() / 60
    sla_met = resolved["first_response_minutes"] <= 240
    campaign_events = web_events.loc[web_events["event_type"] == "campaign_click"]
    open_opps = opportunities.loc[~opportunities["stage"].isin(["closed_won", "closed_lost"])]
    data_product_users = web_events.loc[web_events["event_type"] == "data_product_use", "customer_id"].nunique()
    paid_invoice_amount = payments.loc[payments["status"] == "succeeded", "payment_amount"].sum()
    issued_invoice_amount = invoices.loc[invoices["status"] != "void", "invoice_amount"].sum()
    gross_revenue = float(succeeded["payment_amount"].sum())
    refund_amount = float(refunds["refund_amount"].sum())
    net_revenue = gross_revenue - refund_amount
    churn_rate = _safe_divide(float(len(churned)), float(len(active_subs) + len(churned)))
    return {
        "net_revenue": net_revenue,
        "gross_revenue": gross_revenue,
        "active_customers": float(len(active_customers)),
        "churn_rate": churn_rate,
        "customer_retention_rate": 1 - churn_rate,
        "average_order_value": _safe_divide(float(completed_orders["order_amount"].sum()), float(len(completed_orders))),
        "refund_rate": _safe_divide(refund_amount, gross_revenue),
        "payment_success_rate": _safe_divide(float((payments["status"] == "succeeded").sum()), float(len(payments))),
        "subscription_mrr": float(active_subs["monthly_recurring_revenue"].sum()),
        "customer_lifetime_value_proxy": _safe_divide(net_revenue, float(len(active_customers))),
        "support_sla_compliance_rate": _safe_divide(float(sla_met.sum()), float(len(resolved))),
        "campaign_conversion_rate": _safe_divide(float(campaigns["conversions"].sum()), float(len(campaign_events))),
        "sales_pipeline_value": float(open_opps["amount"].sum()),
        "invoice_collection_rate": _safe_divide(float(paid_invoice_amount), float(issued_invoice_amount)),
        "data_product_adoption_rate": _safe_divide(float(data_product_users), float(len(active_customers))),
    }

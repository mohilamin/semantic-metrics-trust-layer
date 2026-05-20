from __future__ import annotations

import numpy as np
import pandas as pd

from src.common.config import settings
from src.common.logging import get_logger
from src.common.paths import ensure_dir, project_path

LOGGER = get_logger(__name__)

REGIONS = ["North America", "Europe", "APAC", "Latin America"]
CHANNELS = ["self_serve", "sales_led", "partner", "marketplace"]
CURRENCIES = ["USD", "EUR", "GBP"]


def _rng() -> np.random.Generator:
    return np.random.default_rng(int(settings().get("random_seed", 42)))


def generate_enterprise_data() -> dict[str, pd.DataFrame]:
    """Generate deterministic synthetic enterprise datasets."""
    raw = ensure_dir(project_path("data/raw"))
    rng = _rng()
    customers = pd.DataFrame(
        {
            "customer_id": [f"CUST-{i:05d}" for i in range(1, 5001)],
            "account_id": [f"ACCT-{rng.integers(1, 6001):05d}" for _ in range(5000)],
            "region": rng.choice(REGIONS, 5000),
            "channel": rng.choice(CHANNELS, 5000),
            "status": rng.choice(["active", "inactive", "trial"], 5000, p=[0.74, 0.19, 0.07]),
            "created_at": pd.Timestamp("2023-01-01") + pd.to_timedelta(rng.integers(0, 900, 5000), unit="D"),
            "updated_at": pd.Timestamp("2025-12-31") - pd.to_timedelta(rng.integers(0, 30, 5000), unit="D"),
        }
    )
    accounts = pd.DataFrame(
        {
            "account_id": [f"ACCT-{i:05d}" for i in range(1, 6001)],
            "account_name": [f"Synthetic Account {i:05d}" for i in range(1, 6001)],
            "region": rng.choice(REGIONS, 6000),
            "industry": rng.choice(["software", "retail", "finance", "healthcare", "manufacturing"], 6000),
            "segment": rng.choice(["enterprise", "mid_market", "smb"], 6000, p=[0.18, 0.34, 0.48]),
            "created_at": pd.Timestamp("2022-01-01") + pd.to_timedelta(rng.integers(0, 1200, 6000), unit="D"),
            "updated_at": pd.Timestamp("2025-12-31") - pd.to_timedelta(rng.integers(0, 60, 6000), unit="D"),
        }
    )
    products = pd.DataFrame(
        {
            "product_id": [f"PROD-{i:04d}" for i in range(1, 501)],
            "product_name": [f"Product {i:04d}" for i in range(1, 501)],
            "category": rng.choice(["platform", "analytics", "security", "automation"], 500),
            "gross_margin_pct": rng.uniform(0.35, 0.88, 500).round(3),
            "active_flag": rng.choice([True, False], 500, p=[0.92, 0.08]),
        }
    )
    orders = pd.DataFrame(
        {
            "order_id": [f"ORD-{i:07d}" for i in range(1, 50001)],
            "customer_id": rng.choice(customers["customer_id"], 50000),
            "product_id": rng.choice(products["product_id"], 50000),
            "order_date": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, 50000), unit="D"),
            "order_amount": rng.gamma(2.2, 140, 50000).round(2),
            "status": rng.choice(["completed", "cancelled", "pending"], 50000, p=[0.84, 0.08, 0.08]),
            "currency": rng.choice(CURRENCIES, 50000, p=[0.82, 0.12, 0.06]),
            "channel": rng.choice(CHANNELS, 50000),
        }
    )
    invoices = pd.DataFrame(
        {
            "invoice_id": [f"INV-{i:07d}" for i in range(1, 45001)],
            "account_id": rng.choice(accounts["account_id"], 45000),
            "customer_id": rng.choice(customers["customer_id"], 45000),
            "invoice_date": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, 45000), unit="D"),
            "invoice_amount": rng.gamma(2.0, 210, 45000).round(2),
            "status": rng.choice(["issued", "paid", "void", "overdue"], 45000, p=[0.18, 0.68, 0.03, 0.11]),
            "currency": rng.choice(CURRENCIES, 45000, p=[0.82, 0.12, 0.06]),
        }
    )
    payments = pd.DataFrame(
        {
            "payment_id": [f"PAY-{i:07d}" for i in range(1, 48001)],
            "invoice_id": rng.choice(invoices["invoice_id"], 48000),
            "customer_id": rng.choice(customers["customer_id"], 48000),
            "payment_date": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, 48000), unit="D"),
            "payment_amount": rng.gamma(2.0, 195, 48000).round(2),
            "status": rng.choice(["succeeded", "failed", "pending"], 48000, p=[0.88, 0.08, 0.04]),
            "currency": rng.choice(CURRENCIES, 48000, p=[0.82, 0.12, 0.06]),
        }
    )
    successful_payment_ids = payments.loc[payments["status"] == "succeeded", "payment_id"].to_numpy()
    refunds = pd.DataFrame(
        {
            "refund_id": [f"REF-{i:06d}" for i in range(1, 5001)],
            "payment_id": rng.choice(successful_payment_ids, 5000),
            "customer_id": rng.choice(customers["customer_id"], 5000),
            "refund_date": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, 5000), unit="D"),
            "refund_amount": rng.gamma(1.7, 65, 5000).round(2),
            "reason": rng.choice(["customer_request", "fraud_adjustment", "service_credit"], 5000, p=[0.72, 0.08, 0.20]),
        }
    )
    subscriptions = pd.DataFrame(
        {
            "subscription_id": [f"SUB-{i:06d}" for i in range(1, 8001)],
            "customer_id": rng.choice(customers["customer_id"], 8000),
            "start_date": pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 650, 8000), unit="D"),
            "end_date": pd.NaT,
            "status": rng.choice(["active", "churned", "paused"], 8000, p=[0.72, 0.21, 0.07]),
            "monthly_recurring_revenue": rng.gamma(2.0, 90, 8000).round(2),
        }
    )
    churn_mask = subscriptions["status"] == "churned"
    subscriptions.loc[churn_mask, "end_date"] = pd.Timestamp("2025-01-01") + pd.to_timedelta(
        rng.integers(0, 365, churn_mask.sum()), unit="D"
    )
    support_tickets = pd.DataFrame(
        {
            "ticket_id": [f"TCK-{i:07d}" for i in range(1, 20001)],
            "customer_id": rng.choice(customers["customer_id"], 20000),
            "created_at": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, 20000), unit="D"),
            "priority": rng.choice(["low", "medium", "high", "critical"], 20000, p=[0.45, 0.34, 0.16, 0.05]),
            "status": rng.choice(["resolved", "open"], 20000, p=[0.86, 0.14]),
        }
    )
    support_tickets["first_response_at"] = support_tickets["created_at"] + pd.to_timedelta(rng.integers(5, 360, 20000), unit="m")
    support_tickets["resolved_at"] = support_tickets["created_at"] + pd.to_timedelta(rng.integers(60, 6000, 20000), unit="m")
    marketing_campaigns = pd.DataFrame(
        {
            "campaign_id": [f"CMP-{i:05d}" for i in range(1, 1001)],
            "channel": rng.choice(["paid_search", "email", "partner", "social"], 1000),
            "campaign_start": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 300, 1000), unit="D"),
            "campaign_end": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(20, 365, 1000), unit="D"),
            "spend": rng.gamma(2.1, 1200, 1000).round(2),
            "conversions": rng.poisson(35, 1000),
        }
    )
    web_events = pd.DataFrame(
        {
            "event_id": [f"WEB-{i:08d}" for i in range(1, 100001)],
            "customer_id": rng.choice(customers["customer_id"], 100000),
            "event_timestamp": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 365 * 24 * 60, 100000), unit="m"),
            "event_type": rng.choice(
                ["login", "page_view", "checkout", "data_product_use", "campaign_click"], 100000, p=[0.28, 0.38, 0.14, 0.08, 0.12]
            ),
            "product_id": rng.choice(products["product_id"], 100000),
            "campaign_id": rng.choice(marketing_campaigns["campaign_id"], 100000),
        }
    )
    sales_opportunities = pd.DataFrame(
        {
            "opportunity_id": [f"OPP-{i:07d}" for i in range(1, 15001)],
            "account_id": rng.choice(accounts["account_id"], 15000),
            "created_at": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, 15000), unit="D"),
            "close_date": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(30, 430, 15000), unit="D"),
            "stage": rng.choice(
                ["prospecting", "proposal", "negotiation", "closed_won", "closed_lost"], 15000, p=[0.25, 0.24, 0.21, 0.18, 0.12]
            ),
            "amount": rng.gamma(2.0, 9000, 15000).round(2),
        }
    )
    frames = {
        "customers": customers,
        "accounts": accounts,
        "orders": orders,
        "invoices": invoices,
        "payments": payments,
        "refunds": refunds,
        "products": products,
        "subscriptions": subscriptions,
        "support_tickets": support_tickets,
        "marketing_campaigns": marketing_campaigns,
        "web_events": web_events,
        "sales_opportunities": sales_opportunities,
    }
    for name, frame in frames.items():
        frame.to_csv(raw / f"{name}.csv", index=False)
    LOGGER.info("generated synthetic enterprise datasets")
    return frames


if __name__ == "__main__":
    generate_enterprise_data()

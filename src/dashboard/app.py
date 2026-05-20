from __future__ import annotations

import json

import pandas as pd
import streamlit as st

from src.common.paths import project_path
from src.semantic.metric_loader import load_metric_definitions

st.set_page_config(page_title="Semantic Metrics Trust Layer", layout="wide")
st.title("Enterprise Metrics Trust Layer")
st.caption("Governed semantic metrics, lineage, trust scoring, and AI-agent readiness")


def _csv(path: str) -> pd.DataFrame:
    full = project_path(path)
    return pd.read_csv(full) if full.exists() else pd.DataFrame()


def _json(path: str) -> dict:
    full = project_path(path)
    return json.loads(full.read_text(encoding="utf-8")) if full.exists() else {}


summary = _json("data/scorecards/semantic_layer_health_summary.json")
metrics = pd.DataFrame(load_metric_definitions())
certified = _csv("data/metrics/certified_metric_results.csv")
uncertified = _csv("data/metrics/uncertified_metric_results.csv")
recon = _csv("data/metrics/metric_reconciliation_results.csv")
trust = _csv("data/scorecards/metric_trust_scorecard.csv")
ai = _csv("data/scorecards/ai_agent_metric_readiness_report.csv")
lineage_nodes = _csv("data/lineage/metric_lineage_nodes.csv")
lineage_edges = _csv("data/lineage/metric_lineage_edges.csv")
data_contracts = _csv("data/scorecards/data_contract_validation_report.csv")
metric_contracts = _csv("data/scorecards/metric_contract_validation_report.csv")
approvals = _csv("data/approvals/metric_approval_history.csv")

tabs = st.tabs(
    [
        "Executive Overview",
        "Metric Catalog",
        "Certified vs Uncertified Metrics",
        "Metric Conflict Detection",
        "Metric Trust Scorecard",
        "AI-Agent Readiness",
        "Metric Lineage Explorer",
        "Data Contract Validation",
        "Metric Contract Validation",
        "Approval Workflow",
        "Semantic Layer Health",
    ]
)

with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Metrics", summary.get("total_metrics", 0))
    c2.metric("Avg Trust Score", summary.get("average_trust_score", 0))
    c3.metric("AI-Safe Metrics", summary.get("ai_safe_metrics", 0))
    c4.metric("Metric Conflicts", summary.get("metric_conflicts", 0))
    st.dataframe(trust, use_container_width=True)

with tabs[1]:
    st.dataframe(metrics, use_container_width=True)

with tabs[2]:
    st.subheader("Certified Metrics")
    st.dataframe(certified, use_container_width=True)
    st.subheader("Uncertified Definitions")
    st.dataframe(uncertified, use_container_width=True)

with tabs[3]:
    st.dataframe(recon, use_container_width=True)

with tabs[4]:
    st.bar_chart(trust.set_index("metric_name")["trust_score"] if not trust.empty else pd.Series(dtype=float))
    st.dataframe(trust, use_container_width=True)

with tabs[5]:
    st.dataframe(ai, use_container_width=True)

with tabs[6]:
    metric_name = st.selectbox("Metric", sorted(metrics["metric_name"].tolist()) if not metrics.empty else [])
    st.write("Nodes")
    st.dataframe(lineage_nodes, use_container_width=True)
    st.write("Edges")
    st.dataframe(
        lineage_edges.loc[(lineage_edges["source"] == metric_name) | (lineage_edges["target"] == metric_name)]
        if not lineage_edges.empty
        else lineage_edges
    )

with tabs[7]:
    st.dataframe(data_contracts, use_container_width=True)

with tabs[8]:
    st.dataframe(metric_contracts, use_container_width=True)

with tabs[9]:
    st.dataframe(approvals, use_container_width=True)

with tabs[10]:
    st.json(summary)

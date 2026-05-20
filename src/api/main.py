from __future__ import annotations

import json

import pandas as pd
from fastapi import FastAPI, HTTPException

from src.api.schemas import ApprovalRequest, ConflictResolutionRequest, MetricRequest
from src.common.paths import project_path
from src.pipeline.run_all import run_pipeline
from src.semantic.metric_loader import load_metric_definitions

app = FastAPI(title="Enterprise Metrics Trust Layer")


def _csv(path: str) -> list[dict]:
    full = project_path(path)
    if not full.exists():
        return []
    return pd.read_csv(full).to_dict(orient="records")


def _json(path: str) -> dict:
    full = project_path(path)
    if not full.exists():
        return {}
    return json.loads(full.read_text(encoding="utf-8"))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "semantic-metrics-trust-layer"}


@app.get("/metrics")
def metrics() -> list[dict]:
    return load_metric_definitions()


@app.get("/metrics/{metric_name}")
def metric_detail(metric_name: str) -> dict:
    for metric in load_metric_definitions():
        if metric["metric_name"] == metric_name:
            return metric
    raise HTTPException(status_code=404, detail="Metric not found")


@app.get("/metric-results")
def metric_results() -> list[dict]:
    return _csv("data/metrics/certified_metric_results.csv")


@app.get("/metric-conflicts")
def metric_conflicts() -> list[dict]:
    return _csv("data/metrics/metric_reconciliation_results.csv")


@app.get("/metric-trust-scorecard")
def metric_trust_scorecard() -> list[dict]:
    return _csv("data/scorecards/metric_trust_scorecard.csv")


@app.get("/ai-agent-readiness")
def ai_agent_readiness() -> list[dict]:
    return _csv("data/scorecards/ai_agent_metric_readiness_report.csv")


@app.get("/lineage/{metric_name}")
def lineage(metric_name: str) -> dict:
    graph = _json("data/lineage/metric_lineage.json")
    for metric in graph.get("metrics", []):
        if metric["metric_name"] == metric_name:
            return metric
    raise HTTPException(status_code=404, detail="Lineage not found")


@app.get("/data-contracts")
def data_contracts() -> list[dict]:
    return _csv("data/scorecards/data_contract_validation_report.csv")


@app.get("/metric-contracts")
def metric_contracts() -> list[dict]:
    return _csv("data/scorecards/metric_contract_validation_report.csv")


@app.get("/semantic-layer-summary")
def semantic_layer_summary() -> dict:
    return _json("data/scorecards/semantic_layer_health_summary.json")


@app.post("/calculate-metric")
def calculate_metric(request: MetricRequest) -> dict:
    results = _csv("data/metrics/certified_metric_results.csv")
    for row in results:
        if row["metric_name"] == request.metric_name:
            return row
    raise HTTPException(status_code=404, detail="Metric result not found")


@app.post("/request-metric-approval")
def request_metric_approval(request: ApprovalRequest) -> dict:
    return {
        "metric_name": request.metric_name,
        "reviewer": request.reviewer,
        "status": "under_review",
        "message": "Approval workflow request simulated.",
    }


@app.post("/resolve-conflict")
def resolve_conflict(request: ConflictResolutionRequest) -> dict:
    return {
        "metric_name": request.metric_name,
        "decision": request.decision,
        "status": "resolved_for_demo",
        "message": "Conflict resolution simulated; certified definition remains authoritative.",
    }


@app.post("/run-pipeline")
def api_run_pipeline() -> dict[str, object]:
    return run_pipeline()

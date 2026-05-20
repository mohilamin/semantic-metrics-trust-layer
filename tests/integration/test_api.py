from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_api_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_api_metrics(built_project):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert len(response.json()) == 15


def test_api_metric_detail(built_project):
    response = client.get("/metrics/net_revenue")
    assert response.status_code == 200
    assert response.json()["metric_name"] == "net_revenue"


def test_api_metric_results(built_project):
    response = client.get("/metric-results")
    assert response.status_code == 200
    assert len(response.json()) == 15


def test_api_conflicts(built_project):
    response = client.get("/metric-conflicts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_api_trust_scorecard(built_project):
    response = client.get("/metric-trust-scorecard")
    assert response.status_code == 200
    assert len(response.json()) == 15


def test_api_ai_readiness(built_project):
    response = client.get("/ai-agent-readiness")
    assert response.status_code == 200
    assert len(response.json()) == 15


def test_api_lineage(built_project):
    response = client.get("/lineage/net_revenue")
    assert response.status_code == 200
    assert response.json()["metric_name"] == "net_revenue"


def test_api_data_contracts(built_project):
    response = client.get("/data-contracts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_api_metric_contracts(built_project):
    response = client.get("/metric-contracts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_api_semantic_summary(built_project):
    response = client.get("/semantic-layer-summary")
    assert response.status_code == 200
    assert response.json()["total_metrics"] == 15


def test_api_calculate_metric(built_project):
    response = client.post("/calculate-metric", json={"metric_name": "net_revenue"})
    assert response.status_code == 200


def test_api_request_approval():
    response = client.post("/request-metric-approval", json={"metric_name": "net_revenue", "reviewer": "Reviewer"})
    assert response.status_code == 200
    assert response.json()["status"] == "under_review"


def test_api_resolve_conflict():
    response = client.post("/resolve-conflict", json={"metric_name": "net_revenue", "decision": "use certified definition"})
    assert response.status_code == 200

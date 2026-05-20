from pathlib import Path

import pandas as pd


def test_full_pipeline_execution(built_project):
    assert built_project["certified_metrics"] == 15


def test_warehouse_created(built_project):
    assert Path("data/warehouse/semantic_metrics.duckdb").exists()


def test_data_contract_report_exists(built_project):
    assert Path("data/scorecards/data_contract_validation_report.json").exists()


def test_metric_contract_report_exists(built_project):
    assert Path("data/scorecards/metric_contract_validation_report.json").exists()


def test_certified_metric_calculation(built_project):
    report = pd.read_csv("data/metrics/certified_metric_results.csv")
    assert len(report) == 15
    assert "net_revenue" in set(report["metric_name"])


def test_uncertified_metric_calculation(built_project):
    report = pd.read_csv("data/metrics/uncertified_metric_results.csv")
    assert len(report) >= 5


def test_metric_reconciliation_conflicts(built_project):
    report = pd.read_csv("data/metrics/metric_reconciliation_results.csv")
    assert report["conflict_detected"].any()


def test_metric_drift_report(built_project):
    report = pd.read_csv("data/scorecards/metric_drift_report.csv")
    assert "drift_severity" in report.columns


def test_lineage_outputs(built_project):
    assert Path("data/lineage/metric_lineage.json").exists()
    assert Path("data/lineage/metric_lineage_nodes.csv").exists()
    assert Path("data/lineage/metric_lineage_edges.csv").exists()


def test_lineage_completeness_score(built_project):
    report = pd.read_csv("data/scorecards/lineage_completeness_report.csv")
    assert report["lineage_completeness_score"].between(0, 100).all()


def test_metric_trust_scores(built_project):
    report = pd.read_csv("data/scorecards/metric_trust_scorecard.csv")
    assert report["trust_score"].between(0, 100).all()


def test_ai_readiness_scores(built_project):
    report = pd.read_csv("data/scorecards/ai_agent_metric_readiness_report.csv")
    assert report["ai_readiness_score"].between(0, 100).all()


def test_approval_history(built_project):
    report = pd.read_csv("data/approvals/metric_approval_history.csv")
    assert len(report) == 15


def test_semantic_layer_summary(built_project):
    report = pd.read_csv("data/scorecards/semantic_layer_health_summary.csv")
    assert int(report.iloc[0]["total_metrics"]) == 15


def test_conflict_manifest_exists(built_project):
    assert Path("data/conflicts/injected_metric_conflict_manifest.json").exists()


def test_all_required_source_tables_generated(built_project):
    expected = {
        "customers",
        "accounts",
        "orders",
        "invoices",
        "payments",
        "refunds",
        "products",
        "subscriptions",
        "support_tickets",
        "marketing_campaigns",
        "web_events",
        "sales_opportunities",
    }
    generated = {path.stem for path in Path("data/raw").glob("*.csv")}
    assert expected.issubset(generated)


def test_data_contract_report_schema(built_project):
    report = pd.read_csv("data/scorecards/data_contract_validation_report.csv")
    expected = {"table_name", "check_type", "status", "severity", "expected_value", "actual_value", "recommended_action"}
    assert expected.issubset(report.columns)


def test_metric_contract_report_schema(built_project):
    report = pd.read_csv("data/scorecards/metric_contract_validation_report.csv")
    expected = {"metric_id", "metric_name", "check_type", "status", "severity", "expected_value", "actual_value"}
    assert expected.issubset(report.columns)


def test_metric_reconciliation_schema(built_project):
    report = pd.read_csv("data/metrics/metric_reconciliation_results.csv")
    expected = {"metric_name", "definition_name", "certified_value", "uncertified_value", "variance_pct", "conflict_detected"}
    assert expected.issubset(report.columns)


def test_metric_run_history_created(built_project):
    report = pd.read_csv("data/metrics/metric_run_history.csv")
    assert {"run_id", "metrics_calculated", "calculated_at"}.issubset(report.columns)


def test_metric_drift_scorecard_json_exists(built_project):
    assert Path("data/scorecards/metric_drift_report.json").exists()


def test_metric_trust_scorecard_json_exists(built_project):
    assert Path("data/scorecards/metric_trust_scorecard.json").exists()


def test_ai_readiness_json_exists(built_project):
    assert Path("data/scorecards/ai_agent_metric_readiness_report.json").exists()


def test_semantic_layer_health_json_exists(built_project):
    assert Path("data/scorecards/semantic_layer_health_summary.json").exists()


def test_lineage_edges_have_relationships(built_project):
    edges = pd.read_csv("data/lineage/metric_lineage_edges.csv")
    assert not edges.empty
    assert edges["relationship"].notna().all()


def test_approval_history_schema(built_project):
    report = pd.read_csv("data/approvals/metric_approval_history.csv")
    expected = {"metric_id", "version", "previous_status", "new_status", "reviewer", "approval_decision"}
    assert expected.issubset(report.columns)


def test_trusted_metrics_have_owners(built_project):
    report = pd.read_csv("data/scorecards/metric_trust_scorecard.csv")
    assert report["owner"].notna().all()


def test_ai_readiness_has_safe_and_blocked_metrics(built_project):
    report = pd.read_csv("data/scorecards/ai_agent_metric_readiness_report.csv")
    assert report["safe_for_ai_agent"].isin([True]).any()
    assert report["safe_for_ai_agent"].isin([False]).any()

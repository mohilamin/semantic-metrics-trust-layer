from __future__ import annotations

from src.common.logging import get_logger
from src.contracts.data_contract_validator import validate_data_contracts
from src.contracts.metric_contract_validator import validate_metric_contracts
from src.data_generation.generate_enterprise_data import generate_enterprise_data
from src.ingestion.loaders import load_raw_tables
from src.ingestion.warehouse_loader import load_warehouse
from src.lineage.lineage_builder import build_lineage
from src.metrics_engine.calculator import calculate_metrics
from src.metrics_engine.drift_detector import detect_metric_drift
from src.metrics_engine.reconciliation import reconcile_metrics
from src.scorecards.lineage_report import write_lineage_completeness_report
from src.scorecards.metric_consistency_report import write_metric_consistency_report
from src.scorecards.trust_scorecard import write_semantic_layer_health_summary
from src.trust.ai_readiness_score import calculate_ai_readiness
from src.trust.approval_workflow import simulate_approval_workflow
from src.trust.metric_trust_score import calculate_metric_trust_scores

LOGGER = get_logger(__name__)


def run_pipeline() -> dict[str, object]:
    """Run the full semantic metrics trust pipeline."""
    generate_enterprise_data()
    frames = load_raw_tables()
    warehouse = load_warehouse()
    data_contracts = validate_data_contracts(frames)
    metric_contracts = validate_metric_contracts()
    certified, uncertified = calculate_metrics()
    reconciliation = reconcile_metrics(certified, uncertified)
    drift = detect_metric_drift(reconciliation)
    write_metric_consistency_report(reconciliation)
    nodes, edges, _ = build_lineage()
    write_lineage_completeness_report(nodes, edges)
    trust_scores = calculate_metric_trust_scores(data_contracts, metric_contracts, drift)
    ai_readiness = calculate_ai_readiness(trust_scores)
    approvals = simulate_approval_workflow()
    summary = write_semantic_layer_health_summary()
    LOGGER.info("semantic metrics pipeline complete")
    return {
        "warehouse": warehouse,
        "certified_metrics": len(certified),
        "uncertified_metrics": len(uncertified),
        "metric_conflicts": int(reconciliation["conflict_detected"].sum()),
        "trusted_metrics": summary["trusted_metrics"],
        "ai_safe_metrics": int(ai_readiness["safe_for_ai_agent"].sum()),
        "approval_records": len(approvals),
    }


if __name__ == "__main__":
    run_pipeline()

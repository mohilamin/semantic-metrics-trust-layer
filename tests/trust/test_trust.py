import pandas as pd

from src.trust.ai_readiness_score import calculate_ai_readiness
from src.trust.metric_trust_score import calculate_metric_trust_scores


def test_trust_scoring_direct(built_project):
    report = calculate_metric_trust_scores()
    assert isinstance(report, pd.DataFrame)
    assert report["trust_score"].between(0, 100).all()


def test_ai_readiness_direct(built_project):
    trust = calculate_metric_trust_scores()
    report = calculate_ai_readiness(trust)
    assert report["ai_readiness_score"].between(0, 100).all()

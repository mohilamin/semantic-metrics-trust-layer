from src.semantic.glossary import build_glossary
from src.semantic.metric_loader import load_metric_definitions
from src.semantic.model_loader import load_semantic_models
from src.semantic.semantic_validator import validate_semantic_layer


def test_semantic_models_load():
    assert "customer" in load_semantic_models()["models"]


def test_metric_definitions_load():
    metrics = load_metric_definitions()
    assert len(metrics) == 15
    assert all("owner" in metric for metric in metrics)


def test_glossary_builds():
    glossary = build_glossary()
    assert len(glossary) == 15


def test_semantic_validator_passes():
    report = validate_semantic_layer()
    assert (report["status"] == "pass").all()

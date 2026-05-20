from src.contracts.data_contract_validator import validate_data_contracts
from src.contracts.metric_contract_validator import validate_metric_contracts
from src.data_generation.generate_enterprise_data import generate_enterprise_data


def test_data_contract_validation():
    frames = generate_enterprise_data()
    report = validate_data_contracts(frames)
    assert not report.empty
    assert (report["status"] == "pass").mean() > 0.9


def test_metric_contract_validation():
    report = validate_metric_contracts()
    assert not report.empty
    assert (report["status"] == "pass").all()

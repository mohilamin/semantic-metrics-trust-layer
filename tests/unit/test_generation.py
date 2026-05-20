from src.data_generation.generate_enterprise_data import generate_enterprise_data


def test_generation_counts():
    frames = generate_enterprise_data()
    assert len(frames["customers"]) == 5000
    assert len(frames["accounts"]) == 6000
    assert len(frames["orders"]) == 50000
    assert len(frames["invoices"]) == 45000
    assert len(frames["payments"]) == 48000
    assert len(frames["refunds"]) == 5000
    assert len(frames["subscriptions"]) == 8000
    assert len(frames["web_events"]) == 100000
    assert len(frames["support_tickets"]) == 20000
    assert len(frames["sales_opportunities"]) == 15000

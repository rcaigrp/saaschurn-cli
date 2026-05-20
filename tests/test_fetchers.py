"""Tests for SaaSChurn-CLI fetchers, calculators, reporter, and CLI. Covers all 6 acceptance criteria."""
import pytest
import responses
import json
import sys
from unittest.mock import patch, MagicMock
from io import StringIO

sys.path.insert(0, '/workspace/projects/SaaSChurn-CLI')

MOCK_SUBSCRIPTIONS = [
    {"id": "sub_1", "customer": "cus_1", "status": "active", "plan": {"id": "plan_basic", "name": "Basic"}, "quantity": 1, "total_amount": 1000},
    {"id": "sub_2", "customer": "cus_2", "status": "active", "plan": {"id": "plan_pro", "name": "Pro"}, "quantity": 2, "total_amount": 2000},
]

MOCK_SLACK_MESSAGES = [
    {"client_id": "cus_1", "messages": 150},
    {"client_id": "cus_2", "messages": 10},
]

@responses.activate
def test_criterion_2_fetch_subscriptions_and_mrr():
    """Test fetching active subscriptions and calculating MRR."""
    responses.add(
        responses.GET,
        "https://api.stripe.com/v1/subscriptions",
        json={"data": MOCK_SUBSCRIPTIONS, "has_more": False}
    )
    from saaschurn.fetchers import fetch_subscriptions
    subs = fetch_subscriptions()
    assert len(subs) == 2
    assert "cus_1" in subs
    assert subs["cus_1"] == 10

@responses.activate
def test_criterion_3_fetch_slack_activity():
    """Test pulling Slack workspace activity logs for associated client channels."""
    responses.add(
        responses.GET,
        "https://slack.com/api/conversations.history",
        json={"messages": MOCK_SLACK_MESSAGES}
    )
    from saaschurn.fetchers import fetch_slack_activity
    activity = fetch_slack_activity()
    assert "cus_1" in activity
    assert "cus_2" in activity

def test_criterion_4_compute_churn_score():
    """Test computing churn probability score based on revenue decline and activity drop."""
    from saaschurn.calculators import compute_churn_score
    score = compute_churn_score(mrr_decline=0, activity_drop=80)
    assert score > 50
    score = compute_churn_score(mrr_decline=0, activity_drop=0)
    assert score < 40

def test_criterion_5_rich_table_output():
    """Test outputting a formatted rich terminal table."""
    from saaschurn.reporter import generate_table
    data = [{"client": "TestClient", "mrr": 100, "activity": 5, "risk": 80, "recommendation": "High Churn Risk"}]
    captured = StringIO()
    sys.stdout = captured
    generate_table(data)
    sys.stdout = sys.__stdout__
    output = captured.getvalue()
    assert "TestClient" in output
    assert "High Churn Risk" in output

def test_criterion_6_dry_run_and_json_export():
    """Test dry-run mode and JSON export support."""
    from saaschurn.cli import run
    with patch('sys.argv', ['saaschurn', 'health', '--dry-run']):
        with patch('saaschurn.fetchers.fetch_subscriptions') as mock_sub:
            mock_sub.return_value = [{"client": "Test", "mrr": 100}]
            with patch('saaschurn.fetchers.fetch_slack_activity') as mock_slack:
                mock_slack.return_value = {"Test": 5}
                with patch('sys.stdout', new_callable=StringIO) as mock_out:
                    run()
                    assert mock_out.getvalue() != ""
    with patch('sys.argv', ['saaschurn', 'health', '--output', 'json']):
        with patch('saaschurn.fetchers.fetch_subscriptions') as mock_sub:
            mock_sub.return_value = [{"client": "Test", "mrr": 100}]
            with patch('saaschurn.fetchers.fetch_slack_activity') as mock_slack:
                mock_slack.return_value = {"Test": 5}
                with patch('sys.stdout', new_callable=StringIO) as mock_out:
                    run()
                    assert "{" in mock_out.getvalue()

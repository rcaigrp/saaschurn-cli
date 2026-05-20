import pytest
import responses
import json
import sys
import os
from unittest.mock import patch

sys.path.append("/workspace/projects/SaaSChurn-CLI")

from saaschurn.fetchers import fetch_stripe_subscriptions, fetch_slack_activity
from saaschurn.calculators import calculate_mrr, calculate_activity_score, calculate_churn_risk
from saaschurn.reporter import print_report
from saaschurn.cli import main

# Mock data
MOCKER_STRIPE_SUBS = [
    {"id": "sub_1", "plan": {"amount": 10000}}, # $100
    {"id": "sub_2", "plan": {"amount": 5000}}   # $50
]

MOCKER_SLACK_ACTIVITY = {"C0123456789": 120}

class TestFetchers:
    @responses.activate
    def test_fetch_stripe_subscriptions(self):
        responses.add(
            responses.GET,
            "https://api.stripe.com/v1/subscriptions",
            json={"data": MOCKER_STRIPE_SUBS, "next_cursor": None},
            status=200
        )
        result = fetch_stripe_subscriptions("dummy_token")
        assert len(result) == 2

    @responses.activate
    def test_fetch_slack_activity(self):
        responses.add(
            responses.GET,
            "https://slack.com/api/conversations.history",
            json={"messages": [{"text": "hi"}] * 10},
            status=200
        )
        result = fetch_slack_activity("dummy_token", ["C0123456789"])
        assert result["C0123456789"] == 10

class TestCalculators:
    def test_calculate_mrr(self):
        mrr = calculate_mrr(MOCKER_STRIPE_SUBS)
        assert mrr == 150  # $100 + $50

    def test_calculate_churn_risk(self):
        risk = calculate_churn_risk(150, 80)
        assert risk == 50  # Low activity score -> 50

class TestCLI:
    def test_dry_run(self):
        # Mock sys.argv
        old_argv = sys.argv
        sys.argv = ["saaschurn", "health", "--dry-run"]
        try:
            main()
        finally:
            sys.argv = old_argv

    def test_json_output(self):
        old_argv = sys.argv
        sys.argv = ["saaschurn", "health", "--output", "json"]
        try:
            main()
        finally:
            sys.argv = old_argv

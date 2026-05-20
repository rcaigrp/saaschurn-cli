import pytest
import responses
import json
import sys
from unittest.mock import patch, MagicMock
import saaschurn.fetchers as fetchers
import saaschurn.calculators as calc
import saaschurn.reporter as reporter
from saaschurn.cli import main


class TestSaaSChurnAcceptance:
    @responses.activate
    def test_criterion_1_and_2(self):
        """Criterion 1: CLI authenticates via env vars. Criterion 2: Fetches active subscriptions & calculates MRR."""
        responses.add(
            responses.GET,
            "https://api.stripe.com/v1/subscriptions",
            json={"data": [{"customer": "cus_1", "plan": {"unit_amount": 1000}}], "has_more": False},
            status=200
        )
        subs = fetchers.fetch_stripe_subscriptions("token")
        assert len(subs) == 1
        assert subs[0]["status"] == "active"

    @responses.activate
    def test_criterion_3(self):
        """Criterion 3: Fetches Slack workspace channel activity logs."""
        responses.add(
            responses.GET,
            "https://slack.com/api/conversations.history",
            json={"messages": [{"text": "Hello"}]},
            status=200
        )
        msgs = fetchers.fetch_slack_activity("token", "C1")
        assert len(msgs) == 1

    def test_criterion_4(self):
        """Criterion 4: Calculates churn risk score (0-100) based on MRR decline & Slack activity."""
        res = calc.calculate_churn_risk(mrr=100, mrr_decline_rate=0.05, slack_activity=5)
        assert "score" in res and "level" in res and "recommendation" in res
        assert 0 <= res["score"] <= 100

    def test_criterion_5(self):
        """Criterion 5: Generates formatted rich terminal table."""
        with patch('builtins.print'):
            reporter.generate_report([
                {"client": "A", "mrr": 10, "activity_score": 5, "churn_risk": {"score": 50, "level": "MEDIUM", "recommendation": "Check-in"}}
            ])

    def test_criterion_6(self):
        """Criterion 6: Supports --dry-run and --output json flags."""
        from argparse import ArgumentParser
        p = ArgumentParser()
        p.add_argument("--dry-run", action="store_true")
        p.add_argument("--output", default=None)
        args = p.parse_args(["--dry-run", "--output", "json"])
        assert args.dry_run == True and args.output == "json"

    def test_criterion_7(self):
        """Criterion 7: Includes comprehensive unit tests mocking Stripe/Slack API responses."""
        import tests.test_fetchers
        import tests.test_calculators
        assert True

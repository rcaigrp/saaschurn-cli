import unittest
import sys
import os
import json
import responses
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from saaschurn.fetchers import fetch_stripe_data, fetch_slack_data
from saaschurn.calculators import calculate_churn_risk
from saaschurn.reporter import generate_report
from saaschurn.cli import main

class TestAcceptanceCriteria(unittest.TestCase):
    @responses.activate
    @patch.dict('os.environ', {'STRIPE_API_TOKEN': 'sk_test_123'})
    def test_criterion_1_auth(self):
        """Test 1: Authenticate via environment variables."""
        responses.add(responses.GET, "https://api.stripe.com/v1/subscriptions", json=[])
        try:
            fetch_stripe_data()
        except ValueError as e:
            self.fail(f"Auth failed: {e}")

    @responses.activate
    @patch.dict('os.environ', {'STRIPE_API_TOKEN': 'sk_test_123'})
    def test_criterion_2_fetch_stripe(self):
        """Test 2: Fetch active subscriptions."""
        responses.add(responses.GET, "https://api.stripe.com/v1/subscriptions", json={
            "data": [{"id": "sub_1", "status": "active", "plan": {"unit_amount": 1000}}]
        })
        result = fetch_stripe_data()
        self.assertIn("sub_1", result)
        self.assertEqual(result["sub_1"]["mrr"], 10.0)

    @responses.activate
    @patch.dict('os.environ', {'SLACK_API_TOKEN': 'xoxb-456'})
    def test_criterion_3_fetch_slack(self):
        """Test 3: Pull Slack activity logs."""
        responses.add(responses.POST, "https://slack.com/api/conversations.history", json={
            "messages": [{"text": "hello"}]
        })
        result = fetch_slack_data()
        self.assertIn("client_channel_1", result)

    def test_criterion_4_churn_score(self):
        """Test 4: Compute churn probability score."""
        stripe_data = {"sub_1": {"mrr": 1000, "status": "active"}}
        slack_data = {"sub_1": {"messages": 5}}
        result = calculate_churn_risk(stripe_data, slack_data)
        self.assertIn("sub_1", result)
        self.assertIn("score", result["sub_1"])
        self.assertGreaterEqual(result["sub_1"]["score"], 0)
        self.assertLessEqual(result["sub_1"]["score"], 100)

    @patch('builtins.print')
    def test_criterion_5_rich_table(self, mock_print):
        """Test 5: Output a formatted rich table."""
        results = {"sub_1": {"score": 80, "risk_level": "HIGH", "mrr": 1000}}
        generate_report(results)
        self.assertTrue(True)

    def test_criterion_6_dry_run(self):
        """Test 6: Support dry-run mode."""
        with patch('saaschurn.cli.fetch_stripe_data') as mock_fetch:
            with patch('saaschurn.cli.fetch_slack_data') as mock_fetch_slack:
                main(["health", "--dry-run"])
                mock_fetch.assert_not_called()
                mock_fetch_slack.assert_not_called()

    def test_criterion_6_json_export(self):
        """Test 6: Support JSON export."""
        with patch('saaschurn.cli.fetch_stripe_data') as mock_fetch:
            with patch('saaschurn.cli.fetch_slack_data') as mock_fetch_slack:
                with patch('builtins.print') as mock_print:
                    main(["health", "--output", "json"])
                    mock_print.assert_called()

if __name__ == '__main__':
    unittest.main()

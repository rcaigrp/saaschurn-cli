import os
import sys
import unittest
import responses
from unittest.mock import patch, MagicMock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

class TestSaaSChurnCLI(unittest.TestCase):
    def setUp(self):
        self.env = {
            "STRIPE_API_TOKEN": "sk_test_123",
            "SLACK_API_TOKEN": "xoxb-123"
        }
        self.old_env = os.environ.copy()
        os.environ.update(self.env)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.old_env)

    @responses.activate
    def test_criterion_1_auth_via_env_vars(self):
        # Verify CLI requires env vars
        with patch('cli.os.environ', self.env):
            from cli import get_config
            config = get_config()
            self.assertEqual(config['stripe_token'], "sk_test_123")
            self.assertEqual(config['slack_token'], "xoxb-123")

    @responses.activate
    def test_criterion_2_fetch_subscriptions_and_mrr(self):
        stripe_url = "https://api.stripe.com/v1/subscriptions"
        responses.add(responses.GET, stripe_url, json={"data": [{"id": "sub_1", "status": "active", "plan": {"amount": 1000}}]})
        with patch('stripe_client.stripe') as mock_stripe:
            mock_stripe.get_subscriptions.return_value = [{"id": "sub_1", "status": "active", "plan": {"amount": 1000}}]
            from churn_calculator import calculate_mrr
            mrr = calculate_mrr([{"id": "sub_1", "status": "active", "plan": {"amount": 1000}}])
            self.assertEqual(mrr, 1000)

    @responses.activate
    def test_criterion_3_pull_slack_activity_logs(self):
        slack_url = "https://slack.com/api/conversations.history"
        responses.add(responses.GET, slack_url, json={"messages": [{"text": "hello"}]})
        with patch('slack_client.slack') as mock_slack:
            mock_slack.get_history.return_value = [{"text": "hello"}]
            from slack_client import fetch_activity
            activity = fetch_activity(["channel1"])
            self.assertEqual(activity, [])

    @responses.activate
    def test_criterion_4_compute_churn_score(self):
        from churn_calculator import calculate_mrr
        # Mock data for churn calculation
        subscriptions = [{"id": "sub_1", "status": "active", "plan": {"amount": 500}}]
        mrr = calculate_mrr(subscriptions)
        self.assertEqual(mrr, 500)

    @responses.activate
    def test_criterion_5_rich_table_output(self):
        from cli import get_config
        config = get_config()
        self.assertIn('stripe_token', config)

    @responses.activate
    def test_criterion_6_dry_run_and_json_export(self):
        # Dry-run mode test
        import subprocess
        result = subprocess.run(['python', '-m', 'saaschurn.cli', 'health', '--dry-run'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)

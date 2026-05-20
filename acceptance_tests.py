import sys
import unittest
from unittest.mock import patch, MagicMock
import responses
from saaschurn.stripe_client import fetch_active_subscriptions, calculate_mrr
from saaschurn.slack_client import fetch_channel_activity
from saaschurn.churn_calculator import compute_churn_score
from saaschurn.cli import main
import json

class TestStripeClient(unittest.TestCase):
    @patch('saaschurn.stripe_client.stripe')
    def test_fetch_active_subscriptions(self, mock_stripe):
        mock_stripe.Subscription.list.return_value = MagicMock(data=[{'plan': {'amount': 1000}}])
        result = fetch_active_subscriptions("fake_key")
        self.assertEqual(result[0]['plan']['amount'], 1000)

    def test_calculate_mrr(self):
        subs = [{'plan': {'amount': 1000}, 'status': 'active'}]
        self.assertEqual(calculate_mrr(subs), 10)

class TestSlackClient(unittest.TestCase):
    @responses.activate
    def test_fetch_channel_activity(self):
        responses.add(responses.GET, "https://slack.com/api/conversations.history", json={'messages': []})
        result = fetch_channel_activity("fake_token", ["C123"])
        self.assertIn("C123", result)

class TestChurnCalculator(unittest.TestCase):
    def test_compute_churn_score(self):
        self.assertEqual(compute_churn_score(500, {}), 1.0)

class TestCLI(unittest.TestCase):
    @patch('sys.argv', ['cli', '--dry-run'])
    def test_dry_run(self):
        with patch('saaschurn.cli.console') as mock_console:
            main()
            self.assertTrue(mock_console.print.called)

    @patch('sys.argv', ['cli', '--output', 'json'])
    @patch('saaschurn.cli.fetch_active_subscriptions')
    @patch('saaschurn.cli.fetch_channel_activity')
    @patch('saaschurn.cli.compute_churn_score')
    def test_json_output(self, mock_score, mock_activity, mock_subs):
        mock_subs.return_value = [{'plan': {'amount': 1000}}]
        mock_activity.return_value = {'C123': {'messages': []}}
        mock_score.return_value = 0.5
        import io
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        self.assertIn('mrr', captured_output.getvalue())

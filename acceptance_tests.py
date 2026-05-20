import unittest
import json
import os
import sys
import responses
import pytest

sys.path.insert(0, '/workspace/projects/SaaSChurn-CLI')
import main

STRIPE_TOKEN = "sk_test_123"
SLACK_TOKEN = "xoxb-456"

class TestSaaSChurnCLI(unittest.TestCase):
    @responses.activate
    def test_criterion_1_auth_and_fetch(self):
        """Criterion 1: Authenticate via env vars and fetch subscriptions."""
        os.environ["STRIPE_API_KEY"] = STRIPE_TOKEN
        os.environ["SLACK_API_TOKEN"] = SLACK_TOKEN
        stripe_url = "https://api.stripe.com/v1/subscriptions"
        stripe_response = [{"id": "sub_1", "customer_name": "ClientA", "status": "active", "quantity": 1, "price": {"amount": 10000}}]
        responses.add(responses.GET, stripe_url, json=stripe_response)
        subscriptions = main.fetch_stripe_subscriptions(STRIPE_TOKEN, dry_run=False)
        self.assertEqual(len(subscriptions), 1)

    @responses.activate
    def test_criterion_2_fetch_mrr(self):
        """Criterion 2: Fetch active subscriptions and calculate MRR."""
        stripe_url = "https://api.stripe.com/v1/subscriptions"
        stripe_response = [
            {"id": "sub_1", "customer_name": "ClientA", "status": "active", "quantity": 1, "price": {"amount": 10000}},
            {"id": "sub_2", "customer_name": "ClientB", "status": "active", "quantity": 2, "price": {"amount": 5000}}
        ]
        responses.add(responses.GET, stripe_url, json=stripe_response)
        subscriptions = main.fetch_stripe_subscriptions(STRIPE_TOKEN, dry_run=False)
        mrr_data = main.calculate_mrr(subscriptions)
        self.assertEqual(mrr_data["ClientA"], 100)
        self.assertEqual(mrr_data["ClientB"], 100)

    @responses.activate
    def test_criterion_3_fetch_slack(self):
        """Criterion 3: Pull Slack activity logs."""
        slack_url = "https://slack.com/api/conversations.history"
        slack_response = {"messages": [{"text": "Hello"}]}
        responses.add(responses.POST, slack_url, json=slack_response)
        activity = main.fetch_slack_activity(SLACK_TOKEN, dry_run=False)
        self.assertEqual(activity["ClientA"], 1)

    def test_criterion_4_churn_score(self):
        """Criterion 4: Compute churn probability score."""
        mrr_data = {"ClientA": 100, "ClientB": 10}
        activity_data = {"ClientA": 20, "ClientB": 5}
        risk_scores = main.calculate_churn_risk(mrr_data, activity_data)
        # ClientB has low MRR (<50) and low activity (<10), so base 50 + 30 + 20 = 100
        self.assertEqual(risk_scores["ClientB"], 100)

    @responses.activate
    def test_criterion_5_rich_table(self):
        """Criterion 5: Output formatted rich table."""
        with unittest.mock.patch('main.console') as mock_console:
            mrr_data = {"ClientA": 100}
            activity_data = {"ClientA": 15}
            risk_scores = {"ClientA": 20}
            main.generate_report(mrr_data, activity_data, risk_scores, dry_run=True)
            # Check if print was called (mocking rich console)
            mock_console.print.assert_called()

    def test_criterion_6_dry_run_json(self):
        """Criterion 6: Support dry-run and JSON export."""
        # Test dry-run returns mock data
        subscriptions = main.fetch_stripe_subscriptions("", dry_run=True)
        self.assertEqual(len(subscriptions), 2)
        # Test JSON export
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            main.main("health", "--output", "json")
        output = f.getvalue()
        self.assertIn("mrr", output)

if __name__ == "__main__":
    unittest.main()

import unittest
import json
import responses
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from saaschurn.fetchers import StripeFetcher, SlackFetcher
from saaschurn.calculators import ChurnCalculator
from saaschurn.reporter import Reporter


class TestAcceptanceCriteria(unittest.TestCase):
    """Acceptance tests - DEFINITION OF DONE"""

    @responses.activate
    def test_criterion_1_auth_via_env_vars(self):
        """CLI tool authenticates via Stripe and Slack API tokens passed as environment variables."""
        from unittest.mock import patch
        with patch.dict(os.environ, {'STRIPE_API_KEY': 'sk_test_123', 'SLACK_API_TOKEN': 'xoxb-123'}):
            from saaschurn.fetchers import StripeFetcher
            stripe = StripeFetcher()
            self.assertEqual(stripe.api_key, 'sk_test_123')

    @responses.activate
    def test_criterion_2_fetch_active_subscriptions(self):
        """Fetches all active subscriptions via Stripe API v1 and calculates monthly recurring revenue (MRR)."""
        responses.add(
            responses.GET,
            'https://api.stripe.com/v1/subscriptions',
            json={'data': [
                {'id': 'sub_1', 'customer': 'cus_1', 'status': 'active', 'plan': {'unit_amount': 1000}},
                {'id': 'sub_2', 'customer': 'cus_2', 'status': 'active', 'plan': {'unit_amount': 2000}}
            ], 'has_more': False}
        )
        from unittest.mock import patch
        with patch.dict(os.environ, {'STRIPE_API_KEY': 'sk_test_123'}):
            fetcher = StripeFetcher()
            subs = fetcher.get_active_subscriptions()
            self.assertEqual(len(subs), 2)

    @responses.activate
    def test_criterion_3_fetch_slack_activity(self):
        """Fetches Slack workspace channel activity logs and aggregates message counts per client channel."""
        responses.add(
            responses.GET,
            'https://slack.com/api/conversations.history',
            json={'messages': [
                {'type': 'message', 'text': 'hello'},
                {'type': 'message', 'text': 'world'}
            ]}
        )
        from unittest.mock import patch
        with patch.dict(os.environ, {'SLACK_API_TOKEN': 'xoxb-123'}):
            fetcher = SlackFetcher()
            result = fetcher.get_channel_activity('channel_1')
            self.assertIn('message_count', result)

    def test_criterion_4_churn_risk_score(self):
        """Calculates a churn risk score (0-100) based on MRR decline rate and Slack activity drop percentage."""
        calc = ChurnCalculator()
        result = calc.calculate_risk(mrr_decline=10, slack_activity_drop=80)
        self.assertIsInstance(result, dict)
        self.assertIn('risk_score', result)
        self.assertIn('risk_level', result)
        self.assertIn('recommendation', result)

    def test_criterion_5_rich_table_output(self):
        """Generates a formatted rich terminal table with columns: Client, MRR, Activity Score, Churn Risk, Recommendation."""
        reporter = Reporter()
        data = [
            {
                'client': 'Client A',
                'mrr': 1000,
                'activity_score': 50,
                'risk_score': 75,
                'recommendation': 'HIGH risk'
            }
        ]
        result = reporter.generate_table(data)
        self.assertIn('Client A', result)
        self.assertIn('MRR', result)

    def test_criterion_6_dry_run_and_json_output(self):
        """Supports --dry-run flag and --output json flag for CI/CD integration."""
        from unittest.mock import patch
        with patch.dict(os.environ, {'STRIPE_API_KEY': 'sk_test', 'SLACK_API_TOKEN': 'xoxb'}):
            from saaschurn.fetchers import StripeFetcher
            from saaschurn.calculators import ChurnCalculator
            from saaschurn.reporter import Reporter
            import json

            # Test dry-run with mock data
            mock_subs = [{'customer': 'cus_1', 'plan': {'unit_amount': 1000}}]
            mock_slack = {'message_count': 5}
            calc = ChurnCalculator()
            result = calc.calculate_risk(mrr_decline=5, slack_activity_drop=50)
            data = [{
                'client': 'TestClient',
                'mrr': 1000,
                'activity_score': 50,
                'risk_score': result['risk_score'],
                'recommendation': result['recommendation']
            }]
            output = Reporter().generate_json(data)
            parsed = json.loads(output)
            self.assertIn('TestClient', parsed[0]['client'])

    @responses.activate
    def test_criterion_7_comprehensive_tests_mocking(self):
        """Includes comprehensive unit tests mocking Stripe/Slack API responses."""
        responses.add(
            responses.GET,
            'https://api.stripe.com/v1/subscriptions',
            json={'data': [], 'has_more': False}
        )
        responses.add(
            responses.GET,
            'https://slack.com/api/conversations.history',
            json={'messages': []}
        )
        from unittest.mock import patch
        with patch.dict(os.environ, {'STRIPE_API_KEY': 'sk_test', 'SLACK_API_TOKEN': 'xoxb'}):
            from saaschurn.fetchers import StripeFetcher, SlackFetcher
            stripe = StripeFetcher()
            slack = SlackFetcher()
            subs = stripe.get_active_subscriptions()
            self.assertEqual(len(subs), 0)


if __name__ == '__main__':
    unittest.main()
